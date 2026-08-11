#!/bin/bash
# Brainwarden self-check — run it before you push, nothing runs it for you.
#
#   ./check.sh
#
# Assembles all three vault modes from the template and measures them, so a
# broken signpost or a stale reference is caught here and not by whoever
# installs the kit next. No CI service, no account, no minutes — just bash,
# python3 and about two seconds.
set -u
cd "$(dirname "$0")"
fail=0
say() { printf '%-52s %s\n' "$1" "$2"; }
bad() { say "$1" "FAIL — $2"; fail=1; }

python3 -m py_compile vault-template/.tools/search.py vault-template/.tools/hygiene.py vault-template/.tools/harvest.py \
  && say "tools compile" "ok" || bad "tools compile" "syntax error"

( cd vault-template && python3 .tools/search.py inbox --k 3 >/dev/null \
  && python3 .tools/search.py --stats >/dev/null ) \
  && say "search runs" "ok" || bad "search runs" "crashed"

test "$(ls skills | wc -l)" -eq 5 && say "five skills" "ok" || bad "five skills" "count changed"
for s in skills/*/; do test -f "$s/SKILL.md" || bad "skill $s" "no SKILL.md"; done

python3 - <<'PY' && say "manifests valid, versions agree" "ok" || bad "manifests" "invalid or mismatched"
import json, sys
p = json.load(open(".claude-plugin/plugin.json"))
m = json.load(open(".claude-plugin/marketplace.json"))
v = {p["version"], m["metadata"]["version"]} | {x["version"] for x in m["plugins"] if "version" in x}
sys.exit(0 if len(v) == 1 else 1)
PY

! grep -rn "Start here" --include="*.md" --exclude=SETUP-FOR-CLAUDE.md . >/dev/null \
  && say "no stale 'Start here'" "ok" || bad "stale reference" "'Start here' outside the update path"

# The real test: every mode, assembled the way the runbook assembles it.
for mode in personal professional company; do
  V="$(mktemp -d)/$mode"; mkdir -p "$V"
  cp -R vault-template/. "$V/" && rm -rf "$V/modules"
  [ "$mode" != "personal" ] && cp -R vault-template/modules/processes/. "$V/"
  if [ "$mode" = "company" ]; then
    cp -R vault-template/modules/company/. "$V/"
    rm -rf "$V/10-projects" "$V/20-areas" "$V/30-knowledge/people"
    rm -f "$V/About me.md" "$V/_templates/person-note.md" "$V/_templates/project-note.md" \
          "$V/_templates/area-note.md" "$V/_templates/journal-entry.md"
    rm -rf "$V/60-contribution"
    rm -f "$V/handover.md" "$V/_templates/contribution-entry.md" \
          "$V/_templates/learning-note.md" "$V/_templates/meeting-note.md"
  fi
  # the mode line drives hygiene.py's required-field check — without it a
  # work vault would be measured against the personal schema and pass by
  # accident
  sed -i.bak "s/{{MODE}}/$mode/" "$V/CLAUDE.md" && rm -f "$V/CLAUDE.md.bak"
  if ( cd "$V" && python3 .tools/hygiene.py | grep -qE "^(dead links|orphans|folders with notes but no index\.md|frontmatter gaps).*: [1-9]" ); then
    bad "$mode vault clean" "hygiene has findings"
    ( cd "$V" && python3 .tools/hygiene.py | grep -E ".*: [1-9]" | sed 's/^/    /' )
  else
    say "$mode vault clean" "ok"
  fi
  test "$(grep -o '<!-- /\?block:[a-z-]*  *-->' "$V/Home.md" | wc -l)" -eq 8 \
    && say "$mode dashboard markers" "ok" || bad "$mode dashboard markers" "not four pairs"
  # NOTE: the check must run INSIDE the vault — a `cd` in a process
  # substitution does not carry over, which made this pass a wrong path.
  if ( cd "$V" && find . -name index.md -exec dirname {} \; \
       | while IFS= read -r d; do test -f "$d/CLAUDE.md" || { echo "$d"; }; done \
       | grep -q . ); then
    bad "$mode signpost pairs" "an index.md has no CLAUDE.md"
    ( cd "$V" && find . -name index.md -exec dirname {} \; \
      | while IFS= read -r d; do test -f "$d/CLAUDE.md" || echo "    $d"; done )
  else
    say "$mode signpost pairs" "ok"
  fi
  if [ "$mode" = "company" ]; then
    grep -qE '`(10-projects|20-areas|30-knowledge/people)/`' "$V/CLAUDE.md" \
      && ! grep -qE '^\*\*No `10-projects' "$V/CLAUDE.md" \
      && bad "company rules file" "mentions folders this mode does not have" \
      || say "company rules file" "ok"
    test ! -e "$V/_templates/person-note.md" && say "no person template in company" "ok" \
      || bad "no person template in company" "person-note.md still there"
  fi
  rm -rf "$(dirname "$V")"
done

echo
[ "$fail" -eq 0 ] && echo "all checks passed" || echo "SOME CHECKS FAILED"
exit "$fail"
