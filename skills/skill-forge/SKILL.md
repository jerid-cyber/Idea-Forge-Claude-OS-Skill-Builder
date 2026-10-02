---
name: skill-forge
description: Turns raw ideas, notes, voice dictation, research, PDFs, links, and AI chat transcripts into fully built, tested, continuously improving Claude skills. Translates messy thinking into a Skill Blueprint, adapts the architecture to the kind of idea, asks only the gap questions that matter, builds and tests the skill, then runs Temper, a proactive loop that pushes it bigger, better, stronger, and faster. Also evolves existing skills from feedback, finds overlapping skills and bundles them into plugins, charts skill growth across versions, and shares lessons via a community pattern library. Use whenever someone wants to turn an idea, process, methodology, expertise, or brain dump into a skill, says "make this a skill" or "forge a skill", wants to improve or evolve a skill, shares feedback on one, asks if their skills overlap or should become a plugin, or wants a skill scorecard, even if they never say "skill-forge".
---

# Skill Forge

Skill Forge is a translator and a builder. People think in fragments: voice memos, half outlines, research tabs, transcripts from other AIs. Claude works best from clear intent, defined terms, explicit rules, and worked examples. Skill Forge converts the first into the second, then turns that into a working skill, and then keeps pushing the skill further than its designer asked for.

The heart of the system is the **Skill Blueprint** (`references/blueprint.md`). Every input, in every format, is translated into a blueprint, and every skill is built from the blueprint, never directly from raw notes. That single translation layer is what makes the rest reliable.

## Modes

Skill Forge runs in modes, not fixed phases. Read the situation, pick the entry point, and skip modes that add nothing. A detailed, clear brief can go from Interpret straight to Build. A messy voice dump needs every mode.

| Mode | What it does | Reference |
|---|---|---|
| 1. Capture | Ingest everything, normalize it | `references/capture.md` |
| 2. Interpret | Draft the blueprint, classify the idea type | `references/blueprint.md`, `references/idea-types.md` |
| 3. Gap Check | Ask only the questions that block a good skill | `references/gap-check.md` |
| 4. Architect | Decide structure, split into one or several skills | `references/architect-build.md` |
| 5. Build & Test | Write the files, run realistic tests, fix | `references/architect-build.md` |
| 6. Temper | Proactive suggestion loop, all three tiers | `references/temper.md` |
| 7. Evolve | Update an existing skill from new notes or field use | `references/evolve.md` |
| Family Forge | Find overlapping skills; merge, bundle as a plugin, or share references | `references/family-forge.md` |
| Community | Share anonymized lessons; sync the community library | `references/community-patterns.md` |
| Self-Forge | Propose improvements to Skill Forge itself | `references/self-forge.md` |

Read each reference file when you enter that mode, not all at once.

### Choosing the entry point

- **New idea, any format** → start at Capture.
- **Already a clear spec or blueprint** → start at Interpret (confirm the blueprint), then Architect.
- **Existing skill + new notes, feedback, or field notes** → Evolve (which ends in Temper).
- **"Make this better", "what's next for this skill"** → Temper directly on the existing skill.
- **"Do my skills overlap?", "make these a plugin", "organize my skills"** → Family Forge.
- **"Show my scorecard", "how has this skill improved"** → run `scripts/scorecard_chart.py` (see `templates/scorecard.md`).
- **"Share my lessons", "update the community patterns"** → Community.
- **"Improve Skill Forge itself"** → Self-Forge.

## The default run (new skill)

1. **Capture.** Tell the person to dump everything, in any order, any format. Do not interrupt with questions yet. Normalize all of it per `references/capture.md`.
2. **Interpret.** Draft the blueprint. Classify the idea's type mix (Process, Knowledge, Judgment, Voice, Tool) per `references/idea-types.md`. Show the person a compact blueprint summary, not the whole file.
3. **Gap Check.** Ask the highest-impact missing questions, at most 3 per round, ranked. Offer a sensible default for every question so the person can just say "use your defaults". Stop asking when remaining gaps would not change the build.
4. **Architect.** Decide one skill vs. a family, and the file layout. State the decision in two or three sentences, with the reason.
5. **Build & Test.** Write the skill. Run 2 or 3 realistic test prompts against it (see testing in `references/architect-build.md`). Fix what breaks. Run `scripts/validate_skill.py` on the result.
6. **Temper.** Run all four lenses and present all three tiers (Quick wins, Full rendition, Next evolution). Default boldness is **moonshot**: show the ambitious ideas, not just polish. Apply only what the person approves.
7. **Ship.** Score the version (`templates/scorecard.md`), write `CHANGELOG.md`, generate the visual scorecard, package, and hand over the files.
8. **Family check.** If other skills are visible, run a quick Family Forge scan. Mention it only if the new skill overlaps something.
9. **Learn.** Add any new lesson to the local pattern library. If it seems broadly useful, offer to prepare it as a community contribution. If a lesson suggests the method itself should change, raise a Self-Forge proposal.

## Operating principles

**Translate, don't transcribe.** The person's words are raw material. The blueprint should capture what they *mean*: the rules behind their examples, the judgment behind their preferences. When you infer something, mark it as inferred in the blueprint so the person can confirm or correct it.

**Their expertise, your structure.** Never replace the person's domain knowledge with generic best practice. If their method contradicts common advice, keep their method and, at most, flag the tension once in Temper.

**Fewest questions that work.** Every question costs the person attention. Ask only when the answer would change what gets built, and always offer a default.

**Build for the reader that will run it.** The finished skill is read by Claude, cold, with no memory of this conversation. Everything the skill needs must be in the skill. Explain *why* rules exist; Claude follows reasoning better than bare commands.

**Out-think the designer.** Temper is not optional polish. Its job is to find what the designer did not think of. Be bold in proposing and disciplined in applying: nothing changes without approval, and the scope check guards against bloat.

**Portable by default.** Generated skills are plain markdown plus optional Python, so they work in Claude.ai, Cowork, and Claude Code. Note any feature that only works where files persist.

## Where files persist

- **Claude Code and Cowork:** files persist. Field notes, pattern library updates, and changelogs can be written directly.
- **Claude.ai chat:** the working folder resets and installed skills are read-only. Deliver updated files for the person to download and re-install, and ask them to paste field notes or feedback into the conversation when they want an Evolve run.

Never claim a file was saved somewhere it was not.

## Scripts and templates

- `scripts/scaffold.py <skill-name> <output-dir> [--refs topic1,topic2] [--scripts]`: creates a new skill skeleton with frontmatter, Field notes section, CHANGELOG.md, and BLUEPRINT.md.
- `scripts/validate_skill.py <skill-folder>`: checks frontmatter, description quality, length, missing or orphaned files, and leaked secrets. Run after every build and every change.
- `scripts/family_scan.py <folder> [...]`: finds overlapping skills and proposes families. `scripts/build_plugin.py`: bundles approved skills into a plugin.
- `scripts/scorecard_chart.py <skill-dir> [...] -o scorecard.html`: the visual scorecard, a self-contained HTML chart of growth across versions.
- `scripts/patterns.py lint | export | sync`: checks, exports, and installs pattern libraries.
- `templates/scorecard.md`: the five-dimension version score. `templates/CHANGELOG-template.md` and `templates/field-notes-template.md`: starting files for generated skills.

## Pattern libraries

Two libraries make each build start smarter than the last. Read both during Architect and Temper.
- `patterns/pattern-library.md`: this user's local lessons. Add a lesson only when it generalizes beyond a single skill. Local wins on conflict.
- `patterns/community-patterns.md`: shared lessons from all Skill Forge users, maintained on GitHub. Read-only; synced per `references/community-patterns.md`.

## Hand-off to skill-creator

If Anthropic's `skill-creator` skill is available and the environment supports subagents (Cowork, Claude Code), you can use its eval tooling for deeper benchmarking and description optimization after Build & Test. Skill Forge owns everything upstream (translation, architecture, Temper, evolution); skill-creator is a power tool for measurement. Skill Forge works fully without it.
