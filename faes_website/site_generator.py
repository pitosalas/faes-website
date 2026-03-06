#!/usr/bin/env python3
# site_generator.py — generates static HTML site from content directory
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import shutil
from pathlib import Path
from faes_website.content_loader import ContentLoader

NAV_ITEMS = [
    ("index", "Home", "index.html"),
    ("about", "About", "about.html"),
    ("mission", "Mission", "mission.html"),
    ("grants", "Grants", "grants.html"),
    ("board", "Board", "board.html"),
]


class SiteGenerator:
    def __init__(self, content_dir: Path, site_dir: Path):
        self.content_dir = content_dir
        self.site_dir = site_dir
        self.written = []

    def generate(self, include_private: bool = False):
        self._copy_static()
        loader = ContentLoader()
        items = loader.load(self.content_dir) if include_private else loader.load_public(self.content_dir)
        pages = [i for i in items if i["type"] == "page"]
        grants = [i for i in items if i["type"] == "grant"]
        people = [i for i in items if i["type"] == "person"]
        for page in pages:
            self._write_page(page)
        self._write_grants(grants)
        self._write_board(people)
        return self.written

    def _copy_static(self):
        src = self.content_dir.parent / "static"
        dst = self.site_dir / "static"
        if src.is_dir() and not dst.exists():
            dst.symlink_to(src.resolve())

    def _write(self, filename: str, html: str):
        path = self.site_dir / filename
        path.write_text(html, encoding="utf-8")
        self.written.append(filename)

    def _write_page(self, item: dict):
        slug = item.get("slug", item["title"].lower().replace(" ", "-"))
        html = self._page_html(item["title"], slug, item["body_html"])
        self._write(f"{slug}.html", html)

    def _write_grants(self, grants: list):
        cards = "".join(self._grant_card(g) for g in grants)
        body = f"""
      <div class="grants-header">
        <h1>Grants</h1>
        <p>A record of grants awarded by the foundation.</p>
      </div>
      <div class="grants-grid">{cards}</div>"""
        html = self._full_page("Grants", "grants", body)
        self._write("grants.html", html)

    def _grant_card(self, g: dict) -> str:
        return f"""
        <div class="grant-card">
          <h3>{g["title"]}</h3>
          <div class="grant-meta">
            <span>{g.get("year", "")}</span>
            <span>{g.get("recipient", "")}</span>
            <span class="grant-type">{g.get("grant_type", "").capitalize()}</span>
          </div>
          <div class="grant-body">{g["body_html"]}</div>
        </div>"""

    def _write_board(self, people: list):
        board = [p for p in people if p.get("role") == "board"]
        advisors = [p for p in people if p.get("role") == "advisor"]
        board_cards = "".join(self._person_card(p) for p in board)
        advisor_cards = "".join(self._person_card(p) for p in advisors)
        body = f"""
      <div class="board-page">
        <h1>Board &amp; Advisors</h1>
        <h2>Board Members</h2>
        <div class="people-grid">{board_cards}</div>
        <h2>Advisors</h2>
        <div class="people-grid">{advisor_cards}</div>
      </div>"""
        html = self._full_page("Board & Advisors", "board", body)
        self._write("board.html", html)

    def _person_card(self, p: dict) -> str:
        return f"""
        <div class="person-card">
          <h3>{p["title"]}</h3>
          <div class="person-bio">{p["body_html"]}</div>
        </div>"""

    def _page_html(self, title: str, slug: str, body_html: str) -> str:
        body = f"""
      <div class="content-page">
        <div class="content-body">{body_html}</div>
      </div>"""
        return self._full_page(title, slug, body)

    def _full_page(self, title: str, active: str, body: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Fundashon Abram Edgardo Salas</title>
  <link rel="stylesheet" href="static/style.css">
</head>
<body>
  <div class="site-banner"></div>
  {self._header(active)}
  <main>
    <div class="container">{body}
    </div>
  </main>
  {self._footer()}
</body>
</html>
"""

    def _header(self, active: str) -> str:
        links = "".join(
            f'<a href="{href}"{"  class=\"active\"" if slug == active else ""}>{label}</a>'
            for slug, label, href in NAV_ITEMS
        )
        return f"""<header>
    <div class="container">
      <div class="header-inner">
        <div class="site-name"><a href="index.html">Fundashon Abram Edgardo Salas</a></div>
        <nav>{links}</nav>
      </div>
    </div>
  </header>"""

    def _footer(self) -> str:
        return """<footer>
    <div class="container">
      <div class="footer-inner">
        <span>Fundashon Abram Edgardo Salas</span>
        <nav>
          <a href="about.html">About</a> &middot;
          <a href="mission.html">Mission</a> &middot;
          <a href="grants.html">Grants</a> &middot;
          <a href="board.html">Board</a>
        </nav>
      </div>
    </div>
  </footer>"""
