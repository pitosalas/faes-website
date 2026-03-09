#!/usr/bin/env python3
# test_f12_topbar.py — Tests for F12 blue topbar
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator

FOUNDATION_NAME = "Fundashon Abram Edgardo Salas"


def make_site(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    SiteGenerator(content_dir, site_dir).generate(False)
    return site_dir


def test_topbar_present_in_grants_page(tmp_path):
    site_dir = make_site(tmp_path)
    html = (site_dir / "grants.html").read_text()
    assert "site-topbar" in html


def test_topbar_contains_foundation_name(tmp_path):
    site_dir = make_site(tmp_path)
    html = (site_dir / "grants.html").read_text()
    assert FOUNDATION_NAME in html


def test_topbar_present_in_board_page(tmp_path):
    site_dir = make_site(tmp_path)
    html = (site_dir / "board.html").read_text()
    assert "site-topbar" in html


def test_topbar_inside_hero(tmp_path):
    site_dir = make_site(tmp_path)
    html = (site_dir / "grants.html").read_text()
    assert "site-hero" in html
    assert html.index("site-banner") < html.index("site-topbar")


def test_topbar_css_exists():
    css = (Path(__file__).parent.parent / "content" / "static" / "style.css").read_text()
    assert ".site-topbar" in css
    assert ".site-topbar" in css
