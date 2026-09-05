#!/usr/bin/env python3
"""Summarise one experiment into result.md: configuration, per-arm totals, and
every answer with the IoU it earned.

  python scripts/report.py experiment_results/fps ground-truth/<clip>.txt
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from importlib.util import module_from_spec, spec_from_file_location

_spec = spec_from_file_location("sc", Path(__file__).parent / "score.py")
_sc = module_from_spec(_spec); _spec.loader.exec_module(_sc)


def fmt(t):
    return f"{int(t)//60:d}:{t%60:04.1f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("experiment")
    ap.add_argument("truth")
    ap.add_argument("--iou", type=float, default=0.5)
    a = ap.parse_args()

    exp = Path(a.experiment)
    truth = _sc.read_truth(a.truth)
    by_q = {t: v for (_, t), v in truth.items()}
    arms = sorted(p for p in (exp / "arms").iterdir() if (p / "results.jsonl").exists())
    if not arms:
        sys.exit(f"no arms with results under {exp}/arms/")

    L = [f"# {exp.name}\n"]

    cfgs = {p.name: json.loads((p / "run.json").read_text()) for p in arms}
    c0 = next(iter(cfgs.values()))
    varies = {k for k in ("fps", "scene_file", "model", "samples_per_query",
                          "time_encoding", "batch_queries")
              if len({json.dumps(c.get(k)) for c in cfgs.values()}) > 1}

    L += ["## Configuration\n",
          f"- clip `{Path(c0['clip']).name}`, {c0['range_sec'][1]:.0f}s",
          f"- queries `{c0['queries_file']}`, {c0['n_queries']} categories",
          f"- model `{c0['model']}`, {c0['samples_per_query']} samples per query"
          + (", all queries in one call" if c0.get("batch_queries") else ""),
          f"- timestamps `{c0['time_encoding']}`",
          f"- ground truth `{Path(a.truth).name}`",
          f"- **varied across arms: {', '.join(sorted(varies)) or 'nothing'}**\n"]

    L += ["| arm | " + " | ".join(sorted(varies)) + " | frames | tokens in |",
          "|---|" + "---|" * (len(varies) + 2)]
    for p in arms:
        c = cfgs[p.name]
        cells = [str(c.get(k)) for k in sorted(varies)]
        L.append(f"| `{p.name}` | " + " | ".join(cells)
                 + f" | {c['n_frames']} | {c['tokens_in']:,} |")

    # ---- totals -----------------------------------------------------------
    L += ["\n## Result\n",
          "`presence` is whether the yes/no was right, per sample. `localised` "
          "is how many returned intervals land on a real one at "
          f"IoU >= {a.iou:g}. They come apart, and only the second one means "
          "anything for annotation.\n",
          "| arm | presence | localised | mean IoU over matched pairs |",
          "|---|---|---|---|"]
    detail = {}
    for p in arms:
        rows = [json.loads(l) for l in (p / "results.jsonl").read_text().splitlines()]
        samples = sorted({r.get("sample", 1) for r in rows})
        per = {}
        for r in rows:
            per.setdefault(r["query"], {})[r.get("sample", 1)] = r.get("matches") or []
        ok = n = hit = pred = 0
        allious, lines = [], []
        for q, samp in per.items():
            t = by_q.get(q)
            axis = next((ax for (ax, tx) in truth if tx == q), "?")
            if t is None or t["occurred"] not in ("yes", "no"):
                continue
            want = t["occurred"] == "yes"
            for s_ in samples:
                ms = samp.get(s_, [])
                ok += (bool(ms) == want); n += 1
                if not ms:
                    lines.append((axis, s_, "—", "absent",
                                  "correct" if not want else "MISS", ""))
                    continue
                pairs, _, _ = (_sc.match(ms, t["spans"], a.iou) if want
                               else ([], set(), set()))
                best = {i: v for v, i, _ in pairs}
                for i, m in enumerate(ms):
                    v = best.get(i)
                    pred += want
                    hit += bool(want and v is not None and v >= a.iou)
                    if v is not None:
                        allious.append(v)
                    verdict = ("FABRICATED" if not want else
                               f"{v:.2f}" if v is not None and v >= a.iou else
                               f"{v:.2f} below" if v is not None else "no overlap")
                    lines.append((axis, s_,
                                  f"{fmt(m['t_start_sec'])}-{fmt(m['t_end_sec'])}",
                                  m.get("subject", "")[:34], verdict,
                                  m.get("match_quality", "")))
        detail[p.name] = lines
        mi = f"{sum(allious)/len(allious):.2f}" if allious else "—"
        L.append(f"| `{p.name}` | {ok}/{n} ({100*ok/max(1,n):.0f}%) | "
                 f"{hit}/{pred} ({100*hit/max(1,pred):.0f}%) | {mi} |")

    # ---- every answer -----------------------------------------------------
    L += ["\n## Every answer\n",
          "One row per interval the model returned, plus a row where it "
          "returned nothing. `IoU` is against the best unclaimed real span, "
          "matched one-to-one so a single wide interval cannot claim several. "
          "`below` means it overlapped but under the threshold; `no overlap` "
          "means it landed nowhere near.\n"]
    for name, lines in detail.items():
        L += [f"### {name}\n",
              "| category | s | interval | subject | IoU | quality |",
              "|---|---|---|---|---|---|"]
        for ax, s_, iv, subj, verdict, qual in lines:
            L.append(f"| {ax} | {s_} | {iv} | {subj} | {verdict} | {qual} |")
        L.append("")

    L += ["## Reading it\n",
          f"n={c0['samples_per_query']} per arm over {c0['n_queries']} "
          "categories. A difference of a few decisions between arms is inside "
          "the run-to-run variance this probe has already been shown to have, "
          "so the per-answer rows are more informative than the totals.\n",
          "IoU is capped from both ends: the sheet's boundaries were judged by "
          "eye to about a second, and the model can only place an edge on a "
          "sampled frame. On a 6 s event that puts a correct answer near 0.8, "
          "not 1.0.\n",
          "## Reproduce\n", "```bash", f"./experiment_{exp.name}.sh", "```"]

    (exp / "result.md").write_text("\n".join(L) + "\n")
    print(f"-> {exp}/result.md   ({sum(len(v) for v in detail.values())} answer rows)")


if __name__ == "__main__":
    main()
