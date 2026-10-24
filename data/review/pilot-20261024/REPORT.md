# Issue #21 — 01 source verification pilot / QA handoff

**Review date:** 2026-10-24 (Asia/Tokyo; precise retrieval times not logged)  
**Main baseline (before write):** `3fb44752f3074a446bb31d349a0019edf6f80818`  
**Source baseline:** `main` `data/canonical/v1.2-proposed/*` and `places/ENT{001,010,042,070,086}.html`  
**Branch:** `work/01-source-pilot-five`  
**Issue:** [#21](https://github.com/yusuftakuro/turkiye-in-japan/issues/21)  
**Delivery state:** **QA candidate only**. Neither accepted canonical data nor a live-site update.

## Deliverables / definitions

- `entity_review_summary.csv`: **exactly five** rows, one per assigned Entity, with pre-change status, related IDs, sources, uncertainties and judgement (`unchanged`, `updated_candidate`, `HOLD`).
- `atomic_claim_candidates.csv`: **17** independently checkable claim/delta rows (`R001–R017`), containing prior record ID, observed official fact, actual source URL, checked date and promotion guard.
- This report: source interpretation, important conflicts and QA instructions.

Use review claim IDs only as workpaper identifiers. **Do not assign them live CLM IDs**, update `verified_at` in canonical data, or treat the checks as approval. Baseline data itself may be stale even if `verification_status=verified`.

## Summary (5 Entity)

| Entity | Result | Evidence and difference | Candidate action |
|---|---|---|---|
| ENT001 — Istanbul | **unchanged** | Company website [about](https://istanbul.co.jp/about/) and [access](https://istanbul.co.jp/access/) still publish the business and Ginza / Tokyo University Neoponte branches. The old `LOC001`, `LOC002`, `OFF001`, `CH029` identity/offerings align. | No canonical edit. Published normal hours are not proof a restaurant is open on an individual date. |
| ENT010 — Dogal | **updated_candidate** | The [official homepage](https://dogal.jp/) says **online sales ended 2026-05-31**. This directly contradicts `OFF011` and `CH002` marked `available` with a 2026-10-03 verification date. The same company site reports the café/bar continues operating; a [separate shop information page](https://dogal.jp/pages/%E5%BA%97%E8%88%97%E6%83%85%E5%A0%B1) says an earlier physical market closed 2025-03-23, but still includes an outdated online-order description. | Propose `OFF011 availability_status: available→unavailable` and `CH002 availability_status: available→unavailable`. Leave `CH037` unavailable. A new café Offering/Channel/Location is **HOLD** until the legal entity, brand, old-store and café boundaries are resolved. |
| ENT042 — Kushimoto Turkish Memorial Museum | **unchanged** | [Kushimoto Town](https://www.town.kushimoto.wakayama.jp/kanko/oshima/torukokinenkan.html) lists the exhibition, public visitor address, ordinary 9:00–17:00 visiting hours, daily operation and fee. Supports `LOC034` / `OFF045` source description. | Preserve `unknown` for present-day visit/availability unless 00 selects a new evidence-backed rule. Standard published hours are not real-time open status. |
| ENT070 — Kyoto Japan–Türkiye cultural association | **HOLD** | [Kyoto civic-group directory](https://dantai.hitomachi-kyoto.jp/detail/2161) displays an association and described activities; **last updated 2024-03-16**. It is a directory, not a new direct self-publication. Linked [organization-site candidate](https://www.kyoto-nitto.com/) timed out in this review; no verified 2026 schedule or visitor site. | Maintain `provisional`, `unknown`, blank official URL, all `OFF083–OFF086` unknown. Do not merge with similarly named separate organizations or publish its registered address as a visitor destination. |
| ENT086 — Keio Gaigo | **updated_candidate** | [University Turkish-language page](https://www.fls.keio.ac.jp/levelall-10aki/levelall-trk.html) explicitly identifies 2026 autumn Introductory and Elementary offerings. [University course terms](https://www.fls.keio.ac.jp/application.html) set regular applications for **2026-08-06 to 2026-09-14**, course period **2026-10-05 to 2027-01-25**, **Zoom-only**, no in-person lessons. | Propose a *time-scoped note* on `OFF105`/`OFF106`: regular fall applications closed and courses are remotely offered. No visitor location. Keep availability unknown; do not assume both classes ran or additional intake exists. |

## Proposed changes are not canonical mutations

| Target record / field | Baseline | Candidate proposal | Confidence / limitation |
|---|---|---|---|
| `OFF011.availability_status` | `available` | `unavailable` (online sales discontinued) | High: dated operator announcement; QA verify independent retrieval |
| `CH002.availability_status` | `available` | `unavailable` (online checkout no longer offered) | High: operator announcement; URL remaining readable is not an active checkout |
| `CH037` | `in_person / unavailable` | unchanged | High for historic market closure; **cannot** reassign to the café without identity review |
| `ENT010` associated café | not in current public-safe location/offerings | HOLD for distinct candidate records | Operator confirms café existence, but legal/brand/site relationship and safe public projection require 00/Owner decision |
| `OFF105`, `OFF106` | course names, `unknown` | evidence note: normal application period expired; remotely taught | Strong for semester terms; class-specific operation or additional enrolment unverified |
| `ENT070`, `OFF083–OFF086` | `unknown`, `provisional` | HOLD, no semantic promotion | Old registry alone cannot prove continuing operations |

Do not interpret the `ENT010` Entity's `active` flag as evidence that its **online sales channel** is active. The homepage explicitly distinguishes closed online sales from a continuing café. The fact that both original `OFF011` and `CH002` were labelled verified as recently as **2026-10-03** is a source-validation discrepancy worth separate 00 follow-up; this pilot is **not** authority for a mass recheck.

## Provenance and publication safeguards

- All findings above were checked from the URLs cited on **2026-10-24 JST**; source *publication dates* are only asserted where the operator or registry provides them. The date of this check is not proof of ongoing physical operation or acceptance of new enrollments.
- Visitor addresses already permitted by the existing public-safe projection: `LOC001`, `LOC002`, `LOC034`; no actual location records were modified.
- `ENT070` registration location has **not been copied** into candidate records; a mailing/registered location is not necessarily a visitor site. `ENT010` café has a publicly listed customer location, but no candidate record is created without identity scoping.
- Full private Library SSOT not loaded or modified. No attempt to infer private claims, internal-only addresses or full source mappings.
- Do not confuse Kyoto's `日本トルコ文化協会` with another association such as `一般社団法人日本・トルコ協会`; name similarity is insufficient to merge IDs.
- `places/`, public projection CSVs, scripts, site UI, i18n, and `main` are untouched by this branch's changes.

## Validation and independent QA checklist

1. Freeze this Draft PR's **exact head SHA** and independently obtain each primary URL; check claims `R001–R017` and compare with the preserved `main` baseline.
2. Confirm CSV has 5 distinct Entity IDs (`001/010/042/070/086`) and 17 review claims with populated provenance, dated check and remaining-unknown guards.
3. Check only `data/review/pilot-20261024/*` changed; no edits to `data/canonical`, `places`, generator, app code or static output; no private/nonvisitor address added.
4. Explicitly review the Dogal closed **online** Offering + Channel and separate café identity; the official source contains mutually inconsistent legacy and current content.
5. Verify whether the Kyoto association official homepage is actually accessible, and whether a more recent self-published event exists; if not, return **INCONCLUSIVE/HOLD**, not `active`.
6. Confirm the Keio fall-semester intake restriction applies to this semester, not all future offerings. No in-person classroom should be inferred.
7. Assess regression/test output independently. The source worker was **unable to clone** via the local runtime (`Could not resolve host: github.com`), so existing `npm test` and browser tests are **not claimed to have passed**; use GitHub CI or a QA runner.

## Operational result / rollback

- Starting `main` SHA: `3fb44752f3074a446bb31d349a0019edf6f80818`.
- Review count: 5 Entity; 17 atomic claim rows; 2 `unchanged` / 2 `updated_candidate` / 1 `HOLD`.
- Work usage / cost: **not measured** (no reliable usage meter accessible).
- Rollback: close the unmerged Draft PR or delete the review branch; production and canonical data remain as before.
- State to return: **QA**; 02 independent read-only verification, then 00 coordination / Owner action if appropriate. **NO MERGE / NO RELEASE**.
