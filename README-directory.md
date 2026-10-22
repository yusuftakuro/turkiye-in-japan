# Türkiye in Japan: SSOT v1.2 provisional directory

The website explorer is a **static 92-Entity directory**, generated from `data/canonical/v1.2-proposed/*.csv`, a public-safe projection of the archived canonical **proposal**, not a live availability service.

- 92 Entities and 115 Offerings, including 51 provisional entities. Operating or booking status is **not guaranteed**.
- The full list is present directly in the HTML. JavaScript only filters the cards; broken JS must not mean a blank page.
- Public site displays only prefecture/city and approved location names from `public_access=yes` rows. It does not use `address` columns.
- Activity is derived exclusively from Offering type. Do not derive a user activity from general Entity relation tags.
- Three researched identities remain held in issue #12. Current HTML does not describe them as open or merge them.
- Original detail pages for Dogal and Tokyo Camii are unchanged.

To refresh after reviewing a new public-safe export:
```sh
node scripts/build_directory.mjs
node scripts/check_directory.mjs
npm test
```

The full historical data, unresolved identities, and private/nonvisitor locations remain in the Library ZIP. Do not copy them to the public repository.
