---
name: brain-review
description: Weekly review of the Brain — inbox to zero, correct the record, fix what hygiene.py finds, deepen thin notes, refresh Home, and close by naming what the brain can produce next. Use when the user says "brain review", "clean up my brain", "what's in the inbox" — ideally on a fixed weekday.
---

# Brain review (5–10 minutes, weekly)

Steps 0–9 run every week; "Not every week" has its own triggers. Missed weeks are
normal — the review catches up in batches, never scolds.

**Conventions:** `<vault>` = the vault path from the `Brain vault:` line in your
global rules (none set → `~/Brain`). `python3` = your working python command (on
most Windows machines `py -3`; the global rules name it).

## Every week
0. **Load the vault rules first:** `<vault>/CLAUDE.md` (schema, note anatomy, vault
   language, mode, the red line) and `<vault>/index.md` if present. No `CLAUDE.md`?
   Wrong path or unfinished setup — say so and stop.
1. **Inbox to ZERO** (hard rule): process every file DIRECTLY in `<vault>/00-inbox/`,
   except the kit's own files (`Inbox rule.md`, `index.md`, `CLAUDE.md` — never
   processed, never deleted) and `raw/` (`brain-ingest`'s queue). Each file leaves
   through one of three exits, or through SEVERAL if it holds several things (one
   capture with a decision, two dates and a question = four exits).
   - **(a) a note:** paraphrase it (frontmatter, vault language, the matching
     `_templates/` file, placeholders filled with real values) and file by
     ACTIONABILITY: project → `10-projects/` · area → `20-areas/` · **settled
     question → `40-decisions/YYYY-MM-DD-slug.md`** (append-only) · keeper knowledge
     → `30-knowledge/` · person → `30-knowledge/people/` · **recurring task you will
     do again → `50-processes/`** · **something you did, with evidence →
     `60-contribution/`** (last two: work brains only). A meeting note is filed with
     what it is ABOUT.
   - **(b) a date:** one line in `Deadlines.md` (date first) plus one line in its
     project's running log, then delete the inbox file. No knowledge note for a date.
   - **(c) deleted** — say so; deleting is a feature. A capture that is a TASK rather
     than knowledge ("call the insurer") leaves here too: put it where tasks live
     (Home's `block:open-questions`, or its project's log), then delete the file.
   - **dedup first:** `python3 <vault>/.tools/search.py <name/topic>` — extend an
     existing note instead of creating a twin. **Triage:** reference material (links,
     clippings) gets one note, tags, done; full atomization only for material the
     person builds on.
   **Empty-file rule, wins everywhere in this skill:** a file with no body (0 bytes,
   whitespace only, or nothing but a title line) is DELETED and named in the report —
   never filed, never guessed at; the kit files above are the only exception.
   **More than ~20 files?** Prioritized batches (dates → decisions → people → rest),
   report what remains — never half-process silently.
2. **Sweep the week (the guarantee):** all four tracks, then compare with the vault.
   - **files** of the last 7 days:
     `find <work folder> -type f -mtime -7 -not -path '*/.*' | head -40` — work
     folders are named in `About me.md`, `Home.md` or project notes; ask once, then
     record them in `About me.md`.
   - **repos, only if they have any:** `git log --oneline --since="7 days ago"`.
   - **the session queue, if it exists:** `python3 <vault>/.tools/harvest.py --queue`
     lists finished sessions (when, project — no content); for those since the last
     review, ask what came out of them. No queue? Name the SessionEnd hook ONCE
     (`hooks/README.md`), never twice.
   - **the human (never skip):** "what were the 3 most important things this week —
     decisions, dates, people, milestones?" Their answer outranks both machine
     tracks; this step must never end empty.
   Also: what came of last week's dates in `Deadlines.md`? Anything brain-worthy that
   never got captured → inbox now, then through step 1.
3. **Correct the record — dates, then decisions:**
   - **Dates:** new dates → `Deadlines.md`, past dates out. **A moved date REPLACES
     its line, never appends** — hunt the old one first
     (`python3 <vault>/.tools/search.py <old-date> <topic>`), correct every hit
     (`Deadlines.md`, the project note's log, `Home.md`, any `index.md` carrying it),
     and say which files you corrected.
   - **Contradictions:** hold this week's new/changed notes against `40-decisions/`
     and flag what quietly contradicts a recorded decision ("clashes with
     [[2026-05-10-x]], decided because Y — revisit or comply?"). A reversal is a NEW
     record, never an edit of the old one, and it is written on BOTH sides (format:
     vault `CLAUDE.md`): the new file gets `## Status` + `Supersedes <path>`, and in
     the old file the `## Status` BODY is REPLACED by `Superseded by <path>` (append
     the section if it has none) plus `status: deprecated` in its frontmatter — never
     an "in force" line left standing above a supersede notice, nothing else changed.
4. **Vault state — run the tool, don't guess:** `python3 <vault>/.tools/hygiene.py`
   measures orphans, dead links, near-empty notes, notes no signpost reaches, folders
   without `index.md`, frontmatter gaps, notes past their own `stale_after`/
   `review_due`, and one-sided supersede chains. Fix what it lists; hand the human
   only what needs a decision. The findings that need more than a fix:
   - **expired:** either still true (push the date out, say why) or not
     (`status: deprecated`, or fix it) — never leave it expired.
   - **folder without `index.md`:** create one shaped like the root `index.md` (title
     · one line on what lives here · `**Rules here:**` / `**NOT here:**` where they
     differ · `## Entry points` · trailing `<!-- generated: YYYY-MM-DD -->`), plus a
     `CLAUDE.md` beside it holding exactly two lines: `<!-- Loaded automatically when
     Claude reads a file in this folder. -->` and `@index.md`. Report both.
   - **"`status:` still used for maturity":** rename that key to `maturity:`; on an
     old vault in one pass, `grep -rln "^status: \(seed\|growing\|evergreen\)"
     <vault>` — report the count.
   - **orphan clusters** (a folder of machine-written, link-less files: assistant
     memory mirrors, app exports) → ONE generated map note linking every file in it,
     filed by actionability, linked from `Home.md`, regenerated every review. NEVER
     edit the foreign files; the keep/delete/gitignore question goes to the human.
   - **no `hygiene.py` (old vault)?** Manual pass — `find <vault> -name '*.md' -size
     -1c`, spot-check this week's `[[links]]` — and report that the vault needs a kit
     version that ships it.
   Then the two things the tool cannot see:
   - **signposts:** check the entry points you touched this week for staleness FIRST
     (a date or next step quoted in an `index.md` is a second copy: fix the line or
     drop the detail). Then add today's new ENTRY POINTS — notes someone would start
     from — to each written-into folder's `index.md` as real relative paths, never
     `[[wikilinks]]`, under ~25 lines, and set its `<!-- generated: -->` to today.
     Routine notes stay out of the index but must be reachable by a `[[link]]`.
   - **decay:** `find <vault>/10-projects -name '*.md' -mtime +30` → ONE collected
     question, "archive to `90-archive/` or still active?", never one per file —
     archive beats delete for finished projects, delete beats archive for noise.
5. **Deepen 2–3 notes (this is where depth comes from):** the oldest or most-used
   `maturity: seed`/`growing` knowledge notes, preferring frontier notes (many
   outgoing `[[links]]`, few or no inbound); grow them toward the note anatomy in the
   vault `CLAUDE.md` — the missing `source:`, one concrete case or number, a limit or
   counter-position, the `[[links]]`. Research the researchable parts (rules of
   `brain-research`). **What only the human can supply** (their reasoning, example,
   number): park it in the note as `open → ask: …`, add it to Home's
   `block:open-questions`, LEAVE `maturity:` untouched. Never invent a case, a number
   or an opinion; bump `maturity:` only once the anatomy is genuinely met.
6. **Open loops and connections:** list 3–5 things that look stalled (projects
   without recent notes, `open → ask` markers), ask about them, and offer to research
   the researchable ones (skill `brain-research`). Then name 1–3 non-obvious
   connections between this week's notes and older ones; add the `[[link]]` only
   where it changes how a note reads.
7. **Refresh `Home.md`** — all four blocks, without dropping what is already in them.
   **Find each block by its HTML marker, never by its heading text**
   (`<!-- block:right-now -->` … `<!-- /block:right-now -->`, same for
   `next-deadlines`, `open-questions`, `new-this-week`); rewrite only what sits
   BETWEEN a marker pair, and never touch a line carrying `<!-- keep:… -->`.
   - **`right-now`:** active projects with a one-line status each, AND the `Areas:`
     line linking every note in `20-areas/`, rebuilt from the folder listing every
     single time — it is the area notes' only inbound link.
   - **`next-deadlines`:** the next 3 dates from `Deadlines.md` · **`open-questions`:**
     this review's open loops and parked questions · **`new-this-week`:** the 3–5
     newest or most-grown notes.
8. **The yield — the review ends with output, not with a filing report.** In order:
   - **What can the brain do now that it could not last week?** Name it concretely
     out of what you filed today — a question it can now answer, a draft it now has
     the material for — with the notes that carry it. A week that produced nothing
     usable: say so, never manufacture a win.
   - **Ask "what are you working on next?"** For their answer run
     `python3 <vault>/.tools/search.py <topic>` and lay out what is already there —
     the notes, the decisions that bind it, the dates — and the gaps to fill first
     (offer `brain-research` for the researchable ones).
   - **Offer the artifact** that material now supports (summary, draft, plan,
     checklist, comparison, study sheet) and BUILD it on their go: file it with its
     project, link it from the project note, add it to that folder's `index.md` entry
     points, and record it as one line under its project in Home's `block:right-now`.
9. **Commit and report:** `cd <vault> && git add -A && git commit -m "review YYYY-MM-DD"`,
   then report what was filed where, what was deleted, what needs their input, which
   "not every week" items ran, and what the brain produces next — every filing
   decision visible, all of it reversible via Git.

## Not every week
Each has its own trigger; say in the report which ones ran.
- **Structure check** (quarterly-ish, or when the sweep keeps producing material no
  folder fits): an area or folder that no longer matches the person's life → propose
  renaming or archiving it.
- **Maps of content** (past ~150 notes — `python3 <vault>/.tools/search.py --stats`):
  propose building or refreshing them, one per strand, 2–3 sentences of framing each,
  never a bare list of links.
- **Random revisit** (whenever the review ran short): open ONE random older note.
  Stale? Missing an obvious link? A near-twin that should merge? One improvement.

## Work mode (only when the vault `CLAUDE.md` names the mode `professional`)
- **Nothing stays `ownership: mixed`** — split or reclassify every mixed note from
  this week now.
- **The show-them test** on every person note you touched: could this be shown to
  that person if they asked for it? Facts about role, work and agreements pass;
  character judgements and guesses about motives do not — delete them, do not
  rephrase them.
- **Runbooks you actually ran this week** get a fresh `last_verified:`; anything past
  12 months gets flagged as unverified rather than quietly carried on.
- **Contribution log, five minutes:** what shipped, what you reviewed, what you
  designed or documented, who you helped, what you learned — every number with its
  source in the same line. An empty week is a valid entry; never invent impact.

## Company mode (only when the vault `CLAUDE.md` names the mode `company`)
- **`00-inbox/suggestions/` goes to zero too — it is step 1 for a second folder.**
  Each suggestion leaves through exactly one exit: (a) the person who may release it
  says yes → move it to its folder, set `status: stable` and let THEM fill
  `verified:`; (b) it needs a decision they cannot make today → leave it and name it
  in the report, with who has to decide; (c) it is wrong or already covered → delete
  it and say why. Nothing may sit unanswered through two reviews.
- People become ROLES in `60-roles/` — never personal dossiers.
- A NEW note you write goes to `00-inbox/suggestions/`; a note that already lives in
  a folder is edited in place and drops to `status: draft`, never moved out. Either
  way the human sets `verified: {by: human:<name>, at: YYYY-MM-DD}`, never you.
- Never invent an owner, a number or a field value. Missing stays missing.

## Autonomous mode (only when run unattended by a scheduler)
Headless, no human in the loop: (1) delete nothing that isn't unambiguous junk — when
unsure, file it; the step-1 empty-file rule is the exception and still wins (empty =
delete + report). (2) Never archive without asking — list candidates as questions.
(3) Route ALL questions to Home's `block:open-questions`, never to chat — including
step 2's "3 most important things" and step 8's "what are you working on next".
(4) Step 8 still runs: name what the brain can do now, and list the artifact you
would build as an offer instead of building it unasked. (5) Finish with the Home
refresh, `git commit`, and a short report to
`<vault>/.tools/logs/auto-review-YYYY-MM-DD.md` — one file per run, outside the notes
so it never counts as one; keep the last ~12, delete older ones.
