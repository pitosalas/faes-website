# Tasks for Feature F21 — Org directories replace grants.csv

## T01 — Create content/orgs/ directory with org.md files
**Status**: done
**Description**: Create `content/orgs/` and one subdirectory per unique Recipient in `grantsdetailed.csv` (43 orgs including `Unknown`). Each subdirectory gets an `org.md` with correct `grant_type`, `public`, and optionally `logo`/`url` front matter. Migrate logo filenames from existing `grants.csv`. Set `Unknown/org.md` to `public: false`; all others `public: true`.

## T02 — Add OrgLoader class
**Status**: done
**Description**: Create `faes_website/org_loader.py` with class `OrgLoader`. Constructor takes `content_dir` path. Method `load()` returns a dict mapping org name → org metadata dict (grant_type, public, logo, url). Reads each `content/orgs/<name>/org.md`, parses YAML front matter. No HTML generation here.

## T03 — Add 1-to-1 validation in OrgLoader
**Status**: done
**Description**: Add method `validate(recipients: set[str])` to `OrgLoader`. Compares the set of subdirectory names against the provided recipient set from `grantsdetailed.csv`. If they differ, prints a clear error showing extras and missing on each side, then raises `SystemExit(1)`. Called from site_generator before any page is written.

## T04 — Derive summary data from grantsdetailed.csv per org
**Status**: done
**Description**: In `csv_loader.py` (or a new helper), add `summarise_by_org(rows)` that takes the already-parsed grantsdetailed rows and returns a dict mapping org name → `{total, count, recent}`. Reuses the existing Amount parsing logic from F19. This replaces the `total`/`count`/`recent` columns from `grants.csv`.

## T05 — Update site_generator to use OrgLoader + derived summaries
**Status**: done
**Description**: In `site_generator.py`, replace the call that loads `grants.csv` with: (1) load orgs via `OrgLoader.load()`, (2) call `OrgLoader.validate(recipients)`, (3) call `summarise_by_org()`, (4) merge org metadata + summaries into the grant records passed to `_write_grants()`. Remove all references to `grants.csv` loading.

## T06 — Remove grants.csv reading from csv_loader
**Status**: done
**Description**: Delete or stub out the `grants.csv` reading path in `csv_loader.py`. The file remains on disk but is never read. Update any imports or callers that depended on the old grant list.

## T07 — Write tests
**Status**: done
**Description**: Add tests covering: (a) OrgLoader.load() parses org.md fields correctly; (b) validate() passes when sets match; (c) validate() raises SystemExit with informative message when sets differ (extra orgs, missing orgs); (d) summarise_by_org() computes correct total/count/recent; (e) full site generation smoke test uses orgs data and produces grant cards without reading grants.csv.
