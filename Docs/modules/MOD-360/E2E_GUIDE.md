# MOD-360 — LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision

> **Implementation update (2026-08-17):** A schema-constrained OpenAI/LangGraph path is
> implemented for `query_intake_agent`. It redacts sensitive input and filters proposed tools
> and citations against server-supplied allowlists. The other five catalog agents and all runs
> without `MASMS_OPENAI_API_KEY` remain on the deterministic stub. No live-provider pass is
> claimed without an approved sandbox key and dummy data.

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

Anyone who wants to see “agents” in MASMS. QA must record this as a **stub runtime**, never as a live LLM test.

## 2. What this module is

Departmental agents have identities, prompt versions, tool policies, and runs stored in PostgreSQL. FastAPI owns state. The LangGraph adapter returns synthetic output (`stub-lg-{uuid}`) and does **not** call OpenAI or Bedrock.

Low confidence (`< 0.6` or force flag) must create **human review**.

## 3. Status honesty

| Item | Status |
|---|---|
| `/agents` read-only catalog | Implemented |
| `/agent-runs` start, status tabs, pagination | Implemented |
| Force low confidence | Implemented |
| LangGraphAdapter / live LLM | Stubbed |
| Run detail, tool/source inspector, review button | Planned (review API exists) |
| RAG context from MOD-370 | Stubbed / waived for M1 |
| PRE-AI provider contract | Blocked / pending |

Catalog codes: `query_intake_agent`, `requirements_clarifier`, `roadmap_planner`, `ticket_triage_agent`, `qa_review_assistant`, `status_report_drafter`.

## 4. Requirements and dependencies

- MVP-FR-006, MVP-NFR-008, MVP-NFR-009
- Depends on: MOD-100, MOD-120, MOD-240, MOD-350, MOD-370 (RAG waived in M1)

## 5. How to start

**AI Operations → Agents**, then **Agent Runs**. Do not put real client PII in the related-entity fields.

## 6. Screens, buttons, and files

### Agents — `/agents`

File: [`agents-desk-page.tsx`](../../../apps/web/src/components/agents-desk-page.tsx)

| Control | What happens | Status |
|---|---|---|
| Definitions list | GET `/agent-runtime/definitions` | Implemented |
| Create/edit agent | — | Planned |
| Empty / error toast | Implemented | |

### Agent Runs — `/agent-runs`

File: [`agent-runs-desk-page.tsx`](../../../apps/web/src/components/agent-runs-desk-page.tsx)

| Control | What happens | Status |
|---|---|---|
| Start run | Toggles form | Implemented |
| Agent code select | Catalog only | Implemented |
| Related entity type / id | Optional UUID generated | Implemented |
| Project id | Optional | Implemented |
| Force low confidence review | Yes/No | Implemented |
| Start | POST run; stub execution | Stubbed runtime |
| Status tabs + pagination | Implemented | |
| Review / evaluate buttons | — | Planned (API: `/runs/{id}/reviews`) |

Header **AI** button does nothing.

## 7. API, data, and automated tests

Prefix: `/api/v1/agent-runtime`  
Router: [`modules/agents/router.py`](../../../apps/api/src/masms_api/modules/agents/router.py)  
Migration: `20260811_0022`

| Method | Path |
|---|---|
| GET | `/definitions` |
| POST | `/runs` |
| GET | `/runs`, `/runs/{id}` |
| POST | `/runs/{id}/fail`, `/runs/{id}/reviews`, evaluations |

Tests: `tests/unit/agents/`, `tests/integration/agents/`

```bash
uv run pytest tests/unit/agents tests/integration/agents -q --tb=short
```

## 8. Test flows

### F-SETUP

API+web running. Optional project id.

### F-HAPPY

1. Open Agents — six catalog codes visible.
2. Agent Runs → Start run with `query_intake_agent`.
3. Force low confidence = No.
4. **Expected:** run completes or records stub output; model/prompt metadata stored.
5. Repeat with Force = Yes.
6. **Expected:** `review_required` (or equivalent), not silent auto-apply to business tables.

### F-VALIDATE

Unknown agent code via API — rejected.

### F-AUTHZ

Agents must not write `prj_*` / `crm_*` tables. Only `agr_*` + outbox/audit.

### F-TENANT

Other org cannot list runs.

### F-CONCUR

Review POST with stale run version — conflict if supported.

### F-TRANS

Fail a completed run — invalid.

### F-GATE

Low-confidence output requires a human review record. Do not treat stub text as approved SRS.

### F-TERM

Cancelled/failed runs are terminal without a defined reopen on the desk.

### F-RECOVER

Fail endpoint exists for error paths.

### F-CLEAN

Leave stub runs as examples.

## 9. Security, privacy, and approvals

- No secrets in prompts.
- Prompt-injection: related entity text is data, not instructions.
- Client data must not be used for provider training (policy; provider not connected).

## 10. Planned versus implemented

Live worker, tool allowlist enforcement against real tools, review UI, evaluations UI, pgvector context.

## 11. Related journeys

- [J-AGENT](../../testing/CROSS_MODULE_JOURNEYS.md#j-agent-stub-agent-runtime-and-knowledge)

## 12. Pass / fail checklist

| Step | Result |
|---|---|
| Catalog lists approved codes | |
| Stub run starts | |
| Forced low confidence → review_required | |
| Did not claim live LLM | |
| Agent tests run | |
