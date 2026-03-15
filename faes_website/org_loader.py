#!/usr/bin/env python3
# org_loader.py — reads per-org metadata from content/orgs/ subdirectories
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import yaml
from pathlib import Path


class OrgLoader:
    def __init__(self, content_dir: Path):
        self._orgs_dir = content_dir / "orgs"

    def load(self) -> dict:
        if not self._orgs_dir.exists():
            return {}
        result = {}
        for org_dir in sorted(self._orgs_dir.iterdir()):
            if not org_dir.is_dir():
                continue
            org_file = org_dir / "org.md"
            if not org_file.exists():
                raise FileNotFoundError(f"Missing org.md in {org_dir}")
            result[org_dir.name] = self._parse(org_file)
        return result

    def _parse(self, path: Path) -> dict:
        raw = path.read_text(encoding="utf-8")
        parts = raw.split("---", 2)
        data = yaml.safe_load(parts[1]) if len(parts) >= 2 else {}
        self._validate(data, path)
        logo = self._detect_logo(path.parent)
        if logo != data.get("logo", ""):
            self._write_logo(path, data, logo)
        return {
            "grant_type": data["grant_type"],
            "public": data["public"],
            "logo": logo,
            "url": data.get("url", ""),
            "blurb": data.get("blurb", ""),
        }

    IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}

    def _detect_logo(self, org_dir: Path) -> str:
        images = sorted(f.name for f in org_dir.iterdir()
                        if f.suffix.lower() in self.IMAGE_SUFFIXES)
        return images[0] if images else ""

    def _write_logo(self, path: Path, data: dict, logo: str) -> None:
        lines = ["---", f"grant_type: {data['grant_type']}",
                 f"public: {'true' if data['public'] else 'false'}"]
        if logo:
            lines.append(f"logo: {logo}")
        if data.get("url"):
            lines.append(f"url: {data['url']}")
        if data.get("blurb"):
            lines.append(f"blurb: {data['blurb']}")
        lines += ["---", ""]
        path.write_text("\n".join(lines), encoding="utf-8")

    def validate(self, recipients: set) -> None:
        if self._orgs_dir.exists():
            org_names = {d.name for d in self._orgs_dir.iterdir() if d.is_dir()}
        else:
            org_names = set()
        extra_dirs = org_names - recipients
        missing_dirs = recipients - org_names
        if not extra_dirs and not missing_dirs:
            return
        if extra_dirs:
            print("ERROR: orgs/ directories with no matching grantsdetailed.csv recipient:")
            for name in sorted(extra_dirs):
                print(f"  + {name}")
        if missing_dirs:
            print("ERROR: grantsdetailed.csv recipients with no matching orgs/ directory:")
            for name in sorted(missing_dirs):
                print(f"  - {name}")
        raise SystemExit(1)

    def _validate(self, data: dict, path: Path) -> None:
        for field in ("grant_type", "public"):
            if field not in data:
                raise KeyError(f"Missing required field '{field}' in {path}")
        if data["grant_type"] not in ("pilot", "primary"):
            raise ValueError(f"Invalid grant_type '{data['grant_type']}' in {path}")
