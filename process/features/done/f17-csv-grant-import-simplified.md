# Feature description for feature F17
## F17 — CSV Grant Import with Simplified Cards
**Priority**: High
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Replace the current grant content loading system with CSV-based import. Read from `content/grants.csv` with columns: name, total, count, recent. Simplify grant cards to display only recipient name. Remove grant descriptions, logos, grant types, counts, and years from display. Update csv_loader.py to handle the new CSV schema and site_generator.py to build the grants page from CSV data.
