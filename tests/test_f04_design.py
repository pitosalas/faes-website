#!/usr/bin/env python3
# test_f04_design.py — Tests for F04 site design and layout
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path

SITE = Path(__file__).parent.parent / "site"
EXPECTED_PAGES = ["index.html", "about.html", "mission.html", "grants.html"]
REQUIRED_STRUCTURAL = ["<header", "<nav", "<footer", "<main"]
NAV_LINKS = ["index.html", "about.html", "mission.html", "grants.html"]


def test_css_exists():
    assert (SITE / "static" / "style.css").is_file()


def test_css_nonempty():
    assert (SITE / "static" / "style.css").stat().st_size > 0


def test_all_pages_exist():
    for page in EXPECTED_PAGES:
        assert (SITE / page).is_file(), f"Missing: {page}"


def test_pages_reference_stylesheet():
    for page in EXPECTED_PAGES:
        content = (SITE / page).read_text()
        assert "static/style.css" in content, f"{page} missing stylesheet link"


def test_pages_have_structural_elements():
    for page in EXPECTED_PAGES:
        content = (SITE / page).read_text()
        for element in REQUIRED_STRUCTURAL:
            assert element in content, f"{page} missing {element}"


def test_pages_have_nav_links():
    for page in EXPECTED_PAGES:
        content = (SITE / page).read_text()
        for link in NAV_LINKS:
            assert link in content, f"{page} missing nav link to {link}"


def test_grants_page_has_grant_card():
    content = (SITE / "grants.html").read_text()
    assert "grant-card" in content


def test_home_page_has_content():
    content = (SITE / "index.html").read_text()
    assert "Fundashon Abram Edgardo Salas" in content
