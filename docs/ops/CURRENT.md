# CURRENT — Türkiye in Japan
Updated: 2026-10-24 (Asia/Tokyo)
Status: reorganization pilot; do not infer any worker is running from an Issue alone.

## Authority / sources
1. Owner's accepted requirements and decisions; changes require explicit approval where consequential.
2. Complete SSOT v1.2 **proposed** full fixture in private Library: canonical candidate, not public production data.
3. `main` on GitHub: implementation fact; `data/canonical/v1.2-proposed/` is public-safe projection and not the full private fixture.
4. This CURRENT: **task routing**, not a second data SSOT. GitHub Issues/PRs record task changes; CI and deployed website provide separate evidence.
5. AI Knowledge Lab is advisory only. Its docs are not required to resume; do not copy the Knowledge Registry or its rules into this project.

## Observed baseline
- Latest checked main at reset: `7cb6ab4f15b959339675ef5f039fa03d5787a175`. Always read fresh HEAD before acting.
- Deployed static site: https://yusuftakuro.github.io/turkiye-in-japan/
- 92 Entities, 115 Offerings, 51 provisional; 92 static profiles; Japanese/English/Turkish *interface*, not completely translated source content.
- 38 public-safe locations in proposed export; source and current operating/visit status require per-entity verification.
- 8 existing GitHub Actions workflows. No open PR observed at reset.
- Some inherited documentation is outdated (e.g. manifest describing v1.2 as not displayed online); do not rely on historical text over the actual current implementation.
- Existing Issues #1, #2, #4, #6, #8, #10, #12 have older history or outstanding questions. They are **not** implicitly assigned to a new lane; do not close without verification.

## Active pilot (5 entities)
- 00 coordination: [#23](https://github.com/yusuftakuro/turkiye-in-japan/issues/23).
- 01 source research / candidate changes (Work): [#21](https://github.com/yusuftakuro/turkiye-in-japan/issues/21).
- 02 independent QA / baseline / candidate review (Chat + CI): [#22](https://github.com/yusuftakuro/turkiye-in-japan/issues/22).
- Exact set: ENT001, ENT010, ENT042, ENT070, ENT086.
- No canonical merge, schema change, site content release or public availability assertion is authorized by this pilot.
- `01` may draft a proposal PR; `02` reviews a frozen commit read-only; `00` decides routing and separately requests authorization where needed.

## State machine
QUEUED → ACTIVE → QA → READY → INTEGRATED; exceptions HOLD / STOP.
- `01` reports deliverable as `QA`; NEVER declares own candidate canonically accepted.
- `02` reports PASS / FAIL / INCONCLUSIVE with sources and exact SHA; cannot mutate canonical/main.
- `00` advances status only using GitHub evidence, not text from old conversations.
- `READY` is not live. `INTEGRATED` requires merged PR + deploy and behavior checks when web changed.

## Immediate NEXT
1. Keep product unchanged while bootstrapping operations docs (current PR).
2. Owner opens `01` in Work and `02` in a separate Chat using `docs/ops/START.md`; this chat remains 00.
3. Run issue #22 baseline independently at fresh `main`, while issue #21 checks existing source facts and proposes changes.
4. Independent reviewer checks frozen PR SHA; 00 collates results and compares effort/quality against simple single-workflow baseline.

## Restart
Always read AGENTS.md, this document, own Issue, GitHub main/PR and relevant tests. No rehydration from Chat memory alone. If GitHub access or source evidence is unavailable, STOP_AND_REPORT accurately instead of inventing progress.
