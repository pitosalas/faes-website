# Content Authoring Guide

All content files are markdown (`.md`) with YAML front matter.

## Front matter schema

### All content types
| Field  | Type   | Values          | Required |
|--------|--------|-----------------|----------|
| title  | str    | any             | yes      |
| date   | str    | YYYY-MM-DD      | yes      |
| type   | str    | page \| grant   | yes      |
| public | bool   | true \| false   | yes      |

### Pages (type: page)
| Field  | Type   | Description              | Required |
|--------|--------|--------------------------|----------|
| slug   | str    | URL path segment         | yes      |

### Grants (type: grant)
| Field      | Type   | Values              | Required |
|------------|--------|---------------------|----------|
| recipient  | str    | name of recipient   | yes      |
| amount     | str    | e.g. "XCG 3,000"   | yes      |
| year       | int    | e.g. 2024           | yes      |
| status     | str    | awarded \| pending  | yes      |
| grant_type | str    | pilot \| primary    | yes      |

**Note:** Grants are now sourced from `grants.csv` with columns: `name`, `total`, `count`, `recent`, and optional `logo`.

## Example page

```markdown
---
title: About Us
date: 2024-01-01
type: page
slug: about
---

Content here in markdown.
```

## Example grant

```markdown
---
title: 2024 Community Support Grant
date: 2024-03-15
type: grant
recipient: Jane Doe
amount: "XCG 3,000"
year: 2024
status: awarded
grant_type: pilot
---

Description of the grant and its impact.
```

## Inline photos in markdown

Use the photo shortcode on its own line:

```markdown
:photo "children-reading.jpg", "Students reading at the community center", 320, centered
```

Rules:
- The filename is relative to `static/images/`.
- Use double quotes around both filename and caption.
- `pixel-height` must be an integer greater than 0.
- `justify` must be one of: `left`, `right`, `centered`.
- Keep the shortcode on its own line in markdown.
- Whitespace around the comma is allowed.

Common errors:
- Bad syntax (missing quote/comma): raises a parsing error with file and line number.
- Invalid `pixel-height` or `justify`: raises a parsing error with file and line number.
- Missing image file: uses `placeholder-image.jpg` as a fallback (no error).
