#!/usr/bin/env python3
# csv_loader.py — reads grant records from a CSV file into content dicts
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import csv
import markdown
from pathlib import Path


class CsvLoader:
    def load(self, csv_path: Path) -> list[dict]:
        if not csv_path.exists():
            return []
        results = []
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                converted = self._convert(row, csv_path)
                if converted is not None:
                    results.append(converted)
        return results

    def _convert(self, row: dict, source: Path) -> dict:
        self._validate(row, source)
        # Skip the Grand Total row
        if row["name"].strip() == "Grand Total":
            return None
        return {
            "title": row["name"].strip(),
            "count": int(row["count"]),
            "most_recent_year": int(row["recent"]),
            "total": row["total"].strip(),
            "type": "grant",
            "public": True,
            "source_path": source,
        }

    def _validate(self, row: dict, source: Path) -> None:
        for field in ("name", "count", "recent"):
            if field not in row or not row[field].strip():
                raise KeyError(f"Missing required field '{field}' in {source}")
