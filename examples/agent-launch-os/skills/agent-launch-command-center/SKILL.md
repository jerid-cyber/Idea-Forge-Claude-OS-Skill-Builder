---
name: agent-launch-command-center
description: The Agent Launch OS orchestrator. Use whenever the user says "run Agent Launch OS", "what should I work on", "next best move", "run my daily cycle", asks how the system is doing, or when the Agent Launch OS heartbeat fires. Reads the shared brain, keeps the scoreboard, picks what runs next, and routes work to the right Agent Launch OS skill.
---

# Agent Launch OS Command Center

Runs the Agent Launch OS loop: find the most valuable next move, get it done, prove it, repeat.

## Start of every run
1. Look for the working folder `os/`. If it's missing, copy the plugin's `os-template/` files there (brain.md, scoreboard.md, action-log.md, approvals.md). Installed plugin folders are often read-only, so working files live in `os/`.
2. Load `os/brain.md`. If the profile section is empty, run `agent-launch-brain-setup` and stop after it finishes.
3. Load `os/scoreboard.md`, `os/action-log.md`, and `os/approvals.md`.
4. Surface anything waiting in approvals before starting new work.

## Choose the next move
Stage-based. Week 1: `sphere-builder`. From day 8, daily `daily-call-coach` no matter the sphere size, with `sphere-builder` continuing alongside until 150. Waiting for a threshold that may never be reached would stall the whole system. Any appointment: `appointment-tracker`. From day 15 on, if asked: `open-house-planner`. Never run more than 3 moves in a cycle, so results can be traced to actions.

## Routing
| Skill | Job | Authority |
|---|---|---|
| `sphere-builder` | Sphere builder | auto |
| `daily-call-coach` | Daily call coach | suggest |
| `appointment-tracker` | Appointment tracker | auto |
| `open-house-planner` | Open house planner | approve |

Authority: **auto** runs and records; **approve** prepares the action, adds it to `os/approvals.md`, and waits; **suggest** recommends only. Anything that sends, spends, publishes, deletes, or contacts people needs approval.

## End of every run
Log each action in `os/action-log.md`, update `os/scoreboard.md`, refresh `next_moves` in the brain, and give the user a short summary: what ran, what changed, what's waiting for them.

## Field notes
When something about this OS clearly fails or frustrates the user, append one dated line to `field-notes/agent-launch-command-center.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge. Never interrupt the task for this.
