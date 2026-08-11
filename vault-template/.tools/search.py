#!/usr/bin/env python3
"""Brain search: deterministic pre-search over the vault (token saver).

    python3 ~/Brain/.tools/search.py real-rates gold
    python3 ~/Brain/.tools/search.py "chilling effect" --k 5
    python3 ~/Brain/.tools/search.py --stats

Scoring per file and term:

    title/filename   word start 5.0   inside a word 2.0
    tags             word start 3.0   inside a word 1.0
    body line        word start 1.0 for the first, less for each further
                     one, approaching 5.0 · inside a word 0.4 (max 3.0)

Body mentions have diminishing returns, and that is what keeps the ranking
honest: summed straight, a project log that happens to write "Vertrag" on a
hundred lines scored 100.0 and buried `Vertrag.md` — the note that IS about
contracts — at 11.0. On a 10 MB log it reached 132731.0. Repetition is not
aboutness. The total from body mentions now stays under one title hit, so
the file NAMED after the term always wins against one that merely says it
often — while ten mentions still rank above three.

Hits INSIDE a word count — German glues words together, so `Vertrag` has
to find `Rahmenvertrag`, `Kosten` has to find `Mehrkostenforderungen` and
`Straße` has to find `Taborstraße`. They count LESS than a word start and
are capped per term, so `test` still cannot be flooded to the top by a
file that only says `fastest`. Terms shorter than 4 characters match at
word starts only (`ei`, `an` would otherwise match everything).

Accent-insensitive (cafe matches café, Strasse matches Straße). Output:
top-k files with matching lines — Claude then reads ONLY those files.
"""
import os, re, sys, unicodedata

# Windows falls back to the console codepage (cp1252/cp850) the moment the
# output is redirected or piped — and `↳`, or any arrow inside a matched
# note line, does not exist there, so the search died with a
# UnicodeEncodeError. Console streams are utf-8 already; this fixes pipes.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        pass

SKIP_DIRS = {".git", ".obsidian", ".tools", "_templates"}

W_NAME, W_NAME_IN = 5.0, 2.0        # title / filename
W_TAG, W_TAG_IN = 3.0, 1.0          # tags
W_BODY, W_BODY_IN = 1.0, 0.4        # body lines
BODY_CAP = 5.0                      # body word starts approach, never pass, this
BODY_HALF = 4.0                     # shape of that approach (see score_file)
BODY_IN_CAP = 3.0                   # max inside-word body score per term
MIN_IN_LEN = 4                      # shorter terms: word starts only

# Frontmatter vocabulary (see spec 4): `maturity` is the ripeness of a
# knowledge note, `status` is validity. Old vaults still write ripeness
# into `status:` — --stats reads both and flags the leftovers.
MATURITY = ("seed", "growing", "evergreen")
VALIDITY = ("draft", "stable", "deprecated")

# Kit infrastructure, not notes. Counting these inflates every number and
# their code examples ("status: seed | growing | evergreen" in CLAUDE.md)
# used to be counted as real frontmatter.
INFRA_FILES = {"CLAUDE.md", "index.md", "Home.md", "Deadlines.md",
               "About me.md", "About this vault.md", "Inbox rule.md", "README.md"}

def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")

def fold(text):
    """Lowercase + strip accents + German sharp s, so voice-typed queries match."""
    text = text.lower().replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))

def parse_args(argv):
    terms, k, i = [], 8, 0
    while i < len(argv):
        a = argv[i]
        if a == "--k" and i + 1 < len(argv):
            try:
                k = int(argv[i + 1])
            except ValueError:
                pass
            i += 2
            continue
        if a.startswith("--") and a != "--stats":
            # Anything else starting with `--` used to vanish without a word,
            # so `search.py --root /other/vault gold` searched THIS vault for
            # "gold" and looked like it had honoured the flag. There is no
            # --root here on purpose: the tool searches the vault it lives in.
            print(f"Unknown option: {a}\n"
                  "Usage: search.py <term> [term2 ...] [--k N] | --stats\n"
                  "(No --root: this tool searches the vault it sits in — run "
                  "the copy inside that vault.)")
            return None, k
        if not a.startswith("--"):
            terms.append(a)
        i += 1
    return terms, k

def walk_notes(root):
    """Every .md file in the vault, minus tooling folders. Yields (path, relpath)."""
    for dirpath, dirs, files in os.walk(root):
        # Hidden folders are skipped like in hygiene.py: a vault that ships
        # its own `.claude/skills/` would otherwise count five SKILL.md files
        # as notes, and `.private/` would surface in every search.
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in sorted(files):
            if not f.endswith(".md") or f.startswith("_"):
                continue
            path = os.path.join(dirpath, f)
            yield path, os.path.relpath(path, root)

def read(path):
    """utf-8-sig: a byte-order mark would otherwise hide the frontmatter."""
    try:
        return open(path, encoding="utf-8-sig", errors="ignore").read()
    except OSError:
        return None

def tags_block(text):
    """Everything under a YAML `tags:` key, incl. multi-line list items."""
    m = re.search(r"^tags:(.*(?:\n[ \t]+-[^\n]*)*)", text, re.M)
    return m.group(0) if m else ""

def frontmatter(text):
    """The YAML block at the very top — and nothing else.

    Reading fields with `^status:` over the WHOLE file matches YAML
    examples inside fenced code blocks; that is how a one-note vault
    reported two notes with a maturity each."""
    m = re.match(r"---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    return m.group(1) if m else ""

def fm_value(fm, key):
    """One frontmatter value, comment and quotes stripped (`in progress` stays whole)."""
    m = re.search(rf"^{key}:[ \t]*(.+?)[ \t]*$", fm, re.M)
    if not m:
        return None
    return (m.group(1).split(" #")[0].strip().strip("\"'").lower() or None)

def is_infra(rel):
    """Kit scaffolding: root/folder signposts and the raw/ readme."""
    return os.path.basename(rel) in INFRA_FILES

def git_reviews(root):
    """Review history — only if the vault IS a git repo, not if it sits in one.

    `git -C <vault> log` happily answers from a PARENT repository, which
    would report someone else's commits as this vault's review history."""
    import subprocess
    try:
        top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5)
    except Exception:
        return "reviews: unknown (git not available)"
    if top.returncode != 0 or not top.stdout.strip():
        return "reviews: unknown (vault is not a git repo — no version history)"
    if os.path.realpath(top.stdout.strip()) != os.path.realpath(root):
        return ("reviews: unknown (vault is not its own git repo — it sits inside "
                + os.path.realpath(top.stdout.strip()) + ", whose history is not this vault's)")
    try:
        log = subprocess.run(["git", "-C", root, "log", "-i", "--grep", "review",
                              "--format=%as"], capture_output=True, text=True,
                             timeout=5).stdout.split()
    except Exception:
        return "reviews: unknown (git log failed)"
    if not log:
        return "reviews: 0 (no commit mentions a review yet)"
    return f"reviews: {len(log)} (last {log[0]})"

def stats(root):
    """--stats: honest numbers about this vault — folders, maturity, age."""
    import collections
    folders = collections.Counter()
    maturity, validity, other_status = collections.Counter(), collections.Counter(), collections.Counter()
    words, infra, legacy = [], 0, []
    for path, rel in walk_notes(root):
        if is_infra(rel):
            infra += 1
            continue
        folders[rel.split(os.sep)[0] if os.sep in rel else "(root)"] += 1
        text = read(path)
        if text is None:
            continue
        words.append(len(text.split()))
        fm = frontmatter(text)
        ripeness = fm_value(fm, "maturity")
        if ripeness:
            maturity[ripeness] += 1
        value = fm_value(fm, "status")
        if value:
            if value in MATURITY:          # old schema: status held the ripeness
                legacy.append(rel)
                if not ripeness:
                    maturity[value] += 1
            elif value in VALIDITY:
                validity[value] += 1
            else:
                other_status[value] += 1
    print(f"notes: {sum(folders.values())}" + (f" (+ {plural(infra, 'kit file')}, not counted)" if infra else ""))
    if not folders:
        print("  (no notes yet — everything here is still kit scaffolding)")
    for name, n in sorted(folders.items()):
        print(f"  {name}: {n}")
    if words:
        print(f"words/note: median {sorted(words)[len(words) // 2]}")
    if maturity:
        print("maturity: " + " · ".join(f"{s} {n}" for s, n in sorted(maturity.items())))
    if validity:
        print("status: " + " · ".join(f"{s} {n}" for s, n in sorted(validity.items())))
    if other_status:
        print("status (values outside the schema): "
              + " · ".join(f"{s} {n}" for s, n in sorted(other_status.items())))
        print("  ↳ expected: maturity: " + "|".join(MATURITY) + " · status: " + "|".join(VALIDITY)
              + " (a translated scale? then the update path has to map it)")
    if legacy:
        print(f"legacy schema: `status:` still used for maturity in {plural(len(legacy), 'note')} "
              f"(update path: rename it to `maturity:`) — e.g. " + ", ".join(legacy[:3]))
    print(git_reviews(root))
    return 0

def score_file(text, name, terms):
    """Score one file against all terms. Returns (score, up to 3 sample lines)."""
    tags = fold(tags_block(text))
    raw_lines = text.splitlines()
    folded_lines = [fold(l) for l in raw_lines]
    score, starts, insides = 0.0, [], []
    for t in terms:
        pat = re.compile(r"\b" + re.escape(t))
        inside_ok = len(t) >= MIN_IN_LEN
        if pat.search(name):
            score += W_NAME
        elif inside_ok and t in name:
            score += W_NAME_IN
        if pat.search(tags):
            score += W_TAG
        elif inside_ok and t in tags:
            score += W_TAG_IN
        hits, inside_score = 0, 0.0
        for raw, line in zip(raw_lines, folded_lines):
            start_hit = bool(pat.search(line))
            if not start_hit and not (inside_ok and t in line):
                continue
            if start_hit:
                hits += 1
            else:
                inside_score = min(inside_score + W_BODY_IN, BODY_IN_CAP)
            clean = raw.strip()[:120]
            if clean and not raw.startswith("---"):
                bucket = starts if start_hit else insides
                if clean not in starts and clean not in insides and len(bucket) < 3:
                    bucket.append(clean)
        # Diminishing returns instead of a straight sum: the first mention is
        # worth a full W_BODY (1.0), the hundredth almost nothing, and the
        # total can never reach BODY_CAP. A plain cap would do the same job
        # against flooding but would make every file with five or more
        # mentions score IDENTICALLY, and ties get broken alphabetically —
        # that throws away real signal to fix a fake one.
        score += BODY_CAP * hits / (hits + BODY_HALF) + inside_score
    return score, (starts + insides)[:3]

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if "--stats" in sys.argv[1:]:
        return stats(root)
    terms, k = parse_args(sys.argv[1:])
    if terms is None:               # unknown option — already explained
        return 1
    if not terms:
        print("Usage: search.py <term> [term2 ...] [--k N] | --stats"); return 1
    terms = [fold(t) for t in terms]
    scored = []
    for path, rel in walk_notes(root):
        text = read(path)
        if text is None:
            continue
        score, lines = score_file(text, fold(os.path.basename(rel)[:-3]), terms)
        if score:
            # Signposts are halved, not hidden. They describe where things
            # live, so they mention every topic in the vault at least once —
            # and a folder map scoring above the note it points at is how a
            # duplicate check misses the twin it was looking for. Halving
            # keeps "where is X filed?" answerable while a real note on the
            # subject always wins.
            scored.append((score * (0.5 if is_infra(rel) else 1.0), rel, lines))
    scored.sort(key=lambda s: (-s[0], s[1]))
    if not scored:
        print("No hits."); return 0
    for score, rel, lines in scored[:k]:
        print(f"\n[{score:5.1f}] {rel}")
        for l in lines:
            print(f"        {l}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
