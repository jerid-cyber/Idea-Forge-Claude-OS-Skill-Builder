# Changelog: skill-forge

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
- Quick-forge path: one message in, working skill out, Temper afterward (from 1.0)
- Compact Temper for patch-level changes (from 1.0)
- Full worked example of an end-to-end forge in the repo (from 1.0)
