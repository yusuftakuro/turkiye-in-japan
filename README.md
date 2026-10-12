# Türkiye in Japan — stable UI starter v0.1

## Why this version is intentionally simple

This starter removes the blank-screen failure mode of the earlier prototype. Critical page content is present in static HTML, and ordinary links work even if JavaScript fails. Search/category filtering in `explore.html` is progressive enhancement. **This is not the entire SSOT v1 fixture**: only grounded examples from the original 2026-10-03 pilot are present; the final migration ZIP was not available in this chat.

## Pages

- `/index.html` — HOME and entry links
- `/explore.html` — discovery and optional client-side filters
- `/dogal.html` — distinguish online shop from closed physical store
- `/tokyo-camii.html` — one facility, multiple offerings
- `/events.html` — honest empty state

## Local development

No npm install or build is required.

```bash
npm test
python3 -m http.server 4173
```

Open `http://localhost:4173/` in a browser. **Do not test from `file://` or a chat attachment preview**.

## GitHub / Netlify setup

1. Create a new repository `turkiye-in-japan` on GitHub, preferably private while developing.
2. Commit all files at the root, including `.github/workflows/check.yml`.
3. In Netlify: Add new project → Import existing project → GitHub → select this repo.
4. Publish directory: `.`; no build command. A root `netlify.toml` includes these settings.
5. Enable Deploy Previews for pull requests; use preview URLs on the iPhone in Safari.
6. Do **not** declare acceptance until HTTPS preview opens on iPhone and HOME → explore → Dogal works.

`main` should represent the last human-accepted state. Implement new features via issue → branch → pull request → automated check → HTTPS Deploy Preview → iPhone check → merge.

## Deployment gates

- `npm test` passes
- Static contents appear without JavaScript
- Browser screenshot demonstrates viewport without overflow
- Navigation and filter links work
- No console errors
- HTTPS deploy preview is live
- User verified iPhone Safari

## Data provenance

Examples (Dogal, Tokyo Camii, Çankaya, Kilim Tokyo, Turkey Culture Center) are from the 2026-10-03 pilot file. Exact runtime states should not be treated as refreshed to the current day. External links go to official sites observed in that pilot.

## Technical growth rule

Do not introduce TypeScript/Vite/backend/database until actual product functionality requires it. The static baseline is an explicit reliability checkpoint, not a final architectural decision. Any future migration must preserve no-JavaScript readable content or supply an equivalent server-rendered fallback.