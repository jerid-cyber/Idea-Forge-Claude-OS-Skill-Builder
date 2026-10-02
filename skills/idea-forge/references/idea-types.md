# Idea Types: The Adaptive Core

Different kinds of ideas need different skill architectures. Classify every idea as a weighted mix of five types, then build to match the mix. Most real ideas blend two or three.

## The five types

### Process
**Signals:** steps, sequences, "first... then...", checklists, workflows, handoffs, approvals.
**Architecture:** ordered steps in SKILL.md with clear entry and exit conditions. Checkpoints where the person must approve before continuing. Branches for common variations. Keep each step's "why" so Claude can adapt when reality differs from the script.
**Common failure:** too rigid. Real inputs skip or reorder steps. Add "skip this step when..." guidance.

### Knowledge
**Signals:** expertise, reference material, facts, frameworks, "you need to know...", long documents.
**Architecture:** lean SKILL.md that routes to reference files by topic. One reference file per domain or subtopic, each with a clear "read this when..." pointer. Tables of contents for files over 300 lines.
**Common failure:** dumping everything into SKILL.md. Progressive disclosure matters: Claude should load only what the current task needs.

### Judgment
**Signals:** "it depends", "I usually", trade-offs, prioritization, diagnosis, quality calls, coaching.
**Architecture:** decision rules with the reasoning behind them, plus at least 3 worked examples showing the judgment applied to different situations, including one where the obvious answer is wrong. Name the factors the person weighs.
**Common failure:** reducing judgment to a rigid rule. Capture the factors and the reasoning, not just the verdict.

### Voice
**Signals:** tone, brand, style, "sound like me", copywriting, persona, formatting taste.
**Architecture:** a voice guide (traits, each with a do and a don't), before/after rewrites, vocabulary to use and avoid, and 2+ real samples of the person's own writing when available.
**Common failure:** describing voice with adjectives alone ("friendly, professional"). Examples carry voice; adjectives don't.

### Tool
**Signals:** data processing, file conversion, calculations, scraping, formatting files, repetitive mechanical work, integrations.
**Architecture:** scripts in `scripts/` for anything deterministic or repeated, with SKILL.md explaining when to run them and how to interpret results. Note required packages and platform limits.
**Common failure:** asking Claude to do by hand what a 30-line script would do perfectly every time.

## Scoring the mix

Assign rough percentages that sum to 100. They don't need precision; they need to drive decisions:

- Any type at **40% or more** shapes the core of SKILL.md.
- Any type at **15 to 39%** gets its own section or reference file.
- Below **15%**, a few lines suffice.

Example: a real estate listing-presentation coach might be Judgment 40 / Voice 25 / Knowledge 20 / Process 15. So the core of SKILL.md is decision rules with worked examples, there's a voice guide and a market-knowledge reference, and the process gets a short ordered checklist.

## When the mix says "split"

Consider multiple skills when:
- Two parts would trigger on completely different requests.
- One part is used far more often than the rest.
- Different audiences use different parts.
- The combined SKILL.md would exceed roughly 500 lines even with good reference files.

Keep it as one skill when the parts are always used together; splitting forces the person to invoke several skills for one job.
