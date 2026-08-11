#!/usr/bin/env python3
"""How far along is a company vault? — one number that means something.

    python3 .tools/progress.py            # the summary
    python3 .tools/progress.py --open     # every file still carrying gaps
    python3 .tools/progress.py --by-role  # who has to answer how much

A shared vault ships as scaffolding: the structure is right, the house
rules are missing, and every missing rule sits in the text as an
`TO FILL IN` marker (a translated vault uses its own word, e.g. `AUSFÜLLEN`). Two numbers describe that state, and
only one of them matters.

  - **Gaps closed** is the easy number and the misleading one. Markers
    disappear when someone deletes them, and a deleted marker is not an
    answer.
  - **Files verified** is the honest one. A file counts only with
    `status: stable` AND a `verified:` line — a human read it and said
    yes. That is the line between a draft and something a colleague may
    act on, and nothing in this repo sets it automatically.

So the summary leads with the second number. A vault at "90% of markers
gone, 0 files verified" is not 90% done; it is 0% done with tidier text.

Exit code is 0 unless something is actually wrong with the vault.
"""
import argparse
import collections
import os
import re
import sys

# A real gap always names who answers it: `TO FILL IN (bookkeeping): …`.
# The bare word appears far more often in prose ABOUT the gaps — every
# process note explains its own markers, and the roles folder does it once
# per file. Counting those made the vault look a quarter emptier than it
# is, and no amount of answering would ever have driven the number down.
GAP = re.compile(r"(?:TO FILL IN|AUSFÜLLEN)\s*\(([^)]{1,60})\)")
# A placeholder that forgot its role: the marker sits in a quoted line and
# is neither bold nor code — that is a real defect, nobody knows who to ask.
# Case-SENSITIVE on purpose. In a translated vault the marker word is often
# an ordinary verb in that language — German `ausfüllen` ("to fill in")
# appears in normal sentences, and matching case-insensitively reported two
# perfectly fine ones as defects. The shouting spelling is the marker.
ORPHAN = re.compile(r"^\s*>.*(?<![*`])(?:TO FILL IN|AUSFÜLLEN)(?![*`])(?!\s*\()", re.M)
SKIP_DIRS = {".git", ".obsidian", ".tools", ".claude", "_templates", "90-archive"}
# Files that TALK about the markers rather than carrying one. Counting the
# instruction sheet as an open gap would mean the vault can never reach zero.
SKIP_FILES = {"ERSTE-ANTWORTEN.md", "FIRST-ANSWERS.md", "CLAUDE.md",
              "FUER-VERANTWORTLICHE.md", "FOR-MAINTAINERS.md"}


def frontmatter(text):
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) > 2 else ""


def walk(vault):
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in sorted(files):
            if not name.endswith(".md") or name in SKIP_FILES:
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, vault)
            try:
                with open(path, encoding="utf-8-sig", errors="ignore") as fh:
                    yield rel, fh.read()
            except OSError:
                continue


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("vault", nargs="?", default=".")
    ap.add_argument("--open", action="store_true", help="list files with gaps")
    ap.add_argument("--by-role", action="store_true", help="group gaps by who answers")
    a = ap.parse_args()
    vault = os.path.expanduser(a.vault)

    notes = verified = stable = 0
    gaps = collections.Counter()          # file -> markers
    roles = collections.Counter()
    unaddressed = 0

    for rel, text in walk(vault):
        notes += 1
        fm = frontmatter(text)
        is_stable = re.search(r"^status:\s*stable\b", fm, re.M) is not None
        is_verified = re.search(r"^verified:\s*\S", fm, re.M) is not None
        stable += is_stable
        verified += is_stable and is_verified
        found = GAP.findall(text)
        orphans = ORPHAN.findall(text)
        if found or orphans:
            gaps[rel] = len(found) + len(orphans)
            for who in found:
                for part in re.split(r"\s*/\s*", who.strip()):
                    roles[part.strip()] += 1
            unaddressed += len(orphans)

    if not notes:
        print(f"No notes found under {vault}")
        return 1

    total_gaps = sum(gaps.values())
    print(f"\n  {verified} of {notes} notes verified"
          f"   ({stable} stable, {verified} of those confirmed by a human)")
    print(f"  {total_gaps} open gaps in {len(gaps)} files")
    if total_gaps and not verified:
        print("\n  Nothing is company truth yet. The first verified process")
        print("  note is the milestone — not the last deleted marker.")
    elif verified:
        share = 100.0 * verified / notes
        print(f"\n  {share:.0f}% of this vault can be acted on.")

    if a.by_role and roles:
        print("\n  Gaps by who has to answer:")
        for who, n in roles.most_common():
            print(f"    {n:4}  {who}")
        if unaddressed:
            print(f"    {unaddressed:4}  (no role named — these need one)")

    if a.open and gaps:
        print("\n  Files with open gaps (most first):")
        for rel, n in gaps.most_common():
            print(f"    {n:4}  {rel}")

    if not a.open and not a.by_role and gaps:
        print("\n  --open shows which files, --by-role shows who to ask.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
