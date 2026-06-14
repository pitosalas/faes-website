# Tasks for Feature F18 — Markdown photo shortcode

## T01 — Define shortcode parser contract
**Status**: done
**Description**: Specify accepted shortcode grammar exactly as `:photo "name", "caption", pixel-height, justify`, including whitespace tolerance rules and quote handling. Document unsupported variants and expected error messages.

## T02 — Add markdown preprocessor hook in content loading
**Status**: done
**Description**: Update markdown loading flow so body text is preprocessed before `markdown.markdown(...)` runs. Ensure all markdown content types that produce `body_html` use the same preprocessing step.

## T03 — Implement shortcode replacement to semantic HTML
**Status**: done
**Description**: Replace each valid `:photo` line with semantic figure markup including alignment and size: `<figure class="content-photo justify-{justify}">`, `<img src="static/images/{name}" alt="{caption}" style="height: {pixel-height}px; width: auto;">`, and `<figcaption>{caption}</figcaption>`.

## T04 — Validate referenced image files exist
**Status**: done
**Description**: During content parsing, verify that each referenced image exists in `static/images/`. Raise a clear exception with source path and line number when missing.

## T05 — Add stylesheet support for inline content photos
**Status**: done
**Description**: Add minimal CSS for `.content-photo` and caption styling so inserted figures render cleanly on desktop and mobile without disrupting existing layout.

## T06 — Create and track static/images directory
**Status**: done
**Description**: Create `static/images/` (with `.gitkeep`) and document that image filenames in shortcode are relative to this directory.

## T07 — Update content authoring documentation
**Status**: done
**Description**: Update `content/README.md` with shortcode usage examples, escaping notes, and common errors (bad syntax, missing file).

## T08 — Write tests for F18
**Status**: done
**Description**: Add tests covering valid shortcode replacement, multiple photos in one file, caption escaping safety, whitespace handling, malformed shortcode error reporting (with filename/line), invalid height/justify errors, missing image file error, and integration in generated page HTML.
