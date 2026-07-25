# TF23 Encrypt admin transaction data at rest in the published page

## T01 — Add `cryptography` dependency
**Status**: not done
**Description**: Add `cryptography` to `pyproject.toml` dependencies (not
`dev`, it's needed at build time). Run `uv sync`. Test: `uv run python -c
"import cryptography"` succeeds.

## T02 — Derive an AES-256-GCM key from the admin password
**Status**: not done
**Description**: In `site_generator.py`, replace `_hash_password` (SHA-256
digest used only for a hash-compare) with a key-derivation step that
produces a 32-byte AES key from the same `config.yml` `staging.password`
value (e.g. SHA-256 of the password bytes, used directly as the AES-256
key — no separate hash needs to travel to the browser anymore).
Test: unit test that the same password always derives the same key, and two
different passwords derive different keys.

## T03 — Encrypt `all_rows` at build time
**Status**: not done
**Description**: Replace the plain `rows_json=json.dumps(all_rows)` passed
to `admin_page.html` with AES-256-GCM ciphertext + nonce (both base64-encoded
for embedding in HTML/JS), encrypted under the key from T02. Pass both values
to the template instead of `rows_json`.
Test: generator test asserts the rendered `admin.html` contains no
substring from the known transaction data (e.g. a nonprofit name or amount
from the test fixture CSV) anywhere in its output, and does contain the new
ciphertext/nonce template variables.

## T04 — Update `admin_page.html` to embed ciphertext instead of plaintext
**Status**: not done
**Description**: Replace `window.SECRET_ROWS = {{ rows_json | safe }}` with
something like `window.ENCRYPTED_ROWS = "{{ ciphertext_b64 }}"; window.ROWS_NONCE
= "{{ nonce_b64 }}";`. Keep `window.SECRET_YEARS` as-is (year labels alone
aren't sensitive — confirm this with the user before assuming it, since it's
a judgment call, not confirm silently).
Test: generator test (extends T03's test) checks the specific new global
variable names appear in the rendered HTML.

## T05 — Decrypt client-side on password entry
**Status**: not done
**Description**: In `admin-unlock.js`, on password submit: derive the AES
key from the entered password the same way T02 does server-side (SHA-256 of
password bytes, imported as a `SubtleCrypto` AES-GCM key), then call
`crypto.subtle.decrypt` on `window.ENCRYPTED_ROWS` using `window.ROWS_NONCE`
as the IV. On success, store decrypted rows (parsed JSON) somewhere
`admin.js` can read (e.g. `window.SECRET_ROWS`, so `admin.js` needs no
changes) and unlock the UI as today. On failure (decrypt throws), show
"Incorrect password" and leave the UI locked — remove the old separate
SHA-256 hash-compare code path entirely.
Test: manual browser test only — `SubtleCrypto` isn't available in the
pytest/Python test environment. Record command, setup, expected observation,
actual result in this task's status once run.

## T06 — Update `admin.js` if needed
**Status**: not done
**Description**: Confirm `admin.js` reads transaction rows lazily (only
after unlock triggers population), not at module/script-load time, since
`window.SECRET_ROWS` no longer exists until T05's decrypt succeeds. Adjust
any code that currently assumes `SECRET_ROWS` is present at page load.
Test: manual browser test — page loads with no console errors before
password entry, and grids populate correctly after.

## T07 — Remove hardcoded staging password, source from config everywhere
**Status**: not done
**Description**: `staging_server.py`'s hardcoded `PASSWORD = "xyzzy"` must
be replaced with the same `config.yml` `staging.password` value used for
key derivation in T02, so there's exactly one password defined in one place.
Test: existing staging-server tests updated/added to assert the server reads
the password from config, not a hardcoded constant.

## T08 — Full regression pass
**Status**: not done
**Description**: Run `uv run pytest` — all existing tests (F19 chart, F22
charity totals, F03/F07/F08 generator/staging/private tests) must still
pass with the new encrypted data path. Manually verify the demo steps in
F23's "How to Demo" section end-to-end in a browser.
Test: `uv run pytest` exits 0; manual demo steps recorded with actual
result.

## T09 — Write/update tests (required)
**Status**: not done
**Description**: Consolidate the automated tests from T01–T04, T07 into the
test suite (e.g. `tests/test_f23_encrypt_admin_data.py`), covering: no
plaintext leakage in generated `admin.html`, ciphertext/nonce present,
key derivation determinism, config-sourced password in staging server.
Document in this file which parts (T05, T06, T08 browser checks) remain
manual-only and why (no `SubtleCrypto` in the Python test environment).
