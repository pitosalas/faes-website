# F17 Tasks for Feature F17

## T01 — Update csv_loader.py for new CSV format
**Status**: done
**Description**: Modify `CsvLoader` class to read CSV with columns: name, total, count, recent. Convert row to dict with: title (name), count (int), most_recent_year (int), type="grant", public=true. Remove validation for old fields like grant_type, description, logo, url.

## T02 — Update site_generator.py to load grants from CSV
**Status**: done
**Description**: In `SiteGenerator.generate()`, use `CsvLoader` to load grants from `content/grants.csv` instead of using ContentLoader for grant content files. Pass loaded grants to _write_grants().

## T03 — Simplify _grant_card to show recipient name only
**Status**: done
**Description**: In `site_generator.py`, update `_grant_card()` method to render simplified cards with just recipient name. Remove count, year, logo, grant_type, and description/body_html elements.

## T04 — Update grants page header
**Status**: done
**Description**: Update `_write_grants()` method to adjust header text to describe the simplified grants listing.

## T05 — Write tests
**Status**: done
**Description**: Create `tests/test_f17_csv_grants.py` covering: CSV loader reads new format correctly, generates correct number of grant cards, cards contain recipient name, invalid CSV data raises errors, grants sorted by count. Update existing tests in F02, F03, F04, F08, F09, F13 to work with new format.
