# Tutorial: from zero to a running brain (≈ 35 minutes)

For people who have **never used Obsidian or Claude Code**. Every stage
ends with a checkpoint ("how you know it worked").

---

## Stage 1 — Install the tools (10 min)

**Obsidian** (your window into the brain):
1. [obsidian.md](https://obsidian.md) → download → install → open.
2. Don't configure anything yet — just leave it open.

**Claude Code** (the engine):
1. You need a Claude subscription with Claude Code access → [claude.com](https://claude.com).
2. Open a terminal (Mac: `Cmd+Space` → "Terminal" · Windows: Start →
   "PowerShell", ideally with WSL · Linux: any shell) and install —
   current guide: [claude.com/claude-code](https://claude.com/claude-code).
   On Windows, keep vault and Claude on the same side (both in WSL, or
   both native) so paths match.
3. Type `claude`, sign in with your account.

✅ **Checkpoint:** Claude greets you with a prompt in the terminal.

---

## Stage 2 — Start the setup (5 min)

You don't need to download anything — **Claude does that too.** Open the
terminal, type `claude`, then say literally:

> Set up the second brain from this GitHub repo for me:
> https://github.com/nikolajhh2008-svg/brainwarden — clone it and
> follow SETUP-FOR-CLAUDE.md step by step.

Claude fetches the kit, checks your prerequisites, asks four short
questions (life situation, your areas, first goal, **your brain's
language** — German works fine) and **guides you through every step**.

*(Advanced alternative: clone the repo yourself, `cd` into it, start
`claude` and say: "Read SETUP-FOR-CLAUDE.md and set up my brain
accordingly.")*

✅ **Checkpoint:** Claude reports the setup as done and `ls ~/Brain` shows
at least the six core folders (`00-inbox` … `90-archive`) plus any
modules you picked. (If "capture:" isn't recognized right away, restart
Claude Code once — fresh skills load with a new session.)

---

## Stage 3 — Open the vault in Obsidian (2 min)

Obsidian → **"Open folder as vault"** → pick `~/Brain`.
Click around starting from **"Start here"**.

✅ **Checkpoint:** You see "Start here" and can click through to
[[Deadlines]].

---

## Stage 4 — The onboarding interview (10–15 min, the step that matters)

Claude runs it automatically at the end of the setup (questions:
INTERVIEW.md). Just talk — the more you share, the more useful the brain.
Anything that shouldn't go in: just say "private".

✅ **Checkpoint:** Obsidian now shows "About me", individual people notes
under `30-knowledge/people/` — and the graph view shows its first connections.

---

## Stage 5 — Practice the three habits (5 min)

**1. Capture** — in any Claude session:
> capture: idea for the next project — draft the outline by Friday

**2. Ingest** — drop a PDF (handout, paper, contract, manual) into
`~/Brain/00-inbox/raw/` and say:
> ingest

**3. Review** — weekly (or right now, to test it):
> brain review

✅ **Checkpoint:** After the review `00-inbox/` is empty and your thought
has become a linked note.

---

## Your first week

| Day | What to do |
|---|---|
| Day 1 | Setup + interview (this tutorial) |
| Day 2–4 | Only **capture** — every idea, date, person. No sorting! |
| Day 5 | First **"brain review"** — watch the inbox turn into notes |
| Day 6–7 | Pull the first **output**: "Build me a study sheet / project plan / draft for X from my notes" — and try the power move: **"research my brain"** (Claude fills your open questions with sourced facts) |

After that the system carries itself: capture on the side, ten minutes of
review per week. **The success metric is output** — if the brain hasn't
gifted you a text, plan or study sheet after two weeks, tell Claude
exactly that.

---

## If something breaks

→ [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — and when in doubt: **just ask
Claude** ("why isn't my inbox empty?").
