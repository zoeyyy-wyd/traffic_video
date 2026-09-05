#!/usr/bin/env python3
"""Run the camera measurements and write measurements/*.json.

  python scripts/measure.py videos/<clip>.mp4 [--only phase] [--across videos/*.mp4]

Thin CLI over utils/measure.py, which build_scene.py also imports -- one
implementation. Measurements are inputs, not judges: only the hand-filled
sheet scores a run. Each output names its judgement calls.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.measure import (BANDS, HEADS, flow_direction, signal_legibility,
                           signal_phase)
from utils.video import extract, probe

JUDGEMENT = {
    "legibility":
        "The candidate heads were located BY EYE. An automatic sweep of the "
        "intersection returned only construction workers and traffic cones, so "
        "this is 'the heads that were found', not 'all the heads'. The 0.45 "
        "threshold on the difference image, the 40% area cap that rejects a "
        "vehicle passing behind a head as if it were a lens, and the 15-point "
        "range below which a head is called invariant, are all chosen.",
    "flow":
        "Band rectangles were placed by eye from a single frame and are the main "
        "choice in this measurement. So is the r >= 0.45 cutoff for believing a "
        "direction at all. Right-hand driving is an assumption about the "
        "jurisdiction, used only to corroborate the result, never as input.",
    "phase":
        "The thresholds were hand-set on the 2026-08-25 17:00 clip and have not "
        "been validated against a second observer or the other pedestrian head. "
        "Boundaries are +/- 1 s; the phase LABELS are firmer than the "
        "boundaries. Which crosswalk this head governs is not established, so "
        "the timeline is not yet attached to a particular crossing.",
}


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"-> {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--only", nargs="*", default=["legibility", "flow", "phase"],
                    choices=["legibility", "flow", "phase"])
    ap.add_argument("--across", nargs="*", default=None,
                    help="also check the readable head cycles in these clips")
    ap.add_argument("--out-dir", default="measurements")
    a = ap.parse_args()
    out = Path(a.out_dir)
    tag = Path(a.video).stem.split("D-")[-1].replace("_T-", "-")

    if "legibility" in a.only:
        print("measuring signal legibility ...")
        heads = signal_legibility(a.video)
        for k, v in heads.items():
            px = v.get("lit_glyph_native")
            print(f"  {k:<10} {'lens':<8}{px[0]}x{px[1]} px  "
                  f"sep@1.00x {v['downscale_ladder'][0]['separation']}"
                  if v["readable"] else
                  f"  {k:<10} no lens   (varies {v['rb_range_over_clip']} over the clip)")
        across = {}
        if a.across:
            lit = [k for k, v in heads.items() if v["readable"]]
            if lit:
                box = heads[lit[0]]["lit_glyph_box_native"]
                print(f"  checking {lit[0]} across {len(a.across)} clips ...")
                for v in a.across:
                    vals = [np.asarray(im.crop(box).convert("RGB"), float)
                            .reshape(-1, 3) for _, im in
                            extract(v, 0.0, probe(v)["duration_s"] or 0, 1 / 6)]
                    rng = float(np.ptp([x[:, 0].mean() - x[:, 2].mean() for x in vals]))
                    across[Path(v).stem.split("T-")[-1]] = round(rng, 1)
                    print(f"    {Path(v).name:<46} R-B range {rng:6.1f}")
        write(out / "signal-legibility.json", {
            "topic": "which signal faces are readable from this view, and at what size",
            "clip": a.video,
            "method": "Difference two native frames in different phases over each "
                      "candidate head; the changing pixels are the lit face and "
                      "their box measures it. State is then read on that located "
                      "patch across the clip -- reading it over the whole head "
                      "box dilutes an 8x10 screen inside a 60x55 housing to "
                      "nothing, which once made the readable head look unreadable.",
            "judgement": JUDGEMENT["legibility"],
            "reproduce": f"python scripts/measure.py {a.video} --only legibility",
            "heads": heads,
            "rb_range_across_clips": across or None,
            "note": "Separation surviving to 0.41x -- the scale the probe sends -- "
                    "means a wrong answer about signal colour cannot be blamed on "
                    "missing pixels. Glyph SHAPE survives at no scale, native included.",
        })

    if "flow" in a.only:
        print("\nmeasuring flow direction ...")
        flow = flow_direction(a.video)
        for k, v in flow.items():
            print(f"  {k:<13} r={v['r']:5.3f}  "
                  f"{v.get('direction') or 'FAILED: ' + v.get('why', '')}")
        ok = {k: v for k, v in flow.items() if v["status"] == "ok"}
        if {"avenue-east", "avenue-west"} <= set(ok) and \
                ok["avenue-east"]["direction"] != ok["avenue-west"]["direction"]:
            print("  the two sides disagree in sign, which is what a two-way street "
                  "with\n  right-hand driving must produce")
        write(out / "flow-direction.json", {
            "topic": "direction of travel per carriageway, image space",
            "clip": a.video,
            "method": "Virtual tripwires. Motion energy = mean |frame(k+1)-frame(k)| "
                      "in a band; two bands per carriageway, cross-correlated. The "
                      "leading band is the one traffic reaches first. Optical flow "
                      "was tried and failed twice: the per-frame displacement is "
                      "outside any reasonable search window, and widening it leaves "
                      "a window that is >95% static asphalt, so the peak locks onto "
                      "zero shift.",
            "judgement": JUDGEMENT["flow"],
            "reproduce": f"python scripts/measure.py {a.video} --only flow",
            "note": "IMAGE SPACE. Which way is north is not established from this "
                    "view, and a compass label would be a guess handed on as fact.",
            "bands_native": {k: [list(b) for b in v] for k, v in BANDS.items()},
            "carriageways": flow,
        })

    if "phase" in a.only:
        print("\nmeasuring pedestrian phase ...")
        ph = signal_phase(a.video)
        for p in ph["phases"]:
            print(f"  {p['state']:<10} {p['t_start']:6.2f} - {p['t_end']:6.2f} s")
        if ph["cycle_s"]:
            print(f"  WALK onsets {ph['cycle_s']}s apart")
        write(out / f"signal-phase-{tag}.json", {
            "topic": "pedestrian signal phase timeline",
            "clip": a.video,
            "method": "Read mean(R)-mean(B) and mean luminance on the lit screen at "
                      "2 fps. Three states, not two: the countdown flashes, so "
                      "colour separates the hand and luminance splits the rest into "
                      "the white figure and the dark half of a flash.",
            "judgement": JUDGEMENT["phase"],
            "reproduce": f"python scripts/measure.py {a.video} --only phase",
            "not_for_scene": "A phase timeline belongs to one recording. It is not "
                             "folded into the scene block, which is reused across "
                             "clips.",
            **ph,
        })


if __name__ == "__main__":
    main()
