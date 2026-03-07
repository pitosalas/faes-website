#!/usr/bin/env python3
# test_f13_grantee.py — Tests for F13 grantee logo and URL in grant cards
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent

CSV_WITH_LOGO_URL = """\
recipient,times_awarded,status,grant_type,public,description,logo,url
Org Name,1,awarded,pilot,true,A description.,org-logo.png,https://example.org
"""

CSV_NO_LOGO_URL = """\
recipient,times_awarded,status,grant_type,public,description,logo,url
Org Name,1,awarded,pilot,true,A description.,,
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
    html = make_grants_page(tmp_path, CSV_WITH_LOGO_URL)
    assert 'href="https://example.org"' in html


def test_url_link_opens_new_tab(tmp_path):
    html = make_grants_page(tmp_path, CSV_WITH_LOGO_URL)
    assert 'target="_blank"' in html


def test_no_url_keeps_title_plain(tmp_path):
    html = make_grants_page(tmp_path, CSV_NO_LOGO_URL)
    assert "example.org" not in html


def test_logo_renders_img(tmp_path):
    html = make_grants_page(tmp_path, CSV_WITH_LOGO_URL)
    assert "org-logo.png" in html
    assert "<img" in html


def test_logo_uses_static_logos_path(tmp_path):
    html = make_grants_page(tmp_path, CSV_WITH_LOGO_URL)
    assert 'src="static/logos/org-logo.png"' in html


def test_no_logo_omits_img(tmp_path):
    html = make_grants_page(tmp_path, CSV_NO_LOGO_URL)
    assert "static/logos" not in html


def test_static_logos_dir_exists():
    assert (ROOT / "static" / "logos").is_dir()
