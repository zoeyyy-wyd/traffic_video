#!/usr/bin/env python3
"""Generate a blank ground-truth sheet from a query set.

The sheet is the query file copied verbatim with fill-in slots under each
category, so the labels line up with the categories the probe was asked about
and scoring is a line-by-line comparison rather than a translation.

    python scripts/make_gt.py queries/events-key.txt videos/<clip>.mp4
    python scripts/make_gt.py queries/events-key.txt videos/<clip>.mp4 -n 5

Writes notes/ground-truth-<clip stem minus prefix>.txt unless -o is given.
Refuses to overwrite a sheet that already has entries in it -- a half-filled
sheet is hours of work and is not recoverable from anywhere else.
"""
import argparse
import re
import sys
from pathlib import Path

HEAD = """# GROUND TRUTH — {clip}
#
# Reviewer:
# Date:
# Watched at:
#
# LABEL BLIND. Do not open results/*/summary.md while filling this in. Ground
# truth read after seeing the model's answer is not independent of it.
#
# HOW TO FILL. Under each category line:
#
#   occurred:   yes | no | not-reviewed
#
#     yes            it happens -- one numbered line per instance
#     no             you swept the WHOLE clip for it and it does not happen.
#                    Only this turns a model hit into a FABRICATION rather than
#                    merely unverified.
#     not-reviewed   you did not check; leave it, it is dropped from scoring.
#                    A wrong `no` corrupts the score, so guess at nothing.
#
#   t=  start and end, seconds from clip start
#   who: the road user, specific enough that someone else finds the same one
#   ph: pedestrian phase at that moment, for the crosswalk involved:
#       W = white walking figure, F = flashing countdown, R = red hand, - = n/a
#       Only needed where the phase changes what the event means (a vehicle on
#       the crosswalk markings obstructs nobody under a red hand). Leave `-`
#       everywhere else; it is also recoverable from the measured timeline.
#   ?:  certain | probable | ambiguous  (ambiguous is recorded, not scored)
#
# MULTI-LABEL: an instance may satisfy several categories. Record it under
# EVERY category it satisfies -- do not pick one. Scoring is per category and
# independent, so a single-label sheet manufactures false positives.
#
# Category text below is verbatim from {qf}.
# ---------------------------------------------------------------------------
"""

TAIL = """
# ---------------------------------------------------------------------------
# SIGNAL PHASE COUPLING  (free while watching; decides whether vehicle-signal
# events ever become askable here -- the pedestrian head is legible from this
# camera, the vehicle heads are not). Watch the east-corner pedestrian signal.
#
#   white walking figure -> which traffic is moving:
#   red hand             -> which traffic is moving:
#   consistent across cycles?  yes / no:
#
# ---------------------------------------------------------------------------
# SCENE NOTES  (anything that changes what can be asked)
#   -
#   -
#
# ---------------------------------------------------------------------------
# EVENTS SEEN THAT NO CATEGORY COVERS
# The vocabulary is a guess; this section is what the next version is built from.
#   t=        -          s
#   t=        -          s
#   t=        -          s
"""

SLOT = "      {i})  t=        -          s   who:                        ph:      ?:"


def filled(path: Path) -> bool:
    """True if any slot in an existing sheet has been written into."""
    for line in path.read_text().splitlines():
        s = line.strip()
        if s.startswith("#"):
            continue
        if re.match(r"occurred:\s*\S", s):
            return True
        if re.match(r"\d+\)\s+t=\s*[\d.]", s):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("queries", help="query set, 'axis | text' per line")
    ap.add_argument("clip", help="video the sheet is for (name only, not read)")
    ap.add_argument("-n", "--slots", type=int, default=3,
                    help="blank instance lines per category (default 3)")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("-f", "--force", action="store_true",
                    help="overwrite a sheet that already has entries")
    a = ap.parse_args()

    qf = Path(a.queries)
    clip = Path(a.clip).name
    out = Path(a.out) if a.out else Path("notes") / (
        "ground-truth-" + re.sub(r"^.*?D-|\.mp4$", "", clip).replace("_T-", "-") + ".txt")

    if out.exists() and filled(out) and not a.force:
        sys.exit(f"{out} already has entries in it. Refusing to overwrite.\n"
                 f"  Move it aside, or pass --force if you really mean to.")

    lines = [HEAD.format(clip=clip, qf=qf)]
    n = 0
    for ln in qf.read_text().splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            lines.append(ln)
            continue
        n += 1
        lines.append(ln)
        lines.append("    occurred:")
        lines.extend(SLOT.format(i=i) for i in range(1, a.slots + 1))
        lines.append("")
    lines.append(TAIL)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    print(f"{n} categories from {qf} -> {out}")


if __name__ == "__main__":
    main()
