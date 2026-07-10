---
name: brain-capture
description: Frictionless capture into the Brain (~/Brain/00-inbox). Use when the user says "capture: …", "note this down", "remember this for my brain", or when a spontaneous idea surfaces mid-session.
---

# Brain capture (zero friction)

A thought becomes a file in `~/Brain/00-inbox/` IMMEDIATELY — no questions
about filing, no tags, no thinking. Sorting happens later at the review.

## Steps
1. Content = whatever follows "capture:" (or the thought from context when
   they say "capture that").
2. Write the file: `~/Brain/00-inbox/YYYY-MM-DD-<short-slug>.md`
   ```markdown
   # <one-line title>

   <the thought, verbatim or lightly cleaned — fix voice-transcription
   typos, do NOT reinterpret the content. Write in the vault language.>

   _Captured: YYYY-MM-DD HH:MM · Context: <one line on where it came from>_
   ```
3. Confirm with ONE line — naming the destination on special cases so
   nothing feels like it vanished: "✓ captured: <title> → Deadlines +
   Home". No essays.

## Special cases
- **Decisions:** starts with "decision:" (or clearly is one) → write a
  decision record to `~/Brain/40-decisions/YYYY-MM-DD-slug.md` instead
  (template: `40-decisions/_template.md`). Append-only.
- **Deadlines:** if the capture contains a concrete date/deadline, ALSO
  add a one-liner to `~/Brain/Deadlines.md` right away — deadlines must
  never wait for the weekly review. If it lands in the next ~3 dates,
  also refresh the "Next deadlines" block in `~/Brain/Home.md`.
- **Reference material** ("keep this findable": a link, a quote, a
  recommendation): still just one inbox file — the review gives it the
  light treatment (tags, no atomization). Never over-process a bookmark.
- **Several thoughts in one dump** (common with voice): split at clear
  topic boundaries — one file each.

When creating any note from a template, fill `{{DATE}}` (and `{{NAME}}`)
with real values — placeholders never leave the `_templates/` folder.

## Rules
- NEVER ask "where should I file this?" — the inbox is always right.
- One capture = one file. Two thoughts = two files.
- Works from ANY session, whatever project is open.
