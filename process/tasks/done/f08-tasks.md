# F08 Tasks for Feature F08

## T01 — Add include_private option to SiteGenerator
**Status**: done
**Description**: Added `include_private` parameter to `generate()`. When True, uses `ContentLoader().load()` instead of `load_public()` so private pages are included.

## T02 — Add BasicAuthHandler to staging_server.py
**Status**: done
**Description**: Subclassed `SimpleHTTPRequestHandler` with `BasicAuthHandler`. Checks HTTP Basic Auth on every request. Hardwired password is `xyzzy`. Wrong/missing password returns 401 with `WWW-Authenticate` header.

## T03 — Add --private flag to StagingServer and __main__.py
**Status**: done
**Description**: `StagingServer.run()` accepts `private` bool. When True, uses `include_private=True` and `BasicAuthHandler`. `__main__.py` passes `--private` from sys.argv to `StagingServer.run()`.

## T04 — Write tests
**Status**: done
**Description**: Added `tests/test_f08_private.py` with 7 tests covering private page inclusion/exclusion and BasicAuthHandler auth logic.
