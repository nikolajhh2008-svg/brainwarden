---
name: brain-ingest
description: Work sources into the Brain — split PDFs/transcripts/articles from ~/Brain/00-inbox/raw/ (or a URL) into atomic, linked knowledge notes. Use on "ingest", "work in this source", "split this PDF/transcript", or new files in raw/.
---

# Brain ingest (source → atomic notes)

Raw material in, knowledge network out. A source is NEVER filed as one
lump — it gets split into atomic notes and woven into the vault.

## Steps
1. **Fetch the source:** files from `~/Brain/00-inbox/raw/` (PDF via Read,
   URL via WebFetch, transcripts directly). Several files: one pass each.
   **Large PDFs:** Read handles ~20 pages per call — work in page ranges
   (start with the table of contents), never silently truncate a book.
2. **Extract the ideas:** list the 3–12 genuinely useful ideas — the ones
   the person would want to find again. Skip filler.
3. **Write atomic notes** in the vault language, one idea per note, into
   `30-knowledge/<domain>/` (max ONE level of subfolders; if the source
   feeds a thesis/exam/project, link it from that project note). Before
   creating a note, run `python3 ~/Brain/.tools/search.py <topic>` — if a
   note on the idea exists, extend it instead of duplicating:
   - paraphrase in own words (template: `_templates/knowledge-note.md`;
     fill `{{DATE}}` with the real date)
   - `source:` frontmatter with the full reference
   - verbatim quotes only in a source note (`_templates/source-note.md`)
   - `[[link]]` related notes — only where it truly adds understanding
4. **Archive the source file** to `90-archive/raw/` (create if missing) so
   raw/ stays empty.
5. Report in 3 lines: N notes, where, what got linked.

## Rules
- Own words beat copying — a pasted source is collecting, not understanding.
- Every claim that could be cited later needs the exact reference (page!).
- Do not invent structure the source doesn't have; when unsure, fewer,
  denser notes.
