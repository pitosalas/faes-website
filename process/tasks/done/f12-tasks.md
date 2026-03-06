# F12 Tasks for Feature F12

## T01 — Add .site-topbar div to _full_page
**Status**: done
**Description**: In `site_generator.py`, add `<div class="site-topbar">Fundashon Abram Edgardo Salas</div>` as the first element inside `<body>`, before `.site-banner`.

## T02 — Add .site-topbar CSS
**Status**: done
**Description**: Add `.site-topbar` rule to `static/style.css`: background #2188c4, white text, centered, serif font, compact padding.

## T03 — Write tests
**Status**: done
**Description**: Create `tests/test_f12_topbar.py` covering: topbar div present in generated HTML, topbar contains foundation name, all generated pages have topbar.
