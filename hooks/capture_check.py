#!/usr/bin/env python3
"""Brainwarden — capture check (Claude Code "Stop" hook, opt-in).

The problem it solves: capture is a habit, and habits lapse. You work two
days straight, decisions get made, dates get mentioned — and none of it
reaches the brain, because nobody said "capture:". This is the net under
that.

How it works: at the end of a turn it checks ONE thing — has anything been
written to the vault's inbox or decisions folder recently? If yes, it stays
silent. If no, it makes Claude check the five capture triggers once, and
capture what is worth keeping.

Why it is built this way, and not smarter:

  - The pre-filter is a file-timestamp check. No model call, no cost, no
    latency. It costs nothing until it actually fires, which matters if you
    use Claude Code all day.
  - It never writes anything by itself. Systems that silently hoard
    everything drown in their own junk — an audit of 10,134 auto-captured
    memories in another system found 97.8% worthless. This one prompts a
    decision; it does not make one.
  - It cannot nag: at most one reminder per window, never twice in a row.
    A reminder you learn to ignore is worse than none.

Python, not bash, so it behaves the same on macOS, Linux and Windows and
needs no `jq`. Python is already required by the vault's own tools.

Install (opt-in — the setup does not do this for you):

  1. copy this file to  <config>/hooks/capture_check.py
     (<config> is ~/.claude, or whatever CLAUDE_CONFIG_DIR points at)
  2. add it to the "Stop" hooks in <config>/settings.json:

     {"hooks": {"Stop": [{"hooks": [
        {"type": "command", "command": "python3 ~/.claude/hooks/capture_check.py"}
     ]}]}}

     On Windows use the python command that works there, e.g. `py -3`.
  3. that's it — no other dependency

Uninstall: delete the file, remove the entry. Nothing else changes.

Tuning: BRAINWARDEN_CAPTURE_WINDOW (minutes, default 240). Longer if it
feels frequent, shorter if too much slips through. Being annoyed by it
means the window is wrong, not that the net is wrong.
"""
import json
import os
import re
import sys
import time

WINDOW_MIN = int(os.environ.get("BRAINWARDEN_CAPTURE_WINDOW", "240"))


def config_dir():
    return os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"))


def vault_path():
    """Read the vault location from the `Brain vault:` line in the global
    rules — the same line every brain-* skill follows. Falls back to
    ~/Brain only when no line is set."""
    rules = os.path.join(config_dir(), "CLAUDE.md")
    try:
        with open(rules, encoding="utf-8-sig", errors="ignore") as fh:
            for line in fh:
                m = re.match(r"\s*[-*]?\s*Brain vault:\s*(.+)", line)
                if m:
                    path = m.group(1).strip()
                    path = re.split(r"\s+(?:<|←|#)", path)[0].strip().strip('"\'')
                    if path:
                        return os.path.expanduser(path)
    except OSError:
        pass
    return os.path.expanduser("~/Brain")


def wrote_recently(folder, cutoff):
    """Any .md file in there touched within the window? First hit wins —
    no need to walk the whole tree."""
    if not os.path.isdir(folder):
        return False
    for dirpath, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            if not name.endswith(".md"):
                continue
            try:
                if os.path.getmtime(os.path.join(dirpath, name)) >= cutoff:
                    return True
            except OSError:
                continue
    return False


def main():
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}

    # Loop guard: if this stop came from our own block, let go.
    if payload.get("stop_hook_active"):
        return 0

    vault = vault_path()
    inbox = os.path.join(vault, "00-inbox")
    decisions = os.path.join(vault, "40-decisions")

    # No vault on this machine (someone else's computer)? Stay silent.
    if not os.path.isdir(inbox):
        return 0

    cutoff = time.time() - WINDOW_MIN * 60
    marker = os.path.join(config_dir(), "state", "brainwarden-capture-check")

    # Already reminded within the window? At most one per window.
    try:
        if os.path.getmtime(marker) >= cutoff:
            return 0
    except OSError:
        pass

    # Something reached the brain within the window? All good.
    if wrote_recently(inbox, cutoff) or wrote_recently(decisions, cutoff):
        return 0

    os.makedirs(os.path.dirname(marker), exist_ok=True)
    with open(marker, "w", encoding="utf-8") as fh:
        fh.write(str(int(time.time())))

    reason = (
        f"Capture check (automatic hook, at most once every {WINDOW_MIN} minutes): "
        "nothing has reached the brain for a while. Check the capture triggers for "
        "THIS session once: (a) was a decision settled? (b) was a date or deadline "
        "named? (c) did something go live? (d) did a new person come up? (e) was a "
        "lesson learned the hard way? If YES: run brain-capture now "
        f"(inbox: {inbox}, decisions as a record in {decisions}), then end the turn "
        "normally. If NO: just end the turn — invent nothing. Say in one line what "
        "you captured, or that there was nothing worth keeping."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
