# modules/ — mode overlays (kit only, NEVER part of a vault)

The vault template has ONE core. Everything a `professional` or
`company` vault needs on top lives here as an **overlay**: a folder tree
shaped exactly like a vault root, so applying it is a plain copy — no
guessing which file goes where.

```
modules/
├── processes/   → professional AND company   (50-processes/ + the SOP template)
└── company/     → company only               (60/70/80, suggestions/, overrides)
```

This `README.md` is the only file here that must never reach a vault —
it sits one level above the overlays, so copying `modules/<name>/.`
cannot pick it up.

## Applying an overlay (for SETUP-FOR-CLAUDE.md)

```
python3 assemble.py ~/Brain <personal|professional|company>
```

`assemble.py` (kit root) does the whole sequence: core, then the overlays
the mode needs, leaving `modules/` behind, then removing the files a
shared vault must not carry. It never overwrites and lists what it left
alone. Keep the overlay folders shaped like a vault root — that is what
makes applying them a plain copy, and the script relies on it. The list
of files the company mode drops lives in `COMPANY_DROPS` at the top of
that script; when an overlay gains a file that a shared vault must not
have, that list is the one place to change.


Order matters, and the script applies it: the company overlay deliberately OVERWRITES thirteen core files. Nine of
them talk about folders which do not exist in a company vault — six
`index.md` (root, `00-inbox/`, `30-knowledge/`, `40-decisions/`,
`90-archive/`, `_templates/`) plus `Home.md` (the core one links
`[[About me]]`, which company mode deletes), `Deadlines.md` and
`CLAUDE.md`. The other four are **note templates whose frontmatter is
the wrong schema for a shared vault**: `_templates/knowledge-note.md`,
`_templates/source-note.md`, `_templates/sop-note.md` and
`40-decisions/_template.md`. The core versions carry `ownership: private`
— a field the company schema does not define, whose value says the
opposite of what a shared vault is — and none of them carries the four
fields this mode requires on every note (`owner`, `audience`,
`confidentiality`, `review_due`). Left in place, a note copied straight
from the template lands in the vault and `hygiene.py` reports it under
**frontmatter gaps**, which the setup's own Step-9 checklist demands be
zero. Neither `hygiene.py` nor `progress.py` scans `_templates/`, so
nothing in the kit would ever have pointed at the cause.

That is all intended: every link in a signpost has to be a path that
really exists and every template has to produce a note this mode
accepts, otherwise the whole system lies. Use plain
`cp -R` for the overlay even on the adopt path (these are kit
infrastructure, not the human's content); the only content file in the
overlay is `About this vault.md`, so on an adopt run copy that one with
`cp -n` afterwards if it already exists.

The company `Home.md` keeps the SAME four block markers as the core one
(`block:right-now`, `block:next-deadlines`, `block:open-questions`,
`block:new-this-week`) — the skills address those markers, so they must
never be renamed per mode.

`person-note.md` is deleted on purpose, not just left unlisted: a
template for dossiers about people is a trap in a vault whose rule is
"roles, not people".

Overlays only ship a folder's `CLAUDE.md` when they CREATE that folder —
where they merely override an `index.md`, the identical two-line
`CLAUDE.md` is already there from step 1.

`personal` gets no overlay at all.

## What each overlay adds

| Overlay | Adds |
|---|---|
| `processes/` | `50-processes/` and `60-contribution/` (each index + CLAUDE.md), `handover.md`, `_templates/sop-note.md` + `meeting-note.md` + `contribution-entry.md` + `learning-note.md`, and two overriding files: `_templates/index.md` (lists the SOP template) and the root `index.md` (without it the folder that defines this mode is missing from the cold-entry signpost) |
| `company/` | `60-roles/`, `70-onboarding/` (incl. `onboarding-path.md`), `80-partners/`, `00-inbox/suggestions/`, `About this vault.md`, `THIS-COPY.md` (a distributed copy ages silently — this file carries its date), `.tools/progress.py` (how much of the vault is verified, not just how much text exists), `_templates/role-note.md` + `partner-note.md` + `onboarding-plan.md`, and thirteen overriding files: six `index.md` (root, `00-inbox`, `30-knowledge`, `40-decisions`, `90-archive`, `_templates`), `Home.md`, `Deadlines.md` (the core one lacks this mode's required fields), **`CLAUDE.md`** — the binding rules file; the core one describes projects, areas and person notes, none of which exist here, and leaving it in place is the one override whose absence makes an agent create a personnel dossier — and four note templates (`_templates/knowledge-note.md`, `source-note.md`, `sop-note.md`, `40-decisions/_template.md`) whose core versions produce notes that fail this mode's own frontmatter check. |

## Placeholders the setup still has to fill
- `{{MODE}}` and `{{LANGUAGE}}` in the vault `CLAUDE.md`
- `{{MODE}}` and `{{LANGUAGE}}` in the root `index.md` (both variants)
- `{{DATE}}` in `About this vault.md` and **four times in `THIS-COPY.md`**
  (the date of the copy, its `created:`, its first changelog line, and
  `review_due:` — which gets today + 12 months, not today)
- `{{COMPANY}}` in `About this vault.md` and `70-onboarding/onboarding-path.md`
- the `<…>` fields in `About this vault.md`, `Deadlines.md` and
  `70-onboarding/onboarding-path.md` — nine of them, and `hygiene.py`
  cannot see any of them, because `owner: <role that owns this vault>`
  is a perfectly non-empty value. `progress.py` counts them; run it
  before handing the vault over.

## Adding another module later
New folder here, shaped like a vault root, one line in the table above,
and every content folder it introduces brings its own `index.md` +
two-line `CLAUDE.md` — same rule as the core.
