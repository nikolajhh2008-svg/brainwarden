<!-- Machine anchors: the four dashboard blocks are delimited by
     `<!-- block:NAME -->` … `<!-- /block:NAME -->`. Address them by
     MARKER, never by heading text — headings are translated into the
     vault language, markers never are. Refreshing a block means
     replacing only the lines BETWEEN its marker pair; markers,
     headings and everything below the `---` stay untouched. Lines
     carrying `<!-- keep:… -->` survive every refresh — update their
     content, never delete the line. Agents looking for paths rather
     than prose: read index.md instead. -->

Your brain at a glance. You can't get lost: every path leads back here.
(Claude fills and updates this page — starting during setup. No heading
here on purpose — Obsidian already shows the filename as the title.)

## Right now
<!-- block:right-now -->
<!-- Claude: active projects as wikilinks with a one-line status each, e.g. "- exam-prep-biology - next: summarize chapter 3". The "Areas:" line below is the ONLY inbound link the area notes have — refresh its links, never drop the line. -->
- *(your first project appears here during setup)*
- <!-- keep:areas-line -->Areas: *(your areas appear here during setup)*
<!-- /block:right-now -->

## Next deadlines
<!-- block:next-deadlines -->
<!-- Claude: mirror the next 3 dates from Deadlines.md; the full list stays there -->
- *(none yet — every date lives in [[Deadlines]])*
<!-- /block:next-deadlines -->

## Open questions
<!-- block:open-questions -->
<!-- Claude: "open → ask later" markers and stalled loops from the last review -->
- *(fills up as the brain learns what it doesn't know)*
<!-- /block:open-questions -->

## New this week
<!-- block:new-this-week -->
<!-- Claude: the 3-5 most recently added or grown notes as wikilinks, refreshed at every review -->
- *(updated at every brain review)*
<!-- /block:new-this-week -->

---

## How to use your brain
- **Dump a thought** → tell Claude `capture: …` (lands in [[Inbox rule|00-inbox]] — no sorting, ever)
- **Feed it a source** → drop PDFs/transcripts into `00-inbox/raw/` → say `ingest`
- **Ask it something** → *"what does my brain know about …?"*
- **Once a week, fixed day** → `brain review` (~10 min — Claude does the work, you answer questions)
- Me: [[About me]] · People: `30-knowledge/people/` · Rules: [[CLAUDE|CLAUDE.md]]

*The success metric is output — texts, plans, study sheets, decisions.
Never note count.*
