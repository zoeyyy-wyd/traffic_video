#!/usr/bin/env python3
"""Rewrite hand-written scene notes into a prompt block, and show what changed.

    python scripts/build_scene.py scene/12F-Ams.txt

Reads rough notes, asks the model to tidy them into prose the probe can put in
its system prompt, and writes <stem>.built.md next to the source.

The rewrite is constrained to ADD NOTHING. That constraint is the point: every
sentence in the built file is handed to the grounding model as established
fact, so a detail invented during tidying becomes a confident wrong label on
every run afterwards. The script prints the sentences it could not trace back
to the source so the addition is visible rather than buried, and refuses to
write when the rewrite is longer than the source by more than --slack.

    --dry-run   show the rewrite and the diff, write nothing
    --slack N   allow the rewrite to be N% longer in words (default 40)
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.env import load_env, require_key
from utils.vlm import get_backend

SYSTEM = """You tidy rough field notes into a short factual briefing.

Rules, in order of importance:

1. ADD NOTHING. Do not introduce a fact, a number, a direction, a street name,
   or a qualifier that is not in the notes. If the notes are vague, the output
   stays vague. You are rewriting, not researching, and you have not seen the
   place being described.
2. Drop nothing that carries information.
3. Plain declarative sentences, grouped under the headings the notes use. No
   preamble, no summary, no markdown headers beyond the ones implied.
4. If the notes contradict themselves, keep both statements and say they
   conflict. Do not pick one."""


class Built(__import__("pydantic").BaseModel):
    briefing: str
    added_nothing: bool
    notes_that_conflict: list[str]


def words(t):
    return re.findall(r"[a-z0-9']+", t.lower())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("notes")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--slack", type=int, default=40)
    ap.add_argument("--backend", default="gemini")
    ap.add_argument("--model", default=None)
    a = ap.parse_args()

    src = Path(a.notes)
    raw = [ln for ln in src.read_text().splitlines() if not ln.strip().startswith("#")]
    body = "\n".join(raw).strip()
    if not body:
        sys.exit(f"{src} has no content outside comments — write some notes first.")

    load_env()
    require_key(a.backend)
    backend = get_backend(a.backend, a.model)
    res, usage = backend.run(SYSTEM, [], f"Notes:\n\n{body}", Built, 8000)

    out_words, in_words = words(res.briefing), words(body)
    growth = 100 * (len(out_words) - len(in_words)) / max(1, len(in_words))
    new = sorted(set(out_words) - set(in_words) - set(
        "a an the and or of in on at to is are was were it its this that with "
        "for from by as not no but they them their there which while".split()))

    print(f"source {len(in_words)} words -> rewrite {len(out_words)} words "
          f"({growth:+.0f}%)")
    if new:
        print(f"\nwords in the rewrite that are not in your notes ({len(new)}):")
        print("  " + ", ".join(new))
        print("  ^ check these. Anything here that is a fact rather than glue is "
              "something the model added.")
    if res.notes_that_conflict:
        print("\nconflicts it flagged:")
        for c in res.notes_that_conflict:
            print(f"  - {c}")
    print("\n" + "-" * 70)
    print(res.briefing)
    print("-" * 70)

    if growth > a.slack:
        sys.exit(f"\nrewrite is {growth:.0f}% longer than the source "
                 f"(limit {a.slack}%). Not written — it is padding or inventing.")
    if a.dry_run:
        print("\n--dry-run: nothing written")
        return
    out = src.with_suffix(".built.md")
    out.write_text(res.briefing.strip() + "\n")
    print(f"\n-> {out}   (pass it to the probe with --scene {out})")
    if usage.get("in"):
        print(f"   {usage['in']} in / {usage['out']} out tokens")


if __name__ == "__main__":
    main()
