#!/usr/bin/env python3
"""Cold start: what your past Claude Code sessions could give the vault.

    python3 .tools/harvest.py                 # inventory only — reads nothing
    python3 .tools/harvest.py --candidates    # deterministic pre-filter
    python3 .tools/harvest.py --candidates --since 2026-07-01 --max 20
    python3 .tools/harvest.py --root ~/.claude-work/projects   # a second brain
    python3 .tools/harvest.py --queue         # what the hooks have recorded

A new vault is empty, and an empty vault is useless. But the machine has
been listening for months: Claude Code keeps session transcripts in
`~/.claude/projects/` as plaintext JSONL (30 days by default — see
`cleanupPeriodDays`). That is the richest material about how someone
actually works that exists on their disk.

The catch is well documented. An audit of 10,134 auto-captured memories in
another system found 97.8% of them worthless — system-prompt echoes, cron
noise, transient task state, duplicates, and hallucinated profiles of the
user (github.com/mem0ai/mem0/issues/4573). Over 70% of that junk is
recognisable WITHOUT a model, by shape alone. That is what this tool does:
it throws away the obvious garbage for free, so a model only ever looks at
what might be worth something.

WHAT THIS TOOL DOES NOT DO — on purpose:
  - it never writes into the vault
  - it never calls a model, and costs nothing
  - it never decides what is worth keeping; it decides what is obviously NOT

Everything it prints is a candidate for a human to look at. The judging
happens afterwards, on a small sample first, and only with consent.
"""
import argparse, collections, itertools, json, os, re, sys, unicodedata
from datetime import datetime, timezone

# Same reason as in search.py: on Windows the output stream falls back to the
# console codepage as soon as it is piped or redirected, and `--candidates`
# prints `→` on every line — so the one command that fills an empty vault
# died with a UnicodeEncodeError exactly when someone tried to save its
# output to a file.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        pass

# Follow CLAUDE_CONFIG_DIR: a second brain runs under its own config
# directory, and its transcripts live there too. Reading ~/.claude from a
# work vault would harvest the PRIVATE sessions into it — the exact
# crossover the two-brain setup exists to prevent.
CONFIG = os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"))
SESSIONS = os.path.join(CONFIG, "projects")

MAX_LINES = 20_000        # per session; a runaway transcript must not eat RAM
EXCERPT = 300             # characters shown around the phrase that matched

# --- what is obviously not worth keeping, recognisable by shape alone ---
NOISE = [
    (re.compile(r"^\s*<(system-reminder|command-name|local-command|task-notification)", re.I),
     "system plumbing"),
    (re.compile(r"^\s*(Caveat: The messages below were generated|"
                r"This session is being continued from|"
                r"Your task is to create a detailed summary)", re.I),
     "harness scaffolding"),
    (re.compile(r"^\s*(ok|okay|yes|no|ja|nein|passt|danke|thanks|weiter|"
                r"go|stop|warte|hm+|👍|✅)\s*[.!]?\s*$", re.I),
     "acknowledgement"),
    (re.compile(r"^\s*(continue|weiter machen|mach weiter|fortsetzen)\s*$", re.I),
     "continuation"),
    # Injected by the harness, not typed by the human — these arrive as
    # "user" events and are the single biggest source of false candidates.
    (re.compile(r"^\s*(Base directory for this skill|"
                r"Stop hook feedback:|"
                r"Review this change for security|"
                r"Please write a|"
                r"Analyze this codebase and|"
                r"\[Request interrupted)", re.I),
     "injected by the harness"),
    (re.compile(r"^\s*(Changed files|Unified diff|"
                r"The user sent a new message while you were working)", re.I),
     "injected by the harness"),
    # Pasted back INTO the chat: the assistant's own output, a terminal, a
    # build log. The premise of this tool is "only what the human typed";
    # a paste of the machine's words is the machine's words, however it got
    # there. Measured on 1,542 real turns: removes 7 candidates, all junk.
    (re.compile(r"⏺|\[\.{3}Truncated text #|Claude is temporarily overloaded|"
                r"\bSearched for \d+ pattern|\bRecalled \d+ memor|"
                r"^\s*▎|\w+@[\w-]+ ~ %|=> \[internal\] load|"
                r"^\s*\[Image: source: /", re.M),
     "pasted machine output"),
    # A pasted DOCUMENT (two or more Markdown headings): a skill body, a
    # spec, terms and conditions. Documents are `brain-ingest`'s job —
    # they go to 00-inbox/raw/, not into a capture. Removes 6, all junk.
    (re.compile(r"^\s{0,3}#{1,3} \S[\s\S]*?^\s{0,3}#{1,3} \S", re.M),
     "pasted document (→ brain-ingest)"),
]

# Attachments and paths are stripped BEFORE the signal test. A screenshot
# called "Bildschirmfoto 2026-08-06 um 06.42.56.png" is not an appointment,
# and it used to become one the moment dates were recognised at all.
ATTACHMENT = re.compile(
    r"\[Image #\d+\]|\[Image: source:[^\]]*\]|https?://\S+|"
    r"@?\"/[^\"\n]+\"|"                                   # "…/a file.png"
    r"/[\w.-]+(?:(?:/|\\ )[\w.-]+)*\.\w{2,4}")            # /a/path/file.png


# A line has to carry one of these to be a candidate at all: it must be a
# statement about the human's world, not about the machine's state.
SIGNAL = re.compile(
    r"\b(decid|decision|entschied|entscheidung|beschlossen|"          # decisions
    r"deadline|frist|termin|due|until|bis zum|"                       # dates
    r"launched|live gegangen|released|geliefert|fertig geworden|"     # milestones
    r"lesson|gelernt|lektion|never again|nie wieder|merke|"           # lessons
    r"we agreed|wir haben.{0,20}(entschieden|vereinbart)|"
    r"from now on|ab jetzt|ab sofort|künftig|"
    r"turns out|stellt sich heraus|zeigt sich)\b|"
    # Real dates, not the word "date". An appointment is the one capture
    # trigger that is almost never announced with a trigger WORD — "our
    # conversation on Tuesday, 18.08., at 15:00" carried none of the above
    # and was dropped. Clock times alone are deliberately NOT here: they
    # matched "it is 22:33 now" and nothing worth keeping.
    r"(?<![\d.,])(?:0?[1-9]|[12]\d|3[01])\.\s?(?:0?[1-9]|1[0-2])\.(?![\d.])|"
    r"(?<![\d.,])(?:0?[1-9]|[12]\d|3[01])\.\s?(?:Jan|Feb|Mär|Maer|Mar|Apr|Mai|"
    r"May|Jun|Jul|Aug|Sep|Okt|Oct|Nov|Dez|Dec)|"
    r"\b\d{4}-\d{2}-\d{2}\b|"
    # The mirror of the line above for English ("August 18" vs "18. August").
    # It adds nothing on the corpus this was measured against — that corpus
    # is German — and it costs nothing there either: zero new candidates.
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? "
    r"\d{1,2}(?:st|nd|rd|th)?\b|"
    r"\b(?:Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)

def fold(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))

def iter_sessions(root):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != "subagents"]   # sub-agent chatter
        for f in sorted(files):
            if f.endswith(".jsonl"):
                yield os.path.join(dirpath, f)

def session_day(path):
    try:
        return datetime.fromtimestamp(os.path.getmtime(path), timezone.utc).date()
    except OSError:
        return None

def human_lines(path, stats=None):
    """Only what the HUMAN typed. Everything the assistant said is a
    reformulation of it at best, and its own state at worst.

    Read line by line: a transcript can be tens of megabytes (mostly one
    enormous line per pasted image), and slurping it into a list to take
    the head costs the file's size in RAM for no gain."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            seen = 0
            for raw in itertools.islice(fh, MAX_LINES):
                seen += 1
                try:
                    ev = json.loads(raw)
                except (ValueError, TypeError):
                    continue
                if not isinstance(ev, dict) or ev.get("type") != "user":
                    continue
                msg = ev.get("message")
                if not isinstance(msg, dict):     # a format change must not crash us
                    continue
                content = msg.get("content")
                if isinstance(content, list):
                    content = " ".join(c.get("text", "") for c in content
                                       if isinstance(c, dict) and c.get("type") == "text")
                if not isinstance(content, str) or not content.strip():
                    continue
                yield content.strip()
            if stats is not None and seen == MAX_LINES:
                stats["truncated"] += 1       # named in the output, never silent
    except OSError:
        return

def classify(text):
    for pattern, label in NOISE:
        if pattern.search(text):
            return label
    if len(text) < 25:
        return "too short"
    return None

def excerpt(text, match):
    """Show the phrase that made this a candidate, not the first 200
    characters of the turn. In a 15,000-character turn those are almost
    never the same thing, and the head is what a reader used to get."""
    flat = re.sub(r"\s+", " ", text).strip()
    if len(flat) <= EXCERPT + 60:
        return flat
    hit = re.sub(r"\s+", " ", match).strip()
    at = flat.find(hit)
    if at < 0:
        at = 0
    start = max(0, at - EXCERPT // 4)
    end = min(len(flat), start + EXCERPT)
    if start:
        start = flat.find(" ", start) + 1 or start
    if end < len(flat):
        cut = flat.rfind(" ", start, end)
        end = cut if cut > start else end
    return ("…" if start else "") + flat[start:end] + ("…" if end < len(flat) else "")

def inventory(root):
    if not os.path.isdir(root):
        print(f"No session directory at {root} — nothing to harvest.")
        return 1
    by_month, by_project, total, bytes_ = collections.Counter(), collections.Counter(), 0, 0
    oldest = newest = None
    for path in iter_sessions(root):
        total += 1
        try:
            bytes_ += os.path.getsize(path)
        except OSError:
            pass
        day = session_day(path)
        if day:
            by_month[day.strftime("%Y-%m")] += 1
            oldest = day if oldest is None or day < oldest else oldest
            newest = day if newest is None or day > newest else newest
        rel = os.path.relpath(path, root).split(os.sep)[0]
        by_project[rel] += 1
    print(f"sessions: {total} · {bytes_ / 1e9:.1f} GB · {len(by_project)} projects")
    if oldest:
        print(f"range: {oldest} … {newest}")
    print("\nby month:")
    for m, n in sorted(by_month.items()):
        print(f"  {m}: {n}")
    print("\nlargest projects:")
    for p, n in by_project.most_common(8):
        print(f"  {n:5}  {p}")
    print("\nNothing was read. Run with --candidates to pre-filter, or see the")
    print("cold-start section of SETUP-FOR-CLAUDE.md for the full procedure.")
    print("Transcripts older than `cleanupPeriodDays` (default 30) are already gone.")
    return 0

def candidates(root, since, cap):
    if not os.path.isdir(root):
        # Without this, a typo in --root printed "0 turns looked at", which
        # reads as "your sessions hold nothing" rather than "wrong path".
        print(f"No session directory at {root} — nothing to harvest.")
        return 1
    kept, dropped, seen = [], collections.Counter(), set()
    stats = collections.Counter()
    for path in iter_sessions(root):
        day = session_day(path)
        if since and day and day < since:
            continue
        for text in human_lines(path, stats):
            reason = classify(text)
            if reason:
                dropped[reason] += 1
                continue
            probe = ATTACHMENT.sub(" ", text)
            m = SIGNAL.search(probe)
            if not m:
                dropped["no signal word"] += 1
                continue
            shown = excerpt(probe, m.group(0))
            key = fold(shown)[:180]
            if key in seen:
                dropped["duplicate"] += 1
                continue
            seen.add(key)
            kept.append((day, os.path.basename(path)[:8], shown))
    total = len(kept) + sum(dropped.values())
    print(f"human turns looked at: {total}")
    print(f"dropped without a model: {sum(dropped.values())} "
          f"({100 * sum(dropped.values()) // max(total, 1)}%)")
    for reason, n in dropped.most_common():
        print(f"  {n:6}  {reason}")
    if stats["truncated"]:
        print(f"\nNOTE: {stats['truncated']} session(s) were read only to their "
              f"first {MAX_LINES:,} lines — the rest was NOT looked at.")
    print(f"\ncandidates left: {len(kept)}")
    print("These are NOT findings — they are the only lines worth a model's time.")
    print("Each one is shown around the phrase that matched, not from the start.")
    print("Judge a sample first, then decide whether the rest is worth it.\n")
    for day, sid, text in kept[:cap]:
        print(f"[{day} {sid}] {text}")
    if len(kept) > cap:
        print(f"\n… and {len(kept) - cap} more (raise with --max)")
    return 0

def capture_check_state():
    """What the Stop hook has learnt, in plain language. It stores three
    numbers and no content; this is the only place they are readable."""
    path = os.path.join(CONFIG, "state", "brainwarden-capture-check")
    st = {}
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                key, sep, value = line.partition("=")
                if sep and not key.strip().startswith("#"):
                    try:
                        st[key.strip()] = float(value)
                    except ValueError:
                        pass
    except OSError:
        return
    level = int(st.get("level", 0))
    base = 240
    try:
        base = int(os.environ.get("BRAINWARDEN_CAPTURE_WINDOW", "") or 240)
    except ValueError:
        pass
    hours = base * (2 ** min(max(level, -2), 4)) / 60.0
    print("\ncapture check:")
    if level >= 5:
        print("  asleep — five asks in a row produced nothing. It wakes up by")
        print("  itself as soon as something lands in the inbox or decisions.")
    else:
        print(f"  level {level:+d} → asks at most every {hours:.0f}h "
              f"(base {base / 60:.0f}h)")
        print("  every empty answer halves that rate, every capture doubles it.")
    if st.get("last"):
        when = datetime.fromtimestamp(st["last"]).strftime("%Y-%m-%d %H:%M")
        print(f"  last spoke: {when}")

def show_queue(root_cfg):
    """The session queue, if the SessionEnd hook is installed.

    One line per finished session: when, project, id, why it ended. No
    content — the queue records THAT something happened, never what. The
    weekly review walks it and asks about the sessions it has not seen."""
    path = os.path.join(root_cfg, "state", "brainwarden-session-queue.tsv")
    if not os.path.exists(path):
        print("No session queue at " + path)
        print("Either the SessionEnd hook is not installed (see hooks/README.md),")
        print("or this is a place where hooks do not exist at all — Claude in the")
        print("browser, Cowork, a phone. In that case do NOT wait for a tool:")
        print("the week gets reconstructed by ASKING, and the question has to")
        print("carry the cues, because free recall over seven days is poor:")
        print("  · day by day, Monday through Sunday — not 'this week'")
        print("  · by counterpart: go through 30-knowledge/people/ (or 60-roles/,")
        print("    80-partners/) by name — 'anything with them this week?'")
        print("  · by open loop: every date in Deadlines.md and every open")
        print("    question on Home — 'what happened with this one?'")
        print("Phone work leaves no files and no commits, but it leaves people")
        print("and dates, and those the vault already knows.")
        capture_check_state()
        return 0
    rows = [l.split("\t") for l in
            open(path, encoding="utf-8", errors="ignore").read().splitlines() if l.strip()]
    # An EMPTY queue file is not the same story as a queue with nothing new in
    # it, and printing "sessions in queue: 0" told both stories in the same
    # calm voice. Measured on a live machine: the file existed, the hook was
    # installed and registered, sessions had been ending all day, and the
    # queue was zero bytes — the review would have read that as a quiet week.
    # A track that has died has to say so, or it is worse than no track.
    if not rows:
        print(f"sessions in queue: 0 — but the queue file EXISTS ({path})")
        try:
            age = (datetime.now() - datetime.fromtimestamp(
                os.path.getmtime(path))).days
            print(f"  last written {age} day(s) ago, and it is empty.")
        except OSError:
            pass
        stray = path + ".tmp"
        if os.path.exists(stray):
            print(f"  a half-finished trim is still lying next to it: {stray}")
        print("  So either no session has ended since it was emptied, or this")
        print("  track is broken. Check it before believing the zero:")
        print("    · is the SessionEnd hook still in settings.json?")
        print("      (hooks/README.md has the entry)")
        print("    · does it run? end a session and look at the file again")
        print("    · is CLAUDE_CONFIG_DIR the same for the hook and for this")
        print("      tool? A second brain writes its queue somewhere else.")
        print("  Until that is answered, treat the session track as MISSING and")
        print("  ask the cued questions instead (day by day · by counterpart ·")
        print("  by open deadline).")
        capture_check_state()
        return 0
    print(f"sessions in queue: {len(rows)}")
    by_project = collections.Counter(r[1] for r in rows if len(r) > 1)
    print("\nby project:")
    for name, n in by_project.most_common(10):
        print(f"  {n:4}  {name}")
    print("\nmost recent:")
    for r in rows[-15:]:
        when, project, sid = (r + ["", "", ""])[:3]
        print(f"  {when}  {project}  {sid[:8]}")
    print("\nThese are sessions, not findings. The weekly review asks what came")
    print("out of the ones it has not seen yet — that question is the point.")
    print("It is also only ONE track: whoever works in Cowork, in a browser or")
    print("on a phone never appears here, and gets asked the cued questions")
    print("instead (day by day · by counterpart · by open deadline).")
    capture_check_state()
    return 0

def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--queue", action="store_true",
                    help="show the session queue (needs the SessionEnd hook)")
    ap.add_argument("--candidates", action="store_true",
                    help="pre-filter the transcripts (still writes nothing)")
    ap.add_argument("--since", help="only sessions from this date on (YYYY-MM-DD)")
    ap.add_argument("--max", type=int, default=40, help="how many candidates to print")
    ap.add_argument("--root", default=SESSIONS, help="session directory")
    a = ap.parse_args()
    since = None
    if a.since:
        try:
            since = datetime.strptime(a.since, "%Y-%m-%d").date()
        except ValueError:
            print("--since needs YYYY-MM-DD"); return 1
    if a.queue:
        return show_queue(CONFIG)
    root = os.path.expanduser(a.root)
    return candidates(root, since, a.max) if a.candidates else inventory(root)

if __name__ == "__main__":
    sys.exit(main())
