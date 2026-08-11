# Using a Brainwarden vault in Claude Cowork

Cowork is Anthropic's desktop agent for people who do not use a terminal:
you point it at a folder, describe what you want, and it works on the files.
That is exactly the audience a company vault has to reach — a wholesaler, a
bookkeeper, someone in marketing. This page says what carries over, what
does not, and what to do instead.

**The short version: the vault works. The convenience layer does not.**

## What carries over — the part that matters

Everything that makes the vault navigable is plain Markdown, and Cowork
reads the folder you give it:

- **The notes themselves.** Obviously.
- **Every `index.md` signpost.** This is why the kit treats `index.md` as
  the canonical waypoint and the tiny per-folder `CLAUDE.md` as *only* a
  loading mechanism for Claude Code. In Cowork the loading mechanism is
  gone; the signpost is still there, still says what belongs in that folder
  and what does not, and an agent that opens it gets the same orientation.
- **The frontmatter.** `status`, `verified`, `ownership`, `stale_after` are
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

4. **Optional, for people who want the five verbs:** package each skill as
   a zip and enable it under Customize → Skills on claude.ai. They then
   work in Cowork too. Skip this for read-only users — they do not need it.

## Which one for whom

- **Cowork** — everyone who reads: sales, marketing, accounting, branches.
  No terminal, no install beyond the app, folder-scoped access.
- **Claude Code** — whoever maintains the vault: runs the weekly review,
  uses `hygiene.py` and `harvest.py`, wants the capture net. One person per
  company is enough.

Both work on the same folder. Nothing has to be converted, and a vault
maintained in Claude Code is read correctly in Cowork the same day.

*Sources: Cowork overview and help pages on claude.com and
support.claude.com; the hooks gap is tracked as an open issue in the
claude-code repository. Cowork moves quickly — if something here is out of
date, the vault still works; only the paragraph above it needs fixing.*
