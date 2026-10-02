#!/usr/bin/env python3
"""Skill Forge test suite. Run from the repo root: python tests/run_tests.py

Covers: self-validation, scaffold, validator error detection, Family Forge scan
and plugin build, visual scorecard, and pattern library lint/export/sync.
Standard library only; also runs in the GitHub Action.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "skill-forge"
S = SKILL / "scripts"
FX = ROOT / "tests" / "fixtures"
results = []


def run(*args):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"\n      {detail}" if not cond and detail else ""))


def main():
    tmp = Path(tempfile.mkdtemp())

    # 1. Skill Forge validates itself
    code, out = run(S / "validate_skill.py", SKILL)
    check("skill-forge passes its own validator", code == 0 and "ERROR" not in out, out)

    # 2. Scaffold creates a skeleton the validator rejects until filled
    code, out = run(S / "scaffold.py", "demo-skill", tmp, "--refs", "Topic one")
    check("scaffold creates skill", code == 0 and (tmp / "demo-skill" / "SKILL.md").exists(), out)
    code, out = run(S / "validate_skill.py", tmp / "demo-skill")
    check("validator flags unfilled TODOs", code == 1 and "TODO" in out, out)

    # 3. Validator catches a leaked key and a missing reference
    bad = tmp / "bad-skill"
    bad.mkdir()
    (bad / "SKILL.md").write_text("---\nname: bad-skill\ndescription: x\n---\nkey sk-" + "a" * 30
                                  + "\nSee `references/missing.md`.\n", encoding="utf-8")
    code, out = run(S / "validate_skill.py", bad)
    check("validator catches leaked key", "API key" in out, out)
    check("validator catches missing reference", "missing.md" in out, out)

    # 4. Family Forge groups the listing skills, excludes bookkeeping
    code, out = run(S / "family_scan.py", FX / "skills", "--json")
    data = json.loads(out) if code == 0 else {}
    fams = data.get("families", [])
    listing_fam = next((f for f in fams if "listing-objection-handler" in f["members"]), None)
    check("family scan finds the listing family", listing_fam is not None
          and "listing-presentation-coach" in listing_fam["members"], out[:400])
    check("family scan excludes unrelated bookkeeping skill",
          all("bookkeeping-reconciler" not in f["members"] for f in fams), out[:400])
    check("family scan detects shared reference", listing_fam and "glossary.md" in listing_fam["shared_references"])
    code, out = run(S / "family_scan.py", FX / "skills" / "bookkeeping-reconciler")
    check("family scan handles a single skill gracefully", code == 0 and "at least 2" in out, out)

    # 4b. Regressions from the live 187-skill scan: boilerplate chaining,
    #     plugin awareness, designed chains
    lib = tmp / "lib"
    topics = ["tax filing estimates", "payroll timesheets", "youtube video seo", "hiring interviews",
              "inventory reorder stock", "bank reconciliation", "instagram posting calendar",
              "google maps listing", "proposal quotes bids", "newsletter subscribers"]
    tagline = " Runs the Acme 4-phase method (Discovery, Design, Build, Optimize) as an agent and proves results."
    for k, topic in enumerate(topics):
        d = lib / f"acme:skill-{k}"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"---\nname: skill-{k}\ndescription: Handles {topic} for owners.{tagline}"
                                    f" Use whenever {topic} comes up.\n---\n# {topic}\n", encoding="utf-8")
    d = lib / "other:tax-helper"
    d.mkdir()
    (d / "SKILL.md").write_text("---\nname: tax-helper\ndescription: Prepares tax filing estimates and runs "
                                "skill-0 first. Use whenever tax filing estimates come up.\n---\n# tax\n", encoding="utf-8")
    code, out = run(S / "family_scan.py", lib, "--json")
    data = json.loads(out) if code == 0 else {}
    fams = data.get("families", [])
    check("boilerplate tagline does not chain unrelated skills", all(len(f["members"]) <= 3 for f in fams),
          json.dumps(fams)[:400])
    tax = next((f for f in fams if "tax-helper" in f["members"]), {})
    acts = " ".join(tax.get("actions", []))
    check("cross-plugin overlap detected", "CROSS-PLUGIN" in acts, acts)
    check("designed chain recognized instead of merge", "CHAIN" in acts and "MERGE?" not in acts, acts)

    # 5. Plugin build
    code, out = run(S / "build_plugin.py", "listing-suite", tmp,
                    FX / "skills" / "listing-presentation-coach", FX / "skills" / "listing-objection-handler",
                    "--author", "Test")
    manifest = tmp / "listing-suite" / ".claude-plugin" / "plugin.json"
    check("plugin build creates manifest", code == 0 and manifest.exists(), out)
    if manifest.exists():
        m = json.loads(manifest.read_text())
        check("plugin manifest is valid", m["name"] == "listing-suite" and m["author"]["name"] == "Test")
        check("plugin contains both skills",
              (tmp / "listing-suite" / "skills" / "listing-objection-handler" / "SKILL.md").exists())
    code, out = run(S / "build_plugin.py", "listing-suite", tmp, FX / "skills" / "open-house-followup")
    check("plugin build refuses to overwrite", code != 0, out)

    # 6. Visual scorecard
    html_out = tmp / "score.html"
    code, out = run(S / "scorecard_chart.py", FX / "CHANGELOG-sample.md", SKILL, "-o", html_out)
    check("scorecard chart renders", code == 0 and html_out.exists(), out)
    if html_out.exists():
        doc = html_out.read_text()
        check("scorecard has no external resources", not re.search(r'(src|href)=["\']https?://', doc))
        axis = re.findall(r'text-anchor="middle">v([\d.]+)</text>', doc)
        check("scorecard sorts versions numerically", axis[:3] == ["1.0", "1.1", "1.2"], str(axis))
        check("scorecard computes delta and focus", "change <b>+4</b>" in doc and "next focus: <b>Bigger" in doc)
        check("scorecard includes skill-forge history", "skill-forge" in doc)
        check("scorecard ignores the word 'scorecard:' in changelog prose (regression)",
              re.search(r'text-anchor="middle">v1\.1</text>', doc.split("skill-forge</h2>")[1].split("</section>")[0])
              is not None)
        svgs = re.findall(r"<svg.*?</svg>", doc, re.S)
        ok = True
        for svg in svgs:
            try:
                ET.fromstring(svg.replace('viewBox', 'xmlns="http://www.w3.org/2000/svg" viewBox', 1))
            except ET.ParseError:
                ok = False
        check("scorecard SVGs are well-formed", svgs and ok)

    # 7. Pattern libraries
    code, out = run(S / "patterns.py", "lint", SKILL / "patterns" / "community-patterns.md",
                    SKILL / "patterns" / "pattern-library.md")
    check("shipped pattern libraries pass lint", code == 0, out)
    code, out = run(S / "patterns.py", "lint", FX / "bad-patterns.md")
    check("lint catches phone number, bad format, duplicate",
          code == 1 and "phone" in out and "bad format" in out and "duplicate" in out, out)
    code, out = run(S / "patterns.py", "export", FX / "local-patterns.md",
                    "--community", SKILL / "patterns" / "community-patterns.md")
    check("export skips seed/duplicate, keeps new lesson",
          "Ask about the audience" in out and "Judgment skills need" not in out, out)
    check("export flags email for removal", "REMOVE BEFORE SHARING: email" in out, out)
    check("export warns on malformed lines instead of skipping silently", "SKIPPED line 4" in out, out)
    fake = tmp / "fake-skill"
    shutil.copytree(SKILL, fake)
    code, out = run(S / "patterns.py", "sync", FX / "bad-patterns.md", fake)
    check("sync refuses a library that fails lint", code == 1, out)
    code, out = run(S / "patterns.py", "sync", SKILL / "patterns" / "community-patterns.md", fake)
    check("sync installs a clean library with backup",
          code == 0 and (fake / "patterns" / "community-patterns.md.bak").exists(), out)

    shutil.rmtree(tmp, ignore_errors=True)
    passed = sum(ok for _, ok in results)
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
