# Türkiye in Japan — Research intake registry (staging, 2026-10-22)

This directory is the **non-canonical research registry**, not the published website and not the final SSOT v1 database. It is safe to grow while the accepted v1 migration fixture remains unavailable. Nothing here changes the website on `main`.

## State and totals

| Stage | Candidate Entities | State |
|---|---:|---|
| `wave001` | 24 | sourced; identity merge pending |
| `wave002` | 12 | sourced; identity merge pending |
| `wave003` | 18 | sourced; identity merge pending |
| **Total** | **54** | **0 canonically merged** |

Separately, the original pilot had 60 mixed-grain rows; an earlier migration reported 41 canonical Entities. These numbers must **not** be added together or treated as 54 verified active businesses. `pilot_identity_index.csv` is a **deduplication hint only**, not the authoritative pilot fixture (P013 and P057 have known column shifts).

## Useful files

- `candidate_catalog.csv` — all 54 candidate Entity identities plus URL provenance and review state.
- `waveNNN/entities.csv`, `sources.csv`, `claims.csv`, `claim_sources.csv` — supporting layered evidence.
- `wave003/claim_*.csv`, `wave003/location_entities.csv`, `wave003/channel_offerings.csv` — type-specific relationships.
- `wave003/events.csv` — scheduled/completed dated events, **not** confirmed availability.
- `wave003/existing_update_proposals.csv` — existing pilot/wave objects that must be **updated, not duplicated**.
- `../../integrated/possible_duplicates.csv` — suspected relationships, no automatic merging.

## CLI commands

```sh
python3 scripts/check_intake.py
python3 scripts/consolidate.py
python3 scripts/query_registry.py キリム
```

The consolidation builds `integrated/research_registry.sqlite3` locally. Python standard library only; no paid service, no Netlify, no database server.

## Data rules

1. SSOT v1.0 is authoritative; these temporary `W00N-*` IDs are NOT canonical.
2. A Source URL exists for each candidate; sources support explicit, atomic Claims. Statements on a page **do not prove current operating hours, stock, seats or attendance availability**.
3. For an `Entity`, record brand vs legal operator separately where grounded. For `Location`, do not publish an office as an accessible shop. For `Channel`, distinguish product purchase/booking from a generic information page.
4. Never silently collapse aliases or shared-domain organisations; review evidence first.
5. Historical events/closed locations remain records with past dates/status. Future events must be rechecked on their current page shortly before display.
6. Recover the accepted SSOT v1 migration fixture before merging. The source dataset must retain the 222 old Evidence correspondences and 60 original pilot mappings.

## Next definitive gate

Review the 54 candidates against the actual 41 accepted canonical Entities and old `EntityAlias`/`EntityRelation` tables, adopt only identity-confirmed records, then rerun the accepted v1 regression suite (reported 46 checks). Until then, `merge_state = NOT_MERGED` remains true.
