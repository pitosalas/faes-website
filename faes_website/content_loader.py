#!/usr/bin/env python3
# content_loader.py — reads and parses markdown content files with YAML front matter
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import markdown
import yaml
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
_TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "html"
_env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR), autoescape=True)


class ContentLoader:
    def load(self, directory: Path) -> list[dict]:
        results = []
        for path in sorted(directory.rglob("*.md")):
            if path.name == "README.md":
                continue
            if (directory / "orgs") in path.parents:
                continue
            results.append(self._parse_file(path, directory))
        return results

    def _parse_file(self, path: Path, content_dir: Path) -> dict:
        raw = path.read_text(encoding="utf-8")
        front_matter, body = self._split(raw)
        data = yaml.safe_load(front_matter)
        self._validate(data, path)
        preprocessed = self._preprocess_photos(body, path, content_dir)
        data["body_html"] = markdown.markdown(preprocessed)
        data["source_path"] = path
        return data

    def _split(self, raw: str) -> tuple[str, str]:
        if not raw.startswith("---"):
            return "", raw
        parts = raw.split("---", 2)
        return parts[1], parts[2].strip()

    def load_public(self, directory: Path) -> list[dict]:
        return [item for item in self.load(directory) if item.get("public") is True]

    def _validate(self, data: dict, path: Path) -> None:
        for field in ("title", "date", "type", "public"):
            if field not in data:
                raise KeyError(f"Missing required field '{field}' in {path}")
        if data.get("type") == "grant":
            self._validate_grant(data, path)
        if data.get("type") == "person":
            self._validate_person(data, path)

    def _validate_grant(self, data: dict, path: Path) -> None:
        if "grant_type" not in data:
            raise KeyError(f"Missing required field 'grant_type' in {path}")
        if data["grant_type"] not in ("pilot", "primary"):
            raise ValueError(f"Invalid grant_type '{data['grant_type']}' in {path}")

    def _validate_person(self, data: dict, path: Path) -> None:
        if "role" not in data:
            raise KeyError(f"Missing required field 'role' in {path}")
        if data["role"] not in ("board", "advisor"):
            raise ValueError(f"Invalid role '{data['role']}' in {path}")

    def _preprocess_photos(self, body: str, source_path: Path, content_dir: Path) -> str:
        lines = body.splitlines()
        processed = []
        for idx, line in enumerate(lines, start=1):
            if ":photo" not in line:
                processed.append(line)
                continue
            stripped = line.strip()
            if not stripped.startswith(":photo"):
                processed.append(line)
                continue
            processed.append(self._photo_html(stripped, (source_path, idx), content_dir))
        return "\n".join(processed)

    def _photo_html(self, raw_line: str, location: tuple, content_dir: Path) -> str:
        source_path, line_num = location
        pattern = '^:photo\\s+"([^"\\n]+)"\\s*,\\s*"([^"\\n]+)"\\s*,\\s*(\\d+)\\s*,\\s*(left|right|centered)\\s*$'
        match = re.match(pattern, raw_line)
        if match is None:
            raise ValueError(
                f"Invalid :photo syntax in {source_path}:{line_num}. "
                "Expected :photo \"name\", \"caption\", pixel-height, justify"
            )

        name = match.group(1).strip()
        caption = match.group(2).strip()
        height = int(match.group(3))
        justify = match.group(4)
        if height <= 0:
            raise ValueError(f"Invalid pixel-height in {source_path}:{line_num}. Must be > 0")

        image_path = content_dir / "static" / "images" / name
        if not image_path.is_file():
            name = "placeholder-image.jpg"

        return _env.get_template("photo_figure.html").render(
            name=name,
            caption=caption,
            height=height,
            justify=justify,
        ).strip()
