#!/usr/bin/env python3
# __main__.py — entry point for the faes-website static site generator
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path
from faes_website.config_loader import ConfigLoader
from faes_website.site_generator import SiteGenerator
from faes_website.staging_server import StagingServer

ROOT = Path(__file__).parent.parent


def _resolve_csv(args: list[str], config: dict) -> str:
    for i, arg in enumerate(args):
        if arg == "--csv" and i + 1 < len(args):
            return args[i + 1]
    csv_file = config.get("csv_file")
    if csv_file:
        return csv_file
    print("Error: no csv_file in config.yml and --csv not provided")
    sys.exit(1)


def main():
    args = sys.argv[1:]
    config = ConfigLoader().load(ROOT / "config.yml")
    csv_name = _resolve_csv(args, config)
    if "--serve" in args:
        StagingServer(ROOT).run(private="--private" in args, csv_name=csv_name)
    else:
        written = SiteGenerator(ROOT / "content", ROOT / "site").generate(False, csv_name)
        for filename in written:
            print(f"  wrote {filename}")
        print(f"Done — {len(written)} files written to {ROOT / 'site'}")


if __name__ == "__main__":
    main()
