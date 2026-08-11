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
| Folders | `00,10,20,30(+people),40,90` | the same **+ `50-processes/` + `60-contribution/`** | `00,30,40,50,60,70,80,90` — **no** projects/areas, **no** `people/` |
| Self page | `About me.md` | `About me.md` | `About this vault.md` |
| First win | first project + dates | + first workflow | first SOP + the role that owns it |
| Frontmatter | base schema | base **+ `status:` + `ownership:`/`confidentiality:`** | base + `status:` + `owner:`/`audience:`/`confidentiality:`/`review_due:` |
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

Write the four answers into `About this vault.md` (Step 5), into the
fields that page already has: the company name replaces `{{COMPANY}}`
("Whose knowledge this is"), the release authority goes into "Who may
release content", the audience into "Who may read it". The list of areas
has no field yet — add it as a short `## Areas` section with one line per
area; the answer to question 4 belongs in "What is in here — and what is
not".

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
The template has ONE core plus mode overlays in `vault-template/modules/`
(`processes/` for `professional` and `company`, `company/` for `company`;
`personal` gets no overlay). Apply them in exactly this order —
`personal` stops after command 2:

```bash
# 1 — the core, every mode (note the `/.` : the CONTENTS, incl. hidden .tools/)
mkdir -p <vault> && cp -R vault-template/. <vault>/

# 2 — modules/ is kit scaffolding and must NEVER end up inside a vault
rm -rf <vault>/modules

# 3 — professional AND company
cp -R vault-template/modules/processes/. <vault>/

# 4 — company only, after command 3 and in this order
cp -R vault-template/modules/company/. <vault>/
rm -rf <vault>/10-projects <vault>/20-areas <vault>/30-knowledge/people
rm -f  <vault>/"About me.md"
rm -f  <vault>/_templates/person-note.md <vault>/_templates/project-note.md \
       <vault>/_templates/area-note.md <vault>/_templates/journal-entry.md
# these came with the processes overlay and belong to a PERSONAL work brain,
# not to a shared one: in a company vault everything belongs to the company,
# so there is no handover question and no personal contribution log
rm -rf <vault>/60-contribution
rm -f  <vault>/handover.md <vault>/_templates/contribution-entry.md \
       <vault>/_templates/learning-note.md <vault>/_templates/meeting-note.md
```

The order matters: the company overlay deliberately OVERWRITES nine core
files — six `index.md` (root, `00-inbox/`, `30-knowledge/`,
`40-decisions/`, `90-archive/`, `_templates/`), `Home.md`, `Deadlines.md`
and **`CLAUDE.md`** — because they describe a vault that does not exist
here; a signpost pointing at a missing folder makes the whole navigation
lie. `CLAUDE.md` is the one that matters most: the core version calls
itself a *personal* vault, maps `10-projects/`, `20-areas/` and
`30-knowledge/people/`, and states "one person = one note" as a thinking
rule. Left in place, an agent follows it and writes a personnel dossier
into a shared vault — the exact thing `60-roles/` forbids. The company
`Home.md` carries the SAME four block markers, so the review treats it
identically; the company `Deadlines.md` adds the four fields this mode
requires (`owner`, `audience`, `confidentiality`, `review_due`).
The `processes/` overlay likewise brings its own root `index.md`, so that
`50-processes/` appears in the cold-entry signpost. On a FRESH install that overwrite is what you want. On the
ADOPT path it is not: never run the overlay over someone's existing
`Home.md` — copy the company one aside, fold their content into it by
hand, one OK per change (3c). The six deleted templates are deleted on purpose,
not merely left unused: a person-dossier template in a vault whose rule
is "roles, never people" is a trap.

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

The mode overlays (3b, commands 3 and 4) are kit infrastructure, not
their content — apply them with plain `cp -R` even here, with one
precaution: the company overlay also carries the two CONTENT files
`Home.md` and `About this vault.md`. If either already exists in their
vault, move it aside first (`mv "<vault>/Home.md" "<vault>/Home.mine.md"`),
apply the overlay, then restore theirs and fold the template's parts into
it by hand (see the Home bullet below) — a `cp -R` would otherwise
overwrite a page they wrote. `rm -rf <vault>/modules` still applies; the
deletions in command 4 do NOT (see the last bullet below).

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
  template — but the skills need its four dashboard blocks. Copy the
  four marker pairs from `vault-template/Home.md` into THEIR Home
  (`<!-- block:right-now -->` … `<!-- /block:right-now -->`, then
  `next-deadlines`, `open-questions`, `new-this-week`, each with a
  heading above it); their own content stays above and below. If their
  Home is thin, offer to replace it with the template and fold their
  links in. Do this BEFORE Step 5 — every later "fill Home" instruction
  assumes the marker pairs exist.
- On an adopted vault, **never delete a folder** because this mode does
  not use it (3d). Leave it, and note it under Home's "Open questions".

### 3d. What must exist afterwards

| Mode | Folders |
|---|---|
| `personal` | `00-inbox/` (+`raw/`), `10-projects/`, `20-areas/`, `30-knowledge/` (+`people/`), `40-decisions/`, `90-archive/` |
| `professional` | the same **+ `50-processes/` + `60-contribution/`** |
| `company` | `00-inbox/` (+`raw/`, +`suggestions/`), `30-knowledge/`, `40-decisions/`, `50-processes/`, `60-roles/`, `70-onboarding/`, `80-partners/`, `90-archive/` — no `10-projects/`, no `20-areas/`, no `30-knowledge/people/` |

Plus, in every mode: `_templates/`, `.tools/`, `Home.md`, `Deadlines.md`,
`CLAUDE.md`, `index.md`, and the self page (`About me.md`, or
`About this vault.md` in `company`). `modules/` must NOT exist inside the
vault — if it does, command 2 of 3b was skipped.

A folder is missing? You skipped an overlay — apply it (3b). Never
hand-create a module folder: the overlay brings its `index.md`, its
`CLAUDE.md` and the matching note template with it, and a bare `mkdir`
leaves an unsigned folder behind.

`00-inbox/suggestions/` (company only) is where colleagues without
release rights contribute: everything in there is a proposal by
definition, and the weekly review empties it together with the inbox.
Say that sentence when you hand over a company vault.

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

The template and its overlays ship both files for every folder they
create, `_templates/` included — keep what is there, write the pair
yourself only for a folder you create later (a module from 5c, a promoted
project folder), and after Step 5 update the "Entry points" of every
folder you actually filled. `.tools/` is the one folder without
waypoints: it holds tooling, not notes, and search skips it.

The **root `index.md`** is the cold entry for any agent: mode, vault
language, a one-line map per folder, the pointers to `Home.md` (human)
and `CLAUDE.md` (rules), and the search command. It ships with `{{MODE}}`
and `{{LANGUAGE}}` to fill (5e); the company overlay replaces it with its
own variant. Check that its folder map matches the folders that actually
exist — an index that lists a folder the mode does not have is exactly
the lie this system exists to prevent.

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

**`company` mode — put the skills INSIDE the vault instead.** Copy the
five folders to `<vault>/.claude/skills/` and skip `~/.claude/` entirely:

```bash
mkdir -p <vault>/.claude/skills && cp -R skills/. <vault>/.claude/skills/
```

Three reasons, and they all matter more than the one line of convenience
you lose. A shared vault is *handed to people* — as a clone, a zip, a
folder on a drive — and skills that travel with it need no install step,
no admin, no instructions. They load only when Claude Code is started in
that folder, so company content never surfaces in someone's private
session. And when the vault is deleted, the skills go with it; nothing
stays behind on a leaver's machine. The trade-off is real: `capture:`
then works only inside the vault, not from any session. In a shared
vault that is the correct behaviour — a company brain should not be
ambient in someone's private work.

For `personal` and `professional`, keep them in `~/.claude/skills/`: an
ambient brain is exactly the point there.

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
   `50-processes/<slug>.md` (`_templates/sop-note.md`): what triggers it,
   3–7 steps in their words, who is involved, what usually goes wrong.
   That note is what turns a work brain from a notes folder into
   something that can take work off their plate later.
4. **Fill `Home.md`:** their project in the `right-now` block (as a
   `[[wikilink]]` with a one-line status), the "Areas:" line (the one
   carrying `<!-- keep:areas-line -->`) linking every area note, so no
   note starts as an orphan; the process in `right-now` too if there is
   one; their dates in `next-deadlines`; anything you couldn't fill in
   `open-questions`. Replace only what sits between a marker pair.

**`company`** (no projects, no areas — a company vault carries processes,
roles and knowledge):
1. **Write the first SOP** from their answer into
   `50-processes/<slug>.md` (`_templates/sop-note.md`): purpose in one
   line, what triggers it, 3–7 concrete steps in the company's own words,
   who owns it, what usually goes wrong. Their words, their terms — you
   write nothing they did not say.
2. **Create the role that owns it** in `60-roles/<role>.md`
   (`_templates/role-note.md`): what the role is responsible for, which
   processes it owns, what it decides — the ROLE, never a person dossier.
3. **Onboarding entry:** add the SOP to `70-onboarding/onboarding-path.md`
   as the first real step ("day one: read this"), with a real relative
   link.
4. **Fill `Home.md`:** the SOP in the `right-now` block, the role and the
   onboarding path as links, dates in `next-deadlines`, everything open
   (approval, areas without a process yet) in `open-questions`. Replace
   only what sits between a marker pair.
5. **Set the company frontmatter** on all three notes: `owner:` (from 1b
   question 3), `audience:`, `confidentiality:`, `review_due:` and
   `status: draft` until the person named in 1b confirms them — plus
   `generated:` on anything you drafted. `verified:` is never yours to
   fill.

Then, in every mode, two more things:
- **Update the waypoints** of the folders you filled (3e): the new notes
  become "Entry points", the `generated:` marker gets today's date.
- **Show it:** have them open Obsidian ("Open folder as vault" →
  `<vault>`) and click **Home**. A populated brain, minutes in, before
  any interview — that moment is the point of this whole step.

### 5c. Offer the optional modules (`personal` / `professional` only)
Present this list in one short message; each pick becomes a numbered
top-level folder — **the gaps in the numbering exist exactly for this**
(`50–80` in `personal`, `70–80` in `professional`, where `50-processes/`
and `60-contribution/` are taken):
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
  `Inbox rule.md`, `index.md`, `CLAUDE.md`) and the four `<!-- block:… -->`
  markers in `Home.md` (their headings and content are free — see 5e.3).
- **Free:** everything else — area names, module folders, all content
  language, templates (delete what they won't use), even the weekly
  review day.

### 5e. Language, name, and the remaining placeholders
1. **Set language and mode:** replace `{{LANGUAGE}}` (the ENGLISH name of
   the language, e.g. `German`) and `{{MODE}}` (`personal`,
   `professional` or `company`) in `<vault>/CLAUDE.md` and in the root
   `index.md`. In `company` mode additionally: `{{COMPANY}}` in
   `About this vault.md` and `70-onboarding/onboarding-path.md`, plus the
   `<…>` angle-bracket fields in `About this vault.md` (owner, purpose,
   who may read, who may release) from the answers in 1b.
2. If the language is not English, translation happens in TWO waves.
   Measured: a full pass is 23–25 files, which does not fit inside "the
   first win within minutes" — and most of those files the human never
   opens.
   **Now, before you hand over (what they will actually look at):**
   `Home.md`, `Inbox rule.md`, the self page (`About me.md` /
   `About this vault.md`), `Deadlines.md`, and the notes you wrote in
   Step 5b. That is the vault they see.
   **After the handover, in the same session, and say that you are doing
   it:** the `_templates/`, `40-decisions/_template.md`,
   `00-inbox/raw/README.md` and every `index.md` waypoint. Waypoints are
   read by agents, and an agent reads English fine — so an untranslated
   waypoint costs nothing for an hour, while a delayed first win costs
   the whole setup. Keep the `{{…}}` placeholder tokens in all of them.
   The vault's `CLAUDE.md` stays English by design — it is read by
   Claude, not by them. (A shared company vault is the exception worth
   making: there a human owner does open the rules file, so translate it
   too if they ask.)
   Keep untranslated: the kit FILE NAMES, every HTML marker comment,
   frontmatter keys and values (`type:`, `maturity: seed/growing/
   evergreen`, `status: draft/stable/deprecated`) and command words
   (`capture:`, `brain review`) — only prose translates.
3. **Translate the four Home headings too — the markers do the work.**
   `Home.md` delimits its four blocks with marker pairs
   (`<!-- block:right-now -->` … `<!-- /block:right-now -->`, likewise
   `next-deadlines`, `open-questions`, `new-this-week`). Those markers,
   not the headings, are the interface: the skills refresh what sits
   between a pair. So the visible headings belong in the vault language
   like everything else — a half-English dashboard is not a rule of this
   kit, it is a bug.
   - Translate the four headings, leave every marker byte-identical, and
     never delete a line carrying `<!-- keep:… -->` (e.g. the "Areas:"
     line) — update its content instead.
   - An HTML comment is an exact, language-independent token that
     survives translation, renaming and typos; a heading is a
     natural-language string that any of the three can break. That is
     why the marker is the anchor and the heading is free.
   - Adopted Home without markers? You added them in 3c — verify before
     translating, otherwise the first review overwrites the wrong lines.
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
- **This vault is my context. Consult it BEFORE answering from general
  knowledge** whenever a question touches my life, my work, my projects,
  my people, my past decisions, or "what did we say about X". Do not
  guess and do not ask me things the vault already knows.
- **On a conflict, the vault wins.** If a note and your training data
  disagree about my situation, the note is right and you say so.
- Cold start in the vault: read `<vault>/index.md` (the folder map, one
  line each) — then `<vault>/CLAUDE.md` before writing anything.
- Retrieval: run `<python> <vault>/.tools/search.py <terms>` first, then
  read only the hits — never the whole vault. Landed in a folder? Its
  `index.md` says what belongs there and what does not. "What do I know
  about X?" → skill brain-ask.
- Capture triggers: whenever a session produces (a) a decision, (b) a
  deadline, (c) a milestone, (d) a new person, (e) a hard-won lesson →
  file it to <vault>/00-inbox/ immediately (brain-capture). One line of
  confirmation is enough; never let it interrupt what we were doing.
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
grep -nE "<(vault|python|first name|personal\|professional\|company)>|^- Mode: *$" ~/.claude/CLAUDE.md
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

## Step 8 — Two ways to deepen: the harvest, then the interview

The brain works. What it lacks is depth, and there are two sources for
that: what the machine already recorded, and what only the human can say.
Offer the harvest FIRST — an interview that starts from real material asks
better questions than one starting from nothing.

### 8a. The harvest (optional, `personal` and `professional` only)

Claude Code keeps session transcripts in `~/.claude/projects/` as plain
text, 30 days by default. For anyone who has used it for a while, that is
the richest record of how they actually work that exists on their disk —
and it expires. In a `company` vault, skip this step entirely: those
transcripts are personal, and a shared vault is the wrong place for them.

**The rule that makes this safe: nothing is read without a yes, nothing is
written without a second yes.**

1. **Inventory, reading nothing.** `python3 <vault>/.tools/harvest.py`
   prints how many sessions exist, over what period, in which projects —
   file metadata only, no content. Show it and ask whether to go on.
2. **State the expiry, once.** If `cleanupPeriodDays` is unset, the
   default is 30 days and older transcripts are already gone. Offer to
   raise it (`~/.claude/settings.json`) — their call, and a change to
   their configuration, so it needs an explicit yes.
3. **Pre-filter with no model at all.**
   `python3 <vault>/.tools/harvest.py --candidates --since <date>` drops
   harness injections, system plumbing, acknowledgements, duplicates and
   anything without a decision/date/milestone/lesson word in it. Measured
   on a real machine: 1500 human turns in, 34 candidates out. This costs
   nothing and takes seconds, which is the point — the documented failure
   mode of automatic capture is a vault drowning in its own noise (an
   audit of one such system found 97.8% of entries worthless).
4. **Judge a SAMPLE, not the archive.** Take the newest ~20 candidates,
   turn them into proper notes yourself, and show them. If that harvest
   does not convince them, a bigger one will not either — it will just
   take longer.
5. **Only then the rest**, and only with their go.
6. **Every harvested note carries its origin** — the date and the session
   it came from, in the note. Without it, nobody can tell a remembered
   fact from an invented one six months later.
7. **A harvested note is never a decision record.** Decisions get written
   by the human, or confirmed by them; a transcript line that *sounds*
   like a decision is a candidate for a question, not a record.

Cap it: **at most 3 notes per session** harvested, and "nothing worth
keeping in this one" is a correct and frequent result.

### 8b. The onboarding interview (recommended — but THEIR call)
The brain is already usable. Offer the deepening, don't impose it. If the
harvest ran, name the gaps it left and let the interview close those
first — that is a better opening than a generic questionnaire:

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
      own modules — and **no `modules/` folder** (that one is kit
      scaffolding; if it is there, run `rm -rf <vault>/modules`)
- [ ] every folder with notes has both waypoint files:
      ```bash
      cd <vault> && for d in [0-9]*/; do
        [ -f "$d/index.md" ] && [ -f "$d/CLAUDE.md" ] || echo "missing waypoint: $d"
      done
      ```
- [ ] `<vault>/Home.md` names their real first project (`company`: their
      real first process) in the `right-now` block — not the template
      placeholder line
- [ ] `<vault>/Home.md` has a real entry in the `next-deadlines` block
      (or the explicit "no dates yet" line plus the open question from 5a)
- [ ] all four marker pairs survived editing and translation:
      ```bash
      grep -o "<!-- /\?block:[a-z-]*  *-->" <vault>/Home.md | wc -l   # 8 = 4 pairs
      ```
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
      grep -rnE "\{\{(NAME|LANGUAGE|DATE|MODE|COMPANY)\}\}" <vault> --exclude-dir=_templates --exclude-dir=.tools --exclude-dir=.git | grep -v "_template.md"
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
to run itself — ask me any time; it writes what it did to
`<vault>/.tools/logs/auto-review-YYYY-MM-DD.md`, and the auto-review
entry in TROUBLESHOOTING.md has the usage-cost trade-offs first."

## Updating a vault built with an older kit version

Someone already ran this setup before? Never rebuild — update in place.
Their notes are sacred; an update only ever replaces kit infrastructure
(skills, tools, dashboard, waypoints, rules) and renames frontmatter
KEYS — never note content:

1. **Fresh clone** of this repo (old clones may predate a history rewrite
   — if `git pull` errors, delete the old clone folder and re-clone).
   Check `grep "Kit version" <vault>/CLAUDE.md` to see what you're
   upgrading from (vaults older than 1.0.0 have no marker — treat them as
   pre-1.0). After the update, set the marker to the version this clone
   actually is — read it from `.claude-plugin/plugin.json` (top-level
   `version`), never from `CHANGELOG.md`'s top heading, which
   says `[Unreleased]` between releases. Its canonical place is an own
   line directly under the vault CLAUDE.md's intro paragraph, format
   `Kit version: X.Y.Z (…)`; add it there if missing.
2. **Mode:** vaults from before 1.3 have none. Ask the Step-1 question
   once, then record the answer in the Step-6 block (`Mode:` line) and in
   the root `index.md`. A vault with `10-projects/` + `20-areas/` and one
   person's content is `personal` unless they say otherwise — say which
   you assumed. Changing mode never deletes folders: if they now want a
   work brain, build the second vault fresh (Steps 3–9); if an existing
   vault becomes `professional`, apply only the processes overlay —
   `cp -R vault-template/modules/processes/. <vault>/` — and nothing else.
3. **Skills:** replace the old `brain-*` folders in `~/.claude/skills/`
   with the current five from `skills/`. If their skills were
   personalized (translated, custom paths), diff first and port the new
   features instead of overwriting — ask, don't assume.
4. **Migrate `status:` → `maturity:` (renamed in 1.3).** The old
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
5. **Backfill the waypoints (new in 1.3):** older vaults have no
   `index.md`/`CLAUDE.md` pairs at all. Copy the ones their mode ships
   (`vault-template/`, plus the overlays for `professional`/`company`),
   then rewrite each `index.md`'s "Entry points" from what is actually in
   that folder — the real notes, never a full listing — and set the
   `generated:` marker. An `index.md` they already wrote themselves is
   updated, never overwritten wholesale.
6. **Vault additions, never content changes:** bring `Home.md` up to the
   current template — it now carries the four `<!-- block:… -->` marker
   pairs (5e.3); add them around their existing four blocks rather than
   pasting the English template over a translated Home (read
   `{{LANGUAGE}}`'s value from the vault CLAUDE.md and keep their
   language); if an old `Start here.md` exists, fold its links into Home,
   update backlinks to it, then remove it; refresh `.tools/`
   (`search.py`, `hygiene.py` — `hygiene.py` is new in 1.3 and the weekly
   review's hygiene step now depends on it) and the interview script
   (3f); and refresh the whole kit-owned vault `CLAUDE.md` from the
   current template — preserving their `{{LANGUAGE}}`/`{{MODE}}` values
   and any personal edits (diff first, ask when unsure), not just the
   Commands section.
7. **Since 1.2.0 the skills follow the `Brain vault:` line** in the global
   rules — make sure the block has one with their real vault path (add it
   if the old block predates it), plus the `Mode:` and `Human:` lines from
   Step 6.
8. Re-run the Step-9 checklist, then `git commit -m "kit update"`.
