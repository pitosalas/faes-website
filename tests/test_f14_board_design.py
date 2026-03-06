#!/usr/bin/env python3
# test_f14_board_design.py — Tests for F14 board page card design
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent

PERSON_WITH_PHOTO = """\
---
title: Jane Board
date: 2024-01-01
type: person
role: board
public: true
photo: jane.jpg
---
A bio.
"""

PERSON_NO_PHOTO = """\
---
title: Joe Board
date: 2024-01-01
type: person
role: board
public: true
---
A bio.
"""


def board_html(tmp_path, *person_texts):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    for i, text in enumerate(person_texts):
        (content_dir / f"p{i}.md").write_text(text, encoding="utf-8")
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    SiteGenerator(content_dir, site_dir).generate()
    return (site_dir / "board.html").read_text()


def test_card_always_has_img(tmp_path):
    html = board_html(tmp_path, PERSON_NO_PHOTO)
    assert "<img" in html


def test_no_photo_uses_default(tmp_path):
    html = board_html(tmp_path, PERSON_NO_PHOTO)
    assert "default-person.svg" in html


def test_photo_uses_specified_file(tmp_path):
    html = board_html(tmp_path, PERSON_WITH_PHOTO)
    assert "jane.jpg" in html
    assert "default-person.svg" not in html


def test_card_has_person_card_class(tmp_path):
    html = board_html(tmp_path, PERSON_NO_PHOTO)
    assert "person-card" in html


def test_card_has_card_body(tmp_path):
    html = board_html(tmp_path, PERSON_NO_PHOTO)
    assert "person-card-body" in html


def test_default_svg_exists():
    assert (ROOT / "static" / "photos" / "default-person.svg").exists()


def test_people_grid_css_exists():
    css = (ROOT / "static" / "style.css").read_text()
    assert ".people-grid" in css
    assert ".person-card" in css
    assert ".person-photo" in css
