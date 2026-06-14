# Project Notes

## Architecture decisions

- `content/` is a symlink to `../faes-content` (a separate private git repo containing grant data, CSVs, static assets). Files inside cannot be staged through the symlink in this repo.
- Static site is generated to `site/` (production) or `staging/` (local preview); both gitignored.
- The admin page (`admin.html`) is private-only and requires HTTP Basic Auth in staging mode.
- Grant data lives in `grantsdetailed.csv` inside the content repo.
- Per-org metadata lives in `content/orgs/<name>/org.md`.

## Gotchas

- Do not try to `git add content/static/...` — git rejects paths through symlinks. Commit those changes in the `faes-content` repo directly.
- The `Unknown` org always has `public: false` in its org.md.
- The org validator runs before any HTML is written and exits non-zero if orgs dir and CSV recipients don't match exactly.
