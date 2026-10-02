# Community Pattern Library

Shared lessons from Idea Forge users everywhere, reviewed by the maintainer. Read-only for users; update by syncing a newer version (see `references/community-patterns.md`).

Format: `- **<pattern>** — <why> (source: <origin>[, evidence: <what happened>])`
Library version: 2.0

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

## Operating systems
- **Time-box every stage gate.** — A gate that waits for a threshold (e.g. "150 contacts before calls") stalls the whole OS when the threshold is never reached; move on by a date and keep the earlier work running alongside. (source: idea-forge OS test forge, 2026-10-02, evidence: simulated week stalled on day 8)
- **Check that rules still hold together under ramp-up.** — Catch-up rules ("missed work carries over") collide with gentle-start rules and pile pressure on the people who most need less of it. (source: idea-forge OS test forge, 2026-10-02, evidence: simulated week demanded 17 calls on day 9)
- **Simulate a week before shipping an OS.** — Validators catch broken wiring; only a run-through catches stalls, rule clashes, and dead ends in the logic. (source: idea-forge OS test forge, 2026-10-02)
- **Default anything external to approve.** — An OS that sends, spends, or publishes on its own loses trust faster than one that asks. (source: seed)
