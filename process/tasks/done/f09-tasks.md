# F09 Tasks for Feature F09

## T01 — Create CsvLoader class
**Status**: done
**Description**: Create `faes_website/csv_loader.py` with a `CsvLoader` class. It reads `content/grants.csv` (if it exists) using Python's `csv.DictReader`. Converts each row into a grant dict matching the format produced by `ContentLoader`: adds `type: grant`, converts `public` string to bool, converts `year` to int, converts markdown description to HTML body. Returns a list of grant dicts.

## T02 — Integrate CsvLoader into ContentLoader
**Status**: done
**Description**: Update `faes_website/content_loader.py` to instantiate `CsvLoader` and merge its results with the existing markdown-sourced content. CSV grants and markdown grants are combined into a single list. Deduplication is not required (user is responsible for not duplicating entries across both sources).

## T03 — Add sample content/grants.csv
**Status**: done
**Description**: Create `content/grants.csv` with headers and at least two sample rows demonstrating the format. Use the same data style as the existing markdown grant file.

## T04 — Write tests
**Status**: done
**Description**: Create `tests/test_f09_csv.py` with tests covering: CSV file is parsed correctly into grant dicts, `public` field is converted to bool, `year` is converted to int, CSV grants appear in generator output, missing optional CSV file is handled gracefully (no error), CSV and markdown grants are both included when both exist.
