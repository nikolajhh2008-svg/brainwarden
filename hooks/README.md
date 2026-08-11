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

**How it works.** At the end of a turn, it checks one thing: has anything
been written to the vault's inbox or decisions folder in the last four
hours? If yes, it stays silent. If no, it makes Claude check the five
capture triggers once — a decision, a date, a milestone, a new person, a
lesson learned the hard way — and capture what is worth keeping.

**Why it is built this way.** Three constraints shaped it:

1. **No model call in the pre-filter.** The check is a single `find`. It
   costs nothing until it actually fires, which matters if you use Claude
   Code all day.
2. **It never writes by itself.** Systems that silently hoard everything
   drown in their own junk — that is the documented failure mode of
   "extract everything" memory tools, and the reason this kit reports every
   filing instead of doing it quietly. The hook prompts a decision; it does
   not make one.
3. **It cannot nag.** At most one reminder per window, and never twice in a
   row. A reminder you learn to ignore is worse than none.

**What it does not do:** it does not read your conversation, does not send
anything anywhere, and does not decide what is worth keeping. That judgement
stays with the model in front of you, which has the actual context.

**Install:** see the header of the script. Needs nothing but Python 3,
which the vault's own tools already require — so it behaves identically on
macOS, Linux and Windows.

**Tuning:** `BRAINWARDEN_CAPTURE_WINDOW` (minutes, default 240). Longer if
the reminder feels frequent; shorter if too much slips through. If you find
yourself annoyed by it, that is a signal the window is wrong — not that the
net is wrong.
