# Hooks — optional, opt-in

A brain only works if things actually land in it. The five skills cover the
moment you *decide* to capture something. These hooks cover the moment you
*forget* to.

Nothing here is installed by the setup. You add a hook yourself, or you ask
Claude to ("install the capture check from brainwarden's hooks folder").
Removing one is deleting a file and one entry in `settings.json`.

## `capture_check.py`

**What it is for.** Capture is a habit, and habits lapse. You work two days
straight, decisions get made, dates get mentioned — and none of it reaches
the brain, because nobody said "capture:". This hook is the net under that.

**How it works.** At the end of a turn it walks `00-inbox/` and
`40-decisions/` and compares modification times: has any `.md` file been
written there recently? If yes, it stays silent. If no, it makes Claude
check the five capture triggers once — a decision, a date, a milestone, a
new person, a lesson learned the hard way — and capture what is worth
keeping. It never writes into the vault itself.

**It gets quieter on its own.** A reminder on a fixed timer is a nagger, and
naggers get switched off — so this one keeps score, and the score sets the
interval:

| what happened after it asked | what it does next |
|---|---|
| something landed in the vault | asks twice as often (floor: base ÷ 4) |
| nothing landed | asks half as often (ceiling: base × 16) |
| nothing, five times running | goes to sleep — stops asking entirely |
| asleep, and the vault starts filling again | wakes up at the base interval |

With the default base of four hours that ladder runs from one hour to about
two and a half days, and five empty answers in a row end it. You never have
to switch it off; ignoring it *is* switching it off, and starting to capture
again is switching it back on.

**What it can honestly measure — and what it cannot.** It cannot tell
whether you answered, or what you said. All it compares is file timestamps:
did a `.md` file appear in `00-inbox/` or `40-decisions/` after it asked?
That proxy is wrong in two known directions, both of them the right kind of
wrong: a capture you write by hand counts for it even though it did not
cause it, and a turn you interrupt counts against it. The question it is
scoring is not "was I obeyed" but "is this still worth the interruption".

The score is three numbers — when it last spoke, when it last asked, and the
current level — in `<config>/state/brainwarden-capture-check`. No content,
ever. `python3 <vault>/.tools/harvest.py --queue` prints it in plain
language; deleting the file resets everything.

**Why it is built this way.** Four constraints shaped it:

1. **No model call in the pre-filter.** It is a directory walk over two
   folders comparing `mtime`, and it stops at the first recent file. No
   cost, no network, no latency until it actually fires — which matters if
   you use Claude Code all day.
2. **It never writes by itself.** Systems that silently hoard everything
   drown in their own junk — that is the documented failure mode of
   "extract everything" memory tools, and the reason this kit reports every
   filing instead of doing it quietly. The hook prompts a decision; it does
   not make one.
3. **It cannot nag.** One reminder per interval, never twice in a row, and
   the interval grows every time the reminder produces nothing.
4. **If it cannot remember, it says nothing.** When the state file cannot be
   written (read-only config, a directory in its place) the hook stays
   silent instead of asking. It used to abort with a traceback there — on
   *every* turn, since nothing was ever recorded. A reminder that cannot
   remember that it already spoke is not a net, it is a stutter.

**What it does not do:** it does not read your conversation, does not send
anything anywhere, and does not decide what is worth keeping. That judgement
stays with the model in front of you, which has the actual context.

**Install:** see the header of the script. Needs nothing but Python 3, which
the vault's own tools already require — so the script behaves identically on
macOS, Linux and Windows. The `~/.claude/...` in the install snippet is a
shell convention, not part of the path: where it is not expanded (Windows
shells generally do not), write the path out in full.

**Tuning:** `BRAINWARDEN_CAPTURE_WINDOW` (minutes, default 240) sets the
*base* interval that the ladder moves around. `BRAINWARDEN_CAPTURE_CHECK=off`
silences it without uninstalling. If it asks more often than you want, the
honest reading is that the base is too short for you — raise it, or simply
answer "nothing worth keeping" and let it back off by itself.

**Uninstall:** delete the file and the `settings.json` entry. One thing is
left behind: the state file named above — three numbers, harmless, and yours
to delete.

## `session_queue.py`

**What it is for.** The capture check fires when nothing has reached the
brain for hours. The weekly sweep looks at changed files and git logs.
Both are blind to the same person: someone who spends the week in an ERP,
on the phone and in a warehouse leaves no files and no commits. Their week
is invisible.

This hook leaves a trace. When a session ends it appends one line to a
queue file — when, which project, which session, why it ended. The weekly
review reads it and asks about the sessions it has not seen: *what came out
of this one?*

**What it records:** four tab-separated fields, and that is the whole line —
`2026-08-11 17:04` · `lager` · `a1b2c3d4` · `clear`. **What it does not
record:** anything that was said. It does not read the transcript, and it no
longer writes down where the transcript is either: that path sat in the file
for a while, nothing ever read it, and a pointer to everything that was said
is precisely what this hook promises not to keep. The session id is enough
to find a session again.

It also does not call a model — `SessionEnd` hooks share a 1.5-second budget
(raised to match a longer per-hook `timeout`, up to 60 seconds), and
anything that thinks does not fit. Measured on this queue: about 15 ms per
session end, including Python's own start-up. It writes nothing into the
vault; only the review turns a queue line into a note, with a human in the
room.

That restraint is the point. The reliable way to kill a personal knowledge
system is to make it feel like surveillance — and a work vault that seems
to report upwards gets bypassed, not filled.

**It appends, it does not rewrite.** The queue is a rolling window of the
last 500 lines, but trimming it means writing the whole file, and opening a
file for writing empties it *before* the first byte goes back in. A hook
killed in that window — at the 1.5-second mark, say — used to leave an empty
queue behind: the whole history, not the last line. Now the normal path is a
single append, and the rare trim is written beside the file and moved into
place with `os.replace`, which either happens completely or not at all.

**Read it any time:** `python3 <vault>/.tools/harvest.py --queue`
**Install:** see the header of the script. **Uninstall:** delete the file,
the settings entry and the queue.

## What neither hook can see

Both hooks live inside Claude Code. Claude in the browser, Claude Cowork and
a phone have no hook mechanism at all (see `COWORK.md`), and the person this
kit is hardest to fill for — the one whose week happens in an ERP window, a
warehouse and three phone calls — may never open a terminal.

There is no tool to build for them, and installing one anyway would be the
old mistake: a mechanism that measures the people it can reach and calls the
rest invisible. What works instead is the weekly review's last track, the
human — provided the question carries the cues. "What were the three most
important things this week?" is free recall over seven days, which is weak
and biased towards yesterday. These three are not:

- **day by day** — Monday through Sunday, one line each, instead of "the week"
- **by counterpart** — walk `30-knowledge/people/` (or `60-roles/`,
  `80-partners/`) by name: "anything with them this week?" Phone work leaves
  no files, but it leaves people.
- **by open loop** — every date in `Deadlines.md` and every open question on
  `Home.md`: "what happened with this one?"

All three are built from what the vault already knows, so they cost nothing
and work on a machine that has never seen a hook. `harvest.py --queue`
prints them when no queue exists, so the review reads the right instruction
in exactly the situation where the hook can never help.
