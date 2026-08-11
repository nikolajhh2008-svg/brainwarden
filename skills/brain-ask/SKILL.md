---
name: brain-ask
description: Answer questions from the Brain with cited notes. Use when the user says "what does my brain know about …", "ask my brain", "what did I decide about …", "who is …", "what's the status of …", or when any question is about their own life, people, projects or past decisions.
---

# Brain ask (the librarian)

Chats evaporate — the brain doesn't. This skill answers questions from
the human's OWN notes, shows where every claim comes from, and is honest
about what the brain does not know.

**Conventions:** `<vault>` = the vault path from the `Brain vault:` line in
your global rules — **or, if there is no such line, the folder this
session was started in**, when that folder holds a `CLAUDE.md` naming a
vault mode. A shared company vault has no global line on purpose (its
skills travel inside it), so falling back to `~/Brain` there would write
into somebody's private vault. Only when neither exists does `~/Brain`
apply. `python3` = your working python
command (on most Windows machines `py -3`; the global rules name it).

## Steps
1. **Orient, then search wide:** Read `<vault>/index.md` first — the root
   signpost names the mode, the vault language, the folder map and the
   search tool, and unless this session started inside the vault you have
   none of that. (No `index.md`? Read `<vault>/CLAUDE.md` instead.) Then
   skim `<vault>/Home.md` (the living dashboard often frames the answer)
   and run `python3 <vault>/.tools/search.py <terms>` with 2–3 term
   variants (synonyms, the person's name, the project slug). Read ONLY the
   hits — never the whole vault.
2. **Answer from the notes**, in the vault language, citing every source
   note as a `[[link]]` so they can click into it in Obsidian. The notes'
   content outranks your general knowledge — if the vault and your
   training data disagree about the human's life, the vault wins.
3. **Decisions are special:** if the question touches a past decision,
   quote the decision record (`40-decisions/`) including its reasoning —
   that's exactly what the append-only log is for. A record marked
   `Superseded by …` is history: answer from the one that superseded it and
   name both.
4. **Two hits that contradict each other? Do not pick one.** Give both,
   with their dates, say which is newer and where each comes from — a
   moved date usually leaves the old one standing somewhere. Then offer to
   capture the correction. Answering confidently from one of two
   conflicting notes is the worst thing this skill can do: it sounds
   certain and sends the person to last month's appointment. A vault that
   contradicts itself is a finding, not a malfunction.
5. **Say what's missing, plainly:** "your brain has nothing on X" is a
   correct and useful answer — name the closest note you did find so they
   can judge the gap. Never fill gaps with invented vault content.
6. **Offer the next step** when a gap is researchable: "want me to
   research that and work it in?" (→ skill `brain-research`) — or capture
   the open question to the inbox if they answer it themselves on the spot.

## Rules
- Every claim in the answer must be traceable to a note or clearly
  labeled as NOT from the vault.
- In `company` mode (the vault `CLAUDE.md` names it) this is absolute:
  answer only from notes, cite the file path for every statement, and say
  "I don't know" rather than reason your way to a plausible number. Notes
  marked `status: draft` are proposals, not company truth — label them.
- Short questions get short answers — cite, don't lecture.
- Works from ANY session, whatever project is open.
