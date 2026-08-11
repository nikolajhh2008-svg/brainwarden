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

```bash
# 1 — core, every mode (as today)
mkdir -p ~/Brain && cp -R vault-template/. ~/Brain/

# 2 — modules/ is kit scaffolding; a vault must never contain it
rm -rf ~/Brain/modules

# 3 — professional AND company
cp -R vault-template/modules/processes/. ~/Brain/

# 4 — company only
cp -R vault-template/modules/company/. ~/Brain/
rm -rf ~/Brain/10-projects ~/Brain/20-areas ~/Brain/30-knowledge/people
rm -f  ~/Brain/"About me.md"          # replaced by "About this vault.md"
rm -f  ~/Brain/_templates/person-note.md \
       ~/Brain/_templates/project-note.md \
       ~/Brain/_templates/area-note.md \
       ~/Brain/_templates/journal-entry.md   # their folders do not exist here
```

Order matters: step 4 deliberately OVERWRITES six core `index.md` files
that describe folders which do not exist in a company vault — the root
one plus `00-inbox/`, `30-knowledge/`, `40-decisions/`, `90-archive/`
and `_templates/`. That is intended: every link inside an `index.md` has
to be a path that really exists, otherwise the whole signpost system
lies. Use plain `cp -R` for the overlay even on the adopt path (these
are kit infrastructure, not the human's content); the only content file
in the overlay is `About this vault.md`, so on an adopt run copy that
one with `cp -n` afterwards if it already exists.

`person-note.md` is deleted on purpose, not just left unlisted: a
template for dossiers about people is a trap in a vault whose rule is
"roles, not people".

`personal` gets no overlay at all.

## What each overlay adds

| Overlay | Adds |
|---|---|
| `processes/` | `50-processes/` (index + CLAUDE.md), `_templates/sop-note.md` |
| `company/` | `60-roles/`, `70-onboarding/` (incl. `onboarding-path.md`), `80-partners/`, `00-inbox/suggestions/`, `About this vault.md`, `_templates/role-note.md` + `partner-note.md` + `onboarding-plan.md`, and six overriding `index.md` files (root, `00-inbox`, `30-knowledge`, `40-decisions`, `90-archive`, `_templates`) |

## Placeholders the setup still has to fill
- `{{MODE}}` and `{{LANGUAGE}}` in the vault `CLAUDE.md`
- `{{MODE}}` and `{{LANGUAGE}}` in the root `index.md` (both variants)
- `{{DATE}}` in `About this vault.md`
- `{{COMPANY}}` in `About this vault.md` and `70-onboarding/onboarding-path.md`

## Adding another module later
New folder here, shaped like a vault root, one line in the table above,
and every content folder it introduces brings its own `index.md` +
three-line `CLAUDE.md` — same rule as the core.
