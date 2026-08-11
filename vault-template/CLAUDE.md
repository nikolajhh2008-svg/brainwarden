# Brain — personal knowledge vault

One folder, two windows: an Obsidian vault AND a Claude Code working
directory on the same Markdown files. Structure: PARA-inspired
(deliberately flat) plus Zettelkasten principles for knowledge.

Kit version: 1.3.0 (brainwarden — updates read this line to know what
they're upgrading from, and set it to the new version afterwards)

**Vault language: {{LANGUAGE}}** — write all notes, titles and links in
this language (set during setup; the folder names stay English so the
skills keep working).

**Vault mode: {{MODE}}** — one of `personal`, `professional`, `company`
(set during setup). The mode decides which folders exist; `index.md` in
this folder is the map of THIS vault.

## Navigation — read the signpost before you write
Every folder carries an `index.md`: what belongs there, what does NOT,
and the entry points. It is the canonical signpost for ANY agent (the
tiny `CLAUDE.md` next to it only pulls the same file into Claude's
context automatically).
- Landed in a folder via search or glob? Read its `index.md` FIRST.
- Created a note that others should start from? Add it to that
  `index.md` under "Entry points" and bump its `generated:` marker.
- Links inside an `index.md` are **real relative paths**, never
  `[[wikilinks]]` — a wikilink carries no path and an agent cannot
  resolve it. In normal notes `[[wikilinks]]` stay the rule (Obsidian).
- An `index.md` never lists every file — only the ways in.

## Folder map (flat on purpose — folder depth is not a feature)
| Folder | Contains | Rule of thumb |
|---|---|---|
| `00-inbox/` | Raw captures, one file per thought | zero after each review |
| `10-projects/` | Endeavors WITH an end date (deadline, launch, trip) | "What am I working on?" |
| `20-areas/` | Life areas WITHOUT an end (created during setup) | "What am I responsible for long-term?" |
| `30-knowledge/` | Evergreen notes, sources, `people/` | "What do I want to keep?" |
| `40-decisions/` | Decision records (`YYYY-MM-DD-slug.md`) | append-only |
| `50–80` | **Reserved for YOUR modules** (journal, media log, health, money …) | added on demand |
| `90-archive/` | Finished items from 10/20 | cold storage |

**Mode differences (the mode line above says which one applies):**
`professional` adds `50-processes/` (your own runbooks — "how I do this",
not the company's official process) and `60-contribution/` (what you did,
with evidence). `company` adds
`50-processes/`, `60-roles/`, `70-onboarding/`, `80-partners/` and
`00-inbox/suggestions/`, and drops `10-projects/`, `20-areas/` and
`30-knowledge/people/` — roles instead of dossiers about people. Each of
those folders explains its own extra rules in its `index.md`.

**Why the number gaps?** They are deliberate expansion space: new
top-level modules slot in as `50-journal/`, `60-media/` etc. without ever
re-sorting the core. Ask Claude to add a module and it lands in a gap —
the core six folders and their English names stay fixed (the skills
depend on them). Which gaps are still free depends on the mode: in
`personal` all of 50–80; in `professional` everything except 50 and 60
(`50-processes/` and `60-contribution/` sit there); in `company` none — 50–80 are all taken,
so user modules are not offered there.

**Core sorting principle:** file by ACTIONABILITY (which project/area
needs this NOW?), never by topic taxonomy. Findability comes from
`[[links]]`, tags and search — not from folder depth.

## Note schema (machine-readable)
Required on every note OUTSIDE the inbox:
```yaml
---
type: knowledge | source | decision | project | area | person
      | meeting | contribution | sop | role | partner
title: <human readable>
created: YYYY-MM-DD
tags: [kebab-case, lowercase, few]
---
```
Optional — add a field the moment it applies, never "just because":
```yaml
maturity: seed | growing | evergreen   # knowledge notes: how worked out is it?
status: draft | stable | deprecated    # does it still hold? (required from professional up)
source: <URL/book/person>              # one external source
sources: [{resource: <uri>, title: <str>}]      # several sources
stale_after: YYYY-MM-DD                 # from this date on, distrust it
ownership: private | company | mixed    # who it belongs to (work brains: required)
confidentiality: public | internal | strict
ai_release: local | external_ok         # may this leave the machine?
last_verified: YYYY-MM-DD               # runbooks: when you last actually ran it
handover_relevant: true                 # would a stand-in need this? (work brains)
verified: {by: human:<name>, at: YYYY-MM-DD}     # a human confirmed it
generated: {by: <agent>/<model>, at: YYYY-MM-DD} # an AI produced it
```

**`maturity` vs `status` — two different questions.** `maturity` (knowledge
notes) asks how worked out a note is: `seed` = a thin first capture ·
`growing` = own words + a source · `evergreen` = meets the note anatomy
below. `status` asks whether the content still holds: `draft` ·
`stable` · `deprecated`. A note can be `evergreen` and `deprecated` at
once — beautifully worked out, and no longer true. `maturity` marks
maturity, NOT importance: it keeps thinness HONEST and hands the weekly
review its deepening candidates, it is never a reason to reject or
delete a thin note.

**`verified` vs `generated` — the most important distinction in this
vault.** `verified` means a human being read this and said "yes, that is
right". `generated` means a machine wrote it and nobody has checked it
yet. Rule for Claude: never set `verified` yourself — that field belongs
to the human. `generated:` marks notes whose CONTENT you produced —
researched facts, a summary you wrote, a draft procedure. Filing what the
human said, in their words, is not authorship: a capture you paraphrase
into a note does NOT get `generated:`, or the marker would sit on
everything and mean nothing. Old field name: what used to be
`status: seed|growing|evergreen` is now `maturity:` — if you meet the
old spelling in a note, rename it.

**`ownership:` — the field a work brain cannot do without.** In
`professional` mode every note carries `ownership: private | company |
mixed` plus `confidentiality:`. This is not bureaucracy, it is the only
thing that makes the vault separable later. In Germany and Austria an
employee must hand over everything obtained from the employment when they
leave — and courts have held that this includes **notes the employee wrote
themselves** about customer conversations and project work, with only
genuinely private records exempt, and that copies must be deleted too
(§ 667 BGB analog; BAG 14.12.2011 – 10 AZR 283/10). Draw that line on the
day a note is written and leaving takes minutes. Draw it on the last day
and it cannot be drawn at all.

A third field follows from it: `ai_release: local | external_ok`. Be precise
about what it can and cannot do, because it is easy to believe more of it
than is true: **by the time an agent reads this line, the note is already in
its context.** The field cannot stop that and does not pretend to.

What it governs is the step AFTER reading: whether this content may leave
the conversation. `local` means it must not end up in a summary sent
outside, an email draft, a ticket, a support request, a web search query or
a file put somewhere shared — the places where company AI policies
typically draw the line (contracts, customer data, financial figures,
source code). An agent honours it by keeping such a note out of anything it
produces for the outside, and by saying so instead of quietly complying.

If content genuinely must never reach a model at all, no field achieves
that. That is what a second, separate vault is for — the same answer as for
`confidentiality:`. Rule for the weekly review: **nothing stays `mixed` for more than a
week** — split it or reclassify it.

**Notes about colleagues are facts only.** Role, responsibility, how to
reach them, what they are working on, what was agreed. Never character
judgements, performance assessments or guesses about motives. The test
before writing a line: *could I show this to that person if they asked?*
They can: informal management notes about a named person's conduct or
performance fall under a subject access request, and the GDPR's household
exemption does not cover notes with a professional purpose (Art. 2(2)(c),
recital 18; CJEU Lindqvist C-101/01, Ryneš C-212/13).

**Superseding — write it on BOTH files, as plain text.** When a note
replaces another, an agent that searches its way into the OLD file must
find the pointer there, otherwise two plausible versions compete. New
file gets a `## Status` section with
`Supersedes [40-decisions/2026-05-10-old.md](40-decisions/2026-05-10-old.md)`,
old file: its `## Status` body is REPLACED by
  `Superseded by [<path>](<path>)` (append the section if it has none), and
  its frontmatter gets `status: deprecated`. Never leave an "in force" line
  standing above a supersede notice — an agent greps the first `## Status`
  and believes it. Nothing else in the old record changes; this one section
  is the only exception to append-only. **Both keywords
stay English even in a translated vault** — like the frontmatter values, and
for a hard reason: `ersetzt` is an ordinary German verb, so a tool matching
the translated word would flag normal prose as a broken chain — real relative
paths, rest of the old file untouched.

- Inbox captures need NO frontmatter (zero friction) — added at review time.
- File names: descriptive, kebab-case; date-prefixed only for episodic notes.

## Thinking rules
- **Atomic:** one idea per note; one person = one note (`30-knowledge/people/`).
- **Own words:** processing means paraphrasing — copying is collecting,
  not understanding.
- **Processing duty:** the inbox goes to ZERO at every weekly review —
  file it or delete it, never "later".
- **Success metric is output** (texts, decisions, plans) — never note count.
- **Link rule:** add `[[links]]` only when note A truly changes how you
  read note B.
- Maps of content only after ~150 notes; no new top-level folders without
  a deliberate decision.

## Note anatomy (target depth per type — "atomic" means ONE idea, not few words)
- **Knowledge note** (`30-knowledge/`, target `evergreen`): the idea in
  your own words → the evidence (`source:` + where in it) → one concrete
  case, number or example → a limit or counter-position where one exists →
  the `[[links]]`. Aim ~100–400 words. `seed` is allowed — `maturity`
  just keeps the thinness honest and flags it for a later review.
  `maturity: evergreen` is only earned once all of this is actually there.
- **Person note** (`30-knowledge/people/`, `personal`/`professional` only):
  a dossier, not an index card — role/relationship, verified facts,
  recent interactions, open questions.
- **Project note** (`10-projects/`): state + the next physical action + a
  short running log; grows by at least a line every time it comes up.
- **Area note** (`20-areas/`): the standard you hold + current state + what
  you're watching.
- **Decision** (`40-decisions/`): deliberately terse and append-only —
  brevity is correct here.
- **MOC** (only past ~150 notes): a map with 2–3 sentences of framing per
  strand, never a bare list of links.
- **SOP / role / partner note** (company + professional modes): shape and
  required fields live in the `index.md` of `50-processes/`, `60-roles/`
  and `80-partners/`.
- **Principle:** depth comes from revision rounds (the review), not the
  first draft — captures may be thin, `maturity` keeps that honest.

## The red line — Claude gardens, it does not author
The notes are the human's thinking in the human's words. Claude tends the
garden; it never replaces the plants.
- Add researched facts only WITH a source and only marked as research
  (`source:` or an inline "(researched YYYY-MM-DD)").
- Never rewrite or "improve" the human's own opinions, reflections or
  phrasing — ask a question and work their answer in; don't overwrite
  their voice.
- Suggest interpretive summaries and links; don't silently manufacture
  them. A vault full of AI paste becomes an attic — a vault in their
  words stays theirs.

## Instructions for Claude
- Retrieval: ALWAYS run `python3 .tools/search.py <terms>` from the
  vault root (this folder) first — saves context; then read only the
  hits, never the whole vault. (`--stats` prints the vault's honest
  numbers: note counts, maturity distribution, review history.)
- `Home.md` is the living dashboard for the HUMAN — the review refreshes
  all four blocks; deadline captures update "Next deadlines" right away.
  Address the blocks by their `<!-- block:… -->` markers, never by the
  heading text (headings get translated, markers do not), and replace
  only what sits between a marker pair. `index.md` is the equivalent for
  agents — Home is prose, `index.md` is paths.
- Incoming sources: files in `00-inbox/raw/` → skill `brain-ingest`.
- Template per note type: knowledge → `_templates/knowledge-note.md` ·
  source → `source-note.md` · person → `person-note.md` · project →
  `project-note.md` · area → `area-note.md` · journal → `journal-entry.md`
  · SOP → `sop-note.md` · meeting → `meeting-note.md` · learning →
  `learning-note.md` · contribution → `contribution-entry.md` · role →
  `role-note.md` · partner → `partner-note.md` (each only exists in the
  modes that have the matching folder) · decision →
  `40-decisions/_template.md`.
  **Where meeting and learning notes go:** a meeting note is filed with
  what it is ABOUT — the project in `10-projects/`, or `40-decisions/` if
  its only lasting content is one decision (then keep it terse and drop
  the raw notes). A learning note goes to `30-knowledge/`. Neither gets
  its own folder: one meeting is an event, not a category. When instantiating, fill the
  DATE/NAME placeholders with real values; the template files themselves
  keep their placeholder tokens forever (their prose may be translated —
  the tokens stay).
  Never rewrite a decision record — append.
- Inside `30-knowledge/` at most ONE level of subfolders (like `people/`);
  everywhere else, no new subfolder without a reason.
- Before creating a people/knowledge note, search first — extend instead
  of duplicating.
- Review hygiene: `python3 .tools/hygiene.py` reports orphan notes, dead
  links, empty files and notes missing from their folder's `index.md`.
- Cold start from past sessions: `python3 .tools/harvest.py` (inventory
  only) and `--candidates` (deterministic pre-filter). It never writes and
  never calls a model — see Step 8a of the setup runbook for the procedure
  and the consent rules.
- Finished project / ended area → move to `90-archive/`, and remove it
  from the source folder's `index.md` entry points.
- The structure may EVOLVE: if reviews show a folder or area no longer
  fits the person's life, propose the change — the onboarding interview was a
  starting point, not a life sentence.

## Sync
- Versioning: local Git. Do NOT put the vault in iCloud/Dropbox sync
  folders (corruption risk with Git). Phone: Obsidian Sync.

## Commands
- **brain-capture** — frictionless thought → inbox (from any session)
- **brain-ingest** — source from raw/ → triaged notes (light for
  reference material, atomic for build material)
- **brain-ask** — answer questions from the vault, with cited notes
- **brain-review** — weekly: inbox to zero, contradiction check,
  connections, hygiene, refresh Home, git commit
- **brain-research** — fill open questions and thin notes with verified,
  sourced facts
