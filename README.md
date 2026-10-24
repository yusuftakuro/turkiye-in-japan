# Türkiye in Japan

日本にあるトルコ関連の店舗・団体・文化施設・講座などの情報を整理し、検索できる静的Webサイト。

**Website:** https://yusuftakuro.github.io/turkiye-in-japan/

## Current state (2026-10-24)

- `main` contains the publicly visible site, including 92 Entity profiles and 115 related Offerings.
- 51 Entity records are **provisional**. Inclusion is not proof of current opening hours, service availability or visitor access.
- Searchable listing at `explore.html`; one static profile per Entity at `places/ENT###.html`.
- Japanese, English and Turkish *interface* available through `?lang=ja|en|tr`; full translation and editorial QA of all source content are **not** complete.
- Public-safe SSOT v1.2 **proposed** projection is in `data/canonical/v1.2-proposed/`. The full candidate fixture is separate in private Library. Never copy private/office-only addresses into this public repo.
- Browser and directory tests run through GitHub Actions; the site's information is still subject to QA and publication readiness checks. Do not treat historical verification dates as current.
- `noindex` is intentionally set for the preview stage; do not remove without an explicit release decision.

## Operations and restart

- [AGENTS.md](AGENTS.md) — short shared limits and workflow.
- [CURRENT](docs/ops/CURRENT.md) — current responsibilities, exact issues, next pilot actions.
- [START](docs/ops/START.md) — copy-ready setup for 00, 01 and 02.
- [Coordination #23](https://github.com/yusuftakuro/turkiye-in-japan/issues/23) · [Producer #21](https://github.com/yusuftakuro/turkiye-in-japan/issues/21) · [QA #22](https://github.com/yusuftakuro/turkiye-in-japan/issues/22).

Do not create three permanently running Work processes. The default is one coordinator Chat, one active production Work task, and an independent read-only QA Chat plus existing CI. Temporary parallel work must have disjoint files and measurable benefit.

## Local verification

```sh
npm test
node scripts/check_directory.mjs
node scripts/check_details.mjs
node scripts/check_i18n.mjs
python3 scripts/check_canonical_public_v12.py
```

`node scripts/check_i18n_browser.mjs` additionally requires headless Chromium. CI success alone does not prove the deployment is live or user-facing information is current.

## Release

Changes use a bounded branch → PR → CI → independent QA where useful → 00 routing → merge → public-site verification process. Major spec, identity, privacy, rights, canonical schema or general-public release changes require Owner decision. Site deployment is handled by GitHub Pages; there is no new backend or database service in this stage.
