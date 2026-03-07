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
                results.append(self._convert(row, csv_path))
        return results

    def _convert(self, row: dict, source: Path) -> dict:
        self._validate(row, source)
        return {
            "title": row["title"],
            "times_awarded": int(row["times_awarded"]),
            "type": "grant",
            "recipient": row.get("recipient", ""),
            "amount": row.get("amount", ""),
            "year": int(row["year"]),
            "status": row.get("status", ""),
            "grant_type": row["grant_type"],
            "public": row["public"].strip().lower() == "true",
            "body_html": markdown.markdown(row.get("description", "")),
            "logo": row.get("logo", ""),
            "url": row.get("url", ""),
            "source_path": source,
        }

    def _validate(self, row: dict, source: Path) -> None:
        for field in ("title", "times_awarded", "grant_type", "public", "year"):
            if field not in row or not row[field].strip():
                raise KeyError(f"Missing required field '{field}' in {source}")
        if row["grant_type"] not in ("pilot", "primary"):
            raise ValueError(f"Invalid grant_type '{row['grant_type']}' in {source}")
