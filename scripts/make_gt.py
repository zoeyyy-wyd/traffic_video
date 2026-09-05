#!/usr/bin/env python3
"""Generate a blank ground-truth sheet from a query set.

  python scripts/make_gt.py queries/events-key.txt videos/<clip>.mp4

Categories are the query file verbatim, so scoring is line-by-line. Refuses to
overwrite a sheet that already has entries; --force to override.
"""
import argparse
import re
import sys
from pathlib import Path

HEAD = """# GROUND TRUTH — {clip}
# Reviewer / date:
#
# Fill BLIND: do not read the model's answers first.
# occurred:  yes | no | not-reviewed
#   no only after sweeping the WHOLE clip for it -- that is what turns a model
#   hit into a fabrication. Unsure? leave not-reviewed; it is dropped, not
#   guessed.
# Slots: t= start - end (seconds or MM:SS), who: (identifiable), ?: certain |
# probable | ambiguous. An instance fitting two categories goes under both.
# Categories below are verbatim from {qf}.
"""

TAIL = """
# ---------------------------------------------------------------------------
# SIGNAL PHASE COUPLING (free while watching): which traffic moves while the
# pedestrian signal shows the walking figure? / the red hand?
#   walking figure ->
#   red hand       ->
#   consistent across cycles?  yes / no:
#
# SCENE NOTES (anything that changes what can be asked):
#   -
#
# EVENTS NO CATEGORY COVERS (the next vocabulary is built from these):
#   t=        -          s
#   t=        -          s
"""

SLOT = "      {i})  t=        -          s   who:                              ?:"


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
    out = Path(a.out) if a.out else Path("ground-truth") / (
        re.sub(r"^.*?D-|\.mp4$", "", clip).replace("_T-", "-") + ".txt")

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
