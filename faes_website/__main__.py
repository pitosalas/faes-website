#!/usr/bin/env python3
# __main__.py — entry point for the faes-website static site generator
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path
from faes_website.site_generator import SiteGenerator
from faes_website.staging_server import StagingServer

ROOT = Path(__file__).parent.parent


def _get_csv_name(args: list[str]) -> str:
    for i, arg in enumerate(args):
        if arg == "--csv" and i + 1 < len(args):
            return args[i + 1]
    print("Error: --csv <filename> is required")
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if "--serve" in args:
        csv_name = _get_csv_name(args)
        StagingServer(ROOT).run(private="--private" in args, csv_name=csv_name)
    else:
        csv_name = _get_csv_name(args)
        written = SiteGenerator(ROOT / "content", ROOT / "site").generate(False, csv_name)
        for filename in written:
            print(f"  wrote {filename}")
        print(f"Done — {len(written)} files written to {ROOT / 'site'}")


if __name__ == "__main__":
    main()
