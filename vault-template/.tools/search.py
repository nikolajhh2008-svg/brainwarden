#!/usr/bin/env python3
"""Brain search: deterministic pre-search over the vault (token saver).

    python3 ~/Brain/.tools/search.py real-rates gold
    python3 ~/Brain/.tools/search.py "chilling effect" --k 5

Scoring: hits in title/filename (x5), in tags (x3), in body (x1).
Accent-insensitive (cafe matches café). Output: top-k files with
matching lines — Claude then reads ONLY those files, not the whole vault.
"""
import os, re, sys, unicodedata

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
        if not a.startswith("--"):
            terms.append(a)
        i += 1
    return terms, k

def tags_block(text):
    """Everything under a YAML `tags:` key, incl. multi-line list items."""
    m = re.search(r"^tags:(.*(?:\n[ \t]+-[^\n]*)*)", text, re.M)
    return m.group(0) if m else ""

def main():
    terms, k = parse_args(sys.argv[1:])
    if not terms:
        print("Usage: search.py <term> [term2 ...] [--k N]"); return 1
    terms = [fold(t) for t in terms]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scored = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", ".obsidian", ".tools")]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(dirpath, f)
            try:
                text = open(path, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            folded, name = fold(text), fold(f[:-3])
            tags = fold(tags_block(text))
            score, lines = 0, []
            for t in terms:
                if t in name:
                    score += 5
                if t in tags:
                    score += 3
                for line in text.splitlines():
                    if t in fold(line):
                        score += 1
                        clean = line.strip()[:120]
                        if len(lines) < 3 and clean and not line.startswith("---") and clean not in lines:
                            lines.append(clean)
            if score:
                scored.append((score, path, lines))
    scored.sort(reverse=True)
    if not scored:
        print("No hits."); return 0
    for score, path, lines in scored[:k]:
        print(f"\n[{score:>3}] {os.path.relpath(path, root)}")
        for l in lines:
            print(f"      {l}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
