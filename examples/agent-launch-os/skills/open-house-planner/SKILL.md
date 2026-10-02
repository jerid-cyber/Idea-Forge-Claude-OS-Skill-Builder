---
name: open-house-planner
description: Plans an open house for a new agent after their first two weeks. Use when the command center routes here or an agent asks to host an open house.
---

# Open House Planner

Part of Agent Launch OS. **Authority: approve.**

## Inputs
Read `## profile` and `## appointments` in `os/brain.md`.

## Method
No open houses in the first two weeks: they pull attention off the sphere. Exception: one of the broker's own listings with the broker present. After week 2, help pick a listing and plan sign-in and follow-up.

## Output
Write the plan under `## current_state` in `os/brain.md`. Booking the open house or inviting the sphere needs the broker's approval: add it to `os/approvals.md` and wait.

## Handoff
Return to `agent-launch-command-center`.

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/open-house-planner.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
