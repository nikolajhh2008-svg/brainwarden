---
name: brain-review
description: Weekly review of the Brain — inbox to zero, correct the record, fix what hygiene.py finds, deepen thin notes, refresh Home, and close by naming what the brain can produce next. Use when the user says "brain review", "clean up my brain", "what's in the inbox" — ideally on a fixed weekday.
---

# Brain review (5–10 minutes, weekly)

Steps 0–9 run every week; "Not every week" has its own triggers. Missed weeks are normal — catch up
in batches, never scold.

**Conventions:** `<vault>` = the path from the `Brain vault:` line in your global rules; with no
such line, the folder this session started in, provided it holds a `CLAUDE.md` with a mode line;
only if neither exists, `~/Brain`. `python3` = your working python command (on most Windows machines `py -3`;
the global rules name it).

## Every week
0. **Load the vault rules first:** `<vault>/CLAUDE.md` (schema, note anatomy, vault language, mode,
   red line) and `<vault>/index.md` if present. No `CLAUDE.md` → wrong path or unfinished setup: say
   so and stop.
1. **Inbox to ZERO** (hard rule): process every file DIRECTLY in `<vault>/00-inbox/` — never the
   kit's `Inbox rule.md`, `index.md`, `CLAUDE.md`, never `raw/` (`brain-ingest`'s queue). One file
   may take SEVERAL exits (a decision + two dates + a question = four).
   - **(a) a note:** paraphrase it (frontmatter, vault language, matching `_templates/` file, real
     values for placeholders); file by ACTIONABILITY: project → `10-projects/` · area → `20-areas/`
     · **settled question → `40-decisions/YYYY-MM-DD-slug.md`**, append-only · keeper knowledge → `30-knowledge/`
     · person → `30-knowledge/people/` · **recurring task you will do again → `50-processes/`** ·
     **something you did, with evidence → `60-contribution/`** (last two: work brains only). Meeting
     notes file with what they are ABOUT.
   - **(b) a date:** one line in `Deadlines.md` (date first) + one in its project's log, then delete
     the file. No knowledge note for a date.
   - **(c) deleted** — say so; deleting is a feature. A TASK, not knowledge ("call the insurer"),
     goes where tasks live (Home's `block:open-questions` or its project's log), then the file goes.
   - **dedup:** `python3 <vault>/.tools/search.py <name/topic>` before writing — extend, never twin.
     **Triage:** reference material (links, clippings) = one note, tags, done; atomize only what the
     person builds on.
   **Empty-file rule, wins everywhere here:** no body — 0 bytes, whitespace, or a title line only →
   DELETE and name it in the report; never file it, never guess. Kit files excepted.
   **Over ~20 files?** Prioritized batches (dates → decisions → people → rest); report what remains,
   never half-process silently.
2. **Sweep the week (the guarantee):** four tracks, then compare with the vault.
   - **files:** `find <work folder> -type f -mtime -7 -not -path '*/.*' | head -40` — work folders
     come from `About me.md`, `Home.md` or project notes; ask once, then record them in `About me.md`.
   - **repos, if they have any:** `git log --oneline --since="7 days ago"`.
   - **the session queue, if it exists:** `python3 <vault>/.tools/harvest.py --queue` lists finished
     sessions; ask what came out of those since the last review. No queue → name the SessionEnd hook
     ONCE (`hooks/README.md`), never twice.
   - **the human (never skip):** "what were the 3 most important things this week — decisions,
     dates, people, milestones?" Cue the recall, it costs nothing: day by day (Mon, Tue, …) · by
     counterpart (the names in `30-knowledge/people/`, `60-roles/`, `80-partners/`) · by open loop
     (every date in `Deadlines.md`, every open question on `Home.md` — did anything move?). Their
     answer outranks both machine tracks; this step never ends empty, and anything brain-worthy that
     was never captured goes to the inbox now, then through step 1.
3. **Correct the record — dates, then decisions:**
   - **Dates:** new → `Deadlines.md`, past out. **A moved date REPLACES its line, never appends:**
     find the old one first (`python3 <vault>/.tools/search.py <old-date> <topic>`), correct every
     hit (`Deadlines.md`, the project's log, `Home.md`, any `index.md`), and say which files you
     corrected.
   - **Contradictions:** hold this week's new/changed notes against `40-decisions/`; flag what
     quietly contradicts a recorded decision ("clashes with [[2026-05-10-x]], decided because Y —
     revisit or comply?"). A reversal is a NEW record, never an edit, written on BOTH sides: new
     file `## Status` + `Supersedes <path>`; the old file's `## Status` BODY REPLACED by `Superseded by <path>`
     (append the section if missing) + `status: deprecated` in its frontmatter. Never an "in force"
     line above a supersede notice; nothing else in the old record changes.
4. **Vault state — run the tool, don't guess:** `python3 <vault>/.tools/hygiene.py` reports orphans,
   dead links, near-empty notes, unreachable notes, missing `index.md`, frontmatter gaps, expired
   `stale_after`/`review_due`, one-sided supersede chains. (Old vault without it: manual pass —
   `find <vault> -name '*.md' -size -1c`, spot-check this week's `[[links]]` — and report that it
   needs a kit version shipping the tool.) Fix what it lists (a `status:` still holding a maturity
   value is renamed to `maturity:` — old vault in one pass:
   `grep -rln "^status: \(seed\|growing\|evergreen\)" <vault>`); hand the human only what needs a
   decision. What needs more than a fix:
   - **expired:** still true (push the date out, say why) or not (`status: deprecated`, or fix it) —
     never left expired.
   - **folder without `index.md`:** create one shaped like the root `index.md` (title · what lives
     here · `**Rules here:**`/`**NOT here:**` · `## Entry points` · trailing `<!-- generated: YYYY-MM-DD -->`)
     plus a two-line `CLAUDE.md` beside it: `<!-- Loaded automatically when Claude reads a file in this folder. -->`
     and `@index.md`. Report both.
   - **orphan cluster** (a folder of machine-written, link-less files: memory mirrors, app exports)
     → ONE generated map note linking every file, filed by actionability, linked from `Home.md`,
     regenerated every review. NEVER edit the foreign files; keep/delete/gitignore is the human's
     call.
   What the tool cannot see:
   - **signposts:** first fix the stale entry points you touched — a date quoted in an `index.md` is
     a second copy: correct it or drop the detail. Then add today's new ENTRY POINTS to each
     written-into folder's `index.md` as real relative paths, never `[[wikilinks]]`, under ~25
     lines, `<!-- generated: -->` = today. Routine notes stay out of the index but must be reachable
     by a `[[link]]`.
   - **decay:** projects whose log has not moved in 30+ days (`find <vault>/10-projects -name '*.md' -mtime +30`,
     blind to files this review itself touched) → ONE collected question, "archive to `90-archive/`
     or still active?", never one per file. Archive beats delete for finished projects, delete beats
     archive for noise.
5. **Deepen 2–3 notes (this is where depth comes from):** oldest or most-used `maturity: seed`/`growing`
   knowledge notes, preferring frontier notes (many outgoing `[[links]]`, few or no inbound); grow
   them toward the note anatomy in the vault `CLAUDE.md` — missing `source:`, one concrete case or
   number, a limit or counter-position, the `[[links]]`. Research the researchable parts (rules of `brain-research`).
   **What only the human can supply** (their reasoning, example, number): park it as `open → ask: …`,
   add it to Home's `block:open-questions`, LEAVE `maturity:` untouched. Never invent a case, a
   number or an opinion; bump `maturity:` only once the anatomy is met.
6. **Open loops and connections:** list 3–5 stalled things (projects without recent notes, `open → ask`
   markers), ask about them, offer to research the researchable ones (`brain-research`). Then name
   1–3 non-obvious connections between this week's notes and older ones; add the `[[link]]` only
   where it changes how a note reads.
7. **Refresh `Home.md`** — all four blocks, without dropping what is in them. **Address each block
   by its HTML marker, never by heading text** (`<!-- block:right-now -->` … `<!-- /block:right-now -->`,
   same for `next-deadlines`, `open-questions`, `new-this-week`); rewrite only what sits BETWEEN a
   marker pair, never a line carrying `<!-- keep:… -->`.
   **`right-now`:** active projects with a one-line status each, AND the `Areas:` line linking every
   note in `20-areas/`, rebuilt from the folder listing every single time · **`next-deadlines`:**
   next 3 dates from `Deadlines.md` · **`open-questions`:** this review's open loops and parked
   questions · **`new-this-week`:** the 3–5 newest or most-grown notes.
8. **The yield — the review ends with output, not with a filing report.** In order:
   - **What can the brain do now that it could not last week?** Name it out of what you filed today
     — a question it can now answer, a draft it now has the material for — with the notes that carry
     it. Nothing usable this week: say so, never manufacture a win.
   - **Ask "what are you working on next?"** For their answer run `python3 <vault>/.tools/search.py <topic>`
     and lay out what is already there — notes, the decisions that bind it, dates — and the gaps to
     fill first (offer `brain-research` for them).
   - **Offer the artifact** that material now supports (summary, draft, plan, checklist, study
     sheet) and BUILD it on their go: file it with its project, link it from the project note, add
     it to that folder's `index.md` entry points, and record it under its project in Home's `block:right-now`.
9. **Commit and report:** `cd <vault> && git add -A && git commit -m "review YYYY-MM-DD"`, then
   report what was filed where, what was deleted, what needs their input, which "not every week"
   items ran, and what the brain produces next — every filing decision visible, all reversible via
   Git.

## Not every week
Trigger-based, not scheduled; say in the report which ones ran.
- **Structure check** (quarterly-ish, or when the sweep keeps producing material no folder fits):
  propose renaming or archiving an area/folder that no longer matches the person's life.
- **Maps of content** (past ~150 notes — `python3 <vault>/.tools/search.py --stats`): propose one
  map per strand, 2–3 sentences of framing each, never a bare list of links.
- **Random revisit** (whenever the review ran short): open ONE random older note. Stale? Missing an
  obvious link? A near-twin to merge? One concrete improvement.

## Work mode (only when the vault `CLAUDE.md` names the mode `professional`)
- **Nothing stays `ownership: mixed`** — split or reclassify every mixed note from this week now.
- **The show-them test** on every person note you touched: could it be shown to that person? Role,
  work and agreements pass; character judgements and motive guesses do not — delete, don't rephrase.
- **Runbooks you actually ran this week** get a fresh `last_verified:`; anything past 12 months is
  flagged unverified, not quietly carried on.
- **Contribution log, five minutes:** what shipped, reviewed, designed, documented, who you helped,
  what you learned — every number with its source in the same line. An empty week is a valid entry;
  never invent impact.

## Company mode (only when the vault `CLAUDE.md` names the mode `company`)
- **`00-inbox/suggestions/` goes to zero too — step 1 for a second folder.** One exit each: (a) the
  person who may release it says yes → move it to its folder, `status: stable`, THEY fill `verified:`;
  (b) needs a decision they cannot make today → leave it, name it in the report with who decides;
  (c) wrong or already covered → delete it, say why. Nothing sits unanswered through two reviews.
- People become ROLES in `60-roles/` — never personal dossiers.
- A NEW note you write goes to `00-inbox/suggestions/`; a note already living in a folder is edited
  in place and drops to `status: draft`, never moved out. Either way the human sets
  `verified: {by: human:<name>, at: YYYY-MM-DD}`, never you.
- Never invent an owner, a number or a field value. Missing stays missing.

## Autonomous mode (only when run unattended by a scheduler)
Headless, no human in the loop: (1) delete nothing that isn't unambiguous junk — unsure → file it;
the step-1 empty-file rule still wins (empty = delete + report). (2) Never archive without asking —
list candidates as questions. (3) Route ALL questions to Home's `block:open-questions`, never to
chat, including step 2's "3 most important things" and step 8's "what are you working on next". (4)
Step 8 still runs: name what the brain can do now and list the artifact you would build, as an offer
instead of building it. (5) Finish with the Home refresh, `git commit`, and a short report to
`<vault>/.tools/logs/auto-review-YYYY-MM-DD.md` — one per run, outside the notes; keep the last ~12.
