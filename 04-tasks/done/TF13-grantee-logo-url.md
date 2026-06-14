# F13 Tasks for Feature F13

## T01 — Update csv_loader to pass through logo and url fields
**Status**: done
**Description**: In `csv_loader.py _convert`, add `logo` and `url` from the row dict (both optional, default to empty string).

## T02 — Update _grant_card to render logo and url
**Status**: done
**Description**: In `site_generator.py`, update `_grant_card`: if `url` present, wrap title in `<a href="{url}">`. If `logo` present, render `<img src="static/logos/{logo}" alt="{recipient}" class="grantee-logo">` in the card header.

## T03 — Create static/logos/ directory
**Status**: done
**Description**: Create `static/logos/` with a `.gitkeep` so the directory is tracked. Grantee logos dropped here are automatically served.

## T04 — Add logo and url columns to grants.csv
**Status**: done
**Description**: Add `logo` and `url` header columns to `content/grants.csv`. Leave values empty for existing rows to demonstrate optional nature.

## T05 — Write tests
**Status**: done
**Description**: Create `tests/test_f13_grantee.py` covering: url present makes title a link, url absent keeps title plain, logo present renders img tag with static/logos/ path, logo absent omits img, both fields empty leaves card unchanged.
