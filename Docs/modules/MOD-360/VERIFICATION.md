# MOD-360 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** Approved 2026-08-11 by workspace owner

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0021 → 20260811_0022`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/unit/agents tests/integration/agents -q --tb=short` | **24 passed** (2026-08-17; all 6 catalog codes) |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | 34 passed |
| OpenAPI | path count via `create_app().openapi()` | **223** (was 210; +13) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-360` |
| Web build | `npm run build` (in `apps/web`) | passed |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0022 (head)` |

## Behaviors verified in tests

- Definitions seed to 6 approved codes
- Every catalog agent (`query_intake_agent`, `requirements_clarifier`, `roadmap_planner`, `ticket_triage_agent`, `qa_review_assistant`, `status_report_drafter`) starts a stub run and completes with model/prompt/sources
- High-confidence stub run completes with model/prompt/sources
- Low-confidence run enters `review_required`; approve → `completed`
- Evaluation create succeeds
- Unknown `agent_code` rejected (422)
- Run list page shape includes `items` + `page`
- Live local API smoke (2026-08-17): `POST /api/v1/agent-runtime/runs` for all 6 codes returned HTTP 201 / `completed` (LangGraph adapter still stub; `output_json.stub=true`)
