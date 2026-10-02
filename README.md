# Skill Forge

**Turn your ideas into working Claude skills, then make them better than you imagined.**

You think in fragments: voice memos, half outlines, research tabs, transcripts from other AI chats. Claude works best from clear intent, defined terms, explicit rules, and worked examples. Skill Forge translates the first into the second, builds a tested skill, and then proactively pushes it further.

![License: PolyForm Internal Use](https://img.shields.io/badge/license-PolyForm%20Internal%20Use-lightgrey.svg)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-d97757.svg)
![Version](https://img.shields.io/badge/version-1.1.0-green.svg)

---

## Table of Contents

- [What it does](#what-it-does)
- [What to say](#what-to-say)
- [How it reads your ideas](#how-it-reads-your-ideas)
- [Temper: the part that out-thinks you](#temper-the-part-that-out-thinks-you)
- [Keeping skills alive](#keeping-skills-alive)
- [Family Forge](#family-forge)
- [The scorecard](#the-scorecard)
- [Install](#install)
- [Platform notes](#platform-notes)
- [Getting the most out of it](#getting-the-most-out-of-it)
- [Limits and what's next](#limits-and-whats-next)
- [Structure](#structure)
- [Contributing](#contributing) · [License](#license)

---

## What it does

1. **Capture.** Dump everything in any format. No questions yet.
2. **Interpret.** It translates your material into a **Skill Blueprint**, the standard format every skill is built from, and classifies your idea as a mix of five types: Process, Knowledge, Judgment, Voice, and Tool. The mix decides the architecture.
3. **Gap Check.** It asks only the questions that would change the build, three at a time, each with a default you can accept.
4. **Architect.** One skill or a family, and what goes where.
5. **Build & Test.** It writes the skill, runs realistic test prompts, fixes what breaks, and validates the files.
6. **Temper.** The proactive suggestion loop. Four lenses (**Bigger, Better, Stronger, Faster**) and three tiers: **Quick wins**, a **Full rendition**, and **Next evolution** moonshots. Nothing changes without your approval.
7. **Evolve.** Feed it new notes, feedback, or field notes from real use and it upgrades the skill, versions it, and logs every change.

**New in 1.1**

- **Family Forge.** It scans your skill library, finds overlaps, and proposes the right fix: merge duplicates, bundle related skills into a plugin, extract shared references, or sharpen descriptions where skills in different plugins compete to trigger. It recognizes designed pipelines, so it won't tell you to merge a skill with the one it intentionally hands off to.
- **Community pattern library.** Every user's lessons, anonymized and reviewed, make everyone's forges smarter. Your local lessons stay yours; the community library syncs from this repo.
- **Visual scorecard.** A self-contained HTML chart of each skill's growth across versions on Bigger, Better, Stronger, Faster, and Triggering, with a radar of the skill's current shape. See [`examples/scorecard-example.html`](examples/scorecard-example.html).

**Self-Forge:** Skill Forge learns from every build and proposes improvements to its own method for your approval.

## What to say

Skill Forge picks its entry point from what you ask — you never have to name a mode.

| When you want to… | Say something like |
|---|---|
| Build a new skill from an idea | "Make this a skill" · "Forge a skill from my notes" |
| Build from a spec you already have | "Here's the spec, build it" |
| Fix or extend an existing skill | "It keeps doing X, fix it" · "Here are my field notes" |
| Push a skill further | "Make this better" · "What's next for this skill?" |
| Get only small fixes | "Temper this, polish only" |
| Organize a pile of skills | "Do my skills overlap?" · "Make these a plugin" |
| See progress | "Show my scorecard" · "How has this skill improved?" |
| Share what you've learned | "Share my lessons" · "Update the community patterns" |
| Improve Skill Forge itself | "Improve Skill Forge" |

Three phrases worth memorizing: **"Use your defaults"** (skips the remaining questions and builds with sensible, marked choices), **"Polish only"** (Temper without the moonshots), and **"Here are my field notes"** (starts an Evolve run from real-world use).

## How it reads your ideas

### The Skill Blueprint

Every input becomes a **Skill Blueprint** first — 15 sections covering purpose, success criteria, audience, triggers (and near-misses that shouldn't trigger), inputs, outputs, idea-type mix, core method, rules with reasons, judgment calls, glossary, examples, dependencies, open questions, and out of scope. Every skill is built from the blueprint, never directly from raw notes. That single translation layer is why results stay consistent no matter how messy the input.

Two markers matter: **(inferred)** means Skill Forge read between the lines — correct it if it's wrong. **(default)** means it chose for you. Both are fair game to change when new evidence shows up, but it never overrides something you explicitly confirmed without asking.

### The five idea types

Every idea is scored as a blend of five types, and the blend decides how the skill gets built:

| Type | Sounds like | Gets built as |
|---|---|---|
| **Process** | "First… then…", checklists, handoffs | Ordered steps with approval checkpoints |
| **Knowledge** | Expertise, frameworks, reference docs | A lean SKILL.md routing to one reference file per topic |
| **Judgment** | "It depends", "I usually", trade-offs | Decision rules with reasons plus worked examples, including one where the obvious answer is wrong |
| **Voice** | "Sound like me", brand, tone | A voice guide with do/don't pairs and before/after rewrites |
| **Tool** | Calculations, file conversion, data cleanup | Python scripts for anything mechanical or repeated |

## Temper: the part that out-thinks you

Forging makes the steel; tempering makes it stronger. After every build, Temper proposes improvements through four lenses — **Bigger, Better, Stronger, Faster** — in three tiers: **Quick wins**, a **Full rendition**, and **Next evolution** moonshots. Nothing changes without your approval.

Before presenting, every "Bigger" idea passes a **scope check**: if it would make the core job worse, slower, or harder to trigger, it moves to Next evolution as a separate skill idea instead of being bolted on. Parked ideas are recorded in the CHANGELOG so future Temper runs build on them instead of re-suggesting them.

A fast, effective habit: **"Apply all quick wins, park the rest."** Come back to the moonshots once the skill has seen real use.

## Keeping skills alive

A skill is never finished. Every skill Skill Forge builds includes a light **field notes hook**: when the skill frustrates you in real use (a wrong assumption, a missing case, a repeated correction), it notes it in one line. Run Evolve and Skill Forge groups your notes into patterns — one complaint is an anecdote, the same friction three times is a fix — updates the blueprint first, then the skill, and re-runs the original tests plus a new one. A fix that breaks an old test isn't counted as a fix. The skill keeps its name, so the new version installs over the old one.

| Version bump | When | Example |
|---|---|---|
| **Patch** (1.0 → 1.0.1) | Wording fixes, no behavior change | Clarified a confusing instruction |
| **Minor** (1.0 → 1.1) | New capability or meaningful behavior change | Added Family Forge |
| **Major** (1.x → 2.0) | Changed purpose, split or merged skills | Merged two competing skills into one |

## Family Forge

As a skill library grows, overlap causes two problems: skills compete to trigger on the same request, and you maintain the same knowledge in several places. Family Forge scans your skills, scores how similar they are, and proposes the right fix:

| If the scan shows… | Skill Forge proposes |
|---|---|
| Two skills doing the same job | **Merge** into one |
| Related skills, one workflow, different steps | **Plugin family** — installs and updates as one unit |
| The same glossary or rules repeated | **Shared reference** file — fix once, fixed everywhere |
| Skills always run in order | **Plugin + router skill** — you ask once, the router chains them |
| One skill's description already calls the other | **Keep apart, clarify** — it's a designed pipeline |
| Similar words, different jobs | **Leave apart, sharpen descriptions** |

You approve every change.

## The scorecard

Every version is scored 1–5 on five dimensions. A 5 means an expert would struggle to improve it on that dimension. The lowest score tells the next Temper run where to focus.

| Dimension | The question it answers |
|---|---|
| **Bigger** | Does it cover the job end to end for its audience? |
| **Better** | Would an expert be impressed by the output? |
| **Stronger** | Does it hold up against messy input and edge cases? |
| **Faster** | How quickly does the user reach a great result? |
| **Triggering** | Does it activate when it should, and not when it shouldn't? |

Say "show my scorecard" and Skill Forge generates a self-contained HTML chart: a growth line per dimension, a radar comparing the latest version to the previous one, and a version table with the weakest score highlighted. Pass several skills at once for a portfolio view. See [`examples/scorecard-example.html`](examples/scorecard-example.html).

## Install

**Claude.ai / Claude desktop app:** zip the `skills/skill-forge` folder (or download the `.skill` release) and upload it in Settings under Skills.

**Claude Code / Cowork:** install as a plugin from this repository, or copy `skills/skill-forge` into your skills directory.

## Platform notes

Works in Claude.ai, Cowork, and Claude Code. In Cowork and Claude Code, files persist, so field notes and pattern library updates are written automatically. In Claude.ai chat, Skill Forge hands you updated files to re-install and you paste feedback in when you want an upgrade.

## Getting the most out of it

1. **Dump stories, not just rules.** The anecdotes in your material are where Skill Forge finds your real judgment calls — they become the worked examples that make skills expert-grade.
2. **Include good and bad examples.** Good ones become the skill's examples; bad ones become anti-patterns.
3. **Talk instead of typing.** Voice dumps are explicitly supported. Ramble, correct yourself, go on tangents — it keeps the last version of anything you revised.
4. **Paste in your other AI chats freely.** Skill Forge separates what you decided from what the other AI suggested.
5. **Say "use your defaults" when you're busy.** You'll get a working skill faster, and every default is marked so you can revisit it later.
6. **Say "apply all quick wins, park the rest" after Temper.** Safe improvements now, moonshots when you have evidence they matter.
7. **Keep the BLUEPRINT.md with every skill.** It's what makes future Evolve runs fast and accurate.
8. **Do an Evolve run after the first week of real use.** That's when field notes reveal the gaps no test caught.
9. **Run Family Forge whenever you add a batch of skills.** Overlap is the most likely source of the wrong skill firing.
10. **Use Cowork or Claude Code for skills you'll live in.** Persistent files mean field notes, changelogs, and lessons save themselves.

## Limits and what's next

- **Claude.ai chat is read-only for installed skills.** Download updated packages to re-install, or work in Cowork/Code.
- **First forges can feel question-heavy.** Use "use your defaults" liberally — a quicker forge path is parked for the next version.
- **Parked for next:** quick-forge path, compact Temper for patch-level changes, and a full worked end-to-end forge example in this repo.

## Structure

```
skills/skill-forge/
  SKILL.md                 the router and operating principles
  references/              one guide per mode (loaded only when needed)
  patterns/                the growing pattern library
  templates/               scorecard, changelog, field notes
  scripts/                 scaffold, validate_skill, family_scan, build_plugin,
                           scorecard_chart, patterns
  CHANGELOG.md
tests/                     automated suite (python tests/run_tests.py)
examples/                  sample visual scorecard
.github/                   CI checks and issue templates
```

## Contributing

Share lessons with the community pattern library or propose method changes. See [CONTRIBUTING.md](CONTRIBUTING.md). Every pull request is checked automatically.

## License

Licensed under the [PolyForm Internal Use License 1.0.0](LICENSE.md) — free to use for your internal operations, including at work; you may not distribute, share copies, or sell it. © 2026 Jerid Wempen / TitanOne Media.
