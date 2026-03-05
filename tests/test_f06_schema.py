#!/usr/bin/env python3
# test_f06_schema.py — Tests for F06 content schema amendments
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from pathlib import Path
from faes_website.content_loader import ContentLoader

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

VALID_PAGE = """\
---
title: Test Page
date: 2024-01-01
type: page
slug: test
public: true
---

Content here.
"""

VALID_GRANT = """\
---
title: Test Grant
date: 2024-01-01
type: grant
recipient: Jane Doe
amount: "XCG 3,000"
year: 2024
status: awarded
grant_type: pilot
public: true
---

Grant description.
"""


def make_md(tmp_path, filename, text):
    p = tmp_path / filename
    p.write_text(text, encoding="utf-8")
    return tmp_path


def test_missing_public_raises(tmp_path):
    make_md(tmp_path, "nopublic.md", """\
---
title: No Public
date: 2024-01-01
type: page
slug: test
---

Missing public field.
""")
    with pytest.raises(KeyError, match="public"):
        ContentLoader().load(tmp_path)


def test_missing_grant_type_raises(tmp_path):
    make_md(tmp_path, "nogranttype.md", """\
---
title: Test Grant
date: 2024-01-01
type: grant
recipient: Jane Doe
amount: "XCG 3,000"
year: 2024
status: awarded
public: true
---

Missing grant_type.
""")
    with pytest.raises(KeyError, match="grant_type"):
        ContentLoader().load(tmp_path)


def test_invalid_grant_type_raises(tmp_path):
    make_md(tmp_path, "badgranttype.md", """\
---
title: Test Grant
date: 2024-01-01
type: grant
recipient: Jane Doe
amount: "XCG 3,000"
year: 2024
status: awarded
grant_type: invalid
public: true
---

Bad grant_type value.
""")
    with pytest.raises(ValueError, match="grant_type"):
        ContentLoader().load(tmp_path)


def test_load_public_excludes_private(tmp_path):
    make_md(tmp_path, "public.md", VALID_PAGE)
    make_md(tmp_path, "private.md", VALID_PAGE.replace("public: true", "public: false"))
    items = ContentLoader().load_public(tmp_path)
    assert len(items) == 1
    assert items[0]["public"] is True


def test_load_public_includes_public(tmp_path):
    make_md(tmp_path, "a.md", VALID_PAGE)
    make_md(tmp_path, "b.md", VALID_GRANT)
    items = ContentLoader().load_public(tmp_path)
    assert len(items) == 2


def test_valid_grant_loads(tmp_path):
    make_md(tmp_path, "grant.md", VALID_GRANT)
    items = ContentLoader().load(tmp_path)
    assert items[0]["grant_type"] == "pilot"


def test_all_seed_content_loads():
    items = ContentLoader().load(CONTENT)
    assert len(items) > 0
    for item in items:
        assert "public" in item


def test_seed_public_items_filterable():
    items = ContentLoader().load_public(CONTENT)
    assert all(item["public"] is True for item in items)
    assert len(items) > 0
