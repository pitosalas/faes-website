# Feature description for feature F06
## F06 — Content schema amendments: grant type and public/private flag
**Priority**: High
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Two additions to the content front matter schema required by the spec:
1. **Grant type field**: grants must have a `grant_type` field with values `pilot` or `primary` (reflecting the two tiers: XCG 2,500–10,000 vs XCG 10,000–100,000). Update `content/README.md`, seed grant files, `ContentLoader` validation, and tests.
2. **Public/private flag**: all content files must have a `public: true | false` front matter field. Only content marked `public: true` is included when the site is generated. Update schema docs, seed files, `ContentLoader`, and ensure generator respects this flag. Tests must cover that private content is excluded from generator output.
