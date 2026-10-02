#!/usr/bin/env python3
"""Bundle several skill folders into one plugin (Family Forge output).

Usage:
  python build_plugin.py <plugin-name> <output-dir> <skill-dir> [<skill-dir> ...]
      [--description "..."] [--author "Name"] [--version 1.0.0]

Creates:
  <output-dir>/<plugin-name>/
    .claude-plugin/plugin.json
    skills/<each skill copied>/
    README.md   (lists the family and what each skill does)
Never modifies the source skills. Refuses to overwrite an existing folder.
Standard library only.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def read_meta(skill_dir):
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+?)(?=^\w+:|\Z)", fm, re.M | re.S)
    return (name.group(1).strip() if name else skill_dir.name,
            " ".join(desc.group(1).split()) if desc else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("outdir")
    ap.add_argument("skills", nargs="+")
    ap.add_argument("--description", default="")
    ap.add_argument("--author", default="")
    ap.add_argument("--version", default="1.0.0")
    a = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a.name):
        sys.exit("Plugin name must be lowercase and hyphenated.")
    root = Path(a.outdir) / a.name
    if root.exists():
        sys.exit(f"{root} already exists; refusing to overwrite.")

    metas = []
    for s in a.skills:
        sd = Path(s).resolve()
        if not (sd / "SKILL.md").exists():
            sys.exit(f"{sd} has no SKILL.md")
        metas.append((sd, *read_meta(sd)))
    names = [m[1] for m in metas]
    if len(set(names)) != len(names):
        sys.exit("Two skills share a name; rename one before bundling.")

    (root / ".claude-plugin").mkdir(parents=True)
    (root / "skills").mkdir()
    for sd, name, _ in metas:
        shutil.copytree(sd, root / "skills" / name)

    manifest = {"name": a.name, "version": a.version,
                "description": a.description or f"A family of {len(metas)} related skills: {', '.join(names)}."}
    if a.author:
        manifest["author"] = {"name": a.author}
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    lines = [f"# {a.name}", "", manifest["description"], "", "## Skills in this family", ""]
    for _, name, desc in metas:
        short = desc.split(". ")[0].rstrip(".") + "." if desc else ""
        lines.append(f"- **{name}**: {short}")
    lines += ["", "Built with Idea Forge (Family Forge).", ""]
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"Created plugin {root}")
    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        print("  ", f.relative_to(root.parent))


if __name__ == "__main__":
    main()
