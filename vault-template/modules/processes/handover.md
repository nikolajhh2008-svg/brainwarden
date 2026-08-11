---
type: knowledge
title: Handover view
created: {{DATE}}
tags: [handover, meta]
ownership: private
---

# Handover view

Not a folder — a query. A handover folder is guaranteed to be out of date
on the day you need it, because nobody maintains two places at once.

## What belongs to the company

```
python3 .tools/search.py "ownership: company" --k 40
```

Everything that matches leaves with the job. In Germany and Austria an
employee must hand over what they obtained from the employment when they
leave, and courts have held that this includes notes they wrote
themselves about customer conversations and project work — copies
included (§ 667 BGB analog; BAG 14.12.2011 – 10 AZR 283/10). Only
genuinely private records are exempt.

## What is handover-relevant

```
python3 .tools/search.py "handover_relevant: true" --k 40
```

Runbooks above all: the things only you know how to run. The tacit part —
why it is done this way, who to call when it breaks, which workaround is
load-bearing — is what actually gets lost, and it is the part nobody
writes down unprompted.

## What stays yours

`ownership: private` — your contribution log, your learning notes, your
own thinking. After leaving you may use what is in your head; keeping
company material is a different matter.

## Monthly, not weekly

One question: did a new responsibility arrive that has no runbook yet?
That is the whole ritual. Anything more elaborate does not survive
contact with a normal working month.
