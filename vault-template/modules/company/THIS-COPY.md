---
type: knowledge
title: About this copy
created: {{DATE}}
tags: [meta]
owner: knowledge-owner
status: stable
audience: [all]
confidentiality: internal
review_due: {{DATE}}   # setup: today + 12 months — NOT today, or this page expires tomorrow
---

# About this copy

**This copy is from: {{DATE}}**

This is the one real weakness a folder has against a web page. A web page
is current by definition; a folder ages separately on every machine it
sits on. So the date goes here, and this file sits at the front of the
signpost.

## For everyone: is your copy still fresh?

Compare the date above with today.

- **Less than four weeks old:** fine.
- **Older:** get a new one. Say to Claude:

  > **Is my copy of the company vault still current? If not, fetch the
  > latest one.**

  Claude checks and updates it when a pull path is set up. If none is,
  it tells you who to ask.

**Your own notes are safe.** Anything in `00-inbox/` and your drafts in
`00-inbox/suggestions/` live only on your machine and are not
overwritten. Submit the ones that are ready before you update.

## For whoever maintains the vault: how a new copy happens

1. Work the changes into the main copy and release them (`status: stable`
   plus `verified:`).
2. **Raise the date at the top of this file.** This is the step that gets
   forgotten — without it nobody can tell there is anything new.
3. Distribute: either everyone pulls from the shared remote, or you send
   a dated package.

> TO FILL IN (IT / knowledge owner): How is this actually distributed —
> shared access to the Git remote, or a ZIP by mail? And who sends it?
> Replace this line once it is decided.

**Why this matters more than it looks.** A shared vault fails in a
specific way: not with a wrong answer, but with an answer that was right
last quarter. Nobody notices, because a stale note looks exactly like a
current one. The date is the only thing standing between the two, which
is why it is a file of its own rather than a line in a footer.

## What changed recently

- **{{DATE}}** — first version.

<!-- One line per release, newest at the top: what changed that somebody
     would care about. Not every correction individually. -->
