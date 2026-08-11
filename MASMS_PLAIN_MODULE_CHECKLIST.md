# MASMS Plain Module Checklist

Easy view of the implementation plan: **Module -> Main task -> Sub-task**.

Sources: `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md` · status also tracked in
`MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md` and `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md`.

## How to read this

```
Module N: MOD-xxx Title
  M1: [ ] Main task group (example: API)
       M1-1: [ ] First sub-task
       M1-2: [ ] Second sub-task
```

| Mark | Meaning |
|---|---|
| `[x]` | Done |
| `[~]` | Partial |
| `[-]` | Not needed for current stub / deferred by design |
| `[!]` | Blocked (needs human or external dependency) |
| `[ ]` | Not started |

Plan IDs (like `MOD-000-API-001`) are shown in parentheses for traceability.

## Scoreboard

| # | Module | Status | Done | Partial | Open |
|---:|---|---|---:|---:|---:|
| 1 | MOD-000 | In progress (human approval blocked) | 25 | 11 | 0 |
| 2 | MOD-010 | Blocked | 16 | 0 | 0 |
| 3 | MOD-020 | Blocked | 23 | 13 | 8 |
| 4 | MOD-030 | Blocked | 14 | 2 | 0 |
| 5 | MOD-040 | Blocked | 25 | 9 | 0 |
| 6 | MOD-100 | Blocked | 31 | 9 | 0 |
| 7 | MOD-110 | Blocked | 26 | 8 | 0 |
| 8 | MOD-120 | Blocked | 30 | 6 | 0 |
| 9 | MOD-130 | Blocked | 30 | 6 | 0 |
| 10 | MOD-140 | Blocked | 31 | 8 | 0 |
| 11 | MOD-200 | Blocked | 27 | 7 | 0 |
| 12 | MOD-210 | Blocked | 27 | 8 | 0 |
| 13 | MOD-220 | Blocked | 27 | 8 | 0 |
| 14 | MOD-230 | Blocked | 27 | 8 | 0 |
| 15 | MOD-240 | Not started | 0 | 0 | 47 |
| 16 | MOD-250 | Not started | 0 | 0 | 45 |
| 17 | MOD-260 | Not started | 0 | 0 | 43 |
| 18 | MOD-300 | Not started | 0 | 0 | 45 |
| 19 | MOD-310 | Not started | 0 | 0 | 41 |
| 20 | MOD-320 | Not started | 0 | 0 | 43 |
| 21 | MOD-330 | Not started | 0 | 0 | 45 |
| 22 | MOD-340 | Not started | 0 | 0 | 45 |
| 23 | MOD-350 | Not started | 0 | 0 | 43 |
| 24 | MOD-360 | Not started | 0 | 0 | 45 |
| 25 | MOD-370 | Not started | 0 | 0 | 45 |
| 26 | MOD-400 | Not started | 0 | 0 | 45 |
| 27 | MOD-410 | Not started | 0 | 0 | 45 |
| 28 | MOD-420 | Not started | 0 | 0 | 43 |
| 29 | MOD-430 | Not started | 0 | 0 | 47 |
| 30 | MOD-440 | Not started | 0 | 0 | 45 |
| 31 | MOD-450 | Not started | 0 | 0 | 45 |
| 32 | MOD-460 | Not started | 0 | 0 | 43 |
| 33 | MOD-500 | Not started | 0 | 0 | 45 |
| 34 | MOD-510 | Not started | 0 | 0 | 45 |
| 35 | MOD-520 | Not started | 0 | 0 | 45 |
| 36 | MOD-600 | Not started | 0 | 0 | 47 |
| 37 | MOD-610 | Not started | 0 | 0 | 45 |
| 38 | MOD-620 | Not started | 0 | 0 | 43 |
| 39 | MOD-630 | Not started | 0 | 0 | 47 |

**All tasks:** 1749 · done 359 · partial 103 · n/a 148 · blocked 14 · open 1125

## Phase 0 - Governance and Foundation

### Module 1: [!] MOD-000 — Project Governance, Source Baseline, and Change Control

M1: [x] Main goals
     M1-1: [x] Build and verify: baseline register  (MOD-000-MP-001)
     M1-2: [x] Build and verify: requirement mapping  (MOD-000-MP-002)
     M1-3: [x] Build and verify: architecture decision records  (MOD-000-MP-003)
     M1-4: [x] Build and verify: change requests  (MOD-000-MP-004)
     M1-5: [x] Build and verify: approval records  (MOD-000-MP-005)

M2: [x] Database
     M2-1: [x] Design and migrate data for: baseline register  (MOD-000-DB-001)
     M2-2: [x] Design and migrate data for: requirement mapping  (MOD-000-DB-002)
     M2-3: [x] Design and migrate data for: architecture decision records  (MOD-000-DB-003)
     M2-4: [x] Design and migrate data for: change requests  (MOD-000-DB-004)
     M2-5: [x] Design and migrate data for: approval records  (MOD-000-DB-005)

M3: [x] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-000-BE-001)
     M3-2: [x] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-000-BE-002)
     M3-3: [-] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-000-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-000-BE-004)

M4: [x] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-000-API-001)
     M4-2: [x] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-000-API-002)
     M4-3: [x] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-000-API-003)

M5: [~] Frontend
     M5-1: [~] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-000-FE-001)
     M5-2: [~] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-000-FE-002)
     M5-3: [x] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-000-FE-003)
     M5-4: [~] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-000-FE-004)

M6: [x] Workflow / agents / events
     M6-1: [x] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-000-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-000-WF-002)
     M6-3: [x] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-000-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-000-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-000-SEC-001)
     M7-2: [~] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-000-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-000-SEC-003)
     M7-4: [~] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-000-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-000-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-000-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-000-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-000-QA-004)
     M8-5: [~] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-000-QA-005)

M9: [~] Docs
     M9-1: [~] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-000-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-000-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [~] One approved source of truth is identified.  (MOD-000-AC-001)
     M10-2: [x] Material changes require a new version and human approval.  (MOD-000-AC-002)
     M10-3: [x] Every implementation task maps to a module and requirement ID.  (MOD-000-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-000-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-000-AC-901)

### Module 2: [!] MOD-010 — Repository, Toolchain, and Local Development Environment

M1: [x] Main goals
     M1-1: [x] Build and verify: monorepo structure  (MOD-010-MP-001)
     M1-2: [x] Build and verify: language versions  (MOD-010-MP-002)
     M1-3: [x] Build and verify: package managers  (MOD-010-MP-003)
     M1-4: [x] Build and verify: Docker Compose  (MOD-010-MP-004)
     M1-5: [x] Build and verify: formatting and linting  (MOD-010-MP-005)
     M1-6: [x] Build and verify: typing  (MOD-010-MP-006)
     M1-7: [x] Build and verify: tests  (MOD-010-MP-007)
     M1-8: [x] Build and verify: CI build  (MOD-010-MP-008)

M2: [~] Database
     M2-1: [-] Design and migrate data for: monorepo structure  (MOD-010-DB-001)
     M2-2: [-] Design and migrate data for: language versions  (MOD-010-DB-002)
     M2-3: [-] Design and migrate data for: package managers  (MOD-010-DB-003)
     M2-4: [-] Design and migrate data for: Docker Compose  (MOD-010-DB-004)
     M2-5: [-] Design and migrate data for: formatting and linting  (MOD-010-DB-005)
     M2-6: [-] Design and migrate data for: typing  (MOD-010-DB-006)
     M2-7: [-] Design and migrate data for: tests  (MOD-010-DB-007)
     M2-8: [-] Design and migrate data for: CI build  (MOD-010-DB-008)

M3: [~] Backend
     M3-1: [-] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-010-BE-001)
     M3-2: [-] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-010-BE-002)
     M3-3: [-] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-010-BE-003)
     M3-4: [-] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-010-BE-004)

M4: [~] API
     M4-1: [-] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-010-API-001)
     M4-2: [-] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-010-API-002)
     M4-3: [-] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-010-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-010-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-010-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-010-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-010-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-010-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-010-WF-002)
     M6-3: [-] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-010-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-010-WF-004)

M7: [x] Security / audit
     M7-1: [-] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-010-SEC-001)
     M7-2: [-] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-010-SEC-002)
     M7-3: [x] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-010-SEC-003)
     M7-4: [-] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-010-SEC-004)

M8: [x] Testing
     M8-1: [-] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-010-QA-001)
     M8-2: [-] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-010-QA-002)
     M8-3: [-] Add role-permission negative tests and tenant/project isolation tests.  (MOD-010-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-010-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-010-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-010-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-010-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [x] A new developer can start the stack from documented commands.  (MOD-010-AC-001)
     M10-2: [x] CI blocks formatting, type, test, or build failures.  (MOD-010-AC-002)
     M10-3: [x] No real secret exists in source control.  (MOD-010-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-010-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-010-AC-901)

### Module 3: [!] MOD-020 — Shared Architecture, Domain Kernel, and API Standards

M1: [x] Main goals
     M1-1: [x] Build and verify: typed identifiers  (MOD-020-MP-001)
     M1-2: [x] Build and verify: actor context  (MOD-020-MP-002)
     M1-3: [x] Build and verify: tenant context  (MOD-020-MP-003)
     M1-4: [x] Build and verify: domain errors  (MOD-020-MP-004)
     M1-5: [x] Build and verify: unit of work  (MOD-020-MP-005)
     M1-6: [x] Build and verify: outbox  (MOD-020-MP-006)
     M1-7: [x] Build and verify: API problem details  (MOD-020-MP-007)
     M1-8: [x] Build and verify: pagination  (MOD-020-MP-008)
     M1-9: [x] Build and verify: optimistic concurrency  (MOD-020-MP-009)

M2: [x] Database
     M2-1: [x] Design and migrate data for: typed identifiers  (MOD-020-DB-001)
     M2-2: [x] Design and migrate data for: actor context  (MOD-020-DB-002)
     M2-3: [x] Design and migrate data for: tenant context  (MOD-020-DB-003)
     M2-4: [x] Design and migrate data for: domain errors  (MOD-020-DB-004)
     M2-5: [x] Design and migrate data for: unit of work  (MOD-020-DB-005)
     M2-6: [x] Design and migrate data for: outbox  (MOD-020-DB-006)
     M2-7: [x] Design and migrate data for: API problem details  (MOD-020-DB-007)
     M2-8: [x] Design and migrate data for: pagination  (MOD-020-DB-008)
     M2-9: [x] Design and migrate data for: optimistic concurrency  (MOD-020-DB-009)

M3: [~] Backend
     M3-1: [~] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-020-BE-001)
     M3-2: [~] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-020-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-020-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-020-BE-004)

M4: [~] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-020-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-020-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-020-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-020-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-020-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-020-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-020-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-020-WF-001)
     M6-2: [~] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-020-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-020-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-020-WF-004)

M7: [~] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-020-SEC-001)
     M7-2: [~] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-020-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-020-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-020-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-020-QA-001)
     M8-2: [~] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-020-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-020-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-020-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-020-QA-005)

M9: [~] Docs
     M9-1: [~] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-020-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-020-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [~] All modules use the same actor and tenant context.  (MOD-020-AC-001)
     M10-2: [~] Agents and workflows cannot bypass application services.  (MOD-020-AC-002)
     M10-3: [~] API contracts are consistent and documented.  (MOD-020-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-020-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-020-AC-901)

### Module 4: [!] MOD-030 — Environment Configuration, Secrets, CI/CD, and Deployment Skeleton

M1: [x] Main goals
     M1-1: [x] Build and verify: environment matrix  (MOD-030-MP-001)
     M1-2: [x] Build and verify: secret manager  (MOD-030-MP-002)
     M1-3: [x] Build and verify: CI pipelines  (MOD-030-MP-003)
     M1-4: [x] Build and verify: staging deployment  (MOD-030-MP-004)
     M1-5: [x] Build and verify: production approval placeholder  (MOD-030-MP-005)
     M1-6: [x] Build and verify: infrastructure as code  (MOD-030-MP-006)

M2: [~] Database
     M2-1: [-] Design and migrate data for: environment matrix  (MOD-030-DB-001)
     M2-2: [-] Design and migrate data for: secret manager  (MOD-030-DB-002)
     M2-3: [-] Design and migrate data for: CI pipelines  (MOD-030-DB-003)
     M2-4: [-] Design and migrate data for: staging deployment  (MOD-030-DB-004)
     M2-5: [-] Design and migrate data for: production approval placeholder  (MOD-030-DB-005)
     M2-6: [-] Design and migrate data for: infrastructure as code  (MOD-030-DB-006)

M3: [~] Backend
     M3-1: [-] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-030-BE-001)
     M3-2: [-] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-030-BE-002)
     M3-3: [-] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-030-BE-003)
     M3-4: [-] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-030-BE-004)

M4: [~] API
     M4-1: [-] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-030-API-001)
     M4-2: [-] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-030-API-002)
     M4-3: [-] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-030-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-030-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-030-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-030-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-030-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-030-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-030-WF-002)
     M6-3: [-] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-030-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-030-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-030-SEC-001)
     M7-2: [-] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-030-SEC-002)
     M7-3: [x] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-030-SEC-003)
     M7-4: [-] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-030-SEC-004)

M8: [x] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-030-QA-001)
     M8-2: [-] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-030-QA-002)
     M8-3: [-] Add role-permission negative tests and tenant/project isolation tests.  (MOD-030-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-030-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-030-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-030-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-030-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [~] Environment credentials are isolated.  (MOD-030-AC-001)
     M10-2: [x] Production release requires human authorization.  (MOD-030-AC-002)
     M10-3: [x] Artifacts are reproducible and traceable.  (MOD-030-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-030-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-030-AC-901)

### Module 5: [!] MOD-040 — Observability, Audit Foundation, and Operational Health

M1: [x] Main goals
     M1-1: [x] Build and verify: audit logs  (MOD-040-MP-001)
     M1-2: [x] Build and verify: activity events  (MOD-040-MP-002)
     M1-3: [x] Build and verify: status history  (MOD-040-MP-003)
     M1-4: [x] Build and verify: agent runs  (MOD-040-MP-004)
     M1-5: [x] Build and verify: integration events  (MOD-040-MP-005)
     M1-6: [x] Build and verify: OpenTelemetry  (MOD-040-MP-006)
     M1-7: [x] Build and verify: health checks  (MOD-040-MP-007)

M2: [x] Database
     M2-1: [x] Design and migrate data for: audit logs  (MOD-040-DB-001)
     M2-2: [x] Design and migrate data for: activity events  (MOD-040-DB-002)
     M2-3: [x] Design and migrate data for: status history  (MOD-040-DB-003)
     M2-4: [x] Design and migrate data for: agent runs  (MOD-040-DB-004)
     M2-5: [x] Design and migrate data for: integration events  (MOD-040-DB-005)
     M2-6: [-] Design and migrate data for: OpenTelemetry  (MOD-040-DB-006)
     M2-7: [-] Design and migrate data for: health checks  (MOD-040-DB-007)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-040-BE-001)
     M3-2: [~] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-040-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-040-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-040-BE-004)

M4: [~] API
     M4-1: [~] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-040-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-040-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-040-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-040-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-040-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-040-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-040-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-040-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-040-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-040-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-040-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-040-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-040-SEC-002)
     M7-3: [x] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-040-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-040-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-040-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-040-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-040-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-040-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-040-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-040-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-040-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [~] Every controlled action is attributable to an actor.  (MOD-040-AC-001)
     M10-2: [x] Audit records are append-only for operational roles.  (MOD-040-AC-002)
     M10-3: [x] Failures are diagnosable without revealing secrets.  (MOD-040-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-040-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-040-AC-901)

## Phase 1 - Identity, Organization, and Configuration

### Module 6: [!] MOD-100 — Organizations, Actors, Human Users, Agents, Teams, and Departments

M1: [x] Main goals
     M1-1: [x] Build and verify: organizations  (MOD-100-MP-001)
     M1-2: [x] Build and verify: actors  (MOD-100-MP-002)
     M1-3: [x] Build and verify: human users  (MOD-100-MP-003)
     M1-4: [x] Build and verify: agents  (MOD-100-MP-004)
     M1-5: [x] Build and verify: roles  (MOD-100-MP-005)
     M1-6: [x] Build and verify: departments  (MOD-100-MP-006)
     M1-7: [x] Build and verify: teams  (MOD-100-MP-007)
     M1-8: [x] Build and verify: team members  (MOD-100-MP-008)
     M1-9: [x] Build and verify: reporting lines  (MOD-100-MP-009)

M2: [x] Database
     M2-1: [x] Design and migrate data for: organizations  (MOD-100-DB-001)
     M2-2: [x] Design and migrate data for: actors  (MOD-100-DB-002)
     M2-3: [x] Design and migrate data for: human users  (MOD-100-DB-003)
     M2-4: [x] Design and migrate data for: agents  (MOD-100-DB-004)
     M2-5: [x] Design and migrate data for: roles  (MOD-100-DB-005)
     M2-6: [x] Design and migrate data for: departments  (MOD-100-DB-006)
     M2-7: [x] Design and migrate data for: teams  (MOD-100-DB-007)
     M2-8: [x] Design and migrate data for: team members  (MOD-100-DB-008)
     M2-9: [x] Design and migrate data for: reporting lines  (MOD-100-DB-009)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-100-BE-001)
     M3-2: [~] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-100-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-100-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-100-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-100-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-100-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-100-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-100-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-100-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-100-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-100-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-100-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-100-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-100-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-100-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-100-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-100-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-100-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-100-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-100-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-100-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-100-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-100-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-100-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-100-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-100-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [~] Every action and owner resolves to one actor.  (MOD-100-AC-001)
     M10-2: [x] Every operational agent has an active human supervisor.  (MOD-100-AC-002)
     M10-3: [x] Agent and human identities are separate.  (MOD-100-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-100-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-100-AC-901)

### Module 7: [!] MOD-110 — Authentication, Sessions, MFA, and Account Security

M1: [x] Main goals
     M1-1: [x] Build and verify: identity provider  (MOD-110-MP-001)
     M1-2: [x] Build and verify: token validation  (MOD-110-MP-002)
     M1-3: [x] Build and verify: sessions  (MOD-110-MP-003)
     M1-4: [x] Build and verify: MFA  (MOD-110-MP-004)
     M1-5: [x] Build and verify: step-up authentication  (MOD-110-MP-005)
     M1-6: [x] Build and verify: client invitations  (MOD-110-MP-006)
     M1-7: [x] Build and verify: service identities  (MOD-110-MP-007)

M2: [~] Database
     M2-1: [~] Design and migrate data for: identity provider  (MOD-110-DB-001)
     M2-2: [x] Design and migrate data for: token validation  (MOD-110-DB-002)
     M2-3: [x] Design and migrate data for: sessions  (MOD-110-DB-003)
     M2-4: [x] Design and migrate data for: MFA  (MOD-110-DB-004)
     M2-5: [~] Design and migrate data for: step-up authentication  (MOD-110-DB-005)
     M2-6: [x] Design and migrate data for: client invitations  (MOD-110-DB-006)
     M2-7: [x] Design and migrate data for: service identities  (MOD-110-DB-007)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-110-BE-001)
     M3-2: [~] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-110-BE-002)
     M3-3: [-] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-110-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-110-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-110-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-110-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-110-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-110-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-110-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-110-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-110-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-110-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-110-WF-002)
     M6-3: [-] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-110-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-110-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-110-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-110-SEC-002)
     M7-3: [x] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-110-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-110-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-110-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-110-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-110-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-110-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-110-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-110-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-110-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [~] All human and machine actions use authenticated actor identities.  (MOD-110-AC-001)
     M10-2: [x] Privileged actions require appropriate assurance.  (MOD-110-AC-002)
     M10-3: [x] Sessions can be revoked immediately.  (MOD-110-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-110-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-110-AC-901)

### Module 8: [!] MOD-120 — RBAC, Attribute-Based Access, Project Membership, and Row-Level Security

M1: [x] Main goals
     M1-1: [x] Build and verify: permissions  (MOD-120-MP-001)
     M1-2: [x] Build and verify: role permissions  (MOD-120-MP-002)
     M1-3: [x] Build and verify: project members  (MOD-120-MP-003)
     M1-4: [x] Build and verify: module access  (MOD-120-MP-004)
     M1-5: [x] Build and verify: document access  (MOD-120-MP-005)
     M1-6: [x] Build and verify: approval authorities  (MOD-120-MP-006)
     M1-7: [x] Build and verify: RLS policies  (MOD-120-MP-007)
     M1-8: [x] Build and verify: access reviews  (MOD-120-MP-008)

M2: [x] Database
     M2-1: [x] Design and migrate data for: permissions  (MOD-120-DB-001)
     M2-2: [x] Design and migrate data for: role permissions  (MOD-120-DB-002)
     M2-3: [x] Design and migrate data for: project members  (MOD-120-DB-003)
     M2-4: [x] Design and migrate data for: module access  (MOD-120-DB-004)
     M2-5: [x] Design and migrate data for: document access  (MOD-120-DB-005)
     M2-6: [x] Design and migrate data for: approval authorities  (MOD-120-DB-006)
     M2-7: [x] Design and migrate data for: RLS policies  (MOD-120-DB-007)
     M2-8: [x] Design and migrate data for: access reviews  (MOD-120-DB-008)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-120-BE-001)
     M3-2: [~] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-120-BE-002)
     M3-3: [-] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-120-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-120-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-120-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-120-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-120-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-120-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-120-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-120-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-120-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-120-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-120-WF-002)
     M6-3: [-] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-120-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-120-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-120-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-120-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-120-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-120-SEC-004)

M8: [x] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-120-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-120-QA-002)
     M8-3: [x] Add role-permission negative tests and tenant/project isolation tests.  (MOD-120-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-120-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-120-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-120-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-120-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [~] No cross-client access exists through API, database, files, cache, vectors, search, or exports.  (MOD-120-AC-001)
     M10-2: [x] Project access requires valid membership or explicit authority.  (MOD-120-AC-002)
     M10-3: [x] Frontend visibility never replaces backend authorization.  (MOD-120-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-120-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-120-AC-901)

### Module 9: [!] MOD-130 — Skills, Availability, Capacity, Working Hours, and Business Calendars

M1: [x] Main goals
     M1-1: [x] Build and verify: skills  (MOD-130-MP-001)
     M1-2: [x] Build and verify: actor skills  (MOD-130-MP-002)
     M1-3: [x] Build and verify: availability  (MOD-130-MP-003)
     M1-4: [x] Build and verify: capacity allocations  (MOD-130-MP-004)
     M1-5: [x] Build and verify: business calendars  (MOD-130-MP-005)
     M1-6: [x] Build and verify: holidays  (MOD-130-MP-006)
     M1-7: [x] Build and verify: leave periods  (MOD-130-MP-007)
     M1-8: [x] Build and verify: on-call schedules  (MOD-130-MP-008)

M2: [x] Database
     M2-1: [x] Design and migrate data for: skills  (MOD-130-DB-001)
     M2-2: [x] Design and migrate data for: actor skills  (MOD-130-DB-002)
     M2-3: [x] Design and migrate data for: availability  (MOD-130-DB-003)
     M2-4: [x] Design and migrate data for: capacity allocations  (MOD-130-DB-004)
     M2-5: [x] Design and migrate data for: business calendars  (MOD-130-DB-005)
     M2-6: [x] Design and migrate data for: holidays  (MOD-130-DB-006)
     M2-7: [x] Design and migrate data for: leave periods  (MOD-130-DB-007)
     M2-8: [x] Design and migrate data for: on-call schedules  (MOD-130-DB-008)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-130-BE-001)
     M3-2: [~] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-130-BE-002)
     M3-3: [-] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-130-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-130-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-130-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-130-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-130-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-130-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-130-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-130-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-130-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-130-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-130-WF-002)
     M6-3: [-] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-130-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-130-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-130-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-130-SEC-002)
     M7-3: [x] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-130-SEC-003)
     M7-4: [~] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-130-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-130-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-130-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-130-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-130-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-130-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-130-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-130-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [x] Assignments can evaluate skill, access, capacity, calendar, and deadline.  (MOD-130-AC-001)
     M10-2: [x] SLA calculations respect business calendars and time zones.  (MOD-130-AC-002)
     M10-3: [x] Unnecessary personal data is excluded.  (MOD-130-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-130-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-130-AC-901)

### Module 10: [!] MOD-140 — Configuration Administration and Versioned Operational Rules

M1: [x] Main goals
     M1-1: [x] Build and verify: workflow definitions  (MOD-140-MP-001)
     M1-2: [x] Build and verify: status definitions  (MOD-140-MP-002)
     M1-3: [x] Build and verify: transition rules  (MOD-140-MP-003)
     M1-4: [x] Build and verify: follow-up rules  (MOD-140-MP-004)
     M1-5: [x] Build and verify: reminder rules  (MOD-140-MP-005)
     M1-6: [x] Build and verify: escalation rules  (MOD-140-MP-006)
     M1-7: [x] Build and verify: approval workflows  (MOD-140-MP-007)
     M1-8: [x] Build and verify: configuration versions  (MOD-140-MP-008)

M2: [x] Database
     M2-1: [x] Design and migrate data for: workflow definitions  (MOD-140-DB-001)
     M2-2: [x] Design and migrate data for: status definitions  (MOD-140-DB-002)
     M2-3: [x] Design and migrate data for: transition rules  (MOD-140-DB-003)
     M2-4: [x] Design and migrate data for: follow-up rules  (MOD-140-DB-004)
     M2-5: [x] Design and migrate data for: reminder rules  (MOD-140-DB-005)
     M2-6: [x] Design and migrate data for: escalation rules  (MOD-140-DB-006)
     M2-7: [x] Design and migrate data for: approval workflows  (MOD-140-DB-007)
     M2-8: [x] Design and migrate data for: configuration versions  (MOD-140-DB-008)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-140-BE-001)
     M3-2: [x] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-140-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-140-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-140-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-140-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-140-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-140-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-140-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-140-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-140-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-140-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [~] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-140-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-140-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-140-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-140-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-140-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-140-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-140-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-140-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-140-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-140-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-140-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-140-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-140-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-140-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-140-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [x] Only approved effective configuration controls live execution.  (MOD-140-AC-001)
     M10-2: [x] Configuration changes require validation, audit, and rollback support.  (MOD-140-AC-002)
     M10-3: [x] Draft configuration cannot affect live workflows.  (MOD-140-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-140-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-140-AC-901)

## Phase 2 - Client, Query, and Requirement Management

### Module 11: [!] MOD-200 — Client and Contact Management

M1: [x] Main goals
     M1-1: [x] Build and verify: clients  (MOD-200-MP-001)
     M1-2: [x] Build and verify: contacts  (MOD-200-MP-002)
     M1-3: [x] Build and verify: project contacts  (MOD-200-MP-003)
     M1-4: [x] Build and verify: communication preferences  (MOD-200-MP-004)
     M1-5: [x] Build and verify: duplicate suggestions  (MOD-200-MP-005)
     M1-6: [x] Build and verify: merge history  (MOD-200-MP-006)

M2: [x] Database
     M2-1: [x] Design and migrate data for: clients  (MOD-200-DB-001)
     M2-2: [x] Design and migrate data for: contacts  (MOD-200-DB-002)
     M2-3: [x] Design and migrate data for: project contacts  (MOD-200-DB-003)
     M2-4: [x] Design and migrate data for: communication preferences  (MOD-200-DB-004)
     M2-5: [x] Design and migrate data for: duplicate suggestions  (MOD-200-DB-005)
     M2-6: [x] Design and migrate data for: merge history  (MOD-200-DB-006)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-200-BE-001)
     M3-2: [~] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-200-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-200-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-200-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-200-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-200-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-200-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-200-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-200-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-200-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-200-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [-] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-200-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-200-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-200-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-200-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-200-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-200-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-200-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-200-SEC-004)

M8: [x] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-200-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-200-QA-002)
     M8-3: [x] Add role-permission negative tests and tenant/project isolation tests.  (MOD-200-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-200-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-200-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-200-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-200-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [x] Clients may have multiple contacts with explicit authority.  (MOD-200-AC-001)
     M10-2: [x] Duplicate handling preserves history.  (MOD-200-AC-002)
     M10-3: [x] Client records are isolated and auditable.  (MOD-200-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-200-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-200-AC-901)

### Module 12: [!] MOD-210 — Client Queries, Qualification, and Opportunities

M1: [x] Main goals
     M1-1: [x] Build and verify: queries  (MOD-210-MP-001)
     M1-2: [x] Build and verify: opportunities  (MOD-210-MP-002)
     M1-3: [x] Build and verify: qualification answers  (MOD-210-MP-003)
     M1-4: [x] Build and verify: query sources  (MOD-210-MP-004)
     M1-5: [x] Build and verify: query status history  (MOD-210-MP-005)
     M1-6: [x] Build and verify: first response SLA  (MOD-210-MP-006)

M2: [x] Database
     M2-1: [x] Design and migrate data for: queries  (MOD-210-DB-001)
     M2-2: [x] Design and migrate data for: opportunities  (MOD-210-DB-002)
     M2-3: [x] Design and migrate data for: qualification answers  (MOD-210-DB-003)
     M2-4: [x] Design and migrate data for: query sources  (MOD-210-DB-004)
     M2-5: [x] Design and migrate data for: query status history  (MOD-210-DB-005)
     M2-6: [x] Design and migrate data for: first response SLA  (MOD-210-DB-006)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-210-BE-001)
     M3-2: [x] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-210-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-210-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-210-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-210-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-210-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-210-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-210-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-210-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-210-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-210-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [~] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-210-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-210-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-210-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-210-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-210-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-210-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-210-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-210-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-210-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-210-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-210-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-210-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-210-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-210-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-210-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [x] Each valid inquiry creates one traceable query.  (MOD-210-AC-001)
     M10-2: [x] Qualification is reviewable and explainable.  (MOD-210-AC-002)
     M10-3: [x] Conversion preserves communication, documents, follow-ups, and decisions.  (MOD-210-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-210-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-210-AC-901)

### Module 13: [!] MOD-220 — Conversations, Messages, Attachments, and Communication History

M1: [x] Main goals
     M1-1: [x] Build and verify: conversations  (MOD-220-MP-001)
     M1-2: [x] Build and verify: messages  (MOD-220-MP-002)
     M1-3: [x] Build and verify: message revisions  (MOD-220-MP-003)
     M1-4: [x] Build and verify: recipients  (MOD-220-MP-004)
     M1-5: [x] Build and verify: delivery receipts  (MOD-220-MP-005)
     M1-6: [x] Build and verify: attachment links  (MOD-220-MP-006)

M2: [x] Database
     M2-1: [x] Design and migrate data for: conversations  (MOD-220-DB-001)
     M2-2: [x] Design and migrate data for: messages  (MOD-220-DB-002)
     M2-3: [x] Design and migrate data for: message revisions  (MOD-220-DB-003)
     M2-4: [x] Design and migrate data for: recipients  (MOD-220-DB-004)
     M2-5: [x] Design and migrate data for: delivery receipts  (MOD-220-DB-005)
     M2-6: [x] Design and migrate data for: attachment links  (MOD-220-DB-006)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-220-BE-001)
     M3-2: [x] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-220-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-220-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-220-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-220-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-220-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-220-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-220-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-220-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-220-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-220-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [~] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-220-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-220-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-220-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-220-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-220-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-220-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-220-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-220-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-220-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-220-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-220-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-220-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-220-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-220-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-220-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [x] Material communication is linked to the correct entity.  (MOD-220-AC-001)
     M10-2: [x] Sensitive messages follow approval and recipient rules.  (MOD-220-AC-002)
     M10-3: [x] Sent-message history is immutable.  (MOD-220-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-220-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-220-AC-901)

### Module 14: [!] MOD-230 — Requirement Gathering, Completeness Analysis, Clarifications, and Requirement Brief

M1: [x] Main goals
     M1-1: [x] Build and verify: questionnaires  (MOD-230-MP-001)
     M1-2: [x] Build and verify: questionnaire versions  (MOD-230-MP-002)
     M1-3: [x] Build and verify: answers  (MOD-230-MP-003)
     M1-4: [x] Build and verify: requirement briefs  (MOD-230-MP-004)
     M1-5: [x] Build and verify: clarification requests  (MOD-230-MP-005)
     M1-6: [x] Build and verify: completeness scoring  (MOD-230-MP-006)

M2: [x] Database
     M2-1: [x] Design and migrate data for: questionnaires  (MOD-230-DB-001)
     M2-2: [x] Design and migrate data for: questionnaire versions  (MOD-230-DB-002)
     M2-3: [x] Design and migrate data for: answers  (MOD-230-DB-003)
     M2-4: [x] Design and migrate data for: requirement briefs  (MOD-230-DB-004)
     M2-5: [x] Design and migrate data for: clarification requests  (MOD-230-DB-005)
     M2-6: [x] Design and migrate data for: completeness scoring  (MOD-230-DB-006)

M3: [~] Backend
     M3-1: [x] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-230-BE-001)
     M3-2: [x] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-230-BE-002)
     M3-3: [~] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-230-BE-003)
     M3-4: [x] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-230-BE-004)

M4: [~] API
     M4-1: [x] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-230-API-001)
     M4-2: [~] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-230-API-002)
     M4-3: [~] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-230-API-003)

M5: [~] Frontend
     M5-1: [-] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-230-FE-001)
     M5-2: [-] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-230-FE-002)
     M5-3: [-] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-230-FE-003)
     M5-4: [-] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-230-FE-004)

M6: [~] Workflow / agents / events
     M6-1: [~] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-230-WF-001)
     M6-2: [-] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-230-WF-002)
     M6-3: [~] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-230-WF-003)
     M6-4: [-] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-230-WF-004)

M7: [~] Security / audit
     M7-1: [~] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-230-SEC-001)
     M7-2: [x] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-230-SEC-002)
     M7-3: [~] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-230-SEC-003)
     M7-4: [x] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-230-SEC-004)

M8: [~] Testing
     M8-1: [x] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-230-QA-001)
     M8-2: [x] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-230-QA-002)
     M8-3: [~] Add role-permission negative tests and tenant/project isolation tests.  (MOD-230-QA-003)
     M8-4: [-] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-230-QA-004)
     M8-5: [x] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-230-QA-005)

M9: [x] Docs
     M9-1: [x] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-230-DOC-001)
     M9-2: [x] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-230-DOC-002)

M10: [!] Acceptance / Done gate
     M10-1: [x] At least 95% of mandatory fields are answered or explicitly unavailable.  (MOD-230-AC-001)
     M10-2: [x] Unanswered mandatory items have an owner or follow-up.  (MOD-230-AC-002)
     M10-3: [x] The brief is versioned and human-approved.  (MOD-230-AC-003)
     M10-4: [x] All Critical and High defects for this module are resolved.  (MOD-230-AC-900)
     M10-5: [!] The responsible human owner reviews and approves the completion evidence.  (MOD-230-AC-901)

### Module 15: [ ] MOD-240 — Projects, Requirements, Requirement Versions, and SRS Management

M1: [ ] Main goals
     M1-1: [ ] Build and verify: projects  (MOD-240-MP-001)
     M1-2: [ ] Build and verify: requirements  (MOD-240-MP-002)
     M1-3: [ ] Build and verify: requirement versions  (MOD-240-MP-003)
     M1-4: [ ] Build and verify: business rules  (MOD-240-MP-004)
     M1-5: [ ] Build and verify: acceptance criteria  (MOD-240-MP-005)
     M1-6: [ ] Build and verify: assumptions  (MOD-240-MP-006)
     M1-7: [ ] Build and verify: constraints  (MOD-240-MP-007)
     M1-8: [ ] Build and verify: SRS baselines  (MOD-240-MP-008)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: projects  (MOD-240-DB-001)
     M2-2: [ ] Design and migrate data for: requirements  (MOD-240-DB-002)
     M2-3: [ ] Design and migrate data for: requirement versions  (MOD-240-DB-003)
     M2-4: [ ] Design and migrate data for: business rules  (MOD-240-DB-004)
     M2-5: [ ] Design and migrate data for: acceptance criteria  (MOD-240-DB-005)
     M2-6: [ ] Design and migrate data for: assumptions  (MOD-240-DB-006)
     M2-7: [ ] Design and migrate data for: constraints  (MOD-240-DB-007)
     M2-8: [ ] Design and migrate data for: SRS baselines  (MOD-240-DB-008)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-240-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-240-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-240-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-240-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-240-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-240-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-240-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-240-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-240-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-240-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-240-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-240-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-240-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-240-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-240-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-240-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-240-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-240-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-240-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-240-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-240-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-240-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-240-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-240-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-240-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-240-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Every approved requirement has a unique ID and acceptance criteria.  (MOD-240-AC-001)
     M10-2: [ ] SRS cannot become authoritative without human approval.  (MOD-240-AC-002)
     M10-3: [ ] Material changes create new versions and change control.  (MOD-240-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-240-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-240-AC-901)

### Module 16: [ ] MOD-250 — Documents, Standard Templates, Versioning, and Secure File Storage

M1: [ ] Main goals
     M1-1: [ ] Build and verify: documents  (MOD-250-MP-001)
     M1-2: [ ] Build and verify: document versions  (MOD-250-MP-002)
     M1-3: [ ] Build and verify: templates  (MOD-250-MP-003)
     M1-4: [ ] Build and verify: template versions  (MOD-250-MP-004)
     M1-5: [ ] Build and verify: attachments  (MOD-250-MP-005)
     M1-6: [ ] Build and verify: document permissions  (MOD-250-MP-006)
     M1-7: [ ] Build and verify: scan results  (MOD-250-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: documents  (MOD-250-DB-001)
     M2-2: [ ] Design and migrate data for: document versions  (MOD-250-DB-002)
     M2-3: [ ] Design and migrate data for: templates  (MOD-250-DB-003)
     M2-4: [ ] Design and migrate data for: template versions  (MOD-250-DB-004)
     M2-5: [ ] Design and migrate data for: attachments  (MOD-250-DB-005)
     M2-6: [ ] Design and migrate data for: document permissions  (MOD-250-DB-006)
     M2-7: [ ] Design and migrate data for: scan results  (MOD-250-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-250-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-250-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-250-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-250-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-250-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-250-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-250-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-250-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-250-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-250-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-250-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-250-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-250-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-250-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-250-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-250-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-250-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-250-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-250-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-250-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-250-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-250-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-250-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-250-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-250-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-250-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Authoritative documents have version, owner, status, and effective date.  (MOD-250-AC-001)
     M10-2: [ ] Unsafe files never become available or indexed.  (MOD-250-AC-002)
     M10-3: [ ] Access applies to files, previews, extracted text, and embeddings.  (MOD-250-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-250-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-250-AC-901)

### Module 17: [ ] MOD-260 — Project Phases, Milestones, Roadmaps, Dependencies, and Baselines

M1: [ ] Main goals
     M1-1: [ ] Build and verify: phases  (MOD-260-MP-001)
     M1-2: [ ] Build and verify: milestones  (MOD-260-MP-002)
     M1-3: [ ] Build and verify: deliverables  (MOD-260-MP-003)
     M1-4: [ ] Build and verify: phase dependencies  (MOD-260-MP-004)
     M1-5: [ ] Build and verify: project baselines  (MOD-260-MP-005)
     M1-6: [ ] Build and verify: forecasts  (MOD-260-MP-006)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: phases  (MOD-260-DB-001)
     M2-2: [ ] Design and migrate data for: milestones  (MOD-260-DB-002)
     M2-3: [ ] Design and migrate data for: deliverables  (MOD-260-DB-003)
     M2-4: [ ] Design and migrate data for: phase dependencies  (MOD-260-DB-004)
     M2-5: [ ] Design and migrate data for: project baselines  (MOD-260-DB-005)
     M2-6: [ ] Design and migrate data for: forecasts  (MOD-260-DB-006)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-260-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-260-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-260-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-260-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-260-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-260-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-260-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-260-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-260-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-260-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-260-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-260-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-260-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-260-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-260-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-260-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-260-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-260-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-260-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-260-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-260-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-260-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-260-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-260-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-260-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-260-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Every approved requirement maps to a phase.  (MOD-260-AC-001)
     M10-2: [ ] Every milestone has owner, date, status, and approval rules.  (MOD-260-AC-002)
     M10-3: [ ] Multi-phase projects support independent phase completion.  (MOD-260-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-260-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-260-AC-901)

## Phase 3 - Work Management and Agent Orchestration

### Module 18: [ ] MOD-300 — Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion

M1: [ ] Main goals
     M1-1: [ ] Build and verify: tickets  (MOD-300-MP-001)
     M1-2: [ ] Build and verify: subtasks  (MOD-300-MP-002)
     M1-3: [ ] Build and verify: ticket dependencies  (MOD-300-MP-003)
     M1-4: [ ] Build and verify: requirement links  (MOD-300-MP-004)
     M1-5: [ ] Build and verify: ticket evidence  (MOD-300-MP-005)
     M1-6: [ ] Build and verify: readiness checks  (MOD-300-MP-006)
     M1-7: [ ] Build and verify: done checks  (MOD-300-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: tickets  (MOD-300-DB-001)
     M2-2: [ ] Design and migrate data for: subtasks  (MOD-300-DB-002)
     M2-3: [ ] Design and migrate data for: ticket dependencies  (MOD-300-DB-003)
     M2-4: [ ] Design and migrate data for: requirement links  (MOD-300-DB-004)
     M2-5: [ ] Design and migrate data for: ticket evidence  (MOD-300-DB-005)
     M2-6: [ ] Design and migrate data for: readiness checks  (MOD-300-DB-006)
     M2-7: [ ] Design and migrate data for: done checks  (MOD-300-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-300-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-300-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-300-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-300-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-300-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-300-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-300-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-300-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-300-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-300-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-300-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-300-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-300-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-300-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-300-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-300-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-300-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-300-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-300-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-300-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-300-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-300-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-300-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-300-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-300-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-300-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] No ticket becomes Ready without required information.  (MOD-300-AC-001)
     M10-2: [ ] Tickets link to project, phase, owner or queue, and requirement.  (MOD-300-AC-002)
     M10-3: [ ] Done tickets reopen only with authority and evidence.  (MOD-300-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-300-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-300-AC-901)

### Module 19: [ ] MOD-310 — Skill- and Capacity-Based Assignment and Ownership History

M1: [ ] Main goals
     M1-1: [ ] Build and verify: assignments  (MOD-310-MP-001)
     M1-2: [ ] Build and verify: assignment recommendations  (MOD-310-MP-002)
     M1-3: [ ] Build and verify: allocation history  (MOD-310-MP-003)
     M1-4: [ ] Build and verify: acknowledgments  (MOD-310-MP-004)
     M1-5: [ ] Build and verify: reassignment history  (MOD-310-MP-005)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: assignments  (MOD-310-DB-001)
     M2-2: [ ] Design and migrate data for: assignment recommendations  (MOD-310-DB-002)
     M2-3: [ ] Design and migrate data for: allocation history  (MOD-310-DB-003)
     M2-4: [ ] Design and migrate data for: acknowledgments  (MOD-310-DB-004)
     M2-5: [ ] Design and migrate data for: reassignment history  (MOD-310-DB-005)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-310-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-310-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-310-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-310-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-310-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-310-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-310-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-310-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-310-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-310-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-310-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-310-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-310-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-310-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-310-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-310-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-310-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-310-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-310-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-310-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-310-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-310-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-310-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-310-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-310-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-310-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] No assignment is made to an unauthorized or unavailable actor.  (MOD-310-AC-001)
     M10-2: [ ] Overrides require a reason.  (MOD-310-AC-002)
     M10-3: [ ] Assignment history is immutable.  (MOD-310-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-310-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-310-AC-901)

### Module 20: [ ] MOD-320 — Configurable Status and Transition Engine

M1: [ ] Main goals
     M1-1: [ ] Build and verify: workflow resolver  (MOD-320-MP-001)
     M1-2: [ ] Build and verify: transition evaluator  (MOD-320-MP-002)
     M1-3: [ ] Build and verify: status history  (MOD-320-MP-003)
     M1-4: [ ] Build and verify: hold records  (MOD-320-MP-004)
     M1-5: [ ] Build and verify: reopen records  (MOD-320-MP-005)
     M1-6: [ ] Build and verify: available next actions  (MOD-320-MP-006)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: workflow resolver  (MOD-320-DB-001)
     M2-2: [ ] Design and migrate data for: transition evaluator  (MOD-320-DB-002)
     M2-3: [ ] Design and migrate data for: status history  (MOD-320-DB-003)
     M2-4: [ ] Design and migrate data for: hold records  (MOD-320-DB-004)
     M2-5: [ ] Design and migrate data for: reopen records  (MOD-320-DB-005)
     M2-6: [ ] Design and migrate data for: available next actions  (MOD-320-DB-006)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-320-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-320-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-320-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-320-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-320-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-320-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-320-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-320-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-320-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-320-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-320-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-320-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-320-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-320-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-320-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-320-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-320-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-320-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-320-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-320-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-320-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-320-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-320-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-320-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-320-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-320-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] No business status is hard-coded as a database enum.  (MOD-320-AC-001)
     M10-2: [ ] Every transition creates history and audit.  (MOD-320-AC-002)
     M10-3: [ ] Agents cannot skip required approval gates.  (MOD-320-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-320-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-320-AC-901)

### Module 21: [ ] MOD-330 — Human Approval Gates, Delegation, Rejection, and Override

M1: [ ] Main goals
     M1-1: [ ] Build and verify: approvals  (MOD-330-MP-001)
     M1-2: [ ] Build and verify: approval workflows  (MOD-330-MP-002)
     M1-3: [ ] Build and verify: approval steps  (MOD-330-MP-003)
     M1-4: [ ] Build and verify: approval decisions  (MOD-330-MP-004)
     M1-5: [ ] Build and verify: delegations  (MOD-330-MP-005)
     M1-6: [ ] Build and verify: approval evidence  (MOD-330-MP-006)
     M1-7: [ ] Build and verify: human overrides  (MOD-330-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: approvals  (MOD-330-DB-001)
     M2-2: [ ] Design and migrate data for: approval workflows  (MOD-330-DB-002)
     M2-3: [ ] Design and migrate data for: approval steps  (MOD-330-DB-003)
     M2-4: [ ] Design and migrate data for: approval decisions  (MOD-330-DB-004)
     M2-5: [ ] Design and migrate data for: delegations  (MOD-330-DB-005)
     M2-6: [ ] Design and migrate data for: approval evidence  (MOD-330-DB-006)
     M2-7: [ ] Design and migrate data for: human overrides  (MOD-330-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-330-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-330-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-330-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-330-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-330-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-330-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-330-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-330-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-330-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-330-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-330-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-330-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-330-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-330-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-330-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-330-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-330-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-330-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-330-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-330-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-330-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-330-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-330-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-330-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-330-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-330-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Dependent actions remain blocked until approval.  (MOD-330-AC-001)
     M10-2: [ ] Approvals bind to exact versions.  (MOD-330-AC-002)
     M10-3: [ ] Agents cannot approve their own recommendations.  (MOD-330-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-330-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-330-AC-901)

### Module 22: [ ] MOD-340 — Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations

M1: [ ] Main goals
     M1-1: [ ] Build and verify: follow-ups  (MOD-340-MP-001)
     M1-2: [ ] Build and verify: reminders  (MOD-340-MP-002)
     M1-3: [ ] Build and verify: escalations  (MOD-340-MP-003)
     M1-4: [ ] Build and verify: parent-child links  (MOD-340-MP-004)
     M1-5: [ ] Build and verify: SLA pauses  (MOD-340-MP-005)
     M1-6: [ ] Build and verify: business-time deadlines  (MOD-340-MP-006)
     M1-7: [ ] Build and verify: closure evidence  (MOD-340-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: follow-ups  (MOD-340-DB-001)
     M2-2: [ ] Design and migrate data for: reminders  (MOD-340-DB-002)
     M2-3: [ ] Design and migrate data for: escalations  (MOD-340-DB-003)
     M2-4: [ ] Design and migrate data for: parent-child links  (MOD-340-DB-004)
     M2-5: [ ] Design and migrate data for: SLA pauses  (MOD-340-DB-005)
     M2-6: [ ] Design and migrate data for: business-time deadlines  (MOD-340-DB-006)
     M2-7: [ ] Design and migrate data for: closure evidence  (MOD-340-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-340-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-340-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-340-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-340-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-340-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-340-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-340-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-340-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-340-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-340-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-340-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-340-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-340-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-340-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-340-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-340-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-340-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-340-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-340-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-340-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-340-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-340-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-340-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-340-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-340-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-340-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Every request has owner, deadline, rule version, and closure condition.  (MOD-340-AC-001)
     M10-2: [ ] Overdue items trigger configured reminders and escalation.  (MOD-340-AC-002)
     M10-3: [ ] Parent-child chains preserve return routing.  (MOD-340-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-340-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-340-AC-901)

### Module 23: [ ] MOD-350 — Temporal Orchestrator and Durable Business Workflows

M1: [ ] Main goals
     M1-1: [ ] Build and verify: workflow instances  (MOD-350-MP-001)
     M1-2: [ ] Build and verify: workflow signals  (MOD-350-MP-002)
     M1-3: [ ] Build and verify: workflow versions  (MOD-350-MP-003)
     M1-4: [ ] Build and verify: workflow failures  (MOD-350-MP-004)
     M1-5: [ ] Build and verify: interventions  (MOD-350-MP-005)
     M1-6: [ ] Build and verify: 12 approved workflows  (MOD-350-MP-006)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: workflow instances  (MOD-350-DB-001)
     M2-2: [ ] Design and migrate data for: workflow signals  (MOD-350-DB-002)
     M2-3: [ ] Design and migrate data for: workflow versions  (MOD-350-DB-003)
     M2-4: [ ] Design and migrate data for: workflow failures  (MOD-350-DB-004)
     M2-5: [ ] Design and migrate data for: interventions  (MOD-350-DB-005)
     M2-6: [ ] Design and migrate data for: 12 approved workflows  (MOD-350-DB-006)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-350-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-350-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-350-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-350-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-350-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-350-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-350-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-350-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-350-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-350-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-350-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-350-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-350-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-350-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-350-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-350-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-350-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-350-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-350-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-350-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-350-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-350-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-350-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-350-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-350-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-350-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Workflows survive worker restarts.  (MOD-350-AC-001)
     M10-2: [ ] Timers, retries, and duplicate signals are idempotent.  (MOD-350-AC-002)
     M10-3: [ ] Workflow history does not replace PostgreSQL business state.  (MOD-350-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-350-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-350-AC-901)

### Module 24: [ ] MOD-360 — LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision

M1: [ ] Main goals
     M1-1: [ ] Build and verify: agent registry  (MOD-360-MP-001)
     M1-2: [ ] Build and verify: agent runs  (MOD-360-MP-002)
     M1-3: [ ] Build and verify: prompt versions  (MOD-360-MP-003)
     M1-4: [ ] Build and verify: tool policies  (MOD-360-MP-004)
     M1-5: [ ] Build and verify: context builder  (MOD-360-MP-005)
     M1-6: [ ] Build and verify: agent reviews  (MOD-360-MP-006)
     M1-7: [ ] Build and verify: agent evaluations  (MOD-360-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: agent registry  (MOD-360-DB-001)
     M2-2: [ ] Design and migrate data for: agent runs  (MOD-360-DB-002)
     M2-3: [ ] Design and migrate data for: prompt versions  (MOD-360-DB-003)
     M2-4: [ ] Design and migrate data for: tool policies  (MOD-360-DB-004)
     M2-5: [ ] Design and migrate data for: context builder  (MOD-360-DB-005)
     M2-6: [ ] Design and migrate data for: agent reviews  (MOD-360-DB-006)
     M2-7: [ ] Design and migrate data for: agent evaluations  (MOD-360-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-360-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-360-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-360-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-360-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-360-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-360-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-360-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-360-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-360-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-360-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-360-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-360-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-360-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-360-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-360-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-360-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-360-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-360-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-360-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-360-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-360-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-360-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-360-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-360-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-360-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-360-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Every run records model, prompt, sources, tools, output, review, and audit.  (MOD-360-AC-001)
     M10-2: [ ] Agents use business APIs rather than direct database access.  (MOD-360-AC-002)
     M10-3: [ ] Low-confidence or conflicting output creates human review.  (MOD-360-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-360-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-360-AC-901)

### Module 25: [ ] MOD-370 — Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation

M1: [ ] Main goals
     M1-1: [ ] Build and verify: knowledge items  (MOD-370-MP-001)
     M1-2: [ ] Build and verify: knowledge versions  (MOD-370-MP-002)
     M1-3: [ ] Build and verify: chunks  (MOD-370-MP-003)
     M1-4: [ ] Build and verify: embeddings  (MOD-370-MP-004)
     M1-5: [ ] Build and verify: knowledge permissions  (MOD-370-MP-005)
     M1-6: [ ] Build and verify: usage logs  (MOD-370-MP-006)
     M1-7: [ ] Build and verify: knowledge conflicts  (MOD-370-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: knowledge items  (MOD-370-DB-001)
     M2-2: [ ] Design and migrate data for: knowledge versions  (MOD-370-DB-002)
     M2-3: [ ] Design and migrate data for: chunks  (MOD-370-DB-003)
     M2-4: [ ] Design and migrate data for: embeddings  (MOD-370-DB-004)
     M2-5: [ ] Design and migrate data for: knowledge permissions  (MOD-370-DB-005)
     M2-6: [ ] Design and migrate data for: usage logs  (MOD-370-DB-006)
     M2-7: [ ] Design and migrate data for: knowledge conflicts  (MOD-370-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-370-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-370-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-370-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-370-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-370-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-370-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-370-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-370-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-370-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-370-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-370-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-370-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-370-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-370-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-370-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-370-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-370-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-370-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-370-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-370-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-370-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-370-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-370-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-370-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-370-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-370-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Agents cite the source and version used.  (MOD-370-AC-001)
     M10-2: [ ] Project-approved knowledge outranks generic examples.  (MOD-370-AC-002)
     M10-3: [ ] Unauthorized, expired, rejected, or superseded content is excluded.  (MOD-370-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-370-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-370-AC-901)

## Phase 4 - Quality, Change, Release, and Reporting

### Module 26: [ ] MOD-400 — Test Cases, Test Steps, Test Runs, Evidence, and Coverage

M1: [ ] Main goals
     M1-1: [ ] Build and verify: test cases  (MOD-400-MP-001)
     M1-2: [ ] Build and verify: test steps  (MOD-400-MP-002)
     M1-3: [ ] Build and verify: test suites  (MOD-400-MP-003)
     M1-4: [ ] Build and verify: test plans  (MOD-400-MP-004)
     M1-5: [ ] Build and verify: test runs  (MOD-400-MP-005)
     M1-6: [ ] Build and verify: test evidence  (MOD-400-MP-006)
     M1-7: [ ] Build and verify: coverage links  (MOD-400-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: test cases  (MOD-400-DB-001)
     M2-2: [ ] Design and migrate data for: test steps  (MOD-400-DB-002)
     M2-3: [ ] Design and migrate data for: test suites  (MOD-400-DB-003)
     M2-4: [ ] Design and migrate data for: test plans  (MOD-400-DB-004)
     M2-5: [ ] Design and migrate data for: test runs  (MOD-400-DB-005)
     M2-6: [ ] Design and migrate data for: test evidence  (MOD-400-DB-006)
     M2-7: [ ] Design and migrate data for: coverage links  (MOD-400-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-400-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-400-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-400-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-400-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-400-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-400-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-400-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-400-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-400-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-400-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-400-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-400-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-400-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-400-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-400-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-400-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-400-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-400-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-400-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-400-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-400-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-400-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-400-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-400-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-400-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-400-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Every Must-Have requirement has approved test coverage.  (MOD-400-AC-001)
     M10-2: [ ] Critical permissions have negative tests.  (MOD-400-AC-002)
     M10-3: [ ] Test evidence is tied to environment and build.  (MOD-400-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-400-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-400-AC-901)

### Module 27: [ ] MOD-410 — Bug Lifecycle, QA Rejection, Development Reopen, and Retesting

M1: [ ] Main goals
     M1-1: [ ] Build and verify: bugs  (MOD-410-MP-001)
     M1-2: [ ] Build and verify: bug links  (MOD-410-MP-002)
     M1-3: [ ] Build and verify: bug assignments  (MOD-410-MP-003)
     M1-4: [ ] Build and verify: fix submissions  (MOD-410-MP-004)
     M1-5: [ ] Build and verify: retests  (MOD-410-MP-005)
     M1-6: [ ] Build and verify: known issue approvals  (MOD-410-MP-006)
     M1-7: [ ] Build and verify: severity SLA  (MOD-410-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: bugs  (MOD-410-DB-001)
     M2-2: [ ] Design and migrate data for: bug links  (MOD-410-DB-002)
     M2-3: [ ] Design and migrate data for: bug assignments  (MOD-410-DB-003)
     M2-4: [ ] Design and migrate data for: fix submissions  (MOD-410-DB-004)
     M2-5: [ ] Design and migrate data for: retests  (MOD-410-DB-005)
     M2-6: [ ] Design and migrate data for: known issue approvals  (MOD-410-DB-006)
     M2-7: [ ] Design and migrate data for: severity SLA  (MOD-410-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-410-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-410-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-410-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-410-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-410-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-410-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-410-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-410-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-410-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-410-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-410-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-410-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-410-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-410-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-410-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-410-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-410-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-410-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-410-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-410-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-410-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-410-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-410-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-410-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-410-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-410-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] QA can reject and reopen work with evidence.  (MOD-410-AC-001)
     M10-2: [ ] Blocking defects prevent release.  (MOD-410-AC-002)
     M10-3: [ ] Bug history links requirement, ticket, test, fix, retest, and release.  (MOD-410-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-410-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-410-AC-901)

### Module 28: [ ] MOD-420 — Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates

M1: [ ] Main goals
     M1-1: [ ] Build and verify: risks  (MOD-420-MP-001)
     M1-2: [ ] Build and verify: risk reviews  (MOD-420-MP-002)
     M1-3: [ ] Build and verify: change requests  (MOD-420-MP-003)
     M1-4: [ ] Build and verify: impact analyses  (MOD-420-MP-004)
     M1-5: [ ] Build and verify: change approvals  (MOD-420-MP-005)
     M1-6: [ ] Build and verify: baseline updates  (MOD-420-MP-006)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: risks  (MOD-420-DB-001)
     M2-2: [ ] Design and migrate data for: risk reviews  (MOD-420-DB-002)
     M2-3: [ ] Design and migrate data for: change requests  (MOD-420-DB-003)
     M2-4: [ ] Design and migrate data for: impact analyses  (MOD-420-DB-004)
     M2-5: [ ] Design and migrate data for: change approvals  (MOD-420-DB-005)
     M2-6: [ ] Design and migrate data for: baseline updates  (MOD-420-DB-006)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-420-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-420-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-420-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-420-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-420-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-420-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-420-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-420-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-420-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-420-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-420-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-420-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-420-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-420-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-420-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-420-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-420-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-420-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-420-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-420-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-420-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-420-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-420-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-420-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-420-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-420-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Out-of-scope work cannot silently enter development.  (MOD-420-AC-001)
     M10-2: [ ] Approved changes update affected versions and tickets.  (MOD-420-AC-002)
     M10-3: [ ] Rejected and deferred changes preserve evidence and rationale.  (MOD-420-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-420-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-420-AC-901)

### Module 29: [ ] MOD-430 — Releases, Deployment Requests, Production Approval, Rollback, and Closure

M1: [ ] Main goals
     M1-1: [ ] Build and verify: releases  (MOD-430-MP-001)
     M1-2: [ ] Build and verify: release items  (MOD-430-MP-002)
     M1-3: [ ] Build and verify: deployments  (MOD-430-MP-003)
     M1-4: [ ] Build and verify: deployment checks  (MOD-430-MP-004)
     M1-5: [ ] Build and verify: backup confirmations  (MOD-430-MP-005)
     M1-6: [ ] Build and verify: migration plans  (MOD-430-MP-006)
     M1-7: [ ] Build and verify: rollbacks  (MOD-430-MP-007)
     M1-8: [ ] Build and verify: completion reports  (MOD-430-MP-008)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: releases  (MOD-430-DB-001)
     M2-2: [ ] Design and migrate data for: release items  (MOD-430-DB-002)
     M2-3: [ ] Design and migrate data for: deployments  (MOD-430-DB-003)
     M2-4: [ ] Design and migrate data for: deployment checks  (MOD-430-DB-004)
     M2-5: [ ] Design and migrate data for: backup confirmations  (MOD-430-DB-005)
     M2-6: [ ] Design and migrate data for: migration plans  (MOD-430-DB-006)
     M2-7: [ ] Design and migrate data for: rollbacks  (MOD-430-DB-007)
     M2-8: [ ] Design and migrate data for: completion reports  (MOD-430-DB-008)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-430-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-430-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-430-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-430-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-430-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-430-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-430-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-430-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-430-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-430-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-430-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-430-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-430-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-430-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-430-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-430-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-430-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-430-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-430-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-430-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-430-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-430-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-430-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-430-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-430-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-430-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Production cannot start without evidence and approval.  (MOD-430-AC-001)
     M10-2: [ ] Releases trace to requirements, tickets, tests, bugs, changes, and documents.  (MOD-430-AC-002)
     M10-3: [ ] Closure requires client and internal acceptance.  (MOD-430-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-430-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-430-AC-901)

### Module 30: [ ] MOD-440 — Notifications, Preferences, Digests, Delivery, and Failure Handling

M1: [ ] Main goals
     M1-1: [ ] Build and verify: notifications  (MOD-440-MP-001)
     M1-2: [ ] Build and verify: preferences  (MOD-440-MP-002)
     M1-3: [ ] Build and verify: templates  (MOD-440-MP-003)
     M1-4: [ ] Build and verify: deliveries  (MOD-440-MP-004)
     M1-5: [ ] Build and verify: retries  (MOD-440-MP-005)
     M1-6: [ ] Build and verify: dead letters  (MOD-440-MP-006)
     M1-7: [ ] Build and verify: digests  (MOD-440-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: notifications  (MOD-440-DB-001)
     M2-2: [ ] Design and migrate data for: preferences  (MOD-440-DB-002)
     M2-3: [ ] Design and migrate data for: templates  (MOD-440-DB-003)
     M2-4: [ ] Design and migrate data for: deliveries  (MOD-440-DB-004)
     M2-5: [ ] Design and migrate data for: retries  (MOD-440-DB-005)
     M2-6: [ ] Design and migrate data for: dead letters  (MOD-440-DB-006)
     M2-7: [ ] Design and migrate data for: digests  (MOD-440-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-440-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-440-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-440-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-440-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-440-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-440-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-440-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-440-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-440-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-440-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-440-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-440-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-440-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-440-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-440-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-440-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-440-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-440-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-440-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-440-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-440-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-440-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-440-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-440-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-440-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-440-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Notifications are timely, idempotent, auditable, and permission-safe.  (MOD-440-AC-001)
     M10-2: [ ] Users can configure preferences without disabling mandatory critical alerts.  (MOD-440-AC-002)
     M10-3: [ ] Delivery failures are visible and recoverable.  (MOD-440-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-440-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-440-AC-901)

### Module 31: [ ] MOD-450 — Dashboard, Reporting, Search, Project Health, and Activity Timeline

M1: [ ] Main goals
     M1-1: [ ] Build and verify: dashboard read models  (MOD-450-MP-001)
     M1-2: [ ] Build and verify: project health  (MOD-450-MP-002)
     M1-3: [ ] Build and verify: saved filters  (MOD-450-MP-003)
     M1-4: [ ] Build and verify: global search  (MOD-450-MP-004)
     M1-5: [ ] Build and verify: activity timeline  (MOD-450-MP-005)
     M1-6: [ ] Build and verify: reports  (MOD-450-MP-006)
     M1-7: [ ] Build and verify: exports  (MOD-450-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: dashboard read models  (MOD-450-DB-001)
     M2-2: [ ] Design and migrate data for: project health  (MOD-450-DB-002)
     M2-3: [ ] Design and migrate data for: saved filters  (MOD-450-DB-003)
     M2-4: [ ] Design and migrate data for: global search  (MOD-450-DB-004)
     M2-5: [ ] Design and migrate data for: activity timeline  (MOD-450-DB-005)
     M2-6: [ ] Design and migrate data for: reports  (MOD-450-DB-006)
     M2-7: [ ] Design and migrate data for: exports  (MOD-450-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-450-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-450-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-450-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-450-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-450-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-450-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-450-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-450-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-450-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-450-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-450-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-450-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-450-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-450-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-450-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-450-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-450-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-450-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-450-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-450-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-450-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-450-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-450-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-450-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-450-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-450-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Dashboard values reconcile with source records.  (MOD-450-AC-001)
     M10-2: [ ] Normal updates appear within one minute.  (MOD-450-AC-002)
     M10-3: [ ] Counts, search, and exports do not leak unauthorized data.  (MOD-450-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-450-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-450-AC-901)

### Module 32: [ ] MOD-460 — Requirement Traceability, Audit Reports, and Evidence Exports

M1: [ ] Main goals
     M1-1: [ ] Build and verify: requirement-ticket links  (MOD-460-MP-001)
     M1-2: [ ] Build and verify: requirement-test links  (MOD-460-MP-002)
     M1-3: [ ] Build and verify: requirement-release links  (MOD-460-MP-003)
     M1-4: [ ] Build and verify: requirement-document links  (MOD-460-MP-004)
     M1-5: [ ] Build and verify: ticket-test links  (MOD-460-MP-005)
     M1-6: [ ] Build and verify: evidence manifests  (MOD-460-MP-006)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: requirement-ticket links  (MOD-460-DB-001)
     M2-2: [ ] Design and migrate data for: requirement-test links  (MOD-460-DB-002)
     M2-3: [ ] Design and migrate data for: requirement-release links  (MOD-460-DB-003)
     M2-4: [ ] Design and migrate data for: requirement-document links  (MOD-460-DB-004)
     M2-5: [ ] Design and migrate data for: ticket-test links  (MOD-460-DB-005)
     M2-6: [ ] Design and migrate data for: evidence manifests  (MOD-460-DB-006)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-460-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-460-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-460-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-460-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-460-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-460-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-460-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-460-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-460-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-460-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-460-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-460-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-460-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-460-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-460-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-460-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-460-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-460-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-460-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-460-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-460-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-460-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-460-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-460-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-460-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-460-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] At least 95% of Must-Have requirements have complete traceability before release.  (MOD-460-AC-001)
     M10-2: [ ] Controlled actions have 100% audit coverage.  (MOD-460-AC-002)
     M10-3: [ ] Exports are permission-controlled and independently reconcilable.  (MOD-460-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-460-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-460-AC-901)

## Phase 5 - MVP Integrations

### Module 33: [ ] MOD-500 — Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State

M1: [ ] Main goals
     M1-1: [ ] Build and verify: integration connections  (MOD-500-MP-001)
     M1-2: [ ] Build and verify: webhook events  (MOD-500-MP-002)
     M1-3: [ ] Build and verify: sync cursors  (MOD-500-MP-003)
     M1-4: [ ] Build and verify: external mappings  (MOD-500-MP-004)
     M1-5: [ ] Build and verify: outbox events  (MOD-500-MP-005)
     M1-6: [ ] Build and verify: inbox events  (MOD-500-MP-006)
     M1-7: [ ] Build and verify: connection health  (MOD-500-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: integration connections  (MOD-500-DB-001)
     M2-2: [ ] Design and migrate data for: webhook events  (MOD-500-DB-002)
     M2-3: [ ] Design and migrate data for: sync cursors  (MOD-500-DB-003)
     M2-4: [ ] Design and migrate data for: external mappings  (MOD-500-DB-004)
     M2-5: [ ] Design and migrate data for: outbox events  (MOD-500-DB-005)
     M2-6: [ ] Design and migrate data for: inbox events  (MOD-500-DB-006)
     M2-7: [ ] Design and migrate data for: connection health  (MOD-500-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-500-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-500-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-500-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-500-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-500-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-500-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-500-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-500-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-500-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-500-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-500-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-500-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-500-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-500-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-500-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-500-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-500-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-500-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-500-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-500-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-500-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-500-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-500-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-500-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-500-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-500-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Integration failure cannot corrupt internal data.  (MOD-500-AC-001)
     M10-2: [ ] External mappings and events are tenant-scoped and audited.  (MOD-500-AC-002)
     M10-3: [ ] Credentials never appear in logs, prompts, tickets, or business tables.  (MOD-500-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-500-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-500-AC-901)

### Module 34: [ ] MOD-510 — Gmail Client Communication Integration

M1: [ ] Main goals
     M1-1: [ ] Build and verify: Gmail connection  (MOD-510-MP-001)
     M1-2: [ ] Build and verify: history cursor  (MOD-510-MP-002)
     M1-3: [ ] Build and verify: thread mappings  (MOD-510-MP-003)
     M1-4: [ ] Build and verify: message mappings  (MOD-510-MP-004)
     M1-5: [ ] Build and verify: attachment import  (MOD-510-MP-005)
     M1-6: [ ] Build and verify: draft review  (MOD-510-MP-006)
     M1-7: [ ] Build and verify: approved send  (MOD-510-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: Gmail connection  (MOD-510-DB-001)
     M2-2: [ ] Design and migrate data for: history cursor  (MOD-510-DB-002)
     M2-3: [ ] Design and migrate data for: thread mappings  (MOD-510-DB-003)
     M2-4: [ ] Design and migrate data for: message mappings  (MOD-510-DB-004)
     M2-5: [ ] Design and migrate data for: attachment import  (MOD-510-DB-005)
     M2-6: [ ] Design and migrate data for: draft review  (MOD-510-DB-006)
     M2-7: [ ] Design and migrate data for: approved send  (MOD-510-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-510-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-510-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-510-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-510-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-510-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-510-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-510-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-510-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-510-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-510-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-510-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-510-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-510-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-510-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-510-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-510-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-510-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-510-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-510-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-510-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-510-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-510-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-510-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-510-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-510-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-510-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Valid emails create or update exactly one query and thread.  (MOD-510-AC-001)
     M10-2: [ ] Approved outgoing email is sent and linked correctly.  (MOD-510-AC-002)
     M10-3: [ ] Duplicate notifications do not duplicate records.  (MOD-510-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-510-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-510-AC-901)

### Module 35: [ ] MOD-520 — Jira Work Management Integration

M1: [ ] Main goals
     M1-1: [ ] Build and verify: Jira connection  (MOD-520-MP-001)
     M1-2: [ ] Build and verify: project mapping  (MOD-520-MP-002)
     M1-3: [ ] Build and verify: field mapping  (MOD-520-MP-003)
     M1-4: [ ] Build and verify: status mapping  (MOD-520-MP-004)
     M1-5: [ ] Build and verify: issue mapping  (MOD-520-MP-005)
     M1-6: [ ] Build and verify: comment sync  (MOD-520-MP-006)
     M1-7: [ ] Build and verify: conflict handling  (MOD-520-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: Jira connection  (MOD-520-DB-001)
     M2-2: [ ] Design and migrate data for: project mapping  (MOD-520-DB-002)
     M2-3: [ ] Design and migrate data for: field mapping  (MOD-520-DB-003)
     M2-4: [ ] Design and migrate data for: status mapping  (MOD-520-DB-004)
     M2-5: [ ] Design and migrate data for: issue mapping  (MOD-520-DB-005)
     M2-6: [ ] Design and migrate data for: comment sync  (MOD-520-DB-006)
     M2-7: [ ] Design and migrate data for: conflict handling  (MOD-520-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-520-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-520-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-520-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-520-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-520-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-520-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-520-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-520-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-520-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-520-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-520-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-520-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-520-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-520-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-520-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-520-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-520-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-520-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-520-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-520-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-520-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-520-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-520-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-520-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-520-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-520-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] Approved internal tickets create Jira issues and retain keys.  (MOD-520-AC-001)
     M10-2: [ ] Jira cannot bypass internal transition or approval rules.  (MOD-520-AC-002)
     M10-3: [ ] Sync failures are visible, retriable, and audited.  (MOD-520-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-520-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-520-AC-901)

## Phase 6 - Security, Reliability, Pilot, and Production Readiness

### Module 36: [ ] MOD-600 — Security, Privacy, PII, File Safety, Retention, Backup, and Recovery Hardening

M1: [ ] Main goals
     M1-1: [ ] Build and verify: threat model  (MOD-600-MP-001)
     M1-2: [ ] Build and verify: PII inventory  (MOD-600-MP-002)
     M1-3: [ ] Build and verify: retention policies  (MOD-600-MP-003)
     M1-4: [ ] Build and verify: legal holds  (MOD-600-MP-004)
     M1-5: [ ] Build and verify: deletion jobs  (MOD-600-MP-005)
     M1-6: [ ] Build and verify: backup records  (MOD-600-MP-006)
     M1-7: [ ] Build and verify: restore tests  (MOD-600-MP-007)
     M1-8: [ ] Build and verify: security incidents  (MOD-600-MP-008)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: threat model  (MOD-600-DB-001)
     M2-2: [ ] Design and migrate data for: PII inventory  (MOD-600-DB-002)
     M2-3: [ ] Design and migrate data for: retention policies  (MOD-600-DB-003)
     M2-4: [ ] Design and migrate data for: legal holds  (MOD-600-DB-004)
     M2-5: [ ] Design and migrate data for: deletion jobs  (MOD-600-DB-005)
     M2-6: [ ] Design and migrate data for: backup records  (MOD-600-DB-006)
     M2-7: [ ] Design and migrate data for: restore tests  (MOD-600-DB-007)
     M2-8: [ ] Design and migrate data for: security incidents  (MOD-600-DB-008)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-600-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-600-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-600-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-600-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-600-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-600-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-600-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-600-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-600-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-600-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-600-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-600-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-600-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-600-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-600-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-600-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-600-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-600-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-600-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-600-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-600-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-600-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-600-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-600-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-600-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-600-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] No Critical security or isolation defect remains.  (MOD-600-AC-001)
     M10-2: [ ] RPO and RTO targets are validated.  (MOD-600-AC-002)
     M10-3: [ ] Client and company data are excluded from model training by default.  (MOD-600-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-600-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-600-AC-901)

### Module 37: [ ] MOD-610 — Performance, Reliability, Idempotency, Resilience, and Disaster Recovery

M1: [ ] Main goals
     M1-1: [ ] Build and verify: performance tests  (MOD-610-MP-001)
     M1-2: [ ] Build and verify: resilience tests  (MOD-610-MP-002)
     M1-3: [ ] Build and verify: index review  (MOD-610-MP-003)
     M1-4: [ ] Build and verify: SLO dashboards  (MOD-610-MP-004)
     M1-5: [ ] Build and verify: workflow replay  (MOD-610-MP-005)
     M1-6: [ ] Build and verify: integration failure tests  (MOD-610-MP-006)
     M1-7: [ ] Build and verify: DR runbook  (MOD-610-MP-007)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: performance tests  (MOD-610-DB-001)
     M2-2: [ ] Design and migrate data for: resilience tests  (MOD-610-DB-002)
     M2-3: [ ] Design and migrate data for: index review  (MOD-610-DB-003)
     M2-4: [ ] Design and migrate data for: SLO dashboards  (MOD-610-DB-004)
     M2-5: [ ] Design and migrate data for: workflow replay  (MOD-610-DB-005)
     M2-6: [ ] Design and migrate data for: integration failure tests  (MOD-610-DB-006)
     M2-7: [ ] Design and migrate data for: DR runbook  (MOD-610-DB-007)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-610-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-610-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-610-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-610-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-610-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-610-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-610-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-610-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-610-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-610-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-610-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-610-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-610-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-610-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-610-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-610-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-610-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-610-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-610-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-610-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-610-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-610-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-610-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-610-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-610-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-610-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] 95% of normal APIs are under two seconds.  (MOD-610-AC-001)
     M10-2: [ ] Dashboard is under three seconds at pilot load.  (MOD-610-AC-002)
     M10-3: [ ] Durable workflows resume after failure and remain idempotent.  (MOD-610-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-610-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-610-AC-901)

### Module 38: [ ] MOD-620 — Synthetic Sample Projects, Agent Evaluation, End-to-End Acceptance, and UAT

M1: [ ] Main goals
     M1-1: [ ] Build and verify: seed scripts  (MOD-620-MP-001)
     M1-2: [ ] Build and verify: expected decisions  (MOD-620-MP-002)
     M1-3: [ ] Build and verify: agent evaluations  (MOD-620-MP-003)
     M1-4: [ ] Build and verify: E2E tests  (MOD-620-MP-004)
     M1-5: [ ] Build and verify: role-based UAT  (MOD-620-MP-005)
     M1-6: [ ] Build and verify: acceptance evidence  (MOD-620-MP-006)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: seed scripts  (MOD-620-DB-001)
     M2-2: [ ] Design and migrate data for: expected decisions  (MOD-620-DB-002)
     M2-3: [ ] Design and migrate data for: agent evaluations  (MOD-620-DB-003)
     M2-4: [ ] Design and migrate data for: E2E tests  (MOD-620-DB-004)
     M2-5: [ ] Design and migrate data for: role-based UAT  (MOD-620-DB-005)
     M2-6: [ ] Design and migrate data for: acceptance evidence  (MOD-620-DB-006)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-620-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-620-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-620-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-620-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-620-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-620-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-620-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-620-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-620-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-620-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-620-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-620-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-620-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-620-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-620-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-620-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-620-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-620-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-620-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-620-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-620-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-620-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-620-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-620-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-620-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-620-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] All three sample projects pass defined workflows.  (MOD-620-AC-001)
     M10-2: [ ] Agent quality metrics meet targets.  (MOD-620-AC-002)
     M10-3: [ ] No unauthorized agent approval or isolation failure occurs.  (MOD-620-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-620-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-620-AC-901)

### Module 39: [ ] MOD-630 — Controlled Pilot, Production Release, Operations, and Final MVP Sign-Off

M1: [ ] Main goals
     M1-1: [ ] Build and verify: pilot plan  (MOD-630-MP-001)
     M1-2: [ ] Build and verify: pilot users  (MOD-630-MP-002)
     M1-3: [ ] Build and verify: training  (MOD-630-MP-003)
     M1-4: [ ] Build and verify: support readiness  (MOD-630-MP-004)
     M1-5: [ ] Build and verify: known limitations  (MOD-630-MP-005)
     M1-6: [ ] Build and verify: production deployment  (MOD-630-MP-006)
     M1-7: [ ] Build and verify: rollback  (MOD-630-MP-007)
     M1-8: [ ] Build and verify: final sign-offs  (MOD-630-MP-008)

M2: [ ] Database
     M2-1: [ ] Design and migrate data for: pilot plan  (MOD-630-DB-001)
     M2-2: [ ] Design and migrate data for: pilot users  (MOD-630-DB-002)
     M2-3: [ ] Design and migrate data for: training  (MOD-630-DB-003)
     M2-4: [ ] Design and migrate data for: support readiness  (MOD-630-DB-004)
     M2-5: [ ] Design and migrate data for: known limitations  (MOD-630-DB-005)
     M2-6: [ ] Design and migrate data for: production deployment  (MOD-630-DB-006)
     M2-7: [ ] Design and migrate data for: rollback  (MOD-630-DB-007)
     M2-8: [ ] Design and migrate data for: final sign-offs  (MOD-630-DB-008)

M3: [ ] Backend
     M3-1: [ ] Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  (MOD-630-BE-001)
     M3-2: [ ] Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  (MOD-630-BE-002)
     M3-3: [ ] Publish domain events through the transactionally safe outbox when asynchronous processing is required.  (MOD-630-BE-003)
     M3-4: [ ] Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  (MOD-630-BE-004)

M4: [ ] API
     M4-1: [ ] Create versioned CRUD, query, transition, action, and history endpoints required by the module.  (MOD-630-API-001)
     M4-2: [ ] Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  (MOD-630-API-002)
     M4-3: [ ] Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  (MOD-630-API-003)

M5: [ ] Frontend
     M5-1: [ ] Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  (MOD-630-FE-001)
     M5-2: [ ] Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  (MOD-630-FE-002)
     M5-3: [ ] Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  (MOD-630-FE-003)
     M5-4: [ ] Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  (MOD-630-FE-004)

M6: [ ] Workflow / agents / events
     M6-1: [ ] Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  (MOD-630-WF-001)
     M6-2: [ ] Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  (MOD-630-WF-002)
     M6-3: [ ] Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  (MOD-630-WF-003)
     M6-4: [ ] Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  (MOD-630-WF-004)

M7: [ ] Security / audit
     M7-1: [ ] Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  (MOD-630-SEC-001)
     M7-2: [ ] Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  (MOD-630-SEC-002)
     M7-3: [ ] Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  (MOD-630-SEC-003)
     M7-4: [ ] Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  (MOD-630-SEC-004)

M8: [ ] Testing
     M8-1: [ ] Add unit tests for domain rules, validation, conflicts, and invalid state.  (MOD-630-QA-001)
     M8-2: [ ] Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  (MOD-630-QA-002)
     M8-3: [ ] Add role-permission negative tests and tenant/project isolation tests.  (MOD-630-QA-003)
     M8-4: [ ] Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  (MOD-630-QA-004)
     M8-5: [ ] Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  (MOD-630-QA-005)

M9: [ ] Docs
     M9-1: [ ] Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  (MOD-630-DOC-001)
     M9-2: [ ] Record migration, rollback, known limitations, verification commands, and evidence references.  (MOD-630-DOC-002)

M10: [ ] Acceptance / Done gate
     M10-1: [ ] All Critical and High acceptance tests pass.  (MOD-630-AC-001)
     M10-2: [ ] Pilot users approve controlled production use.  (MOD-630-AC-002)
     M10-3: [ ] Cross-functional production readiness sign-off is complete.  (MOD-630-AC-003)
     M10-4: [ ] All Critical and High defects for this module are resolved.  (MOD-630-AC-900)
     M10-5: [ ] The responsible human owner reviews and approves the completion evidence.  (MOD-630-AC-901)

---

Generated by `scripts/generate_plain_module_checklist.py`. Update STATUS in that script (keep aligned with the progress checklist), then regenerate.

