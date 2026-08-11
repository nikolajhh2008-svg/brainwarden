#!/bin/bash
# Brainwarden — capture check (Claude Code "Stop" hook, opt-in)
#
# The problem it solves: capture is a habit, and habits lapse. You work for
# two days, decisions get made, dates get mentioned — and none of it reaches
# the brain, because nobody said "capture:".
#
# What it does: at the end of a turn, if NOTHING has been written to the
# vault for a while, it makes Claude stop and check the capture triggers
# once. If something is worth keeping, it gets captured. If not, the turn
# ends normally.
#
# What it deliberately does NOT do:
#   - it does not read your conversation
#   - it does not write anything by itself
#   - it does not run a model to decide (the pre-filter is one `find` call,
#     so it costs nothing until it actually fires)
#   - it fires at most once per window, so it can never nag
#
# Install (opt-in — the kit does not set this up for you):
#   1. cp hooks/capture-check.sh ~/.claude/hooks/
#      chmod +x ~/.claude/hooks/capture-check.sh
#   2. add it to the "Stop" hooks in ~/.claude/settings.json:
#        {"hooks": {"Stop": [{"hooks": [
#           {"type": "command", "command": "~/.claude/hooks/capture-check.sh"}
#        ]}]}}
#   3. requires `jq` (macOS: brew install jq)
#
# Uninstall: delete the file and remove the entry. Nothing else changes.

set -u

# --- vault path: read it from the global rules, same line the skills use ---
RULES="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/CLAUDE.md"
VAULT=""
if [ -f "$RULES" ]; then
  VAULT=$(grep -m1 -E '^[-*]?[[:space:]]*Brain vault:' "$RULES" 2>/dev/null \
          | sed -E 's/.*Brain vault:[[:space:]]*//; s/[[:space:]]*(<|←).*$//; s/[[:space:]]*$//')
  VAULT="${VAULT/#\~/$HOME}"
fi
[ -n "$VAULT" ] || VAULT="$HOME/Brain"

INBOX="$VAULT/00-inbox"
DECISIONS="$VAULT/40-decisions"
MARKER="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/state/brainwarden-capture-check"
WINDOW_MIN="${BRAINWARDEN_CAPTURE_WINDOW:-240}"   # default 4 hours

input=$(cat)

# Never block twice in a row — if this stop came from our own block, let go.
if command -v jq >/dev/null 2>&1; then
  if echo "$input" | jq -e '.stop_hook_active == true' >/dev/null 2>&1; then
    exit 0
  fi
fi

# No vault on this machine (someone else's computer)? Stay silent.
[ -d "$INBOX" ] || exit 0

# Already reminded within the window? Stay silent — at most one per window.
if [ -f "$MARKER" ] && [ -n "$(find "$MARKER" -mmin "-$WINDOW_MIN" 2>/dev/null)" ]; then
  exit 0
fi

# Something was written to the brain within the window? All good.
recent=$(find "$INBOX" "$DECISIONS" -name '*.md' -mmin "-$WINDOW_MIN" 2>/dev/null | head -1)
[ -n "$recent" ] && exit 0

mkdir -p "$(dirname "$MARKER")"
touch "$MARKER"

cat <<EOF
{"decision":"block","reason":"Capture check (automatic hook, at most once every ${WINDOW_MIN} minutes): nothing has reached the brain for a while. Check the capture triggers for THIS session once: (a) was a decision settled? (b) was a date or deadline named? (c) did something go live? (d) did a new person come up? (e) was a lesson learned the hard way? If YES: run brain-capture now (inbox: ${INBOX}/, decisions as a record in ${DECISIONS}/), then end the turn normally. If NO: just end the turn — invent nothing. Say in one line what you captured, or that there was nothing."}
EOF
