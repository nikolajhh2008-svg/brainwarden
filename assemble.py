#!/usr/bin/env python3
"""Assemble a vault from the template — one command instead of four.

    python3 assemble.py ~/Brain personal
    python3 assemble.py ~/Brain-work professional
    python3 assemble.py ~/Firma company

Why this exists rather than a sequence of `cp` and `rm` commands:

  - **One permission prompt instead of four.** Visual processing of warning
    dialogs drops off measurably from the SECOND one onward (Anderson et
    al., CHI 2015). A setup that asks twenty times has trained the person
    to click through by dialog three — and the one they stop reading first
    is the one that matters.
  - **No `rm -rf` on the path a first-time user walks.** The old sequence
    copied everything and then deleted the scaffolding, which meant the
    scariest-looking command in the whole setup arrived while the human was
    still deciding whether to trust this thing at all. Here the scaffolding
    is simply never copied.
  - **The same on every platform.** No BSD-vs-GNU `cp`, no `rm -rf` that
    behaves differently under PowerShell.
  - **It refuses to overwrite.** Existing files are never touched, and the
    script says which ones it skipped. Adopting an existing vault stays a
    deliberate act, not an accident.

It does exactly one job: put the right files in the right place. Filling
them in — the questions, the first notes, the language — is the setup
runbook's job, and it needs a human in the conversation.
"""
import argparse
import os
import shutil
import sys

MODES = ("personal", "professional", "company")

# Files the company overlay replaces wholesale, and files that belong to a
# PERSONAL work brain and have no place in a shared one. Kept here rather
# than in three separate documents, because that list has drifted before.
COMPANY_DROPS = [
    "10-projects", "20-areas", "30-knowledge/people", "60-contribution",
    "About me.md", "handover.md",
    "_templates/person-note.md", "_templates/project-note.md",
    "_templates/area-note.md", "_templates/journal-entry.md",
    "_templates/contribution-entry.md", "_templates/learning-note.md",
    "_templates/meeting-note.md",
]


def copy_tree(src, dst, skipped, overwrite=False):
    """Copy contents of src into dst. Never overwrites unless told to."""
    for root, dirs, files in os.walk(src):
        # `modules/` is kit scaffolding; the rest is build litter. Git ignores
        # bytecode caches, so a fresh clone has none — but anyone who ran the
        # tools once and then assembled a second vault carried them along.
        dirs[:] = [d for d in dirs
                   if d not in ("modules", "__pycache__", ".git")]
        rel = os.path.relpath(root, src)
        target_dir = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(target_dir, exist_ok=True)
        for name in files:
            if name == ".DS_Store" or name.endswith((".pyc", ".pyo", ".swp")):
                continue
            target = os.path.join(target_dir, name)
            if os.path.exists(target) and not overwrite:
                skipped.append(os.path.relpath(target, dst))
                continue
            shutil.copy2(os.path.join(root, name), target)


def keep_kit_extras(here, vault):
    """Copy the two kit files a vault still needs after the repo is gone.

    The setup tells the human they may delete the cloned repo afterwards,
    and they should — but the deep interview is meant to happen weeks
    later, and the capture hooks are offered as something to come back
    for. Both used to live only in the repo, so both pointed at a folder
    that no longer existed by the time anyone wanted them.

    `.tools/` is kit infrastructure: excluded from search and from the
    placeholder check. The hooks land there inactive; nothing runs until
    a human puts an entry in their own settings.json.
    """
    kept = []
    src = os.path.join(here, "INTERVIEW.md")
    dst = os.path.join(vault, ".tools", "INTERVIEW.md")
    if os.path.isfile(src) and not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        kept.append(".tools/INTERVIEW.md")

    hooks = os.path.join(here, "hooks")
    if os.path.isdir(hooks):
        target = os.path.join(vault, ".tools", "hooks")
        os.makedirs(target, exist_ok=True)
        for name in sorted(os.listdir(hooks)):
            s = os.path.join(hooks, name)
            d = os.path.join(target, name)
            if os.path.isfile(s) and not name.endswith((".pyc", ".pyo")) \
                    and not os.path.exists(d):
                shutil.copy2(s, d)
                kept.append(f".tools/hooks/{name}")
    return kept


def drop(vault, rel):
    path = os.path.join(vault, *rel.split("/"))
    if os.path.isdir(path):
        shutil.rmtree(path)
        return True
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("vault", help="where the vault goes")
    ap.add_argument("mode", choices=MODES)
    ap.add_argument("--from", dest="template", default=None,
                    help="template directory (default: vault-template/ next to this script)")
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    template = a.template or os.path.join(here, "vault-template")
    vault = os.path.expanduser(a.vault)

    if not os.path.isdir(template):
        print(f"No template at {template}"); return 1

    existing = os.path.isdir(vault) and any(
        n for n in os.listdir(vault) if not n.startswith("."))
    if existing:
        print(f"{vault} already has content.")
        print("Nothing will be overwritten — existing files are kept and listed.")
        print("If you meant to start fresh, pick an empty folder instead.\n")

    skipped = []
    copy_tree(template, vault, skipped)

    if a.mode in ("professional", "company"):
        copy_tree(os.path.join(template, "modules", "processes"), vault, skipped,
                  overwrite=not existing)
    if a.mode == "company":
        # The company overlay REPLACES core files that describe folders this
        # mode does not have — a signpost pointing at a missing folder makes
        # the whole navigation lie. On an adopted vault we do not overwrite;
        # the runbook walks that case by hand.
        copy_tree(os.path.join(template, "modules", "company"), vault, skipped,
                  overwrite=not existing)
        removed = [r for r in COMPANY_DROPS if drop(vault, r)]
        if removed:
            print(f"removed (not part of a shared vault): {len(removed)} items")

    kept = keep_kit_extras(here, vault)

    folders = sum(1 for n in os.listdir(vault)
                  if os.path.isdir(os.path.join(vault, n)) and not n.startswith("."))
    print(f"\n{a.mode} vault assembled at {vault}")
    print(f"  {folders} folders · template: {os.path.relpath(template, here)}")
    if kept:
        print(f"  kept for later (survives deleting this repo): {', '.join(kept)}")
    if skipped:
        print(f"\n  {len(skipped)} existing files left untouched:")
        for s in skipped[:10]:
            print(f"    {s}")
        if len(skipped) > 10:
            print(f"    … and {len(skipped) - 10} more")
    print("\nNext: the setup runbook fills it in (questions, first notes,")
    print("language, the global rules block). This script only moved files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
