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

WHY IT BACKS OFF BY ITSELF
--------------------------
A reminder on a fixed timer is a nagger, and naggers get switched off. So
this one keeps score, and the score decides how often it may speak:

    it asks  →  did anything land in the vault afterwards?
       yes   →  it may ask twice as often   (down to 1× BASE/4)
       no    →  it asks half as often       (up to 16× BASE)
                after five empty answers in a row it goes to sleep
                entirely, and wakes up only when the vault starts
                filling again.

What it can honestly measure, and what it cannot: it CANNOT tell whether
you answered, or what you said. It only compares file timestamps — did a
`.md` file appear in `00-inbox/` or `40-decisions/` after it asked? That
proxy is imperfect in a known direction: a capture you write by hand counts
as a hit, and a turn you interrupt counts as a miss. Both are the right
answer for the purpose — the question is not "was I obeyed" but "is this
check still earning the interruption".

The whole score is three numbers in a text file next to the config
(`state/brainwarden-capture-check`): when it last spoke, when it last
asked, and the current level. Delete the file and everything is back to
factory settings. `python3 <vault>/.tools/harvest.py --queue` prints it in
plain language.

Why it is built this way, and not smarter:

  - The pre-filter is a walk over the inbox and decisions folders comparing
    modification times. No model call, no cost, no network. It costs
    nothing until it actually fires, which matters if you use Claude Code
    all day.
  - It never writes anything into the vault by itself. Systems that
    silently hoard everything drown in their own junk — an audit of 10,134
    auto-captured memories in another system found 97.8% worthless. This
    one prompts a decision; it does not make one.
  - It records no content anywhere. Three integers, and nothing else.
  - If it cannot write its own state file it stays SILENT instead of
    speaking, because a reminder that cannot remember it already spoke
    would repeat on every single turn.

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
Silence it without uninstalling: `BRAINWARDEN_CAPTURE_CHECK=off`.

Tuning: BRAINWARDEN_CAPTURE_WINDOW (minutes, default 240) sets the BASE
interval — the level ladder above moves around it. If it still asks more
often than you want, raise the base; the ladder will do the rest by itself.
"""
import json
import os
import re
import sys
import time

DEFAULT_WINDOW = 240             # minutes — the base the ladder moves around
MIN_LEVEL, MAX_LEVEL = -2, 4     # BASE/4  …  BASE*16
DORMANT = MAX_LEVEL + 1          # asleep: only ever checks for a reason to wake
RESOLVE_AFTER = 30 * 60          # seconds before an unanswered ask counts as empty


def base_window():
    """Minutes. A junk value in the environment must not kill the turn."""
    try:
        n = int(os.environ.get("BRAINWARDEN_CAPTURE_WINDOW", "") or DEFAULT_WINDOW)
    except ValueError:
        return DEFAULT_WINDOW
    return n if n > 0 else DEFAULT_WINDOW


def window_seconds(level):
    """The interval for a level. Dormant checks at the slowest cadence."""
    level = min(max(level, MIN_LEVEL), DORMANT)
    return base_window() * 60 * (2 ** min(level, MAX_LEVEL))


def config_dir():
    return os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"))


def state_path():
    return os.path.join(config_dir(), "state", "brainwarden-capture-check")


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


def landed_since(folders, cutoff):
    """Any .md file in there touched at or after `cutoff`? First hit wins —
    no need to walk the whole tree."""
    for folder in folders:
        if not os.path.isdir(folder):
            continue
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


def read_state():
    """`key=value` lines, so a human can read and edit it. An older install
    left a bare timestamp here — that still parses as "last spoke then"."""
    st = {"last": 0.0, "asked": 0.0, "level": 0}
    path = state_path()
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            raw = fh.read()
    except OSError:
        return st
    parsed = False
    for line in raw.splitlines():
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or key not in st:
            continue
        try:
            st[key] = int(float(value)) if key == "level" else float(value)
            parsed = True
        except ValueError:
            continue
    if not parsed:                      # pre-1.4 marker file: one bare epoch
        try:
            st["last"] = float(raw.strip())
        except ValueError:
            try:
                st["last"] = os.path.getmtime(path)
            except OSError:
                pass
    st["level"] = min(max(st["level"], MIN_LEVEL), DORMANT)
    return st


def write_state(st):
    """True only if the state really reached the disk. A hook that cannot
    remember that it spoke must not speak — otherwise it repeats forever,
    which is what a read-only or occupied state path used to cause."""
    path = state_path()
    body = (
        "# brainwarden capture check — delete this file to reset\n"
        "# level: -2 = asks 4x as often, 0 = base, 4 = 16x rarer, 5 = asleep\n"
        f"last={int(st['last'])}\n"
        f"asked={int(st['asked'])}\n"
        f"level={int(st['level'])}\n"
    )
    tmp = path + ".tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(body)
        os.replace(tmp, path)
        return True
    except OSError:
        try:
            os.remove(tmp)
        except OSError:
            pass
        return False


def main():
    if os.environ.get("BRAINWARDEN_CAPTURE_CHECK", "").strip().lower() in (
            "off", "0", "false", "no"):
        return 0

    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}
    if not isinstance(payload, dict):     # valid JSON, unexpected shape
        payload = {}

    vault = vault_path()
    inbox = os.path.join(vault, "00-inbox")
    folders = [inbox, os.path.join(vault, "40-decisions")]

    # No vault on this machine (someone else's computer)? Stay silent.
    if not os.path.isdir(inbox):
        return 0

    now = time.time()
    st = read_state()
    from_our_block = bool(payload.get("stop_hook_active"))

    # 1. Score the last ask, if one is still open. This is the whole
    #    learning mechanism: did anything land after we asked?
    if st["asked"]:
        if from_our_block or now - st["asked"] >= RESOLVE_AFTER:
            hit = landed_since(folders, st["asked"])
            st["level"] = min(max(st["level"] + (-1 if hit else 1),
                                  MIN_LEVEL), DORMANT)
            st["asked"] = 0.0
            write_state(st)

    # Never block twice in a row — the turn we just caused must end.
    if from_our_block:
        return 0

    # 2. One action per interval, at most. The interval is the level's.
    if now - st["last"] < window_seconds(st["level"]):
        return 0
    st["last"] = now

    # 3. Something reached the brain within the interval? Then all is well —
    #    and if we were asleep, that is the signal to wake up.
    if landed_since(folders, now - window_seconds(st["level"])):
        if st["level"] == DORMANT:
            st["level"] = 0
        write_state(st)
        return 0

    if st["level"] == DORMANT:            # asleep, nothing to wake up for
        write_state(st)
        return 0

    # 4. Ask — but only if we can record that we asked.
    st["asked"] = now
    if not write_state(st):
        return 0

    hours = window_seconds(st["level"]) / 3600.0
    left = DORMANT - st["level"]
    backoff = (f"If there is nothing, this check asks half as often next time "
               f"({left} more empty answer{'s' if left != 1 else ''} and it "
               f"sleeps until the vault fills again) — so an honest 'nothing' "
               f"is a useful answer, not a failure.")
    reason = (
        f"Capture check (automatic hook, currently at most once every "
        f"{hours:.0f}h): nothing has reached the brain for a while. Check the "
        "capture triggers for THIS session once: (a) was a decision settled? "
        "(b) was a date or deadline named? (c) did something go live? (d) did "
        "a new person come up? (e) was a lesson learned the hard way? If YES: "
        f"run brain-capture now (inbox: {inbox}, decisions as a record in "
        f"{folders[1]}), then end the turn normally. If NO: just end the turn "
        "— invent nothing. Say in one line what you captured, or that there "
        f"was nothing worth keeping. {backoff} If the human asks to stop being "
        f"asked at all, set level=5 in {state_path()} and tell them deleting "
        "that file undoes it."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:                     # a hook must never break a session
        sys.exit(0)
