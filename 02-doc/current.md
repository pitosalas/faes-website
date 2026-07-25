# Current Session Status

## Last completed
- F22 — Admin page charity totals by year section (145 tests pass)
- Migrated repo to j3 standard process structure (03-features/, 04-tasks/, etc.)
- Full code review completed; 3 MUST violations recorded as issues in 05-issues/
- `.claude/` replaced from `../dome_nav` template; `codereview.md`/`how_to_be.md`
  → `style_guide.md`; CLAUDE.md refs and folder-scheme description updated to
  match (05-issues/{open,closed,deferred}, 04-tasks/chores.md)
- Architecture/design/bug review of `faes_website/` performed; found admin.html
  publishes full transaction data as plaintext JSON on every public build
  (not gated by `include_private`), protected only by cosmetic client-side
  CSS-hiding + SHA-256 compare — real exposure on the live GitHub Pages deploy
- F23 filed: encrypt admin transaction data (AES-256-GCM, key from admin
  password, decrypt client-side via SubtleCrypto) so admin.html can stay on
  the public build with no plaintext data at rest. TF23 written, 9 tasks,
  none started — no code written yet, awaiting go-ahead

## In progress
Nothing currently in progress. F23/TF23 filed but not started.

## Open issues from code review
- I01: Leading underscore naming convention — project-wide MUST conflict;
  needs waiver decision or rename feature (now in `05-issues/open/`)
- I02: Module-level Jinja2 `env` in content_loader.py — side effect at import time
- I03: Silent image fallback in content_loader.py — should raise, not substitute

## Other review findings (SHOULD / minor)
- Several lines over 88 chars in site_generator.py, staging_server.py,
  content_loader.py, csv_loader.py — mostly long render calls and regex strings
- `staging_server.py`: hardcoded `PASSWORD = "xyzzy"` (MUST violation — no
  secrets in code); F23/TF23 T07 folds this in: source password from
  `config.yml` `staging.password` in one place instead
- `staging_server.py`: uses `os.chdir()` — changes global process state
- Imports in content_loader.py not sorted (stdlib before third-party)

## Next
1. Get go-ahead to start F23 (encrypt admin data) — T01 adds `cryptography`
   dependency, then proceed T02–T09 in order per TF23.
2. Decide what to do with I01 (waive or fix).
3. I02 and I03 are straightforward fixes, each a small feature.
