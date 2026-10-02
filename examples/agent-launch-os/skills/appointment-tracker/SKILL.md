---
name: appointment-tracker
description: Tracks appointments set from sphere calls and updates the scoreboard. Use when a call produces an appointment, the command center routes here, or an agent asks how close they are to their first appointment.
---

# Appointment Tracker

Part of Agent Launch OS. **Authority: auto.**

## Inputs
Read `## call_log` in `os/brain.md`.

## Method
Confirm each appointment has a date, a person, and a purpose. Count days since the agent's start date.

## Output
Write appointments under `## appointments` in `os/brain.md` and update `os/scoreboard.md` with days to first appointment. Internal record-keeping only, so it runs on its own.

## Handoff
Return to `agent-launch-command-center`.

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/appointment-tracker.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
