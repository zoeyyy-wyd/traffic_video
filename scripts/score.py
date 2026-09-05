#!/usr/bin/env python3
"""Score one run against a filled ground-truth sheet.

  python scripts/score.py <arm-dir> ground-truth/<clip>.txt [--write FILE]

presence = was the yes/no right, per sample. localised = returned intervals
landing on a real span at IoU >= --iou, matched one-to-one. The two come
apart; only the second matters for annotation. Distinct zeros: `no overlap`,
`no answer`, `—` (negatives). Unreviewed categories are dropped, not guessed.
Sheet times may be seconds or MM:SS. Whole experiment: scripts/report.py.
"""
import argparse
import json
import re
from pathlib import Path

_LINES = []


def out(line=""):
    _LINES.append(line)
    print(line)


def secs(t):
    t = t.strip()
    if ":" in t:
        m, s = t.split(":")[:2]
        return int(m) * 60 + float(s)
    return float(t)


def iou(p, g):
    lo, hi = max(p[0], g[0]), min(p[1], g[1])
    inter = max(0.0, hi - lo)
    union = (p[1] - p[0]) + (g[1] - g[0]) - inter
    return inter / union if union > 0 else 0.0


def match(preds, spans, thr):
    """Greedy one-to-one pairing by IoU, best first.

    One-to-one matters: without it a single interval covering the whole clip
    would "hit" every span in the sheet at once, which is the opposite of
    localisation. Pairs below `thr` are still returned so the mean includes
    near misses rather than only successes.
    """
    cand = sorted(((iou((p["t_start_sec"], p["t_end_sec"]), (g[0], g[1])), i, j)
                   for i, p in enumerate(preds) for j, g in enumerate(spans)),
                  key=lambda x: -x[0])
    used_p, used_g, pairs = set(), set(), []
    for v, i, j in cand:
        if v <= 0 or i in used_p or j in used_g:
            continue
        used_p.add(i); used_g.add(j); pairs.append((v, i, j))
    return pairs, used_p, used_g


def read_truth(path):
    cat, res = None, {}
    for l in Path(path).read_text().splitlines():
        if re.match(r"^[a-z][a-z-]* +\|", l) or l.startswith("negative |"):
            head, _, text = l.partition("|")
            cat = (head.strip(), text.strip())
            res[cat] = {"occurred": None, "spans": []}
        elif cat and re.match(r"^\s+occurred:", l):
            res[cat]["occurred"] = l.split("occurred:")[1].strip().lower() or None
        elif cat and re.search(r"t=\s*[\d:]", l):
            m = re.search(r"t=\s*([\d:.]+)\s*-\s*([\d:.]+)", l)
            if not m:
                continue
            try:
                a_, b_ = secs(m.group(1)), secs(m.group(2))
            except ValueError:
                continue
            if b_ > a_:
                w = re.search(r"who:\s*([^?]*)", l)
                res[cat]["spans"].append((a_, b_, w.group(1).strip() if w else ""))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("truth")
    ap.add_argument("--iou", type=float, default=0.5,
                    help="IoU a pair must reach to count as localised (default 0.5)")
    ap.add_argument("--write", metavar="FILE", default=None,
                    help="also write the table here, so a score need not be "
                         "recomputed to be read")
    a = ap.parse_args()

    truth = read_truth(a.truth)
    by_query = {t: v for (_, t), v in truth.items()}
    rows = [json.loads(l) for l in
            (Path(a.run) / "results.jsonl").read_text().splitlines()]
    samples = sorted({r.get("sample", 1) for r in rows})
    per = {}
    for r in rows:
        per.setdefault(r["query"], {})[r.get("sample", 1)] = r.get("matches") or []

    cfg = {}
    cfgp = Path(a.run) / "run.json"
    if cfgp.exists():
        cfg = json.loads(cfgp.read_text())

    out(f"run    {Path(a.run).name}")
    out(f"truth  {Path(a.truth).name}")
    out(f"model  {cfg.get('model', '?')}   fps {cfg.get('fps', '?')}   "
        f"{len(samples)} samples/query   "
        f"scene {'yes' if cfg.get('scene_file') else 'no'}")
    out()
    hdr = (f"{'category':<16} {'truth':<5} {'samples':<7} {'presence':>8} "
           f"{'localised':>10} {'mean IoU':>10} {'best':>6}  {'FP':>3} {'FN':>4}")
    out(hdr); out("-" * len(hdr))

    tot_p = tot_pn = tot_hit = tot_pred = 0
    for q, samp in per.items():
        t = by_query.get(q)
        axis = next((ax for (ax, tx) in truth if tx == q), "?")
        if t is None or t["occurred"] not in ("yes", "no"):
            out(f"{axis:<16} {'--':<5} {'dropped: not reviewed':>40}")
            continue
        want = t["occurred"] == "yes"
        marks, ok = "", 0
        ious, matched, fp, fn, npred = [], 0, 0, 0, 0
        for s_ in samples:
            ms = samp.get(s_, [])
            marks += "Y" if ms else "n"
            ok += (bool(ms) == want)
            if want:
                pairs, mi, mj = match(ms, t["spans"], a.iou)
                ious += [v for v, _, _ in pairs]
                matched += sum(1 for v, _, _ in pairs if v >= a.iou)
                fp += len(ms) - len(mi)
                fn += len(t["spans"]) - len(mj)
                npred += len(ms)
        tot_p += ok; tot_pn += len(samples)
        tot_hit += matched; tot_pred += npred

        if not want:
            loc = mean = best = fps_ = fns_ = "—"
        elif npred == 0:
            loc, mean, best, fps_, fns_ = "no answer", "—", "—", "—", str(fn)
        elif not ious:
            loc, mean, best = f"0/{npred}", "no overlap", "0.00"
            fps_, fns_ = str(fp), str(fn)
        else:
            loc = f"{matched}/{npred}"
            mean = f"{sum(ious)/len(ious):.2f}"
            best = f"{max(ious):.2f}"
            fps_, fns_ = str(fp), str(fn)
        out(f"{axis:<16} {'yes' if want else 'no':<5} {marks:<7} "
            f"{ok}/{len(samples):<6} {loc:>10} {mean:>10} {best:>6}  "
            f"{fps_:>3} {fns_:>4}")

    out()
    out(f"presence   {tot_p}/{tot_pn} ({100*tot_p/max(1,tot_pn):.0f}%)"
        f"   -- was the yes/no right, per sample")
    out(f"localised  {tot_hit}/{tot_pred} ({100*tot_hit/max(1,tot_pred):.0f}%)"
        f"   -- of the intervals returned, how many land on a real one "
        f"at IoU >= {a.iou:g}")
    out()
    out("These come apart, and the gap is the point: a category can score full "
        "marks on presence")
    out("while every interval it returned points at the wrong moment.")
    out()
    out("How far IoU can be read here is capped from both ends -- the sheet's "
        "boundaries were")
    out("judged by eye to about a second, and the model can only place an edge "
        "on a sampled")
    out("frame. On a 6 s event that puts a correct answer near 0.8, not 1.0. "
        "Unmatched")
    out("predictions are not necessarily wrong either: the sheet lists the "
        "spans a person")
    out("found, not every span that exists.")

    if a.write:
        Path(a.write).write_text("\n".join(_LINES) + "\n")
        print(f"\n-> {a.write}")


if __name__ == "__main__":
    main()
