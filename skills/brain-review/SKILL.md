---
name: brain-review
description: Weekly review of the Brain — inbox to zero, deepen thin notes, surface open loops, keep signposts and Home current, archive stale items. Use when the user says "brain review", "clean up my brain", "what's in the inbox" — ideally on a fixed weekday.
---

# Brain review (5–10 minutes, weekly)

Keeps the brain alive — second brains die of an inbox nobody empties.

**Conventions:** `<vault>` = the vault path from the `Brain vault:` line in
your global rules (none set → `~/Brain`). `python3` = your working python
command (on most Windows machines `py -3`; the global rules name it).

## Steps
0. **Load the vault rules — first, always:** Read `<vault>/CLAUDE.md`
   (schema, note anatomy, vault language, mode, the red line) and
   `<vault>/index.md` (folder map) if present. Unless this session started
   inside the vault, none of it is in your context — filing without it
   produces wrong-language, wrong-schema notes. No `CLAUDE.md`? Wrong path
   or unfinished setup — say so and stop.
1. **Inbox to ZERO** (hard rule): process every file DIRECTLY in
   `<vault>/00-inbox/` — except the kit's own files (`Inbox rule.md`,
   `index.md`, `CLAUDE.md`) and except the `raw/` subfolder (raw/ is
   `brain-ingest`'s queue; a PDF waiting there is not review work). The
   signposts are infrastructure, not captures — never process or delete
   them, not even when the empty-file rule below would seem to apply. Each file leaves through exactly ONE of three exits:
   - **(a) it becomes a note:** paraphrase it (frontmatter, vault language,
     matching template from `_templates/`; fill `{{DATE}}`/`{{NAME}}` with
     real values) and file by ACTIONABILITY: project → `10-projects/` ·
     area → `20-areas/` · **a settled question →
     `40-decisions/YYYY-MM-DD-slug.md`** (decision record, append-only,
     template `40-decisions/_template.md`) · keeper knowledge →
     `30-knowledge/` · person → `30-knowledge/people/`.
   - **(b) it becomes a date:** an appointment or deadline → one line in
     `Deadlines.md` (date first) plus one line in the running log of its
     project — then delete the inbox file. A date needs no knowledge note.
   - **(c) it gets deleted** — say so; deleting is a feature. A capture
     that is a TASK rather than knowledge ("run the onboarding interview",
     "call the insurer") leaves through here too: put the task where tasks
     live for this person — Home's `block:open-questions`, or the log of
     the project it belongs to — then delete the inbox file. A task is not
     a note.
   - **dedup before writing:** `python3 <vault>/.tools/search.py <name/topic>`
     — extend an existing note rather than creating a twin.
   - **triage:** reference material (links, clippings, recommendations)
     gets the light treatment: one note, tags, done. Full atomization is
     only for material the person builds on.
   **Empty-file rule — ONE rule, it wins everywhere in this skill:** a file
   with no body (0 bytes, whitespace only, or nothing but a title line) is
   DELETED and named in the report — never filed, never guessed at.
   **More than ~20 inbox files?** Prioritized batches (dates → decisions →
   people → rest), report what remains — never half-process silently.
2. **Sweep the week (the guarantee):** captures are best-effort, this step
   is the net. All three tracks, then compare against the vault:
   - **files** changed in the last 7 days:
     `find <work folder> -type f -mtime -7 -not -path '*/.*' | head -40`
     — work folders = those named in `About me.md`, `Home.md` or project
     notes; ask once, then record them in `About me.md`.
   - **repos, only if they have any:** `git log --oneline --since="7 days ago"`.
     Most people have none — that is not a failed sweep.
   - **the human (never skip):** "what were the 3 most important things
     this week — decisions, dates, people, milestones?" Their answer
     outranks both machine tracks and is the ONLY source when nothing
     machine-readable shows up. This step must never end empty.
   Also: what came of last week's dates in `Deadlines.md`? Anything
   brain-worthy that never got captured → inbox now, then through step 1.
3. **Deadlines:** new dates from the week → `Deadlines.md`; past dates out.
   **A moved date REPLACES its line, never appends** — two entries for one
   appointment is worse than none. Hunt the old one down first:
   `python3 <vault>/.tools/search.py <old-date> <topic>` and correct every
   hit (`Deadlines.md`, the project note's log, `Home.md`, any `index.md`
   that carries it). Say which files you corrected.
4. **Contradiction check:** hold this week's new/changed notes against
   `40-decisions/` — flag anything that quietly contradicts a recorded
   decision ("clashes with [[2026-05-10-x]], decided because Y — revisit or
   comply?"). A reversal is a NEW record, never an edit of the old one, and
   it is written on BOTH sides:
   - new file: `## Status` + `Supersedes [40-decisions/<old>.md](40-decisions/<old>.md)`
   - old file: its `## Status` BODY is replaced by
     `Superseded by [40-decisions/<new>.md](…)` (append the section if it
     has none) and its frontmatter gets `status: deprecated`. Never leave
     an "in force" line standing above a supersede notice — an agent greps
     the first `## Status` and believes it. Everything else in the old
     record stays untouched; this one section is the only exception to
     append-only.
     Without it, an agent landing there by search believes the old version.
5. **Open loops:** list 3–5 things that look stalled (projects without
   recent notes, "open → ask" markers) and ask about them — and offer:
   "want me to research the researchable ones?" (→ skill `brain-research`).
6. **Connections:** name 1–3 non-obvious connections between this week's
   notes and older ones — what search never surfaces because nobody thinks
   to search for it. Add the `[[link]]` only where it changes how a note reads.
7. **Decay:** notes in `10-projects/` untouched for more than 30 days —
   `find <vault>/10-projects -name '*.md' -mtime +30` — go into ONE
   collected question: "archive to `90-archive/` or still active?" One
   question for all of them, never one per file.
8. **Hygiene — run the tool, don't guess:**
   `python3 <vault>/.tools/hygiene.py` reports orphans, dead `[[links]]`,
   empty files, notes missing from their folder's `index.md`, frontmatter
   gaps and one-sided supersede chains. Fix what it lists; hand the human
   only what needs a decision. No `hygiene.py` (older vault)? Cheap manual
   pass — `find <vault> -name '*.md' -size -1c` for empty files, spot-check
   this week's `[[links]]` — and report that the vault should be updated to
   a kit version that ships `.tools/hygiene.py`.
   - **Migration, old vaults, once:** notes still carrying
     `status: seed|growing|evergreen` → rename that key to `maturity:`
     (`grep -rln "^status: \(seed\|growing\|evergreen\)" <vault>`).
     `status:` now means validity (`draft|stable|deprecated`). Report the count.
   - **Orphan clusters:** a whole folder of machine-written, link-less files
     (assistant memory mirrors, app exports) → ONE generated map note
     linking every file in it, filed by actionability, linked from
     `Home.md`, regenerated every review. NEVER edit the foreign files; only
     the keep/delete/gitignore question goes to the human.
   - **Past ~150 notes** (`python3 <vault>/.tools/search.py --stats`):
     propose building or refreshing maps of content — one per strand, 2–3
     sentences of framing each, never a bare list of links.
9. **Signposts (`index.md`):** check every entry point you touched this
   week for staleness FIRST — a date or next step quoted in an `index.md`
   is a second copy and rots silently; if the note behind it changed, fix
   the line or drop the detail. Then, for every folder you wrote into
   today, add the new ENTRY POINTS (notes someone would start from) to its `index.md`
   as real relative paths — never `[[wikilinks]]`, they carry no path an
   agent can resolve — keep it under ~25 lines and set the trailing
   `<!-- generated: YYYY-MM-DD -->` to today. Routine notes stay out of the
   index but must be reachable by a `[[link]]` from some note; neither →
   orphan (step 8). Folder with content but no `index.md`: create one in the
   shape of the root `index.md` (title · one line on what lives here ·
   `**Rules here:**` / `**NOT here:**` where they differ · `## Entry points`
   · generated marker), plus a `CLAUDE.md` next to it containing exactly
   two lines: `<!-- Loaded automatically when Claude reads a file in this
   folder. -->` and `@index.md`. Report both.
10. **Structure check (quarterly-ish):** an area/folder that no longer
    matches the person's life → propose renaming or archiving it.
11. **Deepen 2–3 notes (this is where depth comes from):** take the oldest
    or most-used `maturity: seed` / `maturity: growing` knowledge notes —
    prefer frontier notes (many outgoing `[[links]]`, few or no inbound
    ones: the dead-ends thinking ran into and never returned to) — and grow
    them toward the note anatomy in the vault `CLAUDE.md`: the missing
    `source:`, one concrete case or number, a limit or counter-position,
    the `[[links]]`. Research the researchable parts (rules of
    `brain-research`).
    **What only the human can supply** (their reasoning, their example,
    their number): park it in the note as `open → ask: …`, add it to Home's
    Home's `block:open-questions`, and LEAVE `maturity:` untouched. Never invent a case,
    a number or an opinion to complete the anatomy — an honest `seed` beats
    a fabricated `evergreen`. Bump `maturity:` only once the anatomy is
    genuinely met; 2–3 notes a week compounds, chasing the whole vault stalls.
12. **Random revisit:** open ONE random older note. Stale? Missing an obvious
    link? A near-twin that should merge? One concrete improvement, move on.
13. **Refresh `Home.md`** — all four blocks, without dropping what is
    already in them. **Find each block by its HTML marker, never by its
    heading text** (`<!-- block:right-now -->` … `<!-- /block:right-now -->`,
    same for `next-deadlines`, `open-questions`, `new-this-week`): the
    headings are translated into the vault language, the markers are not.
    Rewrite only what is BETWEEN a marker pair, and never touch a line
    carrying a `<!-- keep:… -->` marker — it is there because losing it
    breaks something:
    - **`block:right-now`:** active projects with a one-line status each, AND the
      `Areas:` line linking every note in `20-areas/` — rebuild that line
      from the folder listing every single time. It is the only inbound
      link the area notes have; dropping it orphans all of them.
    - **`block:next-deadlines`:** next 3 dates from `Deadlines.md` ·
      **`block:open-questions`:** this review's open loops and parked questions ·
      **`block:new-this-week`:** the 3–5 newest or most-grown notes.
14. **Commit:** `cd <vault> && git add -A && git commit -m "review YYYY-MM-DD"`.
15. **Report:** what was filed where, what was deleted, what needs their
    input — every filing decision visible, all of it reversible via Git.

## Work mode (only when the vault `CLAUDE.md` names the mode `professional`)
- **Nothing stays `ownership: mixed`.** Every mixed note from this week is
  split or reclassified now. A vault that is not separable on an ordinary
  Tuesday is not separable on someone's last day either.
- **The show-them test** on every person note you touched: could this be
  shown to that person if they asked for it? Facts about role, work and
  agreements pass. Character judgements and guesses about motives do not —
  delete them, do not rephrase them.
- **Runbooks you actually ran this week** get a fresh `last_verified:`.
  Anything past 12 months gets flagged as unverified rather than quietly
  carried on — company systems change under you without telling you.
- **Contribution log, five minutes:** what shipped, what you reviewed,
  what you designed or documented, who you helped, what you learned. Every
  number needs its source in the same line — an unsourced number is a
  self-assessment wearing a measurement's clothes. An empty week is a
  valid entry; never invent impact.

## Company mode (only when the vault `CLAUDE.md` names the mode `company`)
- People become ROLES in `60-roles/` — never personal dossiers.
- Nothing becomes company truth unattended, and the two places are not
  interchangeable: a NEW note you write goes to `00-inbox/suggestions/`
  (it does not belong in the folders yet). A note that already lives in a
  folder is edited in place and drops to `status: draft` — moving it out
  would break every link pointing at it. Either way the human sets
  `verified: {by: human:<name>, at: YYYY-MM-DD}`, never you.
- Never invent an owner, a number or a field value. Missing stays missing.

## Rules
- Never let the inbox survive a review.
- Archive beats delete for finished projects; delete beats archive for noise.
- Decision records are appended to, never rewritten.
- Missed weeks are normal — the review catches up in batches, never scolds.

## Autonomous mode (only when run unattended by a scheduler)
Headless, no human in the loop: (1) delete nothing that isn't unambiguous
junk — when unsure, file it; the step-1 empty-file rule is the exception
and still wins (empty = delete + report). (2) Never archive without asking
— list candidates as questions. (3) Route ALL questions, including step 2's
"3 most important things", to Home's `block:open-questions`, never to chat.
(4) Finish with Home refresh, `git commit`, and a short report to
`<vault>/.tools/logs/auto-review-YYYY-MM-DD.md` — one file per run, outside
the notes so it never counts as one; keep the last ~12 and delete older ones.
