#!/usr/bin/env python3
# test_f10_board.py — Tests for F10 board members and advisors page
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from pathlib import Path
from faes_website.content_loader import ContentLoader
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

BOARD_MD = """\
---
title: Jane Board
date: 2024-01-01
type: person
role: board
public: true
---

A board member bio.
"""

ADVISOR_MD = """\
---
title: Joe Advisor
date: 2024-01-01
type: person
role: advisor
public: true
---

An advisor bio.
"""


def make_md(tmp_path, filename, text):
    p = tmp_path / filename
    p.write_text(text, encoding="utf-8")
    return tmp_path


def test_person_loads_correctly(tmp_path):
    make_md(tmp_path, "jane.md", BOARD_MD)
    items = ContentLoader().load(tmp_path)
    assert items[0]["type"] == "person"
    assert items[0]["role"] == "board"
    assert items[0]["title"] == "Jane Board"


def test_missing_role_raises(tmp_path):
    make_md(tmp_path, "norole.md", BOARD_MD.replace("role: board\n", ""))
    with pytest.raises(KeyError, match="role"):
        ContentLoader().load(tmp_path)


def test_invalid_role_raises(tmp_path):
    make_md(tmp_path, "badrole.md", BOARD_MD.replace("role: board", "role: member"))
    with pytest.raises(ValueError, match="role"):
        ContentLoader().load(tmp_path)


def test_board_html_is_generated(tmp_path):
    (tmp_path / "content").mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(tmp_path / "content", site_dir)
    gen.generate(False)
    assert (site_dir / "board.html").exists()


def test_board_html_contains_board_member(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "jane.md").write_text(BOARD_MD, encoding="utf-8")
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(False)
    html = (site_dir / "board.html").read_text()
    assert "Jane Board" in html


def test_board_html_contains_advisor(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "joe.md").write_text(ADVISOR_MD, encoding="utf-8")
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(False)
    html = (site_dir / "board.html").read_text()
    assert "Joe Advisor" in html


def test_board_and_advisors_in_separate_sections(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "jane.md").write_text(BOARD_MD, encoding="utf-8")
    (content_dir / "joe.md").write_text(ADVISOR_MD, encoding="utf-8")
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(False)
    html = (site_dir / "board.html").read_text()
    assert "Board" in html
    assert "Advisors" in html
    assert html.index("Board") < html.index("Jane Board")
    assert html.index("Advisors") < html.index("Joe Advisor")


def test_board_in_navigation(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    gen = SiteGenerator(content_dir, site_dir)
    gen.generate(False)
    html = (site_dir / "board.html").read_text()
    assert "board.html" in html


def test_seed_people_load():
    items = ContentLoader().load(CONTENT)
    people = [i for i in items if i["type"] == "person"]
    names = [p["title"] for p in people]
    assert "Pito Salas" in names
    assert "Janice Godschalk" in names
    assert "Virginia Everts" in names
    assert "Patricia Salas" in names
    assert "Larry Salas" in names
    assert "Harlan Cohen" in names


def test_seed_board_roles():
    items = ContentLoader().load(CONTENT)
    people = [i for i in items if i["type"] == "person" and i.get("lang", "en") == "en"]
    board = [p for p in people if p["role"] == "board"]
    advisors = [p for p in people if p["role"] == "advisor"]
    assert len(board) == 3
    assert len(advisors) == 3
