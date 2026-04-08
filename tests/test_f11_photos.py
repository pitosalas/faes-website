#!/usr/bin/env python3
# test_f11_photos.py — Tests for F11 board member photo support
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator

PERSON_WITH_PHOTO = """\
---
title: Jane Board
date: 2024-01-01
type: person
role: board
public: true
photo: jane.jpg
---

A board member bio.
"""

PERSON_NO_PHOTO = """\
---
title: Joe Board
date: 2024-01-01
type: person
role: board
public: true
---

Another board member.
"""


def setup_site(tmp_path, *person_texts):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    for i, text in enumerate(person_texts):
        (content_dir / f"person{i}.md").write_text(text, encoding="utf-8")
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    SiteGenerator(content_dir, site_dir).generate(False, "grants_claude.csv")
    return (site_dir / "board.html").read_text()


def test_photo_renders_img_tag(tmp_path):
    html = setup_site(tmp_path, PERSON_WITH_PHOTO)
    assert "<img" in html
    assert "jane.jpg" in html


def test_photo_uses_static_photos_path(tmp_path):
    html = setup_site(tmp_path, PERSON_WITH_PHOTO)
    assert 'src="static/photos/jane.jpg"' in html


def test_photo_alt_text_is_person_name(tmp_path):
    html = setup_site(tmp_path, PERSON_WITH_PHOTO)
    assert 'alt="Jane Board"' in html


def test_no_photo_uses_default_placeholder(tmp_path):
    html = setup_site(tmp_path, PERSON_NO_PHOTO)
    assert "default-person.svg" in html


def test_photo_and_no_photo_both_have_img(tmp_path):
    html = setup_site(tmp_path, PERSON_WITH_PHOTO, PERSON_NO_PHOTO)
    assert "jane.jpg" in html
    assert "default-person.svg" in html
    assert html.count("<img") == 2


def test_static_photos_dir_exists():
    root = Path(__file__).parent.parent
    assert (root / "content" / "static" / "photos").is_dir()
