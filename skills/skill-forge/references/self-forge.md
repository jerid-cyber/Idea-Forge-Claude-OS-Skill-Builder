# Self-Forge: Improving Skill Forge Itself

Skill Forge applies its own method to itself. It learns from every forge and proposes improvements to its methodology, always for the owner's approval.

## Two kinds of learning

**Lessons** are about *skills in general*: "Judgment skills with fewer than 3 worked examples underperform." These go in `patterns/pattern-library.md`. Adding a lesson is low-risk; still tell the person what you added.

**Methodology proposals** change *how Skill Forge works*: a new mode, a different question limit, a new Temper lens, a changed default. These always require explicit approval.

## When to raise a proposal

At the end of a forge, raise a methodology proposal only when there's evidence, such as:
- A mode added nothing across several runs, or a step was skipped every time.
- The person had to correct Skill Forge's process (not just the skill's content).
- A failure in testing traces back to a gap in Skill Forge's method, not the specific skill.
- The same lesson appeared in three or more forges, suggesting it belongs in the core method.

Don't raise a proposal every run. Signal over noise.

## Proposal format

```
SELF-FORGE PROPOSAL
Change: <what would change in Skill Forge>
Evidence: <what happened that suggests it>
Effect: <how future forges would be better>
Files affected: <which Skill Forge files>
Risk: <what could get worse>
```

## Applying an approved proposal

1. Copy Skill Forge to a writable location if it's installed read-only.
2. Edit the affected files. Keep `name: skill-forge` unchanged.
3. Run `scripts/validate_skill.py` on Skill Forge itself.
4. Add a dated entry to Skill Forge's own `CHANGELOG.md`.
5. Deliver the updated package. In Cowork and Claude Code, write it in place if the person agrees. In Claude.ai chat, hand over the files for re-install.

## Community contributions (public use)

When Skill Forge is shared publicly, users may propose lessons or methodology changes back to the maintainer. A contributed lesson should state the pattern, the evidence, and an example. The maintainer approves what enters the canonical pattern library.
