#!/usr/bin/env python3
# csv_loader.py — reads grant data from grantsdetailed.csv
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import csv
from collections import defaultdict
from pathlib import Path


class CsvLoader:
    def summarise_by_org(self, csv_path: Path) -> dict:
        if not csv_path.exists():
            return {}
        totals = defaultdict(float)
        counts = defaultdict(int)
        recents = defaultdict(int)
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                name = row.get("Recipient", "").strip()
                year = row.get("Year", "").strip()
                if not name or not year.isdigit():
                    continue
                amount = self._parse_amount(row.get("Amount_NAf", ""))
                totals[name] += amount
                counts[name] += 1
                recents[name] = max(recents[name], int(year))
        return {
            name: {
                "total": self._format_total(totals[name]),
                "count": counts[name],
                "most_recent_year": recents[name],
            }
            for name in totals
        }

    def _format_total(self, amount: float) -> str:
        return f"XCG {amount:,.0f}"

    def load_by_year(self, csv_path: Path) -> dict:
        if not csv_path.exists():
            return {}
        totals = defaultdict(float)
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                year = row.get("Year", "").strip()
                amount = self._parse_amount(row.get("Amount_NAf", ""))
                if year.isdigit():
                    totals[int(year)] += amount
        return dict(sorted(totals.items()))

    def _parse_amount(self, raw: str) -> float:
        cleaned = raw.strip().replace("XCG", "").replace(",", "").replace("$", "").strip().rstrip(".")
        return float(cleaned) if cleaned else 0.0
