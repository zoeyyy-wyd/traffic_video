"""Camera facts computed from the pixels, as inputs to the pipeline (they feed
the scene block via build_scene.py). Camera-constant only. Reproducible is not
authoritative: nothing here scores a run -- the hand-filled sheet does.
"""
from typing import Dict, Optional, Sequence, Tuple

import numpy as np
from PIL import Image

from .video import extract, probe

# --- signal heads, native pixels (x0, y0, x1, y1), 12F-Ams view --------------
HEADS = {
    "ped_E":    (2380, 365, 2440, 420),
    "ped_NW":   (1585, 320, 1645, 375),
    "veh_mast": (1930, 600, 2010, 680),
    "veh_NE":   (2255, 215, 2305, 285),
}

# --- tripwire bands, native pixels. Two per carriageway: upstream, downstream.
BANDS = {
    "avenue-east": [(1700, 1050, 2100, 1150), (1550, 1350, 1950, 1450)],
    "avenue-west": [(1350, 1050, 1690, 1150), (1200, 1350, 1540, 1450)],
    "cross-north": [(1150, 270, 1400, 380),   (2000, 270, 2250, 380)],
    "cross-south": [(1150, 390, 1400, 520),   (2000, 390, 2250, 520)],
}
_VERTICAL = {"avenue-east", "avenue-west"}


def _rb(img: Image.Image, box) -> float:
    a = np.asarray(img.crop(box).convert("RGB"), float).reshape(-1, 3)
    return a[:, 0].mean() - a[:, 2].mean()


def signal_legibility(video: str, states_at: Tuple[float, float] = (120.0, 138.0),
                      sample_every: float = 6.0, heads: Dict = None,
                      min_range: float = 15.0) -> Dict:
    """Which signal faces show a lens to this camera, and how big is it.

    A lit face changes state; a housing does not. Differencing two frames from
    different phases finds the lit pixels, and their box measures them -- no
    hand-drawn region.

    Two guards, both learned from getting it wrong. The state is read on the
    LOCATED patch, not on the whole head: a lit screen is ~8x10 px inside a
    60x55 housing and its swing is diluted to nothing by the surrounding paint,
    which once made the readable head look unreadable. And a changing region
    covering more than 40% of the head is rejected -- at this camera that is a
    vehicle passing behind it, not a lens.
    """
    heads = heads or HEADS
    ta, tb = states_at
    fa, fb = extract(video, ta, ta + 0.6, 1.0), extract(video, tb, tb + 0.6, 1.0)
    if not fa or not fb:
        raise RuntimeError(f"{video}: could not decode frames at {ta}s / {tb}s")
    A, B = fa[0][1], fb[0][1]

    located = {}
    for name, box in heads.items():
        d = np.abs(np.asarray(A.crop(box).convert("RGB"), float)
                   - np.asarray(B.crop(box).convert("RGB"), float)).mean(axis=2)
        ys, xs = np.where(d > d.max() * 0.45) if d.max() > 8 else ((), ())
        if not len(xs):
            located[name] = None
            continue
        w, h = int(xs.max() - xs.min()) + 1, int(ys.max() - ys.min()) + 1
        located[name] = None if w * h > 0.40 * d.size else (
            box[0] + int(xs.min()), box[1] + int(ys.min()),
            box[0] + int(xs.max()) + 1, box[1] + int(ys.max()) + 1)

    end = probe(video)["duration_s"] or 0.0
    series = {k: [] for k in heads}
    for _, im in extract(video, 0.0, end, 1.0 / sample_every):
        for k, box in heads.items():
            series[k].append(_rb(im, located[k] or box))

    out = {}
    for name, box in heads.items():
        rng = float(np.ptp(series[name]))
        scr = located[name]
        if scr is None or rng < min_range:
            out[name] = {"readable": False, "rb_range_over_clip": round(rng, 1)}
            continue
        ladder = []
        for sc in (1.00, 0.73, 0.41):
            if sc < 1.0:
                sa = A.resize((int(A.width * sc), int(A.height * sc)), Image.LANCZOS)
                sb = B.resize((int(B.width * sc), int(B.height * sc)), Image.LANCZOS)
                sb_ = tuple(max(int(v * sc), 0) for v in scr)
                sbox = (sb_[0], sb_[1], max(sb_[0] + 1, sb_[2]), max(sb_[1] + 1, sb_[3]))
            else:
                sa, sb, sbox = A, B, scr
            ladder.append({"scale": sc,
                           "separation": round(abs(_rb(sa, sbox) - _rb(sb, sbox)), 1)})
        out[name] = {"readable": True, "rb_range_over_clip": round(rng, 1),
                     "lit_glyph_native": [scr[2] - scr[0], scr[3] - scr[1]],
                     "lit_glyph_box_native": list(scr),
                     "downscale_ladder": ladder}
    return out


def flow_direction(video: str, fps: float = 4.0, maxlag: int = 24,
                   min_r: float = 0.45, bands: Dict = None) -> Dict:
    """Direction of travel per carriageway, in IMAGE SPACE.

    Virtual tripwires: motion energy is mean |frame(k+1) - frame(k)| in a band.
    Two bands per carriageway, cross-correlated; the leading band is the one
    traffic reaches first, so the lag's sign gives the direction.

    Optical flow was tried and failed twice. At 2 fps a vehicle moves ~100 px at
    960 px width, outside any reasonable phase-correlation window; widen the
    window and it is then >95% static asphalt, so the peak locks onto zero
    shift. A tripwire does not care what is in the band, only when it changes.

    Image space, not compass: which way is north is not established from this
    view, and a guessed compass label would be handed on as fact.
    """
    bands = bands or BANDS
    W, H = 480, 270
    S = 3840 // W
    end = probe(video)["duration_s"] or 0.0
    stack = np.stack([np.asarray(im.convert("L").resize((W, H), Image.BILINEAR),
                                 dtype=np.uint8)
                      for _, im in extract(video, 0.0, end, fps)]).astype(np.float32)
    d = np.abs(np.diff(stack, axis=0))

    def energy(b):
        x0, y0, x1, y1 = b
        return d[:, y0 // S:y1 // S, x0 // S:x1 // S].mean(axis=(1, 2))

    def lag(a, b):
        a = (a - a.mean()) / (a.std() + 1e-9)
        b = (b - b.mean()) / (b.std() + 1e-9)
        best = (0, -9.0)
        for L in range(-maxlag, maxlag + 1):
            c = (np.corrcoef(a[:len(a) - L], b[L:])[0, 1] if L >= 0
                 else np.corrcoef(a[-L:], b[:len(b) + L])[0, 1])
            if c > best[1]:
                best = (L, float(c))
        return best

    out = {}
    for name, (up, down) in bands.items():
        L, r = lag(energy(up), energy(down))
        vertical = name in _VERTICAL
        if abs(L) >= maxlag or r < min_r or L == 0:
            why = ("correlation too weak" if r < min_r else
                   "lag pinned at the search limit" if abs(L) >= maxlag else "no lag")
            out[name] = {"status": "FAILED", "why": why,
                         "lag_frames": L, "r": round(r, 3), "direction": None}
        else:
            out[name] = {"status": "ok", "lag_frames": L, "r": round(r, 3),
                         "direction": (("DOWN the frame" if L > 0 else "UP the frame")
                                       if vertical else
                                       ("LEFT to RIGHT" if L > 0 else "RIGHT to LEFT"))}
    return out


def signal_phase(video: str, screen: Sequence[int] = None, head: Sequence[int] = None,
                 states_at: Tuple[float, float] = (120.0, 138.0), fps: float = 2.0,
                 rb_hand: float = 45.0, min_run: float = 1.6) -> Dict:
    """Pedestrian phase timeline for ONE recording.

    Deliberately not part of `as_scene_text`: a phase timeline belongs to the
    clip it was read from, and a scene block is reused across clips.

    THREE STATES, NOT TWO. The countdown flashes, so the screen is dark for half
    of it. Colour separates the hand from everything else; luminance splits what
    remains into the white figure and the dark half of a flash. A two-level
    threshold on colour alone turns one 12 s countdown into six phantom WALKs.

    The luminance cut is taken over the non-hand samples only, midway between
    their own darkest and brightest. A fixed percentile over the whole clip
    moves with how long the WALK happened to be, and a long WALK then pushes its
    own samples below the cut and relabels itself as flashing.
    """
    if screen is None:
        head = tuple(head or HEADS["ped_E"])
        ta, tb = states_at
        A = extract(video, ta, ta + 0.6, 1.0)[0][1]
        B = extract(video, tb, tb + 0.6, 1.0)[0][1]
        d = np.abs(np.asarray(A.crop(head).convert("RGB"), float)
                   - np.asarray(B.crop(head).convert("RGB"), float)).mean(axis=2)
        ys, xs = np.where(d > d.max() * 0.45)
        if not len(xs):
            raise RuntimeError("nothing changed between those two frames -- are "
                               "they in different phases?")
        screen = (head[0] + int(xs.min()), head[1] + int(ys.min()),
                  head[0] + int(xs.max()) + 1, head[1] + int(ys.max()) + 1)

    end = probe(video)["duration_s"] or 0.0
    rows = []
    for t, im in extract(video, 0.0, end, fps):
        a = np.asarray(im.crop(screen).convert("RGB"), float).reshape(-1, 3)
        rows.append((t, a[:, 0].mean() - a[:, 2].mean(), a.mean()))

    rest = [l for _, rb, l in rows if rb <= rb_hand]
    cut = (min(rest) + max(rest)) / 2 if rest else 0.0
    states = [(t, "DONT_WALK" if rb > rb_hand else
               ("WALK" if lum > cut else "FLASHING")) for t, rb, lum in rows]

    runs, cur, t0, last = [], None, None, None
    for t, st in states:
        if st != cur:
            if cur is not None:
                runs.append([cur, t0, t])
            cur, t0 = st, t
        last = t
    if cur is not None:
        runs.append([cur, t0, last])

    # A RUN OF SHORT RUNS is what flashing looks like, and that block is what
    # collapses -- not the long run beside it. Folding each short run into its
    # predecessor relabels the neighbour, which once turned a correct 17 s WALK
    # into flashing because a half-second blip followed it.
    out, i = [], 0
    while i < len(runs):
        if runs[i][2] - runs[i][1] < min_run:
            j = i
            while j < len(runs) and runs[j][2] - runs[j][1] < min_run:
                j += 1
            out.append(["FLASHING", runs[i][1], runs[j - 1][2]])
            i = j
        else:
            out.append(runs[i]); i += 1
    merged = []
    for r in out:
        if merged and merged[-1][0] == r[0]:
            merged[-1][2] = r[2]
        else:
            merged.append(r)

    phases = [{"state": a_, "t_start": round(b, 2), "t_end": round(c, 2)}
              for a_, b, c in merged if c > b]
    walks = [p for p in phases if p["state"] == "WALK"]
    return {"screen_native": list(screen), "phases": phases,
            "cycle_s": round(walks[1]["t_start"] - walks[0]["t_start"], 1)
            if len(walks) > 1 else None}


def as_scene_text(legibility: Optional[Dict] = None,
                  flow: Optional[Dict] = None) -> str:
    """Render measurements as plain factual sentences for the scene block.

    Failed measurements are omitted, not softened. A carriageway whose direction
    could not be recovered must not appear as a hedge inside a block the model
    is told to treat as established: an uncertain fact stated flatly is worse
    than a missing one, because nothing downstream can tell the two apart.
    """
    out = []
    if legibility:
        veh_dark = [k for k, v in legibility.items()
                    if k.startswith("veh") and not v["readable"]]
        ped_lit = [k for k, v in legibility.items()
                   if k.startswith("ped") and v["readable"]]
        if veh_dark:
            out.append("The vehicle signal heads are seen from above and behind. "
                       "No vehicle signal lens is visible from this camera at any "
                       "time, so the colour of a vehicle signal cannot be read and "
                       "must not be reported.")
        if ped_lit:
            w, h = legibility[ped_lit[0]]["lit_glyph_native"]
            out.append(f"{len(ped_lit)} pedestrian signal head(s) are legible. The "
                       f"lit glyph is a small coloured patch, about {w}x{h} pixels "
                       f"in the full-resolution frame. Orange means the raised hand "
                       f"or a countdown numeral; white means the walking figure. At "
                       f"this size the two are told apart by colour, never by shape.")
    if flow:
        ok = {k: v for k, v in flow.items() if v.get("status") == "ok"}
        av = {k.split("-")[1]: v["direction"] for k, v in ok.items()
              if k.startswith("avenue")}
        if len(av) == 2 and len(set(av.values())) == 2:
            out.append(f"The vertical street is two-way, divided by a double yellow "
                       f"line. Traffic in the lanes on one side runs "
                       f"{list(av.values())[0].lower()}; on the other side it runs "
                       f"{list(av.values())[1].lower()}.")
        for k, v in ok.items():
            if k.startswith("cross"):
                out.append(f"On the horizontal street, the {k.split('-')[1]}ern "
                           f"lanes carry traffic {v['direction'].lower()}.")
    return "\n\n".join(out)
