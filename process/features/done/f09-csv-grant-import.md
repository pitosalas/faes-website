# Feature description for feature F09
## F09 — CSV grant import
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Allow grants to be defined in a CSV file (`content/grants.csv`) in addition to individual markdown files. Each CSV row represents one grant. Columns match the existing grant front matter fields: `title`, `date`, `recipient`, `amount`, `year`, `status`, `grant_type`, `public`, `description`. The `description` column holds plain text (may contain single-line markdown). The `ContentLoader` merges CSV-sourced grants with any existing markdown grant files. A sample `content/grants.csv` is provided. The feature makes it easy to maintain a list of grants in a spreadsheet and export to CSV.
