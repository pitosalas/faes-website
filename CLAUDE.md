# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

We are developing an app called faes-website. Read the files in the process/ folder to understand the development.

The following steps are required when Claude Code first launches:

1. If there is no folder called `process/` then this is the first time running — read and follow: @.claude/bootstrap.md
2. If writing new code or doing a code review, read and follow: @.claude/coding.md
3. For all other prompts in this session: @.claude/method.md

## Commands

```bash
uv sync                                        # install dependencies
uv run faes-website                            # generate static site to site/
uv run faes-website --serve                    # local staging server on port 8000 (public content)
uv run faes-website --serve --private          # staging with HTTP Basic Auth (password: xyzzy, all content)
uv run pytest                                  # run full test suite
uv run pytest tests/test_f03_generator.py      # run a single test file
```

## Architecture

The app is a Python static site generator that reads markdown+YAML content files and produces HTML output deployed to GitHub Pages.

**Pipeline:** `content/*.md` → `ContentLoader` → `SiteGenerator` → `site/*.html` → GitHub Pages

- **`faes_website/content_loader.py`** — reads all `.md` files, parses YAML front matter and markdown body, validates required fields (`title`, `date`, `type`, `public`), and filters public vs. private content
- **`faes_website/site_generator.py`** — generates one HTML file per page, one aggregated `grants.html` with card layout, and symlinks `static/` assets; supports `include_private` flag
- **`faes_website/staging_server.py`** — Python `http.server` on port 8000; optional HTTP Basic Auth for private content preview
- **`faes_website/__main__.py`** — CLI entry point; routes `--serve` and `--private` flags

**Content** lives in `content/` as markdown files with YAML front matter. Required fields: `title`, `date`, `type`, `public`. Grants additionally require `grant_type` (pilot or primary). Output goes to `site/` (production) or `staging/` (local preview); both are gitignored.

**Deployment** is via `.github/workflows/deploy.yml` — pushes to `main` trigger site generation and GitHub Pages deployment to `faesfoundation.com`.

**Tests** in `tests/` are organized by feature (e.g. `test_f03_generator.py`). All 8 features are complete and tested.
