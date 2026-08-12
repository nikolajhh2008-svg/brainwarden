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

**"Submit" needs a real route, and only your company can name it.** A
file you wrote in your own copy is invisible to everyone else until
something carries it back. Whoever set this vault up fills the second
marker below with the actual route — the same channel you would use for
anything else (a shared folder, a mail address, "drop it in the office"),
not a new tool. Until that line is answered, write your suggestions
anyway and tell the person named under "Who may release content" in
[About this vault.md](About%20this%20vault.md) that they exist.

> TO FILL IN (knowledge owner): Where does a finished suggestion go so
> that someone else sees it? Replace this line with the actual route.

## For whoever maintains the vault: how a new copy happens

1. Work the changes into the main copy and release them (`status: stable`
   plus `verified:`).
2. **Raise the date at the top of this file.** This is the step that gets
   forgotten — without it nobody can tell there is anything new. Nothing
   automates it: the weekly review empties the inbox and commits, but it
   does not date this file and does not send anything anywhere. Put both
   on the review's checklist by hand, or the corrections stay on one
   machine.
3. Distribute: either everyone pulls from the shared remote, or you send
   a dated package.

> TO FILL IN (IT / knowledge owner): How is this actually distributed —
> shared access to the Git remote, or a ZIP by mail? And who sends it?
> Replace this line once it is decided.

**If you distribute through Git and more than one person commits:** two
people editing the same note on the same day is a merge conflict, and it
will happen in the first month. The rule that keeps it boring: only the
maintainer's copy is written to; everyone else's copy is read-only and
their contributions travel as files in `00-inbox/suggestions/`, never as
commits. One writer, many readers — that is what the release step in
[About this vault.md](About%20this%20vault.md) already assumes. If you
genuinely need several writers, that is a Git workflow (branches, pull
requests) and this kit does not teach one.

**Why this matters more than it looks.** A shared vault fails in a
specific way: not with a wrong answer, but with an answer that was right
last quarter. Nobody notices, because a stale note looks exactly like a
current one. The date is the only thing standing between the two, which
is why it is a file of its own rather than a line in a footer.

## What changed recently

- **{{DATE}}** — first version.

<!-- One line per release, newest at the top: what changed that somebody
     would care about. Not every correction individually. -->
