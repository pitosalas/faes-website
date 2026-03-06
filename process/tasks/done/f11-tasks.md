# F11 Tasks for Feature F11

## T01 — Update _person_card to render photo
**Status**: done
**Description**: In `site_generator.py`, update `_person_card` to check for a `photo` key. If present, render `<img src="static/photos/{photo}" alt="{title}" class="person-photo">` before the name. If absent, render nothing.

## T02 — Create static/photos/ directory
**Status**: done
**Description**: Create `static/photos/` with a `.gitkeep` so the directory is tracked. Photos dropped here are automatically served.

## T03 — Add photo field example to one person file
**Status**: done
**Description**: Add `photo: pito-salas.jpg` to `content/people/pito-salas.md` as a demonstration of the format. The actual image file is not required for the code to work.

## T04 — Write tests
**Status**: done
**Description**: Create `tests/test_f11_photos.py` covering: person card with photo field includes img tag, person card without photo field omits img tag, img src path uses static/photos/ prefix, alt text equals person title.
