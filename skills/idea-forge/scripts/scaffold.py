#!/usr/bin/env python3
"""Create a new skill folder skeleton.

Usage: python scaffold.py <skill-name> <output-dir> [--refs topic1,topic2] [--scripts]

Creates SKILL.md (with frontmatter placeholders and a Field notes section),
CHANGELOG.md, BLUEPRINT.md placeholder, and optional references/ and scripts/.
Standard library only.
"""
import argparse
import re
import shutil
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

SKILL_TEMPLATE = """---
name: {name}
description: TODO what this skill does and when to use it, including likely user phrasings. Use this whenever ... even if they don't say "{name}".
---

# {title}

TODO one-paragraph purpose.

## When to use
TODO situations and phrasings. Note near-misses that should NOT use this skill.

## Method
TODO core steps, rules (with reasons), and judgment calls.
{refs_section}
## Out of scope
TODO what this skill deliberately does not do.

## Field notes
When something about this skill clearly fails or frustrates the user (a wrong assumption, a missing case, a repeated correction), note it briefly. Where files persist, append one dated line to `field-notes/{name}.md` in the working folder. Where they don't, and only if the issue was significant, mention at the end of your reply that the user can paste the note into Idea Forge to improve this skill. Keep it to one line; never interrupt the task for this.
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("name")
    p.add_argument("outdir")
    p.add_argument("--refs", default="")
    p.add_argument("--scripts", action="store_true")
    a = p.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a.name):
        raise SystemExit("Name must be lowercase and hyphenated, e.g. listing-coach")

    root = Path(a.outdir) / a.name
    if root.exists():
        raise SystemExit(f"{root} already exists; refusing to overwrite.")
    root.mkdir(parents=True)

    refs = [r.strip() for r in a.refs.split(",") if r.strip()]
    refs_section = ""
    if refs:
        (root / "references").mkdir()
        lines = ["\n## Reference files"]
        for r in refs:
            slug = re.sub(r"[^a-z0-9]+", "-", r.lower()).strip("-")
            (root / "references" / f"{slug}.md").write_text(f"# {r}\n\nTODO\n", encoding="utf-8")
            lines.append(f"- `references/{slug}.md`: read when TODO")
        refs_section = "\n".join(lines) + "\n"

    if a.scripts:
        (root / "scripts").mkdir()

    title = a.name.replace("-", " ").title()
    (root / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=a.name, title=title, refs_section=refs_section), encoding="utf-8")

    tmpl = HERE / "templates" / "CHANGELOG-template.md"
    changelog = tmpl.read_text(encoding="utf-8") if tmpl.exists() else "# Changelog\n"
    changelog = changelog.replace("<skill-name>", a.name).replace("<YYYY-MM-DD>", date.today().isoformat())
    (root / "CHANGELOG.md").write_text(changelog, encoding="utf-8")

    bp = HERE / "references" / "blueprint.md"
    (root / "BLUEPRINT.md").write_text(
        f"# Skill Blueprint: {a.name}\n\nFill from the template in Idea Forge's references/blueprint.md.\n",
        encoding="utf-8")

    print(f"Created {root}")
    for f in sorted(root.rglob("*")):
        print("  ", f.relative_to(root.parent))


if __name__ == "__main__":
    main()
