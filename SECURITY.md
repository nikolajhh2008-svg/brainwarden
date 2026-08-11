# Security

Brainwarden is a local-only kit: Markdown files, five Claude Code skills
and three Python scripts (`search.py`, `hygiene.py`, `harvest.py`). There is no server, no
telemetry, no network call of its own — the only things it writes are your
vault, your skills folder (`~/.claude/skills/`) and one opt-in block in
`~/.claude/CLAUDE.md`. Run a second brain alongside the first and it adds
one more vault folder and one more config directory (`~/.claude-work`),
nothing else.

Things worth knowing:

- **The setup asks before every boundary:** touching `~/.claude/CLAUDE.md`,
  scanning your computer during the interview (explicit consent question,
  scope reported, veto honored), and anything involving an existing vault.
- **The scripts and the skills never leave your machine.** What Claude
  itself sends to Anthropic is governed by your Claude Code settings, not
  by this kit.
- **Everything is reversible:** the vault is Git-versioned from the first
  commit, and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) documents the full
  uninstall — three deletions for one brain, plus the second vault,
  its config directory and its shell alias if you set one up.

## Reporting a vulnerability

Found something anyway? Please open a
[GitHub issue](https://github.com/nikolajhh2008-svg/brainwarden/issues)
— or use GitHub's private vulnerability reporting on this repository if
it shouldn't be public.
