#!/usr/bin/env python3
# __main__.py — entry point for the faes-website static site generator
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path
from faes_website.site_generator import SiteGenerator
from faes_website.staging_server import StagingServer

ROOT = Path(__file__).parent.parent


def main():
    if "--serve" in sys.argv:
        StagingServer(ROOT).run(private="--private" in sys.argv)
    else:
        written = SiteGenerator(ROOT / "content", ROOT / "site").generate()
        for filename in written:
            print(f"  wrote {filename}")
        print(f"Done — {len(written)} files written to {ROOT / 'site'}")


if __name__ == "__main__":
    main()
