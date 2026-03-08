# Feature description for feature F17
## F17 — CSV Grant Import with Simplified Cards
**Priority**: High
**Done:** no
**Tests Written:** no
**Test Passing:** no
**Description**: Replace the current grant content loading system with CSV-based import. Read from `content/grants.csv` with columns: Recipient, total, count, most_recent_year. Simplify grant cards to display only: recipient name (as clickable link if URL exists), count (number of times awarded), and most recent year. Remove grant descriptions, logos, and grant types from display. Update csv_loader.py to handle the new CSV schema and site_generator.py to build the grants page from CSV data.
