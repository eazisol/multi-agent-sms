# MOD-620 M1 Verification

Run from repository root.

## Required command set

1. Alembic head via ScriptDirectory (preferred when Postgres may be unreachable):
   - `.\.venv\Scripts\python.exe -c "from alembic.config import Config; from alembic.script import ScriptDirectory; print(ScriptDirectory.from_config(Config('alembic.ini')).get_current_head())"`
2. Skip live `alembic upgrade head` if it would hang on unreachable Postgres.
3. `.\.venv\Scripts\python.exe -m pytest tests/integration/uateval -q --tb=short`
4. `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line`
5. OpenAPI path count:
   - `.\.venv\Scripts\python.exe -c "from masms_api.main import create_app; print(len(create_app().openapi()['paths']))"`
6. Meta modules include check:
   - `.\.venv\Scripts\python.exe -c "from masms_api.main import create_app; app=create_app(); print('MOD-620' in [r for r in app.routes if getattr(r,'path',None)=='/api/v1/meta'][0].endpoint()['modules'])"`
7. `npx next build` in `apps/web`

## Expected outcomes

- Migration `20260811_0036` is head; RLS policies exist on all `ua_*` tables.
- UAT tests pass for AC-001, AC-002, and AC-003.
- Full integration suite remains green.
- `/api/v1/meta` includes `MOD-620`.
- Frontend build succeeds with UAT desk route and navigation `ready: true`.
