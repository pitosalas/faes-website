# faes-website

Static site generator for Fundashon Abram Edgardo Salas.

The project builds a public website from markdown content and org data, then deploys it to GitHub Pages.

## What this project does

- Converts `content/pages/*.md` pages and `content/people/*.md` profiles into static HTML.
- Loads grant recipient data from `content/orgs/` subdirectories (one per org, each with `org.md`).
- Loads grant transaction history from `content/all_bank_transactions.csv`.
- Supports English and Papiamentu page variants.
- Supports public/private preview modes for local staging.
- Adds inline photo shortcodes in markdown content.

## Quick start

### Prerequisites

- Python 3.12+
- `uv`

### Install dependencies

```bash
uv sync
```

### Generate the site

```bash
uv run faes-website
```

Output is written to `site/`.

### Run local staging server

Public content:

```bash
uv run faes-website --serve
```

Private preview (HTTP Basic Auth, password: xyzzy):

```bash
uv run faes-website --serve --private
```

Default staging URL: `http://localhost:8000`

## Development commands

Run all tests:

```bash
uv run pytest
```

Run one test file:

```bash
uv run pytest tests/test_f21_orgs.py
```

## Content system

All author-managed content lives under `content/`.

### Pages and people

Markdown files in `content/pages/` and `content/people/` use YAML front matter. Required keys:

- `title`
- `date`
- `type`
- `public`

Additional rules:

- `type: page` requires `slug`.
- `type: person` requires `role` (`board` or `advisor`).

### Orgs

Each grant recipient has a subdirectory under `content/orgs/<Org Name>/` containing:

- `org.md` — YAML front matter with required fields `grant_type` (`pilot` or `primary`) and `public`; optional fields `name`, `url`, `blurb`, `logo`, `2025_recipient`
- An optional logo image (`.png`, `.jpg`, or `.jpeg`); detected automatically

### Transactions CSV

Grant transaction history is loaded from `content/all_bank_transactions.csv` with columns:

- `date` (YYYY-MM-DD)
- `nonprofit` — must match an `orgs/` subdirectory name exactly
- `amount`
- `notes`

## Inline photo shortcode

Markdown supports inline photo insertion with preprocessing before markdown-to-HTML conversion.

Shortcode format:

```markdown
:photo "name", "caption", pixel-height, justify
```

Example:

```markdown
:photo "punda1.jpg", "Downtown Curacao waterfront", 320, centered
```

Rules:

- `name` is a filename under `static/images/`.
- `caption` is used for both caption text and image `alt` text.
- `pixel-height` must be an integer greater than 0.
- `justify` must be one of `left`, `right`, `centered`.
- Shortcode must be on its own line.

Failure behavior:

- Invalid syntax or values raise an error with source file and line number.
- Missing image files gracefully fall back to `placeholder-image.jpg`.

## Project structure

Key directories and files:

- `faes_website/content_loader.py`: parses front matter, preprocesses photo shortcodes, converts markdown to HTML.
- `faes_website/csv_loader.py`: loads and summarises transaction data from CSV files.
- `faes_website/org_loader.py`: reads per-org metadata from `content/orgs/` subdirectories.
- `faes_website/config_loader.py`: reads and validates `config.yml`.
- `faes_website/site_generator.py`: writes HTML pages and copies/symlinks static assets.
- `faes_website/staging_server.py`: local HTTP server with optional auth.
- `faes_website/__main__.py`: CLI entrypoint.
- `content/pages/`: markdown pages (home, about, mission, language variants).
- `content/people/`: markdown profiles for board members and advisors.
- `content/orgs/`: one subdirectory per grant recipient with `org.md` and optional logo.
- `content/all_bank_transactions.csv`: full grant transaction history.
- `static/`: CSS, logos, photos, and general images (`static/images/`).
- `tests/`: feature-aligned test files (`test_f01_*` through `test_f21_*`).
- `process/`: feature and task tracking docs.

## Generation pipeline

Pipeline overview:

1. Load config from `config.yml`.
2. Read markdown content from `content/pages/` and `content/people/`.
3. Preprocess photo shortcodes inside markdown bodies.
4. Convert markdown to HTML.
5. Load org metadata from `content/orgs/`.
6. Load transaction summaries from `content/all_bank_transactions.csv`.
7. Build pages (`index`, `about`, `mission`, `board`, `grants`, and language variants).
8. Write output into `site/` (or `staging/` for serve flows).

## Deployment

Deployment is handled by GitHub Actions on push to `main`, publishing generated output to GitHub Pages for `faesfoundation.com`.

## Notes for content authors

- Keep text content in markdown, not embedded HTML where possible.
- Put person photos in `static/photos/` when using person front-matter `photo` fields.
- Put inline body images for `:photo` shortcode in `static/images/`.
- Use descriptive captions because they are also used as alt text.
- The `nonprofit` field in `all_bank_transactions.csv` must match an `orgs/` directory name exactly.
