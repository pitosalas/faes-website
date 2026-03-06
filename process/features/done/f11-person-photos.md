# Feature description for feature F11
## F11 — Board member photos
**Priority**: Low
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Add an optional `photo` field to the `person` content type front matter. When present, the value is a filename (e.g. `pito-salas.jpg`) relative to `static/photos/`. The `_person_card` renderer in `SiteGenerator` renders an `<img>` tag when the field is present and omits it when absent. Photos are stored in `static/photos/`. The field is optional so existing person files without a photo continue to work unchanged.
