# Türkiye in Japan — data expansion review pack (wave001 + wave002)

**36 proposed entities (24 + 12), 0 approved canonical merges.** The existing 41-Entity SSOT v1.0 migrated canonical fixture archive is not available here, so the number of usable new canonical Entities is **not** yet known. Do not add 41+36 and label it a verified published database.

## Contents

- `combined/candidate_catalog.csv`: all 36 candidate entities, status flags, regional hints and their primary evidence URLs for quick review.
- `combined/summary.json`: count reconciliations and limits.
- `wave001/`: original 2026-10-17 intake package (24 entities), preserved untouched.
- `wave002/`: 2026-10-21 intake package (12 entities), normalized typed Claim relationships, 2 events, 18 sources and 34 Claims.

## What is excluded from the 36 count?

- Repeat activities/programs by the same legal entity or brand. Those become `Offering`, `Channel`, or `Event` rather than extra businesses.
- Existing Japan-Turkey Society autumn 2026 Turkish-language course and Turkish Cultural Center cooking workshop: staging updates to legacy P048/P040.
- 2026 Sendai Mitsukoshi pop-up is a completed `Event`, not a current Rabirent storefront.

## Next merge gate

Retrieve the *actual accepted* 41-Entity fixture and mapping, compare entity identities and aliases, convert all W001 summary claims into typed atomic claims, preserve historical status, run the 46 accepted regression checks, and merge only verified records. Wave2 does not imply that an official website indicates a shop currently open.