#!/usr/bin/env python3
# test_f18_markdown_photo_shortcode.py — Tests for F18 markdown photo shortcode
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
import pytest
from faes_website.content_loader import ContentLoader
from faes_website.site_generator import SiteGenerator


def make_page(content_dir: Path, body: str, filename: str = "page.md") -> None:
    text = f"""\
---
title: Photo Page
date: 2024-01-01
type: page
slug: photo-page
public: true
---

{body}
"""
    (content_dir / filename).write_text(text, encoding="utf-8")


def make_image(tmp_path: Path, name: str) -> None:
    images = tmp_path / "content" / "static" / "images"
    images.mkdir(parents=True, exist_ok=True)
    (images / name).write_text("image", encoding="utf-8")


def load_one_item(tmp_path: Path, body: str) -> dict:
    content_dir = tmp_path / "content"
    content_dir.mkdir(exist_ok=True)
    make_page(content_dir, body)
    return ContentLoader().load(content_dir)[0]


def test_valid_shortcode_replaced_with_figure_html(tmp_path):
    make_image(tmp_path, "kids.jpg")
    item = load_one_item(tmp_path, ':photo "kids.jpg", "Children at workshop", 240, centered')
    assert '<figure class="content-photo justify-centered">' in item["body_html"]
    assert 'src="static/images/kids.jpg"' in item["body_html"]
    assert 'style="height: 240px; width: auto;"' in item["body_html"]
    assert "<figcaption>Children at workshop</figcaption>" in item["body_html"]


def test_multiple_photo_shortcodes_in_one_file(tmp_path):
    make_image(tmp_path, "one.jpg")
    make_image(tmp_path, "two.jpg")
    body = '\n'.join([
        ':photo "one.jpg", "Caption one", 220, left',
        "Text between",
        ':photo "two.jpg", "Caption two", 180, right',
    ])
    item = load_one_item(tmp_path, body)
    assert item["body_html"].count('class="content-photo justify-') == 2


def test_caption_html_is_escaped(tmp_path):
    make_image(tmp_path, "safe.jpg")
    caption = "<b>bold & safe</b>"
    item = load_one_item(tmp_path, f':photo "safe.jpg", "{caption}", 200, left')
    assert "&lt;b&gt;bold &amp; safe&lt;/b&gt;" in item["body_html"]
    assert "<figcaption><b>" not in item["body_html"]


def test_shortcode_whitespace_is_tolerated(tmp_path):
    make_image(tmp_path, "space.jpg")
    item = load_one_item(tmp_path, ':photo    "space.jpg"   ,    "Spaced caption" ,  300 ,   right')
    assert 'src="static/images/space.jpg"' in item["body_html"]


def test_malformed_shortcode_reports_file_and_line(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    make_page(content_dir, ':photo "bad.jpg" "Missing comma"\nNext line')
    with pytest.raises(ValueError, match=r"page\.md:1"):
        ContentLoader().load(content_dir)


def test_missing_image_uses_placeholder(tmp_path):
    make_image(tmp_path, "placeholder-image.jpg")
    item = load_one_item(tmp_path, ':photo "missing.jpg", "Missing", 220, centered')
    assert 'src="static/images/placeholder-image.jpg"' in item["body_html"]
    assert "Missing" in item["body_html"]


def test_invalid_justify_reports_error(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    make_page(content_dir, ':photo "bad.jpg", "Bad", 200, middle')
    with pytest.raises(ValueError, match=r"page\.md:1"):
        ContentLoader().load(content_dir)


def test_invalid_height_reports_error(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    make_page(content_dir, ':photo "bad.jpg", "Bad", 0, left')
    with pytest.raises(ValueError, match=r"page\.md:1"):
        ContentLoader().load(content_dir)


def test_site_generation_contains_processed_photo_html(tmp_path):
    content_dir = tmp_path / "content"
    site_dir = tmp_path / "site"
    content_dir.mkdir()
    site_dir.mkdir()
    make_image(tmp_path, "story.jpg")
    make_page(content_dir, ':photo "story.jpg", "Story image", 280, centered\n\nParagraph text.')

    SiteGenerator(content_dir, site_dir).generate(False)
    html = (site_dir / "photo-page.html").read_text(encoding="utf-8")
    assert 'class="content-photo justify-centered"' in html
    assert 'src="static/images/story.jpg"' in html
    assert 'height: 280px' in html
    assert "Story image" in html
