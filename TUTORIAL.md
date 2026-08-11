# Tutorial: from zero to a running brain (≈ 20 minutes + optional interview)

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
   "PowerShell" · Linux: any shell) and install — current guide:
   [claude.com/claude-code](https://claude.com/claude-code).

   **On Windows:** one extra install first —
   [Git for Windows](https://git-scm.com/downloads/win), default
   settings, just click through. You don't need to know what it is;
   it's the piece that lets Claude run the setup for you. If anything
   acts up later, the Windows section in
   [TROUBLESHOOTING.md](TROUBLESHOOTING.md) has the fixes.
3. Type `claude`, sign in with your account.

*(Would rather never touch a terminal? **Claude Code also ships as a normal
desktop app for Mac and Windows** — install it like any other program, open
it, type into it. No black screen anywhere, and every later step works the
same. That is the simplest route and the one to take if the terminal is not
your world. Developers who live in an editor can instead use the
[Claude Code extension for VS Code](https://code.claude.com/docs/en/vs-code).)*

✅ **Checkpoint:** Claude greets you with a prompt — in the terminal, in the
desktop app, or in the editor panel, whichever you chose.

---

## Stage 2 — Start the setup (5–10 min, ends with your first win)

You don't need to download anything — **Claude does that too.** Open the
terminal, type `claude`, then say literally:

> Set up the second brain from this GitHub repo for me:
> https://github.com/nikolajhh2008-svg/brainwarden — clone it and
> follow SETUP-FOR-CLAUDE.md step by step.

Claude fetches the kit and checks your prerequisites. Then comes the one
question that shapes everything: **is this brain for you, for your work,
for both kept apart, or for a company?** Unsure? Say "for me". A work
brain can be added later, and nothing you build now is wasted.

After that, four short questions: your situation, the first thing the
brain should help with, the language your notes live in (German works
fine), and the next date you must not miss. From those answers Claude
builds your first real notes: your areas, your first project, your
deadlines, and a `Home` page that shows it all. A company brain starts
differently, with one procedure written down and the role that owns it.

*(Advanced alternative: clone the repo yourself, `cd` into it, start
`claude` and say: "Read SETUP-FOR-CLAUDE.md and set up my brain
accordingly.")*

✅ **Checkpoint:** `ls ~/Brain` (or whichever path Claude named) shows
numbered folders from `00-inbox` to `90-archive` — exactly which ones
depends on your answer above — plus a `_templates` folder, where the note
blueprints live. Every folder that holds notes also carries an `index.md`
and a three-line `CLAUDE.md`: the signposts Claude navigates by, safe for
you to ignore. And Claude tells you your first project (in a company
brain, your first procedure) is already in there. (If "capture:" isn't
recognized right away, restart Claude Code once — fresh skills load with
a new session.)

*(Chose "both, kept separate"? Then you get two vaults and two commands:
`claude` opens the private brain, `workbrain` the work one. Claude builds
the private one first, completely, before starting the second.)*

---

## Stage 3 — See it in Obsidian (2 min)

Obsidian → **"Open folder as vault"** → pick your vault folder (`~/Brain`
unless you chose another path; a work brain defaults to `~/Brain-work`) →
click **Home**.

This is the moment: your dashboard already shows *your* project, *your*
deadlines — a brain that's alive before you wrote a single note yourself.

✅ **Checkpoint:** `Home` names your first project under "Right now" (in a
company brain, your first procedure) and you can click through to
[[Deadlines]].

---

## Stage 4 — The onboarding interview (10–15 min, optional but worth it)

Claude offers this at the end of the setup — **your call, now or later.**
It's what turns a running brain into one that really *knows* you: your
people, your goals, your working style. Just talk — voice dumps welcome,
skipping allowed. Anything that shouldn't go in: just say "private". In a
work brain the private half is skipped by design; in a company brain the
interview is about the company's processes, roles and terms instead of
about you.

✅ **Checkpoint:** Obsidian shows "About me" and individual people notes
under `30-knowledge/people/` — and the graph view shows its first
connections. (Company brain: "About this vault" plus your first roles
under `60-roles/`; there are no notes about people there, on purpose.)
(Skipped it? Fine — it waits as an open question on `Home`.)

---

## Stage 5 — Practice the five verbs (5 min)

**1. Capture** — in any Claude session:
> capture: idea for the next project — draft the outline by Friday

**2. Ingest** — drop a PDF (handout, paper, contract, manual) into
`~/Brain/00-inbox/raw/` and say:
> ingest

**3. Ask** — the librarian, answers only from your notes:
> what does my brain know about my first project?

**4. Review** — weekly (or right now, to test it):
> brain review

**5. Research** — the power move:
> research my brain

✅ **Checkpoint:** After the review, the only things still sitting in
`00-inbox/` are `Inbox rule.md`, `index.md`, `CLAUDE.md` and the `raw/`
folder. **Those always stay** — the rule page is a permanent instruction sheet, and `raw/` is
the drop zone for the next PDF. "Inbox to zero" means every *capture* is
gone: yours has become a linked note somewhere else, and `Home` lists it
under "New this week". The review also runs a check for orphaned notes
and dead links and tells you what it fixed.

---

## Your first week

| Day | What to do |
|---|---|
| Day 1 | Setup (this tutorial) — interview now or later |
| Day 2–4 | Only **capture** — every idea, date, person. No sorting! |
| Day 5 | First **"brain review"** — watch the inbox turn into notes and `Home` refresh itself |
| Day 6–7 | Pull the first **output**: "Build me a study sheet / project plan / draft for X from my notes" — and try **"research my brain"** (Claude fills your open questions with sourced facts) |

After that the system carries itself: capture on the side, ten minutes of
review per week — and if you disappear for a month, the next review just
catches up. **The success metric is output** — if the brain hasn't gifted
you a text, plan or study sheet after two weeks, tell Claude exactly that.

---

## If something breaks

→ [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — and when in doubt: **just ask
Claude** ("why isn't my inbox empty?").
