# Feature description for feature F13
## F13 — Grantee logo and URL in grant cards
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Add optional `logo` (filename, stored in static/logos/) and `url` (full URL) fields to the grant schema. Both fields are optional. When `logo` is present, an img tag is rendered in the grant card. When `url` is present, the grant title becomes a link to the grantee's website. Logos are stored in `static/logos/`. The CSV loader passes these fields through unchanged.
