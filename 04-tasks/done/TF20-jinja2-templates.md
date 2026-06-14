# Tasks for Feature F20 — Extract inline HTML to Jinja2 templates

## T01 — Create templates/html/ directory and base.html
**Status**: done
**Description**: Create `templates/html/` directory. Add `base.html` replacing `_full_page()`, `_header()`, and `_footer()`. Add Jinja2 `Environment` to `SiteGenerator.__init__` using `_TEMPLATES_DIR`. Replace those three methods with `_render_page(title, active, body)`.

## T02 — Create year_chart.html and replace _year_chart
**Status**: done
**Description**: Create `templates/html/year_chart.html` with the Chart.js canvas and script block. Use `{{ labels | tojson }}` and `{{ values | tojson }}` for safe JS literal output. Replace `_year_chart()` with `_render_chart(by_year)`.

## T03 — Create grant_card.html and replace _grant_card
**Status**: done
**Description**: Create `templates/html/grant_card.html`. Replace `_grant_card()` with `_render_grant_card(g)`.

## T04 — Create grants_page.html and update _write_grants
**Status**: done
**Description**: Create `templates/html/grants_page.html` with chart and cards grid sections. Update `_write_grants()` to render body via template.

## T05 — Create person_card.html and replace _person_card
**Status**: done
**Description**: Create `templates/html/person_card.html`. Replace `_person_card()` with `_render_person_card(p)`.

## T06 — Create board_page.html and update _write_board
**Status**: done
**Description**: Create `templates/html/board_page.html`. Update `_write_board()` to render body via template.

## T07 — Create content_page.html and update _write_page
**Status**: done
**Description**: Create `templates/html/content_page.html`. Update `_write_page()` to render body via template instead of inline f-string. Remove `_page_html()` method.

## T08 — Add Jinja2 env to content_loader.py and create photo_figure.html
**Status**: done
**Description**: Add module-level `_env` (autoescape=True) to `content_loader.py`. Create `templates/html/photo_figure.html`. Update `_photo_html()` to render via template; remove `html.escape()` calls and `import html`.

## T09 — Verify all 138 tests pass
**Status**: done
**Description**: Run `uv run pytest` and confirm all 138 tests pass with no regressions.
