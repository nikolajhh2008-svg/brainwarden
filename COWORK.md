# Using a Brainwarden vault in Claude Cowork

Cowork is Anthropic's desktop agent for people who do not use a terminal:
you point it at a folder, describe what you want, and it works on the files.
That is exactly the audience a company vault has to reach — a wholesaler, a
bookkeeper, someone in marketing. This page says what carries over, what
does not, and what to do instead.

**The short version: the vault works. The convenience layer does not.**

> **Whoever set the vault up: this page has to travel.** It is the only
> document in the kit addressed to the colleagues who just read the vault,
> and it lives in the kit repo, which the setup tells you that you may
> delete. Step 7b of `SETUP-FOR-CLAUDE.md` copies it to
> `<vault>/.tools/COWORK.md` (not the vault root — a kit document there
> turns three `hygiene.py` rubrics red) and sends it on. If your vault's
> notes are not in English, translate the instruction block in step 3
> below before you hand it over: it is the one page those colleagues are
> asked to read, and handing it over in a language the rest of the vault
> does not use is how the first ten minutes go wrong.

## What carries over — the part that matters

Everything that makes the vault navigable is plain Markdown, and Cowork
reads the folder you give it:

- **The notes themselves.** Obviously.
- **Every `index.md` signpost.** This is why the kit treats `index.md` as
  the canonical waypoint and the tiny per-folder `CLAUDE.md` as *only* a
  loading mechanism for Claude Code. In Cowork the loading mechanism is
  gone; the signpost is still there, still says what belongs in that folder
  and what does not, and an agent that opens it gets the same orientation.
- **The frontmatter.** `status`, `verified`, `owner`, `review_due` are
  text in a file. Any agent can read them and apply the rules.
- **The vault's `CLAUDE.md`.** Not loaded automatically — but it is a file
  in the root, and a one-line project instruction makes Cowork read it.

Asking "how do we handle a purchase above the cash limit?" needs none of
the machinery. It needs a folder, a signpost and a note. That is the
95 % case for anyone who is not the person maintaining the vault.

## What does not carry over

| | Claude Code | Cowork |
|---|---|---|
| Skills from `.claude/skills/` in the folder | loaded | **not read** — Cowork loads skills enabled on your claude.ai account |
| `CLAUDE.md`, incl. per-folder ones | loaded, subfolder ones lazily | **not documented; assume no** |
| Hooks (`Stop`, `SessionEnd`) | supported | **not supported** (open feature request) |
| Running `.tools/*.py` directly | yes | only as scripts inside an uploaded skill |

Concretely, the two things you lose are the **capture net** (the hook that
notices when nothing has reached the brain for hours) and the **session
queue**. Both are about *filling* the vault. Reading it is unaffected.

That trade is usually the right way round for a company vault: most people
look things up, few people write. Give the maintainer Claude Code and
everyone else Cowork.

## Setting it up in Cowork

1. **Put the vault folder on the machine.** Not in a cloud-sync folder —
   the same rule as for Claude Code.
2. **Claude Desktop → Cowork → add the folder to a project.**
3. **Paste this into the project's instructions** (it replaces what the
   global rules block does in Claude Code — keep it short, it is read every
   time):

   ```
   This folder is a Brainwarden knowledge vault.
   Read index.md first — it is the folder map. Read CLAUDE.md before
   writing anything; it holds the schema and the rules.
   When you open a folder, read its index.md before its notes.
   Content counts as valid only with status: stable AND a filled verified:
   line. Everything else is a draft — say so when you quote it.
   Never invent a figure, a price, a condition or a deadline. "I don't
   know, ask the owner named in the note" is a correct answer.
   ```

4. **Type the first three sentences.** Say this in the handover, out
   loud, because the vault itself does not contain it and a folder full
   of Markdown gives nobody a first move:

   - *"What is this folder, in three sentences?"* — it reads
     `About this vault.md` and answers.
   - *"How do we do <the thing you were hired to do> here?"* — the real
     question, and the one the vault exists for. If the answer is "I
     don't know, ask <role>", that is correct behaviour, not a broken
     folder.
   - *"Write a suggestion into 00-inbox/suggestions/: …"* — how you
     correct something. It is a proposal until someone releases it, you
     cannot break anything, and a rejected one costs nothing.

   Hand these three over in the vault's language, like the block above.

   Nothing has to be learned beyond those three. Everything else in this
   page is for whoever maintains the folder.

5. **Optional, for people who want the five verbs:** package each skill as
   a zip and enable it under Customize → Skills on claude.ai. What carries
   over is the procedure, not the tooling: every skill's retrieval step is
   `python3 .tools/search.py`, and `brain-review` also calls `hygiene.py`,
   `harvest.py --queue` and `git commit` — the last row of the table above
   applies to those lines. Asking and capturing survive it (they are file
   reads and file writes); the weekly review is the one that really wants
   Claude Code. Skip this for read-only users — they do not need it.

   Worth being blunt about, because the setup does the opposite: in
   `company` mode Step 4a copies the five skills into
   `<vault>/.claude/skills/`, and Cowork does not read that folder. For
   everyone on Cowork those files are inert — not broken, just not
   loaded. They are there for the one person who opens the vault in
   Claude Code. Nothing is missing for the readers: looking something up
   needs the project instruction in step 3 and nothing else.

## Which one for whom

- **Cowork** — everyone who reads: sales, marketing, accounting, branches.
  No terminal, no install beyond the app, folder-scoped access.
- **Claude Code** — whoever maintains the vault: runs the weekly review,
  uses `hygiene.py`, `harvest.py --queue` and — in a company vault —
  `progress.py`, wants the capture net. One person per company is enough.

Both work on the same folder. Nothing has to be converted, and a vault
maintained in Claude Code is read correctly in Cowork the same day. Someone
working from a *copy* rather than the shared folder should read
`THIS-COPY.md` in the vault root first: it carries the date that copy was
cut, which is the one thing the notes themselves cannot tell them.

*Sources: Cowork overview and help pages on claude.com and
support.claude.com; the hooks gap is tracked as an open issue in the
claude-code repository. Cowork moves quickly — if something here is out of
date, the vault still works; only the paragraph above it needs fixing.*
