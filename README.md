# 🧠 Brainwarden

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made for Obsidian](https://img.shields.io/badge/Made%20for-Obsidian-7C3AED.svg)](https://obsidian.md)
[![Works with Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-D97706.svg)](https://claude.com/claude-code)
[![checks](https://github.com/nikolajhh2008-svg/brainwarden/actions/workflows/checks.yml/badge.svg)](https://github.com/nikolajhh2008-svg/brainwarden/actions/workflows/checks.yml)

![Brainwarden — an Obsidian vault Claude Code sets up and maintains](.github/assets/hero.jpg)

**The easiest way to start a second brain — you talk, Claude does the
maintenance.** An Obsidian vault and Claude Code working on the same
Markdown files: the setup asks you **three questions** and builds your
first real notes within minutes — your project, your deadlines, a living
`Home` dashboard. No empty vault, no taxonomy homework, no "now what?".

No plugins, no cloud service, no lock-in — just a folder of Markdown,
Git, and five small Claude skills.

## What actually happens

- **You say:** *"capture: dentist Thursday 3pm — and Lena recommended
  that sleep book"* → two inbox files appear instantly; Thursday lands in
  your [[Deadlines]] and on `Home`. At the weekly review the book becomes
  a one-line reference note (tagged, findable, not over-processed) and
  Lena's people note gets a line.
- **You drop a 40-page PDF** into `00-inbox/raw/` and say *"ingest"* →
  if it feeds your exam or project, it comes back as atomic, linked study
  notes; if it's just a manual, it becomes one findable reference note.
  Claude asks when unsure — and always reports what went where.
- **You ask:** *"what does my brain know about my thesis?"* → an answer
  built **only from your own notes**, every claim a clickable `[[link]]`,
  plus an honest "here's what your brain doesn't know yet."

## The one habit

You need exactly **one habit**: dump things into the brain — a sentence
to Claude, a file into the inbox. That's it. Filing, linking, deadline
tracking, weekly cleanup, remembering what you forgot: Claude's job, not
yours. Skip a few weeks? Nothing breaks — the next review catches up in
batches and welcomes you back without guilt. Second brains die of
maintenance debt; this one hands the maintenance to something that never
gets tired of it.

## Who this is for

- **Students** drowning in handouts, deadlines and exam dates — the brain
  becomes study sheets and a deadline memory.
- **Professionals & founders** juggling projects, people and decisions —
  the brain becomes project plans, drafts and an append-only decision log.
- **Anyone using Claude Code** who wants their AI to actually *know* them
  across sessions — not start from zero every conversation.
- **Obsidian-curious beginners** who never got past the empty vault: the
  setup fills it in minutes, and the review keeps it alive.

You need [Obsidian](https://obsidian.md) (free), a Claude subscription
and ~20 minutes from nothing installed to a populated brain (plus an
optional 10–15-minute interview that makes the brain really know you).
You do NOT need to know Markdown, Git, PARA or Zettelkasten — that's
Claude's job.

## Who this is NOT for

Honesty saves everyone time:

- If **tags + search + relaxed standards** already keep your vault alive,
  you don't need this. This is for people for whom the maintenance habit
  — not the tooling — was the thing that failed.
- If you want an AI to **write your thinking for you** — this kit
  deliberately keeps the notes in *your* words. Claude files, links,
  reminds and researches; it doesn't replace your head.
- If you want **maximum features** — this kit is deliberately small
  (five skills, one search script). There are 40-command kits out there;
  this isn't one, on purpose.

## How it works

```mermaid
flowchart LR
    A["💭 thought<br/>(&quot;capture: …&quot;)"] --> B["00-inbox/"]
    C["📄 PDF / transcript"] --> D["00-inbox/raw/"]
    B --> E{"weekly<br/>&quot;brain review&quot;"}
    D --> F{"&quot;ingest&quot;"}
    E --> G["atomic, linked notes<br/>(knowledge · people · projects)"]
    F --> G
    G --> H["🎯 output<br/>study sheets · drafts · decisions"]
    G --> I["💬 cited answers<br/>(&quot;what do I know about …?&quot;)"]
    G --> J["❓ open questions"]
    J -- "&quot;research my brain&quot;" --> G
```

Five verbs, nothing more: **capture** (anytime, formless) · **ingest**
(feed it sources) · **ask** (answers from your own notes, cited) ·
**review** (weekly, inbox to zero — including a sweep of what the week
produced but nobody captured, a contradiction check against your past
decisions, connections nobody thought to search for, and deepening 2–3
thin notes toward `evergreen`) · **research** (Claude fills your open
questions with verified, sourced facts).

## Quickstart

Prerequisites: [Obsidian](https://obsidian.md) (free) and
[Claude Code](https://claude.com/claude-code).

Open Claude Code (`claude` in your terminal) and say **one sentence**:

> Set up the second brain from this GitHub repo for me:
> https://github.com/nikolajhh2008-svg/brainwarden — clone it and
> follow SETUP-FOR-CLAUDE.md step by step.

Claude clones the kit itself, checks your prerequisites, asks three
questions — and minutes later you open Obsidian to a brain that already
contains your first project, your deadlines and a living `Home` page.
The deep onboarding interview comes after that first win, and only if
you want it.

## Pick your path

- **Never used Obsidian or Claude Code?** → **[TUTORIAL.md](TUTORIAL.md)**
  — zero to a running brain, with a checkpoint after every stage.
- **Terminal not your thing?** Two graphical ways, same Quickstart
  sentence pasted there instead:
  [Claudian](https://github.com/YishenTu/claudian) puts Claude Code
  directly **inside Obsidian** (install from Community Plugins; desktop
  only, needs the Claude Code CLI installed once) — you chat right next
  to your notes. Honest heads-up: its default permission mode gives the
  agent broad rights without asking; for a vault of personal notes,
  switch to a stricter mode in its settings first. Alternative: the
  [Claude Code extension for VS Code](https://code.claude.com/docs/en/vs-code)
  — a chat panel, no command line.
- **Comfortable with Claude Code?** The fast lane:
  ```bash
  git clone https://github.com/nikolajhh2008-svg/brainwarden
  cd brainwarden && claude "follow SETUP-FOR-CLAUDE.md step by step"
  ```
- **Already have a vault and just want the five skills?**
  ```
  /plugin marketplace add nikolajhh2008-svg/brainwarden
  /plugin install brainwarden@brainwarden
  ```
  Skills only — they expect the kit's core folders at `~/Brain`; if your
  vault differs, the full setup's adopt path maps it first.
- **Just browsing?** → [`examples/`](examples/) shows what finished notes
  look like, readable right here on GitHub. Nothing to install.

Stuck anywhere? → [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Two guides — one for you, one for your AI

| For | File | What it is |
|---|---|---|
| 🧑 **Human** | [TUTORIAL.md](TUTORIAL.md) | Zero to running brain, with checkpoints |
| 🤖 **Claude** | [SETUP-FOR-CLAUDE.md](SETUP-FOR-CLAUDE.md) | The machine-readable setup runbook — **the repo is the installer** |

You only hand Claude the repo link — it clones, asks, adapts, installs.

## What the setup creates for you

- `~/Brain` with a flat, PARA-inspired base (inbox → projects → areas →
  knowledge → decisions → archive)
- **Your first project and your areas — before any interview.** Claude
  derives them from three answers and names the folders in your words (a
  student gets different areas than a founder)
- **`Home.md`** — a living dashboard Claude keeps current: active
  projects, next deadlines, open questions, what's new this week
- **Your language** — the repo is English; your brain's content can live
  in German or any language you pick during setup
- Five installed skills (capture / ingest / ask / review / research) +
  global rules so **every** future Claude session knows your brain —
  whatever project is open
- Optionally, the **onboarding interview** afterwards (10–15 min): people
  notes, self-image, goals — pre-fillable by a consent-gated scan of your
  own computer ("may I look around to fill this in?")

## Customizing (the numbering is expansion space)

The folder numbers have deliberate gaps: `00` inbox → `10` projects →
`20` areas → `30` knowledge → `40` decisions → … → `90` archive. The gap
between 40 and 90 is **reserved for your modules** — during setup (or any
time later) Claude offers opt-in extras that slot right in:

- `50-journal/` — daily/weekly journaling
- `60-media/` — reading & watch log
- `70-health/` — training, habits, metrics
- `80-money/` — budgets & financial decisions
- …or anything you name yourself

**Fixed** (skills depend on it): the six core folder names and the number
prefixes. **Free:** everything else — area names in your words, your
modules, your language, which templates you keep. Adding a module later
is one sentence: *"add a journal module to my brain."* Already have a
vault? The setup **adopts** your structure instead of overwriting it
(worst case it quarantines your old notes untouched in `OLD_VAULT/` —
never deleted, never restructured without your OK).

## What's inside

| Path | Contents |
|---|---|
| [`vault-template/`](vault-template/) | The complete vault: folder schema, rules ([CLAUDE.md](vault-template/CLAUDE.md)), `Home` dashboard, templates, deterministic search tool |
| [`skills/`](skills/) | The five skills: `brain-capture` · `brain-ingest` · `brain-ask` · `brain-review` · `brain-research` |
| [`SETUP-FOR-CLAUDE.md`](SETUP-FOR-CLAUDE.md) | Step-by-step setup that Claude executes itself |
| [`INTERVIEW.md`](INTERVIEW.md) | The optional onboarding interview (7 blocks, 22 questions) |
| [`examples/`](examples/) | Style models (reference only — never copied into your vault) |
| [`PHILOSOPHY.md`](PHILOSOPHY.md) | Why it's built this way: how second brains die, and the design answers |

**Why so small?** Five skills and one Python file is the product, not a
limitation. Every extra command is one more thing a beginner has to
learn, trust and remember — and the maintenance promise only holds if
the system itself needs none.

## Principles

- **The first win comes before the first chore** — the setup builds real
  notes from three answers; nobody meets an empty vault.
- **Atomic** — one idea = one note; people get individual notes; link everything.
- **Triage** — reference material gets tags and a home; only build
  material gets the full atomic treatment. Organizing effort must never
  exceed the value of what's organized.
- **File by actionability** — "which project/area needs this now?", never
  by topic taxonomy. Findability comes from links and search, not folder depth.
- **Zero-friction capture** — "capture: …" is enough; structure happens at
  review time, not capture time.
- **Processing duty** — the inbox goes to **zero** at every review
  (second brains die of full inboxes, not missing features).
- **The brain shows its work** — every filing decision is reported, every
  change is a Git commit away from undo. No silent auto-capture.
- **The success metric is output** — texts, decisions, study sheets;
  never note count.
- **Append-only decisions** — decision records never get rewritten.
- **Deterministic search first** — `search.py` finds the relevant notes;
  Claude reads hits, not the whole vault (saves context). And what search
  can't find — the things you forgot to ask — the weekly review surfaces.

## Privacy

Everything lives on your machine: your notes in `~/Brain` (yours,
Git-versioned), the five skills in `~/.claude/skills/`, one opt-in block
in `~/.claude/CLAUDE.md`. The kit itself makes no network calls and has
no telemetry. What Claude sends to Anthropic while working is governed
by your own Claude Code settings — not by this kit. Web research and the
setup's computer scan only ever run with your explicit consent, and the
full uninstall is three deletions ([SECURITY.md](SECURITY.md)).

## Contributing

Issues and pull requests welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
Changes: [CHANGELOG.md](CHANGELOG.md)

## License

[MIT](LICENSE) — take it, remix it, pass it on.

---

*Distilled from a real setup used daily: 100+ notes lived in first,
then reduced to a template. The reasoning behind every design choice:
[PHILOSOPHY.md](PHILOSOPHY.md).*
