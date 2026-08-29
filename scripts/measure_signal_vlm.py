#!/usr/bin/env python3
"""Read the pedestrian signal phase by asking a VLM, frame by frame.

    python scripts/measure_signal_vlm.py videos/<clip>.mp4
    python scripts/measure_signal_vlm.py videos/<clip>.mp4 --crop full --fps 0.5

Writes measurements/signal-phase-<clip>-vlm.json in the same shape as the
arithmetic reading, so the two can be compared directly. If an arithmetic
timeline for the same clip is on disk, this prints the agreement table.

WHY BOTH EXIST. Reading `R - B` over the lit screen is deterministic: the same
file gives the same answer every time, and disagreeing with it means changing
a stated parameter and re-running. Asking a model gives an answer that varies
between runs and can only be checked by eye. That is a real difference in kind,
and it is worth having the number rather than the argument -- so this script
exists to measure how large it is on this camera, not to replace the other one.

The head box drifts BETWEEN clips (measured: the same native box frames the
head in all five 2026-08-25 recordings but off-centre differently in each), so
--box must be re-checked when the clip changes. Pass --save-crops to write what
was sent and look at it before believing either answer.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List, Literal

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.env import load_env, require_key
from utils.render import fit
from utils.video import extract
from utils.vlm import get_backend

# ped_E on the 12F-Ams view, from measurements/signal-legibility.json
DEFAULT_BOX = (2385, 372, 2437, 414)

SYSTEM = """You read the face of a pedestrian traffic signal in still frames from a fixed camera.

The head is seen from above and behind, so you are looking at a small dark screen set in a yellow housing. Only the screen matters. It shows one of:

- an ORANGE or RED raised hand, or orange countdown numerals -> "dont_walk"
- a WHITE walking figure -> "walk"
- nothing lit at all -> "dark"  (the countdown flashes, so the dark half of a flash looks like this)

Judge each frame on the colour of the lit part of the screen. The glyph's SHAPE is not resolvable at this scale and you should not try to use it -- an upraised hand and a countdown numeral are the same colour and cannot be told apart here. If the screen is obscured, or you cannot tell, say "unreadable" rather than guessing; a wrong confident answer here is worse than an admitted gap, because this reading is used as ground truth for other work.

Frames are in chronological order and each is preceded by its timestamp."""


class FrameState(BaseModel):
    t_sec: float
    state: Literal["walk", "dont_walk", "dark", "unreadable"]
    confidence: Literal["high", "medium", "low"]


class PhaseRead(BaseModel):
    frames: List[FrameState]
    head_visible: bool
    notes: str


def runs_from(states):
    """[(t,state)] -> merged [(state, t0, t1)]."""
    out, cur, t0, prev = [], None, None, None
    for t, s in states:
        if s != cur:
            if cur is not None:
                out.append((cur, t0, t))
            cur, t0 = s, t
        prev = t
    if cur is not None:
        out.append((cur, t0, prev))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--box", default=",".join(map(str, DEFAULT_BOX)),
                    help="signal head in native pixels, x0,y0,x1,y1")
    ap.add_argument("--crop", choices=["head", "full"], default="head",
                    help="'head' sends a tight native crop -- the best case, and "
                         "the fair test of whether the lens is readable at all. "
                         "'full' sends the whole downscaled frame, which is what "
                         "the probe actually sees")
    ap.add_argument("--pad", type=int, default=30, help="context px around the head")
    ap.add_argument("--fps", type=float, default=1.0)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--batch", type=int, default=30, help="frames per call")
    ap.add_argument("--zoom", type=int, default=6,
                    help="nearest-neighbour magnification of the head crop. Adds "
                         "no information; makes the patch large enough that the "
                         "provider's own downscaling cannot destroy it")
    ap.add_argument("--save-crops", default=None, help="directory to write what was sent")
    ap.add_argument("--backend", default="gemini")
    ap.add_argument("--model", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    x0, y0, x1, y1 = (int(v) for v in a.box.split(","))
    from utils.video import probe as vprobe
    end = a.end if a.end is not None else (vprobe(a.video)["duration_s"] or 0.0)

    print(f"decoding {a.start:.0f}-{end:.0f}s at {a.fps:g} fps ...")
    frames = extract(a.video, a.start, end, a.fps)
    print(f"{len(frames)} frames, crop={a.crop}")

    from PIL import Image
    payload = []
    for t, im in frames:
        if a.crop == "head":
            c = im.crop((x0 - a.pad, y0 - a.pad, x1 + a.pad, y1 + a.pad))
            c = c.resize((c.width * a.zoom, c.height * a.zoom), Image.NEAREST)
        else:
            c = fit(im)
        payload.append((f"t={t:.2f}s", c))

    if a.save_crops:
        d = Path(a.save_crops); d.mkdir(parents=True, exist_ok=True)
        for (lab, img), (t, _) in zip(payload, frames):
            img.save(d / f"{t:08.2f}.png")
        print(f"crops -> {d}")

    load_env(); require_key(a.backend)
    backend = get_backend(a.backend, a.model)
    print(f"backend: {backend.name} / {backend.model}")

    states, tin, tout, calls = [], 0, 0, 0
    for i in range(0, len(payload), a.batch):
        chunk = payload[i:i + a.batch]
        ts = ", ".join(lab.split("=")[1] for lab, _ in chunk)
        text = (f"{len(chunk)} frames, timestamps in order: {ts}\n\n"
                f"Give one entry per frame, in the same order, using these exact "
                f"timestamps for t_sec.")
        res, usage = backend.run(SYSTEM, chunk, text, PhaseRead, 32000)
        calls += 1
        tin += usage.get("in") or 0
        tout += usage.get("out") or 0
        for f in res.frames:
            states.append((f.t_sec, f.state, f.confidence))
        print(f"  batch {calls}: {len(res.frames)}/{len(chunk)} frames"
              f"{'' if res.head_visible else '   [head reported NOT visible]'}")

    states.sort()
    merged = runs_from([(t, s) for t, s, _ in states])
    low = sum(1 for _, _, c in states if c == "low")
    unread = sum(1 for _, s, _ in states if s == "unreadable")

    out = Path(a.out) if a.out else Path("measurements") / (
        "signal-phase-" + Path(a.video).stem.split("D-")[-1].replace("_T-", "-") + "-vlm.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "topic": "pedestrian signal phase timeline, read by a VLM",
        "clip": a.video,
        "read_by": {"backend": backend.name, "model": backend.model,
                    "crop": a.crop, "zoom": a.zoom if a.crop == "head" else None,
                    "fps": a.fps, "box_native": [x0, y0, x1, y1], "calls": calls,
                    "tokens_in": tin, "tokens_out": tout},
        "judgement": "The head box was supplied, not found by the model, so this "
                     "measures reading the face and not locating it. Batching "
                     "means a frame is judged alongside its neighbours, which "
                     "may help or may let one frame's answer drag the next.",
        "per_frame": [{"t_sec": t, "state": s, "confidence": c} for t, s, c in states],
        "phases": [{"state": s, "t_start": t0, "t_end": t1} for s, t0, t1 in merged],
        "reliability": {
            "low_confidence_frames": low,
            "unreadable_frames": unread,
            "rerun_stability": "not measured — run this twice to find out",
        },
    }, indent=2) + "\n")
    print(f"\n{len(states)} frames read, {calls} call(s), {tin} in / {tout} out")
    print(f"low confidence: {low}   unreadable: {unread}")
    print(f"-> {out}")

    # --- compare against an arithmetic timeline if one exists -----------------
    arith = Path("measurements") / (out.name.replace("-vlm.json", ".json"))
    if not arith.exists():
        alt = list(Path("measurements").glob("signal-phase-*[!m].json"))
        arith = alt[0] if len(alt) == 1 else None
    if arith and arith.exists():
        ph = json.loads(arith.read_text())["phases"]
        def at(t):
            for p in ph:
                if p["t_start"] <= t < p["t_end"]:
                    return p["state"]
            return None
        MAP = {"WALK": "walk", "DONT_WALK": "dont_walk", "FLASHING": None}
        agree = dis = skip = 0
        rows = []
        for t, s, c in states:
            ref = MAP.get(at(t) or "", "?")
            if ref is None or s in ("unreadable",) or ref == "?":
                skip += 1; continue
            ok = (s == ref) or (s == "dark" and ref == "dont_walk")
            agree += ok; dis += (not ok)
            if not ok: rows.append((t, s, ref, c))
        tot = agree + dis
        print(f"\nagreement with {arith.name}: {agree}/{tot}"
              f" ({100*agree/max(1,tot):.0f}%), {skip} frames not comparable"
              f" (flashing phase or unreadable)")
        if rows:
            print(f"  {'t':>7} {'vlm':>12} {'arithmetic':>12}  conf")
            for t, s, ref, c in rows[:25]:
                print(f"  {t:7.2f} {s:>12} {ref:>12}  {c}")
            if len(rows) > 25:
                print(f"  ... {len(rows)-25} more")


if __name__ == "__main__":
    main()
