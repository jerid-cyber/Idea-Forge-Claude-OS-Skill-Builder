# Community Pattern Library

Shared lessons from Skill Forge users everywhere, reviewed by the maintainer. Read-only for users; update by syncing a newer version (see `references/community-patterns.md`).

Format: `- **<pattern>** — <why> (source: <origin>[, evidence: <what happened>])`
Library version: 1.1

## Triggering
- **Descriptions should name the user's likely phrasings and say "even if they don't say X."** — Skills under-trigger far more often than they over-trigger. (source: seed)
- **Name near-misses that should go elsewhere.** — Prevents a broad description from hijacking unrelated requests. (source: seed)

## Structure
- **Keep SKILL.md a router once it passes ~300 lines.** — Progressive disclosure keeps context lean and instructions sharp. (source: seed)
- **One topic per reference file, each with a "read this when" pointer.** — Claude loads only what the current task needs. (source: seed)

## Judgment and voice
- **Judgment skills need 3+ worked examples, including one where the obvious answer is wrong.** — Rules alone collapse nuance; examples carry the reasoning. (source: seed)
- **Voice is carried by samples and before/after rewrites, not adjectives.** — "Friendly and professional" describes nearly every brand. (source: seed)

## Robustness
- **Put an approval checkpoint before anything that sends, spends, deletes, or publishes.** — Irreversible actions are where skills cause real harm. (source: seed)
- **Explain the reason behind every hard rule.** — Claude generalizes from reasons; bare MUSTs get followed too literally or ignored at edges. (source: seed)
- **Translate other-AI infrastructure advice into intent.** — Generic answers often prescribe databases or frameworks a skill doesn't need; keep the goal, drop the plumbing. (source: seed)

## Speed
- **Every question should carry a default.** — Lets users skip ahead without blocking the build. (source: seed)
- **Move deterministic, repeated work into scripts.** — Scripts are faster and identical every time. (source: seed)
