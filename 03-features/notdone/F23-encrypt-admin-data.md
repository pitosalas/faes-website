# Feature description for feature F23
## F23 — Encrypt admin transaction data at rest in the published page
**Priority**: High
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: `admin.html` currently embeds the full grant transaction
history as plaintext JSON (`window.SECRET_ROWS`) directly in the page source.
The "Admin" button only toggles a CSS class (`admin-unlocked`) after a
client-side SHA-256 password check — the raw data is present in the HTML on
every page load, password or not, and is visible to anyone who views source
or opens dev tools, with or without knowing the password. Since `admin.html`
is generated on every build (including the public, non-`--private` build
that deploys to GitHub Pages), the full donor/nonprofit transaction history
is effectively public right now.

The site must remain a single static deploy (no backend, no separate
private build) — the admin page must exist on the public site, but the
transaction data it shows must only be recoverable by someone who knows the
password.

## Behaviour

- `admin.html` in the generated site contains no plaintext transaction data
  anywhere in its HTML/JS source — only ciphertext.
- At build time, the transaction rows (`all_rows`, currently passed to
  `rows_json`) are encrypted with a key derived from the staging/admin
  password already configured in `config.yml`.
- In the browser, entering the correct password derives the same key,
  decrypts the data client-side (via the Web Crypto `SubtleCrypto` API,
  already available in-browser — no new JS dependency), and reveals the
  admin sections exactly as today.
- Entering the wrong password fails to decrypt (authenticated encryption —
  e.g. AES-GCM's tag check) and shows "Incorrect password," same as today's
  UX. The separate SHA-256 hash-compare step is removed — a successful
  decrypt *is* the proof of a correct password.
- The chart / org-year grid / charity-totals sections (F19, F22) continue to
  work unchanged once data is decrypted client-side; only the data-loading
  step changes from "already in the DOM" to "decrypt into memory on unlock."
- No change to the `--private` staging server flow beyond what naturally
  falls out of the above (it already password-gates the whole site).

## Non-goals

- No server-side auth, no separate private deploy, no backend of any kind.
- No change to which password is used (still the single `config.yml`
  `staging.password` value, sourced from config, not hardcoded — ties into
  existing open issue about `staging_server.py`'s hardcoded `PASSWORD`).

## Files likely changed

| File | Change |
|------|--------|
| `faes_website/site_generator.py` | Encrypt `all_rows` JSON instead of passing it plain; add `cryptography` as a new dependency |
| `templates/html/admin_page.html` | Embed ciphertext + nonce instead of `rows_json` |
| `content/static/admin-unlock.js` | Derive key from entered password, decrypt via `SubtleCrypto`, drop hash-compare gate |
| `content/static/admin.js` | Read decrypted rows from the unlock step instead of `window.SECRET_ROWS` at load time |
| `pyproject.toml` | Add `cryptography` dependency |

## How to Demo
**Setup**: `uv run faes-website --serve --private`, browse to `/admin.html`.

**Steps**:
1. Load `/admin.html` directly; view page source / dev tools network+DOM.
2. Confirm no transaction dates/amounts/nonprofit names appear anywhere in
   the raw HTML or JS source — only ciphertext bytes.
3. Click "Admin", enter the wrong password — confirm "Incorrect password"
   and no data ever appears.
4. Click "Admin" again, enter the correct password — confirm all existing
   admin sections (chart, org-year grid, charity totals, grid.js table)
   populate exactly as before.

**Expected output**: Admin page fully functional after correct login;
zero plaintext transaction data present in the page at any point before
that, verifiable by reading the raw HTML response.
