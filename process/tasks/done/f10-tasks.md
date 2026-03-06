# F10 Tasks for Feature F10

## T01 — Add person type validation to ContentLoader
**Status**: done
**Description**: In `_validate`, add a check for `type: person` that requires a `role` field with value `board` or `advisor`. Raise `KeyError` if missing, `ValueError` if invalid.

## T02 — Create content/people/ directory with person files
**Status**: done
**Description**: Create `content/people/` and add one `.md` file per person. Board members: Pito Salas, Janice Godschalk, Virginia Everts. Advisors: Patricia Salas, Larry Salas, Harlan Cohen. Each file has front matter with `type: person`, `role: board|advisor`, `public: true`, and a short bio body.

## T03 — Add _write_board() to SiteGenerator and update nav
**Status**: done
**Description**: Add `("board", "Board", "board.html")` to `NAV_ITEMS`. In `generate()`, collect `type: person` items and call `_write_board()`. Implement `_write_board()` to render two sections (Board Members, Advisors) with person cards, writing `board.html`. Add "Board" to the footer nav links.

## T04 — Write tests
**Status**: done
**Description**: Create `tests/test_f10_board.py` covering: person content loads correctly, missing role raises KeyError, invalid role raises ValueError, board.html is generated, board.html contains board member names, board.html contains advisor names, board and advisors are in separate sections, board page is in navigation.
