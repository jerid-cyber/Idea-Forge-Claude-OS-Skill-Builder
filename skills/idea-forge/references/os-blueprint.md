# The OS Blueprint

The OS Blueprint extends the Skill Blueprint (`blueprint.md`) with the system layer. Fill it from the capture inventory; mark inferences `(inferred)` and unknowns `GAP:` exactly as for a skill. Save it as `OS-BLUEPRINT.md` at the plugin root.

Alongside it, the build produces `os.json`, a machine-readable map of the same design that the OS scripts read (`scripts/validate_os.py`, `scripts/os_map.py`). The blueprint is for people; `os.json` is for checking.

## Template

```markdown
# OS Blueprint: <name>
Version: <0.1 draft | 1.0>   Status: <draft | confirmed>   Builder: <owner | consultant | power user>

## 1. Mission
One sentence: what this OS achieves, for whom.

## 2. Scoreboard
The one number that says the OS is working, its baseline, and its target.
Supporting metrics (at most 3).

## 3. Core loop
The cycle the OS runs, in 3 to 6 steps (for example: assess → pick next move → do → measure → repeat).
Which step the orchestrator owns.

## 4. Brain
The shared state file every component reads and writes.
Fields: name, meaning, who writes it, who reads it.
What must exist before anything else runs (the setup step).

## 5. Components
For each component skill: job, reads (brain fields), writes (brain fields), hands off to,
authority (auto | approve | suggest), wave (1 = core loop, 2+ = expansion).
Existing skills to reuse (from Family Forge or the person's library).

## 6. Orchestrator
How it chooses what runs next (a scoring rule, a fixed sequence, or event-driven).
Limits (for example: no more than 3 moves per cycle).

## 7. Cadence and events
Heartbeat schedule (daily, weekly...). Event triggers (new lead, failed metric, approval granted).
Platform note: scheduled runs need Cowork or Claude Code; in Claude.ai chat the person starts each run.

## 8. Handoffs
For each handoff: from, to, what is passed, where it lives (brain field or file).

## 9. Governance
What runs automatically, what needs approval, what only suggests.
Anything that sends, spends, publishes, deletes, or contacts people defaults to approve.
Where approvals queue up and how the person clears them.

## 10. Logs
Action log and approvals queue files.

## 11. Builder and audience
Who builds it, who runs it day to day, their technical comfort.
For consultants: the client, and what the client receives at handoff.

## 12. Waves
Wave 1 (minimum viable OS), wave 2, wave 3: which components land in each, and what proves a wave works.

## 13. Out of scope
What this OS deliberately does not run.
```

## os.json format

```json
{
  "name": "acme-growth-os",
  "version": "1.0.0",
  "mission": "Help Acme book more jobs from local search.",
  "scoreboard": {"metric": "Booked jobs per month", "baseline": "12", "target": "20", "file": "os/scoreboard.md"},
  "brain": {"file": "os/brain.md", "fields": ["business_profile", "offers", "leads", "next_moves"]},
  "orchestrator": "acme-command-center",
  "setup": "acme-brain-setup",
  "heartbeat": {"skill": "acme-heartbeat", "cadence": "weekly"},
  "logs": {"actions": "os/action-log.md", "approvals": "os/approvals.md"},
  "components": [
    {"skill": "lead-intake", "job": "Capture and qualify new leads", "reads": ["business_profile"],
     "writes": ["leads"], "hands_off_to": ["follow-up-writer"], "authority": "auto", "wave": 1}
  ]
}
```

Rules the validator enforces: every component and system skill exists; the orchestrator mentions every component; every field a component reads is written by some component or the setup skill; every handoff target exists; wave 1 forms a complete loop the orchestrator can reach; anything with authority `auto` doesn't send, spend, publish, or delete without an approval step.

## Showing it to the person

Show a compact summary, not the template: mission, scoreboard, the core loop as one line, wave 1 components, and the top open questions. For business owners, describe it as "the system" and "its memory", not "orchestrator" and "brain fields" (see `builder-profiles.md`).
