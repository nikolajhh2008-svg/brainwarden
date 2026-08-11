# _templates

The shape of each note type. Copy a file from here and fill it — never
invent a fresh layout per note.

**Rules here:** these files are NOT notes; search and `--stats` skip this
folder. The `{{DATE}}` / `{{NAME}}` tokens stay unfilled HERE forever and
get real values only in the copy (the surrounding prose may be translated,
the tokens may not). Company mode: every copy needs `owner:`,
`audience:`, `confidentiality:` and `review_due:` filled — a note without
an owner rots. `maturity:` is how worked out it is, `status:` is whether
it still holds. If YOU wrote or filled the note, add
`generated: {by: <agent>/<model>, at: YYYY-MM-DD}`; never set
`verified:` — only a human earns that field, and without it nothing here
is company truth.
**NOT here:** filled-in notes. They go to the folder they belong to —
map in [../index.md](../index.md).

## Entry points
* [sop-note.md](sop-note.md) - a procedure: purpose, scope, roles, steps, exceptions, history
* [role-note.md](role-note.md) - a role: responsibility, limits, cover, needed knowledge
* [partner-note.md](partner-note.md) - an external company: delivery, contact, conditions, experience
* [onboarding-plan.md](onboarding-plan.md) - role-specific plan on top of the shared path
* [knowledge-note.md](knowledge-note.md) - one idea: own words, evidence, case, limit
* [source-note.md](source-note.md) - a book/paper/video: claims, quotes, verdict
* [../40-decisions/_template.md](../40-decisions/_template.md) - decision record (lives with the records)

<!-- generated: 2026-08-11 -->
