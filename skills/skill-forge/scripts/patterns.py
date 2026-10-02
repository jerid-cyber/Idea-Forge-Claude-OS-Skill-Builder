#!/usr/bin/env python3
"""Pattern library tools: lint, export contributions, and sync the community library.

Usage:
  python patterns.py lint <file.md> [...]
      Check every lesson line follows the format and contains no personal data.
  python patterns.py export <local-library.md> [--community <community-patterns.md>]
      Print the local lessons that aren't already in the community library, as
      ready-to-submit contribution blocks (seed lessons are skipped).
  python patterns.py sync <new-community-file.md> <skill-dir>
      Install a newer community library into <skill-dir>/patterns/community-patterns.md
      after linting it. Never touches your local pattern-library.md.

Lesson format (one line):
  - **<pattern>** — <why it matters> (source: <origin>[, evidence: <what happened>])
Standard library only.
"""
import re
import shutil
import sys
from pathlib import Path

LESSON = re.compile(r"^- \*\*(?P<pattern>[^*]{8,200})\*\* — (?P<why>.{8,400}) \(source: (?P<source>[^)]{2,200})\)\s*$")
PII = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "email address"),
    (re.compile(r"\b(?:\+?1[ -.]?)?\(?\d{3}\)?[ -.]?\d{3}[ -.]?\d{4}\b"), "phone number"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "ID number"),
    (re.compile(r"(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})"), "API key"),
    (re.compile(r"https?://\S+"), "URL (link to public docs only, not private pages)"),
]


def lessons(path):
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("- "):
            yield n, line


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def lint(paths):
    problems = 0
    for p in paths:
        seen = set()
        count = 0
        for n, line in lessons(p):
            count += 1
            m = LESSON.match(line)
            if not m:
                print(f"{p}:{n}: bad format. Expected: - **<pattern>** — <why> (source: <origin>)")
                problems += 1
                continue
            key = norm(m.group("pattern"))
            if key in seen:
                print(f"{p}:{n}: duplicate pattern")
                problems += 1
            seen.add(key)
            for rx, label in PII:
                if rx.search(line):
                    print(f"{p}:{n}: possible {label}; contributions must be anonymized")
                    problems += 1
        print(f"{p}: {count} lesson(s), {problems} problem(s) so far")
    return 1 if problems else 0


def export(local, community=None):
    known = set()
    if community and Path(community).exists():
        for _, line in lessons(community):
            m = LESSON.match(line)
            if m:
                known.add(norm(m.group("pattern")))
    out = []
    for n, line in lessons(local):
        m = LESSON.match(line)
        if not m:
            print(f"SKIPPED line {n} (bad format, fix it to share): {line}")
            continue
        if "seed" in m.group("source").lower() or norm(m.group("pattern")) in known:
            continue
        flags = [label for rx, label in PII if rx.search(line)]
        out.append((line, flags))
    if not out:
        print("No new lessons to contribute.")
        return 0
    print("CONTRIBUTION BLOCK (review, anonymize, then submit as a GitHub issue or PR)\n")
    for line, flags in out:
        print(line)
        if flags:
            print(f"  ^ REMOVE BEFORE SHARING: {', '.join(flags)}")
    return 0


def sync(new_file, skill_dir):
    if lint([new_file]):
        print("Refusing to install a community library that fails lint.")
        return 1
    dest = Path(skill_dir) / "patterns" / "community-patterns.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.copy2(dest, dest.with_suffix(".md.bak"))
    shutil.copy2(new_file, dest)
    print(f"Installed {dest} (previous copy saved as .bak)")
    return 0


def main(argv):
    if len(argv) < 2 or argv[0] not in {"lint", "export", "sync"}:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "lint":
        return lint(args)
    if cmd == "export":
        community = args[args.index("--community") + 1] if "--community" in args else None
        return export(args[0], community)
    if len(args) != 2:
        print(__doc__)
        return 2
    return sync(args[0], args[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
