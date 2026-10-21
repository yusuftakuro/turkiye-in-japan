# Türkiye in Japan — Database Expansion / Intake Wave 001

Research date: **2026-10-17**. This is a **candidate intake**, not an update to the accepted SSOT v1.0 canonical fixture.

The current GitHub repository contains a limited static UX prototype, not the 41-Entity SSOT v1.0 migration ZIP. That archive was unavailable in the current connected Library/Drive/project. To preserve identity, ID integrity, and the 46/46 accepted checks, this package **must not be silently appended to a phantom canonical database**.

## What was actually done

- Sourced new Turkey-related operators, organizations, cultural facilities, education, historical sites and public institutions across Japan (mostly outside Tokyo) using official organization websites and government/authorized directory records.
- Split proposed Entity / Location / Offering / Channel / Source / Claim objects with stable **staging IDs** (`W001-...`). All statuses default to `unknown` unless a separate current-state check can justify more.
- Every proposed Entity has one explicit Claim and a supporting Source URL, recorded in `claim_sources.csv`. Entity-level relation tags are distinct from topic suggestions.
- Private/nonpublic or uncertain office addresses are not copied into public visitor location data. Even when the Ministry of Foreign Affairs publishes a diplomatic postal address, that does not mean the office accepts walk-in visitors.
- The original v1 data cannot be positively de-duplicated without the v1 export; comparison with the initial pilot list was performed by name. Original P047 has two candidate updates only; nothing is overwritten.
- The saved candidate file does not claim 24 confirmed active or 24 canonical new entries. Identity and availability remain under verification.

## SSOT migration / review protocol

1. Retrieve exact accepted 41 Entity / 33 Location / 36 Channel / 43 Offering / 3 Event fixture and all Source/Claim ID mappings.
2. Compare candidate identities, Aliases, full official URLs, operators, and brands. Mark ambiguous entries `needs_review`.
3. Admit eligible entities only when evidence supports their distinct identity; remap `W001-...` IDs into canonical stable IDs in a crosswalk.
4. Split each compressed intake Claim into atomic claims (one verifiable fact per Claim), connect to typed `ClaimEntity` and other target junctions, and preserve Source.
5. Expand OfferingTopic, ChannelOffering and Entity relations only when supported by evidence; do not auto-inherit RelationTags.
6. Preserve prior records; apply P047 change as a new historical Location/Claim, not a destructive overwrite.
7. Run all previous 46 SSOT v1 regression tests and new tests for this intake (status, public access, same-name identity, 0 orphan FKs).
8. Merge to canonical only after QA PASS and clearly state canonical count changes, not staging count.

## Source interpretation

`verification_status=verified` in this intake means the *specific relationship/description claim* was observed in its source as of the research date. It does **not** mean the business is currently open, the appointment available, or every Offering can be booked. Data type fields are suggestions until canonical mapping.

`visit=yes` means official pages explicitly invite visitors. Unknown site status remains `unknown`. Honorary consulate entities have **no public-facing office Location** assigned by default.

## Data quality cautions

- The Kyoto Japan–Turkey Cultural Association appears in a directory last updated 2024. Current activity is unknown. Its contact/home address is intentionally omitted.
- The historic Istanbul Bazaar and Oya no Kai listings have not had a recent direct status confirmation. Do not show them as open/active on the site.
- The Osaka cultural center and NPO may be affiliated, but the relationship is not automatically asserted.
- Karanfil was previously branded Topkapi according to its own corporate history; this is a proposed same-entity historical Alias, not a new Entity or a merge with the unrelated Tokyo restaurant called Topkapi.
- Kushimoto Turkish Culture Association and its Cultural Center are separate operator/facility Entities linked by operated_by.
- Source Claim strings in this wave are *intake summaries*, not fully atomic canonical claims. They must be atomized before SSOT merge.