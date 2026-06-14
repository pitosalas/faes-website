# Tasks for Feature F01 — Project scaffold and content directory structure

## T01 — Initialize Python package with pyproject.toml
**Status**: done
**Description**: Create `pyproject.toml` with project name `faes-website`, Python version requirement, and entry point so the generator can be run with `uv run faes-website`. Add dependencies: `jinja2`, `markdown`, `pyyaml`.

## T02 — Create directory structure
**Status**: done
**Description**: Create the following directories: `content/` (source markdown), `site/` (generated output, git-ignored), `faes_website/` (Python package source), `templates/` (Jinja2 HTML templates), `static/` (CSS, images, JS assets).

## T03 — Update .gitignore for generated output
**Status**: done
**Description**: Add `site/` to `.gitignore` so generated HTML is not committed. The site is rebuilt on each push via GitHub Actions.

## T04 — Verify uv run works
**Status**: done
**Description**: Create a minimal `faes_website/__main__.py` with a stub `main()` that prints "faes-website generator". Confirm `uv run faes-website` executes without errors.

## T05 — Write tests for F01
**Status**: done
**Description**: Write pytest tests that verify: (1) required directories exist, (2) `pyproject.toml` has the correct entry point, (3) `uv run faes-website` exits with code 0.
