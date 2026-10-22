# Türkiye in Japan — DB intake wave 002 (2026-10-21)

**Status: staging only, NOT merged into the accepted SSOT v1.0 fixture.**

## Scope

- 12 proposed Entities: Kyushu Turkey association, archaeology and museum research, Turkish language education, craft workshops, restaurant, Turkish textiles/sweets retail, official cultural-tourism body, and historically documented pop-up retail.
- 7 Locations; 12 Offerings; 5 usable Channels; 2 dated Events; 18 Source URLs; 34 atomic Claims with typed Claim junctions.
- Events: 2026-01-02—2026-03-30 **ended** Rabirent pop-up at Sendai Mitsukoshi; 2026-10-26 **scheduled** cooking class by existing Turkish Cultural Center (legacy P040). Review real-time announcements before public use.
- Legacy proposal: P048 2026 autumn Turkish course (existing Japan-Turkey Society), P040 cooking class. **Neither is a new Entity**.

## Provenance and correctness rules

- This package records only sourced assertions; a verified Claim does **not** verify an Entity's ongoing operations or a Channel's available inventory.
- Claim / Entity, Claim / Location, Claim / Channel, Claim / Offering, Claim / Event use **typed junction tables** per SSOT v1.0. Each ClaimSource is supports/contradicts. Values are intentionally atomic whenever possible.
- Sources list original pages and retrieval/check date. No source page was given a guessed publication date.
- Event venues are *not* assigned to organizer Entities as permanent branches.
- Office locations of the embassy and private associations are not promoted to public visitor locations.
- JIAA's field site is in Türkiye; the database's Japan-side record concerns a Japan-linked institution. The physical Institute in Turkey is not counted as a Japan location.
- The association business/operator relationships are **not guessed**. JIAA part_of Middle Eastern Culture Center is sourced explicitly.
- Historical Rabirent pop-up does not substantiate an ongoing store, and its Entity is marked needs_review.
- Do not infer offering status from a currently accessible official website.

## Relationship to existing data

- Initial pilot 60 rows exact name comparison: PASS.
- Previous W001 24 candidate entity names and official URL comparison: PASS.
- Accepted migrated SSOT v1.0 41-Entity fixture: **NOT AVAILABLE**. Every W002-* identifier is a staging identifier, not canonical.
- Source snapshot is 2026-10-21; no claims of completeness.

## Import gate

1. Retrieve actual SSOT v1 fixture, including 222 legacy Evidence crosswalk, 60-pilot mapping, Sources and Claims.
2. Conduct identity + Alias + operator + address + URL collisions against canonical data (not only name/URL).
3. Re-map staging IDs to canonical UUID/IDs and join existing records where appropriate.
4. Recheck current operating status, event status, public access per typed TTL.
5. Run SSOT v1 existing 46 tests and new FK/claim/URL validations.
6. Merge only via reviewed PR. The public GitHub Pages website is not modified by this intake.

## Internal validation

- Errors: 0. See `summary.json` for counts and QA result.
- Source citations (human review): see `sources.csv`.