#!/usr/bin/env python3
"""Score a probe run against a filled ground-truth sheet.

    python scripts/score.py results/<run>/ notes/ground-truth-<clip>.txt

Two numbers per category, and they answer different questions:

  presence   did the run get the yes/no right, per sample
  timing     temporal IoU between the intervals it returned and the real ones,
             matched one-to-one

A category whose sheet entry is `not-reviewed`, or blank, is DROPPED rather
than counted either way. Guessing there would silently turn an unchecked
category into a score.

Times in the sheet may be written as seconds or as MM:SS; both are read.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def secs(t):
    t = t.strip()
    if ":" in t:
        m, s = t.split(":")[:2]
        return int(m) * 60 + float(s)
    return float(t)


def iou(p, g):
    """Temporal IoU of two intervals."""
    lo, hi = max(p[0], g[0]), min(p[1], g[1])
    inter = max(0.0, hi - lo)
    union = (p[1] - p[0]) + (g[1] - g[0]) - inter
    return inter / union if union > 0 else 0.0


def match(preds, spans, thr):
    """Greedy one-to-one pairing by IoU, best first.

    One-to-one matters: without it a single returned interval covering the
    whole clip would "hit" every span in the sheet at once, which is the
    opposite of localisation. Pairs below `thr` are still returned so the mean
    IoU includes near misses rather than only the successes.
    """
    cand = sorted(((iou((p["t_start_sec"], p["t_end_sec"]), (g[0], g[1])), i, j)
                   for i, p in enumerate(preds) for j, g in enumerate(spans)),
                  key=lambda x: -x[0])
    used_p, used_g, out = set(), set(), []
    for v, i, j in cand:
        if v <= 0 or i in used_p or j in used_g:
            continue
        used_p.add(i); used_g.add(j); out.append((v, i, j))
    return out, used_p, used_g


def read_truth(path):
    cat, out = None, {}
    for l in Path(path).read_text().splitlines():
        if re.match(r"^[a-z][a-z-]* +\|", l) or l.startswith("negative |"):
            head, _, text = l.partition("|")
            cat = (head.strip(), text.strip())
            out[cat] = {"occurred": None, "spans": []}
        elif cat and re.match(r"^\s+occurred:", l):
            v = l.split("occurred:")[1].strip().lower()
            out[cat]["occurred"] = v or None
        elif cat and re.search(r"t=\s*[\d:]", l):
            m = re.search(r"t=\s*([\d:.]+)\s*-\s*([\d:.]+)", l)
            if not m:
                continue
            try:
                a, b = secs(m.group(1)), secs(m.group(2))
            except ValueError:
                continue
            if b > a:
                who = re.search(r"who:\s*([^?]*)", l)
                out[cat]["spans"].append((a, b, who.group(1).strip() if who else ""))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("truth")
    ap.add_argument("--iou", type=float, default=0.5,
                    help="IoU a pair must reach to count as localised (default 0.5)")
    a = ap.parse_args()

    truth = read_truth(a.truth)
    by_query = {t: v for (ax, t), v in truth.items()}

    rows = [json.loads(l) for l in (Path(a.run) / "results.jsonl").read_text().splitlines()]
    samples = sorted({r.get("sample", 1) for r in rows})
    per = {}
    for r in rows:
        per.setdefault(r["query"], {})[r.get("sample", 1)] = r.get("matches") or []

    print(f"run   {Path(a.run).name}")
    print(f"truth {Path(a.truth).name}   ({len(samples)} samples per query, "
          f"IoU>={a.iou:g})\n")
    hdr = f"{'category':<16} {'truth':<6} {'samples':<8} {'presence':>9}  {'timing':>18}"
    print(hdr); print("-" * len(hdr))

    tot_p = tot_pn = 0
    for q, samp in per.items():
        t = by_query.get(q)
        axis = next((ax for (ax, tx) in truth if tx == q), "?")
        if t is None or t["occurred"] not in ("yes", "no"):
            print(f"{axis:<16} {'--':<6} {'':<8} {'dropped: not reviewed':>29}")
            continue
        want = t["occurred"] == "yes"
        marks, ok = "", 0
        ious, matched, fp, fn = [], 0, 0, 0
        for s in samples:
            ms = samp.get(s, [])
            said = bool(ms)
            marks += "Y" if said else "n"
            ok += (said == want)
            if want:
                pairs, mi, mj = match(ms, t["spans"], a.iou)
                ious += [i for i, _, _ in pairs]
                matched += sum(1 for i, _, _ in pairs if i >= a.iou)
                fp += len(ms) - len(mi)
                fn += len(t["spans"]) - len(mj)
        tot_p += ok; tot_pn += len(samples)
        if want and (ious or fp or fn):
            mean = sum(ious) / len(ious) if ious else 0.0
            tim = f"IoU {mean:.2f}  {matched}@>={a.iou:g}  +{fp} -{fn}"
        else:
            tim = "—"
        print(f"{axis:<16} {'yes' if want else 'no':<6} {marks:<8} "
              f"{ok}/{len(samples):<7} {tim:>26}")

    print(f"\npresence, all scorable categories: {tot_p}/{tot_pn} "
          f"({100*tot_p/max(1,tot_pn):.0f}%)")
    print(f"\ntiming columns: mean IoU over matched pairs | pairs reaching "
          f"{a.iou:g} | +unmatched predictions -unmatched truth, summed over samples")
    print("\nWhat limits how far IoU can be read here: the sheet's boundaries were "
          "judged by eye to\nabout a second, and the model can only place an edge on "
          "a sampled frame -- a 1 s grid at\n1 fps. On a 6 s event those two together "
          "put a ceiling near 0.8 even for a correct answer.\nUnmatched predictions "
          "are not necessarily wrong either: the sheet lists the spans a person\n"
          "found, not every span that exists.")


if __name__ == "__main__":
    main()
