#!/usr/bin/env python3
# test_f03_generator.py — Tests for F03 static site generator
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
import pytest
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

VALID_PAGE = """\
---
title: Test Page
date: 2024-01-01
type: page
slug: testpage
public: true
---

# Test Heading

Some content here.
"""

PRIVATE_PAGE = """\
---
title: Private Page
date: 2024-01-01
type: page
slug: privatepage
public: false
---

Secret content.
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

Grant description here.
"""


def make_md(path: Path, filename: str, text: str):
    p = path / filename
    p.write_text(text, encoding="utf-8")


def test_generate_produces_page_files(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", VALID_PAGE)
    SiteGenerator(content, site).generate()
    assert (site / "testpage.html").exists()


def test_private_content_not_written(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "private.md", PRIVATE_PAGE)
    SiteGenerator(content, site).generate()
    assert not (site / "privatepage.html").exists()


def test_generate_produces_grants_html(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    # Create CSV file with grant data
    csv_file = content / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Grant","XCG 3,000",1,2024\n'
    )
    SiteGenerator(content, site).generate()
    assert (site / "grants.html").exists()


def test_grants_html_contains_card(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    # Create CSV file with grant data
    csv_file = content / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Grant","XCG 3,000",5,2024\n'
    )
    SiteGenerator(content, site).generate()
    html = (site / "grants.html").read_text()
    assert "grant-card" in html
    assert "Test Grant" in html


def test_page_contains_title(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", VALID_PAGE)
    SiteGenerator(content, site).generate()
    html = (site / "testpage.html").read_text()
    assert "Test Page" in html


def test_page_contains_body_html(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", VALID_PAGE)
    SiteGenerator(content, site).generate()
    html = (site / "testpage.html").read_text()
    assert "<h1>" in html
    assert "Some content here" in html


def test_generate_returns_written_filenames(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", VALID_PAGE)
    make_md(content, "grant.md", VALID_GRANT)
    written = SiteGenerator(content, site).generate()
    assert "testpage.html" in written
    assert "grants.html" in written


def test_generate_real_content():
    site = ROOT / "site"
    written = SiteGenerator(CONTENT, site).generate()
    assert "index.html" in written
    assert "about.html" in written
    assert "mission.html" in written
    assert "grants.html" in written
    assert "history.html" not in written
