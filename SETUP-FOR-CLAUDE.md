# Setup runbook (for Claude Code — work through step by step)

You are setting up a "second brain" for your human: an Obsidian vault that
you read and maintain in every session. This kit contains ONLY structure —
no one else's content.

## Step 0 — You are the guide
The human may not know this kit, Obsidian, or Git. **You drive:**
- Given only the repo URL? Clone it yourself first:
  `git clone https://github.com/nikolajhh2008-svg/brainwarden.git`
- Check ALL prerequisites before starting: **Obsidian** installed (if
  not: obsidian.md, wait), **git** available (`git --version`; if missing,
  guide the install — on macOS `xcode-select --install`), git identity set
  (`git config user.name` — if empty, set a name/email with their OK, or
  they hit "Please tell me who you are" at the first commit), and
  **python3** available (`python3 --version`; on Windows try `py`). No
  git? The setup still works — skip the clone (download the ZIP) and the
  commit steps, and say so.
- Explain each step in ONE sentence before doing it.
- Ask before touching `~/.claude/CLAUDE.md` (step 4).
- **Already have a vault?** Skip the template: scan their existing folder
  structure instead, map it onto the rules (inbox? projects? areas?) and
  only add what's missing. Adopt, don't overwrite.

## Step 1 — Create the vault
**First check whether `~/Brain` already exists.** If it does: STOP and
ask — adopt it (Step 0), merge into it, or let them pick another path.
Never copy over an existing folder unasked.

Fresh install: `mkdir -p ~/Brain && cp -R vault-template/. ~/Brain/`
(note the `/.` — it copies contents incl. hidden `.tools/`, no nesting).
Verify: `~/Brain/CLAUDE.md` and `~/Brain/.tools/search.py` exist. You may
delete the cloned repo folder after setup — mention it.

## Step 2 — Install the skills
Check for name collisions first: if `~/.claude/skills/brain-capture`
(or -ingest / -review / -research) already exists, STOP and ask — never overwrite an
existing skill silently. Then `mkdir -p ~/.claude/skills` and copy the
four folders from `claude-skills/` into it.
Loading note: if `~/.claude/skills/` already existed, new skills load
live in the current session; if the directory was just created, one
restart of Claude Code is needed before the first "capture:".

## Step 3 — Adapt the structure to the human (the most important step)

### 3a. Four questions, then you do the heavy lifting
1. **What's your life right now?** (school / university / job / own
   business / mix — free text is fine)
2. **Which 2–4 areas do you carry long-term?** (health, money, family,
   learning & career … — use THEIR words)
3. **What should this brain produce in the first two weeks?** (an exam
   prep, a project plan, an application … — becomes the first project)
4. **Which language should your brain live in?** (the repo is English;
   the vault content can be German, English, anything)

Then: create their areas as subfolders in `20-areas/` (seed each with a
note from `_templates/area-note.md`), the first project in `10-projects/`
(seeded from `_templates/project-note.md`), personalize `Start here.md`
with those links, set `{{LANGUAGE}}` in `~/Brain/CLAUDE.md` — and if the
language is not English, translate `Start here.md`, `Inbox rule.md`,
`About me.md`, `Deadlines.md` and the `_templates/` into it. The vault's
`CLAUDE.md` stays English by design (it is read by Claude, not by them). Never ask about PARA/Zettelkasten by name — you translate
answers into structure; methods are your job, not theirs.

### 3b. Offer the optional modules (opt-in menu, create ONLY what they pick)
Present this list in one short message; each pick becomes a numbered
top-level folder — **the gaps in the numbering (50–80) exist exactly for
this**:
- **`50-journal/`** — daily/weekly journaling (template ships with the
  kit: `_templates/journal-entry.md`; add a "journal" line to Start here)
- **`60-media/`** — reading/watch log (books, papers, videos with one-line
  verdicts)
- **`70-health/`** or **`70-training/`** — workouts, habits, metrics
- **`80-money/`** — budgets, subscriptions, financial decisions
- or anything they name themselves — their word, their folder

Rules for modules: numbered top-level folder, one intro note inside,
linked from `Start here.md`. Skippers lose nothing — modules can be added
any time later by just asking Claude ("add a journal module to my brain").

### 3c. What is fixed vs. free (tell them this!)
- **Fixed (the skills depend on it):** English top-level folder names for
  `00-inbox`, `10-projects`, `20-areas`, `30-knowledge`, `40-decisions`,
  `90-archive` — and the numbered-prefix scheme.
- **Free:** everything else — area names, module folders (50–80), all
  content language, templates (delete what they won't use), even the
  weekly review day.

### 3d. Fill in placeholders
Ask for their first name. Replace `{{NAME}}` in
`~/Brain/40-decisions/_template.md`, `{{LANGUAGE}}` in `~/Brain/CLAUDE.md`,
and `{{DATE}}` in `About me.md` + `Deadlines.md` with today's date.
**Leave `_templates/` untouched** — their `{{DATE}}`/`{{NAME}}`
placeholders are filled per note, at creation time, forever.

## Step 4 — Global rules
With their OK, add to `~/.claude/CLAUDE.md` (create if missing):

```markdown
## Brain (~/Brain — Obsidian vault + Claude working directory)
- Retrieval: run `python3 ~/Brain/.tools/search.py <terms>` first, then
  read only the hits — never the whole vault.
- Capture triggers: whenever a session produces (a) a decision, (b) a
  deadline, (c) a milestone, (d) a new person, (e) a hard-won lesson →
  file it to ~/Brain/00-inbox/ immediately (brain-capture).
- Weekly ritual: "brain review" (inbox to zero, hygiene, git commit).
```

## Step 5 — Git + the first interview
1. `cd ~/Brain && git init && git add -A && git commit -m "brain setup"`
2. Run the **onboarding interview** — questions, processing rules AND the
   consent-gated local-discovery phase live in `INTERVIEW.md` (this kit).
   Start with its Phase-0 consent question (may Claude scan the computer
   to pre-fill?), then interview with the per-block nudges. Style models:
   `examples/`. Conduct it in the vault language. This is what makes the
   brain valuable — do not shorten it.

## Step 6 — Verify, then hand over
Run this checklist and show the results (fix anything that fails):
- [ ] `ls ~/Brain` shows `00-inbox` … `90-archive` + their modules
- [ ] `python3 ~/Brain/.tools/search.py test` runs without error
- [ ] `ls ~/.claude/skills/` shows the four brain-* skills
- [ ] `grep Brain ~/.claude/CLAUDE.md` shows the rules from step 4
- [ ] `cd ~/Brain && git log --oneline` shows the setup commit
- [ ] No setup placeholders left OUTSIDE the templates:
      `grep -rnE "\{\{(NAME|LANGUAGE|DATE)\}\}" ~/Brain --exclude-dir=_templates | grep -v "_template.md"`
      (templates keep their placeholders on purpose — never "fix" them)

If anything above fails mid-setup and can't be fixed: a fresh install
may simply be removed (`rm -rf ~/Brain`) and restarted — say so instead
of leaving a half-built vault. Then show them how to point Obsidian at
the vault ("Open folder as vault" → `~/Brain`) and demo the three
habits (capture / ingest / review) and the power move: research.
Finish with one sentence on how to extend later: "Ask me to add a module,
rename an area, or change the language — the structure grows with you."
