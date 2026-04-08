#!/usr/bin/env python3
# test_f17_csv_grants.py — Tests for F17 simplified grant cards (now served via F21 org dirs)
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
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
    lines = ["Date,Year,Recipient,Amount_NAf,Notes"] + [f",{y},{r},{a}," for y, r, a in rows]
    (content_dir / "grants_claude.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_grants_page(tmp_path, rows, orgs=None, include_private=False):
    content_dir = tmp_path / "content"
    content_dir.mkdir(exist_ok=True)
    site_dir = tmp_path / "site"
    site_dir.mkdir(exist_ok=True)
    make_detailed_csv(content_dir, rows)
    for org_kwargs in (orgs or []):
        make_org(content_dir / "orgs", **org_kwargs)
    SiteGenerator(content_dir, site_dir).generate(include_private, "grants_claude.csv")
    return (site_dir / "grants.html").read_text()


def test_grant_card_contains_recipient_name(tmp_path):
    html = make_grants_page(tmp_path, [(2024, "Test Organization", "XCG 5000.")],
                            [{"name": "Test Organization"}])
    assert "Test Organization" in html
    assert "<h3>Test Organization</h3>" in html


def test_grant_card_simplified_format(tmp_path):
    html = make_grants_page(tmp_path, [(2024, "Test Org", "XCG 5000.")],
                            [{"name": "Test Org"}])
    assert "Test Org" in html
    assert "Awarded" not in html
    assert "times" not in html
    assert "Most recently" not in html


def test_grants_sorted_by_count_descending(tmp_path):
    rows = [
        (2024, "Low Count", "XCG 1000."),
        (2025, "High Count", "XCG 10000."), (2025, "High Count", "XCG 10000."),
        (2025, "High Count", "XCG 10000."), (2025, "High Count", "XCG 10000."),
        (2025, "High Count", "XCG 10000."), (2025, "High Count", "XCG 10000."),
        (2025, "High Count", "XCG 10000."), (2025, "High Count", "XCG 10000."),
        (2025, "High Count", "XCG 10000."), (2025, "High Count", "XCG 10000."),
        (2023, "Medium Count", "XCG 5000."), (2023, "Medium Count", "XCG 5000."),
        (2023, "Medium Count", "XCG 5000."), (2023, "Medium Count", "XCG 5000."),
        (2023, "Medium Count", "XCG 5000."),
    ]
    orgs = [{"name": "Low Count"}, {"name": "High Count"}, {"name": "Medium Count"}]
    html = make_grants_page(tmp_path, rows, orgs)
    high_pos = html.find("High Count")
    medium_pos = html.find("Medium Count")
    low_pos = html.find("Low Count")
    assert high_pos < medium_pos < low_pos


def test_grant_card_no_description(tmp_path):
    html = make_grants_page(tmp_path, [(2024, "Test Org", "XCG 5000.")],
                            [{"name": "Test Org"}])
    assert "grant-body" not in html
    assert "grant-type" not in html


def test_grant_card_displays_logo_when_present(tmp_path):
    html = make_grants_page(tmp_path, [(2024, "Test Org", "XCG 5000.")],
                            [{"name": "Test Org", "logo": "testlogo.png"}])
    assert 'class="grantee-logo"' in html
    assert 'src="orgs/Test Org/testlogo.png"' in html


def test_grant_card_no_logo_when_absent(tmp_path):
    html = make_grants_page(tmp_path, [(2024, "Test Org", "XCG 5000.")],
                            [{"name": "Test Org", "logo": ""}])
    assert 'class="grantee-logo"' not in html
