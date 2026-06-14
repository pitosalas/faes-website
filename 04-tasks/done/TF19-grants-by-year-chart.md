# Tasks for Feature F19 — Grants by year bar chart

## T01 — Add grantsdetailed.csv content file
**Status**: done
**Description**: Create `content/grantsdetailed.csv` with columns `Year`, `Recipient`, `Amount`. Amounts use XCG currency prefix and comma-formatted thousands (e.g. `XCG 5,000.`). File covers grants from 2008–2025 with a grand-total row at the bottom.

## T02 — Add load_by_year method to CsvLoader
**Status**: done
**Description**: Add `load_by_year(csv_path)` to `CsvLoader` that reads `grantsdetailed.csv`, parses each `Amount` via a helper `_parse_amount()`, and returns a `{year: total}` dict sorted by year. Skip rows with no valid year. Handle the `XCG `, `$`, comma, and trailing-period formatting variants.

## T03 — Wire detailed CSV loading into site generator
**Status**: done
**Description**: In `SiteGenerator.generate()`, load `grantsdetailed.csv` via `csv_loader.load_by_year()` and pass the resulting dict to `_write_grants()`.

## T04 — Render Chart.js bar chart in grants page
**Status**: done
**Description**: Add `_year_chart(by_year)` to `SiteGenerator` that returns an HTML snippet with a `<canvas>` element and an inline `<script>` block that initialises a Chart.js bar chart with the year labels and totals. Chart is inserted above the grant cards grid in `_write_grants()`.

## T05 — Add chart CSS to stylesheet
**Status**: done
**Description**: Add `.chart-section`, `.chart-section h2`, and `.chart-wrapper` rules to `static/style.css` so the chart renders in a card matching the site design, with a fixed height of 320px and `position: relative` for Chart.js responsive sizing.

## T06 — Write tests for F19
**Status**: done
**Description**: Add `tests/test_f19_grants_chart.py` covering: `load_by_year` summing, zero amounts, sorted output, missing file, `_parse_amount` for XCG/dollar/empty formats, skipping non-year rows, real CSV loads, chart HTML in generated page, and chart title.
