# Türkiye in Japan — canonical v1 × intake (54) reconciliation

Date: 2026-10-22

## Included

- `candidate_crosswalk.csv` — all 54 candidate IDs and potential links to existing ENT IDs. Review only; no canonical merge performed.
- `summary.json` — reproducible counts and classification totals.
- `reconciliation-report.md` — manual review cases, integrity preservation, next gates.
- `reconcile_ssot_v1.py` — deterministic script for comparison. Requires an external local copy of the accepted SSOT v1 fixture (not committed to the public GitHub repo).
- `canonical-validation-rerun.json` — output from rerunning the bundled validator (46/46 PASS) with a temporary legacy Evidence CSV path compatibility copy.

The canonical ZIP remains unchanged and stored in Library: `/Türkiye in Japan/turkiye-in-japan-ssot-v1.0-migration.zip`. The 222 original Evidence IDs map to 232 rows. All data here remain a **research intake**, not publicly verified/active current listings.

## Reproduce

```sh
python3 reconcile_ssot_v1.py \
  --canonical-dir /path/to/ssot-v1-fixture \
  --intake-dir /path/to/turkiye-in-japan/data/intake \
  --output-dir /path/to/output
```

The script expects the accepted fixture's `entities.csv`, `sources.csv`, `entity_aliases.csv`, `pilot_record_mapping.csv`, `legacy_evidence_to_v1_mapping.csv`, and `acceptance-test-results.csv`, and the intake's three waves and combined candidate catalog.

## Acceptance boundary

There are 26 preliminary candidates with no observed canonical naming/domain collision and 28 items requiring explicit identity, scope, business channel, or granularity review. None has been assigned a canonical new Entity ID; added canonical Entity count remains **zero**. This is not evidence that only 26 candidates qualify for publication, nor proof that the other 28 are duplicates.