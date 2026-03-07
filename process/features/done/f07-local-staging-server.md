# Feature description for feature F07
## F07 — Local staging server
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: A `--serve` mode that generates the site into a separate `staging/` directory (never touching `site/`) and starts a local HTTP server so the user can preview it in a browser. Invoked with `uv run faes-website --serve`. The `staging/` directory is gitignored and never deployed to GitHub Pages.
