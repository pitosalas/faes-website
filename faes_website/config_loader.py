#!/usr/bin/env python3
# config_loader.py — reads and validates config.yml
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import yaml
from pathlib import Path


class ConfigLoader:
    def load(self, config_path: Path) -> dict:
        if not config_path.exists():
            return {}
        with config_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def css_vars(self, config: dict) -> str:
        t = config.get("org_year_table", {})
        lines = [
            ":root {",
            f"  --org-year-font-size: {t.get('font_size', '0.65rem')};",
            f"  --org-year-col-width: {t.get('year_column_width', '32px')};",
            f"  --org-year-org-width: {t.get('org_column_width', '100px')};",
            f"  --org-year-cell-padding: {t.get('cell_padding', '0.02rem 0.08rem')};",
            "}",
        ]
        return "\n".join(lines)
