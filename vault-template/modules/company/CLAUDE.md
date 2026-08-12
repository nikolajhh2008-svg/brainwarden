# Brain — shared company knowledge vault

One folder, two windows: an Obsidian vault AND a Claude Code working
directory on the same Markdown files. Several people read it, few people
release into it.

Kit version: 1.3.0 (brainwarden — updates read this line to know what
they're upgrading from, and set it to the new version afterwards)

**Vault language: {{LANGUAGE}}** — write all notes, titles and links in
this language (set during setup). Folder names and kit page names may be
translated with everything else: the tools find the inbox, the decisions
folder and the archive by their NUMBER (`00-`, `40-`, `90-`) and a kit page
by its `<!-- kit-page -->` marker, never by an English word. Only
`CLAUDE.md`, `index.md` and `Home.md` keep their names — those three are
loaded by name.

**Vault mode: company** — this is a SHARED vault. It holds how the
company works, not what one person is up to. There are no projects, no
areas, and no dossiers on colleagues; `index.md` in this folder is the
map of THIS vault.

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

## Folder map
| Folder | Contains | Rule of thumb |
|---|---|---|
| `00-inbox/` | Raw captures, one file per thought | zero after each review |
| `00-inbox/suggestions/` | Contributions that are NOT company truth yet | released, or dropped |
| `30-knowledge/` | Shared knowledge: terms, facts, how-things-work | "what should everyone be able to look up?" |
| `40-decisions/` | Decision records (`YYYY-MM-DD-slug.md`) | append-only |
| `50-processes/` | Procedures: how we actually do things (SOPs) | "how is this done here?" |
| `60-roles/` | Role descriptions — tasks, responsibility, cover | roles, never people |
| `70-onboarding/` | First hour / first week / first 30 days | "what does a new person need?" |
| `80-partners/` | Suppliers, service providers, contacts | organisations, not persons |
| `90-archive/` | Retired items, kept for the record | cold storage |

**No `10-projects/`, no `20-areas/`, no `30-knowledge/people/`** — and no
free number gaps: 50–80 are all taken, so this vault has no user modules.
A person's own projects belong in their own private vault.

**Core sorting principle:** file by the QUESTION it answers, not by who
wrote it. Findability comes from `index.md`, `[[links]]`, tags and
search — not from folder depth.

## Note schema (machine-readable)
Required on every note OUTSIDE the inbox:
```yaml
---
type: knowledge | source | decision | sop | role | partner
title: <human readable>
created: YYYY-MM-DD
tags: [kebab-case, lowercase, few]
owner: <role that answers for this content>
status: draft | stable | deprecated
audience: [<role>, <role>]        # or [all]
confidentiality: internal | restricted
review_due: YYYY-MM-DD
---
```
Optional — add a field the moment it applies, never "just because":
```yaml
maturity: seed | growing | evergreen   # knowledge notes: how worked out is it?
source: <URL/book/person>              # one external source
sources: [{resource: <uri>, title: <str>}]      # several sources
stale_after: YYYY-MM-DD                 # from this date on, distrust it
verified: {by: human:<name>, at: YYYY-MM-DD}     # a human confirmed it
generated: {by: <agent>/<model>, at: YYYY-MM-DD} # an AI produced it
version: <n>                            # SOPs: counts up on every release
valid_from: YYYY-MM-DD                  # SOPs: since when this version applies
```

**`verified` vs `generated` — the most important distinction in this
vault.** `verified` means a human being read this and said "yes, that is
right". `generated` means a machine wrote it and nobody has checked it
yet. **Content is company truth only when `status: stable` AND `verified:`
is filled.** Everything else is a proposal, no matter how confident it
reads. Rule for Claude: never set `verified:` yourself — that field
belongs to the person who is allowed to release; anything you write
carries `generated:` and stays `draft` until a human replaces it.

**The two scales above are this vault's authority.** `hygiene.py`,
`search.py --stats` and `progress.py` read the `maturity:` and `status:`
lines out of THIS file and compare notes against what they find here. So the
words may be translated (`status: entwurf | gültig | überholt`) — but then
they must be translated HERE too, and each scale must keep its order:
`maturity` runs unfinished → worked out, `status` runs draft → released →
retired. Translate the values in the notes and not in this file and every
one of those checks quietly stops matching, which reads exactly like a vault
with nothing wrong.

**`maturity` vs `status` — two different questions.** `maturity`
(knowledge notes) asks how worked out a note is: `seed` · `growing` ·
`evergreen`. `status` asks whether the content still holds: `draft` ·
`stable` · `deprecated`. A note can be `evergreen` and `deprecated` at
once — beautifully worked out, and no longer true. Old field name: what
used to be `status: seed|growing|evergreen` is now `maturity:` — if you
meet the old spelling, rename it.

**`confidentiality:` is a LABEL, not access control.** Everyone who can
open this folder can read every file in it. Real separation only comes
from a second, separate vault with its own access rights. Never tell
anyone a note is protected because of this field.

**Superseding — write it on BOTH files, as plain text.** When a note
replaces another, an agent that searches its way into the OLD file must
find the pointer there, otherwise two plausible versions compete. New
file gets a `## Status` section with
`Supersedes [40-decisions/2026-05-10-old.md](40-decisions/2026-05-10-old.md)`,
old file: its `## Status` body is REPLACED by
`Superseded by [<path>](<path>)` (append the section if it has none), and its
frontmatter gets `status: deprecated`. Never leave an "in force" line standing
above a supersede notice. Real relative paths, rest of the file untouched.

- Inbox captures need NO frontmatter (zero friction) — added at review time.
- File names: descriptive, kebab-case; date-prefixed only for episodic notes.

## Thinking rules
- **Atomic:** one idea per note; one role = one note (`60-roles/`).
- **Own words:** processing means paraphrasing — copying is collecting,
  not understanding.
- **Processing duty:** the inbox goes to ZERO at every weekly review —
  file it or delete it, never "later".
- **Success metric is output:** fewer questions asked twice, faster
  onboarding, procedures someone can actually follow. Never note count.
- **Link rule:** add `[[links]]` only when note A truly changes how you
  read note B.
- **Never invent a figure, a condition, a price or a deadline.** An
  honest gap ("open → ask the owner") is useful; a plausible invention is
  dangerous, because somebody will act on it. If it is not in a note and
  not in a source, the answer is "I don't know, ask <owner>".
- Maps of content only after ~150 notes; no new top-level folders without
  a deliberate decision.

## Note anatomy (target depth per type)
- **Procedure / SOP** (`50-processes/`): purpose in one sentence → scope
  (who and when) → roles involved → the steps, numbered, each a single
  action → exceptions and what to do when they hit → revision history.
  Written so a stand-in can follow it without asking.
- **Role note** (`60-roles/`): tasks, what this role decides alone, what
  it must escalate, who covers when it is away, what knowledge it needs.
  Describes the ROLE. If the holder changes, the note stays.
- **Partner note** (`80-partners/`): what they deliver, how to reach them,
  where the terms are filed, experience worth knowing. No judgements
  about named individuals.
- **Knowledge note** (`30-knowledge/`, target `evergreen`): the idea in
  your own words → the evidence (`source:` + where in it) → one concrete
  case, number or example → a limit or counter-position where one exists
  → the `[[links]]`. Aim ~100–400 words.
- **Decision** (`40-decisions/`): deliberately terse and append-only.
  Context → what was decided → why → what follows from it.
- **Onboarding** (`70-onboarding/`): a path, not a pile — first hour,
  first week, first 30 days, each step pointing at a real note.
- **Principle:** depth comes from revision rounds (the review), not the
  first draft.

## The red line — Claude drafts, humans release
- Add researched facts only WITH a source and only marked as research
  (`source:` or an inline "(researched YYYY-MM-DD)").
- Never rewrite a released note (`status: stable` + `verified:`) on your
  own. Propose the change in `00-inbox/suggestions/` and name what would
  change; the owner decides.
- Never write anything about a named employee beyond "currently holds
  role X" — no performance, conduct, health, salary. That is not
  squeamishness: personnel data in a shared vault is a legal problem.
- No usage tracking. Who searched for what, and when, is not recorded —
  in Austria and Germany that is regularly subject to works-council
  co-determination, and a vault that seems to tell on people does not get
  used.

## Instructions for Claude
- Retrieval: ALWAYS run `python3 .tools/search.py <terms>` from the
  vault root (this folder) first — saves context; then read only the
  hits, never the whole vault. (`--stats` prints the vault's honest
  numbers.)
- **Answer with the source.** Every statement cites the note it comes
  from, with its `status:`. If the only hit is `draft` or a suggestion,
  say so before answering. "I don't know" is a correct answer here.
- `Home.md` is the living dashboard for the HUMAN — address its blocks by
  their `<!-- block:… -->` markers, never by the heading text (headings
  get translated, markers do not), and replace only what sits between a
  marker pair. `index.md` is the equivalent for agents — Home is prose,
  `index.md` is paths.
- Incoming sources: files in `00-inbox/raw/` → skill `brain-ingest`.
- Template per note type: SOP → `_templates/sop-note.md` · role →
  `role-note.md` · partner → `partner-note.md` · knowledge →
  `knowledge-note.md` · source → `source-note.md` · onboarding →
  `onboarding-plan.md` · decision → `40-decisions/_template.md`. Fill the
  DATE/NAME placeholders with real values; the template files keep their
  tokens forever. Never rewrite a decision record — append.
- Inside `30-knowledge/` at most ONE level of subfolders; everywhere
  else, no new subfolder without a reason.
- Before creating a note, search first — extend instead of duplicating.
- Review hygiene: `python3 .tools/hygiene.py` reports orphan notes, dead
  links, empty files and notes missing from their folder's `index.md`.
- Retired procedure / former partner → move to `90-archive/`, and remove
  it from the source folder's `index.md` entry points.

## Sync
- Versioning: local Git. Sharing between people: a private Git remote
  everyone clones and pulls — not a cloud sync folder (corruption risk
  with Git, and no review step before content becomes truth).

## Commands
- **brain-capture** — frictionless thought → inbox (from any session)
- **brain-ingest** — source from raw/ → triaged notes
- **brain-ask** — answer questions from the vault, with cited notes
- **brain-review** — weekly: inbox to zero, contradiction check,
  connections, hygiene, refresh Home, git commit
- **brain-research** — fill open questions and thin notes with verified,
  sourced facts
