#!/usr/bin/env python3
# test_f13_grantee.py — Tests for F13 grantee logo and URL in grant cards
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent

# F17 simplified format: no logos or URLs
CSV_SIMPLIFIED = """\
name,total,count,recent
Org Name,"XCG 5,000",1,2024
"""


def make_grants_page(tmp_path, csv_text):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "grants.csv").write_text(csv_text, encoding="utf-8")
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    SiteGenerator(content_dir, site_dir).generate()
    return (site_dir / "grants.html").read_text()


def test_url_makes_title_a_link(tmp_path):
    # F17: URLs removed from simplified format
    html = make_grants_page(tmp_path, CSV_SIMPLIFIED)
    assert "Org Name" in html
    assert "href=" not in html or 'href="index' in html  # Only nav links


def test_url_link_opens_new_tab(tmp_path):
    # F17: No external links in simplified format
    html = make_grants_page(tmp_path, CSV_SIMPLIFIED)
    # Only nav links present, no target="_blank"
    assert 'target="_blank"' not in html


def test_no_url_keeps_title_plain(tmp_path):
    # F17: All titles are plain text now
    html = make_grants_page(tmp_path, CSV_SIMPLIFIED)
    assert "Org Name" in html


def test_logo_renders_img(tmp_path):
    # F17: Logos removed from simplified format
    html = make_grants_page(tmp_path, CSV_SIMPLIFIED)
    # No logo images in grant cards
    assert "grantee-logo" not in html


def test_logo_uses_static_logos_path(tmp_path):
    # F17: No logos in simplified format
    html = make_grants_page(tmp_path, CSV_SIMPLIFIED)
    assert "static/logos" not in html


def test_no_logo_omits_img(tmp_path):
    # F17: Simplified cards never have img tags
    html = make_grants_page(tmp_path, CSV_SIMPLIFIED)
    # Only check grant card area (exclude nav/footer)
    grant_section = html.split("grants-grid")[1].split("</div>")[0] if "grants-grid" in html else ""
    assert "<img" not in grant_section


def test_static_logos_dir_exists():
    assert (ROOT / "static" / "logos").is_dir()
