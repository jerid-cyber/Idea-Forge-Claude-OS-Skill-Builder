# Community Pattern Library

Goal: every user's forge makes everyone's smarter. Lessons learned in one person's builds are anonymized, reviewed by the maintainer, and shipped to all users.

## Two libraries, kept separate

- `patterns/pattern-library.md`: **local** lessons from this user's own forges. Theirs to edit freely.
- `patterns/community-patterns.md`: the **community** library, maintained in the Skill Forge GitHub repo. Read-only for users; updated by syncing a new version.

Read both during Architect and Temper. When they conflict, prefer the local lesson (it reflects this user's world) and mention the difference once if it matters.

## Contributing lessons (user → community)

Offer this when a forge produces a lesson that seems broadly useful, or when the user asks to share. Never send anything automatically.

1. Export new lessons:
   ```bash
   python scripts/patterns.py export patterns/pattern-library.md --community patterns/community-patterns.md
   ```
2. **Anonymize** with the user: remove names, companies, clients, locations, numbers, links to private pages, and anything that identifies a person or business. A lesson should describe a *pattern*, not a story. The export flags obvious personal data, but read every line yourself too.
3. Hand the user the contribution block and these steps: open an issue on the Skill Forge GitHub repo using the "Pattern proposal" template and paste the block in, or submit a pull request adding the lines to `community-patterns.md`.

A good contribution has a general pattern, the reason it matters, and the evidence (what happened in a forge that showed it). One story is an anecdote; the same lesson in several forges is a pattern.

## Syncing (community → user)

- **Claude Code / Cowork with the repo cloned:** `git pull`, then reinstall or copy the updated skill.
- **Any platform with a downloaded file:** get the latest `community-patterns.md` from the repo and run
  ```bash
  python scripts/patterns.py sync <downloaded-file> <path-to-skill-forge>
  ```
  The sync lints the file first and backs up the previous copy.
- **Claude.ai chat:** installed skills are read-only, so update by downloading the latest release and re-installing it. If web access is available, you can fetch the raw file from the repo to show the user what's new.

Never claim the library was updated when it wasn't.

## Maintainer review (for the repo owner)

Accept a community lesson when it:
- generalizes beyond one skill or industry,
- states a reason, not just a rule,
- contains no personal or client data,
- doesn't duplicate or contradict an existing lesson without explaining why.

Run `python scripts/patterns.py lint patterns/community-patterns.md` before merging. The repo's GitHub Action runs the same check on every pull request.
