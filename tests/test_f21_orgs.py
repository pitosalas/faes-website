#!/usr/bin/env python3
# test_f21_orgs.py — Tests for F21 org directories replacing grants.csv
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from pathlib import Path
from faes_website.org_loader import OrgLoader
from faes_website.csv_loader import CsvLoader
from faes_website.site_generator import SiteGenerator

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"


def make_org(orgs_dir: Path, name: str, grant_type="pilot", public=True, logo=""):
    org_dir = orgs_dir / name
    org_dir.mkdir(parents=True, exist_ok=True)
    lines = ["---", f"grant_type: {grant_type}", f"public: {'true' if public else 'false'}"]
    lines += ["---", ""]
    (org_dir / "org.md").write_text("\n".join(lines), encoding="utf-8")
    if logo:
        (org_dir / logo).write_bytes(b"")


def make_detailed_csv(content_dir: Path, rows: list):
    lines = ["date,nonprofit,amount,notes"] + [f"{y}-01-01,{r},{a}," for y, r, a in rows]
    (content_dir / "grants_claude.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


# --- OrgLoader.load() ---

def test_org_loader_reads_grant_type(tmp_path):
    make_org(tmp_path / "orgs", "Test Org", grant_type="primary")
    orgs = OrgLoader(tmp_path).load()
    assert orgs["Test Org"]["grant_type"] == "primary"


def test_org_loader_reads_public_flag(tmp_path):
    make_org(tmp_path / "orgs", "Public Org", public=True)
    make_org(tmp_path / "orgs", "Private Org", public=False)
    orgs = OrgLoader(tmp_path).load()
    assert orgs["Public Org"]["public"] is True
    assert orgs["Private Org"]["public"] is False


def test_org_loader_reads_logo(tmp_path):
    make_org(tmp_path / "orgs", "Logo Org", logo="mylogo.png")
    orgs = OrgLoader(tmp_path).load()
    assert orgs["Logo Org"]["logo"] == "mylogo.png"


def test_org_loader_logo_defaults_empty(tmp_path):
    make_org(tmp_path / "orgs", "No Logo Org")
    orgs = OrgLoader(tmp_path).load()
    assert orgs["No Logo Org"]["logo"] == ""


def test_org_loader_url_defaults_empty(tmp_path):
    make_org(tmp_path / "orgs", "No Url Org")
    orgs = OrgLoader(tmp_path).load()
    assert orgs["No Url Org"]["url"] == ""


def test_org_loader_missing_grant_type_raises(tmp_path):
    org_dir = tmp_path / "orgs" / "Bad Org"
    org_dir.mkdir(parents=True)
    (org_dir / "org.md").write_text("---\npublic: true\n---\n", encoding="utf-8")
    with pytest.raises(KeyError, match="grant_type"):
        OrgLoader(tmp_path).load()


def test_org_loader_invalid_grant_type_raises(tmp_path):
    org_dir = tmp_path / "orgs" / "Bad Org"
    org_dir.mkdir(parents=True)
    (org_dir / "org.md").write_text("---\ngrant_type: mega\npublic: true\n---\n", encoding="utf-8")
    with pytest.raises(ValueError, match="grant_type"):
        OrgLoader(tmp_path).load()


def test_org_loader_missing_orgs_dir_returns_empty(tmp_path):
    orgs = OrgLoader(tmp_path).load()
    assert orgs == {}


# --- OrgLoader.validate() ---

def test_validate_passes_when_sets_match(tmp_path):
    make_org(tmp_path / "orgs", "Org A")
    make_org(tmp_path / "orgs", "Org B")
    OrgLoader(tmp_path).validate({"Org A", "Org B"})  # should not raise


def test_validate_raises_on_extra_dir(tmp_path, capsys):
    make_org(tmp_path / "orgs", "Org A")
    make_org(tmp_path / "orgs", "Extra Org")
    with pytest.raises(SystemExit) as exc:
        OrgLoader(tmp_path).validate({"Org A"})
    assert exc.value.code == 1
    output = capsys.readouterr().out
    assert "Extra Org" in output


def test_validate_raises_on_missing_dir(tmp_path, capsys):
    make_org(tmp_path / "orgs", "Org A")
    with pytest.raises(SystemExit) as exc:
        OrgLoader(tmp_path).validate({"Org A", "Missing Org"})
    assert exc.value.code == 1
    output = capsys.readouterr().out
    assert "Missing Org" in output


def test_validate_passes_when_both_empty(tmp_path):
    OrgLoader(tmp_path).validate(set())  # missing orgs dir + empty set → ok


# --- CsvLoader.summarise_by_org() ---

def test_summarise_computes_count(tmp_path):
    make_detailed_csv(tmp_path, [(2023, "Org A", "XCG 1000."), (2023, "Org A", "XCG 500.")])
    result = CsvLoader().summarise_by_org(tmp_path / "grants_claude.csv")
    assert result["Org A"]["count"] == 2


def test_summarise_computes_total(tmp_path):
    make_detailed_csv(tmp_path, [(2023, "Org A", "XCG 1000."), (2023, "Org A", "XCG 500.")])
    result = CsvLoader().summarise_by_org(tmp_path / "grants_claude.csv")
    assert result["Org A"]["total"] == "XCG 1,500"


def test_summarise_computes_most_recent_year(tmp_path):
    make_detailed_csv(tmp_path, [(2020, "Org A", "XCG 500."), (2023, "Org A", "XCG 1000.")])
    result = CsvLoader().summarise_by_org(tmp_path / "grants_claude.csv")
    assert result["Org A"]["most_recent_year"] == 2023


def test_summarise_multiple_orgs(tmp_path):
    make_detailed_csv(tmp_path, [(2023, "Org A", "XCG 1000."), (2023, "Org B", "XCG 500.")])
    result = CsvLoader().summarise_by_org(tmp_path / "grants_claude.csv")
    assert "Org A" in result
    assert "Org B" in result


def test_summarise_missing_file_returns_empty(tmp_path):
    result = CsvLoader().summarise_by_org(tmp_path / "nonexistent.csv")
    assert result == {}


# --- Site generation smoke test ---

def test_generate_uses_orgs_not_grants_csv(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    make_detailed_csv(content_dir, [(2024, "Test Org", "XCG 5000.")])
    make_org(content_dir / "orgs", "Test Org", grant_type="pilot", public=True)
    SiteGenerator(content_dir, site_dir).generate(include_private=False, csv_name="grants_claude.csv")
    html = (site_dir / "grants.html").read_text()
    assert "Test Org" in html


def test_generate_excludes_private_orgs(tmp_path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    make_detailed_csv(content_dir, [
        (2024, "Public Org", "XCG 5000."),
        (2024, "Private Org", "XCG 1000."),
    ])
    make_org(content_dir / "orgs", "Public Org", public=True)
    make_org(content_dir / "orgs", "Private Org", public=False)
    SiteGenerator(content_dir, site_dir).generate(include_private=False, csv_name="grants_claude.csv")
    html = (site_dir / "grants.html").read_text()
    assert "Public Org" in html
    # Private orgs are always in HTML (hidden via CSS), marked with data-private
    assert "Private Org" in html
    assert 'data-private="true"' in html


def test_generate_validates_orgs_match(tmp_path, capsys):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    make_detailed_csv(content_dir, [(2024, "Known Org", "XCG 5000.")])
    make_org(content_dir / "orgs", "Wrong Org")  # mismatch
    with pytest.raises(SystemExit):
        SiteGenerator(content_dir, site_dir).generate(include_private=False, csv_name="grants_claude.csv")


def test_real_content_orgs_match_grantsdetailed():
    loader = OrgLoader(CONTENT)
    csv_loader = CsvLoader()
    summaries = csv_loader.summarise_by_org(CONTENT / "reconciled_double.csv")
    loader.validate(set(summaries.keys()))  # should not raise
