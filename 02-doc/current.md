# Current Session Status

## Last completed
- F22 — Admin page charity totals by year section (145 tests pass)
- Migrated repo to j3 standard process structure (03-features/, 04-tasks/, etc.)
- Full code review completed; 3 MUST violations recorded as issues in 05-issues/

## In progress
Nothing currently in progress.

## Open issues from code review
- I01: Leading underscore naming convention — project-wide MUST conflict;
  needs waiver decision or rename feature
- I02: Module-level Jinja2 `env` in content_loader.py — side effect at import time
- I03: Silent image fallback in content_loader.py — should raise, not substitute

## Other review findings (SHOULD / minor)
- Several lines over 88 chars in site_generator.py, staging_server.py,
  content_loader.py, csv_loader.py — mostly long render calls and regex strings
- `staging_server.py`: hardcoded `PASSWORD = "xyzzy"` (low-risk — staging only,
  but technically a MUST violation)
- `staging_server.py`: uses `os.chdir()` — changes global process state
- Imports in content_loader.py not sorted (stdlib before third-party)

## Next
Decide what to do with I01 (waive or fix). I02 and I03 are straightforward
fixes that can each be a small feature.
