# F14 Tasks for Feature F14

## T01 — Create default-person.svg placeholder
**Status**: done
**Description**: Create `static/photos/default-person.svg` — a simple person silhouette using the site's muted color palette (#e4e0d8 background, #b0a898 figure).

## T02 — Update _person_card to always render photo
**Status**: done
**Description**: In `site_generator.py`, update `_person_card` to always render an img tag, defaulting to `default-person.svg` when no photo field is set.

## T03 — Add person card CSS
**Status**: done
**Description**: Add `.people-grid`, `.person-card`, `.person-photo`, and `.person-bio` rules to `static/style.css`. Cards have white background, border, rounded corners. Photo fills the card top (square, object-fit cover). Name centered, bio left-aligned below.

## T04 — Write tests
**Status**: done
**Description**: Create `tests/test_f14_board_design.py` covering: person card always contains img tag, card with no photo uses default-person.svg, card with photo uses specified filename, default SVG file exists.
