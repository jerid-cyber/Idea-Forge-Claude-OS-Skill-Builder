#!/usr/bin/env python3
"""Validate a skill folder built by Skill Forge.

Usage: python validate_skill.py <path-to-skill-folder>

Errors must be fixed. Warnings are judgment calls worth raising in Temper.
Standard library only, so it runs in Claude.ai, Cowork, and Claude Code.
"""
import re
import sys
from pathlib import Path


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    current = None
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if kv:
            current = kv.group(1)
            fm[current] = kv.group(2).strip()
        elif current and line.startswith((" ", "\t")):
            fm[current] += " " + line.strip()
    return fm, text[m.end():]


def main(path):
    root = Path(path).resolve()
    errors, warnings = [], []
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: {skill_md} not found")
        return 1

    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append("SKILL.md is missing YAML frontmatter (--- ... ---).")
        fm = {}

    name = fm.get("name", "")
    desc = fm.get("description", "").strip("\"'")
    if not name:
        errors.append("Frontmatter is missing 'name'.")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        errors.append(f"name '{name}' should be lowercase and hyphenated.")
    elif name != root.name:
        warnings.append(f"name '{name}' doesn't match folder name '{root.name}'.")

    if not desc:
        errors.append("Frontmatter is missing 'description'.")
    else:
        if len(desc) > 1024:
            errors.append(f"description is {len(desc)} characters; keep it at or under 1024.")
        if len(desc) < 120:
            warnings.append("description is short; skills tend to under-trigger. Add when-to-use phrasings.")
        if not re.search(r"\b(use (this|when|whenever)|whenever|when (the )?(user|someone|they))\b", desc, re.I):
            warnings.append("description doesn't say WHEN to use the skill.")
        if "<" in desc or ">" in desc:
            errors.append("description contains angle brackets, which can break skill loading.")

    lines = body.count("\n") + 1
    if lines > 500:
        errors.append(f"SKILL.md body is {lines} lines; split detail into references/ (ceiling 500).")
    elif lines > 300:
        warnings.append(f"SKILL.md body is {lines} lines; consider moving detail to references/.")

    # Referenced files exist
    for ref in sorted(set(re.findall(r"`((?:references|scripts|templates|assets|patterns)/[^`\s]+)`", text))):
        if "<" in ref:
            continue
        if not (root / ref).exists():
            errors.append(f"SKILL.md references '{ref}', which doesn't exist.")

    # Orphaned reference files
    for sub in ("references",):
        d = root / sub
        if d.is_dir():
            for f in d.rglob("*.md"):
                rel = f.relative_to(root).as_posix()
                if rel not in text and f.name not in text:
                    warnings.append(f"'{rel}' isn't mentioned in SKILL.md; Claude may never read it.")

    # Long reference files need a table of contents
    for f in root.rglob("*.md"):
        if f == skill_md:
            continue
        content = f.read_text(encoding="utf-8")
        if content.count("\n") > 300 and not re.search(r"(?i)table of contents|^## contents", content, re.M):
            warnings.append(f"'{f.relative_to(root)}' is over 300 lines without a table of contents.")

    # Secrets / personal data smell test
    secret_pat = re.compile(r"(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|api[_-]?key\s*[:=]\s*['\"][^'\"]{8,})", re.I)
    for f in root.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".py", ".json", ".txt", ".yaml", ".yml"}:
            if secret_pat.search(f.read_text(encoding="utf-8", errors="ignore")):
                errors.append(f"'{f.relative_to(root)}' appears to contain an API key or secret.")

    # Unfinished placeholders
    for f in root.rglob("*.md"):
        if f.name == "BLUEPRINT.md" or "template" in f.name.lower():
            continue
        if re.search(r"\bTODO\b", f.read_text(encoding="utf-8")):
            errors.append(f"'{f.relative_to(root)}' still contains TODO placeholders.")

    # Field notes hook
    if "field notes" not in text.lower() and name != "skill-forge":
        warnings.append("No 'Field notes' section; Evolve won't get real-use feedback.")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN:  {w}")
    if not errors and not warnings:
        print("OK: no issues found.")
    elif not errors:
        print(f"OK with {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
