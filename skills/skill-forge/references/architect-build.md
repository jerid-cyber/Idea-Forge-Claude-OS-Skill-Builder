# Modes 4 & 5: Architect, Build & Test

## Architect

### Decide the shape
Use the type mix from `idea-types.md` and the pattern library (`patterns/pattern-library.md`). Decide:

1. **One skill or a family.** Apply the split rules in `idea-types.md`. A family of three or more related skills is a candidate for a plugin.
2. **What lives where.**
   - `SKILL.md`: purpose, when-to-use, the core method, routing to references. Aim for under 300 lines; hard ceiling 500.
   - `references/`: domain knowledge, detailed guides, long examples. One topic per file.
   - `scripts/`: deterministic or repetitive work.
   - `templates/` or `assets/`: output templates, boilerplate.
3. **Autonomy level.** Where must the skill pause for approval? Anything that sends, deletes, spends, publishes, or contacts people needs an explicit approval checkpoint.

State the architecture decision to the person in two or three sentences with the reason. Don't make them read a file tree unless they ask.

### Write the description first
The `description` field in the frontmatter is the only thing Claude sees when deciding whether to use the skill. It decides whether the skill ever runs.

- Say what the skill does AND when to use it, including the person's likely phrasings.
- Include near-synonyms and situations where the user won't name the skill ("even if they don't say X").
- Be a little pushy: skills tend to under-trigger.
- Keep it under about 1,000 characters.
- Avoid triggering on near-misses: if a similar request should go elsewhere, say so.

## Build

### Start from the scaffold
Run `python scripts/scaffold.py <skill-name> <output-dir> --refs "topic one,topic two"` (add `--scripts` for Tool-heavy skills) to create the skeleton, then fill it in.

### Naming
Lowercase, hyphenated, descriptive: `listing-presentation-coach`, not `lpc` or `my-skill`. The folder name matches the `name` field.

### Writing style for skills
- Imperative voice: "Ask for the address", not "The skill should ask for the address."
- Explain the reason behind rules. "Confirm the price before sending, because a wrong price in a client email is hard to retract" generalizes better than "ALWAYS confirm the price."
- Use the person's terminology from the glossary consistently.
- Examples beat descriptions, especially for Judgment and Voice.
- Include an "out of scope" note when the blueprint has one; it prevents drift.
- Write for a reader with zero context. No references to "our conversation" or "as discussed."

### Portability
- Plain markdown and standard Python only, unless a dependency is essential. Note required packages in SKILL.md.
- Where behavior differs by platform (files persist in Cowork and Code, not in Claude.ai chat), say so in the skill.
- No hard-coded personal data, API keys, or account details in a skill meant for sharing.

### Field notes hook (every generated skill)
Add a short section near the end of each generated skill so it can feed future Evolve runs:

```markdown
## Field notes
When something about this skill clearly fails or frustrates the user (a wrong assumption, a missing case, a repeated correction), note it briefly. Where files persist, append one dated line to `field-notes/<skill-name>.md` in the working folder. Where they don't, and only if the issue was significant, mention at the end of your reply that the user can paste the note into Skill Forge to improve this skill. Keep it to one line; never interrupt the task for this.
```

Keep the hook light. A skill that nags about feedback is worse than one without the hook.

## Test

### Test prompts
Write 2 or 3 realistic prompts, the kind the actual audience would type, including one messy or borderline case. Share them with the person and ask if they'd add any.

### Run them
- **Claude.ai chat:** for each prompt, read the built SKILL.md and follow it to complete the task yourself, one at a time. You wrote the skill, so be extra critical: look for places you relied on conversation context the skill doesn't contain.
- **Cowork / Claude Code:** if `skill-creator` is available, use its subagent eval tooling for independent runs and baseline comparison.

### Check each result
- Did it trigger for the right reason (would the description catch this prompt)?
- Did it follow the method, or improvise around a gap?
- Is the output the format and quality the blueprint promised?
- Did it rely on anything not in the skill files?

Fix every failure in the skill files, not by patching the test output. Then run:

```bash
python scripts/validate_skill.py <path-to-skill-folder>
```

Resolve all errors. Warnings are judgment calls; mention notable ones in Temper.
