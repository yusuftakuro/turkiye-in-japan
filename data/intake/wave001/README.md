# Database intake / wave001 (2026-10-17)

**Not canonical SSOT records.** This is an evidence-backed, non-destructive candidate ledger for the Türkiye in Japan project. The accepted 41-Entity SSOT v1.0 migration ZIP is not available in the current session, so these records cannot be safely merged into the canonical fixture yet.

- 24 candidate distinct Entity names, each with a primary Source URL and a Turkey-relationship/Offering description.
- Mostly Osaka, Kyoto, Aichi, Wakayama and Fukuoka to remedy the original Tokyo concentration.
- Proposed candidate ID prefix: `W001-` (temporary). Canonical IDs have **not** been assigned.
- Current operational status for every candidate is intentionally `unknown`; seeing an official listing is not a verified open-now result.
- Every item needs canonical duplicate/identity review before accepting. Historical listings and honorary consulates deserve additional care.
- Candidate update claims for legacy P047 are staged separately and must not overwrite prior history.

The complete import-format staging bundle (Entity, Location, Channel, Offering, Source, Claim, relations, QA) is an accompanying artifact in ChatGPT. This GitHub directory is its reviewable identity/source index, not a claim that the full relational migration has happened.

## Next action
Retrieve the accepted SSOT v1.0 fixture and evidence crosswalk, reconcile candidate IDs and identity, atomize claims, map validated Object relations, run 46 baseline regressions and intake-specific tests; only then promote to canonical. Leave the live GitHub Pages UX unchanged.

Related Issue: #2.
