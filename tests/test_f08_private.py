#!/usr/bin/env python3
# test_f08_private.py — Tests for F08 password-protected private content preview
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import base64
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock
from faes_website.site_generator import SiteGenerator
from faes_website.staging_server import BasicAuthHandler, PASSWORD

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"


def test_include_private_writes_private_pages(tmp_path):
    # Create a test private page
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    pages_dir = content_dir / "pages"
    pages_dir.mkdir()
    (pages_dir / "private.md").write_text("""---
title: Private Page
date: 2024-01-01
type: page
slug: private
public: false
---

Private content.
""", encoding="utf-8")
    # Add grants.csv
    (content_dir / "grants.csv").write_text(
        "name,total,count,recent\n"
        '"Test Org","XCG 5,000",1,2024\n',
        encoding="utf-8"
    )
    
    staging = tmp_path / "staging"
    staging.mkdir()
    written = SiteGenerator(content_dir, staging).generate(include_private=True)
    assert "private.html" in written


def test_exclude_private_omits_private_pages(tmp_path):
    # Create a test private page
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    pages_dir = content_dir / "pages"
    pages_dir.mkdir()
    (pages_dir / "private.md").write_text("""---
title: Private Page
date: 2024-01-01
type: page
slug: private
public: false
---

Private content.
""", encoding="utf-8")
    # Add grants.csv
    (content_dir / "grants.csv").write_text(
        "name,total,count,recent\n"
        '"Test Org","XCG 5,000",1,2024\n',
        encoding="utf-8"
    )
    
    staging = tmp_path / "staging"
    staging.mkdir()
    written = SiteGenerator(content_dir, staging).generate(include_private=False)
    assert "private.html" not in written


def test_include_private_still_writes_public_pages(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    written = SiteGenerator(CONTENT, staging).generate(include_private=True)
    for page in ["index.html", "about.html", "mission.html", "grants.html"]:
        assert page in written


def make_handler(auth_header=None):
    handler = BasicAuthHandler.__new__(BasicAuthHandler)
    handler.headers = {"Authorization": auth_header} if auth_header else {}
    return handler


def test_auth_handler_rejects_no_credentials():
    handler = make_handler()
    assert not handler._authorized()


def test_auth_handler_rejects_wrong_password():
    creds = base64.b64encode(b"user:wrongpassword").decode()
    handler = make_handler(f"Basic {creds}")
    assert not handler._authorized()


def test_auth_handler_accepts_correct_password():
    creds = base64.b64encode(f"user:{PASSWORD}".encode()).decode()
    handler = make_handler(f"Basic {creds}")
    assert handler._authorized()


def test_auth_handler_rejects_non_basic_scheme():
    handler = make_handler("Bearer sometoken")
    assert not handler._authorized()
