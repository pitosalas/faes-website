# Feature description for feature F03
## F03 — Static site generator (Python)
**Priority**: High
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: A Python program that reads all markdown files from `content/`, applies HTML templates, and writes the generated site to `site/`. Must handle: YAML front matter parsing, markdown-to-HTML conversion, applying layout templates, generating an index/home page, copying static assets, and filtering out content where `public: false`. Only public content is written to `site/`. Invoked with `uv run` from the project root.
