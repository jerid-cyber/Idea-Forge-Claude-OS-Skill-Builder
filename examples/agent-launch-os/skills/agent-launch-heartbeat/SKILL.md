---
name: agent-launch-heartbeat
description: Puts Agent Launch OS on a schedule. Use when the user says "put Agent Launch OS on autopilot", "run this every week", "set up the heartbeat", "schedule my runs", or after setup is complete.
---

# Agent Launch OS Heartbeat

Runs `agent-launch-command-center` on a daily cadence and reports what happened.

## Setting it up
- **Cowork or Claude Code:** create a scheduled task (or cron/CI job) that runs: "Run the Agent Launch OS daily cycle." Confirm the schedule with the user.
- **Claude.ai chat:** scheduled runs aren't available. Tell the user plainly, and give them the one line to send each day: "Run my Agent Launch OS daily cycle."

## Each beat
Call `agent-launch-command-center`. Then send a short report: scoreboard change, actions taken, approvals waiting.

## Event triggers
An appointment is set; the agent reports zero calls two days in a row.

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/agent-launch-heartbeat.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
