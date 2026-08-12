#!/usr/bin/env python3
"""Brainwarden self-check — run it before you push, nothing runs it for you.

    ./check.sh          macOS · Linux · Git Bash
    py -3 check.py      Windows PowerShell / cmd
    python3 check.py    anywhere

Assembles all three vault modes from the template and measures them, so a
broken signpost or a stale reference is caught here and not by whoever
installs the kit next. No CI service, no account, no minutes — just python3
and about two seconds.

Why this is Python and not the bash script it used to be. Three reasons, in
the order they were found:

  1. The bash version reported "all checks passed" while hygiene.py crashed
     on all three modes. The line was `hygiene.py | grep -qE …`: in a pipe
     the exit status is grep's, a crashed tool prints nothing, grep finds
     nothing, and "no findings" reads exactly like "clean". Every check
     downstream of that pipe was decoration. Here every tool is run with
     subprocess and its RETURN CODE is checked before its output is.
  2. It measured 4 of hygiene's 8 rubrics. The grep listed dead links,
     orphans, missing index.md and frontmatter gaps — a template with a
     one-sided supersede chain, an expired note or an unreachable note
     passed. Here every rubric hygiene prints must be zero, so a rubric
     added later is enforced the day it appears, without touching this file.
  3. bash, mktemp, find, sed, grep, cp -R and rm -rf are six dependencies
     that behave differently on BSD and GNU and do not exist in PowerShell
     at all. python3 is already a hard requirement of the kit — the vault's
     own tools are written in it. So this adds nothing and removes six.

check.sh still exists and still works; it only looks for a python now.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(ROOT, "vault-template")
TOOLS = os.path.join(TEMPLATE, ".tools")
MODES = ("personal", "professional", "company")

failures = []


def say(label, verdict):
    print(f"{label:<52} {verdict}")


def ok(label):
    say(label, "ok")


def bad(label, why):
    say(label, f"FAIL — {why}")
    failures.append(label)


def run(args, **kw):
    """A tool run whose exit code actually counts."""
    return subprocess.run([sys.executable] + args, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", **kw)


def tool(name):
    return os.path.join(TOOLS, name)


# --------------------------------------------------------------- 1. compile
def load_company_drops():
    """Die Ausschlussliste aus assemble.py lesen — nie kopieren.

    Ein Prüfer mit eigener Abschrift dessen, was er prüft, driftet und
    bestätigt irgendwann die falsche Liste. Deshalb wird sie hier zur
    Laufzeit aus der einen Quelle gezogen."""
    src = os.path.join(ROOT, "assemble.py")
    try:
        with open(src, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return []
    m = re.search(r"COMPANY_DROPS\s*=\s*\[(.*?)\]", text, re.S)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


def check_compiles():
    targets = [tool(n) for n in ("search.py", "hygiene.py", "harvest.py")]
    # progress.py lebt im company-Overlay und war deshalb in keiner Liste —
    # ein Syntaxfehler darin ging grün durch, obwohl genau dieses Werkzeug
    # die eine Zahl liefert, auf die sich ein Firmen-Vault verlässt.
    prog = os.path.join(TEMPLATE, "modules", "company", ".tools", "progress.py")
    if os.path.exists(prog):
        targets.append(prog)
    targets += [os.path.join(ROOT, "hooks", n)
                for n in ("capture_check.py", "session_queue.py")]
    for extra in ("assemble.py",):                    # optional, checked if present
        p = os.path.join(ROOT, extra)
        if os.path.exists(p):
            targets.append(p)
    missing = [t for t in targets if not os.path.exists(t)]
    if missing:
        return bad("tools compile", "missing: " + ", ".join(os.path.basename(m)
                                                            for m in missing))
    r = run(["-m", "py_compile"] + targets)
    if r.returncode:
        return bad("tools compile", "syntax error: " + r.stderr.strip()[:120])
    ok(f"tools compile ({len(targets)} files)")


# ------------------------------------------------------------- 2. the tools
def check_search():
    r1 = run([tool("search.py"), "inbox", "--k", "3"], cwd=TEMPLATE)
    r2 = run([tool("search.py"), "--stats"], cwd=TEMPLATE)
    for r in (r1, r2):
        if r.returncode or "Traceback" in r.stderr:
            return bad("search runs", f"exit {r.returncode}: {r.stderr.strip()[:120]}")
    ok("search runs")


def check_harvest(tmp):
    """harvest.py was only ever compiled, never started. Run it against a
    synthetic session directory so no real transcript is read."""
    sessions = os.path.join(tmp, "sessions", "some-project")
    os.makedirs(sessions)
    events = [
        {"type": "user", "message": {"content": "ok"}},
        {"type": "user", "message": {"content":
            "Wir haben entschieden, den Termin auf den 14.09. zu verschieben."}},
        {"type": "assistant", "message": {"content": "…"}},
    ]
    with open(os.path.join(sessions, "abcd1234.jsonl"), "w", encoding="utf-8") as fh:
        for e in events:
            fh.write(json.dumps(e) + "\n")
    root = os.path.join(tmp, "sessions")
    inv = run([tool("harvest.py"), "--root", root])
    cand = run([tool("harvest.py"), "--root", root, "--candidates", "--max", "5"])
    for label, r, needle in (("inventory", inv, "sessions:"),
                             ("--candidates", cand, "candidates left:")):
        if r.returncode or "Traceback" in r.stderr:
            return bad("harvest runs", f"{label}: exit {r.returncode} "
                                       f"{r.stderr.strip()[:100]}")
        if needle not in r.stdout:
            return bad("harvest runs", f"{label}: no {needle!r} in output")
    ok("harvest runs")


def check_hooks(tmp):
    """The hooks were never compiled and never started. Run both against a
    throwaway config directory and a throwaway vault — nothing real is read
    or written."""
    cfg = os.path.join(tmp, "cfg")
    vault = os.path.join(tmp, "hookvault")
    inbox = os.path.join(vault, "00-inbox")
    os.makedirs(inbox)
    os.makedirs(cfg)
    with open(os.path.join(cfg, "CLAUDE.md"), "w", encoding="utf-8") as fh:
        fh.write(f"- Brain vault: {vault}\n")
    stale = os.path.join(inbox, "old.md")
    with open(stale, "w", encoding="utf-8") as fh:
        fh.write("an old capture\n")
    os.utime(stale, (0, 0))                  # long outside the capture window
    env = dict(os.environ, CLAUDE_CONFIG_DIR=cfg)
    hook = os.path.join(ROOT, "hooks", "%s.py")

    def call(script, payload):
        return subprocess.run([sys.executable, hook % script],
                              input=json.dumps(payload), capture_output=True,
                              text=True, encoding="utf-8", errors="replace", env=env)

    r = call("capture_check", {"stop_hook_active": True})
    if r.returncode or r.stdout.strip():
        return bad("hooks run", "capture_check does not honour stop_hook_active")
    r = call("capture_check", {})
    if r.returncode or "Traceback" in r.stderr:
        return bad("hooks run", f"capture_check: exit {r.returncode} "
                                f"{r.stderr.strip()[:100]}")
    try:
        if json.loads(r.stdout)["decision"] != "block":
            raise ValueError
    except (ValueError, KeyError, TypeError):
        return bad("hooks run", "capture_check did not block on a cold vault")
    r = call("capture_check", {})            # immediately again
    if r.stdout.strip():
        return bad("hooks run", "capture_check nags twice inside one window")

    r = call("session_queue", {"reason": "clear", "cwd": vault, "session_id": "s1"})
    if r.returncode or "Traceback" in r.stderr:
        return bad("hooks run", f"session_queue: exit {r.returncode} "
                                f"{r.stderr.strip()[:100]}")
    queue = os.path.join(cfg, "state", "brainwarden-session-queue.tsv")
    rows = [l for l in open(queue, encoding="utf-8").read().splitlines() if l.strip()]
    # when · project · session · why it ended, and possibly more later — the
    # first four are what harvest.py --queue and the weekly review read.
    fields = rows[0].split("\t") if rows else []
    if len(rows) != 1 or len(fields) < 4 or not re.match(r"\d{4}-\d\d-\d\d ", fields[0]):
        return bad("hooks run", f"queue line malformed: {rows!r}")
    call("session_queue", {"reason": "resume", "cwd": vault, "session_id": "s2"})
    rows = [l for l in open(queue, encoding="utf-8").read().splitlines() if l.strip()]
    if len(rows) != 1:
        return bad("hooks run", "session_queue recorded a `resume`")
    r = run([tool("harvest.py"), "--queue"], env=env)
    if r.returncode or "sessions in queue: 1" not in r.stdout:
        return bad("hooks run", "harvest --queue does not read the queue back")
    ok("hooks run")


# ------------------------------------------------------------- 3. the repo
def check_skills():
    skills = os.path.join(ROOT, "skills")
    dirs = sorted(d for d in os.listdir(skills)
                  if os.path.isdir(os.path.join(skills, d)))
    if len(dirs) != 5:
        return bad("five skills", f"count changed ({len(dirs)})")
    for d in dirs:
        if not os.path.isfile(os.path.join(skills, d, "SKILL.md")):
            return bad("five skills", f"{d} has no SKILL.md")
    ok("five skills")


def check_manifests():
    try:
        p = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json"),
                           encoding="utf-8"))
        m = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"),
                           encoding="utf-8"))
        versions = {p["version"], m["metadata"]["version"]} | {
            x["version"] for x in m["plugins"] if "version" in x}
    except (OSError, ValueError, KeyError) as e:
        return bad("manifests valid, versions agree", f"unreadable: {e}")
    if len(versions) != 1:
        return bad("manifests valid, versions agree", f"mismatched: {sorted(versions)}")
    ok("manifests valid, versions agree")


def check_stale_reference():
    hits = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if not f.endswith(".md") or f == "SETUP-FOR-CLAUDE.md":
                continue
            path = os.path.join(dirpath, f)
            try:
                text = open(path, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            if "Start here" in text:
                hits.append(os.path.relpath(path, ROOT))
    if hits:
        return bad("no stale 'Start here'", "outside the update path: " + ", ".join(hits))
    ok("no stale 'Start here'")


def check_kit_portability():
    """The kit itself must survive a `git clone` on Windows and on Linux."""
    spec = importlib.util.spec_from_file_location("hyg", tool("hygiene.py"))
    hyg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hyg)
    odd, seen, clash, undecodable = [], {}, [], []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for name in dirs + files:
            why = hyg.windows_unsafe(name)
            if why:
                odd.append(f"{os.path.relpath(os.path.join(dirpath, name), ROOT)} — {why}")
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
            key = rel.replace(os.sep, "/").lower()
            if key in seen:
                clash.append(f"{seen[key]} vs {rel}")
            seen[key] = rel
            if os.path.splitext(f)[1] in (".md", ".py", ".json", ".sh", ".txt"):
                try:
                    open(os.path.join(dirpath, f), encoding="utf-8-sig").read()
                except UnicodeDecodeError:
                    undecodable.append(rel)
                except OSError:
                    pass
    problems = odd + clash + [f"{r} — not valid UTF-8" for r in undecodable]
    if problems:
        return bad("kit survives clone on Windows/Linux", "; ".join(problems[:3]))
    ok("kit survives clone on Windows/Linux")


# ------------------------------------------------------ 4. the assembled vaults
def file_inventory(root):
    """Every file under root, as vault-relative paths. Used to prove that a
    second assemble run changes nothing."""
    out = set()
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in files:
            if name.endswith((".pyc", ".pyo")):
                continue
            out.add(os.path.relpath(os.path.join(dirpath, name), root))
    return out


def assemble(dest, mode):
    """Build a vault exactly the way the runbook builds it.

    There used to be a copy-then-delete fallback here for the case where
    assemble.py is missing. It was dead code that carried a live trap: it was
    the very mechanism assemble.py replaced BECAUSE it is not idempotent (the
    delete pass runs once, so a second run rebuilds every folder the first
    one removed), and it kept a SECOND copy of the company drop list, which
    is the list assemble.py's own comment says has drifted before. A checker
    holding a stale copy of the thing it checks is not a fallback."""
    script = os.path.join(ROOT, "assemble.py")
    if not os.path.exists(script):
        raise RuntimeError("assemble.py is missing — nothing to check")
    r = run([script, dest, mode, "--from", TEMPLATE])
    if r.returncode:
        raise RuntimeError(f"assemble.py failed: {r.stderr.strip()[:200]}")


def set_mode(vault, mode):
    """Fill the placeholders the way step 5e does — in EVERY file.

    The mode line drives hygiene's required-field check; without it a work
    vault is measured against the personal schema and passes by accident.
    And it used to stop there: only `{{MODE}}`, only `CLAUDE.md`. So the
    checked vault still carried `{{LANGUAGE}}` and `{{COMPANY}}` everywhere,
    and a new placeholder could never be noticed by anything.
    """
    werte = {"{{MODE}}": mode, "{{LANGUAGE}}": "English",
             "{{COMPANY}}": "Example GmbH"}
    for dirpath, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in ("_templates", ".tools", ".git")]
        for name in files:
            if not name.endswith(".md") or name == "_template.md":
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            neu = text
            for k, v in werte.items():
                neu = neu.replace(k, v)
            if neu != text:
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(neu)


REPORT = re.compile(r"^(?P<title>\S.*?): (?P<n>\d+)(?: \(.*\))?$")
# Every rubric hygiene prints must be zero — that part is automatic. What is
# NOT automatic is a rubric DISAPPEARING: this checker reads the rubrics off
# hygiene's own output, so a rubric that stops being printed simply stops
# being enforced, and the line still says "ok". The count is printed in the
# label, which made it visible and not enforced — the exact shape of check
# this file was rewritten to get rid of. So the floor is stated here, and
# raising it is the deliberate act of adding a rubric.
MIN_RUBRICS = 10


def hygiene_findings(vault):
    """(mode line, {rubric: count}) — and a crash is a crash, not `0 findings`.

    Runs the vault's OWN copy of the tool: hygiene derives the vault root from
    its own location, so calling the template's copy would measure the
    template no matter which vault you point it at."""
    r = run([os.path.join(vault, ".tools", "hygiene.py")], cwd=vault)
    if r.returncode or "Traceback" in r.stderr:
        raise RuntimeError(f"hygiene.py exit {r.returncode}: {r.stderr.strip()[:200]}")
    mode_line, counts = "", {}
    for line in r.stdout.splitlines():
        if line.startswith("mode: "):
            mode_line = line[len("mode: "):]
        m = REPORT.match(line)
        if m and not line.startswith("mode:"):
            counts[m.group("title")] = int(m.group("n"))
    if not counts:
        raise RuntimeError("hygiene.py printed no findings at all")
    return mode_line, counts


def check_mode(mode, tmp):
    vault = os.path.join(tmp, mode)
    try:
        assemble(vault, mode)
    except RuntimeError as e:
        return bad(f"{mode} vault assembles", str(e)[:120])

    # Run it a SECOND time on the same folder before anything else touches
    # it. This check exists because that case was broken and invisible: the
    # company mode rebuilt every folder it had just removed, then refused to
    # clean up because the vault "already had content". Assembling always
    # into a fresh temp directory is exactly what hid it.
    before = file_inventory(vault)
    try:
        assemble(vault, mode)
    except RuntimeError as e:
        return bad(f"{mode} assembles twice", str(e)[:120])
    after = file_inventory(vault)
    if before != after:
        added = sorted(after - before)[:4]
        bad(f"{mode} assembles twice",
            f"second run changed the vault: +{len(after - before)} "
            f"-{len(before - after)} ({', '.join(added)})")
    else:
        ok(f"{mode} assembles twice")

    set_mode(vault, mode)

    try:
        mode_line, counts = hygiene_findings(vault)
    except RuntimeError as e:
        return bad(f"{mode} vault clean", str(e)[:160])
    if mode_line != mode:
        bad(f"{mode} mode detected", f"hygiene reports {mode_line!r}")
    else:
        ok(f"{mode} mode detected")
    dirty = {k: v for k, v in counts.items() if v}
    if dirty:
        bad(f"{mode} vault clean ({len(counts)} rubrics)", "findings")
        for k, v in sorted(dirty.items()):
            print(f"    {k}: {v}")
    elif len(counts) < MIN_RUBRICS:
        bad(f"{mode} vault clean ({len(counts)} rubrics)",
            f"hygiene printed only {len(counts)} of {MIN_RUBRICS} rubrics — "
            "one stopped being measured")
    else:
        ok(f"{mode} vault clean ({len(counts)} rubrics)")

    home = open(os.path.join(vault, "Home.md"), encoding="utf-8").read()
    markers = re.findall(r"<!-- /?block:[a-z-]+ +-->", home)
    if len(markers) != 8:
        bad(f"{mode} dashboard markers", f"{len(markers)} instead of four pairs")
    else:
        ok(f"{mode} dashboard markers")

    unpaired = []
    for dirpath, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if "index.md" in files and "CLAUDE.md" not in files:
            unpaired.append(os.path.relpath(dirpath, vault))
    if unpaired:
        bad(f"{mode} signpost pairs", "index.md without CLAUDE.md: " + ", ".join(unpaired))
    else:
        ok(f"{mode} signpost pairs")

    # Ein Platzhalter-Inventar statt nur {{MODE}}. Vorher konnte ein neuer
    # Token ({{TIMEZONE}}, {{FIRMA}}) unbemerkt im ausgelieferten Vault
    # stehen bleiben — die Prüfung kannte genau einen.
    rest = set()
    for dirpath, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in ("_templates", ".tools", ".git", ".claude")]
        for name in files:
            if not name.endswith(".md") or name == "_template.md":
                continue
            try:
                with open(os.path.join(dirpath, name), encoding="utf-8") as fh:
                    rest.update(re.findall(r"\{\{[A-Z_]+\}\}", fh.read()))
            except OSError:
                continue
    # {{DATE}} und {{NAME}} füllt erst das Runbook je Notiz — hier ist der
    # Vault noch roh, also gehören sie nicht in diese Prüfung.
    rest -= {"{{DATE}}", "{{NAME}}"}
    if rest:
        bad(f"{mode} placeholders resolved", "still unset: " + ", ".join(sorted(rest)))
    else:
        ok(f"{mode} placeholders resolved")

    # Ein Wegweiser, aus dem jemand die Einstiege entfernt hat, sieht für
    # jede bisherige Prüfung gesund aus: Datei da, CLAUDE.md daneben, keine
    # toten Links. Er führt nur nirgendwo mehr hin.
    leer = []
    for dirpath, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "_templates"]
        if "index.md" not in files:
            continue
        hat_notizen = any(f.endswith(".md") and f not in ("index.md", "CLAUDE.md")
                          for f in files)
        if not hat_notizen:
            continue
        with open(os.path.join(dirpath, "index.md"), encoding="utf-8") as fh:
            inhalt = fh.read()
        if not re.search(r"\]\([^)]+\.md\)", inhalt):
            leer.append(os.path.relpath(dirpath, vault) or "(root)")
    if leer:
        bad(f"{mode} signposts lead somewhere", "no entry points: " + ", ".join(leer[:3]))
    else:
        ok(f"{mode} signposts lead somewhere")

    if mode == "company":
        rules = open(os.path.join(vault, "CLAUDE.md"), encoding="utf-8").read()
        mentions = re.search(r"`(10-projects|20-areas|30-knowledge/people)/`", rules)
        disclaims = re.search(r"^\*\*No `10-projects", rules, re.M)
        if mentions and not disclaims:
            bad("company rules file", "mentions folders this mode does not have")
        else:
            ok("company rules file")
        # Die GANZE Ausschlussliste, nicht nur ein Eintrag. Vorher war 1 von
        # 13 geprüft: elf Dateien und zwei Ordner hätten unbemerkt in einem
        # geteilten Vault landen können — darunter `About me.md` und
        # `handover.md`, die es dort per Definition nicht gibt.
        drops = load_company_drops()
        reste = [d for d in drops
                 if os.path.exists(os.path.join(vault, *d.split("/")))]
        if reste:
            bad("company drop list honoured",
                f"{len(reste)} of {len(drops)} still there: {', '.join(reste[:3])}")
        else:
            ok(f"company drop list honoured ({len(drops)} entries)")


# The vault a real translation produces. Every entry here is copied from a
# live German vault, not invented: `90-archiv`, `Termine.md`, `Über mich.md`,
# `Inbox-Regel.md`, and a `status:` scale in German.
TRANSLATED_DIRS = {"10-projects": "10-projekte", "20-areas": "20-bereiche",
                   "30-knowledge": "30-wissen", "40-decisions": "40-entscheidungen",
                   "50-processes": "50-prozesse", "90-archive": "90-archiv"}
TRANSLATED_FILES = {"Deadlines.md": "Termine.md", "About me.md": "Über mich.md",
                    "Inbox rule.md": "Inbox-Regel.md"}
TRANSLATED_SCALES = {"maturity": "roh | wachsend | ausgearbeitet",
                     "status": "entwurf | gültig | überholt"}
# …and the notes then carry those words, which is the half that actually
# breaks things: a tool comparing against `stable` reports "0 verified" on a
# vault where everything is `gültig`, and reports it in the same calm voice
# as a vault where nothing is verified yet.
TRANSLATED_VALUES = {"seed": "roh", "growing": "wachsend", "evergreen": "ausgearbeitet",
                     "draft": "entwurf", "stable": "gültig", "deprecated": "überholt"}


def translation_pairs():
    """Every spelling a link to a renamed kit file can have: the file name,
    its percent-encoded form (`About%20me.md`, which is what a Markdown link
    to a name with a space looks like) and the bare stem a `[[wikilink]]`
    uses. Longest first, so `Deadlines.md` is rewritten before `Deadlines`."""
    pairs = list(TRANSLATED_DIRS.items())
    for old, new in TRANSLATED_FILES.items():
        o, n = os.path.splitext(old)[0], os.path.splitext(new)[0]
        pairs += [(old, new), (old.replace(" ", "%20"), new.replace(" ", "%20")),
                  (o, n)]
    return sorted(pairs, key=lambda p: -len(p[0]))


def translate(vault):
    """Turn an assembled vault into the vault a German setup actually leaves
    behind: translated folder names, translated kit file names, a translated
    schema scale and a translated mode LABEL (the value stays)."""
    pairs = translation_pairs()
    for dirpath, _dirs, files in os.walk(vault):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for old, new in pairs:
                text = text.replace(old, new)
            if os.path.dirname(path) == vault and name == "CLAUDE.md":
                for key, scale in TRANSLATED_SCALES.items():
                    text = re.sub(rf"^{key}:[ \t]*[^\n#]*\|[^\n#]*?([ \t]*#|$)",
                                  lambda m, k=key, s=scale: f"{k}: {s}{m.group(1)}",
                                  text, flags=re.M)
                text = text.replace("**Vault mode:", "**Betriebsart:")
            else:
                text = re.sub(r"^(maturity|status):[ \t]*(\w+)[ \t]*$",
                              lambda m: f"{m.group(1)}: "
                                        f"{TRANSLATED_VALUES.get(m.group(2), m.group(2))}",
                              text, flags=re.M)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
    for old, new in TRANSLATED_FILES.items():
        for dirpath, _dirs, files in os.walk(vault):
            if old in files:
                os.rename(os.path.join(dirpath, old), os.path.join(dirpath, new))
    for old, new in TRANSLATED_DIRS.items():
        src = os.path.join(vault, old)
        if os.path.isdir(src):
            os.rename(src, os.path.join(vault, new))


def check_translated_vault(tmp):
    """A translated vault must measure exactly like an English one.

    This is the check that closes a whole family of bugs rather than one bug.
    Every single one of them was the same mistake — a tool recognising
    something by an ENGLISH word that a human is invited to translate: the
    archive by `90-archive`, the decisions folder by `40-decisions`, the
    deadline page by `Deadlines.md`, the schema by `draft|stable|deprecated`,
    a replaced note by `status: deprecated`. Each was found by hand, months
    apart, and each time only at the one place it was noticed. The failure
    mode is always silence: the check does not crash, it just stops finding
    anything, and a report that finds nothing is indistinguishable from a
    clean vault. So the whole class is measured here, once, and any new
    English literal anywhere in the tools shows up as a finding on a vault
    that is provably correct."""
    vault = os.path.join(tmp, "uebersetzt")
    try:
        assemble(vault, "personal")
    except RuntimeError as e:
        return bad("translated vault measures clean", str(e)[:120])
    set_mode(vault, "personal")
    translate(vault)

    try:
        mode_line, counts = hygiene_findings(vault)
    except RuntimeError as e:
        return bad("translated vault measures clean", str(e)[:160])
    if mode_line != "personal":
        return bad("translated vault measures clean",
                   f"mode lost in translation: {mode_line!r}")
    if len(counts) < MIN_RUBRICS:
        return bad("translated vault measures clean",
                   f"only {len(counts)} of {MIN_RUBRICS} rubrics ran")
    dirty = {k: v for k, v in counts.items() if v}
    if dirty:
        bad("translated vault measures clean",
            "; ".join(f"{k}: {v}" for k, v in sorted(dirty.items()))[:200])
        return
    # The two folders the capture hook watches must still be found — by
    # number, never by name. This was a real bug: a captured decision landed
    # in `40-entscheidungen`, the hook looked for `40-decisions`, found
    # nothing, and counted the turn as "nothing reached the brain".
    sys.path.insert(0, os.path.join(ROOT, "hooks"))
    try:
        import capture_check
        inbox, decisions = capture_check.watched_folders(vault)
    except ImportError:
        return bad("translated vault measures clean", "capture_check not importable")
    finally:
        sys.path.pop(0)
    if not inbox or not decisions:
        return bad("translated vault measures clean",
                   f"hook lost a watched folder: inbox={inbox}, decisions={decisions}")
    # And the vault's own pages must still count as kit files, not as notes.
    r = run([os.path.join(vault, ".tools", "search.py"), "--stats"], cwd=vault)
    if r.returncode or "Traceback" in r.stderr:
        return bad("translated vault measures clean",
                   f"search --stats: exit {r.returncode} {r.stderr.strip()[:100]}")
    m = re.search(r"^notes: (\d+)", r.stdout, re.M)
    if not m or int(m.group(1)):
        return bad("translated vault measures clean",
                   f"search counts {m.group(1) if m else '?'} notes in an empty "
                   "vault — a translated kit page is being read as a note")
    ok("translated vault measures clean")


def check_promise_not_to_overwrite(tmp):
    """`assemble.py` prints "Nothing will be overwritten — existing files are
    kept". That sentence used to be false: an earlier version copied
    everything and then deleted the scaffolding, and it deleted somebody
    else's notes along with it. It was fixed, and then it was true because
    the code happened to be right, which is not the same as being checked.

    A promise printed to a human who is deciding whether to trust this thing
    is the last place to rely on a code path staying correct by accident. So
    it is measured: fill a folder, assemble all three modes on top of it, and
    require every pre-existing byte to still be there."""
    vault = os.path.join(tmp, "adopted")
    mine = {"30-wissen/eigene.md": "meine Notiz, die niemand anfassen darf\n",
            "Home.md": "# Mein eigenes Home\n",
            ".obsidian/app.json": "{}\n",
            "40-entscheidungen/2026-01-01-alt.md": "alt\n"}
    for rel, text in mine.items():
        path = os.path.join(vault, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    for mode in MODES:
        try:
            assemble(vault, mode)
        except RuntimeError as e:
            return bad("assemble keeps its no-overwrite promise", str(e)[:120])
    broken = []
    for rel, text in mine.items():
        path = os.path.join(vault, *rel.split("/"))
        if not os.path.exists(path):
            broken.append(f"{rel} was DELETED")
        elif open(path, encoding="utf-8").read() != text:
            broken.append(f"{rel} was OVERWRITTEN")
    if broken:
        return bad("assemble keeps its no-overwrite promise", "; ".join(broken))
    ok("assemble keeps its no-overwrite promise")


NUMBERS = re.compile(r"(\d+) of (\d+) notes verified.*?\((\d+) stable"
                     r".*?(\d+) open gaps in (\d+) files", re.S)


def check_translated_company(tmp):
    """The company vault's own number, measured in both languages.

    `progress.py` leads with "how many notes has a human released" — and it
    decided that by looking for the literal word `stable`. In a vault whose
    scale is `entwurf | gültig | überholt` that number is zero forever, and
    zero is exactly what a brand-new vault legitimately reports. The tool
    would have said the same thing whether the vault was empty or fully
    released. So: build the same vault twice, translate one, and require
    both to report the SAME numbers."""
    out = {}
    for label, tongue in (("en", False), ("de", True)):
        vault = os.path.join(tmp, f"firma-{label}")
        try:
            assemble(vault, "company")
        except RuntimeError as e:
            return bad("progress.py counts the same in any language", str(e)[:120])
        if tongue:
            translate(vault)
        r = run([os.path.join(vault, ".tools", "progress.py"), vault])
        if r.returncode or "Traceback" in r.stderr:
            return bad("progress.py counts the same in any language",
                       f"{label}: exit {r.returncode} {r.stderr.strip()[:100]}")
        m = NUMBERS.search(r.stdout)
        if not m:
            return bad("progress.py counts the same in any language",
                       f"{label}: cannot read its own summary back")
        out[label] = m.groups()
    if out["en"] != out["de"]:
        return bad("progress.py counts the same in any language",
                   f"english {out['en']} vs translated {out['de']}")
    ok("progress.py counts the same in any language")


def check_mode_guard(tmp):
    """The checker's own alarm: an unreplaced {{MODE}} must be VISIBLE.

    hygiene falls back to `personal` — the loosest schema — when it cannot
    read the mode. A half-finished setup would otherwise be measured against
    the wrong rules and report a clean bill of health forever."""
    vault = os.path.join(tmp, "no-mode")
    try:
        assemble(vault, "professional")          # deliberately no set_mode()
        mode_line, _ = hygiene_findings(vault)
    except RuntimeError as e:
        return bad("unset {{MODE}} is reported", str(e)[:120])
    if "NOT SET" not in mode_line:
        return bad("unset {{MODE}} is reported",
                   f"hygiene silently assumed {mode_line!r}")
    ok("unset {{MODE}} is reported")


def main():
    check_compiles()
    check_search()
    check_skills()
    check_manifests()
    check_stale_reference()
    check_kit_portability()
    with tempfile.TemporaryDirectory() as tmp:
        check_harvest(tmp)
        check_hooks(tmp)
        check_mode_guard(tmp)
        check_translated_vault(tmp)
        check_translated_company(tmp)
        check_promise_not_to_overwrite(tmp)
        for mode in MODES:
            check_mode(mode, tmp)
    print()
    if failures:
        print(f"SOME CHECKS FAILED ({len(failures)}): " + ", ".join(failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
