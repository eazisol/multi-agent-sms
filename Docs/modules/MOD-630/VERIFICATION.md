# MOD-630 M1 Verification

Run from repository root.

## Required command set

1. Alembic head via ScriptDirectory (preferred when Postgres may be unreachable):
   - `.\.venv\Scripts\python.exe -c "from alembic.config import Config; from alembic.script import ScriptDirectory; print(ScriptDirectory.from_config(Config('alembic.ini')).get_current_head())"`
2. Skip live `alembic upgrade head` if it would hang on unreachable Postgres.
3. `.\.venv\Scripts\python.exe -m pytest tests/integration/pilot -q --tb=short`
4. `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line`
5. OpenAPI path count:
   - `.\.venv\Scripts\python.exe -c "from masms_api.main import create_app; print(len(create_app().openapi()['paths']))"`
6. Meta modules include check:
   - `.\.venv\Scripts\python.exe -c "from masms_api.main import create_app; app=create_app(); print('MOD-630' in [r for r in app.routes if getattr(r,'path',None)=='/api/v1/meta'][0].endpoint()['modules'])"`
7. `npx next build` in `apps/web`

## Expected outcomes

- Migration `20260811_0037` is head; RLS policies exist on all `pl_*` tables.
- Pilot tests pass for AC-001, AC-002, and AC-003, plus production-record gating and org isolation.
- Full integration suite remains green.
- `/api/v1/meta` includes `MOD-630`.
- Frontend build succeeds with Pilot desk route and navigation `ready: true`.
