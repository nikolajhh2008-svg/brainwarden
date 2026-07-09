# Contributing

Thanks for making the kit better! The ground rules:

1. **Stay lean.** The kit is deliberately small — every addition must make
   the start easier, not heavier. New mandatory folders, plugins or
   services carry a high burden of proof.
2. **Self-explanatory for Claude.** Anything a human would have to do
   should instead be done by Claude via `SETUP-FOR-CLAUDE.md`. Test
   changes by running the setup once from scratch.
3. **No personal data.** Templates and examples stay generic
   ({{NAME}} placeholders). PRs containing real names/addresses are rejected.

## Process
- **Bug/idea:** open an issue (English preferred), short and concrete.
- **PR:** fork → branch → PR with 2–3 sentences: what, why, how tested.

## Style
- Markdown, ~80-char feel, no HTML tricks.
- Examples follow `examples/` (frontmatter + "Related:" links, marked as
  demo content).
