# F07 Tasks for Feature F07

## T01 — Add --serve flag to __main__.py
**Status**: done
**Description**: Parse sys.argv for `--serve`. If present, delegates to StagingServer. If absent, generates to `site/` as before.

## T02 — Create StagingServer class in faes_website/staging_server.py
**Status**: done
**Description**: Class that generates the site to `staging/` using `SiteGenerator`, then starts Python's built-in `http.server` on localhost:8000. Prints the URL and blocks until Ctrl-C.

## T03 — Add staging/ to .gitignore
**Status**: done
**Description**: Added `staging/` to `.gitignore` so it is never committed or deployed.

## T04 — Write tests
**Status**: done
**Description**: Added `tests/test_f07_staging.py` with 5 tests verifying staging generates to correct dir, does not touch site/, copies CSS, staging/ is gitignored, and StagingServer initializes correctly.
