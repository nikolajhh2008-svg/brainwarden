---
name: brain-review
description: Weekly review of the Brain (~/Brain) — inbox to zero, surface open loops, archive stale items. Use on "brain review", "clean up my brain", "what's in the inbox", ideally on a fixed weekday.
---

# Brain review (5–10 minutes, weekly)

Keeps the brain alive — the #1 killer of second brains is an inbox nobody
empties.

## Steps
1. **Inbox to ZERO** (hard rule): PROCESS every file in `~/Brain/00-inbox/`
   (except `Inbox rule.md`) — never just move it:
   - paraphrase into a proper note (frontmatter, vault language, matching
     template from `_templates/` — knowledge-note / project-note /
     area-note / person-note; fill `{{DATE}}` with the real date) and file
     by ACTIONABILITY: project → `10-projects/…` · area → `20-areas/…` ·
     keeper knowledge → `30-knowledge/…` · person → `30-knowledge/people/`
   - **dedup first:** `python3 ~/Brain/.tools/search.py <name/topic>` —
     extend an existing note rather than creating a twin
   - or delete it (say so — deleting is a feature).
   **More than ~20 inbox files?** Work in prioritized batches (deadlines →
   decisions → people → rest) and report what remains — never half-process
   silently.
2. **Sweep the week (the safety net):** captures are best-effort — the
   review is the guarantee. Look at what the week ACTUALLY produced and
   compare it against the brain: recently modified files in their project
   folders, `git log` of active repos, and session context if available.
   Decisions, deadlines, people or milestones that never got captured →
   into the inbox now, then process them like everything else.
3. **Deadlines:** new dates from the week → `Deadlines.md`; past dates out.
4. **Open loops:** list 3–5 things that look stalled (projects without
   recent notes, "open → ask" markers) and ask about them — and offer:
   "want me to research the researchable ones?" (→ skill `brain-research`).
5. **Hygiene:** orphan notes (no inbound links), dead `[[links]]`, empty
   files — fix or report.
6. **Structure check (quarterly-ish):** if an area/folder no longer matches
   the person's life, propose renaming/archiving it. The onboarding interview
   was a starting point, not a cage.
7. **Commit:** `cd ~/Brain && git add -A && git commit -m "review YYYY-MM-DD"`.
8. Report: what was filed where, what was deleted, what needs their input.

## Rules
- Never let the inbox survive a review.
- Archive beats delete for finished projects; delete beats archive for noise.
