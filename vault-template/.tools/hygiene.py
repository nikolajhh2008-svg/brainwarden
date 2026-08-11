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
    expired        notes past their own stale_after / review_due date
    supersede      "Supersedes X" without X saying "Superseded by" (spec 4.2)
    fences         an unclosed ``` — everything below it escaped every check
    portability    files that do not survive a move to another OS: not-UTF-8
                   notes, names differing only in case, names Windows refuses

Read-only, standard library only, exit code 0 even with findings — this
is a report, not a test. Code is masked before links are read, so the
`[[example]]` inside a rules file is never reported as a dead link.
Hidden folders (`.git`, `.obsidian`, `.private` …) are not scanned, but
links pointing INTO them still resolve if the file is there.
"""
import collections, datetime, os, re, sys, unicodedata
from urllib.parse import unquote

# Windows writes reports in the console codepage (cp1252/cp850) as soon as
# the output is redirected or piped — and `→`, `↳` do not exist there, so
# the report died with a UnicodeEncodeError halfway through. A console
# stream is already utf-8 on Windows, so this only ever fixes pipes.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):
        pass

SKIP_DIRS = {".git", ".obsidian", ".tools", "_templates", "node_modules",
             # Only present in the KIT, never in a vault: overlays are
             # half-vaults whose links only resolve once they are copied on
             # top of a core. Scanning them reports links as dead that are
             # correct in every real vault.
             "modules"}
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

# `[text](target)` in the two forms a vault actually contains. Splitting the
# target at the first space (the old approach) cut `<mit leer zeichen.md>`
# down to `mit` and reported a living file as a dead link — and the file it
# pointed at then showed up as an orphan on top. So: the angle form keeps its
# spaces, the bare form tolerates one level of parentheses (`studie (2026).md`),
# and only a genuine "title" in quotes is dropped.
MD_LINK = re.compile(
    r"!?\[[^\]\n]*\]\("
    r"(?:<([^>\n]*)>|((?:[^()\n]|\([^()\n]*\))+?))"
    r"(?:[ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'))?[ \t]*\)")

def norm(text):
    """Compare names the way a human would: case- and accent-insensitive."""
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))

# Windows refuses these outright. A note called `KI: Schutz oder Überwachung.md`
# is a perfectly good title on macOS and Linux and simply cannot be checked out
# on Windows — git clone fails on that file. Worth knowing before it is pushed.
WIN_RESERVED = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} \
                                            | {f"lpt{i}" for i in range(1, 10)}
WIN_CHARS = '<>:"|?*'

def windows_unsafe(name):
    """Why this file name cannot exist on Windows — or '' if it can."""
    hits = sorted({c for c in name if c in WIN_CHARS})
    if any(ord(c) < 32 for c in name):
        hits.append("control character")
    if hits:
        return "illegal on Windows: " + " ".join(hits)
    if name != name.rstrip(" .") and name not in (".", ".."):
        return "ends in a space or dot — Windows silently drops it"
    if os.path.splitext(name)[0].lower() in WIN_RESERVED:
        return "reserved device name on Windows"
    return ""

def mask_inline(line):
    return re.sub(r"`+[^`\n]*`+", lambda m: " " * len(m.group(0)), line)

def mask_code(text):
    """Blank out fenced blocks and `inline code`, keeping line numbers intact.

    A vault's own rule files show `[[wikilink]]` syntax as an example.
    Without this, every review would report those examples as dead links.

    Returns (masked text, line number of an unterminated fence or None).
    An opening ``` that is never closed used to blank the ENTIRE rest of the
    file: every link after it went unchecked, and the report said nothing.
    A forgotten fence is a typo, not an instruction to stop looking — so the
    rest is read as ordinary text and the typo is reported instead."""
    lines = text.split("\n")
    out, fence, opened_at = [], None, None
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if fence:
            out.append("")
            if stripped.startswith(fence):
                fence, opened_at = None, None
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence, opened_at = stripped[:3], i
            out.append("")
            continue
        out.append(mask_inline(line))
    if fence is not None:
        for i in range(opened_at, len(lines)):
            out[i] = mask_inline(lines[i])
        return "\n".join(out), opened_at + 1
    return "\n".join(out), None

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


def read_ignores(root):
    """Folders another system writes into, from `.hygieneignore` in the root.

    A vault is a folder, so other tools end up writing into it — an
    assistant's memory store, a Zotero export, a plugin's daily notes.
    Those files follow their own conventions and will never carry this
    schema. Reported forever, they are noise that pushes the real findings
    off the end: measured on one live vault, 42 of 42 findings came from a
    single machine-written folder, and a report that is always red is a
    report nobody reads.

    One folder path per line, `#` starts a comment. Never silent — the
    header says how many folders were skipped and how many notes that hid.
    """
    path = os.path.join(root, ".hygieneignore")
    out = []
    try:
        with open(path, encoding="utf-8-sig", errors="ignore") as fh:
            for line in fh:
                line = line.split("#")[0].strip().strip("/")
                if line:
                    out.append(line.replace("\\", "/"))
    except OSError:
        pass
    return out

class Vault:
    """The vault as a link graph. Reads every note exactly once."""

    def __init__(self, root):
        self.root = root
        self.notes = {}     # rel -> raw text
        self.masked = {}    # rel -> same text, code blanked out
        self.files = set()  # every file (incl. attachments), for link resolution
        self.by_name = {}   # normalised name/stem -> rel (first wins, like Obsidian)
        self.by_path_ci = {}    # lowercased rel path -> real rel path
        self.unterminated = []  # notes with an unclosed ``` fence
        self.mojibake = []      # files that are not valid UTF-8
        self.case_clash = []    # names that differ only in case
        self.odd_names = []     # names that cannot exist on Windows
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(dirpath, f), root)
                self.files.add(rel)
                key_ci = rel.replace(os.sep, "/").lower()
                # Two files whose names differ only in case can coexist on
                # Linux but NOT on macOS or Windows: copying that vault to
                # either loses one of them, silently. Only a case-sensitive
                # filesystem can even produce this, which is the point.
                if key_ci in self.by_path_ci:
                    self.case_clash.append(f"{self.by_path_ci[key_ci]}  vs  {rel}")
                else:
                    self.by_path_ci[key_ci] = rel
                bad = windows_unsafe(os.path.basename(rel))
                if bad:
                    self.odd_names.append(f"{rel} — {bad}")
                for key in {norm(f), norm(os.path.splitext(f)[0])}:
                    self.by_name.setdefault(key, rel)
                if f.endswith(".md") and not f.startswith("_"):
                    try:
                        raw = open(os.path.join(dirpath, f), "rb").read()
                    except OSError:
                        continue
                    # utf-8-sig: a byte-order mark would hide the frontmatter.
                    # A note saved as cp1252 or UTF-16 (Windows Notepad "ANSI",
                    # PowerShell 5.1 `>`) decodes to rubbish here AND shows as
                    # rubbish in Obsidian — errors="ignore" used to hide that
                    # completely, so the note simply stopped being findable.
                    try:
                        text = raw.decode("utf-8-sig")
                    except UnicodeDecodeError:
                        self.mojibake.append(rel)
                        text = raw.decode("utf-8-sig", errors="ignore")
                    else:
                        if "\x00" in text:      # UTF-16 without a BOM
                            self.mojibake.append(rel)
                    self.notes[rel] = text
                    self.masked[rel], fence_line = mask_code(text)
                    if fence_line:
                        self.unterminated.append(f"{rel}:{fence_line}")

    def links(self, rel, only_lines_matching=None):
        """Internal links of a note as (target, line number, raw form).

        `only_lines_matching`: a compiled regex — then only links on lines
        that match it are returned (used for the Supersedes/Superseded pairs)."""
        for n, line in enumerate(self.masked[rel].split("\n"), 1):
            if only_lines_matching and not only_lines_matching.search(line):
                continue
            # The two substring guards are not micro-optimisation: without
            # them a very long line full of `[` and no closing `)` makes the
            # link regex backtrack quadratically (measured: 200k characters
            # took 35 seconds). A link cannot exist without these two bytes.
            if "[[" in line:
                for m in re.finditer(r"!?\[\[([^\]\n|#^]*)", line):
                    target = m.group(1).strip()
                    if target:
                        yield target, n, f"[[{target}]]"
            if "](" in line:
                for m in MD_LINK.finditer(line):
                    target = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
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
        # A link written on Windows may carry backslashes. Normalising them
        # here is what makes one vault give the SAME answer on all three
        # systems: untouched, `unterordner\note.md` counts as a bare name on
        # macOS/Linux (dead) and as a path on Windows (alive).
        tgt = target.replace("\\", "/")
        for base in (os.path.dirname(source), ""):
            for suffix in ("", ".md"):
                cand = os.path.normpath(os.path.join(base, tgt + suffix))
                # `../../x` climbs OUT of the vault; whatever it finds there
                # is not a note of this vault and must not count as resolved.
                if cand.startswith(".." + os.sep) or cand == "..":
                    continue
                if cand in self.files or self.exists_exact(cand):
                    return cand
        if "/" in tgt or tgt.startswith("."):
            return None
        return self.by_name.get(norm(os.path.basename(tgt)))

    def exists_exact(self, cand):
        """Does this path exist with EXACTLY this spelling?

        `os.path.exists` says yes to `ZIEL.md` when the file is `Ziel.md` on
        macOS and Windows, and no on Linux — the same vault, two verdicts.
        Only files outside the walk (hidden folders like `.private/`) get
        here at all, so the extra listdir costs nothing in practice."""
        full = os.path.join(self.root, cand)
        if not os.path.exists(full):
            return False
        head, name = os.path.split(full)
        try:
            return name in os.listdir(head or ".")
        except OSError:
            return False

    def case_variant(self, target, source):
        """The real file a link would have hit if case were ignored.

        Turns the useless "dead link" into the actionable "you wrote ZIEL.md,
        the file is Ziel.md" — the single most likely reason a vault is clean
        on a Mac and broken on the Linux box it is cloned onto."""
        tgt = target.replace("\\", "/")
        for base in (os.path.dirname(source), ""):
            for suffix in ("", ".md"):
                cand = os.path.normpath(os.path.join(base, tgt + suffix))
                real = self.by_path_ci.get(cand.replace(os.sep, "/").lower())
                if real and real != cand:
                    return real
        return None

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

def vault_mode(root):
    """(mode, why) — personal | professional | company, from the vault's CLAUDE.md.

    The mode decides which frontmatter fields are required. Guessing it from
    the folder layout would be fragile; the rules file states it outright.

    `why` is empty when the mode was really found, and says so otherwise. The
    fallback is `personal` — the LOOSEST schema, requiring neither `ownership:`
    nor the company fields. A half-finished setup still carries `{{MODE}}`, and
    that used to be measured against the loosest schema in silence: "frontmatter
    gaps: 0" on a work vault that has none of the required fields."""
    try:
        text = open(os.path.join(root, "CLAUDE.md"), encoding="utf-8-sig",
                    errors="ignore").read()
    except OSError:
        return "personal", "not detected — no CLAUDE.md in the vault root"
    # The label gets translated ("Betriebsart:", "Mode du coffre :"), the
    # VALUE does not — the kit freezes personal|professional|company. So key
    # off the value on a line that looks like a mode declaration.
    m = re.search(r"^\*\*[^\n:]{0,40}:\s*(personal|professional|company)\b",
                  text, re.M | re.I)
    if m and m.group(1).lower() in ("personal", "professional", "company"):
        return m.group(1).lower(), ""
    # A company overlay says so in its heading even before setup fills the line
    if re.search(r"^#.*company knowledge vault", text, re.M | re.I):
        return "company", ""
    if "{{MODE}}" in text:
        return "personal", ("NOT SET — CLAUDE.md still contains {{MODE}}; "
                            "setup step 5e never ran")
    return "personal", "not detected — no mode line in CLAUDE.md"

def main():
    argv = sys.argv[1:]
    limit, root = 10, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # A bare path is accepted as the vault. It used to be swallowed in
    # silence: `hygiene.py /some/vault` then scanned the tool's OWN vault and
    # printed a clean bill of health for a folder the caller never asked
    # about. A report about the wrong vault is worse than an error message.
    skip = False
    for i, a in enumerate(argv):
        if skip:
            skip = False
            continue
        if a == "--max" and i + 1 < len(argv):
            try:
                limit = max(1, int(argv[i + 1]))
            except ValueError:
                pass
            skip = True
        elif a == "--root" and i + 1 < len(argv):
            root = os.path.abspath(os.path.expanduser(argv[i + 1]))
            skip = True
        elif a.startswith("-"):
            print(__doc__.strip()); return 1
        else:
            root = os.path.abspath(os.path.expanduser(a))
    if not os.path.isdir(root):
        print(f"No vault at {root}"); return 1

    v = Vault(root)
    if not v.notes:
        print(f"hygiene — {root}\nNo notes found (is this a vault?)"); return 0

    ignores = read_ignores(root)

    def ignored(rel):
        """Inside a folder listed in `.hygieneignore`."""
        p = rel.replace(os.sep, "/")
        return any(p == i or p.startswith(i + "/") for i in ignores)

    ignored_notes = sorted(r for r in v.notes if ignored(r))
    ignored_folders = sorted({i for i in ignores
                              if any(r.replace(os.sep, "/").startswith(i)
                                     for r in ignored_notes)})

    signposts = {rel for rel in v.notes if v.is_signpost(rel)}
    inbound = collections.Counter()
    dead, signposted = [], set()
    graph = collections.defaultdict(set)
    for rel in sorted(v.notes):
        if ignored(rel):
            continue
        for target, line, raw in v.links(rel):
            hit = v.resolve(target, rel)
            if hit is None:
                variant = v.case_variant(target, rel)
                dead.append(f"{rel}:{line} → {raw}" + (
                    f"  [the file is {variant} — only the spelling differs, "
                    "which is a dead link on Linux]" if variant else ""))
            elif hit != rel:
                inbound[hit] += 1
                if hit in v.notes:
                    graph[rel].add(hit)

    # Reachable = a PATH leads here from some signpost, not just a direct
    # entry in one. Requiring the direct entry contradicted the rule the
    # vault itself states — "an index.md never lists every file, only the
    # ways in" — and made "0 unreachable" achievable only by listing every
    # file, which is the opposite of what a signpost is for. A note the
    # signpost reaches through two links is found; a note nothing leads to
    # is not, and that is the actual finding.
    queue = list(signposts)
    while queue:
        for nxt in graph.get(queue.pop(), ()):
            if nxt not in signposted:
                signposted.add(nxt)
                queue.append(nxt)

    orphans, near_empty, gaps, expired = [], [], [], []
    mode, mode_note = vault_mode(root)
    today = datetime.date.today().isoformat()
    gap_counts = collections.Counter()
    for rel, text in sorted(v.notes.items()):
        if ignored(rel):
            continue
        if not is_infra(rel) and not unlinked_ok(rel) and not inbound[rel]:
            orphans.append(rel)
        words = len(body(text).split())
        # Inbox captures are SUPPOSED to be short — friction there costs
        # captures, which is the failure this kit exists to prevent. Counting
        # them as a defect punishes exactly the behaviour the rules ask for,
        # and someone coming back after three weeks would read "six notes too
        # thin" instead of "six things you remembered".
        if not is_infra(rel) and words < NEAR_EMPTY_WORDS \
                and top_folder(rel) != "00-inbox":
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
        # Mode-dependent required fields. In a work brain `ownership:` is the
        # one field with a legal consequence — it decides what has to be handed
        # over when the job ends. A rule nothing measures is a wish.
        if mode == "professional" and not re.search(r"^ownership:\s*\S", fm, re.M):
            missing.append("no ownership:")
        if mode == "company":
            for field in ("owner", "status", "audience", "confidentiality"):
                if not re.search(rf"^{field}:\s*\S", fm, re.M):
                    missing.append(f"no {field}:")
        if missing:
            gap_counts.update(missing)
            gaps.append(f"{rel} — {', '.join(missing)}")
        # A date that expires and nobody notices is decoration. These two
        # fields promise "distrust me after this day" — so somebody has to
        # say when that day has passed.
        for field in ("stale_after", "review_due"):
            m = re.search(rf"^{field}:\s*(\d{{4}}-\d{{2}}-\d{{2}})", fm, re.M)
            if m and m.group(1) < today:
                expired.append(f"{rel} — {field}: {m.group(1)}")

    # Reachability only means something where a folder HAS a signpost —
    # otherwise the missing index.md is the finding, not the notes.
    unreachable, no_index, folders = [], [], collections.defaultdict(list)
    for rel in v.notes:
        folders[os.path.dirname(rel)].append(rel)
    for folder, members in sorted(folders.items()):
        real = sorted(r for r in members
                      if not is_infra(r) and not unlinked_ok(r) and not ignored(r))
        if not real:
            continue
        if os.path.join(folder, "index.md") in v.notes:
            unreachable += [r for r in real if r not in signposted
                            and not SUPERSEDED.search(v.notes[r])]
        else:
            no_index.append((len(real), f"{folder or '(root)'} ({len(real)} notes)"))
    no_index = [line for _, line in sorted(no_index, reverse=True)]

    chains, seen = [], set()
    # Both directions, in every language a translated vault might use. A
    # vault whose rules file was translated writes "Ersetzt durch" — matching
    # only the English would report "0 one-sided chains" on a vault full of
    # them, which is worse than not checking at all.
    # The keywords stay ENGLISH even in a translated vault — same rule as for
    # frontmatter values, and for a hard reason: "ersetzt" is an ordinary German
    # verb ("this folder replaces no system"), so matching it would flag normal
    # prose as a broken chain. Translated forms are still recognised, but only
    # at the start of a line, where a status note stands and prose does not.
    # The English form is anchored too, for the same reason as the translated
    # ones: a signpost entry like `* [x.md](x.md) - supersedes the old flow`
    # DESCRIBES a replacement, it does not declare one, and reading it as a
    # claim invented a chain whose other half could never exist. A real status
    # note stands at the start of its line (after at most a list or quote mark
    # and bold), which is exactly what spec 4.2 prescribes.
    LEAD = r"^[ \t]*(?:[-*>][ \t]*)?\**[ \t]*"
    sup = re.compile(LEAD + r"(supersedes\b|ersetzt(?! durch)\b|remplace\b)", re.I | re.M)
    supby = re.compile(LEAD + r"(superseded by\b|ersetzt durch\b|remplacé par\b)", re.I | re.M)
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
    print(f"mode: {mode}" + (f" ({mode_note})" if mode_note else ""))
    print(f"{len(v.notes)} notes scanned ({len([r for r in v.notes if is_infra(r)])} kit files, "
          f"{len(signposts)} signposts)")
    if ignored_notes:
        # Named, never silent: an exemption you cannot see is indistinguishable
        # from a check that stopped working.
        print(f"skipped via .hygieneignore: {len(ignored_notes)} notes in "
              f"{', '.join(ignored_folders)}")
    report(f"orphans — nothing links here (excl. {', '.join(UNLINKED_OK)})", orphans, limit)
    report("dead links — target does not exist", dead, limit)
    report(f"near-empty — under {NEAR_EMPTY_WORDS} words of body", near_empty, limit)
    report("not reachable from a signpost (index.md / MOC / Home)", unreachable, limit)
    report("folders with notes but no index.md (spec 3)", no_index, limit)
    report("frontmatter gaps", gaps, limit,
           note=" (" + " · ".join(f"{k} {n}" for k, n in sorted(gap_counts.items())) + ")"
           if gap_counts else "")
    report("past their own expiry date (stale_after / review_due)", expired, limit)
    report("supersede chains without a back-reference (spec 4.2)", chains, limit)
    report("unterminated ``` fence — links below it were never checked",
           v.unterminated, limit)
    portability = ([f"{r} — not valid UTF-8 (save it as UTF-8; search cannot "
                    "read it and Obsidian shows rubbish)" for r in v.mojibake]
                   + [f"{c} — names differ only in case; macOS and Windows "
                      "cannot hold both" for c in v.case_clash]
                   + v.odd_names)
    report("portability — breaks on another operating system", portability, limit)
    return 0

if __name__ == "__main__":
    sys.exit(main())
