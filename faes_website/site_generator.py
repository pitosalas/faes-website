#!/usr/bin/env python3
# site_generator.py — generates static HTML site from content directory
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import shutil
from pathlib import Path
from faes_website.content_loader import ContentLoader
from faes_website.csv_loader import CsvLoader

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
        people = [i for i in items if i["type"] == "person"]
        
        # Load grants from CSV
        csv_loader = CsvLoader()
        csv_path = self.content_dir / "grants.csv"
        grants = csv_loader.load(csv_path)
        detailed_path = self.content_dir / "grantsdetailed.csv"
        by_year = csv_loader.load_by_year(detailed_path)
        
        # Group pages by slug to find translations
        pages_by_slug = {}
        for page in pages:
          slug = page.get("slug", page["title"].lower().replace(" ", "-"))
          lang = page.get("lang", "en")
          if slug not in pages_by_slug:
            pages_by_slug[slug] = {}
          pages_by_slug[slug][lang] = page
        
        # Write pages with translation info
        for slug, lang_variants in pages_by_slug.items():
          for lang, page in lang_variants.items():
            has_translation = len(lang_variants) > 1
            other_lang = "pap" if lang == "en" else "en"
            translation_url = None
            if has_translation and other_lang in lang_variants:
              translation_url = f"{slug}_pap.html" if other_lang == "pap" else f"{slug}.html"
            self._write_page(page, lang, translation_url)
        
        self._write_grants(grants, by_year)
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

    def _write_page(self, item: dict, lang: str = "en", translation_url: str = None):
        slug = item.get("slug", item["title"].lower().replace(" ", "-"))
        filename = f"{slug}_pap.html" if lang == "pap" else f"{slug}.html"
        html = self._page_html(item["title"], slug, item["body_html"], lang, translation_url)
        self._write(filename, html)

    def _write_grants(self, grants: list, by_year: dict):
        grants = [g for g in grants if g is not None]
        grants.sort(key=lambda g: g["count"], reverse=True)
        cards = "".join(self._grant_card(g) for g in grants)
        chart = self._year_chart(by_year)
        body = f"""
      <div class="grants-header">
        <h1>Grants</h1>
      </div>
      {chart}
      <h2 class="grants-list-header">Grant Recipients</h2>
      <div class="grants-grid">{cards}</div>"""
        html = self._full_page("Grants", "grants", body)
        self._write("grants.html", html)

    def _year_chart(self, by_year: dict) -> str:
        labels = list(by_year.keys())
        values = [by_year[y] for y in labels]
        return f"""
      <div class="chart-section">
        <h2>Total Grants by Year (data is not yet fully correct.)</h2>
        <div class="chart-wrapper">
          <canvas id="grantsChart"></canvas>
        </div>
      </div>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <script>
        const ctx = document.getElementById('grantsChart');
        new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: {labels},
            datasets: [{{
              label: 'Total Donations (XCG)',
              data: {values},
              backgroundColor: 'rgba(74, 124, 89, 0.75)',
              borderColor: 'rgba(74, 124, 89, 1)',
              borderWidth: 2,
              borderRadius: 6,
              borderSkipped: false,
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                callbacks: {{
                  label: ctx => 'XCG ' + ctx.parsed.y.toLocaleString()
                }}
              }}
            }},
            scales: {{
              y: {{
                beginAtZero: true,
                ticks: {{
                  callback: val => 'XCG ' + val.toLocaleString()
                }},
                grid: {{ color: 'rgba(0,0,0,0.06)' }}
              }},
              x: {{
                grid: {{ display: false }},
                offset: true,
              }}
            }}
          }}
        }});
      </script>"""

    def _grant_card(self, g: dict) -> str:
        title = g["title"]
        logo = g.get("logo", "")
        logo_html = ""
        if logo:
            logo_html = f'<img src="static/logos/{logo}" alt="{title} logo" class="grantee-logo">'
        return f"""
        <div class="grant-card">
          <h3>{title}</h3>
          {logo_html}
        </div>"""

    def _write_board(self, people: list):
        board = [p for p in people if p.get("role") == "board" and p.get("lang", "en") == "en"]
        advisors = [p for p in people if p.get("role") == "advisor" and p.get("lang", "en") == "en"]
        board_cards = "".join(self._person_card(p) for p in board)
        advisor_cards = "".join(self._person_card(p) for p in advisors)
        body = f"""
      <div class="board-page">
        <h2>Board</h2>
        <div class="people-grid">{board_cards}</div>
        <h2>Advisors</h2>
        <div class="people-grid">{advisor_cards}</div>
      </div>"""
        html = self._full_page("Board", "board", body)
        self._write("board.html", html)

    def _person_card(self, p: dict) -> str:
        photo = p.get("photo") or "default-person.svg"
        return f"""
        <div class="person-card">
          <img src="static/photos/{photo}" alt="{p["title"]}" class="person-photo">
          <div class="person-card-body">
            <h3>{p["title"]}</h3>
            <div class="person-bio">{p["body_html"]}</div>
          </div>
        </div>"""

    def _page_html(self, title: str, slug: str, body_html: str, lang: str = "en", translation_url: str = None) -> str:
        body = f"""
      <div class="content-page">
        <div class="content-body">{body_html}</div>
      </div>"""
        return self._full_page(title, slug, body, lang, translation_url)

    def _full_page(self, title: str, active: str, body: str, lang: str = "en", translation_url: str = None) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Fundashon Abram Edgardo Salas</title>
  <link rel="stylesheet" href="static/style.css">
</head>
<body class="page-{active}">
  <div class="site-hero">
    <div class="site-banner"></div>
    <div class="site-topbar">Fundashon Abram Edgardo Salas</div>
  </div>
  {self._header(active, lang, translation_url)}
  <main>
    <div class="container">{body}
    </div>
  </main>
  {self._footer()}
</body>
</html>
"""

    def _header(self, active: str, lang: str = "en", translation_url: str = None) -> str:
        links = "".join(
            f'<a href="{href}"{"  class=\"active\"" if slug == active else ""}>{label}</a>'
            for slug, label, href in NAV_ITEMS
        )
        lang_label = "Papiamentu" if lang == "en" else "English"
        if translation_url:
            lang_href = translation_url
        else:
            lang_href = "index_pap.html" if lang == "en" else "index.html"
        links += f'<a href="{lang_href}" class="nav-lang-switch">{lang_label}</a>'
        return f"""<header>
    <div class="container">
      <div class="header-inner">
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
