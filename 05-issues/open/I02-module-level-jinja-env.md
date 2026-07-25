# I02 — Module-level Jinja2 Environment in content_loader.py (side effect at import)

## Symptom
codereview.md MUST: "No side effects at module import time."

`content_loader.py` lines 11–12 create a `jinja2.Environment` and bind it to
a module-level name `env` at import time:

```python
TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "html"
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)
```

This runs filesystem-dependent code the moment the module is imported,
before any instance is created.

## Tests done
Tests pass currently because the templates directory always exists in the
repo. But in environments where templates are missing, the import itself
would behave unexpectedly.

## Latest theory
Move `env` construction into `ContentLoader.__init__` or lazy-initialise
it on first use inside `photo_html`. This also allows tests to override the
templates directory per-instance if needed.
