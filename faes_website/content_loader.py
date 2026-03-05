#!/usr/bin/env python3
# content_loader.py — reads and parses markdown content files with YAML front matter
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import markdown
import yaml
from pathlib import Path


class ContentLoader:
    def load(self, directory: Path) -> list[dict]:
        results = []
        for path in sorted(directory.rglob("*.md")):
            if path.name == "README.md":
                continue
            results.append(self._parse_file(path))
        return results

    def _parse_file(self, path: Path) -> dict:
        raw = path.read_text(encoding="utf-8")
        front_matter, body = self._split(raw)
        data = yaml.safe_load(front_matter)
        self._validate(data, path)
        data["body_html"] = markdown.markdown(body)
        data["source_path"] = path
        return data

    def _split(self, raw: str) -> tuple[str, str]:
        if not raw.startswith("---"):
            return "", raw
        parts = raw.split("---", 2)
        return parts[1], parts[2].strip()

    def _validate(self, data: dict, path: Path) -> None:
        for field in ("title", "date", "type"):
            if field not in data:
                raise KeyError(f"Missing required field '{field}' in {path}")
