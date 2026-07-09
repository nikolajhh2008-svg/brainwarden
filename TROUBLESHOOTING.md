# FAQ & troubleshooting

**Obsidian shows nothing?** Obsidian → "Open folder as vault" → pick
`~/Brain`. Done — Obsidian and Claude work on the same files.

**Do I need to know Markdown?** No. You dump ("capture: …"), Claude does
structure. In Obsidian you just click [[links]].

**Why not iCloud/Dropbox?** Cloud sync + Git on the same folder causes
file conflicts and corrupted vaults. For your phone: Obsidian Sync.

**Can my brain be in German (or any language)?** Yes — the repo is
English, but during setup Claude asks for your vault language and writes
(and translates the starter pages) accordingly. Only folder names stay
English so the skills keep working.

**Inbox overflowing?** That's what the weekly ritual is for: "brain
review" — Claude processes the inbox to zero. Second brains die of full
inboxes, not missing features.

**Claude doesn't know my brain in a new session?** The rules from setup
step 4 (in `~/.claude/CLAUDE.md`) tell every session where the brain
lives. Test it: ask "search my brain for X".

**Why do the folder numbers jump (…40, then 90)?** The gap is expansion
space: optional modules (journal, media log, health, money …) slot in as
50–80 without re-sorting anything. Ask Claude to add one anytime.

**Can I rename folders?** Area folders are named after YOUR life —
Claude creates them with your words during setup. Keep the numbered
top-level scheme (stable sorting) and the English top-level names (the
skills depend on them).

**What does NOT belong in the brain?** Operational knowledge of active
code projects (belongs in that repo's CLAUDE.md) and anything you call
"private".

**Setup died halfway?** A fresh install can simply be removed
(`rm -rf ~/Brain`) and restarted — nothing else on your machine changed
except `~/.claude/skills/` and the rules block in `~/.claude/CLAUDE.md`,
both safe to re-run. An adopted vault: ask Claude to undo its last
changes via Git.

**Broke Git / wrong commit?** No drama: `cd ~/Brain && git log --oneline`
shows history, `git checkout -- <file>` restores a file. When in doubt,
ask Claude — the brain is versioned, nothing is ever truly gone.

**I already have an Obsidian vault.** Tell Claude during setup — it will
adopt your existing structure (scan, map, add only what's missing)
instead of overwriting anything.

**How do I uninstall completely?** Three things and you're clean:
`rm -rf ~/Brain` (or keep it — it's just Markdown), delete the four
`brain-*` folders from `~/.claude/skills/`, and remove the "Brain" block
from `~/.claude/CLAUDE.md`. Nothing else was touched.

**Does it work with Obsidian's Canvas and Bases?** Yes — the vault is
plain Markdown, so every Obsidian feature works on top. If you want
Claude to build canvases (visual maps) or bases (table views) for you,
install Obsidian's official Claude skills for markdown/canvas/bases and
just ask ("build me a canvas map of my ABA project").
