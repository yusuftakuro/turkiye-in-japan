# Türkiye in Japan — Individual Entity profiles (2026-10-23)

The public-safe SSOT v1.2 projection supports **92 static HTML profiles**, from `places/ENT001.html` to `places/ENT092.html`. The explorer links to every profile.

- All pages are HTML-rendered at build time. JavaScript is not required to read the data or open an official link.
- Data fields: public name and identity class, Offerings, explicitly visitor-public Locations, Channels, source URLs, verified relations, record confirmation date.
- Current opening/booking/visitor status is **not inferred** from historical CSV fields. `provisional` identities remain labeled as such.
- Only place names and prefecture/city are shown, never `address`. Do not import internal or nonvisitor locations.
- Claims sourced after the original pilot are linked when available; older records may only have a published official URL. Do not create factual summaries unsupported by records.
- The detail pages are intentionally Japanese-only for now. English/Turkish content must be separately translated and reviewed, not auto-presented as verified.

Run after updating the public fixture:

```sh
node scripts/build_directory.mjs
node scripts/build_details.mjs
node scripts/check_details.mjs
node scripts/check_directory.mjs
npm test
```

The full SSOT archive and internal-only addresses remain outside the public repository.
