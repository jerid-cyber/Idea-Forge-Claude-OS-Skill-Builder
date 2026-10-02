# Family Forge

Goal: spot when several skills overlap, and propose the right family structure: merge them, bundle them as a plugin, or extract a shared reference. As a library grows, overlap creates confusion (two skills competing to trigger) and duplicated upkeep. Family Forge turns a pile of skills into a system.

## When it runs

- **On request:** "do any of my skills overlap", "organize my skills", "make these a plugin".
- **Proactively, at the end of every forge:** if other skills are visible, run a quick scan with the new skill included and mention it only if the new skill overlaps something (one or two sentences, not a report).
- **During Temper:** a "Bigger" idea that amounts to a sibling skill is a Family Forge question.

## Where to find skills

Scan whatever skill folders are readable. Common locations:
- Claude.ai: `/mnt/skills/user/` and `/mnt/skills/plugins/` (read-only)
- Claude Code: `~/.claude/skills/`, `.claude/skills/` in the project, and installed plugin folders
- Any folder the person uploads or points to (for example, a cloned GitHub repo)

## Run the scan

```bash
python scripts/family_scan.py <folder> [<folder> ...]
```

Add `--json` for machine-readable output, or `--threshold 0.3` to show only stronger overlaps. The scan compares descriptions, names, and headings (TF-IDF similarity) and checks for shared reference files. Treat its output as a lead, not a verdict: read the overlapping skills' SKILL.md files before proposing anything.

## Decide the action

| Signal | Proposal | Why |
|---|---|---|
| Two skills do the same job (high similarity, same triggers, same output) | **Merge** into one skill | Competing skills trigger unpredictably and drift apart |
| Related skills serve one audience or workflow but different steps | **Plugin family** | Installs and updates as a unit; each skill stays focused |
| Different skills repeat the same knowledge (glossary, voice guide, rules) | **Shared reference** | One source of truth; fix once, fixed everywhere |
| A sequence is always run in order (A then B then C) | **Plugin + a router skill** | The router chains them so the user asks once |
| Similar, but one skill's description names or runs the other (scanner says CHAIN) | **Keep apart, clarify** | It's a designed pipeline; make each description say when to use which |
| Similar words but genuinely different jobs | **Leave apart, sharpen descriptions** | Add near-miss exclusions so each triggers cleanly |

Always check: would merging make the result over 500 lines or trigger on unrelated requests? If so, prefer a plugin family over a merge.

## Present the proposal

```
FAMILY FORGE
Family: <name> (<n> skills): <members>
What they share: <one sentence>
Proposal: <Merge | Plugin family | Shared reference | Router | Leave apart>
Effect: <what gets better for the user>
Risk: <what could get worse>
```

Nothing changes without approval.

## Apply an approved proposal

- **Plugin family:**
  ```bash
  python scripts/build_plugin.py <plugin-name> <output-dir> <skill-dir> <skill-dir> ... --author "<name>"
  ```
  This copies the skills into a new plugin folder with `.claude-plugin/plugin.json` and a README; the originals are untouched. Then sharpen each skill's description so siblings don't compete, and validate each one.
- **Merge:** build a combined blueprint from both skills (mark the source of each item), forge the merged skill through Architect and Build & Test, and keep the stronger skill's name. Log the merge in its CHANGELOG as a major version.
- **Shared reference:** create the shared file once inside the plugin, point each skill to it, and remove the duplicates.

After any family change, run Temper on the family as a whole: lenses apply to the system, not just each skill.
