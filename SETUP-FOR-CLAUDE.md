# Setup runbook (for Claude Code — work through step by step)

You are setting up a "second brain" for your human: an Obsidian vault that
you read and maintain in every session. This kit contains ONLY structure —
no one else's content.

**Design goal: the first visible win within minutes.** Ask little, build
early, show results. The deep interview comes AFTER the human has seen
their brain work — never before.

## Step 0 — You are the guide
The human may not know this kit, Obsidian, or Git. **You drive:**
- Speak the human's language: from your very first reply, run the
  entire conversation (checks, questions, explanations) in the
  language they use with you — this runbook is English, the
  conversation is theirs.
- Given only the repo URL? Clone it yourself first:
  `git clone https://github.com/nikolajhh2008-svg/brainwarden.git`
- Check ALL prerequisites before starting: **Obsidian** installed (if
  not: obsidian.md, wait), **git** available (`git --version`; if missing,
  guide the install — on macOS `xcode-select --install`), git identity set
  (`git config user.name` — if empty, set a name/email with their OK, or
  they hit "Please tell me who you are" at the first commit), and
  **python** available — try in this order and REMEMBER which one worked
  (you need it again in Step 4): `python3 --version` → `python --version`
  → (Windows) `py -3 --version`. None? Guide the install (python.org,
  "Add to PATH" checked). No git? The setup still works — skip the clone
  (download the ZIP) and the commit steps, and say so.
- Explain each step in ONE sentence before doing it.
- Ask before touching `~/.claude/CLAUDE.md` (step 4).
- **Already have a vault?** Adopt, don't overwrite: scan their existing
  folder structure, map it onto the rules (inbox? projects? areas?) and
  only add what's missing. If the structures clash badly, offer the
  **quarantine path** instead: move their old notes into
  `~/Brain/OLD_VAULT/` (visible, untouched, still theirs) and integrate
  them gradually at reviews. Never delete or restructure existing notes
  without an explicit OK per change. After adopting, list every note
  still living outside the core folders under Home's "Open questions"
  as a migration backlog (the reviews work through it) — and point out
  that capture now writes to `00-inbox/`; note any pre-existing inbox
  file of theirs for merging at the first review.

## Step 1 — Create the vault
**First check whether `~/Brain` already exists.** If it does: STOP and
ask — adopt it (Step 0), merge into it, or let them pick another path.
Never copy over an existing folder unasked.

**Their vault lives somewhere else** (iCloud folder, different name,
`~/Documents/Notes` …)? **Don't move it.** Adopt it in place and record
its real path in Step 4's `Brain vault:` line — the skills follow that
line, not a hardcoded location. `~/Brain` is just the default for fresh
installs. (Everywhere this runbook says `~/Brain`, substitute their
actual vault path.)

Fresh install (ONLY into an empty/new `~/Brain`):
`mkdir -p ~/Brain && cp -R vault-template/. ~/Brain/`
(note the `/.` — it copies contents incl. hidden `.tools/`, no nesting).

**Adopting an existing vault? NEVER run that copy over it** — `cp -R`
silently overwrites files they may already have (their own `Home.md`,
`About me.md` …). Copy only what's missing instead:
`cd vault-template && cp -Rn . ~/Brain/` (`-n` = never overwrite a file; on macOS BSD-cp exits NON-ZERO when it skips existing files —
that exit code is expected here, never retry without `-n`
that exists), then check nothing of theirs changed before going on.

**If they already had a `Home.md`,** `cp -n` correctly skipped the
template — but the skills need its four dashboard blocks (`Right now`,
`Next deadlines`, `Open questions`, `New this week`). Add those four
headings to THEIR existing Home (their own content stays above); if
their Home is thin, offer to replace it with the template and fold their
links in. Do this BEFORE Step 3b — every later "fill Home" instruction
assumes the blocks exist.

Verify: `~/Brain/CLAUDE.md` and `~/Brain/.tools/search.py` exist. You may
delete the cloned repo folder after setup — mention it. Before
deleting, copy `INTERVIEW.md` into the vault
(`cp INTERVIEW.md <vault>/.tools/`) so the deep interview keeps its
script when they ask for it weeks later.

## Step 2 — Install the skills
Installed the kit as a Claude Code plugin? The five skills are already
loaded — skip this step.
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
From those answers, without further questions.
**Adopting?** Search before you build: run `search.py` for the project
and areas from their answers — if they already exist somewhere in the
old structure, MOVE them into `10-projects/`/`20-areas/` (one OK per
move) and enrich them. Never create a duplicate next to their original.
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
   `About me.md`, `Deadlines.md`, `00-inbox/raw/README.md`, the decision
   template `40-decisions/_template.md` and the `_templates/` into it
   (keep the `{{…}}` placeholder tokens; the vault's `CLAUDE.md` stays
   English by design — it is read by Claude, not by them). Keep
   untranslated: the kit FILE NAMES (`Home.md`, `Deadlines.md`,
   `About me.md`, `Inbox rule.md`), the four Home block headings,
   frontmatter values (`type:`, `status: seed/growing/evergreen`) and
   command words (`capture:`, `brain review`) — only content
   translates. Replace `{{LANGUAGE}}` with the ENGLISH language name
   (e.g. `German`).
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
  `90-archive` — the numbered-prefix scheme, the kit file names
  (`Home.md`, `Deadlines.md`, `About me.md`, `Inbox rule.md`) and the
  four Home block headings (their CONTENT is free).
- **Free:** everything else — area names, module folders (50–80), all
  content language, templates (delete what they won't use), even the
  weekly review day.

### 3e. Fill in remaining placeholders
Ask for their first name (you'll use it when filling future decision
records and addressing them). Replace `{{DATE}}` with today's date in
`About me.md` + `Deadlines.md` — nothing else.
**Never fill the `{{DATE}}`/`{{NAME}}` placeholder tokens inside the
template files** (`_templates/` and `40-decisions/_template.md`) — they
are filled per note, at creation time, forever. Translating the
templates' surrounding prose into the vault language (Step 3b) is
expected and fine — only the placeholder tokens stay.

## Step 4 — Global rules
With their OK, add to `~/.claude/CLAUDE.md` (create if missing):

Use the python command that worked in Step 0 — on most Windows machines
that is `py -3`, not `python3`; write the block with the right one:

Write the vault's REAL path into the first line — the skills read it
from here, which is what lets the kit work with a vault anywhere (an
adopted iCloud vault, a different name, several machines):

```markdown
## Brain (Obsidian vault + Claude working directory)
- Brain vault: ~/Brain   ← the actual path; every brain-* skill uses this
- Retrieval: run `python3 <vault>/.tools/search.py <terms>` first, then
  read only the hits — never the whole vault. "What do I know about X?"
  → skill brain-ask.
- Capture triggers: whenever a session produces (a) a decision, (b) a
  deadline, (c) a milestone, (d) a new person, (e) a hard-won lesson →
  file it to ~/Brain/00-inbox/ immediately (brain-capture).
- Weekly ritual: "brain review" (inbox to zero, hygiene, refresh Home.md,
  git commit).
```

Re-running the setup? `grep "Brain vault:" ~/.claude/CLAUDE.md`
first — if the block exists, REPLACE it instead of appending a
second one.

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
  interview — say: *interview me for my brain* — script:
  `.tools/INTERVIEW.md`") and list it under Home's
  "Open questions". Never pressure — the interview also works in pieces.

Either way, if anything changed after Step 5's baseline commit:
`cd ~/Brain && git add -A && git commit -m "onboarding"` — never hand
over a dirty tree.

## Step 7 — Verify, then hand over
Run this checklist and show the results (fix anything that fails).
Vault not at `~/Brain`? Substitute its recorded path in every command:
- [ ] `ls ~/Brain` shows `00-inbox` … `90-archive` + their modules
- [ ] `~/Brain/Home.md` names their real first project under "Right now"
      (not the template placeholder line)
- [ ] `python3 ~/Brain/.tools/search.py test` runs without error
- [ ] `ls ~/.claude/skills/` shows the five brain-* skills
- [ ] `grep Brain ~/.claude/CLAUDE.md` shows the rules from step 4
- [ ] `cd ~/Brain && git log --oneline` shows the setup commit
- [ ] No setup placeholders left OUTSIDE the templates:
      `grep -rnE "\{\{(NAME|LANGUAGE|DATE)\}\}" ~/Brain --exclude-dir=_templates | grep -v "_template.md"`
      (templates keep their placeholders on purpose — never "fix" them;
      note: on the ADOPT path, `About me.md`/`Deadlines.md`/`CLAUDE.md`
      arrive fresh from the template — Step 3b.4/3e must still fill
      their `{{LANGUAGE}}`/`{{DATE}}` even when the "first win" was
      built from existing notes)

If anything above fails mid-setup and can't be fixed: a fresh install
may simply be removed (`rm -rf ~/Brain`) and restarted — say so instead
of leaving a half-built vault.

Hand over with a 30-second demo of the five verbs, each one line:
**capture** (dump a thought) · **ingest** (drop a PDF into raw/) ·
**ask** ("what does my brain know about …") · **review** (weekly,
~10 min) · **research** ("research my brain" — fills open questions with
sourced facts). Finish with one sentence on how to extend later: "Ask me
to add a module, rename an area, or change the language — the structure
grows with you." Optional extra to mention (don't set it up unasked):
"I can also schedule the weekly review to run itself — ask me any time;
see the auto-review entry in TROUBLESHOOTING.md for the usage-cost
trade-offs first."

## Updating a vault built with an older kit version

Someone already ran this setup before? Never rebuild — update in place.
Their notes are sacred; an update only ever replaces kit infrastructure
(skills, search tool, dashboard, rules):

1. **Fresh clone** of this repo (old clones may predate a history rewrite
   — if `git pull` errors, delete the old clone folder and re-clone).
   Check `grep "Kit version" ~/Brain/CLAUDE.md` to see what you're
   upgrading from (vaults older than 1.0.0 have no marker — treat them as
   pre-1.0). After the update, set the marker to the current version —
   its canonical place is the template's: an own line directly under the
   vault CLAUDE.md's intro paragraph, format `Kit version: X.Y.Z (…)`;
   add it there if missing.
2. **Skills:** replace the old `brain-*` folders in `~/.claude/skills/`
   with the current five from `skills/`. If their skills were
   personalized (translated, custom paths), diff first and port the new
   features instead of overwriting — ask, don't assume.
3. **Vault additions, never content changes:** create `Home.md` from the
   template and fill its blocks from their real notes — in the VAULT'S
   language (read `{{LANGUAGE}}`'s value from the vault CLAUDE.md and
   re-translate kit text, never paste the English template over a
   translated Home); if an old
   `Start here.md` exists, fold its links into Home, update backlinks to
   it, then remove it; refresh `.tools/search.py` with the current
   version; and refresh the whole kit-owned vault `CLAUDE.md` from the
   current template — preserving their `{{LANGUAGE}}` value and any
   personal edits (diff first, ask when unsure), not just the Commands
   section.
4. **Since 1.2.0 the skills follow the `Brain vault:` line** in the
   global rules — make sure the block has one with their real vault
   path (add it if the old block predates it).
5. Re-run the Step-7 checklist, then `git commit -m "kit update"`.
