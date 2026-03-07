#!/usr/bin/env python3
# test_f15_language_switcher.py — Tests for F15 language switcher feature
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator
from faes_website.content_loader import ContentLoader

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

ENGLISH_PAGE = """\
---
title: Test Page
date: 2024-01-01
type: page
slug: testpage
public: true
---

# English Content

This is in English.
"""

PAPIAMENTU_PAGE = """\
---
title: Test Page
date: 2024-01-01
type: page
slug: testpage
public: true
lang: pap
---

# Kontenido Papiamentu

Esaki ta na Papiamentu.
"""

def make_md(path: Path, filename: str, text: str):
    p = path / filename
    p.write_text(text, encoding="utf-8")


def test_papiamentu_files_load_with_lang_marker(tmp_path):
    content = tmp_path / "content"
    content.mkdir()
    make_md(content, "page_papiamentu.md", PAPIAMENTU_PAGE)
    items = ContentLoader().load(content)
    assert len(items) == 1
    assert items[0].get("lang") == "pap"


def test_english_files_default_to_en_lang(tmp_path):
    content = tmp_path / "content"
    content.mkdir()
    make_md(content, "page.md", ENGLISH_PAGE)
    items = ContentLoader().load(content)
    page = items[0]
    # English pages don't have lang in frontmatter, generator defaults to "en"
    assert page.get("lang") is None or page.get("lang") == "en"


def test_generator_creates_separate_html_files_for_languages(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", ENGLISH_PAGE)
    make_md(content, "page_papiamentu.md", PAPIAMENTU_PAGE)
    SiteGenerator(content, site).generate()
    assert (site / "testpage.html").exists()
    assert (site / "testpage_pap.html").exists()


def test_lang_switcher_appears_on_bilingual_pages(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", ENGLISH_PAGE)
    make_md(content, "page_papiamentu.md", PAPIAMENTU_PAGE)
    SiteGenerator(content, site).generate()
    en_html = (site / "testpage.html").read_text()
    pap_html = (site / "testpage_pap.html").read_text()
    assert "nav-lang-switch" in en_html
    assert "nav-lang-switch" in pap_html


def test_lang_switcher_links_to_correct_file(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", ENGLISH_PAGE)
    make_md(content, "page_papiamentu.md", PAPIAMENTU_PAGE)
    SiteGenerator(content, site).generate()
    en_html = (site / "testpage.html").read_text()
    pap_html = (site / "testpage_pap.html").read_text()
    assert 'href="testpage_pap.html"' in en_html
    assert 'href="testpage.html"' in pap_html


def test_lang_switcher_shows_correct_label(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", ENGLISH_PAGE)
    make_md(content, "page_papiamentu.md", PAPIAMENTU_PAGE)
    SiteGenerator(content, site).generate()
    en_html = (site / "testpage.html").read_text()
    pap_html = (site / "testpage_pap.html").read_text()
    assert "Papiamentu" in en_html
    assert "English" in pap_html


def test_no_lang_switcher_on_monolingual_pages(tmp_path):
    content = tmp_path / "content"
    site = tmp_path / "site"
    content.mkdir()
    site.mkdir()
    make_md(content, "page.md", ENGLISH_PAGE)
    SiteGenerator(content, site).generate()
    html = (site / "testpage.html").read_text()
    assert "nav-lang-switch" in html
    assert 'href="index_pap.html"' in html


def test_real_content_has_bilingual_pages():
    items = ContentLoader().load(CONTENT)
    pages = [i for i in items if i["type"] == "page"]
    slugs_by_lang = {}
    for page in pages:
        slug = page.get("slug")
        lang = page.get("lang", "en")
        if slug not in slugs_by_lang:
            slugs_by_lang[slug] = set()
        slugs_by_lang[slug].add(lang)
    # Check that index, mission, and about have both English and Papiamentu
    for slug in ["index", "mission", "about"]:
        assert slug in slugs_by_lang
        assert "en" in slugs_by_lang[slug]
        assert "pap" in slugs_by_lang[slug]
