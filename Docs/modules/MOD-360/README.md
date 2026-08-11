# MOD-360 — LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision

**Status:** Implementation draft (M1 registry + stub adapter + ops desks)  
**Human Done (AC-901):** Approved 2026-08-11 by workspace owner

## Purpose

Persist approved agent definitions, prompt versions, tool policies, context profiles, runs, reviews, and evaluations in PostgreSQL. FastAPI owns mutable business state; the LangGraph adapter is a stub that does not call a live LLM.

## Honesty (M1 limits)

- Live LangGraph worker / LLM provider is **not** required for M1.
- `LangGraphAdapter` returns `stub-lg-{uuid}` run ids and synthetic structured output.
- MOD-370 RAG is waived for M1: context profiles are stored stubs only.
- Agents mutate only `agr_*` (+ outbox/audit), not other business tables.
- Frontend desks list definitions and runs — not a full agent studio.
- AC-901 human Done approved 2026-08-11 by workspace owner.

## M1 delivered

API: `/api/v1/agent-runtime`  
Migration: `20260811_0022`  
FE: `/agents`, `/agent-runs`

| ID | Entity |
|---|---|
| MP-001 | `agr_agent_definitions` |
| MP-002 | `agr_agent_runs` |
| MP-003 | `agr_prompt_versions` |
| MP-004 | `agr_tool_policies` |
| MP-005 | `agr_context_profiles` |
| MP-006 | `agr_agent_reviews` |
| MP-007 | `agr_agent_evaluations` |

## Approved agent codes

`query_intake_agent`, `requirements_clarifier`, `roadmap_planner`, `ticket_triage_agent`, `qa_review_assistant`, `status_report_drafter`

## Key rules

- Only catalog codes may start runs.
- Every run records model, prompt version, sources, tools used, output, confidence, and review flag.
- Confidence `< 0.6` (or `force_low_confidence`) → `review_required` until human review.
- Outbox events: `agent_runtime.run.started`, `.completed`, `.failed`, `.review_required`, `.reviewed`, `.evaluated`.
