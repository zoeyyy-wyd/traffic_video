#!/usr/bin/env python3
"""Probe what a VLM can ground in fixed-camera intersection footage.

Two modes over the same frames:

  query   give it a described situation; can it locate that, and say so when
          the situation is not there?  This is the experiment.
  open    give it no hint; what does it find on its own?

Every run gets its own directory under results/, named for when it ran and
what it ran, holding summary.md, results.jsonl and run.json. Nothing is ever
appended to a previous run's output.

  # look at what the model would receive -- no API call, no key needed
  python scripts/vlm_probe.py data/clip.mp4 --dry-run

  # a whole recording as one grid, for deriving real ROI coordinates
  python scripts/vlm_probe.py data/clip.mp4 --overview runs/overview.jpg

  # the query probe
  python scripts/vlm_probe.py data/clip.mp4 --start 40 --end 100 \
      --roi 0.28,0.00,0.40,0.42 \
      --query "a vehicle that entered the intersection and stopped partway
               because someone was crossing in front of it"

  # a batch of queries from a file, one per line -- the golden set turned
  # into an experiment.  Include queries for situations that did NOT occur:
  # a probe that never answers "absent" has not been tested.
  python scripts/vlm_probe.py data/clip.mp4 --queries queries.txt

  # open-ended, no query
  python scripts/vlm_probe.py data/clip.mp4 --start 40 --end 100

  # how the frames carry their timestamps -- an ablation, one channel at a
  # time. Each arm lands in its own run directory on its own.
  for enc in burn,list burn interleave burn,interleave; do
      python scripts/vlm_probe.py data/clip.mp4 --queries queries.txt \
          --time-encoding $enc --name "ts-${enc//,/-}"
  done

Deps: pip install -r requirements.txt
Keys: cp .env
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
from utils.render import (ROI_PRESETS, apply_roi, fit, overview_grid,
                          parse_roi, stamp)
from utils.schema import QueryResult, WindowResult
from utils.video import extract, probe, windows
from utils.vlm import (CHANNELS, DEFAULT_ENCODING, SYSTEM_OPEN, SYSTEM_QUERY,
                       get_backend, open_prompt, parse_encoding, query_prompt)


def fmt(t):
    return f"{int(t) // 3600:d}:{int(t) // 60 % 60:02d}:{t % 60:05.2f}"


def sample_overview(video, start, end, every, roi):
    thumbs, t = [], start
    while t < end:
        got = extract(video, t, t + min(1.0, every), 1.0)
        if got:
            thumbs.append((got[0][0], apply_roi(got[0][1], roi)))
        t += every
    return thumbs


def slug(text):
    """Filesystem- and shell-safe directory component."""
    text = re.sub(r"[^a-z0-9._-]+", "-", text.lower())
    return re.sub(r"-{2,}", "-", text).strip("-.") or "run"


def run_label(a):
    """The part of the run directory name that says what was run.

    Ablations are loops over one flag, so a name that does not carry the
    condition leaves a dozen directories distinguishable only by their
    timestamp. When the caller supplies --name they have said what matters;
    otherwise the varying levers -- query set, roi, fps -- go in the name.
    """
    if a.name:
        return slug(a.name)
    base = Path(a.queries).stem if a.queries else ("query" if a.query else "open")
    roi = a.roi if a.roi in ROI_PRESETS else "custom"
    return slug(f"{base}-roi-{roi}-fps{a.fps:g}")


def link_frames(run_dir, frames_dir):
    """A `frames` symlink inside the run directory.

    The frames are the evidence for every claim in summary.md, and they live
    outside results/ because they are large and disposable while the summary
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
    without its fps, roi and model is not interpretable.
    """
    L = []
    w = L.append
    w(f"# probe run: {path.parent.name}\n")
    w(f"- clip: `{a.video}`")
    w(f"- range: {a.start:.0f}s - {plan[-1][1]:.0f}s "
      f"({info['width']}x{info['height']}, vfr={info['likely_vfr']})")
    w(f"- timestamps: `{a.time_encoding}` "
      f"(channels: {', '.join(CHANNELS)}, or none)")
    w(f"- roi: `{a.roi}` | fps: {a.fps:g} | "
      f"{'windows of ' + format(a.window, 'g') + 's' if a.window else 'whole range, one call'}")
    w(f"- frames per call: {len(plan[0][3])} | model: {backend.model} "
      f"(resolution={getattr(backend, 'resolution', '-')}, "
      f"thinking={getattr(backend, 'thinking_level', '-')})")
    w(f"- frames written to `{frames_dir}`\n")

    if mode == "query":
        axes = {}
        for r in results:
            d = axes.setdefault(r["axis"], {"n": 0, "hit": 0})
            d["n"] += 1
            d["hit"] += bool(r["matches"])
        w("## by axis\n")
        w("| axis | answered present | note |")
        w("|---|---|---|")
        for ax in sorted(axes):
            d = axes[ax]
            note = ("**every hit here is a fabrication**"
                    if ax == "negative" and d["hit"] else
                    "ground truth known: all absent" if ax == "negative" else "")
            w(f"| {ax} | {d['hit']}/{d['n']} | {note} |")
        w("")
        w("## per query\n")
        for r in results:
            w(f"### [{r['axis']}] {r['query']}\n")
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
    p.add_argument("--roi", default="wide",
                   help="preset name or fractions x,y,w,h. "
                        "'wide' (default) drops only the brick wall and the "
                        "facade opposite, which contain no road users; "
                        "'junction' crops to the intersection box, trading the "
                        "approaches away for pixels; 'none' sends the full frame")
    p.add_argument("--time-encoding", default=DEFAULT_ENCODING,
                   help="how each frame's timestamp reaches the model, as a "
                        "comma-separated subset of "
                        f"{','.join(CHANNELS)} (or 'none'). 'burn' draws it "
                        "into the pixels, 'list' names every timestamp in one "
                        "text block, 'interleave' puts one timestamp block "
                        "immediately before its own frame. The channels are "
                        "independent and this is worth an ablation: change "
                        f"one at a time. Default '{DEFAULT_ENCODING}'")
    p.add_argument("--backend", choices=["gemini", "claude"], default="gemini")
    p.add_argument("--model", default=None)
    p.add_argument("--max-output-tokens", type=int, default=32000,
                   help="output budget per call. Thinking is drawn from the "
                        "same budget, so too low a value returns an empty body")
    p.add_argument("--env", default=None)
    p.add_argument("--name", default=None,
                   help="label for this run, used in its directory name. "
                        "Default is composed from the query set, roi and fps "
                        "so an ablation loop separates itself")
    p.add_argument("--results-root", default="results",
                   help="parent of the per-run directories")
    p.add_argument("--run-dir", default=None,
                   help="use exactly this directory instead of composing "
                        "results/<timestamp>-<name>. Overrides --name")
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
        roi = parse_roi(a.roi)
        enc = parse_encoding(a.time_encoding)
    except ValueError as e:
        sys.exit(str(e))
    # normalised, so the record says what ran rather than how it was typed
    a.time_encoding = ",".join(sorted(enc)) or "none"
    started = datetime.now()

    info = probe(a.video)
    print(json.dumps(info, indent=2))
    if info["likely_vfr"]:
        print("\n!! variable frame rate -- timestamps below come from PTS, "
              "never from frame index\n", file=sys.stderr)
    end = a.end if a.end is not None else (info["duration_s"] or 0.0)

    if a.overview:
        thumbs = sample_overview(a.video, a.start, end, a.overview_every, roi)
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
               Path(a.results_root) / f"{started:%Y%m%d-%H%M%S}-{run_label(a)}")
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
        frames = [(t, apply_roi(img, roi)) for t, img in
                  extract(a.video, t0, t1, a.fps)]
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
        "roi": a.roi,
        "roi_fractions": list(roi) if roi else None,
        "time_encoding": a.time_encoding,
        "backend": backend.name,
        "model": backend.model,
        "resolution": getattr(backend, "resolution", None),
        "thinking_level": getattr(backend, "thinking_level", None),
        "max_output_tokens": a.max_output_tokens,
        "queries_file": a.queries,
        "axis_filter": a.axis,
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
            res, usage = backend.run(SYSTEM_OPEN, payload,
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
            for qi, (axis, q) in enumerate(queries):
                try:
                    res, usage = backend.run(SYSTEM_QUERY, payload,
                                             query_prompt(frames, t0, t1, q, enc),
                                             QueryResult, a.max_output_tokens)
                except Exception as e:
                    # One bad call must not discard the answers already in
                    # hand. Record the failure as a row and keep going.
                    failures.append({"axis": axis, "query": q,
                                     "error": f"{type(e).__name__}: {e}"})
                    append_jsonl(jsonl_path, {"window": [t0, t1], "mode": "query",
                                              "time_encoding": a.time_encoding,
                                              "query_index": qi, "axis": axis,
                                              "query": q, "error": str(e)})
                    print(f"\n[{axis}] {q[:64]}\n  FAILED  {type(e).__name__}: "
                          f"{str(e)[:160]}")
                    continue
                usages.append(usage)
                rec = {"window": [t0, t1], "mode": "query",
                       "time_encoding": a.time_encoding, "query_index": qi,
                       "axis": axis, "query": q, **res.model_dump()}
                results.append(rec)
                append_jsonl(jsonl_path, rec)
                verdict = "MATCH" if res.matches else "absent"
                mark = "  <-- FABRICATED" if (res.matches and axis == "negative") else ""
                print(f"\n[{axis}] {q[:64]}\n  {verdict}{mark}")
                for m in res.matches:
                    print(f"    [{m.match_quality}/{m.confidence}] "
                          f"{m.t_start_sec:.1f}-{m.t_end_sec:.1f}s "
                          f"(clearest {m.clearest_frame_sec:.1f}s)  {m.subject}")
                    print(f"    {m.what_happens}")
                if res.considered_and_rejected:
                    print(f"    ruled out: {res.considered_and_rejected[:160]}")
                if not res.matches and res.why_not_found:
                    print(f"    why not: {res.why_not_found[:160]}")

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
