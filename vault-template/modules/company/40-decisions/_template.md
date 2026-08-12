---
type: decision
title: <title>
created: {{DATE}}
tags: []
owner: <role that made the call — the ROLE, not only the person>
status: stable
audience: [all]
confidentiality: internal
review_due: <YYYY-MM-DD — at the latest one year out>
verified:
---

# Decision: <title>

**Date:** {{DATE}} · **Decided by:** <role from 60-roles/> ({{NAME}})

## Context
<Why did this decision come up? 2–4 sentences.>

## Decision
<What was decided — concrete, with numbers/names.>

## Alternatives (rejected)
- <option> — <why not>

## Status
In force.

<!-- Company mode: `owner`, `audience`, `confidentiality` and `review_due`
     are required like everywhere else, and `owner:` is the ROLE that made
     the call — a record whose only owner is a person's name loses its
     owner the day that person leaves. `status: stable` is correct from
     the start (a decision either was made or it wasn't), but it only
     becomes company truth once a human fills `verified:`. There is no
     `ownership:` field in a shared vault.

     When this record is replaced, this section is REWRITTEN, not extended:
     the line above is replaced by `Superseded by [<path>](<path>)`, and the
     frontmatter gets `status: deprecated`. Two `## Status` sections, the
     first still saying "In force", is the one failure this convention
     exists to prevent — an agent greps the first hit and believes it.
     The new record gets its own `## Status` with
     `Supersedes [40-decisions/<old-file>.md](<old-file>.md)`.
     Rewriting THIS section is the single exception to append-only;
     everything else in a decision record stays untouched forever. -->
