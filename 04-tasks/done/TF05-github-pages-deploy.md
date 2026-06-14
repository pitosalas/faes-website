# F05 Tasks for Feature F05

## T01 — Create .github/workflows/deploy.yml
**Status**: done
**Description**: Created GitHub Actions workflow triggered on push to `main`. Steps: checkout, install uv, uv sync, uv run faes-website, upload-pages-artifact, deploy-pages.

## T02 — Configure GitHub Pages source in workflow
**Status**: done
**Description**: Used `actions/upload-pages-artifact` + `actions/deploy-pages` with `pages: write` and `id-token: write` permissions.

## T03 — Ensure site/ is not gitignored
**Status**: done
**Description**: Moved `style.css` from `site/static/` to root `static/`. Updated `SiteGenerator._copy_static()` to copy `static/` into `site/static/` at build time. CI generates the full `site/` from scratch on each run.

## T04 — Write tests
**Status**: done
**Description**: Added `tests/test_f05_deploy.py` with 8 tests verifying workflow exists, triggers on main, runs generator, deploys pages, has correct permissions, and that the generator copies static assets.
