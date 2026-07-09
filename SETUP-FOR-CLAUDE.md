# Setup runbook (for Claude Code — work through step by step)

You are setting up a "second brain" for your human: an Obsidian vault that
you read and maintain in every session. This kit contains ONLY structure —
no one else's content.

**Design goal: the first visible win within minutes.** Ask little, build
early, show results. The deep interview comes AFTER the human has seen
their brain work — never before.

## Step 0 — You are the guide
The human may not know this kit, Obsidian, or Git. **You drive:**
- Given only the repo URL? Clone it yourself first:
  `git clone https://github.com/nikolajhh2008-svg/brainwarden.git`
- Check ALL prerequisites before starting: **Obsidian** installed (if
  not: obsidian.md, wait), **git** available (`git --version`; if missing,
  guide the install — on macOS `xcode-select --install`), git identity set
  (`git config user.name` — if empty, set a name/email with their OK, or
  they hit "Please tell me who you are" at the first commit), and
  **python3** available (`python3 --version`; on Windows try `py`). No
  git? The setup still works — skip the clone (download the ZIP) and the
  commit steps, and say so.
- Explain each step in ONE sentence before doing it.
- Ask before touching `~/.claude/CLAUDE.md` (step 4).
- **Already have a vault?** Adopt, don't overwrite: scan their existing
  folder structure, map it onto the rules (inbox? projects? areas?) and
  only add what's missing. If the structures clash badly, offer the
  **quarantine path** instead: move their old notes into
  `~/Brain/OLD_VAULT/` (visible, untouched, still theirs) and integrate
  them gradually at reviews. Never delete or restructure existing notes
  without an explicit OK per change.

## Step 1 — Create the vault
**First check whether `~/Brain` already exists.** If it does: STOP and
ask — adopt it (Step 0), merge into it, or let them pick another path.
Never copy over an existing folder unasked.

Fresh install: `mkdir -p ~/Brain && cp -R vault-template/. ~/Brain/`
(note the `/.` — it copies contents incl. hidden `.tools/`, no nesting).
Verify: `~/Brain/CLAUDE.md` and `~/Brain/.tools/search.py` exist. You may
delete the cloned repo folder after setup — mention it.

## Step 2 — Install the skills
Check for name collisions first: if `~/.claude/skills/brain-capture`
(or -ingest / -review / -research / -ask) already exists, STOP and ask —
never overwrite an existing skill silently. Then
`mkdir -p ~/.claude/skills` and copy the five folders from
`skills/` into it.
Loading note: if `~/.claude/skills/` already existed, new skills load
live in the current session; if the directory was just created, one
restart of Claude Code is needed before the first "capture:".

## Step 3 — Adapt to the human + build the first win (the most important step)

### 3a. Three questions — ONE short message, then you do the heavy lifting
1. **What's your life right now?** (school / university / job / own
   business / mix — free text is fine)
2. **What's the first thing this brain should help you with?** (an exam,
   a project plan, an application, a decision to make … — this becomes
   the first project)
3. **Which language should your notes live in?** (the repo is English;
   the content can be German, anything)

Do NOT ask anything else before the first win. Never mention PARA or
Zettelkasten by name — you translate answers into structure; methods are
your job, not theirs.

### 3b. Build the first win — real notes, within minutes
From those answers, without further questions:
1. **Propose 2–4 areas** derived from answer 1, in THEIR words ("I'd
   create these areas for you: … — rename anything"), then create them as
   subfolders in `20-areas/`, each with ONE seed note named like the
   folder (e.g. `20-areas/studies/studies.md`, from
   `_templates/area-note.md`).
2. **Create the first project** in `10-projects/` from answer 2 (template:
   `_templates/project-note.md`) — with real content: the goal in their
   words, a concrete next step, and any date they mentioned (dates ALSO go
   to `Deadlines.md`).
3. **Fill `Home.md`:** their project under "Right now" (as a
   `[[wikilink]]` with a one-line status), an "Areas:" line linking every
   area seed note (so no note starts as an orphan), their dates under
   "Next deadlines", anything you couldn't fill under "Open questions".
   Home is the living dashboard — from now on it always reflects the
   current state of the brain.
4. **Set the language:** replace `{{LANGUAGE}}` in `~/Brain/CLAUDE.md`.
   If it's not English, translate `Home.md`, `Inbox rule.md`,
   `About me.md`, `Deadlines.md` and the `_templates/` into it (the
   vault's `CLAUDE.md` stays English by design — it is read by Claude,
   not by them).
5. **Show it:** have them open Obsidian ("Open folder as vault" →
   `~/Brain`) and click **Home**. A populated brain, minutes in, before
   any interview — that moment is the point of this whole step.

### 3c. Offer the optional modules (opt-in menu, create ONLY what they pick)
Present this list in one short message; each pick becomes a numbered
top-level folder — **the gaps in the numbering (50–80) exist exactly for
this**:
- **`50-journal/`** — daily/weekly journaling (template ships with the
  kit: `_templates/journal-entry.md`)
- **`60-media/`** — reading/watch log (books, papers, videos with one-line
  verdicts)
- **`70-health/`** or **`70-training/`** — workouts, habits, metrics
- **`80-money/`** — budgets, subscriptions, financial decisions
- or anything they name themselves — their word, their folder

Rules for modules: numbered top-level folder, one intro note inside,
linked from `Home.md` ("How to use your brain" block). Skippers lose
nothing — modules can be added any time later by just asking Claude
("add a journal module to my brain").

### 3d. What is fixed vs. free (tell them this!)
- **Fixed (the skills depend on it):** English top-level folder names for
  `00-inbox`, `10-projects`, `20-areas`, `30-knowledge`, `40-decisions`,
  `90-archive` — and the numbered-prefix scheme.
- **Free:** everything else — area names, module folders (50–80), all
  content language, templates (delete what they won't use), even the
  weekly review day.

### 3e. Fill in remaining placeholders
Ask for their first name. Replace `{{NAME}}` in
`~/Brain/40-decisions/_template.md` and `{{DATE}}` in `About me.md` +
`Deadlines.md` with today's date.
**Leave `_templates/` untouched** — their `{{DATE}}`/`{{NAME}}`
placeholders are filled per note, at creation time, forever.

## Step 4 — Global rules
With their OK, add to `~/.claude/CLAUDE.md` (create if missing):

```markdown
## Brain (~/Brain — Obsidian vault + Claude working directory)
- Retrieval: run `python3 ~/Brain/.tools/search.py <terms>` first, then
  read only the hits — never the whole vault. "What do I know about X?"
  → skill brain-ask.
- Capture triggers: whenever a session produces (a) a decision, (b) a
  deadline, (c) a milestone, (d) a new person, (e) a hard-won lesson →
  file it to ~/Brain/00-inbox/ immediately (brain-capture).
- Weekly ritual: "brain review" (inbox to zero, hygiene, refresh Home.md,
  git commit).
```

This block is what makes the brain ambient: EVERY future Claude session —
whatever project is open — knows where the brain lives and when to write
to it. Without it, the brain only exists inside the vault folder.

## Step 5 — Git: commit the clean scaffold
`cd ~/Brain && git init && git add -A && git commit -m "brain setup"`
(Before the interview, so the first commit is the clean baseline.)
If the git identity was missing in Step 0, set it **repo-local** here —
`cd ~/Brain && git config user.name "…" && git config user.email "…"` —
never `--global` without asking first.

## Step 6 — Offer the onboarding interview (recommended — but THEIR call)
The brain is already usable. Offer the deepening, don't impose it:

> "Your brain is running. The next step is the onboarding interview
> (10–15 minutes) — it's what makes the brain really *know* you.
> Now or later?"

- **Now:** run `INTERVIEW.md` (this kit) — start with its Phase-0 consent
  question (may Claude scan the computer to pre-fill?), then interview
  with the per-block nudges, in the vault language. Style models:
  `examples/`. Afterwards refresh `Home.md` and commit.
- **Later:** write one note to `00-inbox/` ("run the onboarding
  interview — say: *interview me for my brain*") and list it under Home's
  "Open questions". Never pressure — the interview also works in pieces.

Either way, if anything changed after Step 5's baseline commit:
`cd ~/Brain && git add -A && git commit -m "onboarding"` — never hand
over a dirty tree.

## Step 7 — Verify, then hand over
Run this checklist and show the results (fix anything that fails):
- [ ] `ls ~/Brain` shows `00-inbox` … `90-archive` + their modules
- [ ] `~/Brain/Home.md` names their real first project under "Right now"
      (not the template placeholder line)
- [ ] `python3 ~/Brain/.tools/search.py test` runs without error
- [ ] `ls ~/.claude/skills/` shows the five brain-* skills
- [ ] `grep Brain ~/.claude/CLAUDE.md` shows the rules from step 4
- [ ] `cd ~/Brain && git log --oneline` shows the setup commit
- [ ] No setup placeholders left OUTSIDE the templates:
      `grep -rnE "\{\{(NAME|LANGUAGE|DATE)\}\}" ~/Brain --exclude-dir=_templates | grep -v "_template.md"`
      (templates keep their placeholders on purpose — never "fix" them)

If anything above fails mid-setup and can't be fixed: a fresh install
may simply be removed (`rm -rf ~/Brain`) and restarted — say so instead
of leaving a half-built vault.

Hand over with a 30-second demo of the five verbs, each one line:
**capture** (dump a thought) · **ingest** (drop a PDF into raw/) ·
**ask** ("what does my brain know about …") · **review** (weekly,
~10 min) · **research** ("research my brain" — fills open questions with
sourced facts). Finish with one sentence on how to extend later: "Ask me
to add a module, rename an area, or change the language — the structure
grows with you."

## Updating a vault built with an older kit version

Someone already ran this setup before? Never rebuild — update in place.
Their notes are sacred; an update only ever replaces kit infrastructure
(skills, search tool, dashboard, rules):

1. **Fresh clone** of this repo (old clones may predate a history rewrite
   — if `git pull` errors, delete the old clone folder and re-clone).
2. **Skills:** replace the old `brain-*` folders in `~/.claude/skills/`
   with the current five from `skills/`. If their skills were
   personalized (translated, custom paths), diff first and port the new
   features instead of overwriting — ask, don't assume.
3. **Vault additions, never content changes:** create `Home.md` from the
   template and fill its blocks from their real notes; if an old
   `Start here.md` exists, fold its links into Home, update backlinks to
   it, then remove it; refresh `.tools/search.py` with the current
   version; update the Commands section of their vault `CLAUDE.md`.
4. Re-run the Step-7 checklist, then `git commit -m "kit update"`.
