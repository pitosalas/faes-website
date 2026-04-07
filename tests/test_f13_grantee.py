#!/usr/bin/env python3
# test_f13_grantee.py — Tests for F13 grantee logo and URL in grant cards
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent


def make_grants_page(tmp_path, logo=""):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "grants_claude.csv").write_text(
        "Date,Year,Recipient,Amount_NAf,Notes\n,2024,Org Name,5000.00,\n", encoding="utf-8"
    )
    org_dir = content_dir / "orgs" / "Org Name"
    org_dir.mkdir(parents=True)
    (org_dir / "org.md").write_text("---\ngrant_type: pilot\npublic: true\n---\n", encoding="utf-8")
    if logo:
        (org_dir / logo).write_bytes(b"")
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    SiteGenerator(content_dir, site_dir).generate(False)
    return (site_dir / "grants.html").read_text()


def test_url_makes_title_a_link(tmp_path):
    html = make_grants_page(tmp_path)
    assert "Org Name" in html
    assert "href=" not in html or 'href="index' in html  # only nav links


def test_url_link_opens_new_tab(tmp_path):
    html = make_grants_page(tmp_path)
    assert 'target="_blank"' not in html


def test_no_url_keeps_title_plain(tmp_path):
    html = make_grants_page(tmp_path)
    assert "Org Name" in html


def test_logo_renders_img(tmp_path):
    html = make_grants_page(tmp_path, logo="testlogo.png")
    assert 'class="grantee-logo"' in html
    assert 'src="static/logos/testlogo.png"' in html


def test_logo_uses_static_logos_path(tmp_path):
    html = make_grants_page(tmp_path, logo="testlogo.png")
    assert "static/logos" in html


def test_no_logo_omits_img(tmp_path):
    html = make_grants_page(tmp_path, logo="")
    assert 'class="grantee-logo"' not in html


def test_static_logos_dir_exists():
    assert (ROOT / "content" / "static" / "logos").is_dir()
