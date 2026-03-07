# Tasks for Feature F16 — Split people content by language

## T01 — Convert people markdown to pure markdown
**Status**: done
**Description**: Remove embedded HTML from person content, including `content/people/pito-salas.md`, and keep the content as standard markdown only.

## T02 — Add Papiamentu person files
**Status**: done
**Description**: Create `_papiamentu.md` files for each person with matching front matter and body text set to `Coming soon`.

## T03 — Prevent duplicate board cards from language variants
**Status**: done
**Description**: Update board generation so only the default language person records are rendered in `board.html`.

## T04 — Write tests for F16
**Status**: done
**Description**: Add tests to verify board rendering excludes Papiamentu variants and still renders default-language people correctly.
