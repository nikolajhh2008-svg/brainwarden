# The onboarding interview (for Claude: offered in the setup's interview step — or whenever the human says "interview me for my brain")

Goal: after this conversation the brain knows its subject — the human in a
private or work brain, the company in a shared one. The interview is
**optional and deferrable** — the brain already works without it; this is
the deepening. Two phases: an optional **local discovery** (with explicit
consent), then the **interview** — which works far better once you have
something concrete to ask about. It also works in pieces: a block now, a
block next week.

**This file is a script, not a note.** After setup it lives at
`<vault>/.tools/INTERVIEW.md`. It is never part of the vault's content: it
gets no frontmatter, it is excluded from search, and nothing in it is ever
"filled in" — the setup's placeholder check skips `.tools/` for exactly
that reason. If a check ever flags this file, fix the check, not the file.

## Which track — decide this before the first question

Read the mode, in this order — the first one that answers wins:

1. the `Mode:` line in the global rules block, if there is one
2. `**Vault mode: …**` in the vault's own `CLAUDE.md` — this is the reliable
   one, because a shared company vault has no global rules block at all
3. the root `index.md`

The LABEL may be translated (`Betriebsart:`, `Modus:`); the VALUE never is —
it is always `personal`, `professional` or `company`. Key off the value.
Found nothing? Ask, in one sentence, and write the answer into the vault's
`CLAUDE.md` so nobody has to ask twice. Then:

| Mode | Track | What the interview is about |
|---|---|---|
| `personal` | **A**, all blocks | the human and their life |
| `professional` | **A**, work blocks only | the human's working knowledge |
| `company` | **B** | the company's processes, roles and terms |

In a `professional` vault, skip everything private: no family, no hobbies,
no health, no private plans. That vault exists precisely so those things
stay in the other one — if something private comes up anyway, offer to put
it in their personal brain instead.

In a `company` vault a personal deep interview is simply the wrong
instrument: a shared vault holds how the company works, not who someone
is. Track B never asks about a person's life, and it records roles rather
than people.

## Phase 0 — Ask THIS first (verbatim, before any question)

**Track A (`personal` / `professional`):**

> "Before the interview: may I look around this computer — folders like
> Documents and your projects, and my own past sessions with you — to
> pre-fill your brain with what I find? I'll list everything I looked at,
> nothing leaves this machine, and you can veto any note. Yes or no is
> both fine — the interview works either way."

**If yes:** spend a few minutes scanning what the permissions allow —
`~/Documents`, `~/Desktop`, project folders, git repos (authors, README
names), and prior Claude session context if available. Extract people,
projects, deadlines, interests, tools. Then:
- pre-fill draft notes, each marked in its frontmatter as
  `source: local discovery` with today's real date,
- open the interview with what you found: **"I saw X — tell me about
  it"** beats every generic question,
- report the list of locations you touched, and delete anything they veto.

**If no:** skip silently, never mention it again.

**Track B (`company`) — stricter, and the default is no.** A work machine
holds other people's data; a broad scan would sweep it into a vault
several colleagues can read. Ask instead:

> "Is there a specific folder with process descriptions, checklists or
> handbooks I should look at — one you're allowed to share with the team?
> If not, we'll do it entirely by conversation."

Only ever read the folder they name, never mailboxes, never personal
folders of colleagues, and report every file you used.

## How to interview (people don't know what to say — help them)

Ask **block by block**, voice dumps welcome, any order, skipping allowed.
The golden rule: **never leave a thin answer thin.** When someone says
"hmm, not much" — give them three concrete options to react to (the
per-block nudges below), name examples, ask for names/dates/numbers.
React to what they said before moving on ("you mentioned a brother —
what's his name?"). Decompose everything into ATOMIC notes afterwards:
**one idea = one note**, everything linked. Invent nothing; mark gaps as
"open → ask later". If they say "private": don't write it down, don't
probe.

---

# Track A — the human (`personal`, and `professional` where marked)

**In a `professional` vault, Block 4 is the interview.** Start there, then
pick up 2, 3, 5, 6, 7, 8 in their trimmed form — and ask nothing twice:
Block 1 stays at role and employer, the *content* of the work belongs to
Block 4 alone.

## Block 1 — You at a glance *(personal: both questions · professional: question 1, short)*
1. Who are you in three sentences — name, age, where you live, what you
   mainly do right now (school / university / job / your own thing)?
   *(professional: your role and where you work — one sentence. Do NOT
   ask what the work consists of here; that is Block 4, and asking it
   twice is how an interview loses people.)*
2. How would you describe yourself — and which part would others
   instantly confirm? *(personal only — a work vault does not need a
   self-portrait; how they work comes up in Block 7.)*
   *Nudge if stuck: night owl or early bird? builder or planner?
   starts things or finishes things?*

## Block 2 — Your people *(personal: everyone · professional: work only)*
3. Who counts as family, and who actually plays a role in your daily
   life (who lives where, with whom)? *(personal only)*
4. Who are your closest friends — names plus one line each?
   *(personal only)*
5. Which people matter at school/university/work (mentor, boss, teacher,
   business partner)?
   *Nudge: who would you call first with a problem? who do you learn
   the most from? anyone you actively avoid?*

## Block 3 — Everyday life & obligations *(personal · professional: work week)*
6. What does a normal week look like — what's fixed, what's flexible?
7. Which dates, deadlines or exams are coming in the next 3 months?
   (Everything counts, official stuff too — the brain becomes your
   deadline memory.)
   *Nudge: exams · applications · renewals/contracts · trips · family
   dates · anything governmental (license, service, visa, taxes).*
   *(professional: submissions, reviews, audits, contract dates.)*
8. Which ongoing duties are you carrying — and which are you pushing
   ahead of you?

## Block 4 — Zoom in: your work or your studies (adaptive) *(both — and the core block in a professional vault)*
This block is where the brain earns its keep: knowing someone's actual
tasks — not their title — is what later lets it take work off their
plate. **Narrow down first, then go deep.**
- `personal`: ask which applies (studying / working / both) and follow
  only the fitting branch; both if both.
- `professional`: take the "If working" branch without asking — a work
  vault has already answered that question. The "If studying" branch
  never applies there; if they also study, that belongs in their
  personal brain.

**If working:**
- What exactly is your job — what does the work consist of, concretely?
  *Nudge: not the title, the activities. "I check price lists, answer
  customer mails, prepare orders" beats "sales".*
- Which tasks come back every single week?
  *Nudge: reports? invoices? stock checks? the same three mails? List
  them — recurring work is the most valuable thing this block collects.*
- Where does most of your time actually go — and which part of that
  annoys you the most?
- Which programs or tools do you work in daily — and which one fights
  you the most?
- Who do you work with most closely (names, roles)?

**If studying (school or university):**
- Where are you (school/university, which year) — and what's the big
  goal right now (final exams, degree, a specific grade)?
- Which subjects or courses demand the most from you right now?
- What eats most of your learning time?
  *Nudge: summarizing? memorizing? writing? procrastinating one
  specific subject?*
- Which exams, submissions or presentations are coming up — with dates?
- Which apps or tools do you use for school — notes, flashcards,
  calendar?

## Block 5 — Projects & goals *(both — professional: work projects only)*
9. What are you actually working on right now (work, school, personal) —
   and which of these projects is closest to your heart?
   *Nudge: also the unofficial stuff — a side project, something you
   build/learn at night, something you promised someone.*
10. What should be different 12 months from now?
11. The bigger picture: where do you want to be in ~5 years — which part
    is a dream, which is already a plan?

## Block 6 — Knowledge & interests *(personal · professional: expertise only)*
12. What are you genuinely good at — what do people come to you for?
13. What do you want to learn next?
    *Nudge: a skill for work/school · a language · a tool (AI? coding?) ·
    something physical (sport, instrument, license)?*
14. What do you consume regularly and gladly (books, podcasts, channels,
    creators) — and which of it actually shapes your thinking?
    *(professional: trade press, standards, communities.)*
15. Which hobbies do you REALLY do regularly — and which only exist on
    paper? *(personal only)*
    *Nudge: what did you actually do last weekend? what would friends
    say you always talk about?*

## Block 7 — Working style & energy *(both)*
16. When during the day are you most productive, and what does your real
    (not ideal) sleep/energy rhythm look like?
17. How do you learn/work best — honestly, as it is?
18. What currently eats most of your time or nerves?
    *Nudge: a duty? a person? commuting? your phone? something you keep
    postponing?*
19. What should Claude do more often in your collaboration — and less?

## Block 8 — Closing *(both)*
20. What do you have genuine respect for in the coming year?
21. What else should your brain absolutely know that I didn't ask about?
22. Are there areas that stay fundamentally "private"? (I'll create a
    no-go note so future sessions respect it too.)

## After Track A (mandatory processing)
- Merge the interview with any Phase-0 discovery drafts (interview wins
  on conflicts — the human's words beat file traces)
- People individually into `30-knowledge/people/` (template:
  `_templates/person-note.md`) · facts/principles/goals as atomic notes
  into `30-knowledge/` or `10-projects/` (templates: `knowledge-note.md`,
  `project-note.md`; fill the templates' date and name placeholders with
  real values) — search before creating to avoid twins
- Recurring tasks from the zoom-in block: in a `personal` vault one note
  per area (`20-areas/`); in a `professional` vault one process note per
  recurring task (`50-processes/`) — trigger, steps, owner, what usually
  goes wrong. That is the raw material for everything an assistant can
  later take off their plate.
- Dates into `Deadlines.md` (one line per date, date first) · self-image
  into `About me.md` (as a hub with links, including a "remaining gaps"
  list) — keep the `**Name:**` line from setup at the top
- Frontmatter: `maturity:` only on notes in `30-knowledge/`; from a
  `professional` vault upwards every note outside the inbox also carries
  `status: draft | stable | deprecated`
- Refresh `Home.md` — new projects/deadlines/open questions from the
  interview belong on the dashboard immediately; replace only what sits
  between the `<!-- block:… -->` marker pairs and never delete a
  `<!-- keep:… -->` line — and update the `index.md` entry points of
  every folder you filled
- Link everything, `git commit`
- Ask 3–5 follow-up questions about the biggest gaps

---

# Track B — the company (`company`)

Same rules (block by block, never leave a thin answer thin, invent
nothing), different subject. You are mapping how the company works so a
new colleague — or an agent — can find their way without asking a person.
Interview whoever knows the area; several short sessions with different
people beat one long one. Record **roles, not personal profiles**: "the
person who does the invoicing" becomes `60-roles/invoicing.md`, never a
dossier on a colleague.

## Block C1 — The company at a glance
1. What does the company do, for whom — in three sentences a new
   colleague would understand?
2. How big is it, and which areas exist (the answer from setup — confirm
   and complete it)?
3. What goes wrong most often when someone new starts — what do people
   have to explain over and over?
   *Nudge: that answer is usually the second SOP you should write.*

## Block C2 — The processes (the heart of this track)
Go area by area. For EACH process, collect exactly these five things —
without them a note is decoration:
4. What is it called internally, and what triggers it? (a customer mail,
   a date, an order, month-end …)
5. What happens then — 3 to 7 steps, in the company's own words?
6. Who owns it, and who has to be involved?
7. What typically goes wrong, and what does one do then?
8. Which tools or systems are involved (and where do their files live)?
   *Nudge if stuck: walk me through the last real case, from the first
   mail to the moment it was done.*

## Block C3 — The questions that keep coming back
The cheapest wins in a company vault: every question answered twice is a
note that was missing.
9. Which questions do customers ask again and again — and what is the
   answer you always give?
   *Nudge: ask them to open the last few mails or messages; the same
   three questions are usually right there.*
10. Which questions do colleagues ask each other over and over?
    *Nudge: "how do I do X again?" · "who is responsible for Y?" ·
    "where do I find Z?"*
11. Which of these answers differ depending on who you ask? (Those come
    first — a contradiction in the company is worth more written down
    than ten uncontested notes.)

## Block C4 — What only lives in one head
The point of a shared vault. Ask it plainly, without blame — this is
about the company's resilience, never about judging a person.
12. If one person were out for four weeks — what would stall, and what
    would nobody know how to do?
13. Who is the only one who can do a particular thing (a system, a
    customer, a machine, a supplier relationship)?
14. Which knowledge exists only as experience — "you just know that after
    two years"? Which of it can be written down, and which really cannot?
    *Nudge: exceptions and special cases ("customer X always gets …",
    "with supplier Y you have to …") are exactly this kind of knowledge.*
    *Anything named here becomes an SOP or a knowledge note — and if the
    person is not available today, an open question on `Home`.*

## Block C5 — Roles and responsibilities
15. Which roles exist — who decides what?
16. Which decisions may be made alone, and which need approval by whom?
17. Which role owns which of the processes from C2?
    *(Role names, not people. If a role currently has exactly one person,
    that is fine — the note still describes the role.)*

## Block C6 — Language and terms
18. Which words does the company use that an outsider would misread?
    (product names, abbreviations, internal shorthand, customer
    categories)
19. Are there terms used differently in two areas? (Those are the ones
    that cause the most expensive misunderstandings.)
    *This block becomes a glossary in `30-knowledge/` — one note per
    term, so an agent searching for the word actually lands on the
    meaning.*

## Block C7 — Partners and suppliers
20. Which suppliers, service providers or partners matter — for what?
21. Who is the contact for each, and which agreements/deadlines exist
    (contracts, renewals, notice periods)?

## Block C8 — Onboarding
22. What does someone new need in their first week — in which order?
23. Which three documents or explanations would you hand them first?

## Block C9 — Rules, approval and confidentiality
24. Who says "this version is now official"? (confirm the setup answer)
25. How often should content be reviewed — is there a rhythm per area?
26. Which content is confidential, and towards whom?
    Repeat the honest limit once: a `confidentiality:` field is a
    **label**, not a lock — everyone with access to the folder can read
    everything in it. Content that must be genuinely unreadable for part
    of the team belongs in a separate vault.
27. Which fixed dates does the company have to hit (audits, inventory,
    reporting, contract dates)?

## After Track B (mandatory processing)
- One process = one note in `50-processes/` (`_templates/sop-note.md`):
  purpose, trigger, steps, owner, what goes wrong, tools — search first,
  extend instead of duplicating
- One role = one note in `60-roles/` (`_templates/role-note.md`):
  responsibility, owned processes, decision rights — never a personal
  dossier; there is no `people/` folder in this vault
- The recurring answers from C3 and the head-only knowledge from C4:
  whichever is a procedure becomes an SOP, everything else an atomic
  note in `30-knowledge/`. Where two people answered differently, write
  ONE note, name the contradiction in it, and put the decision question
  on `Home` — never two competing notes.
- Terms from C6 as atomic notes in `30-knowledge/`, one per term,
  cross-linked where two areas use a word differently
- Partners from C7 into `80-partners/` (`_templates/partner-note.md`),
  one per partner, with the contract dates mirrored into `Deadlines.md`
- The onboarding path from C8 into
  `70-onboarding/onboarding-path.md` (`_templates/onboarding-plan.md`):
  a short ordered route with real relative links to the SOPs, not a wall
  of text
- Decisions that came up during the interview ("we decided in March to
  stop doing X") into `40-decisions/` as dated records
- Frontmatter on EVERY note: base schema + `status:` + `owner:`,
  `audience:`, `confidentiality:`, `review_due:` (default 12 months).
  Anything you drafted also carries `generated: {by: …, at: …}` — that is
  the transparency marker from the setup, not decoration. `verified:` is
  never yours to fill; that field belongs to the human who confirms it.
- Anything unapproved stays `status: draft` until the person named in C9
  confirms it — a company brain publishes after approval, not on write.
  Interviewed someone without release rights? Their material goes to
  `00-inbox/suggestions/` and stays a proposal until it is released.
- Refresh `Home.md` (only between the `<!-- block:… -->` marker pairs)
  and the `index.md` entry points of every folder you filled, then
  `git commit`
- Ask 3–5 follow-up questions about the biggest gaps, and name the areas
  that still have no process note at all
