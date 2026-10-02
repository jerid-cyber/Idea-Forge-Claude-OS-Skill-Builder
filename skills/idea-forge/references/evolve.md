# Mode 7: Evolve

Goal: improve an existing skill from new notes, feedback, or field notes without losing what already works.

## Inputs Evolve accepts
- New ideas or notes the person wants folded in.
- Feedback ("it keeps doing X", "it missed Y").
- Field notes files (`field-notes/<skill-name>.md`) written by the skill during real use.
- An existing skill with no blueprint (reverse-engineer one first).

## Steps

1. **Load the current state.** Read the skill's files, its `BLUEPRINT.md` and `CHANGELOG.md` if present. If the skill is installed read-only, copy it to a writable working folder first. If there's no blueprint, reverse-engineer one from the skill and mark everything `(inferred)`.
2. **Capture the new material** as in `capture.md`. For field notes, group entries into patterns: one complaint is an anecdote; the same friction three times is a fix.
3. **Diff against the blueprint.** For each new item: does it add, change, or contradict the existing design? Contradictions with confirmed blueprint items need the person's decision; contradictions with `(inferred)` or `(default)` items can be resolved in favor of the new evidence.
4. **Gap Check** only for what the new material leaves unclear.
5. **Update** the blueprint first, then the skill files. Keep the skill's original `name` and folder name so it installs over the old version.
6. **Test** with the original test prompts plus at least one new prompt that exercises the change. A fix that breaks an old test isn't a fix.
7. **Temper** the updated version (Temper runs on every change).
8. **Version and log.** Bump the version, update the scorecard, and add a changelog entry.

## Versioning
- **Patch (1.0 → 1.0.1):** wording fixes, small examples, no behavior change.
- **Minor (1.0 → 1.1):** new capability or meaningful behavior change, backward compatible.
- **Major (1.x → 2.0):** changed purpose, split or merged skills, or anything that changes how people invoke it.

## Changelog format

```markdown
## <version> — <YYYY-MM-DD>
Source: <new notes | feedback | field notes | Temper>
Changed:
- <what changed and why>
Scorecard: Bigger <n> / Better <n> / Stronger <n> / Faster <n> / Triggering <n>

## Ideas parked
- <next-evolution idea> (from <version>)
```

## Field notes hygiene
After an Evolve run consumes field notes, tell the person which notes were addressed. Where files persist, move addressed entries under an "Addressed in <version>" heading rather than deleting them, so the history stays traceable.
