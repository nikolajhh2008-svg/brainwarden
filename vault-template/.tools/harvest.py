#!/usr/bin/env python3
"""Cold start: what your past Claude Code sessions could give the vault.

    python3 .tools/harvest.py                 # inventory only — reads nothing
    python3 .tools/harvest.py --candidates    # deterministic pre-filter
    python3 .tools/harvest.py --candidates --since 2026-07-01 --max 20
    python3 .tools/harvest.py --root ~/.claude-work/projects   # a second brain

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
import argparse, collections, json, os, re, sys, unicodedata
from datetime import datetime, timezone

# Follow CLAUDE_CONFIG_DIR: a second brain runs under its own config
# directory, and its transcripts live there too. Reading ~/.claude from a
# work vault would harvest the PRIVATE sessions into it — the exact
# crossover the two-brain setup exists to prevent.
SESSIONS = os.path.join(
    os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")), "projects")

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
]
# A line has to carry one of these to be a candidate at all: it must be a
# statement about the human's world, not about the machine's state.
SIGNAL = re.compile(
    r"\b(decid|decision|entschied|entscheidung|beschlossen|"          # decisions
    r"deadline|frist|termin|due|am \d{1,2}\.|until|bis zum|"          # dates
    r"launched|live gegangen|released|geliefert|fertig geworden|"     # milestones
    r"lesson|gelernt|lektion|never again|nie wieder|merke|"           # lessons
    r"we agreed|wir haben.{0,20}(entschieden|vereinbart)|"
    r"from now on|ab jetzt|ab sofort|künftig|"
    r"turns out|stellt sich heraus|zeigt sich)\b", re.I)

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

def human_lines(path, cap_bytes=4_000_000):
    """Only what the HUMAN typed. Everything the assistant said is a
    reformulation of it at best, and its own state at worst."""
    try:
        size = os.path.getsize(path)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            if size > cap_bytes:      # a few sessions are enormous; sample the head
                fh = iter(list(fh)[:8000])
            for raw in fh:
                try:
                    ev = json.loads(raw)
                except (ValueError, TypeError):
                    continue
                if ev.get("type") != "user":
                    continue
                msg = ev.get("message") or {}
                content = msg.get("content")
                if isinstance(content, list):
                    content = " ".join(c.get("text", "") for c in content
                                       if isinstance(c, dict) and c.get("type") == "text")
                if not isinstance(content, str) or not content.strip():
                    continue
                yield content.strip()
    except OSError:
        return

def classify(text):
    for pattern, label in NOISE:
        if pattern.search(text):
            return label
    if len(text) < 25:
        return "too short"
    return None

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
    kept, dropped, seen = [], collections.Counter(), set()
    for path in iter_sessions(root):
        day = session_day(path)
        if since and day and day < since:
            continue
        for text in human_lines(path):
            reason = classify(text)
            if reason:
                dropped[reason] += 1
                continue
            if not SIGNAL.search(text):
                dropped["no signal word"] += 1
                continue
            key = fold(re.sub(r"\s+", " ", text))[:180]
            if key in seen:
                dropped["duplicate"] += 1
                continue
            seen.add(key)
            kept.append((day, os.path.basename(path)[:8], text))
    total = len(kept) + sum(dropped.values())
    print(f"human turns looked at: {total}")
    print(f"dropped without a model: {sum(dropped.values())} "
          f"({100 * sum(dropped.values()) // max(total, 1)}%)")
    for reason, n in dropped.most_common():
        print(f"  {n:6}  {reason}")
    print(f"\ncandidates left: {len(kept)}")
    print("These are NOT findings — they are the only lines worth a model's time.")
    print("Judge a sample first, then decide whether the rest is worth it.\n")
    for day, sid, text in kept[:cap]:
        flat = re.sub(r"\s+", " ", text)
        print(f"[{day} {sid}] {flat[:200]}{'…' if len(flat) > 200 else ''}")
    if len(kept) > cap:
        print(f"\n… and {len(kept) - cap} more (raise with --max)")
    return 0

def show_queue(root_cfg):
    """The session queue, if the SessionEnd hook is installed.

    One line per finished session: when, project, id, why it ended. No
    content — the queue records THAT something happened, never what. The
    weekly review walks it and asks about the sessions it has not seen."""
    path = os.path.join(root_cfg, "state", "brainwarden-session-queue.tsv")
    if not os.path.exists(path):
        print("No session queue at " + path)
        print("The SessionEnd hook is not installed — see hooks/README.md.")
        print("Without it the weekly sweep only sees changed files and git logs,")
        print("which is nothing at all for work that happens on the phone.")
        return 0
    rows = [l.split("\t") for l in
            open(path, encoding="utf-8", errors="ignore").read().splitlines() if l.strip()]
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
        return show_queue(os.path.expanduser(
            os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")))
    root = os.path.expanduser(a.root)
    return candidates(root, since, a.max) if a.candidates else inventory(root)

if __name__ == "__main__":
    sys.exit(main())
