# Türkiye in Japan — compact agent entrypoint

Read `docs/ops/CURRENT.md` and your assigned GitHub Issue before changing anything. These are workflow pointers, not alternate database authorities. Public repository: never commit private addresses, credentials, complete private Library SSOT or unreviewed personal data.

## Project in one paragraph
GitHub Pages static web directory about Türkiye-related places and organizations in Japan. `main` is implementation fact. Public-safe SSOT v1.2 proposed export at `data/canonical/v1.2-proposed/`: 92 Entity, 115 Offering, 51 provisional. The complete candidate full fixture is separate in private Library. 92 generated `places/ENT###.html` profiles, `explore.html`, and ja/en/tr UI. Listings do not prove that venues are open, courses available, or locations visitor-accessible.

## Scope and authority
- 00 coordination: decides priority, creates/assigns Issues, verifies PR/CI/deploy, escalates major decisions. Owner remains final authority for purpose/major spec, canonical changes with uncertain identity, schema, privacy/rights, mass edits, major redesign.
- 01 producer: bounded source/evidence research and implementations on its designated branch. Cannot final-QA own changes, mutate private/canonical data unilaterally, or merge/release.
- 02 QA: independent and read-only by default. Freeze exact PR commit and baseline, validate official sources, data semantics and UI, report PASS/FAIL/INCONCLUSIVE. No self-initiated changes, merge or release.
- Specialist: at most one by default, maximum two only for cross-domain risk; only when existing deterministic tests are insufficient.

## Non-negotiable invariants
- Do not confuse identity review with operational availability. Distinguish unknown, closed, historical and verified current states.
- Distinguish Entity, Location, Channel, Offering, Event, Source, atomic Claim. No automatic merge based solely on name/domain.
- Never publish office-only, registered, private or unverified visitor locations.
- Preserve IDs, source/Claim provenance, accepted data history and public-safe projection constraints.
- Do not translate proper names or unverifiable claims as if verified. UI has three languages; full content does not.
- Natural precise Japanese; no stock AI-generated metaphor, vague slogans, or decorative filler.
- Keep all 92 static detail pages readable with JavaScript off; localization is an enhancement.
- Check actual current state before work. Do not use stale branch, old PR or chat summary as authority.
- Do not bypass failing CI, weaken tests to pass or claim public deployment from merge alone.

## Working pattern
1. Fresh-read assigned Issue, HEAD, existing PRs and touched files.
2. Define a small testable scope, deliverable, out-of-scope and rollback.
3. Work in a named task branch. Separate candidate data from public canonical projection.
4. Run applicable validations; attach exact commit SHA, log/evidence and change summary.
5. Send compact RESULT: issue, state, files/records, sources, tests, concerns, next action.
6. Let 00 route QA and release; only explicit assigned authority authorizes irreversible action.

## Existing commands
`npm test`
`node scripts/check_directory.mjs`
`node scripts/check_details.mjs`
`node scripts/check_i18n.mjs`
`node scripts/check_i18n_browser.mjs` (headless Chromium required)
`python3 scripts/check_canonical_public_v12.py`

Details of temporary work and minimal mobile launch commands: `docs/ops/START.md`. This file is intentionally short; do not duplicate whole Knowledge Lab, SSOT, or prior chat history here.
