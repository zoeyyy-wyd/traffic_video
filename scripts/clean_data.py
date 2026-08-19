#!/usr/bin/env python3
"""Report, and optionally remove, video files that are not usable.

Written after the 6.5 GB upload left 74 zero-byte placeholders behind. It also
catches the failure that is easier to miss: a file that is not empty but was
truncated in transfer. An mp4 keeps its index at the end of the file, so a
partial copy usually will not open at all -- but it still occupies bytes and
still looks fine in a directory listing.

Dry run by default. Nothing is deleted without --apply.

  python scripts/clean_data.py data/12thFBotwinik            # report only
  python scripts/clean_data.py data/12thFBotwinik --deep     # also decode a frame
  python scripts/clean_data.py data/12thFBotwinik --apply    # delete empty files
  python scripts/clean_data.py data/12thFBotwinik --apply --status empty,unreadable
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.video import verify

VIDEO_EXT = {".mp4", ".mkv", ".avi", ".mov", ".ts", ".m4v"}
# Deleted by default: a zero-byte file carries no information and nothing can
# be recovered from it. Everything else is reported but kept, because a broken
# file is evidence about the transfer and may be worth re-fetching rather than
# silently dropping.
DEFAULT_REMOVE = {"empty"}


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("root", help="directory to scan")
    p.add_argument("--deep", action="store_true",
                   help="also decode one frame per file (slower, catches more)")
    p.add_argument("--apply", action="store_true",
                   help="actually delete; without it nothing is removed")
    p.add_argument("--status", default=",".join(sorted(DEFAULT_REMOVE)),
                   help=f"comma-separated statuses to delete "
                        f"(default: {','.join(sorted(DEFAULT_REMOVE))}). "
                        f"choices: empty, unreadable, no_duration, undecodable")
    p.add_argument("--keep-dirs", action="store_true",
                   help="do not remove directories left empty")
    a = p.parse_args()

    root = Path(a.root).resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")
    remove = {s.strip() for s in a.status.split(",") if s.strip()}
    bad = remove - {"empty", "unreadable", "no_duration", "undecodable"}
    if bad:
        sys.exit(f"unknown status: {', '.join(sorted(bad))}")

    files = sorted(f for f in root.rglob("*")
                   if f.is_file() and not f.is_symlink()
                   and f.suffix.lower() in VIDEO_EXT)
    if not files:
        sys.exit(f"no video files under {root}")

    print(f"scanning {len(files)} file(s) under {root}"
          f"{' (deep)' if a.deep else ''}\n")

    groups = {}
    for i, f in enumerate(files, 1):
        r = verify(str(f), deep=a.deep)
        groups.setdefault(r["status"], []).append(r)
        if i % 50 == 0 or i == len(files):
            print(f"  {i}/{len(files)}", end="\r", flush=True)
    print(" " * 30, end="\r")

    print(f"{'status':<12} {'files':>6} {'size':>10}")
    print("-" * 32)
    for status in ("ok", "empty", "unreadable", "no_duration", "undecodable"):
        g = groups.get(status)
        if g:
            print(f"{status:<12} {len(g):6d} {human(sum(r['size'] for r in g)):>10}"
                  + ("   <- will delete" if status in remove and a.apply else
                     "   <- would delete" if status in remove else ""))

    doomed = [r for s in remove for r in groups.get(s, [])]
    if not doomed:
        print("\nnothing to remove.")
        return

    print(f"\n{len(doomed)} file(s), {human(sum(r['size'] for r in doomed))}:")
    for r in doomed[:15]:
        print(f"  [{r['status']}] {Path(r['path']).relative_to(root)}  ({r['detail']})")
    if len(doomed) > 15:
        print(f"  ... and {len(doomed) - 15} more")

    if not a.apply:
        print(f"\ndry run -- nothing deleted. re-run with --apply to remove.")
        return

    removed = freed = 0
    for r in doomed:
        try:
            os.remove(r["path"])
            removed += 1
            freed += r["size"]
        except OSError as e:
            print(f"  failed: {r['path']}: {e}", file=sys.stderr)
    print(f"\ndeleted {removed} file(s), freed {human(freed)}")

    if not a.keep_dirs:
        pruned = 0
        # deepest first, so a directory emptied by pruning its children goes too
        for d in sorted((d for d in root.rglob("*") if d.is_dir()),
                        key=lambda p: -len(p.parts)):
            try:
                d.rmdir()      # only succeeds when already empty
                pruned += 1
                print(f"  removed empty dir: {d.relative_to(root)}")
            except OSError:
                pass
        if pruned:
            print(f"pruned {pruned} empty director{'y' if pruned == 1 else 'ies'}")


if __name__ == "__main__":
    main()
