#!/usr/bin/env python3
# test_f09_csv.py — Tests for F09 CSV grant import (superseded by F21 org directories)
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.content_loader import ContentLoader

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"


def test_content_loader_ignores_grants_csv(tmp_path):
    """ContentLoader no longer loads grants from grants.csv (superseded by F21)"""
    (tmp_path / "grants.csv").write_text(
        "name,total,count,recent\nJane Doe,\"XCG 3,000\",1,2024\n",
        encoding="utf-8",
    )
    items = ContentLoader().load(tmp_path)
    assert not any(i.get("type") == "grant" for i in items)


def test_content_loader_does_not_load_org_md_files(tmp_path):
    """ContentLoader skips org.md files inside content/orgs/"""
    org_dir = tmp_path / "orgs" / "Test Org"
    org_dir.mkdir(parents=True)
    (org_dir / "org.md").write_text(
        "---\ngrant_type: pilot\npublic: true\n---\n",
        encoding="utf-8",
    )
    items = ContentLoader().load(tmp_path)
    assert len(items) == 0
