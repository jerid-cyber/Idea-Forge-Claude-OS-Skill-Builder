# Mode 1: Capture

Goal: get everything out of the person's head and files, then normalize it into clean source material for the blueprint. Do not judge, organize, or question yet.

## Opening the dump

Invite a full dump in one message. Something like: "Give me everything: voice notes, outlines, docs, links, chat transcripts, examples of good and bad output. Order doesn't matter. I'll sort it and only ask about what's missing." If they've already shared material, skip the invitation and confirm what you have.

## Normalizing by input type

**Voice dictation / transcripts of speech.** Expect repetition, tangents, self-corrections, and filler. Keep the *last* version of any idea they corrected. Treat stories and anecdotes as gold: they usually contain the real rules and judgment calls. Pull out each story as a worked example.

**Typed notes and outlines.** Headings often reveal the person's mental model of the steps. Preserve their order and naming unless it is clearly accidental.

**Research docs, PDFs, links.** Separate *the person's own position* from *source material they collected*. Research is supporting evidence, not the skill's voice. Fetch links when tools allow; if a link cannot be opened, say so and ask for the key points.

**Other AI chat transcripts.** Be skeptical. Separate what the *person* said (decisions, preferences, corrections) from what the *other AI* proposed. AI-proposed content is only part of the blueprint if the person adopted it. Generic frameworks from other AIs (for example, vector databases or orchestration frameworks) often describe infrastructure a Claude skill does not need; translate the underlying intent instead of copying the architecture.

**Existing prompts, SOPs, templates, examples of good output.** These are high-value. Good-output examples become the skill's examples; bad-output examples become anti-patterns.

## The capture inventory

After normalizing, build an internal inventory with these buckets (it feeds the blueprint):

- **Intent statements:** what the person wants the skill to accomplish, in their words
- **Steps and sequences**
- **Rules and constraints** ("always", "never", "only if")
- **Judgment calls** ("it depends on...", "I usually...", "the tricky part is...")
- **Terms** that carry special meaning for this person or field
- **Examples:** good, bad, stories, edge cases
- **Audience and context:** who uses the skill, where, for what
- **Outputs:** formats, files, deliverables
- **Contradictions:** places where the material disagrees with itself
- **Open threads:** ideas mentioned but not developed

Contradictions and open threads become Gap Check candidates. Do not resolve contradictions by guessing.

## Reflect back briefly

Before moving on, reflect the essence in two or three sentences: "Here's what I'm hearing: you want a skill that..." This catches big misreads early and costs the person almost nothing.
