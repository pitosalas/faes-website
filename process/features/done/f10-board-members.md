# Feature description for feature F10
## F10 — Board members and advisors page
**Priority**: Medium
**Done:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: A dedicated "Board" page listing the foundation's board members and advisors in two sections. Each person is defined by a markdown file in `content/people/` with YAML front matter fields: `title` (full name), `date`, `type: person`, `role: board|advisor`, `public: true|false`. The body is an optional short bio. `ContentLoader` validates the `role` field. `SiteGenerator` generates `board.html` from all `type: person` items, grouped by role. The Board page is added to the main navigation. Initial board members: Pito Salas, Janice Godschalk, Virginia Evers-Kleinmoedig. Initial advisors: Patricia Salas, Larry Salas, Harlan Cohen.
