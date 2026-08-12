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
    near-empty     notes with almost no body (a folder whose index.md
                   carries `<!-- short-notes-ok -->` is exempt)
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
# Fallbacks only. The vault's own CLAUDE.md is the authority — see
# schema_scale(). A German vault writes `roh | wachsend | ausgearbeitet` and
# `entwurf | gültig | überholt`, and comparing against the English words made
# every one of these checks quietly stop working in exactly the vault that
# had followed its own rules.
MATURITY = ("seed", "growing", "evergreen")
VALIDITY = ("draft", "stable", "deprecated")
INFRA_FILES = {"CLAUDE.md", "index.md", "Home.md", "Deadlines.md", "About me.md",
               "About this vault.md", "Inbox rule.md", "README.md",
               "THIS-COPY.md"}
# Orphans there are not a finding: captures are unlinked by definition
# (the review empties the inbox) and the archive is cold storage.
# Recognised by NUMBER, not by name. The setup asks people to keep folder
# names English, and real vaults do not: a German vault carries `90-archiv`,
# `30-wissen`, `40-entscheidungen`. Matching the English spelling meant the
# inbox and archive exemptions silently stopped applying in exactly the
# vaults that had followed the rest of the advice. The numeric prefix is
# what the numbering scheme exists for, and it survives every translation.
UNLINKED_PREFIXES = ("00-", "90-")
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

# A field the setup has not filled in yet: `<YYYY-MM-DD>`, `{{DATE}}`,
# `TO FILL IN (role)`. Not a defect of this file — the kit ships them on
# purpose and `progress.py` is what counts them down.
PLACEHOLDER = re.compile(r"^(?:<[^>]*>|\{\{[^}]*\}\}|TO FILL IN\b|AUSFÜLLEN\b)",
                         re.I)

FRONTMATTER = re.compile(r"---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", re.S)

def frontmatter(text):
    m = FRONTMATTER.match(text)
    return m.group(1) if m else ""

def body(text):
    m = FRONTMATTER.match(text)
    return text[m.end():] if m else text

def aliases(fm):
    """`aliases:` from frontmatter, both YAML spellings.

        aliases: [Jonas Reuter, J. Reuter]
        aliases:
          - Jonas Reuter
    """
    m = re.search(r"^aliases:[ \t]*(.*)$", fm, re.M)
    if not m:
        return []
    inline = m.group(1).strip()
    if inline.startswith("["):
        return [a.strip().strip("\"'") for a in inline[1:].rstrip("]").split(",")
                if a.strip()]
    if inline:
        return [inline.strip("\"'")]
    out = []
    for line in fm[m.end():].splitlines():
        if re.match(r"^[ \t]+-[ \t]*\S", line):
            out.append(line.split("-", 1)[1].strip().strip("\"'"))
        elif line.strip():
            break
    return [a for a in out if a]


# Both directions of a supersede chain, in every language a translated vault
# might use. The English keywords are frozen by the kit, but a vault whose
# rules file was translated writes "Ersetzt durch" anyway — matching only the
# English would report "0 one-sided chains" on a vault full of them, which is
# worse than not checking at all. Everything is anchored at the START of a
# line: `ersetzt` is an ordinary German verb ("this folder replaces no
# system"), and a signpost entry like `* [x.md](x.md) - supersedes the old
# flow` DESCRIBES a replacement rather than declaring one. A real status note
# stands at the start of its line, which is what spec 4.2 prescribes.
LEAD = r"^[ \t]*(?:[-*>][ \t]*)?\**[ \t]*"
SUP = re.compile(LEAD + r"(supersedes\b|ersetzt(?! durch)\b|remplace\b)", re.I | re.M)
SUPBY = re.compile(LEAD + r"(superseded by\b|ersetzt durch\b|remplacé par\b)", re.I | re.M)


def schema_scale(root, key, fallback):
    """The values THIS vault uses for `maturity:` / `status:`, in the order
    its own CLAUDE.md declares them.

    A translated vault writes `status: entwurf | gültig | überholt` in its
    rules file and in every note. Comparing against the English words made
    the legacy-schema check and the superseded exemption silently stop
    working — a check that cannot fire is indistinguishable from a clean
    vault. The rules file is the authority; English is only the fallback.
    The ORDER is what the kit freezes, not the words: position 0 is the
    unfinished state, the last position is the retired one.
    """
    try:
        with open(os.path.join(root, "CLAUDE.md"), encoding="utf-8-sig",
                  errors="ignore") as fh:
            rules = fh.read()
    except OSError:
        return list(fallback)
    # The value ends at the line comment: the schema line almost always
    # carries an explanation behind `#`.
    hit = re.search(rf"^{key}:[ \t]*([^\n#]*\|[^\n#]*?)[ \t]*(?:#.*)?$", rules, re.M)
    if not hit:
        return list(fallback)
    values = [w.strip().lower() for w in hit.group(1).split("|") if w.strip()]
    return values or list(fallback)


def superseded_pattern(retired):
    """A note that has been replaced. Dropped from its folder's index.md on
    purpose (the signpost lists what applies, not what applied), so flagging
    it forever would make "0 unreachable" impossible from the first
    replacement onwards."""
    words = "|".join(re.escape(v) for v in dict.fromkeys(list(retired) + ["deprecated"]))
    return re.compile(SUPBY.pattern + rf"|^[ \t]*status:[ \t]*(?:{words})\b",
                      re.M | re.I)


KIT_PAGE = "<!-- kit-page"


def is_infra(rel, text=""):
    """Kit scaffolding rather than a note.

    Three rules, in order of how well they survive a translation. The
    `<!-- kit-page -->` marker is the reliable one — an HTML comment is an
    exact token that renaming and translating cannot break, the same reason
    `Home.md` addresses its blocks by marker and not by heading. Then the
    structural rule, then the English name list, which only holds where
    nobody translated anything. The
    name list only holds in an English vault: a German one carries
    `Termine.md`, `Über mich.md`, `Inbox-Regel.md`, and those were then
    measured as ordinary notes — counted in `--stats`, checked for
    frontmatter, ranked in search against the notes they point at. The
    structural rule is that a vault's own pages live in its ROOT and its
    notes live in a numbered folder; that is true in every language, and it
    is what the folder map has said all along."""
    return (KIT_PAGE in text[:2000] or os.sep not in rel
            or os.path.basename(rel) in INFRA_FILES)

def top_folder(rel):
    return rel.split(os.sep)[0] if os.sep in rel else "(root)"

def unlinked_ok(rel):
    return top_folder(rel).startswith(UNLINKED_PREFIXES)


def is_inbox(rel):
    return top_folder(rel).startswith("00-")


def is_material(rel):
    """The archive's raw folder holds the SOURCES an ingest was made from —
    a PDF, an article, a transcript. They are material, not notes: no
    frontmatter, any length, nobody links to them. Every note-shaped check
    skips them, or ordinary use grows the report by one finding per source.

    Matched by shape, not by name: any `90-*` folder, any subfolder whose
    name contains `raw` (`raw/`, `raw-verarbeitet/`, `rohmaterial-raw/`)."""
    parts = rel.replace(os.sep, "/").split("/")
    return (len(parts) > 2 and parts[0].startswith("90-")
            and "raw" in parts[1].lower())


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
        # A path the walk cannot enter is not a clean path — it is an
        # UNMEASURED one. os.walk swallows the error by default, so a folder
        # without read permission simply vanished: every rubric reported zero
        # and the report was indistinguishable from a healthy vault. Anything
        # that could not be read is named in the header instead.
        self.unreadable = []
        for dirpath, dirs, files in os.walk(root, onerror=self.unreadable.append):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
            # Folder names travel too. The rubric promises "names Windows
            # refuses", and only file names were ever checked — so a folder
            # called `Q&A: 2026` or `Notizen ` passed, and the clone that
            # broke on it broke on Windows, not here.
            for d in dirs:
                bad = windows_unsafe(d)
                if bad:
                    self.odd_names.append(
                        os.path.relpath(os.path.join(dirpath, d), root) + f"/ — {bad}")
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
                    except OSError as e:
                        # Silently dropping it meant the note was in no rubric
                        # at all — not an orphan, not near-empty, not anything.
                        self.unreadable.append(e)
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
                    # `aliases:` resolves in Obsidian, so a link written
                    # against one is LIVE. Without this the tool reported
                    # every alias link as dead — while the vault's own rules
                    # tell people to put spelling variants there. The tool
                    # contradicted the rule, and the rule was right.
                    for alias in aliases(frontmatter(text)):
                        self.by_name.setdefault(norm(alias), rel)

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
        # A leading `/` means "from the vault root" — never "from the root of
        # this disk". Untouched, os.path.join throws away everything before an
        # absolute component, so `[boot](/etc/passwd)` resolved against the
        # real filesystem and was reported as a HEALTHY link: the one rubric
        # that exists to find links pointing nowhere said the link pointing
        # clean out of the vault was fine.
        tgt = tgt.lstrip("/")
        if not tgt:
            return None
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
    # A company overlay says so in its heading even before setup fills the
    # line. English only, so a translated overlay ("gemeinsames Firmenwissen")
    # falls through to the structural test below rather than to `personal`.
    if re.search(r"^#.*company knowledge vault", text, re.M | re.I):
        return "company", ""
    # Structural fallback: the FOLDERS say which mode this is, in every
    # language, because the numbering scheme is what the kit freezes.
    # `company` is the only mode with 70-/80- and without 10-/20-.
    try:
        tops = {n[:3] for n in os.listdir(root)
                if os.path.isdir(os.path.join(root, n))}
    except OSError:
        tops = set()
    if tops & {"70-", "80-"} and not tops & {"10-", "20-"}:
        return "company", "not stated in CLAUDE.md — read from the folder layout"
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

    # Ein Ordner darf in seinem EIGENEN Wegweiser erklären, dass seine
    # Notizen kurz sein sollen — ein Gedächtnis-Spiegel, ein Glossar, ein
    # Zitat-Ordner. Das ist zielgenauer als `.hygieneignore`: Nur diese
    # eine Rubrik schweigt dort, jede andere Prüfung greift weiter.
    short_ok = set()
    for rel in v.notes:
        if os.path.basename(rel) == "index.md" and "<!-- short-notes-ok" in v.notes[rel]:
            short_ok.add(os.path.dirname(rel))

    orphans, near_empty, gaps, expired = [], [], [], []
    mode, mode_note = vault_mode(root)
    # Both vocabularies stay live: a half-translated vault carries notes in
    # each, and dropping one of them only moves the blind spot.
    maturity_values = set(schema_scale(root, "maturity", MATURITY)) | set(MATURITY)
    validity_values = schema_scale(root, "status", VALIDITY)
    superseded = superseded_pattern([validity_values[-1], VALIDITY[-1]])
    today = datetime.date.today().isoformat()
    gap_counts = collections.Counter()
    for rel, text in sorted(v.notes.items()):
        if ignored(rel):
            continue
        if not is_infra(rel, text) and not unlinked_ok(rel) and not inbound[rel]:
            orphans.append(rel)
        words = len(body(text).split())
        # Inbox captures are SUPPOSED to be short — friction there costs
        # captures, which is the failure this kit exists to prevent. Counting
        # them as a defect punishes exactly the behaviour the rules ask for,
        # and someone coming back after three weeks would read "six notes too
        # thin" instead of "six things you remembered".
        if not is_infra(rel, text) and words < NEAR_EMPTY_WORDS \
                and not is_inbox(rel) and not is_material(rel) \
                and os.path.dirname(rel) not in short_ok:
            near_empty.append(f"{rel} ({words} words)")
        # Inbox captures need no frontmatter, and neither do the raw sources
        # `brain-ingest` files away: a PDF, an article, a transcript is
        # MATERIAL, not a note. Measured on a four-week test run, every
        # ingested source left a permanent finding here — one per source,
        # forever. At one source a week the report reaches fifty findings in
        # a year, and a report that is always red stops being read. The one
        # tool that finds the real problems then drowns in its own noise.
        if is_infra(rel, text) or is_inbox(rel) or is_material(rel):
            continue
        fm, missing = frontmatter(text), []
        if not re.search(r"^type:\s*\S", fm, re.M):
            missing.append("no type:")
        if not re.search(r"^created:\s*\S", fm, re.M):
            missing.append("no created:")
        s = re.search(r"^status:\s*([^\s#]+)", fm, re.M)
        if s and s.group(1).lower() in maturity_values:
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
        # A date the tool cannot READ is the worse half of the same problem.
        # The pattern used to demand exactly `\d{4}-\d{2}-\d{2}` anywhere in
        # the line, so `stale_after: "2020-01-01"` (YAML quoting), `2020-1-1`
        # (unpadded) and `01.01.2020` (the German spelling a translated vault
        # produces) all matched NOTHING — and a field that matches nothing is
        # a field that never expires. The note promised "distrust me after
        # this day" and the report stayed silent about it forever. So: read
        # the value, accept the spellings that are unambiguous, and say so
        # out loud when it cannot be read instead of assuming it is fine.
        for field in ("stale_after", "review_due"):
            m = re.search(rf"^{field}:[ \t]*(.+?)[ \t]*$", fm, re.M)
            if not m:
                continue
            value = m.group(1).split(" #")[0].strip().strip("\"'")
            iso = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})$", value)
            if iso:
                day = "%04d-%02d-%02d" % tuple(int(g) for g in iso.groups())
                if day < today:
                    expired.append(f"{rel} — {field}: {value}")
            elif value and not PLACEHOLDER.match(value):
                # An UNFILLED field is a different finding from an unreadable
                # one, and it already has an owner: `progress.py` counts
                # `<…>` and `{{…}}` as open gaps, and the setup fills them.
                # Reporting them here too made a freshly assembled vault
                # arrive with a finding it cannot fix — the report is meant
                # to start at zero, and a repair that moves it off zero on
                # day one is not a repair.
                expired.append(f"{rel} — {field}: {value!r} is not a readable "
                               "date (YYYY-MM-DD) — nothing can ever expire it")

    # Reachability only means something where a folder HAS a signpost —
    # otherwise the missing index.md is the finding, not the notes.
    unreachable, no_index, folders = [], [], collections.defaultdict(list)
    for rel in v.notes:
        folders[os.path.dirname(rel)].append(rel)
    for folder, members in sorted(folders.items()):
        real = sorted(r for r in members
                      if not is_infra(r, v.notes[r]) and not unlinked_ok(r) and not ignored(r))
        if not real:
            continue
        if os.path.join(folder, "index.md") in v.notes:
            unreachable += [r for r in real if r not in signposted
                            and not superseded.search(v.notes[r])]
        else:
            no_index.append((len(real), f"{folder or '(root)'} ({len(real)} notes)"))
    no_index = [line for _, line in sorted(no_index, reverse=True)]

    chains, seen = [], set()
    # SUP / SUPBY are defined at module level — the SAME two patterns the
    # `unreachable` exemption above uses. They were two separate regexes for a
    # while, one multilingual and one English-only, and the English-only half
    # meant a translated vault got its chains checked but never its
    # exemptions: every replaced note showed up as unreachable, forever.
    for rel in sorted(v.notes):
        for keyword, back, phrase in ((SUP, SUPBY, "Superseded by"), (SUPBY, SUP, "Supersedes")):
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
    print(f"{len(v.notes)} notes scanned ({len([r for r in v.notes if is_infra(r, v.notes[r])])} kit files, "
          f"{len(signposts)} signposts)")
    if ignored_notes:
        # Named, never silent: an exemption you cannot see is indistinguishable
        # from a check that stopped working.
        print(f"skipped via .hygieneignore: {len(ignored_notes)} notes in "
              f"{', '.join(ignored_folders)}")
    if v.unreadable:
        # Deliberately NOT a rubric: a rubric says "your vault has a defect",
        # this says "this report is incomplete". The difference matters — a
        # missing permission is a fact about the machine, not about the notes.
        print(f"could not be read, so NOT checked — {len(v.unreadable)} path(s):")
        for e in v.unreadable[:limit]:
            path = getattr(e, "filename", None) or str(e)
            print(f"  {path} — {getattr(e, 'strerror', None) or 'unreadable'}")
        if len(v.unreadable) > limit:
            print(f"  … and {len(v.unreadable) - limit} more")
    report("orphans — nothing links here (excl. inbox 00-*, archive 90-*)", orphans, limit)
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
