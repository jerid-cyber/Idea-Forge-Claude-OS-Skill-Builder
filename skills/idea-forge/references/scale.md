# Scale: Skill, Family, or OS

Idea Forge builds at three scales. Choosing the right one is the most important architecture decision, because building too big creates upkeep with no payoff, and building too small leaves the person stitching skills together by hand.

## The three scales

**Skill.** One job, done well. Triggered when needed, done when the job is done.

**Family.** Several related skills that share an audience or a workflow, shipped together as a plugin. Each skill still runs on its own; there's no shared memory or schedule beyond what each skill does alone.

**OS (operating system).** A system that runs a whole area of work: a shared brain every component reads and writes, an orchestrator that decides what runs next, a cadence that runs without being asked, defined handoffs between components, one scoreboard, and clear authority levels. Examples: a business growth OS, a coaching companion, an agent-onboarding system.

## Detection test

Score the capture inventory against these signals:

| Signal | Points toward |
|---|---|
| One job, one output, one trigger | Skill |
| Several jobs, same audience, used independently | Family |
| Components need to remember what other components learned | OS |
| Work should happen on a schedule or in response to events, not only on request | OS |
| Something must decide *which* job to do next | OS |
| Four or more jobs that feed each other in a loop | OS |
| One number should tell you whether the whole thing is working | OS |
| The person says "system", "OS", "run my...", "on autopilot", "the whole..." | OS (confirm) |

**Choose OS only when at least three OS signals are present.** With one or two, build a Family and note in Temper that it could be promoted to an OS later. Say the decision and the reason in one sentence: "This is an OS: it needs shared memory across eight jobs, a weekly cadence, and one score."

When the person asks for an OS but the signals say Skill or Family, tell them plainly and recommend the smaller build, with what would justify upgrading later. Respect their final call.

## Promotion and demotion

Scales aren't permanent:
- **Skill → Family:** a Temper "Bigger" idea becomes a sibling skill, or Family Forge finds neighbors.
- **Family → OS:** components start passing information to each other by hand, the person wants it to run on its own, or they keep asking "what should I do next?"
- **OS → Family:** the brain and orchestrator go unused; the person only ever runs single components.

Promotion reuses everything already built: existing skills become components, and their blueprints feed the OS Blueprint.

## Where to go next
- Skill: `blueprint.md`, then the default run in SKILL.md.
- Family: build each skill, then `family-forge.md` to bundle them.
- OS: `os-blueprint.md`, `os-architecture.md`, then `os-build-test.md`.
