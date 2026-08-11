# Changelog

## [1.3.0] — 2026-08-11

One kit, three kinds of brain, and a vault an AI agent can navigate
without guessing. Existing vaults are updated in place: the update path
replaces kit infrastructure and renames one frontmatter key, never a
line of your note content.

### A cold start from what the machine already recorded

- **`.tools/harvest.py`** turns past Claude Code sessions into vault
  material. It inventories without reading anything, then pre-filters
  deterministically — no model call, no cost: harness injections, system
  plumbing, acknowledgements, duplicates and anything without a
  decision/date/milestone/lesson word. Measured on a real machine: 1500
  human turns in, 34 candidates out. Step 8a of the setup runbook is the
  procedure around it: nothing is read without a yes, nothing written
  without a second one, a sample of twenty is judged before the archive,
  every harvested note carries its origin, at most three per session.
  The reason it is that strict: an audit of 10,134 auto-captured memories
  in another system found 97.8% of them worthless.

### Two things change in existing vaults

- **`status:` no longer means maturity — that field is now `maturity:`.**
  Two different questions were sharing one key: how worked out is this
  note, and does it still hold? A note can be beautifully written and no
  longer true, and the old schema had no way to say so. From now on
  `maturity: seed | growing | evergreen` on knowledge notes, and
  `status: draft | stable | deprecated` wherever validity matters
  (required from a work brain upwards). **The update path in
  SETUP-FOR-CLAUDE.md migrates existing vaults:** it shows you the hits
  first, renames only the key, never a value or a line of text, and
  commits that rename on its own so it can be reverted alone. Leftovers
  are caught later too — `brain-review` renames what it meets,
  `hygiene.py` and `search.py --stats` report what is left.
- **Every folder that holds notes now carries two navigation files.**
  Older vaults have none; the update path copies the pair
  into each folder and rewrites the entry points from what is actually
  in it, leaving any `index.md` you wrote yourself in place.

### The vault is now built for agents first

- **A signpost in every folder.** `index.md` states what belongs there,
  what does not, and the two or three notes worth starting from, in
  about 25 lines. Next to it, a three-line `CLAUDE.md` pulls that
  signpost into Claude's context the moment a file in that folder is
  read, so it costs nothing until it is needed. `index.md` is the
  canonical half, because any tool can read a plain file.
- **A root `index.md`** is the cold entry point for a session that has
  never seen the vault: mode, note language, one line per folder, the
  search command, and the pointers to `Home.md` (yours) and `CLAUDE.md`
  (the rules).
- **Links inside a signpost are real relative paths, never
  `[[wikilinks]]`** — a wikilink carries no path, so an agent reading
  the raw file cannot resolve it. Inside notes, wikilinks stay the rule.
- **Who stands behind a note is a field now.** `verified: {by: human:…,
  at: …}` means a person confirmed the content, `generated: {by: …,
  at: …}` means a machine drafted it. Claude never sets `verified:` on
  its own work. `Deadlines.md` makes the same distinction for dates:
  confirmed ones under "Hard (verified)", the rest until checked.
- **A replacement is recorded on both files.** The new note gets
  `Supersedes <path>`, the outdated one gets `Superseded by <path>`
  appended as plain text. An agent that lands in the old version through
  a search now finds the pointer instead of believing what it reads.

### Three kinds of brain

- **The setup opens with one question:** for me · for my work · both,
  kept separate · for a company. It decides which folders exist, which
  questions follow and what the first win is. Unclear answers default to
  a private brain, and the choice is recorded in the vault so every
  later session reads it instead of guessing.
- **Work brain:** everything a private one has, minus the private half,
  plus `50-processes/` for the workflows you repeat. The first win
  includes the first workflow written down.
- **Company vault:** shared knowledge for several people, with
  `50-processes/`, `60-roles/`, `70-onboarding/`, `80-partners/` and an
  `00-inbox/suggestions/` drop zone for colleagues without release
  rights. No projects, no areas, and **roles instead of dossiers on
  people**, which is a data-protection decision, not a style one.
  Company notes additionally carry `owner:`, `audience:`,
  `confidentiality:` and `review_due:`. `confidentiality:` is a label
  and not access control, and the setup says so out loud.
- **Two brains side by side:** the second one gets its own Claude Code
  configuration directory and a one-word start command (`workbrain`,
  or `teambrain` for a company), so work rules, skills and sessions
  never load in a private session.
- **Company mode states two things out loud** during setup, as pointers
  rather than legal advice: this kit keeps no usage or search log of any
  kind, and people working with an AI system must be able to tell that
  they are.

### New tool: `.tools/hygiene.py`

The weekly review's hygiene step used to ask for a vault-wide link-graph
judgement with no instrument for it. It now measures instead: orphans,
dead links, near-empty notes, notes no signpost points to, folders that
lost their `index.md`, frontmatter gaps and one-sided supersede chains.
Read-only, standard library only, and it masks code blocks first so a
rules file's `[[example]]` is never reported as a dead link.

### Search

- **German compounds are found.** Hits inside a word now count, so
  `Vertrag` finds `Rahmenvertrag` and `Kosten` finds
  `Mehrkostenforderungen`. They score lower than a hit at a word start
  and are capped per term, so short common words cannot flood the
  results; terms under four characters still match at word starts only.
- **`--stats` tells the truth again:** it reads `maturity:`, flags notes
  still using `status:` for it, and no longer counts kit files such as
  `CLAUDE.md` and the templates as if they were your notes.

### Also

- **`Home.md` survives translation.** Its four dashboard blocks are
  delimited by `<!-- block:… -->` markers, and the skills address those
  markers rather than the headings, so a German vault gets German
  headings instead of a half-English dashboard.
- **Interview goes deeper where it counts:** new adaptive block 4
  ("Zoom in: your work or your studies") — narrow down first
  (studying / working / both), then follow the fitting branch into
  concrete tasks, recurring work, time sinks and tools. Recurring
  tasks land as area notes: the raw material for everything an
  assistant can later take off your plate. The interview also picks its
  track from the mode, and never runs a personal deep interview on a
  shared company vault.
- **Deadlines.md states its format:** one line per deadline, date
  first (`2026-08-15` or `15.08.2026`) — readable for humans and
  parseable for tools that treat the file as the deadline source.
- **New note types with templates and worked examples:** SOP, role,
  partner and onboarding plan, plus `examples/EXAMPLE-sop.md` and
  `examples/EXAMPLE-role.md` showing the bar.

## [1.2.0] — 2026-07-10

For everyone: works with the vault you already have, wherever it lives.

- **The vault path is no longer hardcoded.** Setup records your real
  vault location in a `Brain vault:` line in the global rules, and all
  five skills follow it — an adopted vault stays exactly where it is
  (iCloud folder, different name, anything). `~/Brain` is just the
  default for fresh installs. The plugin install now genuinely works
  for people who already have a vault.
- **Non-English setups fixed end-to-end** (found by a fresh from-zero
  test): the "leave templates untouched" rule no longer contradicts the
  translate instruction (tokens stay, prose translates), and the raw
  zone's README joined the translate list.
- **Search stops indexing templates** — no more placeholder noise in
  results — and the decision template uses one date format throughout.
- **Windows made calmer:** the tutorial's stage 1 is jargon-free (one
  install, one sentence), details moved to the Windows section in
  TROUBLESHOOTING; the skills name the `py -3` fallback.

## [1.1.0] — 2026-07-10

Depth release: notes now grow over time instead of staying thin — plus
platform hardening from real end-to-end tests.

- **Maturity status for knowledge notes:** `status: seed | growing |
  evergreen` in the note schema — thinness stays honest, and the review
  gets its deepening queue
- **The review compounds depth:** two new steps — deepen 2–3 seed notes
  toward the anatomy each week, and a random revisit that keeps old
  corners alive; plus explicit autonomous-mode rules for scheduled runs
- **Note anatomy per type** documented in the vault CLAUDE.md (a
  knowledge note wants evidence, one concrete case and a
  counter-position — "atomic" means one idea, not few words)
- **"The red line"** — the AI-gardens-it-does-not-author doctrine is now
  an operational rule Claude loads every session, not just philosophy
- **Optional unattended weekly review** documented (Claude Desktop
  Routines or a scheduler job) with an honest subscription-cost warning
- **Windows hardening:** Git-for-Windows guidance up front, `py -3`
  fallback for the search tool, a Windows quirks section in
  TROUBLESHOOTING; **mobile capture** gets an honest FAQ (Sync vs.
  shortcut vs. notes-app — and what we don't promise)
- **Safety fixes from adopt/update end-to-end tests** (also shipped as a
  hotfix to 1.0.0): adopting an existing vault can no longer overwrite
  the user's files, no duplicate first-win projects, migration backlog
  lands on Home, updates refresh the whole vault CLAUDE.md, and the
  vault ships its own `.gitignore`

## [1.0.0] — 2026-07-09

Initial public release.

- **Setup built around the first win:** three questions, then Claude
  builds your real first notes itself — areas, first project, deadlines
  and a populated `Home` dashboard, minutes in. The deep onboarding
  interview comes after that, and only if you want it.
- **`Home.md`** — a living dashboard Claude keeps current: active
  projects, next deadlines, open questions, new this week
- Vault template: PARA-inspired structure (`00-inbox` / `10-projects` /
  `20-areas` / `30-knowledge` / `40-decisions` / `90-archive`) with
  deliberate numbering gaps for optional modules (journal, media,
  health, money, or your own)
- Five Claude Code skills: `brain-capture`, `brain-ingest` (with
  reference-vs-build triage), `brain-ask` (cited answers from your own
  notes), `brain-review` (weekly sweep, contradiction check against past
  decisions, connection surfacing), `brain-research` (sourced enrichment)
- Guided setup: TUTORIAL.md for humans, SETUP-FOR-CLAUDE.md as the
  AI-driven installer; global rules make the brain ambient in every
  Claude session; existing vaults are adopted (or quarantined into
  `OLD_VAULT/`), never overwritten
- Local search tool (`.tools/search.py`), a named template for every
  note type, examples, troubleshooting/FAQ, MIT license
