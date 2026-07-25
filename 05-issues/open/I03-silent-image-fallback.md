# I03 — Missing image silently replaced with placeholder (should raise)

## Symptom
codereview.md MUST: "Do not compensate for a violated expectation by
reinterpreting, coercing, defaulting, or branching to 'make it work'."

`content_loader.py` lines 94–96:

```python
image_path = content_dir / "static" / "images" / name
if not image_path.is_file():
    name = "placeholder-image.jpg"
```

If an author references an image that doesn't exist, the code silently
substitutes a placeholder instead of reporting the error. This hides typos
in `:photo` directives and produces a page that renders without warning.

## Tests done
None for this path — the silent fallback is the current behaviour and tests
don't assert on it.

## Latest theory
Replace the silent fallback with a `FileNotFoundError` (or at minimum a
`print`/`warnings.warn`) that names the missing file and the source location.
Authors should be told clearly that their image reference is broken.
