# Idea Forge
### Your Claude OS & Skill Builder

**Turn a brain dump into a working Claude skill, plugin, or complete operating system, then make it better than you imagined.**

You think in fragments: voice memos, half outlines, research tabs, transcripts from other AI chats. Claude works best from clear intent, defined terms, explicit rules, and worked examples. Idea Forge translates the first into the second, builds it, tests it, and keeps pushing it further.

*Formerly Skill Forge.*

![License: PolyForm Internal Use](https://img.shields.io/badge/license-PolyForm%20Internal%20Use-lightgrey.svg)
![Claude Plugin](https://img.shields.io/badge/Claude-Plugin-d97757.svg)
![Version](https://img.shields.io/badge/version-2.1.0-green.svg)

---

## Table of Contents

- [Three scales](#three-scales)
- [When does an idea become an OS?](#when-does-an-idea-become-an-os)
- [How it works](#how-it-works)
- [Built for three kinds of builders](#built-for-three-kinds-of-builders)
- [Also included](#also-included)
- [See a finished OS](#see-a-finished-os)
- [Install](#install)
- [Upgrading from Skill Forge v1.x](#upgrading-from-skill-forge-v1x)
- [Say this, get that](#say-this-get-that)
- [Platform notes](#platform-notes)
- [Getting the most out of it](#getting-the-most-out-of-it)
- [Structure](#structure)
- [Contributing](#contributing) · [License](#license)

---

## Three scales

| Scale | What you get | Example |
|---|---|---|
| **Skill** | One job, done well | A listing-presentation coach |
| **Family** | Related skills shipped together as a plugin | A seller-side toolkit |
| **OS** | A system that runs a whole area of work: shared memory, an orchestrator that picks the next move, a schedule, components that hand off to each other, one scoreboard, and approval rules | A new-agent launch system, a business growth OS |

Idea Forge picks the scale from your dump and tells you why. It will tell you when an idea doesn't need an OS, because an OS you don't need is upkeep with no payoff.

## When does an idea become an OS?

Idea Forge chooses OS only when **at least three** of these signals are present. With one or two, it builds a Family and notes that it could be promoted later. Scales aren't permanent — a skill can grow into a family, and a family into an OS, reusing everything already built.

| Signal in your idea | Points toward |
|---|---|
| One job, one output, one trigger | Skill |
| Several jobs, same audience, used independently | Family |
| Parts need to remember what other parts learned | OS |
| Work should happen on a schedule or on events | OS |
| Something has to decide which job runs next | OS |
| Four or more jobs that feed each other in a loop | OS |
| One number should say whether the whole thing works | OS |
| You say "system", "OS", "run my…", "on autopilot" | OS (it confirms first) |

## How it works

1. **Capture.** Dump everything in any format. No questions yet.
2. **Interpret.** It picks the scale, translates your material into a **blueprint**, and classifies your idea as a mix of five types (Process, Knowledge, Judgment, Voice, Tool) that shape the architecture.
3. **Gap Check.** It asks only the questions that would change the build, each with a default.
4. **Architect and Build.** It writes the skill, or for an OS, builds the smallest working system first (orchestrator, shared brain, heartbeat, and the core-loop components), then expands in waves.
5. **Test.** Realistic test prompts for skills. For an OS, a structural validator plus a **simulated week**: it runs a realistic week through the system to catch stalls, rule clashes, and dead ends.
6. **Temper.** The proactive suggestion loop: four lenses (**Bigger, Better, Stronger, Faster**), three tiers (**Quick wins**, **Full rendition**, **Next evolution**). Nothing changes without your approval.
7. **Evolve.** Feed it new notes, feedback, or field notes from real use and it upgrades, versions, and logs every change.

## Built for three kinds of builders

- **Business owners:** plain language, smart defaults, results over file trees.
- **Consultants:** a client discovery mode, one reusable OS core with a brain per client, and a client handoff package.
- **Power users:** the blueprint, `os.json`, and every script, directly.

## Also included

- **OS audit and system map.** Point it at any OS-style plugin, even one built by hand, and it finds the orchestrator, brain, and heartbeat, checks routing, memory, handoffs, and approval gates, and draws the system as an HTML map.
- **Family Forge.** Finds overlapping skills and proposes merges, plugin families, shared references, or sharper descriptions. It recognizes designed pipelines.
- **Visual scorecard.** Each skill's growth across versions, as a chart.
- **Community pattern library.** Anonymized lessons from every user's forges make everyone's builds smarter.
- **Self-Forge.** It proposes improvements to its own method for the maintainer's approval.

## See a finished OS

[`examples/agent-launch-os/`](examples/agent-launch-os/) was forged from a voice dump about coaching new real estate agents. It includes the OS Blueprint, `os.json`, the system map, and the [simulated week](examples/agent-launch-os/SIMULATED-WEEK.md) that caught two logic bugs a validator never could.

## Install

**Claude.ai / Claude desktop app:** download the `.skill` release and upload it in Settings under Skills (or tap **Save skill** when Claude hands you the file).

**Claude Code / Cowork:** install as a plugin from this repository, or copy `skills/idea-forge` into your skills directory.

## Upgrading from Skill Forge v1.x

Version 2.1 renamed the skill from Skill Forge to Idea Forge. If both are installed in your account, remove `skill-forge` and keep `idea-forge` — two near-identical skills compete to trigger.

## Say this, get that

You never need to remember mode names. These phrases route straight to the right place.

| Say this | What Idea Forge does |
|---|---|
| "Forge this" / "make this a skill" + your dump | Full default run, starting at Capture |
| "Here's a clear spec, build it" | Confirms the blueprint, goes straight to Architect |
| "Build me an OS for…" | Capture, then checks the OS signals and says honestly if it should be smaller |
| "Use your defaults" | Ends the question rounds and builds |
| "Evolve [skill] with these notes" | Folds in field notes, re-tests, Tempers, bumps version |
| "Make this better" / "what's next?" | Temper on an existing skill |
| "Polish only" | Temper without the moonshot tier |
| "Do my skills overlap?" / "organize my skills" | Family Forge scan and proposal |
| "Make these a plugin" | Bundles approved skills into one plugin |
| "Audit my OS" / "map my system" | Validation plus visual system map, then Temper |
| "Show my scorecard" | HTML growth chart across versions |
| "I'm building this for a client" | Consultant mode with discovery and handoff package |
| "Share my lessons" | Prepares anonymized community contributions |
| "Improve Idea Forge itself" | Self-Forge proposals for your approval |

Three phrases worth memorizing: **"Use your defaults"**, **"Polish only"**, and **"Apply all quick wins, park the rest."**

## Platform notes

Works in Claude.ai, Cowork, and Claude Code. Scheduled OS runs and persistent memory files work in Cowork and Claude Code. In Claude.ai chat, an OS runs when you start it ("run my weekly cycle"), and Idea Forge hands you updated files to re-install.

## Getting the most out of it

1. **Dump raw, don't pre-organize.** Dictated voice notes are some of the best input — stories carry your real rules.
2. **Tell stories.** "The time a buyer walked because the well report came late" teaches more than "always get the well report early."
3. **Bring a good and a bad example.** Good outputs become examples; bad ones become anti-patterns.
4. **Use "defaults" freely.** Every question comes with one, and anything you skip is marked and revisit-able.
5. **Say who it's for** — your business, a client, or the public. It changes the language, defaults, and deliverables.
6. **Let Temper be bold; apply selectively.** Moonshots cost nothing to read — park them and they come back on later runs.
7. **Keep field notes.** A one-line note whenever a skill misses is the cheapest improvement you'll ever make.
8. **Build systems where files persist.** Use Cowork or Claude Code for any OS so the brain, logs, and heartbeat survive.
9. **Audit before you build more.** Your existing library is the fastest win — Family Forge first, new builds second.

An honest note: Idea Forge's own scorecard rates Faster at 3 of 5, its lowest dimension. First-time forges can feel question-heavy — a one-message quick-forge path is already parked. Until then, the fastest route is a clear dump plus "use your defaults."

## Structure

```
skills/idea-forge/
  SKILL.md                 router and operating principles
  references/              one guide per mode and scale (loaded only when needed)
  patterns/                local and community pattern libraries
  templates/               scorecard, changelog, field notes
  scripts/                 scaffold, validate_skill, os_scaffold, validate_os, os_map,
                           family_scan, build_plugin, scorecard_chart, patterns
  CHANGELOG.md
examples/                  worked OS example and sample scorecard
tests/                     automated suite (python tests/run_tests.py)
.github/                   CI checks and issue templates
```

## Contributing

Share lessons with the community pattern library or propose method changes. See [CONTRIBUTING.md](CONTRIBUTING.md). Every pull request is checked automatically.

## License

Licensed under the [PolyForm Internal Use License 1.0.0](LICENSE.md) — free to use for your internal operations, including at work; you may not distribute, share copies, or sell it. © 2026 Jerid Wempen / TitanOne Media.
