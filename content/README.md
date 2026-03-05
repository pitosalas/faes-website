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
