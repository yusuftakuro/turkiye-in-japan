# Issue #26 — Dogal online sales correction candidate

**Checked:** 2026-10-25 (Asia/Tokyo)  
**Baseline:** `main` at `b374ce19b50acc3d9b8ca487da700b59dc7ff996`  
**Source:** [Doğal Official Online Shop](https://dogal.jp/)  
**State:** review candidate for independent QA; not a private full-SSOT update, merge, or release.

## Source finding

The operator's homepage currently retains product navigation and catalogue links. Its notice says online-shop sales ended on **2026-05-31** and separately says Turkish Cafe & Bar Doğal continues operating. This is an internal page-content conflict; the dated, explicit closure notice is the direct evidence for the online sales status. No checkout was used to override that statement. The notice does not establish a café Offering, channel, or visitor Location, so this candidate adds none and does not reuse former market Channel `CH037`.

## Candidate changes

- `OFF011.availability_status`: `available` → `unavailable`; checked 2026-10-25.
- `CH002.availability_status`: `available` → `unavailable`; checked 2026-10-25.
- Entity `ENT010`, historical market Channel `CH037`, all Entity/Offering/Location IDs, and public visitor-location rows are unchanged.
- Explore cards derive activity filters from Offerings whose status is not `unavailable`. `unknown` remains included. Dogal's card states the online sales end date and that it is separate from café operations; Dogal is removed from the current SHOP filter.
- The generated static detail page labels the online sales Offering as unavailable, displays the dated closure notice, and links to the official source. The notice is present in Japanese fallback HTML and has English/Turkish UI translations.
- The full proposed private fixture has not been accessed or changed. The public-safe projection edit is interim and must be reconciled to the private fixture by 00 before any canonical promotion.

## Validation

Commands run locally:

- `npm test` — PASS, including targeted checks for OFF011/CH002 status, exact closure date/source, Dogal's SHOP-filter exclusion, retained `unknown` retail in the SHOP filter, static detail notice, and protected record counts.
- `node scripts/check_directory.mjs` — PASS; 92 distinct cards and reproducible generation.
- `node scripts/check_details.mjs` — PASS; 92 generated detail pages match their source data.
- `node scripts/check_i18n.mjs` — PASS; all 92 pages retain localization and generated output is current.
- `python3 scripts/check_canonical_public_v12.py` — PASS; 92 Entities, 115 Offerings, 64 Channels, 38 public Locations, 155 evidence rows.
- `node scripts/check_i18n_browser.mjs` — NOT RUN: this environment has no Chrome/Chromium binary. Browser-rendered EN/TR output needs independent verification.

Static HTML remains readable with JavaScript disabled. No private or nonvisitor address was added. Rollback is to close this unmerged PR or revert its branch; no live files or `main` were changed.
