# Feature description for feature F08
## F08 — Password-protected private content preview
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: `uv run faes-website --serve --private` generates all content (including `public: false` pages) to `staging/` and serves it with HTTP Basic Auth (hardwired password: `xyzzy`). Without `--private`, the staging server continues to serve public-only content with no auth. The SiteGenerator gains an `include_private` option that uses `load()` instead of `load_public()`.
