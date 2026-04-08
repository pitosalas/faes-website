#!/usr/bin/env python3
# test_f16_people_language_split.py — Tests for F16 people language split
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator

PERSON_EN = """\
---
title: Jane Doe
date: 2024-01-01
type: person
role: board
public: true
---

English bio.
"""

PERSON_PAP = """\
---
title: Jane Doe
date: 2024-01-01
type: person
role: board
public: true
lang: pap
---

Coming soon
"""


def board_html(tmp_path, *person_texts):
    content_dir = tmp_path / "content"
    site_dir = tmp_path / "site"
    content_dir.mkdir()
    site_dir.mkdir()
    for i, text in enumerate(person_texts):
        suffix = "_papiamentu" if "lang: pap" in text else ""
        (content_dir / f"person{i}{suffix}.md").write_text(text, encoding="utf-8")
    SiteGenerator(content_dir, site_dir).generate(False, "grants_claude.csv")
    return (site_dir / "board.html").read_text()


def test_board_excludes_papiamentu_people_variants(tmp_path):
    html = board_html(tmp_path, PERSON_EN, PERSON_PAP)
    assert "English bio" in html
    assert "Coming soon" not in html


def test_board_still_renders_default_language_people(tmp_path):
    html = board_html(tmp_path, PERSON_EN)
    assert "Jane Doe" in html
    assert "English bio" in html
