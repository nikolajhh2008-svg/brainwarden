# 40-decisions

One record per decision that was actually made — what was decided, why,
and what was rejected.

**Rules here:** append-only. A decision record is NEVER rewritten and
never deleted: if it turns out wrong, write a new record and link both
files to each other in plain text (`Supersedes [path]` in the new one,
`Superseded by [path]` appended to the old one) — an agent that lands in
the outdated record has to find the pointer THERE. File names
`YYYY-MM-DD-slug.md`, date first, so the folder sorts chronologically.
Terse is correct here; length is not a virtue.
**NOT here:** options still being weighed — those stay in the project
note in [../10-projects/](../10-projects/index.md) until they are
decided. Reusable insight from the decision →
[../30-knowledge/](../30-knowledge/index.md).

## Entry points
* [_template.md](_template.md) - the shape every record follows

<!--
With content, list only the decisions still in force that explain how
this vault or this life is set up, e.g.:
`* [2026-01-15-digital-notes.md](2026-01-15-digital-notes.md) - why everything lives in this vault`
Superseded records stay in the folder but drop off this list.
-->

<!-- generated: 2026-08-11 -->
