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
name,total,count,recent
Jane Doe,"XCG 3,000",1,2024
Org Name,"XCG 10,000",2,2023
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
    # New format: all grants are public
    assert items[0]["public"] is True
    assert items[1]["public"] is True


def test_csv_times_awarded_converted_to_int(tmp_path):
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    # New format: field is called 'count'
    assert items[0]["count"] == 1
    assert isinstance(items[0]["count"], int)


def test_csv_type_is_grant(tmp_path):
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    assert all(i["type"] == "grant" for i in items)


def test_csv_description_converted_to_html(tmp_path):
    # New format: no description/body_html in simplified cards
    csv_path = write_csv(tmp_path, SAMPLE_CSV)
    items = CsvLoader().load(csv_path)
    assert "body_html" not in items[0]


def test_csv_missing_file_returns_empty(tmp_path):
    items = CsvLoader().load(tmp_path / "nonexistent.csv")
    assert items == []


def test_csv_invalid_grant_type_raises(tmp_path):
    # New format: no grant_type validation needed
    # Test that invalid count raises error instead
    bad = "name,total,count,recent\nTest,XCG 1000,invalid,2024\n"
    csv_path = write_csv(tmp_path, bad)
    with pytest.raises(ValueError):
        CsvLoader().load(csv_path)


def test_csv_missing_required_field_raises(tmp_path):
    # New format: requires name, total, count, recent
    bad = "name,total\nJane,XCG 1000\n"
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
    # New format: field is called 'count'
    assert all(isinstance(i["count"], int) for i in items)
