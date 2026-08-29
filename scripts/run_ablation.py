#!/usr/bin/env python3
"""Run one ablation as ONE experiment, in one directory.

    python scripts/run_ablation.py videos/<clip>.mp4 \\
        --queries queries/events-key.txt --name scene --repeat 2 \\
        --arm "no-scene=" \\
        --arm "with-scene=--scene scene/12F-Ams.built.md"

Writes:

    results/<timestamp>-<name>/
        experiment.json          what varied, what was held fixed
        <arm>/rep<N>/            one probe run: summary.md, results.jsonl, run.json
        comparison.md            arm-by-arm verdict per query, flips called out

The point of the layout is that an ablation is a single experiment, not a pile
of sibling runs that happen to have been made the same afternoon. Everything
that varied is in `experiment.json`; everything that did not is stated there
once instead of being re-derived by diffing run.json files later.

Repeats are inside the experiment for the same reason. A difference between two
arms at n=1 is not a difference -- the same prompt on the same frames has
already produced different answers on different runs of this probe, so an arm
comparison without repeats cannot tell an effect from that variance.
"""
import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(run_dir):
    f = run_dir / "results.jsonl"
    return [json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []


def verdict(rows, axis, query):
    for r in rows:
        if r.get("axis") == axis and r.get("query") == query:
            if "error" in r:
                return "FAILED", []
            ms = r.get("matches") or []
            return ("present" if ms else "absent"), ms
    return "-", []


# phrases lifted straight from a scene block; if an arm that was given the block
# uses them far more often than an arm that was not, it is repeating what it was
# told rather than reporting what it saw
ECHO = ["up the frame", "down the frame", "right to left", "left to right",
        "left of the yellow", "right of the yellow", "double yellow",
        "scaffolding shed", "tree canopy"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--queries", required=True)
    ap.add_argument("--name", required=True, help="what this ablation is called")
    ap.add_argument("--arm", action="append", required=True,
                    help="NAME=extra probe flags. Repeatable. Empty flags = baseline")
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--fps", type=float, default=0.5)
    ap.add_argument("--common", default="", help="flags applied to every arm")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    arms = []
    for spec in a.arm:
        if "=" not in spec:
            sys.exit(f"--arm needs NAME=flags, got {spec!r}")
        n, _, flags = spec.partition("=")
        arms.append((n.strip(), flags.strip()))

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    exp = ROOT / "results" / f"{ts}-{a.name}"
    exp.mkdir(parents=True, exist_ok=True)

    manifest = {
        "experiment": a.name,
        "started": datetime.now().isoformat(timespec="seconds"),
        "held_fixed": {"video": a.video, "queries": a.queries, "fps": a.fps,
                       "common_flags": a.common or None},
        "varied": {n: (f or "(baseline: no extra flags)") for n, f in arms},
        "repeats": a.repeat,
        "arms": [],
    }
    (exp / "experiment.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"experiment -> {exp}\n")

    for name, flags in arms:
        for rep in range(1, a.repeat + 1):
            rd = exp / name / f"rep{rep}"
            out = ROOT / "runs" / f"{ts}-{a.name}" / name / f"rep{rep}"
            cmd = [sys.executable, str(ROOT / "scripts" / "vlm_probe.py"), a.video,
                   "--queries", a.queries, "--fps", str(a.fps),
                   "--run-dir", str(rd), "--out", str(out)]
            cmd += a.common.split() + flags.split()
            print(f"--- {name} rep{rep}\n    {' '.join(cmd[1:])}")
            if a.dry_run:
                continue
            r = subprocess.run(cmd, cwd=ROOT)
            manifest["arms"].append({"arm": name, "rep": rep, "dir": str(rd.relative_to(ROOT)),
                                     "exit": r.returncode})
            (exp / "experiment.json").write_text(json.dumps(manifest, indent=2) + "\n")

    if a.dry_run:
        return

    # ---- comparison -------------------------------------------------------
    data = {(n, rep): load(exp / n / f"rep{rep}")
            for n, _ in arms for rep in range(1, a.repeat + 1)}
    queries = []
    for rows in data.values():
        for r in rows:
            k = (r.get("axis"), r.get("query"))
            if k[0] and k not in queries:
                queries.append(k)

    L = [f"# {a.name} — arm comparison\n",
         f"- clip: `{a.video}`",
         f"- queries: `{a.queries}` | fps {a.fps:g} | {a.repeat} repeat(s) per arm\n",
         "Held fixed and varied: `experiment.json`. "
         "A flip between arms at one repeat is not an effect; check the repeats "
         "column before reading anything into it.\n",
         "## verdict per query\n",
         "| axis | query | " + " | ".join(n for n, _ in arms) + " |",
         "|---|---|" + "---|" * len(arms)]
    flips = []
    for axis, q in queries:
        cells = []
        for n, _ in arms:
            vs = [verdict(data[(n, rep)], axis, q)[0] for rep in range(1, a.repeat + 1)]
            cells.append("/".join(vs))
        if len({c.split("/")[0] for c in cells}) > 1:
            flips.append((axis, q, cells))
        L.append(f"| {axis} | {q[:58]} | " + " | ".join(cells) + " |")

    L.append("\n## flips between arms\n")
    if flips:
        for axis, q, cells in flips:
            L.append(f"- **{axis}** — {q}")
            for (n, _), c in zip(arms, cells):
                L.append(f"  - `{n}`: {c}")
    else:
        L.append("None. Every query got the same present/absent verdict in every arm.")

    L.append("\n## echo check\n")
    L.append("How often each arm's own prose uses wording that appears in a scene "
             "block. An arm that was given the block and uses this language far "
             "more than one that was not is repeating what it was told; the "
             "phrases are not evidence of having looked.\n")
    L.append("| arm | matches | phrases used |")
    L.append("|---|---|---|")
    for n, _ in arms:
        hits = defaultdict(int)
        for rep in range(1, a.repeat + 1):
            for r in data[(n, rep)]:
                for m in (r.get("matches") or []):
                    txt = (m.get("what_happens", "") + " " + m.get("subject", "")).lower()
                    for p in ECHO:
                        if p in txt:
                            hits[p] += 1
        L.append(f"| {n} | {sum(hits.values())} | "
                 + (", ".join(f"{k} ×{v}" for k, v in sorted(hits.items())) or "—") + " |")

    (exp / "comparison.md").write_text("\n".join(L) + "\n")
    print(f"\n-> {exp}/comparison.md")


if __name__ == "__main__":
    main()
