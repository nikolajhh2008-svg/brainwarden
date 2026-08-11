#!/usr/bin/env python3
"""Brainwarden — session queue (Claude Code "SessionEnd" hook, opt-in).

The gap this closes: the capture check only fires when nothing has reached
the brain for hours, and the weekly review's sweep looks at changed files
and git logs. Someone who works in Odoo, on the phone and in a warehouse
leaves no such traces. Their week is invisible to both.

This hook leaves a trace. When a session ends it appends ONE line to a
queue file — when, in which project, which session, why it ended. That is
all. The weekly review reads the queue, and for sessions it has not seen it
asks the one question the machine cannot answer: "what came out of this?"

What it deliberately does NOT do:

  - It does not read the transcript, and since v1.4 it does not even write
    down where the transcript IS. The path was in the file for a while and
    nothing ever read it — a pointer to everything that was said, kept for
    no purpose, is exactly the thing this hook promises not to keep. The
    session id is enough to find a session again.
  - It does not call a model. `SessionEnd` hooks share a 1.5-second budget
    (documented); anything that thinks does not fit and would make the hook
    a liability rather than a net.
  - It does not write into the vault. The queue lives next to the config,
    and only the review turns any of it into a note — with a human present.
  - It records no content. When, where, which session, why it ended.
    Nothing said.

That last point is not squeamishness. A system that quietly writes down
what people said stops being used — the reliable way to kill a personal
knowledge system is to make it feel like surveillance.

It appends rather than rewrites, and trims with a temp file plus
`os.replace`. Rewriting the whole file on every session end meant that a
hook killed at the 1.5-second mark left an empty queue behind: the file is
truncated the moment it is opened for writing, so the crash window covered
the entire history rather than the last line.

Install (opt-in):

  1. copy to  <config>/hooks/session_queue.py
  2. add to the "SessionEnd" hooks in <config>/settings.json:

     {"hooks": {"SessionEnd": [{"hooks": [
        {"type": "command", "command": "python3 ~/.claude/hooks/session_queue.py"}
     ]}]}}

Uninstall: delete the file, remove the entry, delete the queue.
Read it any time:  python3 <vault>/.tools/harvest.py --queue
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

MAX_LINES = 500          # a rolling window; older lines fall off the top
TRIM_BYTES = 200_000     # only then is it worth rewriting the file at all


def config_dir():
    return os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"))


def queue_path():
    return os.path.join(config_dir(), "state", "brainwarden-session-queue.tsv")


def clean(value):
    """One field, one line, no tabs — the file has to stay `cut`-able."""
    return re.sub(r"\s+", " ", str(value)).strip() or "?"


def trim(path):
    """Keep the last MAX_LINES. Written beside the file and moved into
    place, so an interrupted trim leaves the old queue intact."""
    tmp = path + ".tmp"
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            lines = fh.read().splitlines()
        if len(lines) <= MAX_LINES:
            return
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines[-MAX_LINES:]) + "\n")
        os.replace(tmp, path)
    except OSError:
        try:
            os.remove(tmp)
        except OSError:
            pass


def main():
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}
    if not isinstance(payload, dict):      # valid JSON, unexpected shape
        payload = {}

    # A session that is being picked up again has not ended. Claude Code
    # sends `clear`, `logout`, `prompt_input_exit` or `other` here today;
    # this guard costs nothing and holds if another value ever arrives.
    reason = payload.get("reason") or "other"
    if clean(reason) == "resume":
        return 0

    session = payload.get("session_id") or "?"
    cwd = payload.get("cwd") or os.getcwd()
    project = os.path.basename(str(cwd).rstrip(os.sep)) or "?"
    when = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

    # Tabs, not JSON: a human can read this file, and so can `cut`.
    line = "\t".join(clean(x) for x in (when, project, session, reason))

    path = queue_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        if os.path.getsize(path) > TRIM_BYTES:
            trim(path)
    except OSError:
        pass          # a queue that cannot be written must never break a session

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:                      # a hook must never break a session
        sys.exit(0)
