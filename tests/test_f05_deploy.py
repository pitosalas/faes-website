#!/usr/bin/env python3
# test_f05_deploy.py — Tests for F05 GitHub Pages deployment workflow
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path

ROOT = Path(__file__).parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "deploy.yml"


def test_workflow_file_exists():
    assert WORKFLOW.is_file()


def test_workflow_triggers_on_main():
    content = WORKFLOW.read_text()
    assert "branches:" in content
    assert "main" in content


def test_workflow_runs_generator():
    content = WORKFLOW.read_text()
    assert "uv run faes-website" in content


def test_workflow_deploys_pages():
    content = WORKFLOW.read_text()
    assert "actions/deploy-pages" in content


def test_workflow_uploads_site_artifact():
    content = WORKFLOW.read_text()
    assert "upload-pages-artifact" in content
    assert "site/" in content


def test_workflow_has_pages_permissions():
    content = WORKFLOW.read_text()
    assert "pages: write" in content
    assert "id-token: write" in content


def test_static_source_exists():
    assert (ROOT / "content" / "static" / "style.css").is_file()


def test_generator_copies_static(tmp_path):
    from faes_website.site_generator import SiteGenerator
    content = ROOT / "content"
    site = tmp_path / "site"
    site.mkdir()
    SiteGenerator(content, site).generate(False, "grants_claude.csv")
    assert (site / "static" / "style.css").is_file()
