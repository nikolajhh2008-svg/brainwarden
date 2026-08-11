#!/usr/bin/env python3
"""Brainwarden — session queue (Claude Code "SessionEnd" hook, opt-in).

The gap this closes: the capture check only fires when nothing has reached
the brain for hours, and the weekly review's sweep looks at changed files
and git logs. Someone who works in Odoo, on the phone and in a warehouse
leaves no such traces. Their week is invisible to both.

This hook leaves a trace. When a session ends it appends ONE line to a
queue file — which session, when, in which project. That is all. The
weekly review reads the queue, and for sessions it has not seen it asks the
one question the machine cannot answer: "what came out of this?"

What it deliberately does NOT do:

  - It does not read the transcript. It writes down that one exists.
  - It does not call a model. `SessionEnd` hooks share a 1.5-second budget
    (documented); anything that thinks does not fit and would make the hook
    a liability rather than a net.
  - It does not write into the vault. The queue lives next to the config,
    and only the review turns any of it into a note — with a human present.
  - It records no content. Which session, when, where. Nothing said.

That last point is not squeamishness. A system that quietly writes down
what people said stops being used — the reliable way to kill a personal
knowledge system is to make it feel like surveillance.

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


def config_dir():
    return os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"))


def queue_path():
    return os.path.join(config_dir(), "state", "brainwarden-session-queue.tsv")


def main():
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}

    # `clear` and `logout` mean the person walked away from finished work.
    # `resume` means they are coming back to it — nothing ended, skip.
    if payload.get("reason") == "resume":
        return 0

    transcript = payload.get("transcript_path") or ""
    session = payload.get("session_id") or os.path.basename(transcript)[:8] or "?"
    project = os.path.basename(payload.get("cwd") or os.getcwd()) or "?"
    reason = payload.get("reason") or "other"
    when = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

    # Tabs, not JSON: a human can read this file, and so can `cut`.
    line = "\t".join(re.sub(r"\s+", " ", str(x)) for x in
                     (when, project, session, reason, transcript))

    path = queue_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        lines = []
        if os.path.exists(path):
            with open(path, encoding="utf-8", errors="ignore") as fh:
                lines = fh.read().splitlines()
        lines.append(line)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines[-MAX_LINES:]) + "\n")
    except OSError:
        pass          # a queue that cannot be written must never break a session

    return 0


if __name__ == "__main__":
    sys.exit(main())
