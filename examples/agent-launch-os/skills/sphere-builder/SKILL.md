---
name: sphere-builder
description: Builds the new agent's sphere in the CRM during week 1. Use when the command center routes week-1 work here or when an agent asks how to load their sphere or who to add.
---

# Sphere Builder

Part of Agent Launch OS. **Authority: auto.**

## Inputs
Read `## profile` in `os/brain.md` (start date, CRM, experience).

## Method
1. Help the agent list everyone they personally know: family, friends, past coworkers, neighbors, service providers. Say "sphere", never "contacts".
2. Target at least 150 people in week 1. That's the fuel for daily calls; a thin sphere stalls calls by week 3.
3. If they're under 100 by day 5, run a 20-minute memory-jogger session by category.

## Output
Write the sphere count and gaps under `## sphere` in `os/brain.md`, and log the action. This is internal work, so it runs on its own.

## Handoff
When the sphere hits 150, hand off to `daily-call-coach`.

## Field notes
When something about this skill clearly fails or frustrates the user, append one dated line to `field-notes/sphere-builder.md` where files persist; otherwise mention briefly that the note can be pasted into Idea Forge.
