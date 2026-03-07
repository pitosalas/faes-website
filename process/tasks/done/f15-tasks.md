# Tasks for Feature F15 — Language switcher for bilingual pages

## T01 — Create separate Papiamentu content files
**Status**: done
**Description**: Extract Papiamentu content from home.md, mission.md, and about.md into separate files: home_papiamentu.md, mission_papiamentu.md, and about_papiamentu.md. Add `lang: pap` to frontmatter of Papiamentu files.

## T02 — Update English content files to remove bilingual grid
**Status**: done
**Description**: Remove the bilingual-grid HTML and Papiamentu sections from home.md, mission.md, and about.md, leaving only the English content in clean markdown format.

## T03 — Update content loader to handle language variants
**Status**: done
**Description**: Modify content_loader.py to recognize language variants (files ending in _papiamentu.md) and associate them with their English counterparts using the slug field.

## T04 — Add language switcher to page template
**Status**: done
**Description**: Update site_generator.py to add a language switcher button near the top of pages that have translations. The button should link to the alternate language version (index_pap.html, mission_pap.html, about_pap.html).

## T05 — Update site generator to create language-specific HTML files
**Status**: done
**Description**: Modify site_generator.py to generate separate HTML files for Papiamentu versions (e.g., index_pap.html, mission_pap.html, about_pap.html) from the _papiamentu.md files.

## T06 — Add CSS styling for language switcher button
**Status**: done
**Description**: Add CSS rules to static/style.css for the language switcher button, making it visually distinct and accessible.

## T07 — Write tests for F15
**Status**: done
**Description**: Write pytest tests that verify: (1) Papiamentu files are loaded separately, (2) language switcher button appears on bilingual pages, (3) correct HTML files are generated for both languages, (4) links between language versions work correctly.
