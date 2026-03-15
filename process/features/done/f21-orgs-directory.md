# Feature description for feature F21
## F21 — Org directories replace grants.csv
**Priority**: High
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Replace `content/grants.csv` as the source of per-org metadata with a new `content/orgs/` directory structure. Each organisation that appears in `grantsdetailed.csv` (Recipient column) gets a subdirectory under `content/orgs/` whose name is exactly the Recipient string. Each subdirectory contains one file, `org.md`, with YAML front matter holding the org's metadata. Summary data (total amount, grant count, most recent year) continues to be derived from `grantsdetailed.csv`. `grants.csv` is ignored by the code going forward.

## content/orgs/ layout

```
content/orgs/
  Mikve Israel Emanuel/
    org.md
  Citro/
    org.md
  ...one directory per unique Recipient in grantsdetailed.csv...
```

## org.md front matter schema

| Field        | Required | Values / notes                        |
|-------------|----------|---------------------------------------|
| `grant_type` | yes      | `pilot` or `primary`                  |
| `public`     | yes      | `true` or `false`                     |
| `logo`       | no       | filename only, stored in `static/logos/` |
| `url`        | no       | full URL to grantee website           |

Markdown body is optional (reserved for future description use).

The `Unknown` recipient is included as a directory with `public: false`.

## Validation rule

At site-generation start, before any HTML is written, the generator must compare:
- Set A: unique Recipient values in `grantsdetailed.csv` (excluding blank/header rows and grand-total rows)
- Set B: subdirectory names under `content/orgs/`

If A ≠ B, print a clear error listing extras and missing entries on each side, then exit with a non-zero status. The site is not generated.

## Summary data derivation

For each org, compute from `grantsdetailed.csv`:
- **total**: sum of all Amount values (same parsing logic as F19)
- **count**: number of rows
- **recent**: maximum Year value

These replace the `total`, `count`, and `recent` columns previously read from `grants.csv`.

## What is removed / changed

- `csv_loader.py` no longer reads `grants.csv`
- `content/grants.csv` remains on disk but is not read
- All downstream code that consumed `grants.csv` columns (`total`, `count`, `recent`, `logo`) is updated to use org directory data + derived grantsdetailed values
