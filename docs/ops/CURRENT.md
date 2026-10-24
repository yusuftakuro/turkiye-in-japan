# CURRENT — Türkiye in Japan
Updated: 2026-10-24 (Asia/Tokyo)
Status: first five-Entity evidence pilot in QA/HOLD; P1 corrective Draft PR queued.

## Authority
- Owner sets priorities and approves consequential canonical, identity, privacy and public release changes.
- `main` is the implementation baseline; the **full v1.2 proposed SSOT** is separately held in private Library.
- `data/canonical/v1.2-proposed/` is a **public-safe projection**, not a complete private canonical fixture. 92 Entities, 115 Offerings, 51 provisional, 38 public-safe Locations.
- GitHub Issues/PRs record tasks and evidence; CI and live deployment require separate checks.
- AI Knowledge Lab is reference guidance, not a mandatory runtime dependency.

## Current GitHub state (checked 2026-10-24)
- `main`: `3fb44752f3074a446bb31d349a0019edf6f80818` at this checkpoint. Always refresh before acting.
- Site: https://yusuftakuro.github.io/turkiye-in-japan/ — 92 static detail profiles; ja/en/tr interface (not fully translated source content). No claim of all venues currently open.
- `01` five-record evidence review: [Issue #21](https://github.com/yusuftakuro/turkiye-in-japan/issues/21), [Draft PR #25](https://github.com/yusuftakuro/turkiye-in-japan/pull/25) at head `18f14bec0e99907e36f7a23c097b5dcd43302b4f`, **unmerged**. Exactly 3 new review-only files, 5 summary rows, 17 atomic evidence candidates. Existing site/data unchanged.
- `02` independent QA: [Issue #22](https://github.com/yusuftakuro/turkiye-in-japan/issues/22). Separate-Chat QA findings transcribed by 00 to GitHub; five *producer dispositions* accepted, but overall **HOLD** (P1 Dogal contradiction; not all named regression checks independently run). ENT070 current operation is INCONCLUSIVE.
- `00` coordination: [Issue #23](https://github.com/yusuftakuro/turkiye-in-japan/issues/23).

## Next active routing
1. **01 / P1 / QUEUED:** [Issue #26](https://github.com/yusuftakuro/turkiye-in-japan/issues/26) — propose correction of Dogal closed online sales (OFF011, CH002) and avoid misleading shop filter/profile. **New Draft PR, no merge or deploy.** Distinguish café/old market; no new Location or Entity without identity review.
2. **02 / QA:** complete unexecuted named checks for #25; then review #26 at its **new fixed head SHA** independently and read-only. Report PASS/FAIL/INCONCLUSIVE, URLs, scope, CI, site semantics.
3. **01 / P2 / QUEUED:** [Issue #27](https://github.com/yusuftakuro/turkiye-in-japan/issues/27) — Keio 2026 autumn enrollment deadline and Zoom-only format, time-scoped; after #26.
4. **00:** assess QA, Owner decision where needed, integrate only authorized reviewed changes; then verify actual deployment and public content.

## Scope/quality rules
- Entity identity, Offering availability, Channel availability, Location visitor access, course registration period and real-time opening are distinct fields/claims.
- `unknown` is not `available`. An online site still displaying a catalog does not by itself prove checkout is active. Ordinary hours do not prove live availability.
- Full private SSOT and public projection must not silently diverge; an interim projection correction must be labeled and reconciled later.
- No sensitive/private addresses in GitHub. No blanket translation of proper names or unverified claims.
- `01` may create candidate PR; `02` is READ_ONLY; `00` manages release gates.
- For product changes: tests, frozen SHA, independent QA, explicit merge gate, and post-deploy verification. Do not weaken tests.

## State machine
QUEUED → ACTIVE → QA → READY → INTEGRATED; exceptions HOLD / STOP.
- `READY` ≠ deployed.
- `INTEGRATED` for user-facing change requires merged SHA, CI and live-site verification.
- Chat and Work are not always-on background processes; opening a new Issue does not launch Work.

## Restart
Read `AGENTS.md`, this CURRENT, own Issue and latest GitHub head/PR/CI. `docs/ops/START.md` has copy-ready current prompts. Use task evidence, not stale chat context.
