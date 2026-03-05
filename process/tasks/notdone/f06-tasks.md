# Tasks for Feature F06 — Content schema amendments: grant type and public/private flag

## T01 — Add grant_type field to schema docs and seed grant files
**Status**: not done
**Description**: Update `content/README.md` to add `grant_type: pilot | primary` as a required field for grant content. Update `content/grants/2024-community-support.md` to include `grant_type`. Currency is XCG (Curaçao guilders) — ensure amount field reflects this in docs.

## T02 — Add public field to schema docs and all seed content files
**Status**: not done
**Description**: Update `content/README.md` to add `public: true | false` as a required field for all content types. Update all existing seed files in `content/pages/` and `content/grants/` to include `public: true`.

## T03 — Update ContentLoader to validate new fields
**Status**: not done
**Description**: Update `faes_website/content_loader.py` to validate that `public` is present on all content. For grant type content, also validate that `grant_type` is present. Raise `KeyError` with a descriptive message if either required field is missing.

## T04 — Add ContentLoader filter for private content
**Status**: not done
**Description**: Add a method `load_public(directory: Path) -> list[dict]` to `ContentLoader` that calls `load()` and returns only items where `public == True`. The generator will use this method rather than `load()` directly.

## T05 — Write tests for F06
**Status**: not done
**Description**: Update `tests/test_f02_content.py` or add `tests/test_f06_schema.py` with tests that verify:
1. A grant file missing `grant_type` raises `KeyError`
2. A content file missing `public` raises `KeyError`
3. `load_public()` excludes items with `public: false`
4. `load_public()` includes items with `public: true`
5. All seed content files pass validation (have all required fields)
