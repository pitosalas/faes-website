# Tasks for Feature F22 — Admin page: charity totals for selected year-to-date

## T01 — Add charity-totals div to admin_page.html
**Status**: done
**Description**: Add a `<div id="charity-totals-section">` with a heading and
an inner `<div id="charity-totals-grid">` below the existing `#org-year-grid`
div in `templates/html/admin_page.html`.

## T02 — Implement buildCharityTotals() in admin.js
**Status**: done
**Description**: Add a `buildCharityTotals(selectedYear)` function to
`content/static/admin.js`. It filters `ALL_ROWS` to dates from Jan 1 of
`selectedYear` through today (or all rows when `selectedYear === "all"`),
aggregates by nonprofit, drops zero-total charities, sorts by total descending,
and renders a gridjs.Grid into `#charity-totals-grid`. Wire it into the existing
`select` change listener and call it once on page load.

## T03 — Write tests
**Status**: done
**Description**: Add a test in `tests/test_f22_admin_charity_totals.py` that
runs a full site generation and asserts the rendered `admin.html` contains
the `charity-totals-grid` div id.
