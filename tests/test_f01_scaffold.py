#!/usr/bin/env python3
# test_f01_scaffold.py — tests for F01 project scaffold
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_required_directories_exist():
    for d in ["content", "faes_website", "templates", "content/static"]:
        assert (ROOT / d).is_dir(), f"Missing directory: {d}"


def test_pyproject_entry_point():
    with open(ROOT / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    scripts = config["project"]["scripts"]
    assert "faes-website" in scripts
    assert scripts["faes-website"] == "faes_website.__main__:main"


def test_pyproject_dependencies():
    with open(ROOT / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    deps = config["project"]["dependencies"]
    for pkg in ["jinja2", "markdown", "pyyaml"]:
        assert any(pkg in d.lower() for d in deps), f"Missing dependency: {pkg}"


def test_uv_run_exits_zero():
    result = subprocess.run(
        ["uv", "run", "faes-website", "--csv", "grants_claude.csv"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Done" in result.stdout
