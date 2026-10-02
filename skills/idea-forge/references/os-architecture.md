# OS Architecture

Read this in Architect when the scale is OS. It explains each system part, the design choices, and the failure modes to avoid. The scaffold (`scripts/os_scaffold.py`) generates a working version of every part below.

## Contents
1. Brain
2. Setup skill
3. Orchestrator
4. Heartbeat and events
5. Components
6. Handoffs
7. Scoreboard
8. Governance
9. Logs
10. Plugin layout

## 1. Brain
One markdown file (default `os/brain.md`) holding everything components need to share: the profile of the person or business, current state, decisions, and the queue of next moves. Markdown, not a database, so people can read and correct it and it works everywhere.

- Give each field a heading and a one-line meaning. Components read and write by heading.
- Every field has at least one writer and one reader. A field nobody reads is clutter; a field nobody writes is a bug.
- Keep facts and status separate: profile facts change rarely, status changes every run.
- Never store secrets or account numbers in the brain.

## 2. Setup skill
Creates the brain the first time, by interviewing the person (with defaults) or reading what's connected. The orchestrator calls it automatically when the brain is missing. It also handles "we changed our hours/prices/offer" updates.

## 3. Orchestrator
The command center. Every run: load the brain, scoreboard, and approvals; surface pending approvals first; pick what runs next; route; log.

Choose one routing style:
- **Scoring rule** (best for growth and optimization OSes): `priority = impact × weight ÷ effort`, with a cap on moves per cycle so results can be attributed.
- **Fixed sequence** (best for onboarding and fulfillment): a stage machine; the brain records the current stage.
- **Event-driven** (best for operations): specific events map to specific components.

Include a routing table naming every component. Cap work per cycle (three moves is a good default); an OS that does everything at once can't tell what worked.

## 4. Heartbeat and events
The heartbeat skill sets up and runs the cadence: it calls the orchestrator on schedule and reports what happened. Event triggers ("new review", "metric dropped 20%") let the OS respond between beats.

Platform reality: scheduled runs work in Cowork and Claude Code (scheduled tasks, cron, or CI). In Claude.ai chat, the heartbeat becomes a checklist the person starts with "run my weekly cycle." Say this plainly in the heartbeat skill.

## 5. Components
Ordinary skills with three additions: they read their inputs from the brain, write their results back, and end by naming the next handoff or returning control to the orchestrator. Each states its authority level at the top. Components should also run standalone when someone asks for that job directly.

## 6. Handoffs
A handoff names what passes from one component to the next and where it lives (a brain field or a file). Unwritten handoffs are where OSes break: component B assumes something component A never wrote. Define every handoff in `os.json`; the validator checks them.

## 7. Scoreboard
One number with a baseline and target, in `os/scoreboard.md`, updated by the orchestrator each cycle. It's how the OS proves it works and how the orchestrator decides what matters. Supporting metrics: three at most.

## 8. Governance
Three authority levels, stated per component:
- **auto:** runs and records without asking. Only for reversible, internal work (analysis, drafts, scoring).
- **approve:** prepares the action, queues it in `os/approvals.md`, and waits. Default for anything that sends, spends, publishes, deletes, or contacts people.
- **suggest:** recommends only; the person does it.

When in doubt, choose approve. An OS that acts wrongly on its own loses trust faster than one that asks.

## 9. Logs
`os/action-log.md` (what ran, when, result) and `os/approvals.md` (waiting, approved, rejected). The orchestrator reads both at the start of every run, which is what gives the OS continuity between sessions.

## 10. Plugin layout

```
<os-name>/
  .claude-plugin/plugin.json
  os.json                     machine-readable map
  OS-BLUEPRINT.md             human-readable design
  README.md                   how to install and run it
  os-template/                starting brain, scoreboard, and log files
  skills/
    <os>-command-center/      orchestrator
    <os>-brain-setup/         setup
    <os>-heartbeat/           cadence
    <component>/ ...          one folder per component
```

The `os-template/` files are copied into the person's working folder as `os/` on first run, because installed plugin folders are often read-only.

## Common failure modes
- **The blob:** every component reads and writes everything. Fix: narrow reads and writes per component.
- **The dead end:** a component finishes but nothing picks up its output. Fix: every component hands off or returns to the orchestrator.
- **The runaway:** auto-authority on external actions. Fix: approve by default.
- **The forgotten setup:** components assume the brain exists. Fix: the orchestrator checks and runs setup first.
- **The vanity score:** the scoreboard measures activity, not outcomes. Fix: pick a number the person would pay to move.
