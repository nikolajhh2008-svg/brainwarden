#!/bin/sh
# Brainwarden self-check — run it before you push, nothing runs it for you.
#
#   ./check.sh          macOS · Linux · Git Bash
#   py -3 check.py      Windows PowerShell / cmd — the same checks
#
# The checks themselves live in check.py. This file only finds a python and
# hands over, so the command you already know keeps working.
#
# Why they moved: this script used to run `hygiene.py | grep -qE …` and read
# the exit status of GREP. When hygiene crashed it printed nothing, grep
# found nothing, and "no findings" was indistinguishable from "clean" — the
# self-check reported all green on three crashed runs. Checking a return
# code is the whole point of a self-check, and doing it in the language the
# kit already requires costs no new dependency and drops six (bash, mktemp,
# find, sed, grep, cp) that differ between BSD, GNU and PowerShell.
set -u
cd "$(dirname "$0")" || exit 1

for py in python3 python py; do
  if command -v "$py" >/dev/null 2>&1; then
    if [ "$py" = "py" ]; then
      exec py -3 check.py "$@"
    fi
    exec "$py" check.py "$@"
  fi
done

echo "No Python found (tried python3, python, py). Install Python 3." >&2
exit 1
