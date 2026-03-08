# faes-website

Static site generator for Fundashon Abram Edgardo Salas.

The project builds a public website from markdown content and CSV grant data, then deploys it to GitHub Pages.

## What this project does

- Converts `content/**/*.md` pages and people profiles into static HTML.
- Imports grants from `content/grants.csv`.
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

Private preview (HTTP Basic Auth):

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
uv run pytest tests/test_f18_markdown_photo_shortcode.py
```

## Content system

All author-managed content lives under `content/`.

### Markdown files

Markdown files use YAML front matter. Required keys for markdown items:

- `title`
- `date`
- `type`
- `public`

Additional rules:

- `type: page` requires `slug`.
- `type: person` requires `role` (`board` or `advisor`).

### Grants CSV

Grants are loaded from `content/grants.csv` with schema:

- `name` (required)
- `total` (required)
- `count` (required)
- `recent` (required)
- `logo` (optional) - filename relative to `static/logos/`

The generated grants page currently renders simplified cards with recipient names and optional logos.

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
- `faes_website/csv_loader.py`: loads grants from CSV.
- `faes_website/site_generator.py`: writes HTML pages and copies/symlinks static assets.
- `faes_website/staging_server.py`: local HTTP server with optional auth.
- `faes_website/__main__.py`: CLI entrypoint.
- `content/`: markdown pages and people plus `grants.csv`.
- `static/`: CSS, logos, photos, and general images (`static/images/`).
- `templates/`: template assets (if used by feature changes).
- `tests/`: feature-aligned test files (`test_f01_*` through `test_f18_*`).
- `process/`: feature and task tracking docs.

## Generation pipeline

Pipeline overview:

1. Read markdown and CSV content.
2. Preprocess photo shortcodes inside markdown bodies.
3. Convert markdown to HTML.
4. Build pages (`index`, `about`, `mission`, `board`, `grants`, and language variants).
5. Write output into `site/` (or `staging/` for serve flows).

## Deployment

Deployment is handled by GitHub Actions on push to `main`, publishing generated output to GitHub Pages for `faesfoundation.com`.

## Notes for content authors

- Keep text content in markdown, not embedded HTML where possible.
- Put person photos in `static/photos/` when using person front-matter `photo` fields.
- Put inline body images for `:photo` shortcode in `static/images/`.
- Use descriptive captions because they are also used as alt text.
