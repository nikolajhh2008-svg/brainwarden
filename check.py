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
def check_compiles():
    targets = [tool(n) for n in ("search.py", "hygiene.py", "harvest.py")]
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
    if len(rows) != 1 or len(rows[0].split("\t")) != 5:
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
def assemble(dest, mode):
    """Build a vault exactly the way the runbook builds it."""
    script = os.path.join(ROOT, "assemble.py")
    if os.path.exists(script):
        r = run([script, dest, mode, "--from", TEMPLATE])
        if r.returncode:
            raise RuntimeError(f"assemble.py failed: {r.stderr.strip()[:200]}")
        return
    shutil.copytree(TEMPLATE, dest)
    shutil.rmtree(os.path.join(dest, "modules"))
    if mode != "personal":
        overlay(os.path.join(TEMPLATE, "modules", "processes"), dest)
    if mode == "company":
        overlay(os.path.join(TEMPLATE, "modules", "company"), dest)
        for d in ("10-projects", "20-areas", os.path.join("30-knowledge", "people"),
                  "60-contribution"):
            shutil.rmtree(os.path.join(dest, d), ignore_errors=True)
        for f in ("About me.md", "handover.md",
                  *(os.path.join("_templates", n) for n in
                    ("person-note.md", "project-note.md", "area-note.md",
                     "journal-entry.md", "contribution-entry.md",
                     "learning-note.md", "meeting-note.md"))):
            try:
                os.remove(os.path.join(dest, f))
            except OSError:
                pass


def overlay(src, dest):
    for dirpath, _dirs, files in os.walk(src):
        rel = os.path.relpath(dirpath, src)
        target = os.path.normpath(os.path.join(dest, rel))
        os.makedirs(target, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(dirpath, f), os.path.join(target, f))


def set_mode(vault, mode):
    """The mode line drives hygiene's required-field check — without it a work
    vault is measured against the personal schema and passes by accident."""
    path = os.path.join(vault, "CLAUDE.md")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.replace("{{MODE}}", mode))


REPORT = re.compile(r"^(?P<title>\S.*?): (?P<n>\d+)(?: \(.*\))?$")


def hygiene_findings(vault):
    """(mode line, {rubric: count}) — and a crash is a crash, not `0 findings`."""
    r = run([tool("hygiene.py")], cwd=vault)
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

    if mode == "company":
        rules = open(os.path.join(vault, "CLAUDE.md"), encoding="utf-8").read()
        mentions = re.search(r"`(10-projects|20-areas|30-knowledge/people)/`", rules)
        disclaims = re.search(r"^\*\*No `10-projects", rules, re.M)
        if mentions and not disclaims:
            bad("company rules file", "mentions folders this mode does not have")
        else:
            ok("company rules file")
        if os.path.exists(os.path.join(vault, "_templates", "person-note.md")):
            bad("no person template in company", "person-note.md still there")
        else:
            ok("no person template in company")


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
