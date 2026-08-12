# MOD-510 Verification

**Date:** 2026-08-12  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0031 → 20260811_0032`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/gmail -q --tb=short` | **3 passed** |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | **51 passed** |
| OpenAPI | path count via `create_app().openapi()` | **344** (was 329; +15) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-510` |
| Web build | `npx next build` (in `apps/web`) | **passed** (`/gmail` in route table) |

## Behaviors verified in tests

- Inbound idempotency by `gmail_message_id` (409 on duplicate, single thread/message)
- Draft → submit → approve → send creates `local-gmail-sim-*` approved send + outbound mapping
- Push notification idempotency by `external_event_id`

## Known limitations

- Simulated inbound/outbound only; no live Gmail API
- `credential_ref` only; no raw tokens in DB/API/audit
- Attachment import is local-stub ref
- AC-901 not obtained
