#!/usr/bin/env python3
# site_generator.py — generates static HTML site from content directory
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from faes_website.content_loader import ContentLoader
from faes_website.csv_loader import CsvLoader
from faes_website.org_loader import OrgLoader

NAV_ITEMS = [
    ("index", "Home", "index.html"),
    ("about", "About", "about.html"),
    ("mission", "Mission", "mission.html"),
    ("grants", "Grants", "grants.html"),
    ("board", "Board", "board.html"),
]

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "html"


class SiteGenerator:
    def __init__(self, content_dir: Path, site_dir: Path):
        self.content_dir = content_dir
        self.site_dir = site_dir
        self.written = []
        self._lang = "en"
        self._translation_url = None
        self._env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), autoescape=False)

    def generate(self, include_private: bool, csv_name: str):
        self._copy_static()
        loader = ContentLoader()
        items = loader.load(self.content_dir) if include_private else loader.load_public(self.content_dir)
        pages = [i for i in items if i["type"] == "page"]
        people = [i for i in items if i["type"] == "person"]

        csv_loader = CsvLoader()
        detailed_path = self.content_dir / csv_name
        summaries = csv_loader.summarise_by_org(detailed_path)
        by_year = csv_loader.load_by_year(detailed_path)
        all_rows = csv_loader.load_all_rows(detailed_path)
        org_loader = OrgLoader(self.content_dir)
        org_loader.validate(set(summaries.keys()))
        orgs = org_loader.load()
        self._copy_org_logos(orgs)
        grants = self._build_grants(summaries, orgs, include_private)

        pages_by_slug = {}
        for page in pages:
            slug = page.get("slug", page["title"].lower().replace(" ", "-"))
            lang = page.get("lang", "en")
            if slug not in pages_by_slug:
                pages_by_slug[slug] = {}
            pages_by_slug[slug][lang] = page

        for slug, lang_variants in pages_by_slug.items():
            for lang, page in lang_variants.items():
                has_translation = len(lang_variants) > 1
                other_lang = "pap" if lang == "en" else "en"
                translation_url = None
                if has_translation and other_lang in lang_variants:
                    translation_url = f"{slug}_pap.html" if other_lang == "pap" else f"{slug}.html"
                self._write_page(page, lang, translation_url)

        self._write_grants(grants)
        self._write_secret(by_year, all_rows)
        self._write_board(people)
        return self.written

    def _copy_static(self):
        src = self.content_dir / "static"
        dst = self.site_dir / "static"
        if not src.is_dir():
            return
        if dst.is_symlink() and not dst.exists():
            dst.unlink()
        if not dst.exists():
            dst.symlink_to(src.resolve())

    def _write(self, filename: str, html: str):
        path = self.site_dir / filename
        path.write_text(html, encoding="utf-8")
        self.written.append(filename)

    def _render_page(self, title: str, active: str, body: str) -> str:
        return self._env.get_template("base.html").render(
            title=title,
            active=active,
            body=body,
            lang=self._lang,
            translation_url=self._translation_url,
            nav_items=NAV_ITEMS,
        )

    def _write_page(self, item: dict, lang: str, translation_url):
        self._lang = lang
        self._translation_url = translation_url
        slug = item.get("slug", item["title"].lower().replace(" ", "-"))
        filename = f"{slug}_pap.html" if lang == "pap" else f"{slug}.html"
        body = self._env.get_template("content_page.html").render(body_html=item["body_html"])
        self._write(filename, self._render_page(item["title"], slug, body))

    def _build_grants(self, summaries: dict, orgs: dict, include_private: bool) -> list:
        result = []
        for name, summary in summaries.items():
            org = orgs[name]
            if not include_private and not org["public"]:
                continue
            logo = f"orgs/{name}/{org['logo']}" if org["logo"] else ""
            result.append({
                "title": name,
                "count": summary["count"],
                "most_recent_year": summary["most_recent_year"],
                "most_recent_date": summary["most_recent_date"],
                "total": summary["total"],
                "logo": logo,
                "url": org.get("url", ""),
                "blurb": org.get("blurb", ""),
                "grant_type": org["grant_type"],
                "public": org["public"],
            })
        return result

    def _copy_org_logos(self, orgs: dict):
        for name, meta in orgs.items():
            if not meta["logo"]:
                continue
            src = self.content_dir / "orgs" / name / meta["logo"]
            if not src.is_file():
                continue
            dst_dir = self.site_dir / "orgs" / name
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst_dir / meta["logo"])

    def _write_grants(self, grants: list):
        self._lang = "en"
        self._translation_url = None
        grants = [g for g in grants if g is not None]
        grants.sort(key=lambda g: g["count"], reverse=True)
        cards_html = "".join(self._render_grant_card(g) for g in grants)
        body = self._env.get_template("grants_page.html").render(cards_html=cards_html)
        self._write("grants.html", self._render_page("Grants", "grants", body))

    def _write_secret(self, by_year: dict, all_rows: list):
        self._lang = "en"
        self._translation_url = None
        years = sorted(by_year.keys(), reverse=True)
        chart_html = self._render_chart(by_year)
        body = self._env.get_template("secret_page.html").render(
            chart_html=chart_html,
            years=years,
            rows_json=json.dumps(all_rows),
        )
        self._write("secret.html", self._render_page("Secret", "secret", body))

    def _render_chart(self, by_year: dict) -> str:
        labels = list(by_year.keys())
        values = [by_year[y] for y in labels]
        return self._env.get_template("year_chart.html").render(labels=labels, values=values)

    def _render_grant_card(self, g: dict) -> str:
        return self._env.get_template("grant_card.html").render(
            title=g["title"],
            logo=g.get("logo", ""),
            url=g.get("url", ""),
            blurb=g.get("blurb", ""),
            most_recent_year=g.get("most_recent_year", 0),
            most_recent_date=g.get("most_recent_date", ""),
        )

    def _write_board(self, people: list):
        board_en = [p for p in people if p.get("role") == "board" and p.get("lang", "en") == "en"]
        advisors_en = [p for p in people if p.get("role") == "advisor" and p.get("lang", "en") == "en"]
        board_pap = [p for p in people if p.get("role") == "board" and p.get("lang") == "pap"]
        advisors_pap = [p for p in people if p.get("role") == "advisor" and p.get("lang") == "pap"]
        has_pap = bool(board_pap or advisors_pap)

        self._lang = "en"
        self._translation_url = "board_pap.html" if has_pap else None
        body = self._env.get_template("board_page.html").render(
            board_cards_html="".join(self._render_person_card(p) for p in board_en),
            advisor_cards_html="".join(self._render_person_card(p) for p in advisors_en),
        )
        self._write("board.html", self._render_page("Board", "board", body))

        if has_pap:
            self._lang = "pap"
            self._translation_url = "board.html"
            body = self._env.get_template("board_page.html").render(
                board_cards_html="".join(self._render_person_card(p) for p in board_pap),
                advisor_cards_html="".join(self._render_person_card(p) for p in advisors_pap),
            )
            self._write("board_pap.html", self._render_page("Board", "board", body))

    def _render_person_card(self, p: dict) -> str:
        photo = p.get("photo") or "default-person.svg"
        return self._env.get_template("person_card.html").render(
            name=p["title"],
            photo=photo,
            bio_html=p["body_html"],
        )
