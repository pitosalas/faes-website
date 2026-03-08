#!/usr/bin/env python3
# test_f19_grants_chart.py — Tests for F19 grants-by-year bar chart
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from pathlib import Path
from faes_website.csv_loader import CsvLoader
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

SAMPLE_DETAILED = """\
Year,Recipient,Amount
2020,Org A,"XCG 5,000."
2020,Org B,XCG 500.
2021,Org A,"XCG 10,000."
2022,Org C,XCG .
"""


def write_detailed(tmp_path, text):
    p = tmp_path / "grantsdetailed.csv"
    p.write_text(text, encoding="utf-8")
    return p


def test_load_by_year_sums_correctly(tmp_path):
    p = write_detailed(tmp_path, SAMPLE_DETAILED)
    result = CsvLoader().load_by_year(p)
    assert result[2020] == pytest.approx(5500.0)
    assert result[2021] == pytest.approx(10000.0)


def test_load_by_year_zero_amount_counts_as_zero(tmp_path):
    p = write_detailed(tmp_path, SAMPLE_DETAILED)
    result = CsvLoader().load_by_year(p)
    assert result[2022] == pytest.approx(0.0)


def test_load_by_year_sorted_ascending(tmp_path):
    p = write_detailed(tmp_path, SAMPLE_DETAILED)
    result = CsvLoader().load_by_year(p)
    assert list(result.keys()) == sorted(result.keys())


def test_load_by_year_missing_file_returns_empty(tmp_path):
    result = CsvLoader().load_by_year(tmp_path / "nonexistent.csv")
    assert result == {}


def test_parse_amount_xcg_format():
    loader = CsvLoader()
    assert loader._parse_amount("XCG 5,000.") == pytest.approx(5000.0)
    assert loader._parse_amount("XCG 419.6") == pytest.approx(419.6)
    assert loader._parse_amount("XCG 2,222.5") == pytest.approx(2222.5)


def test_parse_amount_empty_xcg():
    assert CsvLoader()._parse_amount("XCG .") == pytest.approx(0.0)


def test_parse_amount_dollar_format():
    assert CsvLoader()._parse_amount("$5,000.00") == pytest.approx(5000.0)


def test_load_by_year_skips_non_year_rows(tmp_path):
    csv_text = "Year,Recipient,Amount\n2023,Org A,XCG 1000.\n,,XCG 999.\n"
    p = write_detailed(tmp_path, csv_text)
    result = CsvLoader().load_by_year(p)
    assert list(result.keys()) == [2023]


def test_real_detailed_csv_loads():
    result = CsvLoader().load_by_year(CONTENT / "grantsdetailed.csv")
    assert len(result) > 10
    assert all(isinstance(k, int) for k in result.keys())
    assert all(v >= 0 for v in result.values())


def test_chart_html_in_generated_grants_page(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "grants.csv").write_text(
        "name,total,count,recent\nOrg A,XCG 1000,1,2023\n", encoding="utf-8"
    )
    (content_dir / "grantsdetailed.csv").write_text(
        "Year,Recipient,Amount\n2023,Org A,XCG 1000.\n", encoding="utf-8"
    )
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(content_dir, site_dir)
    gen._write_grants([], {2023: 1000.0})
    html = (site_dir / "grants.html").read_text()
    assert "grantsChart" in html
    assert "2023" in html
    assert "1000" in html


def test_chart_title_in_grants_page(tmp_path):
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(tmp_path / "content", site_dir)
    gen._write_grants([], {2024: 5000.0})
    html = (site_dir / "grants.html").read_text()
    assert "Total Grants by Year" in html
