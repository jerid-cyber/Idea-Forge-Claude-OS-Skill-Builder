#!/usr/bin/env python3
"""Validate an operating system (OS) plugin.

Usage:
  python validate_os.py <os-folder> [--json]
  python validate_os.py <folder-of-skills> --prefix get-found-os: [--json]

Strict mode (the folder has os.json): checks the system against its design:
every skill exists, the orchestrator names every component, every field read is
written somewhere, every handoff target exists, wave 1 is reachable, and auto
authority isn't used for external actions.

Inferred mode (no os.json, e.g. an OS built by hand): finds the orchestrator,
setup, heartbeat, and brain file from the skills themselves, then checks routing
coverage, brain usage, broken skill references, and approval gates on
external actions. --prefix selects skills named "<prefix><skill>".

Errors break the system. Warnings are worth a look in Temper.
Standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

EXTERNAL = re.compile(r"\b(send|sends|sending|email the|text the|publish|publishes|post to|posts to|"
                      r"charge|spend|pay |payment run|delete|deletes|refund|launch(?:es)? (?:the )?(?:campaign|ad))\b", re.I)
GATE = re.compile(r"\b(approv\w*|confirm\w*|permission|sign[- ]off|explicit yes|never sends? on its own|draft)\b", re.I)


def read(p):
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def skill_dirs(root, prefix=""):
    dirs = {}
    for s in sorted(root.rglob("SKILL.md")):
        folder = s.parent.name
        if prefix and not folder.startswith(prefix):
            continue
        m = re.search(r"^name:\s*(.+)$", read(s), re.M)
        name = m.group(1).strip().strip("\"'") if m else folder
        dirs[name] = s.parent
    return dirs


def full_text(d):
    """SKILL.md plus its reference files: routing tables often live in references."""
    parts = [read(d / "SKILL.md")]
    parts += [read(f) for f in sorted((d / "references").glob("*.md"))] if (d / "references").is_dir() else []
    return "\n".join(parts)


def body(d):
    t = read(d / "SKILL.md")
    m = re.match(r"^---\s*\n.*?\n---\s*\n", t, re.S)
    return t[m.end():] if m else t


def mentions(text, name):
    return re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", text) is not None


def gate_check(name, d, warnings):
    b = body(d)
    for para in re.split(r"\n\s*\n", b):
        if EXTERNAL.search(para) and not GATE.search(para) and not GATE.search(b[:1500]):
            snippet = " ".join(para.split())[:110]
            warnings.append(f"{name}: external action without a visible approval step: \"{snippet}...\"")
            return


def strict(root, spec):
    errors, warnings = [], []
    dirs = skill_dirs(root / "skills" if (root / "skills").is_dir() else root)
    comps = spec.get("components", [])
    names = [c["skill"] for c in comps]
    system = {"orchestrator": spec.get("orchestrator"), "setup": spec.get("setup"),
              "heartbeat": (spec.get("heartbeat") or {}).get("skill")}

    for role, n in system.items():
        if not n:
            (errors if role == "orchestrator" else warnings).append(f"os.json has no {role}.")
        elif n not in dirs:
            errors.append(f"{role} skill '{n}' not found.")
    for n in names:
        if n not in dirs:
            errors.append(f"component '{n}' not found in skills/.")
    if len(set(names)) != len(names):
        errors.append("duplicate component names in os.json.")

    orch = system["orchestrator"]
    if orch in dirs:
        ot = full_text(dirs[orch])
        for n in names:
            if not mentions(ot, n):
                errors.append(f"orchestrator never mentions component '{n}', so it can never route there.")
        if system["setup"] and not mentions(ot, system["setup"]):
            warnings.append("orchestrator doesn't call the setup skill when the brain is missing.")

    brain = spec.get("brain", {})
    fields = set(brain.get("fields", []))
    brain_file = brain.get("file", "")
    written = {f for c in comps for f in c.get("writes", [])} | ({"profile"} if "profile" in fields else set())
    read_fields = {f for c in comps for f in c.get("reads", [])}
    for c in comps:
        for f in c.get("reads", []) + c.get("writes", []):
            if fields and f not in fields:
                errors.append(f"'{c['skill']}' uses brain field '{f}', which isn't declared in os.json brain.fields.")
        for f in c.get("reads", []):
            if f not in written:
                errors.append(f"'{c['skill']}' reads '{f}', but no component or setup writes it.")
        for t in c.get("hands_off_to", []):
            if t not in names and t not in system.values():
                errors.append(f"'{c['skill']}' hands off to '{t}', which doesn't exist.")
        auth = c.get("authority")
        if auth not in {"auto", "approve", "suggest"}:
            errors.append(f"'{c['skill']}' has authority '{auth}'; use auto, approve, or suggest.")
        d = dirs.get(c["skill"])
        if d:
            b = body(d)
            if brain_file and (c.get("reads") or c.get("writes")) and Path(brain_file).name not in b:
                warnings.append(f"'{c['skill']}' never mentions the brain file ({brain_file}).")
            if auth == "auto" and EXTERNAL.search(b):
                errors.append(f"'{c['skill']}' is 'auto' but its instructions include external actions; use 'approve'.")
            if "TODO" in b:
                warnings.append(f"'{c['skill']}' still has TODO placeholders.")
    for f in fields - read_fields - {"profile", "next_moves", "current_state"}:
        warnings.append(f"brain field '{f}' is never read by any component.")

    # Dead ends: components that hand off nowhere and aren't the last step back to the orchestrator
    for c in comps:
        d = dirs.get(c["skill"])
        if not c.get("hands_off_to") and d and orch and not mentions(body(d), orch):
            warnings.append(f"'{c['skill']}' hands off nowhere and never returns to the orchestrator (dead end).")

    for role, n in system.items():
        if n in dirs and "TODO" in body(dirs[n]):
            warnings.append(f"{role} skill '{n}' still has TODO placeholders.")
    tmpl = root / "os-template"
    if tmpl.is_dir():
        for f in sorted(tmpl.glob("*.md")):
            if "TODO" in read(f):
                warnings.append(f"os-template/{f.name} still has TODO placeholders.")

    wave1 = [c for c in comps if c.get("wave", 1) == 1]
    if not wave1:
        errors.append("no wave 1 components: there's no minimum viable OS.")
    if not spec.get("scoreboard", {}).get("metric") or "TODO" in spec.get("scoreboard", {}).get("metric", ""):
        warnings.append("scoreboard metric isn't defined yet.")
    return errors, warnings, {"mode": "strict", "skills": len(dirs), "components": len(names),
                              "orchestrator": orch, "brain": brain_file}


def inferred(root, prefix):
    errors, warnings = [], []
    dirs = skill_dirs(root, prefix)
    if len(dirs) < 3:
        return [f"found only {len(dirs)} skill(s); an OS needs more. Check the folder or --prefix."], [], {}

    def find(pattern):
        hits = [n for n in dirs if re.search(pattern, n)]
        if not hits:
            hits = [n for n, d in dirs.items()
                    if re.search(pattern, re.search(r"^description:\s*(.*)$", read(d / "SKILL.md"), re.M | re.I).group(1)
                                 if re.search(r"^description:", read(d / "SKILL.md"), re.M) else "", re.I)]
        return hits[0] if hits else None

    orch = find(r"command-center|orchestrat|router|hub$")
    setup = find(r"brain-setup|setup|onboard")
    # Heartbeat: only names or descriptions that clearly mean a schedule runner.
    # Words like "autopilot" in a skill name are too loose and caused false matches.
    beat = find(r"heartbeat|scheduler")
    # Shared brain: a file most skills read. Prefer brain/memory names; accept others
    # only when they're clearly shared. Report "none" rather than guess.
    brain_hits = {}
    for d in dirs.values():
        for f in set(re.findall(r"[\w./-]*\.md", read(d / "SKILL.md"))):
            f = f.lstrip("./")
            # Shared guideline files (style, safety rules) are references, not memory,
            # so only state-like names count as a brain.
            if re.search(r"brain|memory|state|context", Path(f).name):
                brain_hits[f] = brain_hits.get(f, 0) + 1
    brain = None
    for f, count in sorted(brain_hits.items(), key=lambda kv: -kv[1]):
        if count >= max(2, 0.25 * len(dirs)):
            brain = f
            break

    if not orch:
        errors.append("no orchestrator found (a command-center, router, or orchestrator skill).")
    if not brain:
        warnings.append("no shared brain file found: no memory file is read by most skills, so components "
                        "may not share what they learn (it may use another memory mechanism; check before changing anything).")
    if not setup:
        warnings.append("no setup skill found to create the brain.")
    if not beat:
        warnings.append("no heartbeat skill found; the OS only runs when asked.")

    components = [n for n in dirs if n not in {orch, setup, beat}]
    if orch:
        ot = full_text(dirs[orch])
        unrouted = [n for n in components if not mentions(ot, n)]
        for n in unrouted:
            errors.append(f"orchestrator never mentions '{n}', so it can't route there.")
    if brain:
        name = Path(brain).name
        no_brain = [n for n in components if name not in read(dirs[n] / "SKILL.md")]
        for n in no_brain:
            warnings.append(f"'{n}' never mentions the brain ({name}).")
    # Broken references: a backticked name that looks like a skill in this OS but doesn't exist
    known = set(dirs)
    stems = {re.sub(r"-[^-]+$", "", n) for n in known}
    for n, d in dirs.items():
        for ref in set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+){1,})`", body(d))):
            if ref not in known and re.sub(r"-[^-]+$", "", ref) in stems and not ref.endswith((".md", "-md")):
                warnings.append(f"'{n}' references `{ref}`, which isn't a skill in this OS.")
    for n, d in dirs.items():
        gate_check(n, d, warnings)
    return errors, warnings, {"mode": "inferred", "skills": len(dirs), "components": len(components),
                              "orchestrator": orch, "setup": setup, "heartbeat": beat, "brain": brain}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--prefix", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = Path(a.folder).resolve()
    spec_path = root / "os.json"
    if spec_path.exists():
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERROR: os.json is not valid JSON: {e}")
            return 1
        errors, warnings, info = strict(root, spec)
    else:
        errors, warnings, info = inferred(root, a.prefix)

    if a.json:
        print(json.dumps({"info": info, "errors": errors, "warnings": warnings}, indent=2))
    else:
        print("OS: " + ", ".join(f"{k}={v}" for k, v in info.items()))
        for e in errors:
            print(f"ERROR: {e}")
        for w in warnings:
            print(f"WARN:  {w}")
        print("OK: no issues found." if not errors and not warnings else
              f"{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
