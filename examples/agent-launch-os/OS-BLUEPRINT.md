# OS Blueprint: agent-launch-os
Version: 0.2   Status: confirmed   Builder: power user (worked example)

Forged from a voice dump about coaching new real estate agents through their first 30 days.

## 1. Mission
Get every new agent to their first appointment within 30 days.

## 2. Scoreboard
Days from start to first appointment. Baseline 45, target 30.

## 3. Core loop
Build sphere → call daily → log conversations → set appointment → measure → repeat. The command center owns "what's next."

## 4. Brain (`os/brain.md`)
profile (setup) · sphere (sphere-builder) · call_log (daily-call-coach) · appointments (appointment-tracker) · current_state · next_moves (command center)

## 5. Components
| Skill | Reads | Writes | Hands off to | Authority | Wave |
|---|---|---|---|---|---|
| sphere-builder | profile | sphere | daily-call-coach | auto | 1 |
| daily-call-coach | profile, sphere, call_log | call_log | appointment-tracker | suggest | 1 |
| appointment-tracker | call_log | appointments | command center | auto | 1 |
| open-house-planner | profile, appointments | current_state | command center | approve | 2 |

## 6. Orchestrator
Stage-based: week 1 sphere building; from day 8 daily calls regardless of sphere size (sphere building continues alongside); appointments go to the tracker; open houses only from day 15.

## 7. Cadence and events
Daily heartbeat. Events: appointment set; zero calls two days in a row.

## 8. Governance
Sphere building and tracking are internal (auto). Calls are made by the agent (suggest). Booking open houses or inviting the sphere needs the broker's approval.

## 9. Glossary
**Sphere:** everyone the agent personally knows. Never "contacts."

## 10. Out of scope
Contracts, legal, and pricing questions go to the broker.

## Test history
See `SIMULATED-WEEK.md`: two logic issues found and fixed (stage-gate stall, ramp-up rule clash).
