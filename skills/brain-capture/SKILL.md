---
name: brain-capture
description: Frictionless capture into the Brain's inbox. Use when the user says "capture: …", "note this down", "remember this for my brain", or when a spontaneous idea, decision or date surfaces mid-session.
---

# Brain capture (zero friction)

A thought becomes a file in `<vault>/00-inbox/` IMMEDIATELY — no questions
about filing, no tags, no thinking. Sorting happens later at the review.

**Conventions:** `<vault>` = the vault path from the `Brain vault:` line in
your global rules (none set → `~/Brain`). `python3` = your working python
command (on most Windows machines `py -3`; the global rules name it).

## Steps
0. **Read `<vault>/CLAUDE.md` before the first write of the session.** It
   carries the vault language, the schema and the mode — and unless this
   session was started inside the vault, none of it is in your context.
   Not there? Wrong path or unfinished setup: say so instead of writing
   files into a random folder. (One read per session is enough.)
1. Content = whatever follows "capture:" (or the thought from context when
   they say "capture that").
2. Write the file: `<vault>/00-inbox/YYYY-MM-DD-<short-slug>.md`
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
- **Decisions — recognize them by MEANING, not by keyword:** the human
  settles an open question ("decision: …", "Entscheidung: …", "décision :",
  "we're going with Postgres", "ok, no second supplier"). Whatever language
  or wording they used, write a decision record to
  `<vault>/40-decisions/YYYY-MM-DD-slug.md` instead of an inbox file
  (template: `40-decisions/_template.md`) — context, decision, rejected
  alternatives. Append-only.
  **Reverses an earlier decision?** Search it first
  (`python3 <vault>/.tools/search.py <topic>`), then write both sides: the
  new record gets a `## Status` section with
  `Supersedes [40-decisions/<old>.md](40-decisions/<old>.md)`, and the OLD
  file: its `## Status` body is REPLACED by
  `Superseded by [<path>](<path>)` (append the section if it has none), and
  its frontmatter gets `status: deprecated`. Never leave an "in force" line
  standing above a supersede notice — an agent greps the first `## Status`
  and believes it. Nothing else in the old record changes; this one section
  is the only exception to append-only.
- **Dates:** a capture with a concrete date/deadline ALSO gets a one-liner
  in `<vault>/Deadlines.md` right away (date first) — dates never wait for
  the weekly review. If it lands in the next ~3 dates, refresh the "Next
  deadlines" block in `<vault>/Home.md` too.
  **A moved date REPLACES its line, it is never appended** — two dates for
  one appointment is worse than none. Find the old one first:
  `python3 <vault>/.tools/search.py <old-date> <topic>`, then update every
  hit (Deadlines.md, the project note's log, Home.md) and say in your one
  line which files you corrected.
- **Reference material** ("keep this findable": a link, a quote, a
  recommendation): still just one inbox file — the review gives it the
  light treatment (tags, no atomization). Never over-process a bookmark.
- **Several thoughts in one dump** (common with voice): split at clear
  topic boundaries — one file each.

When creating any note from a template, fill `{{DATE}}` (and `{{NAME}}`)
with real values — placeholders never leave the `_templates/` folder.

## Company mode (only when the vault `CLAUDE.md` names the mode `company`)
Captures still go straight to the inbox. But anything about a person is
captured as a ROLE, not a dossier, and nothing you write becomes company
truth: a note that leaves the inbox keeps `status: draft` until a human
sets `verified: {by: human:<name>, at: YYYY-MM-DD}`.

## Rules
- NEVER ask "where should I file this?" — the inbox is always right.
- One capture = one file. Two thoughts = two files.
- Capture what they said; never add a conclusion they didn't draw.
- Works from ANY session, whatever project is open.
