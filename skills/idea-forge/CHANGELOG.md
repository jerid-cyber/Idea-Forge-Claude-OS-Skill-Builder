# Changelog: idea-forge

## 2.1 — 2026-10-02
Source: owner request
Changed:
- Renamed from Skill Forge to Idea Forge, tagline "Your Claude OS & Skill Builder", so the name says what goes in (ideas) and the tagline says what comes out (skills and operating systems). Install as a new skill and remove the old skill-forge so the two don't compete.
Scorecard: Bigger 5 / Better 4 / Stronger 4 / Faster 3 / Triggering 4 — Faster still lags: no quick-forge path yet

## 2.0 — 2026-10-02
Source: new notes (OS-Forge)
Changed:
- Three scales: Skill, Family, OS. Interpret picks the scale with a stated reason and builds smaller when the signals don't justify an OS
- OS Blueprint and os.json: mission, scoreboard, core loop, shared brain, components with reads, writes, handoffs, authority, and waves
- OS architecture guide: brain, setup, orchestrator, heartbeat and events, handoffs, governance, logs, common failure modes
- OS build in waves, simulated-week test, system-level Temper, consultant client handoff package
- Builder profiles: business owner, consultant, power user
- New scripts: os_scaffold.py, validate_os.py (strict and inferred audit of any OS-style plugin), os_map.py (visual system map with health findings)
- Worked example: Agent Launch OS, forged from a voice dump; the simulated week caught and fixed two logic bugs
- Community pattern library 2.0 with four OS lessons
- License: consultants may build for paying clients
Scorecard: Bigger 5 / Better 4 / Stronger 4 / Faster 3 / Triggering 4 — Faster still lags: no quick-forge path yet

## 1.1 — 2026-10-02
Source: Temper (Next evolution, approved)
Changed:
- Family Forge: scans skill folders for overlap (family_scan.py), proposes merge, plugin family, shared reference, or router; bundles approved families (build_plugin.py); runs a quick check after every forge
- Community pattern library: local and community libraries split; lint, export (with personal-data flags), and sync tooling (patterns.py); GitHub issue template, contribution guide, and CI check
- Visual scorecard: self-contained HTML growth chart, radar, and version table across one or many skills (scorecard_chart.py), generated at Ship and after every Evolve
- Automated test suite (tests/run_tests.py) run locally and by GitHub Actions
Scorecard: Bigger 5 / Better 4 / Stronger 4 / Faster 3 / Triggering 4 — still question-heavy for first-time users; needs a quick-forge path

## 1.0 — 2026-10-02
Source: initial forge
Changed:
- Modes: Capture, Interpret, Gap Check, Architect, Build & Test, Temper, Evolve, plus Self-Forge
- Skill Blueprint as the single translation layer
- Adaptive idea-type mix (Process, Knowledge, Judgment, Voice, Tool)
- Temper suggestion loop: four lenses, three tiers, moonshot by default; runs before launch, after real use, and on every change
- Field notes hook, version scorecard, seeded pattern library, scaffold and validate scripts
Scorecard: Bigger 4 / Better 4 / Stronger 3 / Faster 3 / Triggering 4 — needs real-world forges to tune question limits and seed more patterns

## Ideas parked
- Portfolio dashboard combining Family Forge, OS maps, and scorecards across a whole library (from 1.1)
- Quick-forge path: one message in, working skill out, Temper afterward (from 1.0)
- Compact Temper for patch-level changes (from 1.0)
