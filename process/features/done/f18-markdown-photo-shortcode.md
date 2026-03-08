# Feature description for feature F18
## F18 — Markdown photo shortcode
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Add a lightweight markdown preprocessor that recognizes a photo shortcode line in markdown content: `:photo "name", "caption", pixel-height, justify`. The preprocessor runs before markdown-to-HTML conversion and replaces each shortcode with semantic HTML using `<figure>`, `<img>`, and `<figcaption>`. Images are referenced from a dedicated directory `static/images/` using the provided filename. Example input `:photo "children-reading.jpg", "Students reading at the community center", 320, centered` becomes `<figure class="content-photo justify-centered"><img src="static/images/children-reading.jpg" alt="Students reading at the community center" style="height: 320px; width: auto;"><figcaption>Students reading at the community center</figcaption></figure>`. Invalid shortcode syntax should raise a clear error that includes the source filename and line number. Missing image files should raise a clear error during generation so broken images are caught early.

## Parser contract
- A shortcode must appear on its own markdown line.
- Accepted grammar: `:photo "name", "caption", pixel-height, justify`
- Whitespace is allowed around `:photo` arguments and comma separator.
- `name` and `caption` must be double-quoted and non-empty.
- `pixel-height` must be an integer greater than 0.
- `justify` must be one of: `left`, `right`, `centered`.
- Unsupported forms (single quotes, missing comma, missing quotes, trailing text, invalid height/justify) raise `ValueError` with `path:line` in the message.
- If `name` does not exist at `static/images/{name}`, falls back to `placeholder-image.jpg`.
