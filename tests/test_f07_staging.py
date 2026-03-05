#!/usr/bin/env python3
# test_f07_staging.py — Tests for F07 local staging server
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
from faes_website.site_generator import SiteGenerator
from faes_website.staging_server import StagingServer

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"
EXPECTED_PAGES = ["index.html", "about.html", "mission.html", "grants.html"]


def test_staging_generates_to_staging_dir(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    SiteGenerator(CONTENT, staging).generate()
    for page in EXPECTED_PAGES:
        assert (staging / page).exists(), f"Missing {page} in staging"


def test_staging_does_not_touch_site_dir(tmp_path):
    staging = tmp_path / "staging"
    site = tmp_path / "site"
    staging.mkdir()
    site.mkdir()
    SiteGenerator(CONTENT, staging).generate()
    assert list(site.iterdir()) == []


def test_staging_copies_css(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    SiteGenerator(CONTENT, staging).generate()
    assert (staging / "static" / "style.css").is_file()


def test_staging_dir_gitignored():
    gitignore = (ROOT / ".gitignore").read_text()
    assert "staging/" in gitignore


def test_staging_server_init():
    server = StagingServer(ROOT)
    assert server.content_dir == ROOT / "content"
    assert server.staging_dir == ROOT / "staging"
