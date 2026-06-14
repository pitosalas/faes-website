# Feature description for feature F22
## F22 — Admin page: charity totals for selected year-to-date
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Add a new section to `admin.html` that shows the total amount
granted to each charity from January 1 of the year selected in the existing
year dropdown up through today's date. Only charities that received at least
one grant in that date range are shown. The section reacts to the same
`#year-select` dropdown that already drives the grants grid.

## Behaviour

- The section heading and table appear below the existing `#org-year-grid`.
- When the page loads, the table is populated for the most-recently-selected
  year (the dropdown's initial value, which is the latest year).
- When the user changes the year dropdown, the table updates immediately
  (no page reload).
- The date range is: `YYYY-01-01` to today's date (inclusive), where `YYYY`
  is the year currently selected in the dropdown.
- If the dropdown is set to "all years", use all rows regardless of date.
- Rows with a date before Jan 1 of the selected year, or after today, are
  excluded.
- Only charities with a positive total in the filtered range are listed.
- The table is sorted by total descending.
- Amounts are displayed in the existing `formatAmount` style (e.g. `XCG 5,000`).
- A grand-total row appears at the bottom of the table.

## Data available in the browser

All grant rows are already passed to the page as `window.SECRET_ROWS`.
Each row has:
- `date`      — ISO-8601 string `"YYYY-MM-DD"` (or partial `"YYYY"` fallback)
- `nonprofit` — string name of the charity
- `amount`    — numeric (float)
- `year`      — integer year

The filtering and aggregation are done entirely in client-side JavaScript —
no changes to the Python generator are needed for the core feature.

## Implementation sketch

1. **`admin_page.html`** — add a `<div id="charity-totals-section">` after the
   `#org-year-grid` div. Include a heading and an empty `<div id="charity-totals-grid">`.
2. **`admin.js`** — add a function `buildCharityTotals(selectedYear)` that:
   - Computes `rangeStart = selectedYear + "-01-01"` and `rangeEnd = today`.
   - Filters `ALL_ROWS` to rows whose `date >= rangeStart` and `date <= rangeEnd`
     (or all rows when `selectedYear === "all"`).
   - Aggregates totals per nonprofit.
   - Drops charities with zero total.
   - Sorts by total descending.
   - Renders a `gridjs.Grid` into `#charity-totals-grid`.
3. Hook `buildCharityTotals` into the existing `select` `change` event listener
   so it re-renders whenever the year changes.
4. Call `buildCharityTotals` once on page load with the initial year.

## Files changed

| File | Change |
|------|--------|
| `templates/html/admin_page.html` | Add `#charity-totals-section` div |
| `content/static/admin.js` | Add `buildCharityTotals()` function and wire up |

No Python changes needed.

## Tests

- Unit tests for the year-range filtering logic are not straightforward to
  write for client-side JS in the current pytest suite. Instead, add a Python
  generator test that verifies the admin page HTML contains the new section
  div id (`charity-totals-grid`).
