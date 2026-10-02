# The Skill Blueprint

The blueprint is the translation layer between human thinking and a buildable skill. Fill it from the capture inventory. Mark anything you inferred (rather than heard) with `(inferred)` so the person can confirm it. Leave a field as `GAP:` plus a short note when it is unknown and matters; those become Gap Check questions.

Save it as `BLUEPRINT.md` next to the skill when files persist, so future Evolve runs can start from it. In Claude.ai, include it in the delivered package.

## Template

```markdown
# Skill Blueprint: <working name>
Version: <0.1 draft | 1.0 | ...>   Status: <draft | confirmed>

## 1. Purpose
One or two sentences: what this skill accomplishes and for whom.

## 2. Success looks like
What a great result looks like, concretely. How the person would judge it.

## 3. Audience and context
Who invokes the skill, where (chat, Cowork, Code), their skill level, the situation they're in.

## 4. Triggers
Phrases, situations, and file types that should activate the skill.
Near-misses that should NOT activate it.

## 5. Inputs
What the skill receives (formats, files, typical messiness). What it should ask for if missing.

## 6. Outputs
Deliverables and formats. Length and tone expectations.

## 7. Idea type mix
Process __% / Knowledge __% / Judgment __% / Voice __% / Tool __%
One line on why.

## 8. Core method
The steps, rules, or approach, in the person's terms. Ordered if it is a process.

## 9. Rules and constraints
Hard rules (with the reason behind each). Things to never do.

## 10. Judgment calls
"It depends" situations and how the person decides. Each with an example if possible.

## 11. Glossary
Terms with this person's specific meaning. Ambiguous terms resolved.

## 12. Examples
Good outputs, bad outputs, and edge cases, drawn from the person's material.

## 13. Dependencies
Tools, connectors, scripts, data, or other skills it relies on. Platform limits.

## 14. Open questions
Remaining GAP items, ranked.

## 15. Out of scope
What this skill deliberately does not do (prevents bloat later).
```

## Showing the blueprint to the person

Do not paste the whole template into the chat unless asked. Show a compact summary: purpose, type mix, core method in a few lines, and the top open questions. The full file is for the build and for future-you.

## Confirming

The blueprint is "confirmed" when the person has seen the summary and either answered the gap questions or accepted defaults. Inferred items they did not object to can stay, still marked `(inferred)`, so a later Evolve run knows they were never explicitly confirmed.
