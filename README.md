# Türkiye in Japan — UI starter v0.1

**Status:** UX / development baseline, not a live or complete service.
**Source of truth:** Türkiye in Japan — SSOT v1.0.
**Data:** Limited, source-grounded examples from the 2026-10-03 pilot; not the full SSOT v1 migrated fixture. Confirm current operating status on each provider's official page.

## Pages
- `index.html` — home and discovery entry points
- `explore.html` — find by activity, topic, and keyword
- `dogal.html` — online store vs closed physical location
- `tokyo-camii.html` — one facility with multiple offerings
- `events.html` — upcoming events empty state

The essential content is directly in HTML. Links and copy remain usable without JavaScript. Filters are progressive enhancement.

## Local verification

```sh
npm test
python3 -m http.server 4173
```

Open http://localhost:4173/ in a browser — **not** a local file preview in ChatGPT.

## GitHub Pages publication

The site needs no dependency installation or build tool. Host directly from GitHub Pages (no Netlify).

1. Set the repository `yusuftakuro/turkiye-in-japan` to **Public** on GitHub Settings > General > Danger Zone > Change visibility. All repository source, history, and issues become public.
2. Open Settings > Pages > Build and deployment.
3. Source: **Deploy from a branch**. Branch: **main**; folder: **/(root)**. Save.
4. Wait for GitHub Pages to show a live HTTPS URL. Verify it opens on iPhone Safari.

The URL should normally take the form `https://yusuftakuro.github.io/turkiye-in-japan/`, but **do not treat it as live until its HTTP status and actual page contents have been verified**.

Because the website is intentionally static, all navigation uses relative links and works under the `/turkiye-in-japan/` project path.

## Required acceptance gates

- `npm test` / GitHub Actions pass.
- HTML body displays without JavaScript.
- HOME → Explore → Dogal (and Tokyo Camii, Events) works.
- No broken CSS/JS requests or uncaught browser errors.
- 320–430px viewport: no major overflow / missing content.
- The live HTTPS URL is confirmed accessible.
- The user checks the same URL in iPhone Safari and accepts it.

A CI result or HTML file existing on GitHub is **not** evidence that the live site is working.

## Development policy

- Chat: scope, decisions, specification.
- GitHub Issues: testable work units.
- Feature branch + PR: code changes and automated checks.
- The published `main` branch is the last accepted state.
- No claim of release success without a real URL and a user-visible validation.

Do not import the malformed original pilot P013/P057 rows as canonical data. No guessed identities, addresses, availability, translated text, or event dates.
