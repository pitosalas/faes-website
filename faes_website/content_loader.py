#!/usr/bin/env python3
# content_loader.py — reads and parses markdown content files with YAML front matter
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import markdown
import yaml
from pathlib import Path
from faes_website.csv_loader import CsvLoader


class ContentLoader:
    def load(self, directory: Path) -> list[dict]:
        results = []
        for path in sorted(directory.rglob("*.md")):
            if path.name == "README.md":
                continue
            results.append(self._parse_file(path))
        results.extend(CsvLoader().load(directory / "grants.csv"))
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

    def load_public(self, directory: Path) -> list[dict]:
        return [item for item in self.load(directory) if item.get("public") is True]

    def _validate(self, data: dict, path: Path) -> None:
        for field in ("title", "date", "type", "public"):
            if field not in data:
                raise KeyError(f"Missing required field '{field}' in {path}")
        if data.get("type") == "grant":
            if "grant_type" not in data:
                raise KeyError(f"Missing required field 'grant_type' in {path}")
            if data["grant_type"] not in ("pilot", "primary"):
                raise ValueError(f"Invalid grant_type '{data['grant_type']}' in {path}")
