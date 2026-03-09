# Content Authoring Guide

All content files are markdown (`.md`) with YAML front matter.

## Directory layout

```
content/
  pages/          — page markdown files
  people/         — person markdown files
  grants.csv      — grant recipients (name, total, count, recent, logo)
  grantsdetailed.csv — per-year grant amounts (Year, Recipient, Amount)
  static/
    style.css     — site stylesheet
    images/       — photos used in page content via :photo shortcode
    logos/        — grantee logo images
    photos/       — board/advisor portrait photos
```

## Front matter schema

### All content types
| Field  | Type   | Values          | Required |
|--------|--------|-----------------|----------|
| title  | str    | any             | yes      |
| date   | str    | YYYY-MM-DD      | yes      |
| type   | str    | page \| person  | yes      |
| public | bool   | true \| false   | yes      |

### Pages (type: page)
| Field  | Type   | Description              | Required |
|--------|--------|--------------------------|----------|
| slug   | str    | URL path segment         | yes      |
| lang   | str    | en \| pap (default: en)  | no       |

### People (type: person)
| Field  | Type   | Values              | Required |
|--------|--------|---------------------|----------|
| role   | str    | board \| advisor    | yes      |
| photo  | str    | filename in static/photos/ | no  |
| lang   | str    | en \| pap (default: en)    | no  |

## Example page

```markdown
---
title: About Us
date: 2024-01-01
type: page
slug: about
public: true
---

Content here in markdown.
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
