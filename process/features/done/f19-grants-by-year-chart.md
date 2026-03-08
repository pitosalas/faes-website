# Feature description for feature F19
## F19 — Grants by year bar chart
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Add a bar chart to the grants page that visualises total donation amounts by year, drawn from a new `content/grantsdetailed.csv` file. Each row in the detailed CSV has columns `Year`, `Recipient`, and `Amount` (formatted as `XCG 1,000.`). The site generator reads this file, sums amounts per year, and injects a Chart.js bar chart above the grant cards on `grants.html`. The chart uses green bars with XCG-formatted axis labels and tooltips.

## Data format
- `grantsdetailed.csv` columns: `Year`, `Recipient`, `Amount`
- Amount format: `XCG 1,000.` (prefix `XCG`, comma-separated thousands, optional trailing decimal point)
- Rows with no numeric amount (e.g. `XCG .`) are treated as zero and excluded from chart totals
- A trailing blank row and a grand-total row (no Year) are ignored

## Chart contract
- Rendered via Chart.js (CDN) as a `<canvas>` element
- Bar color: `rgba(74, 124, 89, ...)` matching site green palette
- Y-axis ticks and tooltips formatted as `XCG {n}` with locale commas
- No legend (self-explanatory)
- Responsive, constrained to 320px height
- Appears between the page intro and the grant cards grid
