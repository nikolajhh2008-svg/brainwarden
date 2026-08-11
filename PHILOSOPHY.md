# Why this kit works (and why second brains usually die)

The design isn't taste — it's built against the documented ways personal
knowledge systems fail; most are abandoned within months, and the causes
repeat. If you know the reasoning, you can bend every rule intelligently.

## The four causes of death

**1. Capture friction.** If saving a thought takes more than a moment,
you stop saving thoughts. Complex capture flows cost "30 seconds to
2 minutes" per entry, which quietly kills the habit.
→ *Kit answer:* one inbox, one phrase ("capture: …"), zero required
metadata. Structure is applied later, by Claude, not by you at 11 pm.

**2. Over-engineering.** The classic arc: initial excitement → elaborate
folder taxonomy → maintaining the system costs more than it returns →
abandoned. Tiago Forte's warning: *"if your organizational system is as
complex as your life, maintaining it will rob you of the time and energy
you need to live that life."*
→ *Kit answer:* six flat folders in a private brain, eight at most in a
company one, filing by **actionability** (which project or area needs
this now?) instead of topic trees — and the sorting itself is delegated
to the weekly review, which Claude runs.

**3. Collecting without using** (the "digital attic"). Notes go in,
nothing ever comes out; the vault becomes storage, then guilt, then
abandoned.
→ *Kit answer:* the success metric is **output** — study sheets, drafts,
plans, decisions. `brain-ask` makes withdrawal as easy as deposit, and the
weekly review pulls in the same direction: it surfaces stalled loops and
open questions and offers to research them. What the review does *not* do
is ask you what the brain should produce next. That would close the loop
properly, and it belongs on the wish list, not in this description.

**4. All setup, no payoff.** Beginners spend the first session choosing
taxonomies and comparing methods, meet an empty vault, and never come
back — the investment came before any win.
→ *Kit answer:* the setup asks who the brain is for, then **four short
questions**, and then builds real notes itself — your project, your
deadlines, a populated `Home` dashboard. The first win arrives minutes
in, before any interview, before any method talk. And returning after
weeks away is a designed path (the review catches up in batches), not a
walk of shame.

## Why the vault is built for agents first

The premise of this kit is that you will not maintain the vault. An AI
will, in sessions that start cold and land in the middle of your notes
through a search or a glob. So the first question asked of every design
decision is not "does this look tidy in Obsidian?" but: **can an agent
that lands here keep going without guessing?** Four things follow from
that.

**Signposts, not search alone.** Search returns files, not orientation. A
model that reads three hits out of four hundred notes has no idea what
the folder is for, what does not belong in it, or which note the others
hang off. So every folder that holds notes carries an `index.md` that
says exactly that in about 25 lines, plus a three-line `CLAUDE.md` that
pulls the signpost into Claude's context on the first read in that
folder. `index.md` is the canonical one because it is a plain file any
tool can open, Claude or not; the `CLAUDE.md` is only the delivery
mechanism. And a signpost lists entry points, never every file, and only
things an agent cannot see for itself — describing a visible file listing
costs tokens and dilutes the lines that carry information.

**Real paths, not wikilinks, inside a signpost.** `[[Note name]]` is an
Obsidian convention that resolves through the app's index; an agent
reading the raw file gets a name and no location. Inside notes,
wikilinks stay the rule, because that is what makes the graph work for
you. Inside signposts, links are relative paths, because that is what
makes them work without Obsidian.

**Validity is a field, not a tone of voice.** A person reads "we used to
do it that way" and understands. A model reads it as instruction. So the
two questions a note raises get two machine-readable fields instead of
one: `maturity:` says how worked out it is, `status:` says whether it
still holds. A note can be `evergreen` and `deprecated` at the same time,
beautifully worked out and no longer true. The pair that matters most in
a shared vault is `verified:` against `generated:`: a human confirmed
this, or a machine drafted it. Claude never sets `verified:` on its own
work, which is what stops a proposal from quietly becoming the rule.

**Only what is in the Markdown counts.** No database, no index to
rebuild, no hidden sidecar file. That is why a note that replaces another
gets the notice written into the body of *both* files: an agent that
arrives in the outdated version through a search reads that body, and
nothing else will tell it. Rules nothing checks erode, so
`.tools/hygiene.py` reports the one-sided chains, along with orphans,
dead links, near-empty notes, frontmatter gaps and folders that lost
their signpost.

## The structural choices, briefly defended

- **PARA-inspired, not PARA-pure.** Projects/Areas/Archive come from PARA
  (fortelabs.com/blog/para) because actionability-first works for any
  life situation. We add `30-knowledge` as an explicit Zettelkasten-style
  space and `40-decisions` as an append-only log — decisions are the
  highest-value notes a person owns, and they must never be rewritten.
- **Flat beats deep.** Links, tags and deterministic search
  (`.tools/search.py`) do the finding; folder depth just hides things.
  (This is the Linking-Your-Thinking insight, minus the learning curve.)
  Deterministic, not embeddings: the same query gives the same hits
  forever, with no index to build and nothing to send anywhere. It also
  scores matches inside a word, because German glues words together and a
  search for `Vertrag` that misses `Rahmenvertrag` is simply broken.
- **Three shapes, one core.** A brain for yourself, one for your work,
  one shared by a company: one core template, the same five skills, and
  overlays copied on top. Two purposes never share a vault, because "keep
  this separate" is a promise a folder cannot keep. A shared vault also
  drops person notes and carries roles instead: a role description
  survives every hire and every departure, and nobody has to be assessed
  for it.
- **Numbered with gaps.** `00 10 20 30 40 … 90` keeps folders sorted and
  leaves 50–80 for later, so growth never forces a re-sort — the useful
  half of Johnny Decimal without its rigidity. In a private brain those
  four numbers are yours (journal, media, health, money, or your own); a
  work brain spends two on `50-processes/` and `60-contribution/`; a company vault spends all
  four on processes, roles, onboarding and partners.
- **The interview is a starting point, not a cage.** Reviews are
  explicitly allowed to propose structure changes as your life changes.
- **AI as maintainer, not author.** Claude files, links, prunes and
  reminds — but the notes are your words. A brain full of paraphrased-
  by-you ideas stays useful; a brain full of AI paste becomes an attic.
  (The operational rule lives in the vault's CLAUDE.md: "The red line".)
- **The brain shows its work.** Auto-capture systems that silently hoard
  everything drown in their own junk — the documented failure mode of
  "extract everything" memory tools. Here every filing is reported, every
  change is a Git commit, and deleting is a first-class feature.

## Why an AI-maintained vault at all — instead of just chatting with AI?

Because chats evaporate. Every conversation you have about a thought
disappears into scroll history; the vault is the persistent, structured,
searchable thing the AI reads from and writes into. A year later, search
and the graph still work — and every new session starts already knowing
your context instead of from zero. **The AI is the librarian, not the
library.** And the two retrieval modes complement each other: search
finds what you know to look for; the weekly review surfaces what you
forgot to ask.

## Sources worth reading
- Tiago Forte — *The PARA Method*: https://fortelabs.com/blog/para/
- Nick Milo — Linking Your Thinking: https://www.linkingyourthinking.com/
- Johnny Decimal (numbering): https://johnnydecimal.com/
