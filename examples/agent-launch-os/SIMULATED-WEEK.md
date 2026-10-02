# Simulated week: Agent Launch OS v0.1
Scenario: new agent starts Monday, is nervous about the phone, and knows fewer people than expected.

| Day | What ran | Brain change | Problem |
|---|---|---|---|
| 0 | brain-setup | profile filled (start date, CRM, broker) | none |
| 1 | command-center → sphere-builder | sphere: 40 | none |
| 3 | sphere-builder | sphere: 60 | none |
| 5 | sphere-builder (memory jogger, under 100) | sphere: 90 | none |
| 8 | command-center → sphere-builder again | sphere: 105 | **STALL:** routing waits for 150 before any calls start. An agent with a small sphere never reaches the calling stage, so the OS never produces an appointment. |
| 8 (after fix) | daily-call-coach (role-play, then 3 real calls) | call_log: 3 | **RULE CLASH:** "missed calls get made up" demands 17 calls on day 9 from an agent still in phone-confidence ramp-up. |
| 9 (after fix) | daily-call-coach | call_log: 6, one warm conversation | none |
| 10 | appointment-tracker | appointments: 1 (day 10) | none; scoreboard updated |

## Fixes applied
1. Orchestrator: sphere building is time-boxed to week 1; calls start on day 8 no matter the sphere size, and sphere building continues alongside.
2. Call coach: the make-up rule pauses during role-play ramp-up; the target steps 3 → 6 → 10.
