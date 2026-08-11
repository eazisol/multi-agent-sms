# MOD-400 — Test Cases, Test Steps, Test Suites, Test Plans, Test Runs, Evidence, Coverage Links

**Status:** Implementation draft (M1 registry + execution + `/test-cases` desk)  
**Human Done (AC-901):** NOT obtained

## Purpose

Persist requirement-linked test cases with steps, suites, plans, runs, environment/build-bound evidence, and Must-Have coverage links.

## Honesty (M1 limits)

- No external test-runner / CI executor integration.
- Suites and plans store case/suite ID lists as JSON (lightweight composition).
- FE is list + create + approve + run + coverage summary — not a full QA studio.
- Notifications / Temporal / LangGraph wiring deferred.
- AC-901 remains blocked pending human review.

## M1 delivered

API: `/api/v1/test-cases`  
Migration: `20260811_0024`  
FE: `/test-cases`

| ID | Entity |
|---|---|
| MP-001 | `tc_cases` |
| MP-002 | `tc_steps` |
| MP-003 | `tc_suites` |
| MP-004 | `tc_plans` |
| MP-005 | `tc_runs` |
| MP-006 | `tc_evidence` |
| MP-007 | `tc_coverage_links` |

## Acceptance behavior (M1)

- **AC-001:** Coverage summary reports Must-Have covered vs uncovered requirement IDs
- **AC-002:** Approved `permission` / `negative` cases counted in coverage summary
- **AC-003:** Evidence stores `environment_code` + `build_ref` from the run

## Key rules

- Only `approved` cases may start a run
- Run transitions enforce domain matrix; completion may attach evidence
- Outbox: `testcase.case.created`, `.run.started`, `.run.completed`, `.coverage.linked`
