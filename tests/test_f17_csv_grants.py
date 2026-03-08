#!/usr/bin/env python3
# test_f17_csv_grants.py — tests for F17 CSV Grant Import with Simplified Cards
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from pathlib import Path
from faes_website.csv_loader import CsvLoader
from faes_website.site_generator import SiteGenerator


def test_csv_loader_reads_new_format(tmp_path):
    """CSV loader reads new format with name, total, count, recent columns"""
    csv_file = tmp_path / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Org","XCG 10,000",5,2025\n'
        '"Another Org","XCG 5,000",3,2024\n'
    )
    loader = CsvLoader()
    grants = loader.load(csv_file)
    assert len(grants) == 2
    assert grants[0]["title"] == "Test Org"
    assert grants[0]["count"] == 5
    assert grants[0]["most_recent_year"] == 2025
    assert grants[0]["total"] == "XCG 10,000"
    assert grants[0]["type"] == "grant"
    assert grants[0]["public"] is True


def test_csv_loader_filters_grand_total(tmp_path):
    """CSV loader skips the Grand Total row"""
    csv_file = tmp_path / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Org","XCG 10,000",5,2025\n'
        '"Grand Total","XCG 10,000",5,2025\n'
    )
    loader = CsvLoader()
    grants = loader.load(csv_file)
    assert len(grants) == 1
    assert grants[0]["title"] == "Test Org"


def test_csv_loader_validates_required_fields(tmp_path):
    """CSV loader raises error for missing required fields"""
    csv_file = tmp_path / "grants.csv"
    csv_file.write_text(
        "name,total,recent\n"  # missing count
        '"Test Org","XCG 10,000",2025\n'
    )
    loader = CsvLoader()
    with pytest.raises(KeyError, match="Missing required field 'count'"):
        loader.load(csv_file)


def test_site_generator_loads_grants_from_csv(tmp_path):
    """SiteGenerator loads grants from CSV instead of content files"""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    
    # Create a CSV file with grants
    csv_file = content_dir / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Mikve Israel Emanuel","XCG 72,320",22,2025\n'
        '"Citro","XCG 32,423",10,2025\n'
    )
    
    # Create a simple page
    pages_dir = content_dir / "pages"
    pages_dir.mkdir()
    home_page = pages_dir / "home.md"
    home_page.write_text(
        "---\n"
        "title: Home\n"
        "date: 2024-01-01\n"
        "type: page\n"
        "slug: index\n"
        "public: true\n"
        "---\n"
        "# Welcome\n"
    )
    
    gen = SiteGenerator(content_dir, site_dir)
    written = gen.generate(include_private=False)
    
    assert "grants.html" in written
    grants_html = (site_dir / "grants.html").read_text()
    assert "Mikve Israel Emanuel" in grants_html
    assert "Citro" in grants_html


def test_grant_card_contains_recipient_name(tmp_path):
    """Grant card HTML contains the recipient name"""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    
    csv_file = content_dir / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Organization","XCG 5,000",3,2024\n'
    )
    
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(include_private=False)
    
    grants_html = (site_dir / "grants.html").read_text()
    assert "Test Organization" in grants_html
    assert "<h3>Test Organization</h3>" in grants_html


def test_grant_card_simplified_format(tmp_path):
    """Grant card contains only the organization name"""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    
    csv_file = content_dir / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Org","XCG 5,000",7,2024\n'
    )
    
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(include_private=False)
    
    grants_html = (site_dir / "grants.html").read_text()
    assert "Test Org" in grants_html
    # Should NOT contain count or year
    assert "Awarded" not in grants_html
    assert "times" not in grants_html
    assert "Most recently" not in grants_html



def test_grants_sorted_by_count_descending(tmp_path):
    """Grants are sorted by count in descending order"""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    
    csv_file = content_dir / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Low Count","XCG 1,000",2,2024\n'
        '"High Count","XCG 10,000",10,2025\n'
        '"Medium Count","XCG 5,000",5,2023\n'
    )
    
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(include_private=False)
    
    grants_html = (site_dir / "grants.html").read_text()
    # Check that High Count appears before Medium Count, which appears before Low Count
    high_pos = grants_html.find("High Count")
    medium_pos = grants_html.find("Medium Count")
    low_pos = grants_html.find("Low Count")
    
    assert high_pos < medium_pos < low_pos


def test_grant_card_no_description(tmp_path):
    """Grant card does not contain description elements"""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    
    csv_file = content_dir / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Org","XCG 5,000",3,2024\n'
    )
    
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(include_private=False)
    
    grants_html = (site_dir / "grants.html").read_text()
    assert "grant-body" not in grants_html
    assert "grant-type" not in grants_html


def test_csv_loader_reads_optional_logo(tmp_path):
    """CSV loader reads optional logo column"""
    csv_file = tmp_path / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent,logo\n"
        '"Test Org","XCG 10,000",5,2025,testlogo.png\n'
        '"No Logo Org","XCG 5,000",3,2024,\n'
    )
    loader = CsvLoader()
    grants = loader.load(csv_file)
    assert len(grants) == 2
    assert grants[0]["logo"] == "testlogo.png"
    assert "logo" not in grants[1]


def test_grant_card_displays_logo_when_present(tmp_path):
    """Grant card displays logo when present in CSV"""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    
    # Create placeholder logo
    logos_dir = site_dir.parent / "static" / "logos"
    logos_dir.mkdir(parents=True, exist_ok=True)
    (logos_dir / "testlogo.png").write_text("")
    
    csv_file = content_dir / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent,logo\n"
        '"Test Org","XCG 5,000",3,2024,testlogo.png\n'
    )
    
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(include_private=False)
    
    grants_html = (site_dir / "grants.html").read_text()
    assert 'class="grantee-logo"' in grants_html
    assert 'src="static/logos/testlogo.png"' in grants_html


def test_grant_card_no_logo_when_absent(tmp_path):
    """Grant card does not display logo when absent in CSV"""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    
    csv_file = content_dir / "grants.csv"
    csv_file.write_text(
        "name,total,count,recent\n"
        '"Test Org","XCG 5,000",3,2024\n'
    )
    
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(include_private=False)
    
    grants_html = (site_dir / "grants.html").read_text()
    assert 'class="grantee-logo"' not in grants_html
