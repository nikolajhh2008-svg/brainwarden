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

**I stopped using it for weeks — is it dead?** No. That's a design case,
not a failure: the next "brain review" catches up in prioritized batches
(deadlines first), sweeps what the weeks actually produced, and refreshes
`Home`. No guilt, no restart needed — just say "brain review".

**Claude filed something wrong (or I want to undo something)?** Every
review and ingest reports exactly what went where — nothing is silent.
To undo: tell Claude ("move that note / undo the last review") or use
Git yourself (`git log`, `git checkout -- <file>`). The brain is
versioned; every change is one commit away from undone.

**`Home` looks stale?** The weekly review refreshes all four blocks
(projects, deadlines, open questions, new notes); deadline captures
update the deadline block immediately. Out of sync anyway? Say
"refresh Home".

**What are these `<!-- block:… -->` comments in `Home`?** Invisible
markers around each of the four blocks — Obsidian doesn't show them, and
Claude uses them to find the right block when it refreshes the page. They
are why your headings can be in your language: the markers are the
address, the headings are just text. Two rules if you edit `Home`
yourself: don't delete a marker line, and don't delete a line marked
`<!-- keep:… -->` (that's how the "Areas:" line survives every refresh) —
change its content instead. If a block ever stops updating, a marker was
probably lost; say "repair Home's block markers".

**Claude doesn't know my brain in a new session?** The global rules block
the setup wrote (in `~/.claude/CLAUDE.md`) tells every session where the
brain lives. Test it: ask "search my brain for X". Nothing happens? Check
that the block is really there — `grep "Brain vault:" ~/.claude/CLAUDE.md`
— and that the path in it is your real vault path. Grepping for the plain
word "Brain" proves nothing: it matches any unrelated line and looks green
even when the block is missing entirely.

**Can I have one brain for private and one for work?** Yes, and that is
the normal setup: two vaults in two folders, each with its own rules. The
second one gets its own Claude Code configuration directory plus a
one-word start command, so nothing bleeds across. Ask Claude for it — it
adds a line like
`alias workbrain='CLAUDE_CONFIG_DIR=~/.claude-work claude'` to your shell
profile.

**What's the difference between `claude` and `workbrain`?** Which brain
you're talking to. `claude` starts your normal setup with the private
brain's rules, skills and session history; `workbrain` starts the same
program with a different configuration directory, so it sees the work
vault's rules, its own copy of the skills and its own sessions. Same
program, two separate memories — nothing you capture in one shows up in
the other. First start of a new one may ask you to log in once; that's
normal.

**The skills write into the wrong brain.** Three usual causes, in this
order: (1) you started the wrong command — a session started with
`claude` writes to the brain configured in `~/.claude/CLAUDE.md`, never
to the work vault; (2) the `Brain vault:` line in that configuration
directory points at the other vault (check both files:
`grep "Brain vault:" ~/.claude/CLAUDE.md ~/.claude-work/CLAUDE.md`); (3)
only one of the two configuration directories has the five `brain-*`
skills — each needs its own copy. Anything already filed in the wrong
place: tell Claude to move it ("move that note into my work brain"), or
`git checkout` it away — the vault is versioned.

**After the update some notes still say `status: seed`.** The kit renamed
that field: maturity (`seed`/`growing`/`evergreen`) now lives in
`maturity:`, and `status:` means validity (`draft`/`stable`/
`deprecated`). Say *"finish the status → maturity migration"* — Claude
lists the affected notes first, renames only the field name (never a
value, never your text) and commits it separately, so it can be undone on
its own. Notes whose `status:` is `draft`/`stable`/`deprecated` are
already correct and stay untouched.

**A folder has no `index.md` (or no tiny `CLAUDE.md`) in it.** Those two
are the signposts every folder with notes carries: `index.md` says what
belongs there, what does not and where to start; the three-line
`CLAUDE.md` next to it just pulls that signpost into Claude's context
automatically. Vaults built before those existed simply lack them — say
*"backfill the missing index files in my brain"*. Folders you created by
hand need the pair too; without it, agents guess, and guessing is what
this system exists to prevent. `python3 .tools/hygiene.py` lists notes
that no `index.md` mentions.

**Why do the folder numbers jump (…40, then 90)?** The gap is expansion
space: optional modules (journal, media log, health, money …) slot in as
50–80 without re-sorting anything. Ask Claude to add one anytime. In a
work brain `50-processes/` and `60-contribution/` already sit there, and a company brain uses
all of 50–80 (processes, roles, onboarding, partners) — there, new
content goes into one of those instead of a new folder.

**My work brain has folders my private one doesn't (and vice versa).**
That's the mode: a private brain has projects and areas, a work brain
adds `50-processes/` for recurring workflows and `60-contribution/` for what you actually did, a company brain drops
projects, areas and person notes entirely and carries processes, roles,
onboarding and partners instead. Each folder explains itself in its own
`index.md`.

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

**A newer kit version came out — how do I update?** One sentence to
Claude: *"Update my brainwarden setup from
https://github.com/nikolajhh2008-svg/brainwarden — follow the Updating
section in SETUP-FOR-CLAUDE.md."* Your notes are never touched; updates
only replace skills, the search tool and the dashboard scaffolding.

**How do I uninstall completely?** Three things and you're clean:
`rm -rf ~/Brain` (or keep it — it's just Markdown), delete the five
`brain-*` folders from `~/.claude/skills/`, and remove the "Brain" block
from `~/.claude/CLAUDE.md`. Nothing else was touched. Have a second
brain? Then also `rm -rf` its vault folder and its configuration
directory (`~/.claude-work`), and delete the `alias workbrain=…` line
from your shell profile (`~/.zshrc` or `~/.bashrc`).

**Does it work with Obsidian's Canvas and Bases?** Yes — the vault is
plain Markdown, so every Obsidian feature works on top. If you want
Claude to build canvases (visual maps) or bases (table views) for you,
install Obsidian's official Claude skills for markdown/canvas/bases and
just ask ("build me a canvas map of my thesis project").

**Can Claude run the weekly review on its own (unattended)?** Yes — but
it's opt-in, and you should know the trade-offs first:
- **It spends your Claude subscription.** Every unattended run uses plan
  usage like a normal session. A weekly review is cheap; anything more
  frequent adds up fast. Weekly is the sweet spot — never sub-daily.
- **It edits and commits on its own.** Safe *because* the vault is
  Git-backed — every change stays one `git checkout` from undo — and it
  follows the review skill's autonomous rules: it deletes nothing
  uncertain, archives nothing unasked, and parks every question in Home's
  "Open questions" block instead of a chat you'll never see.
- **It writes down what it did.** Each unattended run appends a short
  report to `<your vault>/.tools/logs/auto-review-YYYY-MM-DD.md` — one
  file per run: what it filed, what it left alone, what it wants to ask
  you. That folder is tooling, not notes: it stays out of search results
  and out of your Obsidian graph, and you can read it any time or delete
  it without losing anything (the Git history holds the same story).
  Housekeeping: the review keeps the last ~12 files and deletes older
  ones. What the log does NOT contain: anything about who read or
  searched what — the kit does not track usage, deliberately.
- **It's a convenience, not the system.** The manual "brain review" is
  the real ritual; the scheduler just presses the button on weeks you
  forget. A phone reminder is the simpler, free alternative.

Two ways to set it up: the easiest is **Claude Code Desktop → Routines**
(same on macOS/Windows/Linux: New routine → Local → your `~/Brain` →
instructions "run the brain-review skill on this vault" → Weekly).
Terminal users can instead ask Claude — *"set up an automatic weekly
brain review"* — and it writes the scheduler job for your OS (launchd /
cron / Task Scheduler, with the full path to `claude` — scheduled tasks
don't know your PATH).

## Company brains

**How do several people share one vault?** Through a private Git remote:
one person sets the vault up, pushes it, everyone else clones it and
pulls. Not through a synced cloud folder — Git plus Dropbox/OneDrive on
the same folder is the classic way to corrupt a vault. Everything stays
plain Markdown, so anyone can read it with or without Claude.

**Can I control who sees what?** Not inside one vault. The
`confidentiality:` field is a **label** that marks content as internal or
restricted — it satisfies the marking duty for trade secrets, but it
locks nothing: whoever can open the folder can read every file in it.
Real separation means a second vault with its own repository and its own
access rights. Decide that before filling the vault, not after.

**Does the kit track who searched what?** No, and that is deliberate. A
record of who looked up what, and when, can be used to monitor
performance — in Austria and Germany such systems are regularly subject
to works-council co-determination. There is no search log, no per-person
statistic and no telemetry in this kit, and adding one would turn a
knowledge tool into a monitoring tool. (The optional unattended review
logs what *it changed in the vault*, never who read anything.) None of
this is legal advice — your legal contact or works council decides.

**Do colleagues have to know an AI maintains this vault?** Yes, and it
costs you one sentence: since August 2026 the EU AI Act's transparency
obligation applies inside companies too — people working with an AI
system must be able to tell. That's why `About this vault.md` says so in
its first lines and AI-drafted notes carry a `generated:` marker. Leave
both in place; that's the visible part of the obligation.

**Someone wants to contribute but can't release content.** That's what
`00-inbox/suggestions/` is for: everything in there is a proposal by
definition. The person named as release-authority in `About this
vault.md` turns it into `status: stable` with a filled `verified:` — the
weekly review empties that folder just like the inbox.

**Why are there no notes about people?** A shared vault describes roles,
not colleagues: `60-roles/` holds what a role is responsible for and
decides, never a dossier on a named employee. Personal notes about
people belong in a private brain — that's a data-protection line, not a
missing feature.

## Windows quirks

**Setting up on Windows — the two-minute version:** install Git for
Windows (default settings), stay on native Windows (skip WSL unless you
already live in it — Obsidian handles WSL paths badly), and after
installing Claude Code run `claude doctor`: it should list Git Bash. If
it doesn't, or anything below matches your symptom, read on.

**`claude` says "not recognized" although the install reported success?**
Re-run the install from CMD instead of PowerShell:
`curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`

**Setup hangs at `mkdir`/copy commands?** Almost always: Git for Windows
is missing, so Unix-style commands run in PowerShell where they're
invalid. Install [Git for Windows](https://git-scm.com/downloads/win)
(default settings), open a fresh terminal, restart `claude`. Check with
`claude doctor` — it should find Git Bash. Paths looking mangled
(`C:Userscl`)? Same cause, same fix.

**`python3` "not recognized"?** Windows Python usually ships `python`
and `py`, not `python3`. Tell Claude: *"python3 doesn't exist here, use
py -3"* — it will also fix the search command in your global CLAUDE.md
so future sessions use the right one.

**Using WSL and Obsidian can't open the vault (or is very slow)?**
Obsidian is a Windows app and handles `\\wsl$` paths badly — known
Obsidian limitation, not a kit bug. Put the vault on the Windows side
(`C:\Users\You\Brain` = `/mnt/c/Users/You/Brain` from WSL): Obsidian
opens it normally, and the speed difference is not noticeable at a few
hundred Markdown files.

## Capturing on the go (mobile)

Your vault lives locally and is versioned with Git — three honest ways
to feed it from your phone, each with a catch:

1. **Obsidian Sync** (easiest, ~$4/month): install the Obsidian app on
   your phone, enable Sync for the vault. The rule that keeps it safe:
   **Git on the desktop, Sync to the phone — never both on the same
   device against the same folder** (that's where corrupted-vault
   stories come from).
2. **Quick-capture shortcut into `00-inbox/`** (free, still needs a
   sync): an iOS Shortcut or Android automation that appends text to an
   inbox file — but the text only reaches your desktop via some sync
   (way 1, or iCloud with all its Git caveats). A typing shortcut, not a
   transport.
3. **Phone notes app + one capture** (free, zero setup, always works):
   jot or dictate into your normal notes app; back at the computer, one
   *"capture: [paste]"* to Claude. Costs you one manual step in the
   evening — and nothing else.

What we don't promise: real-time sync everywhere, zero-cost + zero-setup
at once, or running Git itself from the phone (possible via Working
Copy/MGit, but far more setup than this kit asks of anyone).
