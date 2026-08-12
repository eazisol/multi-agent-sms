# MOD-600 M1 Verification

**Human Done (AC-901):** Obtained 2026-08-12 (human owner sign-off)

Run from repository root.

## Required command set

1. Alembic head via ScriptDirectory (preferred when Postgres may be unreachable):
   - `.\.venv\Scripts\python.exe -c "from alembic.config import Config; from alembic.script import ScriptDirectory; print(ScriptDirectory.from_config(Config('alembic.ini')).get_current_head())"`
2. `alembic upgrade head` (note and continue if it hangs on unreachable DB)
3. `.\.venv\Scripts\python.exe -m pytest tests/integration/securityhardening -q --tb=short`
4. `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line`
5. OpenAPI path count:
   - `.\.venv\Scripts\python.exe -c "from masms_api.main import create_app; print(len(create_app().openapi()['paths']))"`
6. Meta modules include check:
   - `.\.venv\Scripts\python.exe -c "from masms_api.main import create_app; app=create_app(); print('MOD-600' in [r for r in app.routes if getattr(r,'path',None)=='/api/v1/meta'][0].endpoint()['modules'])"`
7. `npx next build` in `apps/web`

## Expected outcomes

- Migration `20260811_0034` is head; RLS policies exist on all `sh_*` tables.
- Security hardening tests pass for AC-001, AC-002, and AC-003.
- Full integration suite remains green.
- `/api/v1/meta` includes `MOD-600`.
- Frontend build succeeds with Security desk route and navigation `ready: true`.
