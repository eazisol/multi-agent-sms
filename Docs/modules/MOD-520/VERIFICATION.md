# MOD-520 M1 Verification

**Human Done (AC-901):** Obtained 2026-08-12 (human owner sign-off)

Run from repository root.

## Required command set

1. `alembic upgrade head`
2. `pytest tests/integration/jira/test_jira_api.py`
3. `pytest tests/integration`
4. OpenAPI path count check (example):
   - `python -c "from masms_api.main import create_app; print(len(create_app().openapi()['paths']))"`
5. Meta modules include check:
   - `python -c "from masms_api.main import create_app; import json; app=create_app(); routes=[r for r in app.routes if getattr(r,'path',None)=='/api/v1/meta']; print('MOD-520' in routes[0].endpoint()['modules'])"`
6. `npx next build --prefix apps/web`

## Expected outcomes

- Jira migration applies successfully with RLS policies on all `jr_*` tables.
- Jira integration tests pass:
  - approved-only push + retained key
  - inbound webhook conflict without internal-status mutation
  - failed comment sync visible then retried successfully
- Full integration suite remains green.
- `/api/v1/meta` includes `MOD-520`.
- Frontend build succeeds with Jira desk route and navigation entry.
