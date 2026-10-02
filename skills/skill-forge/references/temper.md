# Mode 6: Temper

Forging makes the steel; tempering makes it stronger. Temper is the proactive suggestion loop. Its job is to find what the designer didn't think of and push the skill **bigger, better, stronger, and faster** than they imagined.

## When Temper runs

- **Before launch:** after Build & Test, every new skill.
- **After real use:** whenever field notes or feedback arrive (via Evolve).
- **On every change:** any time a skill is updated, Temper runs on the updated version.

Default boldness is **moonshot**: always present all three tiers, including ambitious ideas. The person can ask for "polish only" on a given run.

## The four lenses

Work through each lens deliberately. Generate more ideas than you'll present, then keep the strongest.

### Bigger: scope and reach
- What adjacent tasks would the same user want next? Could the skill handle them with little added complexity?
- Who else could use this (other roles, industries, skill levels)? What would need to change?
- Is this really one skill in a family? Would a companion skill or a plugin serve better?
- Could it connect to tools, connectors, or other skills to do more of the job end to end?

### Better: quality of output
- Would an expert in this field be impressed by the output? Where would they wince?
- Are there enough examples, especially for judgment and voice?
- Which edge cases are unhandled?
- Does the output format fit how it'll actually be used (pasted, sent, printed, presented)?
- Is there a step where asking one smart question would sharply improve the result?

### Stronger: robustness (red-team pass)
Actively try to break it:
- Messy, partial, or contradictory input.
- A user who doesn't know the jargon.
- A request that's a near-miss (should it trigger? does it?).
- An instruction that, followed literally, produces a bad result.
- Missing approval checkpoints before anything irreversible.
- Platform differences (does it break in Claude.ai chat where files don't persist?).
- Stale facts: anything in the skill that will go out of date.

### Faster: speed and effort
- Can any question be replaced by a smart default?
- Can any manual step become a script?
- Is SKILL.md longer than it needs to be? Move detail into references.
- Can the user reach a first useful result sooner (quick mode, a template, a one-shot path)?

## Scope check

Before presenting, test every "Bigger" idea: does it make the core job worse, slower, or harder to trigger correctly? If yes, move it to Next evolution as a *separate* skill or plugin idea rather than an expansion. Ambition goes in the proposals; discipline goes in what's applied.

## Present in three tiers

```
QUICK WINS (small, safe, apply in minutes)
1. <change> — <why it matters>
...

FULL RENDITION (the improved version, ready to build now)
<2–4 sentence description of v-next: what changes and the combined effect>
Key changes: <short list>

NEXT EVOLUTION (where this goes in v2/v3, the moonshots)
1. <idea> — <what it unlocks> — <rough effort: small / medium / large>
...
```

Guidelines:
- 3 to 6 quick wins, one full rendition, 2 to 4 next-evolution ideas.
- Tag each item with its lens: [Bigger] [Better] [Stronger] [Faster].
- Lead with the single highest-impact item and say why.
- Be concrete. "Add 3 worked examples of price objections, including one where the agent should walk away" beats "add more examples."

## Applying

Nothing changes without approval. The person can approve all quick wins, pick individual items, approve the full rendition, or park ideas. Record parked next-evolution ideas in the skill's `CHANGELOG.md` under "Ideas parked" so future Temper runs build on them instead of re-suggesting them.

After applying, re-run the relevant tests, re-validate, and update the scorecard (`templates/scorecard.md`).
