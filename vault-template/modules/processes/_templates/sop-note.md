---
type: sop
title: <what this procedure produces, as a task: "Approve an incoming invoice">
created: {{DATE}}
ownership: private        # work brains: private | company | mixed — delete this line in a personal brain
last_verified: {{DATE}}   # the day you last actually ran this
handover_relevant: true   # a stand-in would need this to run it without you
tags: []
owner: <team or role that answers for this content — never a private person's name>
status: draft
version: 1.0
valid_from: {{DATE}}
review_due: <YYYY-MM-DD — at the latest one year out>
verified:
audience: [<role>, <role>]
confidentiality: internal
---

# <Procedure name>

## Purpose
<What this procedure achieves and why it exists. 1–3 sentences. If you
cannot name what goes wrong without it, it is not an SOP yet.>

## Scope
<Applies to: which cases, which locations, which systems. And explicitly:
what it does NOT cover.>

## Roles
| Role | Does what |
|---|---|
| <role from 60-roles/> | <their part> |
| <role> | <their part> |

## Procedure
1. <Imperative, one action, checkable. Name the system and the button.>
2. <…>
3. <…>

## Exceptions
- <case> → <what to do instead, and who decides>
- Nothing fits? Stop and ask <role> — do not improvise in silence.

## Change history
| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | {{DATE}} | First version | {{NAME}} |

<!-- Binding only with `status: stable` AND a filled `verified:`
     ({by: human:<name>, at: YYYY-MM-DD}). Claude never sets `verified:`.
     Any change to a stable SOP: bump `version`, add a history row,
     push `review_due` forward. `confidentiality` is a LABEL, not
     access control — real protection only comes from separate vaults. -->
