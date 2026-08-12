#!/usr/bin/env python3
"""How far along is a company vault? — one number that means something.

    python3 .tools/progress.py            # the summary
    python3 .tools/progress.py --open     # every file still carrying gaps
    python3 .tools/progress.py --by-role  # who has to answer how much

A shared vault ships as scaffolding: the structure is right and the house
rules are missing. Those missing rules come in TWO shapes, and an earlier
version of this script only counted one of them — which made a freshly
assembled vault report "1 open gap" when nine more were sitting in plain
sight:

  - **`<angle-bracket>` fields** — `owner: <role that owns this vault>`,
    `**Who may release content:** <role(s)>`. This is the common shape;
    a fresh company vault ships nine of them across three files, and
    `hygiene.py` cannot see them because `<role that owns this vault>` is
    a perfectly non-empty value.
  - **`TO FILL IN (role)` markers** (a translated vault uses its own
    word, e.g. `AUSFÜLLEN`) — used where the gap is a whole decision
    rather than one field, e.g. how copies are distributed.

Both are counted. Command examples in backticks (`search.py <terms>`) are
not, and neither are the template files, which keep their placeholders
forever by design.

Two numbers describe the vault's state, and only one of them matters.

  - **Gaps closed** is the easy number and the misleading one. A field
    stops being counted when someone types anything into it, and typing
    something is not the same as it being right.
  - **Files verified** is the honest one. A file counts only with
    `status: stable` AND a `verified:` line — a human read it and said
    yes. That is the line between a draft and something a colleague may
    act on, and nothing in this repo sets it automatically.

So the summary leads with the second number. A vault at "90% of gaps
closed, 0 files verified" is not 90% done; it is 0% done with tidier text.

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
# An unfilled `<…>` field, in the only two places one can legitimately sit:
# a frontmatter line, or a bold-label prose line. Anything inside backticks
# is a command example (`search.py <terms>`), never a gap — that distinction
# is the whole reason this is two narrow patterns instead of one broad one.
# FIELD deliberately does not require a closing `>`: the longest field in
# the shipped `About this vault.md` wraps across two lines, so every
# line-based scan that demanded `<…>` missed exactly the field that
# describes what the vault is FOR.
FIELD = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:[ \t]*<[^`\n]", re.M)
LABEL = re.compile(r"^\*\*[^*\n]+:\*\*[ \t]*<[^`\n]", re.M)
SKIP_DIRS = {".git", ".obsidian", ".tools", ".claude", "_templates", "90-archive"}
# Files that TALK about the gaps rather than carrying one, and files whose
# placeholders are permanent by design. Counting the rules sheet or a note
# template as an open gap would mean the vault can never reach zero.
SKIP_FILES = {"CLAUDE.md", "_template.md"}


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
    gaps = collections.Counter()          # file -> gaps of both shapes
    roles = collections.Counter()
    unaddressed = fields = markers = 0

    for rel, text in walk(vault):
        notes += 1
        fm = frontmatter(text)
        is_stable = re.search(r"^status:\s*stable\b", fm, re.M) is not None
        is_verified = re.search(r"^verified:\s*\S", fm, re.M) is not None
        stable += is_stable
        verified += is_stable and is_verified
        found = GAP.findall(text)
        orphans = ORPHAN.findall(text)
        # `<…>` fields: frontmatter lines are matched against the frontmatter
        # block only, so a `type: knowledge | source` example further down the
        # body cannot be mistaken for one.
        open_fields = len(FIELD.findall(fm)) + len(LABEL.findall(text))
        if found or orphans or open_fields:
            gaps[rel] = len(found) + len(orphans) + open_fields
            for who in found:
                for part in re.split(r"\s*/\s*", who.strip()):
                    roles[part.strip()] += 1
            unaddressed += len(orphans)
            fields += open_fields
            markers += len(found) + len(orphans)

    if not notes:
        print(f"No notes found under {vault}")
        return 1

    total_gaps = sum(gaps.values())
    print(f"\n  {verified} of {notes} notes verified"
          f"   ({stable} stable, {verified} of those confirmed by a human)")
    print(f"  {total_gaps} open gaps in {len(gaps)} files"
          f"   ({fields} unfilled <…> fields, {markers} marked TO FILL IN)")
    if total_gaps and not verified:
        print("\n  Nothing is company truth yet. The first verified process")
        print("  note is the milestone — not the last deleted marker.")
    elif verified:
        share = 100.0 * verified / notes
        print(f"\n  {share:.0f}% of this vault can be acted on.")

    if a.by_role and (roles or fields):
        print("\n  Gaps by who has to answer:")
        for who, n in roles.most_common():
            print(f"    {n:4}  {who}")
        if unaddressed:
            print(f"    {unaddressed:4}  (no role named — these need one)")
        if fields:
            # A `<…>` field never names a role; the file it sits in does.
            # --open is the list that actually helps here.
            print(f"    {fields:4}  (unfilled <…> fields — see --open)")

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
