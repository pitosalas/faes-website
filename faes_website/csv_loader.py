#!/usr/bin/env python3
# csv_loader.py — reads grant records from a CSV file into content dicts
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import csv
import markdown
from collections import defaultdict
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
        result = {
            "title": row["name"].strip(),
            "count": int(row["count"]),
            "most_recent_year": int(row["recent"]),
            "total": row["total"].strip(),
            "type": "grant",
            "public": True,
            "source_path": source,
        }
        logo_key = next((k for k in row if k.strip().lower() == "logo"), None)
        if logo_key and row[logo_key].strip():
            result["logo"] = row[logo_key].strip()
        return result

    def _validate(self, row: dict, source: Path) -> None:
        for field in ("name", "count", "recent"):
            if field not in row or not row[field].strip():
                raise KeyError(f"Missing required field '{field}' in {source}")

    def load_by_year(self, csv_path: Path) -> dict:
        if not csv_path.exists():
            return {}
        totals = defaultdict(float)
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                year = row.get("Year", "").strip()
                amount = self._parse_amount(row.get("Amount", ""))
                if year.isdigit():
                    totals[int(year)] += amount
        return dict(sorted(totals.items()))

    def _parse_amount(self, raw: str) -> float:
        cleaned = raw.strip().replace("XCG", "").replace(",", "").replace("$", "").strip().rstrip(".")
        return float(cleaned) if cleaned else 0.0
