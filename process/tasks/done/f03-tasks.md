# F03 Tasks for Feature F03

## T01 — Create SiteGenerator class
**Status**: done
**Description**: Created `faes_website/site_generator.py` with a `SiteGenerator` class that accepts `content_dir` and `site_dir` as Path args and has a `generate()` method that orchestrates the full build using `ContentLoader.load_public()`.

## T02 — Implement shared HTML structure as Python functions
**Status**: done
**Description**: Implemented `_header(active)` and `_footer()` as methods returning HTML strings for the nav/header/footer common to all pages.

## T03 — Implement page generation
**Status**: done
**Description**: For each public content item with `type == "page"`, writes `{slug}.html` to `site/`. Body is the rendered `body_html` from ContentLoader.

## T04 — Implement grants page generation
**Status**: done
**Description**: Collects all public items with `type == "grant"` and writes `site/grants.html` as a card grid with title, recipient, year, amount, and grant_type badge.

## T05 — Wire up __main__.py
**Status**: done
**Description**: `main()` calls `SiteGenerator(content_dir, site_dir).generate()` and prints a summary of files written.

## T06 — Write tests
**Status**: done
**Description**: Added `tests/test_f03_generator.py` with 8 tests verifying page generation, private content exclusion, grants HTML, card content, and real content run.
