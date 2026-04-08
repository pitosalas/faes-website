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
        recent_dates = defaultdict(str)
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                name = row.get("nonprofit", "").strip()
                date_str = row.get("date", "").strip()
                year = date_str[:4] if len(date_str) >= 4 else ""
                if not name or not year.isdigit():
                    continue
                amount = self._parse_amount(row.get("amount", ""))
                totals[name] += amount
                counts[name] += 1
                recents[name] = max(recents[name], int(year))
                date = self._parse_date(date_str, year)
                if date > recent_dates[name]:
                    recent_dates[name] = date
        return {
            name: {
                "total": self._format_total(totals[name]),
                "count": counts[name],
                "most_recent_year": recents[name],
                "most_recent_date": recent_dates[name],
            }
            for name in totals
        }

    def _parse_date(self, date_str: str, year: str) -> str:
        if len(date_str) == 10 and date_str[4] == "-":
            return date_str
        return f"{year}-12-31"

    def _format_total(self, amount: float) -> str:
        return f"XCG {amount:,.0f}"

    def load_by_year(self, csv_path: Path) -> dict:
        if not csv_path.exists():
            return {}
        totals = defaultdict(float)
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                date_str = row.get("date", "").strip()
                year = date_str[:4] if len(date_str) >= 4 else ""
                amount = self._parse_amount(row.get("amount", ""))
                if year.isdigit():
                    totals[int(year)] += amount
        return dict(sorted(totals.items()))

    def load_all_rows(self, csv_path: Path) -> list:
        if not csv_path.exists():
            return []
        rows = []
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                date_str = row.get("date", "").strip()
                year = date_str[:4] if len(date_str) >= 4 else ""
                if not year.isdigit():
                    continue
                rows.append({
                    "date": date_str,
                    "nonprofit": row.get("nonprofit", "").strip(),
                    "notes": row.get("notes", "").strip(),
                    "amount": self._parse_amount(row.get("amount", "")),
                    "year": int(year),
                })
        rows.sort(key=lambda r: r["date"], reverse=True)
        return rows

    def _parse_amount(self, raw: str) -> float:
        cleaned = raw.strip().replace("XCG", "").replace(",", "").replace("$", "").strip().rstrip(".")
        return float(cleaned) if cleaned else 0.0
