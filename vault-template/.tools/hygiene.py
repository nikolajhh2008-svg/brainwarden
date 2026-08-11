#!/usr/bin/env python3
"""Brain hygiene: the link graph of the vault, as a report.

    python3 ~/Brain/.tools/hygiene.py
    python3 ~/Brain/.tools/hygiene.py --max 25
    python3 ~/Brain/.tools/hygiene.py --root /path/to/another/vault

The weekly review asks for orphans, dead links and empty files. Guessing
that from a few hundred notes is exactly what a model is bad at, so it is
measured here instead:

    orphans        notes nothing links to
    dead links     [[wikilinks]] and [markdown](links) whose target is gone
    near-empty     notes with almost no body
    unreachable    notes no index.md and no map of content points to (spec 3)
    folders        folders that carry notes but no index.md signpost
    frontmatter    missing type:/created:, or `status:` still used for maturity
    supersede      "Supersedes X" without X saying "Superseded by" (spec 4.2)

Read-only, standard library only, exit code 0 even with findings — this
is a report, not a test. Code is masked before links are read, so the
`[[example]]` inside a rules file is never reported as a dead link.
Hidden folders (`.git`, `.obsidian`, `.private` …) are not scanned, but
links pointing INTO them still resolve if the file is there.
"""
import collections, os, re, sys, unicodedata
from urllib.parse import unquote

SKIP_DIRS = {".git", ".obsidian", ".tools", "_templates", "node_modules"}
NEAR_EMPTY_WORDS = 15
MATURITY = ("seed", "growing", "evergreen")
INFRA_FILES = {"CLAUDE.md", "index.md", "Home.md", "Deadlines.md", "About me.md",
               "About this vault.md", "Inbox rule.md", "README.md"}
# Orphans there are not a finding: captures are unlinked by definition
# (the review empties the inbox) and the archive is cold storage.
UNLINKED_OK = ("00-inbox", "90-archive")
# Superseded records are deliberately dropped from their folder's index.md
# (the signpost lists what applies, not what applied). Flagging them forever
# would make "0 unreachable" impossible from the first replacement onwards.
SUPERSEDED = re.compile(r"^\s*(superseded by|status:\s*deprecated)", re.M | re.I)
EXTERNAL = ("http://", "https://", "mailto:", "tel:", "obsidian://", "ftp://", "//")

def norm(text):
    """Compare names the way a human would: case- and accent-insensitive."""
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))

def mask_code(text):
    """Blank out fenced blocks and `inline code`, keeping line numbers intact.

    A vault's own rule files show `[[wikilink]]` syntax as an example.
    Without this, every review would report those examples as dead links."""
    out, fence = [], None
    for line in text.split("\n"):
        stripped = line.lstrip()
        if fence:
            out.append("")
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
            out.append("")
            continue
        out.append(re.sub(r"`+[^`\n]*`+", lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)

FRONTMATTER = re.compile(r"---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", re.S)

def frontmatter(text):
    m = FRONTMATTER.match(text)
    return m.group(1) if m else ""

def body(text):
    m = FRONTMATTER.match(text)
    return text[m.end():] if m else text

def is_infra(rel):
    return os.path.basename(rel) in INFRA_FILES

def top_folder(rel):
    return rel.split(os.sep)[0] if os.sep in rel else "(root)"

def unlinked_ok(rel):
    return top_folder(rel) in UNLINKED_OK

class Vault:
    """The vault as a link graph. Reads every note exactly once."""

    def __init__(self, root):
        self.root = root
        self.notes = {}     # rel -> raw text
        self.masked = {}    # rel -> same text, code blanked out
        self.files = set()  # every file (incl. attachments), for link resolution
        self.by_name = {}   # normalised name/stem -> rel (first wins, like Obsidian)
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(dirpath, f), root)
                self.files.add(rel)
                for key in {norm(f), norm(os.path.splitext(f)[0])}:
                    self.by_name.setdefault(key, rel)
                if f.endswith(".md") and not f.startswith("_"):
                    try:   # utf-8-sig: a byte-order mark would hide the frontmatter
                        text = open(os.path.join(dirpath, f), encoding="utf-8-sig",
                                    errors="ignore").read()
                    except OSError:
                        continue
                    self.notes[rel] = text
                    self.masked[rel] = mask_code(text)

    def links(self, rel, only_lines_matching=None):
        """Internal links of a note as (target, line number, raw form).

        `only_lines_matching`: a compiled regex — then only links on lines
        that match it are returned (used for the Supersedes/Superseded pairs)."""
        for n, line in enumerate(self.masked[rel].split("\n"), 1):
            if only_lines_matching and not only_lines_matching.search(line):
                continue
            for m in re.finditer(r"!?\[\[([^\]\n|#^]*)", line):
                target = m.group(1).strip()
                if target:
                    yield target, n, f"[[{target}]]"
            for m in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", line):
                target = m.group(1).strip().split(" ")[0].strip("<>")
                target = unquote(target.split("#")[0]).strip()
                if target and not target.startswith(EXTERNAL) and not target.startswith("#"):
                    yield target, n, f"({target})"

    def resolve(self, target, source):
        """Obsidian-style: by path (relative to the note, then to the vault
        root), otherwise by file name anywhere. Returns a rel path or None.

        The name fallback applies ONLY to bare names (`[[Some note]]`), never
        to targets that carry a path. A path says where the file is; falling
        back to "some file with that name, somewhere" would make every broken
        relative link resolve — `../gone/index.md` would silently land on any
        of the ten `index.md` files in the vault, and the dead-link check
        would report zero on a vault whose signpost chain is broken."""
        for base in (os.path.dirname(source), ""):
            for suffix in ("", ".md"):
                cand = os.path.normpath(os.path.join(base, target + suffix))
                if cand in self.files or os.path.exists(os.path.join(self.root, cand)):
                    return cand
        if "/" in target or target.startswith("."):
            return None
        return self.by_name.get(norm(os.path.basename(target)))

    def is_signpost(self, rel):
        """index.md, Home.md and maps of content — the way INTO a folder."""
        name = os.path.basename(rel)
        return (name in ("index.md", "Home.md")
                or "moc" in norm(name).replace("-", " ").replace("_", " ").split()
                or bool(re.search(r"^type:\s*moc\b", frontmatter(self.notes[rel]), re.M)))

def report(title, items, limit, note=""):
    print(f"\n{title}: {len(items)}{note}")
    for line in items[:limit]:
        print(f"  {line}")
    if len(items) > limit:
        print(f"  … and {len(items) - limit} more")

def main():
    argv = sys.argv[1:]
    limit, root = 10, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for i, a in enumerate(argv):
        if a == "--max" and i + 1 < len(argv):
            try:
                limit = max(1, int(argv[i + 1]))
            except ValueError:
                pass
        elif a == "--root" and i + 1 < len(argv):
            root = os.path.abspath(os.path.expanduser(argv[i + 1]))
        elif a.startswith("--") and a not in ("--max", "--root"):
            print(__doc__.strip()); return 1
    if not os.path.isdir(root):
        print(f"No vault at {root}"); return 1

    v = Vault(root)
    if not v.notes:
        print(f"hygiene — {root}\nNo notes found (is this a vault?)"); return 0

    signposts = {rel for rel in v.notes if v.is_signpost(rel)}
    inbound = collections.Counter()
    dead, signposted = [], set()
    for rel in sorted(v.notes):
        for target, line, raw in v.links(rel):
            hit = v.resolve(target, rel)
            if hit is None:
                dead.append(f"{rel}:{line} → {raw}")
            elif hit != rel:
                inbound[hit] += 1
                if rel in signposts and hit in v.notes:
                    signposted.add(hit)

    orphans, near_empty, gaps = [], [], []
    gap_counts = collections.Counter()
    for rel, text in sorted(v.notes.items()):
        if not is_infra(rel) and not unlinked_ok(rel) and not inbound[rel]:
            orphans.append(rel)
        words = len(body(text).split())
        if not is_infra(rel) and words < NEAR_EMPTY_WORDS:
            near_empty.append(f"{rel} ({words} words)")
        if is_infra(rel) or top_folder(rel) == "00-inbox":
            continue                     # inbox captures need no frontmatter
        fm, missing = frontmatter(text), []
        if not re.search(r"^type:\s*\S", fm, re.M):
            missing.append("no type:")
        if not re.search(r"^created:\s*\S", fm, re.M):
            missing.append("no created:")
        s = re.search(r"^status:\s*([\w-]+)", fm, re.M)
        if s and s.group(1) in MATURITY:
            missing.append("`status:` still used for maturity")
        if missing:
            gap_counts.update(missing)
            gaps.append(f"{rel} — {', '.join(missing)}")

    # Reachability only means something where a folder HAS a signpost —
    # otherwise the missing index.md is the finding, not the notes.
    unreachable, no_index, folders = [], [], collections.defaultdict(list)
    for rel in v.notes:
        folders[os.path.dirname(rel)].append(rel)
    for folder, members in sorted(folders.items()):
        real = sorted(r for r in members if not is_infra(r) and not unlinked_ok(r))
        if not real:
            continue
        if os.path.join(folder, "index.md") in v.notes:
            unreachable += [r for r in real if r not in signposted
                            and not SUPERSEDED.search(v.notes[r])]
        else:
            no_index.append((len(real), f"{folder or '(root)'} ({len(real)} notes)"))
    no_index = [line for _, line in sorted(no_index, reverse=True)]

    chains, seen = [], set()
    sup, supby = re.compile(r"supersedes\b", re.I), re.compile(r"superseded by\b", re.I)
    for rel in sorted(v.notes):
        for keyword, back, phrase in ((sup, supby, "Superseded by"), (supby, sup, "Supersedes")):
            for target, line, raw in v.links(rel, keyword):
                hit = v.resolve(target, rel)
                if not hit or hit not in v.notes or hit == rel:
                    continue
                partners = {v.resolve(t, hit) for t, _, _ in v.links(hit, back)}
                if rel not in partners and (rel, hit, phrase) not in seen:
                    seen.add((rel, hit, phrase))
                    chains.append(f'{rel}:{line} → {hit}, but {hit} has no "{phrase}" back to it')

    print(f"hygiene — {root}")
    print(f"{len(v.notes)} notes scanned ({len([r for r in v.notes if is_infra(r)])} kit files, "
          f"{len(signposts)} signposts)")
    report(f"orphans — nothing links here (excl. {', '.join(UNLINKED_OK)})", orphans, limit)
    report("dead links — target does not exist", dead, limit)
    report(f"near-empty — under {NEAR_EMPTY_WORDS} words of body", near_empty, limit)
    report("not reachable from a signpost (index.md / MOC / Home)", unreachable, limit)
    report("folders with notes but no index.md (spec 3)", no_index, limit)
    report("frontmatter gaps", gaps, limit,
           note=" (" + " · ".join(f"{k} {n}" for k, n in sorted(gap_counts.items())) + ")"
           if gap_counts else "")
    report("supersede chains without a back-reference (spec 4.2)", chains, limit)
    return 0

if __name__ == "__main__":
    sys.exit(main())
