# Brain — personal knowledge vault

One folder, two windows: an Obsidian vault AND a Claude Code working
directory on the same Markdown files. Structure: PARA-inspired
(deliberately flat) plus Zettelkasten principles for knowledge.

**Vault language: {{LANGUAGE}}** — write all notes, titles and links in
this language (set during setup; the folder names stay English so the
skills keep working).

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

**Why the number gaps?** They are deliberate expansion space: new
top-level modules slot in as `50-journal/`, `60-media/` etc. without ever
re-sorting the core. Ask Claude to add a module and it lands in a gap —
the core six folders and their English names stay fixed (the skills
depend on them).

**Core sorting principle:** file by ACTIONABILITY (which project/area
needs this NOW?), never by topic taxonomy. Findability comes from
[[links]], tags and search — not from folder depth.

## Note schema (machine-readable)
Frontmatter for every note OUTSIDE the inbox:
```yaml
---
type: knowledge | source | decision | project | area
tags: [kebab-case, lowercase, few]
source: <URL/book/person — only for external sources>
created: YYYY-MM-DD
---
```
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

## Instructions for Claude
- Retrieval: ALWAYS run `python3 ~/Brain/.tools/search.py <terms>` first
  (saves context), then read only the hits — never the whole vault.
- Incoming sources: files in `00-inbox/raw/` → skill `brain-ingest`.
- Template per note type: knowledge → `_templates/knowledge-note.md` ·
  source → `source-note.md` · person → `person-note.md` · project →
  `project-note.md` · area → `area-note.md` · journal → `journal-entry.md`
  · decision → `40-decisions/_template.md`. When instantiating, fill the
  DATE/NAME placeholders with real values; the files inside `_templates/`
  keep their placeholders forever.
  Never rewrite a decision record — append.
- Inside `30-knowledge/` at most ONE level of subfolders (like `people/`);
  everywhere else, no new subfolder without a reason.
- Before creating a people/knowledge note, search first — extend instead
  of duplicating.
- Review hygiene: orphan notes, dead `[[links]]`, empty files.
- Finished project / ended area → move to `90-archive/`.
- The structure may EVOLVE: if reviews show a folder or area no longer
  fits the person's life, propose the change — the onboarding interview was a
  starting point, not a life sentence.

## Sync
- Versioning: local Git. Do NOT put the vault in iCloud/Dropbox sync
  folders (corruption risk with Git). Phone: Obsidian Sync.

## Commands
- **brain-capture** — frictionless thought → inbox (from any session)
- **brain-ingest** — split a source from raw/ into atomic notes
- **brain-review** — weekly: inbox to zero, hygiene, git commit
