# I01 — Leading-underscore naming used throughout (codereview MUST violation)

## Symptom
codereview.md MUST: "No leading underscore prefix on methods, functions,
instance variables, or other custom identifiers."

This convention is violated everywhere in the codebase:

- `__main__.py`: `_resolve_csv`
- `csv_loader.py`: `_parse_date`, `_format_total`, `_parse_amount`
- `org_loader.py`: `_orgs_dir`, `_parse`, `_detect_logo`, `_write_logo`, `_validate`
- `site_generator.py`: `_lang`, `_translation_url`, `_admin_hash`, `_env`,
  and all private render/write methods
- `staging_server.py`: `_authorized`

## Tests done
None — this is a naming/style issue, not a runtime bug.

## Latest theory
The underscore convention was established early (F01) and carried through
all 22 features. It conflicts with the j3 codereview standard adopted in
the recent process migration.

**Decision needed:** either waive this rule for this repo (document in
CLAUDE.md) or create a feature to rename all affected identifiers.
If waived, add an explicit note so future code doesn't continue the pattern
by accident.
