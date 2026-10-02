# OS Build, Test, and Temper

## Build in waves

Never build the whole OS at once. A working small system beats an impressive broken one.

**Wave 1: minimum viable OS.** Brain, setup, orchestrator, heartbeat, and the components on the core loop (usually three to five). Wave 1 is done when one full cycle runs end to end: setup fills the brain, the orchestrator picks a move, a component does it and writes back, the scoreboard updates.

**Wave 2+.** Add components in groups that each close a new loop or remove a manual step. Each wave gets its own test and Temper pass.

## Steps

1. Generate the skeleton:
   ```bash
   python scripts/os_scaffold.py <os-name> <output-dir> --components "job one,job two,job three" [--cadence weekly] [--author "Name"]
   ```
   This creates the plugin layout, `os.json`, the brain and log templates, and working orchestrator, setup, and heartbeat skills with component stubs.
2. Fill in `os.json` from the OS Blueprint: reads, writes, handoffs, authority, and waves per component.
3. Write each component skill using the normal Build guidance (`architect-build.md`), adding the brain reads and writes, the handoff, and the authority line.
4. Write the orchestrator's routing rule and table, the setup interview, and the heartbeat schedule.
5. Validate the system, then each skill:
   ```bash
   python scripts/validate_os.py <os-folder>
   python scripts/validate_skill.py <os-folder>/skills/<each-skill>
   ```
6. Draw the system map:
   ```bash
   python scripts/os_map.py <os-folder> -o os-map.html
   ```

`validate_os.py` also audits existing OS-style plugins that have no `os.json` (inferred mode). Use it in Evolve to reverse-engineer and check an OS the person already built.

## Test: the simulated week

Single-skill tests can't catch system failures. Run a realistic week through the OS:

1. **Create a scenario** with the person's real context: who they are, what happens Monday to Friday (a new lead, a bad review, a slow day, a metric drop, an approval left waiting).
2. **Day 0:** run setup with the scenario's facts. Check the brain is complete.
3. **Each day:** run the orchestrator as the heartbeat or event would. Follow the routing to components, have each write back, and record the brain changes.
4. **Watch for:** dead ends (output nobody picks up), stale reads (a component using last week's data), approval pile-ups, the orchestrator picking the same move repeatedly, and scoreboard changes that don't trace to any action.
5. **Report** the week as a short log: day, what ran, what changed, problems found. Fix problems in the skill files and `os.json`, then rerun the days that failed.

In Claude.ai chat, run the simulation yourself by reading each skill and following it. In Cowork or Claude Code, independent subagents per component make the test more honest.

## System Temper

Run the four lenses on the system as a whole, in addition to each component:

- **Bigger:** which manual step between components could become a component? Which adjacent loop would double the OS's value? Should the OS connect to another OS?
- **Better:** does the orchestrator pick the moves an expert would pick? Is the scoreboard an outcome the person would pay for?
- **Stronger:** what happens when one component fails mid-cycle? When the brain has a wrong fact? When approvals sit for two weeks? When the person disappears for a month?
- **Faster:** how long from install to the first visible result? Which questions can setup skip by reading connected tools?

Present in the same three tiers, and include a recommendation for the next wave.

## Consultant handoff package

When the builder is a consultant (see `builder-profiles.md`), finish with a client package: a plain-language README for the client (what the OS does, what it needs from them, how approvals work), a filled brain from discovery, the system map, the scorecard baseline, and a 30-day check-in plan.
