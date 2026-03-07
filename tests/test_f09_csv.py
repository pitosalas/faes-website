#!/usr/bin/env python3
# test_f09_csv.py — Tests for F09 CSV grant import
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from pathlib import Path
from faes_website.csv_loader import CsvLoader
from faes_website.content_loader import ContentLoader

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

SAMPLE_CSV = """\
title,times_awarded,recipient,amount,year,status,grant_type,public,description
Test Pilot Grant,1,Jane Doe,XCG 5000,2024,awarded,pilot,true,Supported a **reading** program.
Test Primary Grant,2,Org Name,XCG 20000,2024,awarded,primary,false,Funded restoration work.
"""


def write_csv(tmp_path, text):
    p = tmp_path / "grants.csv"
    p.write_text(text, encoding="utf-8")
    return p


def test_csv_parses_two_rows(tmp_path):
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    assert len(items) == 2


def test_csv_public_converted_to_bool(tmp_path):
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    assert items[0]["public"] is True
    assert items[1]["public"] is False


def test_csv_year_converted_to_int(tmp_path):
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    assert items[0]["year"] == 2024
    assert isinstance(items[0]["year"], int)


def test_csv_type_is_grant(tmp_path):
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    assert all(i["type"] == "grant" for i in items)


def test_csv_description_converted_to_html(tmp_path):
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    assert "<strong>reading</strong>" in items[0]["body_html"]


def test_csv_missing_file_returns_empty(tmp_path):
    items = CsvLoader().load(tmp_path / "nonexistent.csv")
    assert items == []


def test_csv_invalid_grant_type_raises(tmp_path):
    bad = SAMPLE_CSV.replace("pilot", "unknown")
    csv_path = write_csv(tmp_path, bad)
    with pytest.raises(ValueError, match="grant_type"):
        CsvLoader().load(csv_path)


def test_csv_missing_required_field_raises(tmp_path):
    bad = "title,times_awarded,recipient\nOnly Title,1,Jane\n"
    csv_path = write_csv(tmp_path, bad)
    with pytest.raises(KeyError):
        CsvLoader().load(csv_path)


def test_content_loader_merges_csv_and_md(tmp_path):
    (tmp_path / "page.md").write_text("""\
---
title: A Page
date: 2024-01-01
type: page
slug: a-page
public: true
---

Content.
""", encoding="utf-8")
    write_csv(tmp_path, SAMPLE_CSV)
    items = ContentLoader().load(tmp_path)
    types = [i["type"] for i in items]
    assert "page" in types
    assert types.count("grant") == 2


def test_seed_csv_loads_correctly():
    items = CsvLoader().load(CONTENT / "grants.csv")
    assert len(items) >= 2
    assert all(i["type"] == "grant" for i in items)
    assert all(isinstance(i["year"], int) for i in items)
