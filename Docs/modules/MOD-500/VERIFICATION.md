# MOD-500 Verification

**Date:** 2026-08-12  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0030 → 20260811_0031`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/integrations -q --tb=short` | **3 passed** |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | **48 passed** |
| OpenAPI | path count via `create_app().openapi()` | **329** (was 316; +13) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-500` |
| Web build | `npx next build` (in `apps/web`) | **passed** (`/integrations` in route table) |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0031 (head)` |

## Behaviors verified in tests

- Inbox `force_fail` leaves mapping count unchanged; successful process creates mapping
- Cross-org connection GET 404; cross-org mapping list empty; audit + kernel outbox relay
- `client_secret` / `access_token` rejected; credential_ref opaque; audit redaction

## Known limitations

- Simulated relay/process only; no OAuth token exchange or live provider calls
- `ig_outbox_events` distinct from kernel `sys_outbox_messages`
- Webhook signature validation, rate limits, Temporal workers deferred
