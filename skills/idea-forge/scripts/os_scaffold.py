#!/usr/bin/env python3
"""Generate a working OS plugin skeleton.

Usage:
  python os_scaffold.py <os-name> <output-dir> --components "job one,job two,job three"
      [--cadence weekly] [--author "Name"] [--mission "..."]

Creates a Claude plugin with: os.json, OS-BLUEPRINT.md, README.md, os-template/
(brain, scoreboard, action log, approvals), and four kinds of skills:
<os>-command-center (orchestrator), <os>-brain-setup, <os>-heartbeat, and one
stub per component. Component stubs contain TODOs that validate_skill.py will
flag until they're written. Standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("outdir")
    ap.add_argument("--components", required=True)
    ap.add_argument("--cadence", default="weekly")
    ap.add_argument("--author", default="")
    ap.add_argument("--mission", default="TODO one-sentence mission")
    a = ap.parse_args()

    name = slug(a.name)
    if not name:
        sys.exit("Invalid OS name.")
    base = name[:-3] if name.endswith("-os") else name
    root = Path(a.outdir) / name
    if root.exists():
        sys.exit(f"{root} already exists; refusing to overwrite.")
    jobs = [j.strip() for j in a.components.split(",") if j.strip()]
    if len(jobs) < 2:
        sys.exit("An OS needs at least 2 components. For one job, build a skill instead.")
    comps = [{"skill": slug(j), "job": j} for j in jobs]
    orch, setup, beat = f"{base}-command-center", f"{base}-brain-setup", f"{base}-heartbeat"
    title = name.replace("-", " ").title().replace(" Os", " OS")

    # os.json
    os_json = {
        "name": name, "version": "0.1.0", "mission": a.mission,
        "scoreboard": {"metric": "TODO the one number that proves this OS works", "baseline": "", "target": "",
                       "file": "os/scoreboard.md"},
        "brain": {"file": "os/brain.md", "fields": ["profile", "current_state", "next_moves"]},
        "orchestrator": orch, "setup": setup,
        "heartbeat": {"skill": beat, "cadence": a.cadence},
        "logs": {"actions": "os/action-log.md", "approvals": "os/approvals.md"},
        "components": [],
    }
    for k, c in enumerate(comps):
        nxt = [comps[k + 1]["skill"]] if k + 1 < len(comps) else []
        os_json["components"].append({
            "skill": c["skill"], "job": c["job"], "reads": ["profile"], "writes": ["current_state"],
            "hands_off_to": nxt, "authority": "approve", "wave": 1 if k < 3 else 2})
    write(root / "os.json", json.dumps(os_json, indent=2))

    manifest = {"name": name, "version": "0.1.0", "description": f"{title}: an operating system built with Idea Forge."}
    if a.author:
        manifest["author"] = {"name": a.author}
    write(root / ".claude-plugin" / "plugin.json", json.dumps(manifest, indent=2))

    # Templates copied to the working folder on first run
    write(root / "os-template" / "brain.md", f"""
# {title} Brain

Shared memory for every {title} skill. Read before acting; write back after. Never store passwords, API keys, or account numbers here.

## profile
Who this OS serves and their stable facts. Written by {setup}.

## current_state
What's happening now. Updated by components after each action.

## next_moves
Ranked queue of what to do next. Maintained by {orch}.
""")
    write(root / "os-template" / "scoreboard.md", f"""
# {title} Scoreboard

Metric: TODO
Baseline: TODO
Target: TODO

| Date | Value | Change | Driven by |
|---|---|---|---|
""")
    write(root / "os-template" / "action-log.md", f"# {title} Action Log\n\n| Date | Skill | Action | Result |\n|---|---|---|---|")
    write(root / "os-template" / "approvals.md", f"# {title} Approvals\n\n## Waiting\n\n## Approved\n\n## Rejected")

    routing = "\n".join(f"| `{c['skill']}` | {c['job']} | approve |" for c in comps)
    write(root / "skills" / orch / "SKILL.md", f"""
---
name: {orch}
description: The {title} orchestrator. Use whenever the user says "run {title}", "what should I work on", "next best move", "run my {a.cadence} cycle", asks how the system is doing, or when the {title} heartbeat fires. Reads the shared brain, keeps the scoreboard, picks what runs next, and routes work to the right {title} skill.
---

# {title} Command Center

Runs the {title} loop: find the most valuable next move, get it done, prove it, repeat.

## Start of every run
1. Look for the working folder `os/`. If it's missing, copy the plugin's `os-template/` files there (brain.md, scoreboard.md, action-log.md, approvals.md). Installed plugin folders are often read-only, so working files live in `os/`.
2. Load `os/brain.md`. If the profile section is empty, run `{setup}` and stop after it finishes.
3. Load `os/scoreboard.md`, `os/action-log.md`, and `os/approvals.md`.
4. Surface anything waiting in approvals before starting new work.

## Choose the next move
TODO the routing rule. Default: score each open move as impact x weight / effort, pick the top 1 to 3. Never run more than 3 moves in a cycle, so results can be traced to actions.

## Routing
| Skill | Job | Authority |
|---|---|---|
{routing}

Authority: **auto** runs and records; **approve** prepares the action, adds it to `os/approvals.md`, and waits; **suggest** recommends only. Anything that sends, spends, publishes, deletes, or contacts people needs approval.

## End of every run
Log each action in `os/action-log.md`, update `os/scoreboard.md`, refresh `next_moves` in the brain, and give the user a short summary: what ran, what changed, what's waiting for them.

## Field notes
When something about this OS clearly fails or frustrates the user, append one dated line to `field-notes/{orch}.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge. Never interrupt the task for this.
""")
    write(root / "skills" / setup / "SKILL.md", f"""
---
name: {setup}
description: Creates or updates the {title} brain, the shared memory every {title} skill reads. Use when setting up {title} for the first time, when the user says "set up {title}" or "update my info", reports that something changed (offer, prices, hours, goals), or when another {title} skill finds the brain missing or out of date.
---

# {title} Brain Setup

## First run
1. If `os/` doesn't exist, copy the plugin's `os-template/` files into `os/`.
2. Read connected tools and public sources first; only ask for what they can't answer.
3. Interview for the profile: TODO list the questions, each with a default.
4. Write answers under `## profile` in `os/brain.md` and set the scoreboard baseline.
5. Hand back to `{orch}`.

## Updates
When something changes, edit only the affected lines, note the date, and tell the user which skills the change affects.

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/{setup}.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
""")
    write(root / "skills" / beat / "SKILL.md", f"""
---
name: {beat}
description: Puts {title} on a schedule. Use when the user says "put {title} on autopilot", "run this every week", "set up the heartbeat", "schedule my runs", or after setup is complete.
---

# {title} Heartbeat

Runs `{orch}` on a {a.cadence} cadence and reports what happened.

## Setting it up
- **Cowork or Claude Code:** create a scheduled task (or cron/CI job) that runs: "Run the {title} {a.cadence} cycle." Confirm the schedule with the user.
- **Claude.ai chat:** scheduled runs aren't available. Tell the user plainly, and give them the one line to send each { {'daily': 'day', 'weekly': 'week', 'monthly': 'month'}.get(a.cadence, 'cycle') }: "Run my {title} {a.cadence} cycle."

## Each beat
Call `{orch}`. Then send a short report: scoreboard change, actions taken, approvals waiting.

## Event triggers
TODO events that should run the orchestrator between beats (for example a new lead or a metric drop).

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/{beat}.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
""")
    for k, c in enumerate(comps):
        nxt = comps[k + 1]["skill"] if k + 1 < len(comps) else orch
        write(root / "skills" / c["skill"] / "SKILL.md", f"""
---
name: {c['skill']}
description: TODO what this {title} skill does ({c['job']}) and when to use it. Use when {orch} routes this job here, or whenever the user asks for {c['job'].lower()} directly.
---

# {c['job'].title()}

Part of {title}. **Authority: approve.**

## Inputs
Read `## profile` in `os/brain.md`. TODO other fields.

## Method
TODO the steps, rules (with reasons), and judgment calls.

## Output
Write results under `## current_state` in `os/brain.md` and log the action in `os/action-log.md`. Anything that sends, spends, publishes, deletes, or contacts people goes to `os/approvals.md` first.

## Handoff
When done, hand off to `{nxt}`.

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/{c['skill']}.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
""")

    write(root / "OS-BLUEPRINT.md", f"# OS Blueprint: {name}\n\nFill from Idea Forge's references/os-blueprint.md template.")
    comp_lines = "\n".join(f"- **{c['skill']}**: {c['job']}" for c in comps)
    write(root / "README.md", f"""
# {title}

{a.mission}

## What's inside
- **{orch}**: decides what runs next
- **{setup}**: sets up the system's memory
- **{beat}**: runs it on a {a.cadence} schedule
{comp_lines}

## Get started
Install the plugin, then say: "Set up {title}." After setup, say "Run my {title} {a.cadence} cycle", or ask for the heartbeat to put it on a schedule.

Built with Idea Forge.
""")
    print(f"Created OS {root}")
    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        print("  ", f.relative_to(root.parent))


if __name__ == "__main__":
    main()
