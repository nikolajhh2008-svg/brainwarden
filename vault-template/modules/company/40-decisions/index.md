# 40-decisions

One record per decision that was actually made — what was decided, why,
and what was rejected. This is the folder that answers "why is it like
this?" without asking the person who decided it.

**Rules here:** append-only. A record is NEVER rewritten and never
deleted: if it turns out wrong, write a new record and link both files
in plain text (`Supersedes [path]` in the new one, `Superseded by
[path]` plus `status: deprecated` appended to the old one) — an agent
that lands in the outdated record has to find the pointer THERE. File
names `YYYY-MM-DD-slug.md`, date first. Company mode: name the deciding
`owner:` role, not only a person. Terse is correct here.
**NOT here:** options still being weighed — those stay in the
suggestion or the note where they came up. HOW something is executed →
[../50-processes/](../50-processes/index.md); an SOP links the decision
instead of repeating its reasoning.

## Entry points
* [_template.md](_template.md) - the shape every record follows

<!--
With content, list only the decisions still in force that shape daily
work, e.g.:
* [2026-01-15-single-supplier-packaging.md](2026-01-15-single-supplier-packaging.md) - why we buy boxes from one source
Superseded records stay in the folder but drop off this list.
-->

<!-- generated: 2026-08-11 -->
