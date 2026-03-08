#!/usr/bin/env python3
# test_f02_content.py — tests for F02 content authoring and ContentLoader
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from pathlib import Path
from faes_website.content_loader import ContentLoader

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def fixture_dir(tmp_path):
    return tmp_path


def make_md(tmp_path, filename, text):
    p = tmp_path / filename
    p.write_text(text, encoding="utf-8")
    return tmp_path


def test_front_matter_parsed(tmp_path):
    make_md(tmp_path, "test.md", """\
---
title: Test Page
date: 2024-01-01
type: page
slug: test
public: true
---

Hello world.
""")
    items = ContentLoader().load(tmp_path)
    assert len(items) == 1
    assert items[0]["title"] == "Test Page"
    assert items[0]["type"] == "page"
    assert items[0]["slug"] == "test"


def test_markdown_body_converted_to_html(tmp_path):
    make_md(tmp_path, "test.md", """\
---
title: Test
date: 2024-01-01
type: page
slug: test
public: true
---

# Heading One
""")
    items = ContentLoader().load(tmp_path)
    assert "<h1>" in items[0]["body_html"]


def test_missing_title_raises(tmp_path):
    make_md(tmp_path, "bad.md", """\
---
date: 2024-01-01
type: page
public: true
---

No title here.
""")
    with pytest.raises(KeyError, match="title"):
        ContentLoader().load(tmp_path)


def test_all_seed_content_loads():
    items = ContentLoader().load(CONTENT)
    assert len(items) > 0
    for item in items:
        assert "title" in item
        assert "type" in item
        # CSV grants don't have body_html (simplified format)
        if item["type"] != "grant":
            assert "body_html" in item
