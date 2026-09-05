#!/usr/bin/env python3
"""Probe what a VLM can ground in fixed-camera intersection footage.

query mode: locate described situations. open mode: report events unprompted.
One run, one directory (summary.md, results.jsonl, run.json); a run never
appends to another run's rows.

  python scripts/vlm_probe.py videos/<clip>.mp4 \
      --queries queries/events-key.txt --fps 1 --batch-queries --samples 5
  python scripts/vlm_probe.py videos/<clip>.mp4 --dry-run   # render only, no API
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.env import key_status, load_env, require_key
from utils.render import fit, overview_grid, stamp
from utils.schema import BatchQueryResult, QueryResult, WindowResult
from utils.video import extract, probe, windows
from utils.vlm import (CHANNELS, DEFAULT_ENCODING, SYSTEM_OPEN, SYSTEM_QUERY,
                       batch_query_prompt, get_backend, open_prompt,
                       parse_encoding, query_prompt, with_scene)


def fmt(t):
    return f"{int(t) // 3600:d}:{int(t) // 60 % 60:02d}:{t % 60:05.2f}"


def sample_overview(video, start, end, every):
    thumbs, t = [], start
    while t < end:
        got = extract(video, t, t + min(1.0, every), 1.0)
        if got:
            thumbs.append(got[0])
        t += every
    return thumbs


def slug(text):
    """Filesystem- and shell-safe directory component."""
    text = re.sub(r"[^a-z0-9._-]+", "-", text.lower())
    return re.sub(r"-{2,}", "-", text).strip("-.") or "run"


def clip_tag(video):
    """Shortest thing that identifies which recording this was.

    The date and time in the filename are what distinguish one clip from
    another; the camera name is the same for all of them and carries nothing.
    """
    stem = Path(video).stem
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})_T-(\d{2})_(\d{2})", stem)
    return f"{m.group(2)}{m.group(3)}-{m.group(4)}{m.group(5)}" if m else slug(stem)[:16]


def run_label(a):
    """Directory name that says what was run, readable without opening it.

    A directory called `20260829-214844-scene` tells you when it ran and
    nothing about what it was. The condition goes first and the timestamp last:
    the timestamp is only there to keep two runs of the same configuration
    apart, and it is the least interesting thing about a run.
    """
    if a.name:
        return slug(a.name)
    base = Path(a.queries).stem if a.queries else ("query" if a.query else "open")
    parts = [base, clip_tag(a.video), f"fps{a.fps:g}"]
    if getattr(a, "samples", 1) > 1:
        parts.append(f"n{a.samples}")
    if getattr(a, "batch_queries", False):
        parts.append("batch")
    if getattr(a, "scene", None):
        parts.append("scene")
    if a.window:
        parts.append(f"win{a.window:g}")
    return slug("_".join(parts))


def link_frames(run_dir, frames_dir):
    """A `frames` symlink inside the run directory.

    The frames are the evidence for every claim in summary.md, and they live
    outside the run directory because they are large and disposable while the summary
    is neither. The link keeps them one hop away instead of one path guess.
    """
    link = run_dir / "frames"
    try:
        if link.is_symlink() or link.exists():
            return
        link.symlink_to(os.path.relpath(frames_dir.resolve(), run_dir.resolve()))
    except OSError:
        pass  # a filesystem without symlinks costs a convenience, not a result


def render_frame(t, img, enc):
    """One frame as the model will receive it: (label, image).

    The label is the interleaved text block that precedes this image, or None
    when that channel is off; the burnt-in caption is a separate channel, so
    both, either or neither can be in play.
    """
    label = f"t={t:.2f}s" if "interleave" in enc else None
    return label, fit(stamp(img, f"t={t:.2f}s") if "burn" in enc else img)


def save_frames(frames, out_dir, tag, enc):
    """Persist exactly what the model is shown.

    When a probe misses something the first question is whether the evidence
    was legible at all, so this is written whether or not a call is made. It
    follows `enc`, so with the burn channel off these files are the bare
    pixels the model got -- the timestamp is still in the filename, where a
    person can read it and the model cannot.
    """
    d = Path(out_dir) / tag
    d.mkdir(parents=True, exist_ok=True)
    for t, img in frames:
        render_frame(t, img, enc)[1].save(d / f"{t:08.2f}.jpg", quality=88)
    return d


def append_jsonl(path, rec):
    """Persist one record the moment it exists.

    Batching writes until the end of a window means a single failed call
    discards every answer already paid for.
    """
    with path.open("a") as fh:
        fh.write(json.dumps(rec) + "\n")


def write_summary(path, a, info, plan, mode, results, usages,
                  backend, frames_dir, failures=()):
    """A readable record of one run.

    The terminal output scrolls away and the jsonl is for machines; this is the
    file a person opens next week to remember what was asked and what came
    back, so it records the parameters alongside the answers -- a verdict
    without its fps and model is not interpretable.
    """
    L = []
    w = L.append
    w(f"# probe run: {path.parent.name}\n")
    w(f"- clip: `{a.video}`")
    w(f"- range: {a.start:.0f}s - {plan[-1][1]:.0f}s "
      f"({info['width']}x{info['height']}, vfr={info['likely_vfr']})")
    w(f"- timestamps: `{a.time_encoding}` "
      f"(channels: {', '.join(CHANNELS)}, or none)")
    w(f"- fps: {a.fps:g} | "
      f"{'windows of ' + format(a.window, 'g') + 's' if a.window else 'whole range, one call'}")
    w(f"- frames per call: {len(plan[0][3])} | model: {backend.model} "
      f"(resolution={getattr(backend, 'resolution', '-')}, "
      f"thinking={getattr(backend, 'thinking_level', '-')})")
    w(f"- frames written to `{frames_dir}`\n")

    if mode == "query":
        # group by query, so repeated samples of one query stay together and a
        # split verdict is visible as a split rather than averaged into a rate
        per_q = {}
        for r in results:
            per_q.setdefault((r["axis"], r["query"]), []).append(bool(r["matches"]))
        axes = {}
        for (ax, _), hits in per_q.items():
            d = axes.setdefault(ax, {"q": 0, "all": 0, "none": 0, "split": 0})
            d["q"] += 1
            d["all"] += all(hits)
            d["none"] += not any(hits)
            d["split"] += (any(hits) and not all(hits))
        nsamp = max(len(v) for v in per_q.values()) if per_q else 1
        w("## by axis\n")
        if nsamp > 1:
            w(f"{nsamp} samples per query. **split** = the samples disagreed with "
              f"each other, so that query has no stable answer on these frames "
              f"and must not be counted either way.\n")
        w("| axis | all samples present | all absent | split | note |")
        w("|---|---|---|---|---|")
        for ax in sorted(axes):
            d = axes[ax]
            note = ("**a hit here is a fabrication**"
                    if ax == "negative" and d["all"] else
                    "ground truth known: all absent" if ax == "negative" else "")
            w(f"| {ax} | {d['all']}/{d['q']} | {d['none']}/{d['q']} | "
              f"{d['split']}/{d['q']} | {note} |")
        w("")
        split = [f"{ax} — {q[:60]}" for (ax, q), h in per_q.items()
                 if any(h) and not all(h)]
        if split:
            w("### queries whose samples disagreed\n")
            for line in split:
                w(f"- {line}")
            w("")
        w("## per query\n")
        for r in results:
            tag = f" (sample {r['sample']})" if r.get("sample") and nsamp > 1 else ""
            w(f"### [{r['axis']}] {r['query']}{tag}\n")
            if r["matches"]:
                for m in r["matches"]:
                    w(f"- **match** `{m['match_quality']}` / conf "
                      f"`{m['confidence']}` at "
                      f"{m['t_start_sec']:.1f}-{m['t_end_sec']:.1f}s "
                      f"(clearest {m['clearest_frame_sec']:.1f}s)")
                    w(f"  - subject: {m['subject']}")
                    w(f"  - {m['what_happens']}")
            else:
                w("- **absent**")
                if r["why_not_found"]:
                    w(f"  - why not: {r['why_not_found']}")
            if r["considered_and_rejected"]:
                w(f"- ruled out: {r['considered_and_rejected']}")
            if r["unreadable_reasons"]:
                w(f"- unreadable: {'; '.join(r['unreadable_reasons'])}")
            w("")
    else:
        for r in results:
            w(f"## window {r['window'][0]:.0f}-{r['window'][1]:.0f}s\n")
            w(f"- signal face visible: {r['signal_head_visible']}")
            w(f"- {r['scene_notes']}\n")
            for e in r["events"]:
                w(f"- **{e['event_type']}** [{e['confidence']}] "
                  f"{e['t_start_sec']:.1f}-{e['t_end_sec']:.1f}s")
                w(f"  - {e['what_happened']}")
                w(f"  - signal: {e['signal_state_claimed']} "
                  f"(`{e['signal_state_basis']}`)")
            w("")

    if failures:
        w("## failed calls\n")
        for f in failures:
            w(f"- [{f['axis']}] {f['query']}\n  - `{f['error']}`")
        w("")
    tin = sum(u["in"] or 0 for u in usages)
    tout = sum(u["out"] or 0 for u in usages)
    w(f"---\n\n{len(usages)} call(s) ok, {len(failures)} failed, "
      f"{tin} in / {tout} out tokens")
    path.write_text("\n".join(L))


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("--query", help="one situation to locate")
    p.add_argument("--queries", help="file of situations, one per line as "
                                     "'axis | situation' (# comments ignored)")
    p.add_argument("--axis", help="only run queries on these axes, "
                                  "comma-separated. e.g. --axis negative")
    p.add_argument("--start", type=float, default=0.0)
    p.add_argument("--end", type=float, default=None)
    p.add_argument("--window", type=float, default=None,
                   help="split into windows of this many seconds. Default is "
                        "one window over the whole range: a clip is 3 minutes, "
                        "which fits in context, and asking where in the clip a "
                        "situation occurs is a stronger test of localisation "
                        "than asking whether it is in each 8-second slice")
    p.add_argument("--overlap", type=float, default=3.0,
                   help="window overlap, only used with --window")
    p.add_argument("--fps", type=float, default=1.0,
                   help="frames sampled per second within a window. Raise for "
                        "situations that turn on a fast moment")
    p.add_argument("--min-frames", type=int, default=2,
                   help="skip windows with fewer frames; one frame shows no motion")
    p.add_argument("--time-encoding", default=DEFAULT_ENCODING,
                   help="how each frame's timestamp reaches the model, as a "
                        "comma-separated subset of "
                        f"{','.join(CHANNELS)} (or 'none'). 'burn' draws it "
                        "into the pixels, 'list' names every timestamp in one "
                        "text block, 'interleave' puts one timestamp block "
                        "immediately before its own frame. The channels are "
                        "independent and this is worth an ablation: change "
                        f"one at a time. Default '{DEFAULT_ENCODING}'")
    p.add_argument("--batch-queries", action="store_true",
                   help="all queries in one call: frames sent once instead of once per query; queries stop being independent")
    p.add_argument("--samples", type=int, default=1,
                   help="independent answers per query; each is its own call, so cost scales with N")
    p.add_argument("--scene", default=None,
                   help="scene facts for the system prompt (see build_scene.py); run a no-scene arm too")
    p.add_argument("--backend", choices=["gemini", "claude"], default="gemini")
    p.add_argument("--model", default=None)
    p.add_argument("--max-output-tokens", type=int, default=32000,
                   help="output budget per call. Thinking is drawn from the "
                        "same budget, so too low a value returns an empty body")
    p.add_argument("--env", default=None)
    p.add_argument("--name", default=None,
                   help="label for this run, used in its directory name. "
                        "Default is composed from the query set and fps "
                        "so an ablation loop separates itself")
    p.add_argument("--results-root", default="experiment_results/adhoc",
                   help="parent of the per-run directories. Experiments name "
                        "their own arm directories with --run-dir; this is "
                        "where a one-off run lands")
    p.add_argument("--run-dir", default=None,
                   help="use exactly this directory instead of composing "
                        "<results-root>/<label>_<time>. Overrides --name")
    p.add_argument("--out", default=None,
                   help="where rendered frames go (large; gitignored). "
                        "Default runs/<run directory name>, so frames and "
                        "findings carry the same name. They are kept apart "
                        "because the findings are worth keeping and reading "
                        "while the frames are working material")
    p.add_argument("--overview", help="write a thumbnail grid here and exit")
    p.add_argument("--overview-every", type=float, default=60.0)
    p.add_argument("--dry-run", action="store_true",
                   help="render what would be sent; make no API calls")
    return p.parse_args()


def load_queries(a):
    """-> [(axis, text)]. File lines are 'axis | query', axis optional."""
    if a.queries:
        out = []
        for ln in Path(a.queries).read_text().splitlines():
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            axis, sep, text = ln.partition("|")
            out.append((axis.strip(), text.strip()) if sep
                       else ("unspecified", ln))
        if a.axis:
            want = {x.strip() for x in a.axis.split(",")}
            out = [(ax, q) for ax, q in out if ax in want]
            if not out:
                sys.exit(f"no queries on axis {a.axis} in {a.queries}")
        if not out:
            sys.exit(f"no queries in {a.queries}")
        return out
    return [("unspecified", a.query)] if a.query else []


def main():
    a = parse_args()
    try:
        enc = parse_encoding(a.time_encoding)
    except ValueError as e:
        sys.exit(str(e))
    # normalised, so the record says what ran rather than how it was typed
    a.time_encoding = ",".join(sorted(enc)) or "none"
    started = datetime.now()

    scene = Path(a.scene).read_text() if a.scene else ""
    if a.scene:
        print(f"scene context: {a.scene} ({len(scene.split())} words)")
    sys_open, sys_query = with_scene(SYSTEM_OPEN, scene), with_scene(SYSTEM_QUERY, scene)

    info = probe(a.video)
    print(json.dumps(info, indent=2))
    if info["likely_vfr"]:
        print("\n!! variable frame rate -- timestamps below come from PTS, "
              "never from frame index\n", file=sys.stderr)
    end = a.end if a.end is not None else (info["duration_s"] or 0.0)

    if a.overview:
        thumbs = sample_overview(a.video, a.start, end, a.overview_every)
        if not thumbs:
            sys.exit("no frames sampled")
        Path(a.overview).parent.mkdir(parents=True, exist_ok=True)
        overview_grid(thumbs).save(a.overview, quality=85)
        print(f"\n{len(thumbs)} thumbnails -> {a.overview}")
        return

    if end <= a.start:
        sys.exit(f"nothing to probe: start={a.start} end={end}")

    queries = load_queries(a)
    mode = "query" if queries else "open"
    print(f"\nmode: {mode}" + (f"  ({len(queries)} quer"
          f"{'y' if len(queries) == 1 else 'ies'})" if queries else ""))

    # One run, one directory. The timestamp makes the name unique without the
    # caller having to remember one, which is what previously turned two runs
    # of the same command into a single jsonl with no way to separate them.
    run_dir = (Path(a.run_dir) if a.run_dir else
               Path(a.results_root) / f"{run_label(a)}_{started:%m%d-%H%M}")
    out = Path(a.out) if a.out else Path("runs") / run_dir.name
    out.mkdir(parents=True, exist_ok=True)
    jsonl_path = run_dir / "results.jsonl"
    md_path = run_dir / "summary.md"
    cfg_path = run_dir / "run.json"

    backend = None
    if not a.dry_run:
        env_file = load_env(a.env)
        require_key(a.backend)
        backend = get_backend(a.backend, a.model)
        print(f"backend: {backend.name} / {backend.model}  "
              f"[{key_status(a.backend)}]")

    # frames are decoded once and reused across every query in the batch
    spans = (windows(a.start, end, a.window, a.overlap) if a.window
             else [(a.start, end)])
    plan = []
    for t0, t1 in spans:
        frames = extract(a.video, t0, t1, a.fps)
        if len(frames) < a.min_frames:
            continue
        tag = f"{t0:07.2f}-{t1:07.2f}"
        save_frames(frames, out, tag, enc)
        plan.append((t0, t1, tag, frames))
    if not plan:
        sys.exit("no usable windows")

    span = f"{a.window:g}s each" if a.window else \
           f"whole range, {plan[0][1] - plan[0][0]:.0f}s"
    nframes = sum(len(f) for *_, f in plan)
    print(f"{len(plan)} window(s), {span}, {a.fps:g} fps, {nframes} frames "
          f"total, timestamps: {a.time_encoding}")
    if a.dry_run:
        print(f"\nframes -> {out}\nopen them: if you cannot resolve the "
              f"situation yourself, the model cannot either.")
        return

    # Appending to a directory that already holds answers silently merges two
    # runs into one jsonl, and a comparison between conditions is worthless if
    # it cannot be told which rows came from which.
    if (run_dir / "results.jsonl").exists():
        sys.exit(f"{run_dir}/results.jsonl already exists.\n"
                 f"  A run never appends to another run's rows. Move it aside, "
                 f"or point --run-dir somewhere else.")
    run_dir.mkdir(parents=True, exist_ok=True)
    link_frames(run_dir, out)
    # Written before the first call, not after the last: a run that dies
    # halfway still leaves a directory that says what it was trying to do.
    cfg = {
        "run": run_dir.name,
        "started": started.isoformat(timespec="seconds"),
        "mode": mode,
        "clip": a.video,
        "video": info,
        "range_sec": [a.start, plan[-1][1]],
        "window_sec": a.window,
        "overlap_sec": a.overlap if a.window else None,
        "fps": a.fps,
        "time_encoding": a.time_encoding,
        "backend": backend.name,
        "model": backend.model,
        "resolution": getattr(backend, "resolution", None),
        "thinking_level": getattr(backend, "thinking_level", None),
        "max_output_tokens": a.max_output_tokens,
        "scene_file": a.scene,
        "scene_words": len(scene.split()),
        "queries_file": a.queries,
        "axis_filter": a.axis,
        "samples_per_query": a.samples,
        "batch_queries": a.batch_queries,
        "n_queries": len(queries),
        "n_windows": len(plan),
        "n_frames": nframes,
        "frames_dir": str(out),
    }
    cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")

    results, usages, failures = [], [], []
    for t0, t1, tag, frames in plan:
        payload = [render_frame(t, img, enc) for t, img in frames]

        if mode == "open":
            res, usage = backend.run(sys_open, payload,
                                     open_prompt(frames, t0, t1, enc),
                                     WindowResult, a.max_output_tokens)
            usages.append(usage)
            rec = {"window": [t0, t1], "mode": "open",
                   "time_encoding": a.time_encoding, **res.model_dump()}
            results.append(rec)
            append_jsonl(jsonl_path, rec)
            flag = "" if res.signal_head_visible else "  [no signal face visible]"
            print(f"\n{tag}  {len(res.events)} event(s){flag}")
            for e in res.events:
                print(f"  - {e.event_type} [{e.confidence}] "
                      f"{e.t_start_sec:.1f}-{e.t_end_sec:.1f}s  "
                      f"signal={e.signal_state_claimed} ({e.signal_state_basis})")
                print(f"    {e.what_happened}")
        else:
            if a.batch_queries:
                for sample in range(1, a.samples + 1):
                    try:
                        res, usage = backend.run(
                            sys_query, payload,
                            batch_query_prompt(frames, t0, t1, queries, enc),
                            BatchQueryResult, a.max_output_tokens)
                    except Exception as e:
                        failures.append({"axis": "*batch*", "query": f"all {len(queries)}",
                                         "sample": sample,
                                         "error": f"{type(e).__name__}: {e}"})
                        print(f"\nbatch s{sample}  FAILED  {type(e).__name__}: {str(e)[:140]}")
                        # The first sample failing after the whole backoff
                        # schedule means the quota will not clear inside this
                        # run. Every later sample would repeat the same ~16
                        # minutes of waiting to reach the same answer, so stop
                        # rather than spend an hour proving it.
                        if sample == 1:
                            print("  first sample exhausted its retries -- "
                                  "aborting rather than repeating the wait for "
                                  "every remaining sample")
                            break
                        continue
                    usages.append(usage)
                    got = {ans.query_index for ans in res.answers}
                    missing = [i for i in range(len(queries)) if i not in got]
                    if missing:
                        # A batched call that silently drops a query would look
                        # like "absent" downstream, which is a different claim.
                        print(f"\n!! batch s{sample}: {len(missing)} quer"
                              f"{'y' if len(missing)==1 else 'ies'} not answered "
                              f"-- indices {missing}. Recorded as failures, not as absent.")
                        for i in missing:
                            failures.append({"axis": queries[i][0], "query": queries[i][1],
                                             "sample": sample, "error": "not answered in batch"})
                    print(f"\n--- batch sample {sample} ---")
                    for ans in sorted(res.answers, key=lambda x: x.query_index):
                        if not 0 <= ans.query_index < len(queries):
                            print(f"  !! query_index {ans.query_index} out of range, dropped")
                            continue
                        axis, q = queries[ans.query_index]
                        d = ans.model_dump(); d.pop("query_index", None)
                        rec = {"window": [t0, t1], "mode": "query",
                               "time_encoding": a.time_encoding,
                               "query_index": ans.query_index, "sample": sample,
                               "batched": True, "axis": axis, "query": q, **d}
                        results.append(rec)
                        append_jsonl(jsonl_path, rec)
                        mark = "  <-- FABRICATED" if (ans.matches and axis == "negative") else ""
                        print(f"  [{axis}] {'MATCH' if ans.matches else 'absent'}{mark}"
                              f"  {q[:52]}")
                        for m in ans.matches:
                            print(f"      {m.t_start_sec:.1f}-{m.t_end_sec:.1f}s "
                                  f"(clearest {m.clearest_frame_sec:.1f}s)  {m.subject}")
                continue

            for qi, (axis, q) in enumerate(queries):
                print(f"\n[{axis}] {q[:64]}")
                verdicts = []
                for sample in range(1, a.samples + 1):
                    try:
                        res, usage = backend.run(sys_query, payload,
                                                 query_prompt(frames, t0, t1, q, enc),
                                                 QueryResult, a.max_output_tokens)
                    except Exception as e:
                        # One bad call must not discard the answers already in
                        # hand. Record the failure as a row and keep going.
                        failures.append({"axis": axis, "query": q, "sample": sample,
                                         "error": f"{type(e).__name__}: {e}"})
                        append_jsonl(jsonl_path, {"window": [t0, t1], "mode": "query",
                                                  "time_encoding": a.time_encoding,
                                                  "query_index": qi, "sample": sample,
                                                  "axis": axis, "query": q,
                                                  "error": str(e)})
                        print(f"  s{sample}  FAILED  {type(e).__name__}: "
                              f"{str(e)[:140]}")
                        continue
                    usages.append(usage)
                    rec = {"window": [t0, t1], "mode": "query",
                           "time_encoding": a.time_encoding, "query_index": qi,
                           "sample": sample, "axis": axis, "query": q,
                           **res.model_dump()}
                    results.append(rec)
                    append_jsonl(jsonl_path, rec)
                    verdict = "MATCH" if res.matches else "absent"
                    verdicts.append(verdict)
                    mark = "  <-- FABRICATED" if (res.matches and axis == "negative") else ""
                    tag = f"  s{sample}" if a.samples > 1 else "  "
                    print(f"{tag}{verdict}{mark}")
                    for m in res.matches:
                        print(f"      [{m.match_quality}/{m.confidence}] "
                              f"{m.t_start_sec:.1f}-{m.t_end_sec:.1f}s "
                              f"(clearest {m.clearest_frame_sec:.1f}s)  {m.subject}")
                        print(f"      {m.what_happens}")
                    if not res.matches and res.why_not_found:
                        print(f"      why not: {res.why_not_found[:150]}")
                # Disagreement across samples is not a detail to average away:
                # it means the verdict for this query is a draw, not a reading.
                if len(set(verdicts)) > 1:
                    print(f"  !! samples DISAGREE: {'/'.join(verdicts)} "
                          f"-- this query has no stable answer on these frames")

    print("\n" + "=" * 60)
    if failures:
        print(f"{len(failures)} call(s) FAILED:")
        for f in failures:
            print(f"  [{f['axis']}] {f['query'][:50]}\n    {f['error'][:140]}")
        print()
    if not results:
        print("no successful calls")
        return
    if mode == "query":
        axes = {}
        for r in results:
            a_ = axes.setdefault(r["axis"], {"n": 0, "hit": 0, "qual": {}})
            a_["n"] += 1
            if r["matches"]:
                a_["hit"] += 1
                for m in r["matches"]:
                    a_["qual"][m["match_quality"]] = \
                        a_["qual"].get(m["match_quality"], 0) + 1
        print(f"{'axis':<14} {'answered present':>17}   match quality")
        print("-" * 60)
        for ax in sorted(axes):
            d = axes[ax]
            qual = ", ".join(f"{v} {k}" for k, v in sorted(d["qual"].items())) or "-"
            note = ""
            if ax == "negative" and d["hit"]:
                note = f"   <-- {d['hit']} FABRICATED"
            print(f"{ax:<14} {d['hit']:>8}/{d['n']:<8} {qual}{note}")

        neg = axes.get("negative")
        if neg:
            # The one score that needs no annotation: these did not happen, so
            # every hit is a fabrication and every miss is correct restraint.
            print(f"\nnegative controls: {neg['n'] - neg['hit']}/{neg['n']} "
                  f"correctly answered absent")
        sup = sum(1 for r in results for m in r["matches"]
                  if m["match_quality"] == "superficial")
        if sup:
            print(f"{sup} match(es) self-reported as superficial -- "
                  f"surface features, not the described situation")
    else:
        n = sum(len(r["events"]) for r in results)
        blind = sum(1 for r in results if not r["signal_head_visible"])
        inferred = sum(1 for r in results for e in r["events"]
                       if e["signal_state_basis"] != "read_directly")
        print(f"{len(results)} windows, {n} event(s)")
        print(f"  {blind}/{len(results)} windows had no legible signal face")
        print(f"  {inferred}/{n} events rest on a signal state not read directly")

    tin = sum(u["in"] or 0 for u in usages)
    tout = sum(u["out"] or 0 for u in usages)
    if tin:
        line = f"tokens: {tin} in / {tout} out"
        pin, pout = usages[0].get("price_in"), usages[0].get("price_out")
        line += (f"  ~= ${tin / 1e6 * pin + tout / 1e6 * pout:.2f}"
                 if pin and pout else "  (no pricing pinned for this backend)")
        print(line)
    write_summary(md_path, a, info, plan, mode, results, usages,
                  backend, out, failures)
    cfg.update({"finished": datetime.now().isoformat(timespec="seconds"),
                "calls_ok": len(usages), "calls_failed": len(failures),
                "tokens_in": tin, "tokens_out": tout})
    cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")
    print(f"\n-> {run_dir}/\n     summary.md  results.jsonl  run.json"
          f"\n   frames: {out}")


if __name__ == "__main__":
    main()
