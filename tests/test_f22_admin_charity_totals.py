#!/usr/bin/env python3
# test_f22_admin_charity_totals.py — Tests for F22 charity totals section on admin page
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator


def test_charity_totals_section_present_in_admin_page(tmp_path):
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(tmp_path / "content", site_dir)
    gen._write_admin({2024: 5000.0}, [])
    html = (site_dir / "admin.html").read_text()
    assert "charity-totals-grid" in html


def test_charity_totals_heading_present(tmp_path):
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(tmp_path / "content", site_dir)
    gen._write_admin({2024: 1000.0}, [])
    html = (site_dir / "admin.html").read_text()
    assert "charity-totals-section" in html
