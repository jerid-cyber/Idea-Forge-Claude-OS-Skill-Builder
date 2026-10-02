# Version Scorecard

Rate each version 1–5 so improvement is measured, not guessed. Score honestly; a 5 means an expert would struggle to improve it on that dimension.

| Dimension | Question | 1 | 3 | 5 |
|---|---|---|---|---|
| Bigger | Does it cover the job end to end for its audience? | Narrow slice | Core job covered | Whole job plus natural next steps |
| Better | Would an expert be impressed by the output? | Generic | Solid | Expert-grade, specific |
| Stronger | Does it hold up against messy input and edge cases? | Breaks easily | Handles common cases | Robust, with checkpoints |
| Faster | How quickly does the user reach a great result? | Many questions, manual steps | Reasonable | Smart defaults, scripted, minimal friction |
| Triggering | Does it activate when it should and not when it shouldn't? | Misses often | Mostly right | Reliable, near-misses excluded |

Record in CHANGELOG.md:
`Scorecard: Bigger 3 / Better 4 / Stronger 3 / Faster 4 / Triggering 4 — <one line on biggest gap>`

The lowest score points to where the next Temper run should focus.

## Visualize it

Turn the scorecard history into a chart the person can open or share:

```bash
python scripts/scorecard_chart.py <skill-dir> [<skill-dir> ...] -o scorecard.html --title "My Skills"
```

The output is one self-contained HTML file (no external resources) with a growth line per dimension, a radar showing the latest version's shape against the previous one, and a version table with the weakest score highlighted. Pass several skills for a portfolio view. Generate it at Ship and after every Evolve. Deliver it as a file, or publish it as a hosted page where the platform supports that. It's also a good GitHub Pages asset.
