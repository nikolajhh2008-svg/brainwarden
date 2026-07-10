---
name: brain-ask
description: Answer questions from the Brain (~/Brain) with cited notes. Use when the user says "what does my brain know about …", "ask my brain", "what did I decide about …", "who is …", "what's the status of …", or when any question is about their own life, people, projects or past decisions.
---

# Brain ask (the librarian)

Chats evaporate — the brain doesn't. This skill answers questions from
the human's OWN notes, shows where every claim comes from, and is honest
about what the brain does not know.

## Steps
1. **Prime, then search wide:** skim `~/Brain/Home.md` first (the living
   dashboard — it often already frames the answer). Then
   `python3 ~/Brain/.tools/search.py <terms>` with 2–3 term variants
   (synonyms, the person's name, the project slug) and read ONLY the
   hits — never the whole vault.
2. **Answer from the notes**, in the vault language, citing every source
   note as a `[[link]]` so they can click into it in Obsidian. The notes'
   content outranks your general knowledge — if the vault and your
   training data disagree about the human's life, the vault wins.
3. **Decisions are special:** if the question touches a past decision,
   quote the decision record (`40-decisions/`) including its reasoning —
   that's exactly what the append-only log is for.
4. **Say what's missing, plainly:** "your brain has nothing on X" is a
   correct and useful answer. Never fill gaps with invented vault content.
5. **Offer the next step** when a gap is researchable: "want me to
   research that and work it in?" (→ skill `brain-research`) — or capture
   the open question to the inbox if they answer it themselves on the spot.

## Rules
- Every claim in the answer must be traceable to a note or clearly
  labeled as NOT from the vault.
- Short questions get short answers — cite, don't lecture.
- Works from ANY session, whatever project is open.
