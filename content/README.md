# Content Authoring Guide

All content files are markdown (`.md`) with YAML front matter.

## Directory layout

```
content/
  pages/          — page markdown files
  people/         — person markdown files
  orgs/           — one subdirectory per grantee org
    <Org Name>/
      org.md      — org metadata (grant_type, public, email, blurb, …)
      logo.jpg    — logo image (auto-detected, any .png/.jpg/.jpeg)
  all_bank_transactions.csv  — authoritative grants ledger (active)
  reconciled_double.csv      — legacy reconciled ledger
  static/
    style.css     — site stylesheet
    images/       — photos used in page content via :photo shortcode
    logos/        — grantee logo images
    photos/       — board/advisor portrait photos
```

> **Privacy note:** `orgs/*/org.md` files contain contact names and
> email addresses for org staff. This repo is public — do not add
> personal emails that should not be publicly indexed.

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
| Field  | Type   | Values                     | Required |
|--------|--------|----------------------------|----------|
| role   | str    | board \| advisor           | yes      |
| photo  | str    | filename in static/photos/ | no       |
| lang   | str    | en \| pap (default: en)    | no       |

### Orgs (orgs/<Name>/org.md)
| Field           | Type   | Values              | Required |
|-----------------|--------|---------------------|----------|
| grant_type      | str    | pilot \| primary    | yes      |
| public          | bool   | true \| false       | yes      |
| logo            | str    | image filename      | auto     |
| url             | str    | org website URL     | no       |
| blurb           | str    | short description   | no       |
| email           | str    | contact email       | no       |
| 2025_recipient  | bool   | true \| false       | no       |
| 2026_plan       | int    | planned grant amt   | no       |
| email_confirmed | bool   | true \| false       | no       |

Org names in `orgs/` must exactly match recipient names in
`all_bank_transactions.csv`. A mismatch fails the build.

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
