# Contributing to Skill Forge

The fastest way to make Skill Forge better for everyone is to share what you learn.

## Share a lesson (community pattern library)

1. Ask Claude: "Share my Skill Forge lessons." It runs `scripts/patterns.py export`, flags personal data, and helps you anonymize.
2. Open an issue with the **Pattern proposal** template and paste the block, or open a pull request adding lines to `skills/skill-forge/patterns/community-patterns.md`.
3. The maintainer reviews it. Accepted lessons ship in the next release, so every user's forges get smarter.

A good lesson describes a pattern, not a story; explains why; and contains no names, clients, locations, contact details, or private links.

## Propose a method change

Use the **Methodology proposal** issue template. Include evidence from real forges.

## Code changes

Run the checks before opening a pull request. GitHub runs them too.

```bash
python skills/skill-forge/scripts/validate_skill.py skills/skill-forge
python skills/skill-forge/scripts/patterns.py lint skills/skill-forge/patterns/community-patterns.md
python tests/run_tests.py
```

Scripts use the Python standard library only, so Skill Forge runs anywhere Claude does. Please keep it that way.
