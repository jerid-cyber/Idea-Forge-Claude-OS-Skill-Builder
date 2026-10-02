---
name: agent-launch-brain-setup
description: Creates or updates the Agent Launch OS brain, the shared memory every Agent Launch OS skill reads. Use when setting up Agent Launch OS for the first time, when the user says "set up Agent Launch OS" or "update my info", reports that something changed (offer, prices, hours, goals), or when another Agent Launch OS skill finds the brain missing or out of date.
---

# Agent Launch OS Brain Setup

## First run
1. If `os/` doesn't exist, copy the plugin's `os-template/` files into `os/`.
2. Read connected tools and public sources first; only ask for what they can't answer.
3. Interview for the profile: start date (default today), CRM name (default: ask), prior sales experience (default none), broker's name.
4. Write answers under `## profile` in `os/brain.md` and set the scoreboard baseline.
5. Hand back to `agent-launch-command-center`.

## Updates
When something changes, edit only the affected lines, note the date, and tell the user which skills the change affects.

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/agent-launch-brain-setup.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
