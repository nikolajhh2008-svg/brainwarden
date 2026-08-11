# Setup runbook (for Claude Code — work through step by step)

You are setting up a "second brain" for your human: an Obsidian vault that
you read and maintain in every session. This kit contains ONLY structure —
no one else's content.

**Design goal: the first visible win within minutes.** Ask little, build
early, show results. The deep interview comes AFTER the human has seen
their brain work — never before.

**One runbook, three modes.** There is no second runbook. `personal`,
`professional` and `company` run through the same steps below; the mode
only decides which folders exist, which files are created, which questions
you ask and what the first win is. Every mode-specific instruction is
marked as such — everything unmarked applies to all three.

**Two substitutions you make everywhere, in every command and in every
file you write:**
- `<vault>` → the vault's real absolute path (e.g. `/Users/lena/Brain`).
- `<python>` → the python command that actually worked in Step 2
  (`python3`, `python` or `py -3`).

Never leave `<vault>`, `<python>` or a default path like `~/Brain` in a
file you created for a vault that lives somewhere else. A leftover
placeholder points every future session at a path that does not exist.

## Step 0 — How you run this setup (posture — no questions yet)
The human may not know this kit, Obsidian, or Git. **You drive:**
- Speak the human's language: from your very first reply, run the
  entire conversation (checks, questions, explanations) in the
  language they use with you — this runbook is English, the
  conversation is theirs.
- Explain each step in ONE sentence before doing it.
- Ask before writing anything outside the vault: `~/.claude/CLAUDE.md`,
  the skills directory (Step 4), the shell profile (Step 4).
- Never guess an answer the human has not given. A question costs
  seconds; a wrong assumption costs the whole structure.
- Never say "mode", "personal/professional/company", "PARA" or
  "Zettelkasten" to them. You translate their answers into structure;
  methods are your job, not theirs.

## Step 1 — Ask this FIRST: which brain is this?
Before the prerequisites, before any folder, before anything else. One
short message, plain words:

> "One question before we start: is this brain for you personally, for
> your work, or one that several people in a company use together?
>
> 1 — **for me**: my life, school/studies, projects, private things
> 2 — **for my work**: my professional knowledge, kept apart from private
> 3 — **both, kept separate**: one for me, one for work
> 4 — **for a company**: several people share it and add to it"

Map their answer silently — they never have to pick a word:

| Answer | Mode(s) | Vaults |
|---|---|---|
| 1 | `personal` | one |
| 2 | `professional` | one |
| 3 | `personal` + `professional` | **two** (Steps 3–9 run once per vault) |
| 4 | `company` | one |

Any other combination they name (e.g. "for me and for our company") works
the same way: one vault per purpose, built one after the other, personal
one first. `company` is ALWAYS its own vault — never a folder inside a
private one.

Answer unclear, or "I don't know"? Default to `personal` and say so in one
sentence: *"I'll build your personal one — we can add a work brain any
time."* Never leave the mode implicit: it is recorded in Step 6 and in the
root `index.md`, and every later session reads it from there.

**What the mode actually changes — the complete difference:**

| | `personal` | `professional` | `company` |
|---|---|---|---|
| Folders | `00,10,20,30(+people),40,90` | the same **+ `50-processes/`** | `00,30,40,50,60,70,80,90` — **no** projects/areas, **no** `people/` |
| Self page | `About me.md` | `About me.md` | `About this vault.md` |
| First win | first project + dates | + first workflow | first SOP + the role that owns it |
| Frontmatter | base schema | base **+ `status:`** | base + `status:` + `owner:`/`audience:`/`confidentiality:`/`review_due:` |
| Interview | person track | person track, work only | process track (Step 8) |
| Who writes | the human | the human | anyone; published after approval |
| Modules 50–80 | free for their own | `50` taken, `60–80` free | all taken — no user modules |

`30-knowledge/people/` exists only in `personal` and `professional`. A
company vault gets `60-roles/` instead: role descriptions, not dossiers on
colleagues.

### 1a. Answer 3 — two brains, and how they stay apart
Tell them in ONE sentence what they get, no technical detail:

> "You'll get two separate brains: `claude` opens the private one,
> `workbrain` the work one — separate notes, separate rules, separate
> sessions. Nothing crosses over."

Concretely (details in Step 4 and Step 6): two vault folders at two paths,
two sets of rules, and for the second brain its own Claude Code
configuration directory plus a one-word shell alias. Build the private
vault completely first (Steps 3–9), then the work vault — never both half
way.

### 1b. `company` only — four more questions, in ONE message
1. **What's the company called?** (used for the vault name and its
   front page)
2. **Which areas are there — who does what?** (2–8 in their words:
   sales, workshop, accounting, warehouse …)
3. **Who may approve content — who says "this is now the official
   version"?** (a name or a role; may be them)
4. **Is there knowledge that not everyone in the company may see?**

To question 4, add this honestly, in one breath — never let them believe
in protection the kit does not provide:

> "A field in the file can mark something as confidential, but it does not
> lock anything: everyone who can open the folder can read every file in
> it. Real separation only comes from a second, separate vault with its
> own access rights. So: is there anything that must be genuinely
> unreadable for part of the team? Then it belongs in its own vault, and
> we decide that now, not later."

Write the four answers into `About this vault.md` (Step 5), under the
headings `Company`, `Areas`, `Approval`, `Confidential content` — add a
heading if the template does not have it yet.

### 1c. `company` only — two things you say out loud once
Not features, not settings — notices. Say them plainly, then move on, and
state clearly that this is a pointer, not legal advice; the company's
legal contact or works council decides:

- **No usage tracking.** A record of who searched for what, and when, is
  regularly subject to works-council co-determination in Austria and
  Germany (it can be used to monitor performance). This kit logs nothing
  of the kind: no search log, no per-person statistics, no usage
  telemetry — and it should stay that way. (The optional unattended
  review writes a log of what *it changed in the vault* — never who read
  or searched anything; see TROUBLESHOOTING.md.)
- **People must be able to tell it's an AI.** Since August 2026 the EU AI
  Act's transparency obligation also applies inside a company: employees
  working with an AI system must be able to recognise that. Practically:
  `About this vault.md` states in its first lines that Claude maintains
  this vault, and notes drafted by AI carry a `generated:` line in their
  frontmatter. Keep both — they are the visible part of that obligation.

## Step 2 — Prerequisites
Check ALL of these before touching anything:
- Given only the repo URL? Clone the kit yourself first:
  `git clone https://github.com/nikolajhh2008-svg/brainwarden.git`
- **Obsidian** installed (if not: obsidian.md, wait).
- **git** available (`git --version`; if missing, guide the install — on
  macOS `xcode-select --install`), and a git identity set
  (`git config user.name` — if empty, set a name/email with their OK, or
  they hit "Please tell me who you are" at the first commit).
- **python** available — try in this order and REMEMBER which one worked
  (this is `<python>` for the rest of the setup):
  `python3 --version` → `python --version` → (Windows) `py -3 --version`.
  None? Guide the install (python.org, "Add to PATH" checked).
- No git? The setup still works — skip the clone (download the ZIP) and
  the commit steps, and say so.

## Step 3 — Create the vault
Run this step once per vault (two vaults for answer 3 — the private one
first, completely, through Step 9).

### 3a. Where it lives
Default paths, offered — never imposed:

| Mode | Default path | Started with |
|---|---|---|
| `personal` | `~/Brain` | `claude` (Step 4) |
| `professional` | `~/Brain-work` | `workbrain` |
| `company` | `~/Brain-<company-slug>` (e.g. `~/Brain-acme`) | `teambrain` |

**First check whether the target path already exists.** If it does: STOP
and ask — adopt it (3c), merge into it, or pick another path. Never copy
over an existing folder unasked.

**Their vault already lives somewhere else** (iCloud folder, different
name, `~/Documents/Notes` …)? **Don't move it.** Adopt it in place and
record its real path in Step 6's `Brain vault:` line — the skills follow
that line, not a hardcoded location. The defaults above are only for fresh
installs. From here on, `<vault>` means the path you actually used.

### 3b. Fresh install (ONLY into an empty or non-existent folder)
    mkdir -p <vault> && cp -R vault-template/. <vault>/
(note the `/.` — it copies the contents including the hidden `.tools/`,
without nesting a folder inside a folder).

### 3c. Adopting an existing vault — add only what is missing
**Never run the 3b copy over an existing vault.** `cp -R` silently
overwrites files they may already have (their own `Home.md`,
`About me.md` …). Use the never-overwrite copy:

    cd vault-template && cp -Rn . <vault>/

**A non-zero exit code is expected here and means nothing is wrong.**
`-n` skips every file that already exists, and macOS BSD `cp` returns a
non-zero status when it skips. That is the safety net doing its job:
- **NEVER retry without `-n`**, and never "fix" it with `-f` or `-R` alone
  — that is precisely the command that overwrites their notes.
- Read the list of skipped files as information: those are the files they
  already had.
- Then verify that nothing of theirs changed (`cd <vault> && git status`
  if it is a Git repo, otherwise spot-check their `Home.md` and one of
  their own notes) before going on.

The rest of adopting:
- Scan their existing folder structure and map it onto the rules of this
  mode (inbox? projects? areas? processes?); add only what is missing.
- Structures clash badly? Offer the **quarantine path**: move their old
  notes into `<vault>/OLD_VAULT/` (visible, untouched, still theirs) and
  integrate them gradually at reviews. Never delete or restructure
  existing notes without an explicit OK per change.
- After adopting, list every note still living outside the core folders
  under Home's "Open questions" as a migration backlog (the reviews work
  through it), and point out that capture now writes to `00-inbox/` —
  note any pre-existing inbox file of theirs for merging at the first
  review.
- **If they already had a `Home.md`,** `cp -n` correctly skipped the
  template — but the skills need its four dashboard blocks (`Right now`,
  `Next deadlines`, `Open questions`, `New this week`). Add those four
  headings to THEIR existing Home (their own content stays above); if
  their Home is thin, offer to replace it with the template and fold
  their links in. Do this BEFORE Step 5 — every later "fill Home"
  instruction assumes the blocks exist.
- On an adopted vault, **never delete a folder** because this mode does
  not use it (3d). Leave it, and note it under Home's "Open questions".

### 3d. The folders of this mode
After a fresh copy (3b), the vault holds every folder the kit ships.
Remove what this mode does not use — **only ever directly after a fresh
copy into an empty folder, never on an adopted vault:**

- `personal`:
  `cd <vault> && rm -rf 50-processes 60-roles 70-onboarding 80-partners "About this vault.md"`
- `professional`:
  `cd <vault> && rm -rf 60-roles 70-onboarding 80-partners "About this vault.md"`
- `company`:
  `cd <vault> && rm -rf 10-projects 20-areas 30-knowledge/people "About me.md"`

What must exist afterwards:

| Mode | Folders |
|---|---|
| `personal` | `00-inbox/` (+`raw/`), `10-projects/`, `20-areas/`, `30-knowledge/` (+`people/`), `40-decisions/`, `90-archive/` |
| `professional` | the same **+ `50-processes/`** |
| `company` | `00-inbox/` (+`raw/`), `30-knowledge/`, `40-decisions/`, `50-processes/`, `60-roles/`, `70-onboarding/`, `80-partners/`, `90-archive/` |

Plus, in every mode: `_templates/`, `.tools/`, `Home.md`, `Deadlines.md`,
`CLAUDE.md`, `index.md`, and the self page (`About me.md`, or
`About this vault.md` in `company`).

A folder this mode needs is missing from the template? Create it
(`mkdir -p <vault>/50-processes`) and give it its two waypoint files (3e).

### 3e. Waypoints — two files per folder
**Every folder that holds notes gets exactly two navigation files.** This
is what lets an agent that lands in a folder cold keep going without
guessing:

- `CLAUDE.md` — always exactly this content, nothing else:
  ```markdown
  <!-- Loaded automatically when Claude reads a file in this folder. -->
  @index.md
  ```
- `index.md` — the waypoint, max ~25 lines, in the vault language:
  ```markdown
  # <folder name>

  <one line: what lives here>

  **Rules here:** <only what differs from the vault rules>
  **NOT here:** <where that belongs instead, with a real path>

  ## Entry points
  * [note-name](note-name.md) - one line why you'd start here

  <!-- generated: YYYY-MM-DD -->
  ```

Rules for `index.md`: real relative paths, **never** `[[wikilinks]]` (a
wikilink carries no path and an agent cannot resolve it); no file names
with spaces; only entry points, never a full file listing; nothing an
agent could see for itself. Nothing to list yet? Write
`* (none yet — the first note lands here)`.

The template ships these files — keep what is there, create what is
missing, and after Step 5 update the "Entry points" of every folder you
actually filled. `_templates/` and `.tools/` get NO waypoints: they hold
tooling, not notes, and the search tool skips them.

The **root `index.md`** is the cold entry for any agent and states: the
mode, the vault language, a one-line map per folder, the pointer to
`Home.md` (for the human) and `CLAUDE.md` (the rules), and the search
command with the real `<python>` and the real `<vault>` path.

### 3f. Keep the interview script
Copy the interview into the vault before the cloned repo folder is
deleted, so the deep interview still has its script weeks later:

    cp INTERVIEW.md <vault>/.tools/

`.tools/` is kit infrastructure, not vault content: it is excluded from
search and from the placeholder check in Step 9. Never edit the copy, and
never "fill in" anything inside it.

**Verify this step:** `<vault>/CLAUDE.md`, `<vault>/index.md`,
`<vault>/.tools/search.py` and `<vault>/.tools/INTERVIEW.md` exist. You
may delete the cloned repo folder after the setup — mention it.

## Step 4 — Install the skills
Installed the kit as a Claude Code plugin? The five skills are already
loaded — skip the copying, but read 4b if there are two brains.

### 4a. One brain (the normal case)
Check for name collisions first: if `~/.claude/skills/brain-capture`
(or `-ingest` / `-review` / `-research` / `-ask`) already exists, STOP and
ask — never overwrite an existing skill silently. Then
`mkdir -p ~/.claude/skills` and copy the five folders from `skills/` into
it.

Loading note: if `~/.claude/skills/` already existed, new skills load live
in the current session; if the directory was just created, one restart of
Claude Code is needed before the first "capture:".

### 4b. Two brains — separate configuration directories
The first brain keeps the normal setup (`~/.claude`), so its capture
triggers work in every session — that ambient reach is the point of the
whole kit. Which one is first: the `personal` one if there is one,
otherwise the single private/work vault. A `company` vault is **never**
the ambient one — company content must not leak into private sessions.

Every additional brain gets its own configuration directory. `Brain #2`
below stands for `~/.claude-work` (professional) or
`~/.claude-<company-slug>` (company):

1. `mkdir -p ~/.claude-work/skills`
2. copy the same five skill folders in there as well (each configuration
   directory needs its own copy)
3. with their OK, add one line to their shell profile (`~/.zshrc` on
   macOS, `~/.bashrc` on most Linux/Git-Bash setups):
   ```bash
   alias workbrain='CLAUDE_CONFIG_DIR=~/.claude-work claude'
   ```
   (`company`: `alias teambrain='CLAUDE_CONFIG_DIR=~/.claude-acme claude'`)
4. `source ~/.zshrc` (or open a new terminal), then `workbrain` starts
   Claude Code with the work brain's rules, skills and sessions only.

`CLAUDE_CONFIG_DIR` is Claude Code's documented way to keep two setups
apart: rules (`CLAUDE.md`), skills and session history live inside that
directory — so the work brain's rules never load in a private session and
vice versa. Say ONE sentence about it; the human does not have to
understand it, only see that it is cleanly separated, and know the two
words they type: `claude` for private, `workbrain` for work. Expect a
one-time login prompt at the first start in a fresh configuration
directory — that is normal, not an error.

Only if they explicitly ask for their everyday `claude` sessions to stay
brain-free: give BOTH brains an alias (`brain` and `workbrain`, each with
its own configuration directory) and leave `~/.claude/CLAUDE.md`
untouched — then nothing is ambient and every capture happens inside a
brain session.

## Step 5 — Adapt to the human + build the first win (the most important step)

### 5a. The questions — ONE short message, then you do the heavy lifting
`personal` / `professional`:
1. **What's your life right now?** (school / university / job / own
   business / mix — free text is fine) — in a work brain: what your work
   actually consists of.
2. **What's the first thing this brain should help you with?** (an exam,
   a project plan, an application, a decision to make … — this becomes
   the first project)
3. **Which language should your notes live in?** (the repo is English;
   the content can be German, anything)
4. **What's the next date you must not miss?** (one is enough — an exam,
   a submission, an appointment, a renewal, a trip)

`company` (the four questions from 1b are already answered):
1. **Which process should we write down first — something you could
   explain to a new colleague today?** (order intake, month-end closing,
   handling a complaint, onboarding a supplier …)
2. **Which language should the content live in?**
3. **Which fixed date must this vault not miss?** (audit, inventory,
   contract renewal, a recurring monthly deadline)

Question 4 (resp. 3) is not small talk: without one real date, the "Next
deadlines" block on `Home` stays empty and the first win is only half
visible. If nothing comes back, nudge ONCE with concrete examples
(*"exam · rent · a contract that renews · a birthday · a doctor's
appointment"*). Still nothing? Write `- (no dates yet)` into that block
and put "collect the first dates" under Home's "Open questions" — then
move on.

Do NOT ask anything else before the first win.

### 5b. Build the first win — real notes, within minutes
From those answers, without further questions.

**House rules while you build** (they resolve the questions two setups
would otherwise answer differently):
- **One note = one file.** A project is `10-projects/<slug>.md`, an area
  `20-areas/<slug>.md`, a process `50-processes/<slug>.md`. Never create
  a folder for a single note. A note becomes a folder only when a SECOND
  file genuinely belongs to it — then `10-projects/<slug>/` holds
  `<slug>.md` plus the two waypoint files from 3e.
- **`maturity:` is for knowledge notes only** (`seed` / `growing` /
  `evergreen`, in `30-knowledge/`). Project, area, process, role,
  partner and decision notes get NO maturity — they are not "thin", they
  are current or outdated, and that is what `status:` is for.
- **`status: draft | stable | deprecated`** on every note outside
  `00-inbox/` from `professional` upwards; in `company` mode plus
  `owner:`, `audience:`, `confidentiality:` and `review_due:` (default:
  today + 12 months — say that you set it).
- File names kebab-case, no spaces, no umlauts; the CONTENT is in their
  language.
- Every date you hear also goes into `Deadlines.md` — one line, date
  first.

**Adopting?** Search before you build: run `search.py` for the project,
areas or processes from their answers — if they already exist somewhere in
the old structure, MOVE them into place (one OK per move) and enrich them.
Never create a duplicate next to their original.

**`personal` / `professional`:**
1. **Propose 2–4 areas** derived from answer 1, in THEIR words ("I'd
   create these areas for you: … — rename anything"), then create one
   note per area in `20-areas/` from `_templates/area-note.md`, named
   like the area (`20-areas/studies.md`).
2. **Create the first project** in `10-projects/` from answer 2
   (`_templates/project-note.md`) — with real content: the goal in their
   words, a concrete next step, and every date from answer 4.
3. **`professional` additionally: the first workflow.** Take the
   recurring task from answer 1 that annoys them most and write it into
   `50-processes/<slug>.md`: what triggers it, 3–7 steps in their words,
   who is involved, what usually goes wrong. That note is what turns a
   work brain from a notes folder into something that can take work off
   their plate later.
4. **Fill `Home.md`:** their project under "Right now" (as a
   `[[wikilink]]` with a one-line status), an "Areas:" line linking every
   area note (so no note starts as an orphan), the process under "Right
   now" too if there is one, their dates under "Next deadlines", anything
   you couldn't fill under "Open questions".

**`company`** (no projects, no areas — a company vault carries processes,
roles and knowledge):
1. **Write the first SOP** from their answer into
   `50-processes/<slug>.md`: purpose in one line, what triggers it, 3–7
   concrete steps in the company's own words, who owns it, what usually
   goes wrong. Their words, their terms — you write nothing they did not
   say.
2. **Create the role that owns it** in `60-roles/<role>.md`: what the
   role is responsible for, which processes it owns, what it decides —
   the ROLE, never a person dossier.
3. **Onboarding entry:** one line in `70-onboarding/index.md` (or a first
   note there) linking the SOP: "day one: read this".
4. **Fill `Home.md`:** the SOP under "Right now", the role and the
   onboarding entry as links, dates under "Next deadlines", everything
   open (approval, unanswered areas) under "Open questions".

Then, in every mode:
5. **Update the waypoints** of the folders you filled (3e): the new notes
   become "Entry points", `generated:` gets today's date.
6. **Show it:** have them open Obsidian ("Open folder as vault" →
   `<vault>`) and click **Home**. A populated brain, minutes in, before
   any interview — that moment is the point of this whole step.

### 5c. Offer the optional modules (`personal` / `professional` only)
Present this list in one short message; each pick becomes a numbered
top-level folder — **the gaps in the numbering exist exactly for this**
(`50–80` in `personal`, `60–80` in `professional`, where `50-processes/`
is taken):
- **`50-journal/`** — daily/weekly journaling (template ships with the
  kit: `_templates/journal-entry.md`)
- **`60-media/`** — reading/watch log (books, papers, videos with one-line
  verdicts)
- **`70-health/`** or **`70-training/`** — workouts, habits, metrics
- **`80-money/`** — budgets, subscriptions, financial decisions
- or anything they name themselves — their word, their folder

Rules for modules: numbered top-level folder, one intro note inside, the
two waypoint files from 3e, linked from `Home.md` ("How to use your brain"
block). Skippers lose nothing — modules can be added any time later by
just asking Claude ("add a journal module to my brain").

In `company` mode there are no user modules: `50–80` are taken by
processes, roles, onboarding and partners. Something is missing there? It
belongs into one of those four, or it is a decision (`40-decisions/`).

### 5d. What is fixed vs. free (tell them this!)
- **Fixed (the skills depend on it):** the English top-level folder names
  of this mode (3d), the numbered-prefix scheme, the kit file names
  (`Home.md`, `Deadlines.md`, `About me.md` / `About this vault.md`,
  `Inbox rule.md`, `index.md`, `CLAUDE.md`) and the four Home block
  headings (their CONTENT is free).
- **Free:** everything else — area names, module folders, all content
  language, templates (delete what they won't use), even the weekly
  review day.

### 5e. Language, name, and the remaining placeholders
1. **Set the language:** replace `{{LANGUAGE}}` in `<vault>/CLAUDE.md`
   and in the language line of the root `index.md` with the ENGLISH name
   of the language (e.g. `German`).
2. If it is not English, translate `Home.md`, `Inbox rule.md`, the self
   page (`About me.md` / `About this vault.md`), `Deadlines.md`,
   `00-inbox/raw/README.md`, the decision template
   `40-decisions/_template.md`, the `_templates/` and every `index.md`
   waypoint into it (keep the `{{…}}` placeholder tokens). The vault's
   `CLAUDE.md` stays English by design — it is read by Claude, not by
   them.
   Keep untranslated: the kit FILE NAMES, the four Home block headings,
   frontmatter keys and values (`type:`, `maturity: seed/growing/
   evergreen`, `status: draft/stable/deprecated`) and command words
   (`capture:`, `brain review`) — only prose translates.
3. **The four Home headings stay English — make that visible.** They are
   an interface, not text: the skills address the blocks by name. So the
   page must not look like an abandoned translation:
   - put an anchor comment directly above each of the four headings, so
     later kit versions can address the blocks independently of any
     visible text:
     ```markdown
     <!-- brain-block: next-deadlines -->
     ## Next deadlines
     ```
     The four anchors are `right-now`, `next-deadlines`,
     `open-questions`, `new-this-week`. If the template already ships
     them, leave them alone.
   - and add ONE line in the vault language under Home's intro:
     *"The four block headings stay English on purpose — Claude's skills
     address them by that name."*
   An agent looks for the anchor first and the heading text second: the
   anchor is an exact, language-independent token, while a heading is a
   natural-language string that translation, renaming or a typo can
   break.
4. **The first name** (`personal` / `professional`): ask for it and write
   it down in two places — after that, no session ever asks again:
   - `About me.md`, as the first line under the heading:
     `**Name:** <first name>`
   - the global rules block in Step 6, as the `Human:` line.
   In `company` mode you do not record a name: a shared vault gets no
   personal dossier, and decision records name the deciding **role**.
5. **`{{DATE}}`:** replace it with today's date in the self page and
   `Deadlines.md`, and with the real date in every note you created from
   a template. **Never fill the `{{DATE}}`/`{{NAME}}` tokens inside the
   template files** (`_templates/`, `40-decisions/_template.md`) or
   anywhere in `.tools/` — the templates are filled per note, at creation
   time, forever, and `.tools/` is tooling, not content. Translating the
   templates' surrounding prose is expected and fine — only the tokens
   stay.

## Step 6 — Global rules
With their OK, write this block into the rules file **of this vault's
configuration directory** — that is `~/.claude/CLAUDE.md` for the ambient
brain, and `~/.claude-work/CLAUDE.md` (resp. `~/.claude-<company-slug>/
CLAUDE.md`) for every additional brain from Step 4b. Create the file if it
does not exist.

```markdown
## Brain (Obsidian vault + Claude working directory)
- Brain vault: <vault>   ← the actual path; every brain-* skill uses this
- Mode: <personal|professional|company> — <one line: what belongs in here>
- Human: <first name>
- Retrieval: run `<python> <vault>/.tools/search.py <terms>` first, then
  read only the hits — never the whole vault. "What do I know about X?"
  → skill brain-ask.
- Capture triggers: whenever a session produces (a) a decision, (b) a
  deadline, (c) a milestone, (d) a new person, (e) a hard-won lesson →
  file it to <vault>/00-inbox/ immediately (brain-capture).
- Weekly ritual: "brain review" (inbox to zero, hygiene, refresh Home.md,
  git commit).
```

Before writing, substitute **every** `<vault>`, `<python>`, `<first name>`
and `<mode>` — including the two paths inside the retrieval and capture
lines. Those are the lines that break an adopted vault: a `Brain vault:`
line pointing at `~/Documents/Notes` while the capture trigger still says
`~/Brain/00-inbox/` sends every future capture into a folder that does not
exist. In `company` mode drop the `Human:` line.

Use the python command that worked in Step 2 — on most Windows machines
that is `py -3`, not `python3`.

Two or more brains? Add one line to each block so no session writes into
the wrong vault:
```markdown
- Other brain on this machine: <other vault> (work) — started with
  `workbrain`; never write its content into this vault.
```

Check yourself before moving on — this must return nothing:
```bash
grep -nE "<(vault|python|first name|mode)>" ~/.claude/CLAUDE.md
```

Re-running the setup? `grep -n "Brain vault:" ~/.claude/CLAUDE.md` first —
if the block exists, REPLACE it instead of appending a second one.

This block is what makes the brain ambient: EVERY future Claude session in
this configuration directory — whatever project is open — knows where the
brain lives and when to write to it. Without it, the brain only exists
inside the vault folder.

## Step 7 — Git: commit the clean scaffold
`cd <vault> && git init && git add -A && git commit -m "brain setup"`
(Before the interview, so the first commit is the clean baseline.)
If the git identity was missing in Step 2, set it **repo-local** here —
`cd <vault> && git config user.name "…" && git config user.email "…"` —
never `--global` without asking first.

`company` only: several people share the vault through a **private Git
remote** (each person clones and pulls) — never through a synced cloud
folder; Git plus cloud sync on the same folder is how vaults corrupt.
Before the first push, check the vault contains no credentials and no
personal data that does not belong there.

## Step 8 — Offer the onboarding interview (recommended — but THEIR call)
The brain is already usable. Offer the deepening, don't impose it:

> "Your brain is running. The next step is the onboarding interview
> (10–15 minutes) — it's what makes the brain really *know* you.
> Now or later?"

In `company` mode, ask differently — the interview is about the company,
not about them:

> "Your company brain is running. The next step is a walk-through of your
> processes (10–15 minutes): what runs how, who owns it, and the terms
> your company uses. Now or later?"

- **Now:** run `INTERVIEW.md` (this kit) — start with its Phase-0 consent
  question, then follow the track for this mode (person track for
  `personal`/`professional`, process track for `company`), in the vault
  language. Style models: `examples/`. Afterwards refresh `Home.md` and
  the waypoints, then commit.
- **Later:** write one note to `00-inbox/` ("run the onboarding interview
  — say: *interview me for my brain* — script: `.tools/INTERVIEW.md`")
  and list it under Home's "Open questions". Never pressure — the
  interview also works in pieces.

Either way, if anything changed after Step 7's baseline commit:
`cd <vault> && git add -A && git commit -m "onboarding"` — never hand over
a dirty tree.

## Step 9 — Verify, then hand over
Run this checklist and show the results (fix anything that fails).
Substitute `<vault>`, `<python>` and — for a second brain — the
configuration directory in every command:

- [ ] `ls <vault>` shows exactly the folders of this mode (3d) plus their
      modules
- [ ] every folder with notes has both waypoint files:
      ```bash
      cd <vault> && for d in [0-9]*/; do
        [ -f "$d/index.md" ] && [ -f "$d/CLAUDE.md" ] || echo "missing waypoint: $d"
      done
      ```
- [ ] `<vault>/Home.md` names their real first project (`company`: their
      real first process) under "Right now" — not the template
      placeholder line
- [ ] `<vault>/Home.md` has a real entry under "Next deadlines" (or the
      explicit "no dates yet" line plus the open question from 5a)
- [ ] `<python> <vault>/.tools/search.py test` runs without error, and
      `ls <vault>/.tools/` shows `search.py`, `hygiene.py` and
      `INTERVIEW.md`
- [ ] `ls ~/.claude/skills/` shows the five brain-* skills — with two
      brains, check the second configuration directory too
      (`ls ~/.claude-work/skills/`)
- [ ] `grep -n "Brain vault:" ~/.claude/CLAUDE.md` (resp.
      `~/.claude-work/CLAUDE.md`) shows the block from Step 6 with the
      REAL path — not `<vault>`, and not `~/Brain` unless that is the
      real path. Do NOT grep for the word "Brain": it matches any
      unrelated line that happens to contain it and reports green on a
      rules file that has no block at all.
- [ ] `cd <vault> && git log --oneline` shows the setup commit
- [ ] `company` only: every note carries the company frontmatter —
      ```bash
      cd <vault> && grep -rL "^owner:" --include="*.md" 50-processes 60-roles 70-onboarding 80-partners 30-knowledge 40-decisions | grep -vE "(index|CLAUDE|_template)\.md"
      ```
      must be empty
- [ ] No setup placeholders left OUTSIDE the templates and tooling:
      ```bash
      grep -rnE "\{\{(NAME|LANGUAGE|DATE)\}\}" <vault> --exclude-dir=_templates --exclude-dir=.tools --exclude-dir=.git | grep -v "_template.md"
      ```
      `_templates/`, `40-decisions/_template.md` and `.tools/` are
      excluded on purpose: the templates keep their tokens forever, and
      `.tools/` holds the search tool and the interview script — kit
      infrastructure, not vault content. If a placeholder shows up in
      there, the fix is the command above, never the file: "repairing"
      `.tools/INTERVIEW.md` or a template breaks the script that still
      has to work months from now.
      Note: on the ADOPT path the self page, `Deadlines.md` and
      `CLAUDE.md` arrive fresh from the template — Step 5e must still
      fill their `{{LANGUAGE}}`/`{{DATE}}` even when the "first win" was
      built from existing notes.

If anything above fails mid-setup and can't be fixed: a fresh install may
simply be removed (`rm -rf <vault>`) and restarted — say so instead of
leaving a half-built vault.

Hand over with a 30-second demo of the five verbs, each one line:
**capture** (dump a thought) · **ingest** (drop a PDF into raw/) ·
**ask** ("what does my brain know about …") · **review** (weekly,
~10 min) · **research** ("research my brain" — fills open questions with
sourced facts). With two brains, add the one sentence that matters:
`claude` opens the private one, `workbrain` the work one. Finish with one
sentence on how to extend later: "Ask me to add a module, rename an area,
or change the language — the structure grows with you." Optional extra to
mention (don't set it up unasked): "I can also schedule the weekly review
to run itself — ask me any time; see the auto-review entry in
TROUBLESHOOTING.md for the usage-cost trade-offs and where it logs."

## Updating a vault built with an older kit version

Someone already ran this setup before? Never rebuild — update in place.
Their notes are sacred; an update only ever replaces kit infrastructure
(skills, tools, dashboard, waypoints, rules) and renames frontmatter
KEYS — never note content:

1. **Fresh clone** of this repo (old clones may predate a history rewrite
   — if `git pull` errors, delete the old clone folder and re-clone).
   Check `grep "Kit version" <vault>/CLAUDE.md` to see what you're
   upgrading from (vaults older than 1.0.0 have no marker — treat them as
   pre-1.0). After the update, set the marker to the version at the top of
   this repo's `CHANGELOG.md`; its canonical place is an own line directly
   under the vault CLAUDE.md's intro paragraph, format
   `Kit version: X.Y.Z (…)`; add it there if missing.
2. **Mode:** vaults from before 2.0 have none. Ask the Step-1 question
   once, then record the answer in the Step-6 block (`Mode:` line) and in
   the root `index.md`. A vault with `10-projects/` + `20-areas/` and one
   person's content is `personal` unless they say otherwise — say which
   you assumed. Changing mode never deletes folders: if they now want a
   work brain, build the second vault fresh (Steps 3–9); if they add
   `professional` to an existing vault, only `50-processes/` is created.
3. **Skills:** replace the old `brain-*` folders in `~/.claude/skills/`
   with the current five from `skills/`. If their skills were
   personalized (translated, custom paths), diff first and port the new
   features instead of overwriting — ask, don't assume.
4. **Migrate `status:` → `maturity:` (breaking rename in 2.0).** The old
   kit used `status: seed|growing|evergreen` for maturity; `status:` is
   now reserved for validity (`draft|stable|deprecated`). Only the KEY
   changes, never a value, never a line of note text:
   - See what will change first:
     ```bash
     cd <vault> && grep -rn "^status: *\(seed\|growing\|evergreen\)" --include="*.md" .
     ```
   - Then rename in place (macOS: `sed -i ''`, Linux/Git-Bash: `sed -i`):
     ```bash
     cd <vault> && find . -name "*.md" -not -path "./.git/*" \
       -exec sed -i '' -E 's/^status: (seed|growing|evergreen)$/maturity: \1/' {} +
     ```
   - Re-run the grep — it must come back empty — then `git diff --stat`
     and commit this alone (`git commit -m "migrate status → maturity"`),
     so it can be reverted on its own.
   - A `status:` with any OTHER value (`draft`, `stable`, `deprecated`,
     or something they invented): leave it. List anything unclear and
     ask — never guess at a value.
   - Tell them in one sentence what changed and why: maturity ("how far
     is this note?") and validity ("is this still true?") are two
     different questions that used to share one field.
5. **Backfill the waypoints (new in 2.0):** every folder holding notes
   gets `index.md` + `CLAUDE.md` per 3e, with entry points taken from what
   is actually in there — the real notes, not a full listing. Existing
   `index.md` files are updated, never overwritten wholesale.
6. **Vault additions, never content changes:** create `Home.md` from the
   template and fill its blocks from their real notes — in the VAULT'S
   language (read `{{LANGUAGE}}`'s value from the vault CLAUDE.md and
   re-translate kit text, never paste the English template over a
   translated Home), including the four block anchors from 5e.3; if an
   old `Start here.md` exists, fold its links into Home, update backlinks
   to it, then remove it; refresh `.tools/` (`search.py`, `hygiene.py`)
   and the interview script (3f) with the current versions; and refresh
   the whole kit-owned vault `CLAUDE.md` from the current template —
   preserving their `{{LANGUAGE}}` value and any personal edits (diff
   first, ask when unsure), not just the Commands section.
7. **Since 1.2.0 the skills follow the `Brain vault:` line** in the global
   rules — make sure the block has one with their real vault path (add it
   if the old block predates it), plus the `Mode:` and `Human:` lines from
   Step 6.
8. Re-run the Step-9 checklist, then `git commit -m "kit update"`.
