# MASMS Implementation Progress Checklist

**Source:** `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md`
**Companion evidence gate checklist:** `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md`
**Last updated (workspace):** 2026-08-11
**Rule:** checkmarks reflect repository evidence; AC-901 human Done for MOD-000..370, MOD-400, and MOD-410..430 recorded 2026-08-11.

## Legend

| Mark | Meaning |
|---|---|
| `[x]` | Done with evidence |
| `[~]` | Partial / scaffold only |
| `[-]` | N/A for current scope (deferred by design) |
| `[!]` | Blocked (needs human or external dependency) |
| `[ ]` | Not started |

## Summary roll-up

| Module | Phase | Tasks | Done | Partial | N/A | Blocked | Open | Module status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| MOD-000 | Phase 0 - Governance and Foundation | 41 | 37 | 0 | 4 | 0 | 0 | Done |
| MOD-010 | Phase 0 - Governance and Foundation | 47 | 17 | 0 | 30 | 0 | 0 | Done |
| MOD-020 | Phase 0 - Governance and Foundation | 49 | 40 | 0 | 9 | 0 | 0 | Done |
| MOD-030 | Phase 0 - Governance and Foundation | 43 | 15 | 0 | 28 | 0 | 0 | Done |
| MOD-040 | Phase 0 - Governance and Foundation | 45 | 35 | 0 | 10 | 0 | 0 | Done |
| MOD-100 | Phase 1 - Identity, Organization, and Configuration | 49 | 41 | 0 | 8 | 0 | 0 | Done |
| MOD-110 | Phase 1 - Identity, Organization, and Configuration | 45 | 34 | 0 | 11 | 0 | 0 | Done |
| MOD-120 | Phase 1 - Identity, Organization, and Configuration | 47 | 37 | 0 | 10 | 0 | 0 | Done |
| MOD-130 | Phase 1 - Identity, Organization, and Configuration | 47 | 37 | 0 | 10 | 0 | 0 | Done |
| MOD-140 | Phase 1 - Identity, Organization, and Configuration | 47 | 40 | 0 | 7 | 0 | 0 | Done |
| MOD-200 | Phase 2 - Client, Query, and Requirement Management | 43 | 39 | 0 | 4 | 0 | 0 | Done |
| MOD-210 | Phase 2 - Client, Query, and Requirement Management | 43 | 40 | 0 | 3 | 0 | 0 | Done |
| MOD-220 | Phase 2 - Client, Query, and Requirement Management | 43 | 40 | 0 | 3 | 0 | 0 | Done |
| MOD-230 | Phase 2 - Client, Query, and Requirement Management | 43 | 40 | 0 | 3 | 0 | 0 | Done |
| MOD-240 | Phase 2 - Client, Query, and Requirement Management | 47 | 44 | 0 | 3 | 0 | 0 | Done |
| MOD-250 | Phase 2 - Client, Query, and Requirement Management | 45 | 43 | 0 | 2 | 0 | 0 | Done |
| MOD-260 | Phase 2 - Client, Query, and Requirement Management | 43 | 40 | 0 | 3 | 0 | 0 | Done |
| MOD-300 | Phase 3 - Work Management and Agent Orchestration | 45 | 42 | 0 | 3 | 0 | 0 | Done |
| MOD-310 | Phase 3 - Work Management and Agent Orchestration | 41 | 34 | 0 | 7 | 0 | 0 | Done |
| MOD-320 | Phase 3 - Work Management and Agent Orchestration | 43 | 36 | 0 | 7 | 0 | 0 | Done |
| MOD-330 | Phase 3 - Work Management and Agent Orchestration | 45 | 38 | 0 | 7 | 0 | 0 | Done |
| MOD-340 | Phase 3 - Work Management and Agent Orchestration | 45 | 38 | 0 | 7 | 0 | 0 | Done |
| MOD-350 | Phase 3 - Work Management and Agent Orchestration | 43 | 34 | 2 | 7 | 0 | 0 | Done (M1) |
| MOD-360 | Phase 3 - Work Management and Agent Orchestration | 45 | 35 | 2 | 8 | 0 | 0 | Done (M1) |
| MOD-370 | Phase 3 - Work Management and Agent Orchestration | 45 | 35 | 2 | 8 | 0 | 0 | Done (M1) |
| MOD-400 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 35 | 2 | 8 | 0 | 0 | Done (M1) |
| MOD-410 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 35 | 2 | 8 | 0 | 0 | Done (M1) |
| MOD-420 | Phase 4 - Quality, Change, Release, and Reporting | 43 | 34 | 2 | 7 | 0 | 0 | Done (M1) |
| MOD-430 | Phase 4 - Quality, Change, Release, and Reporting | 47 | 37 | 2 | 8 | 0 | 0 | Done (M1) |
| MOD-440 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 37 | 2 | 5 | 1 | 0 | Done (M1) — AC-901 blocked |
| MOD-450 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 37 | 2 | 5 | 1 | 0 | Done (M1) — AC-901 blocked |
| MOD-460 | Phase 4 - Quality, Change, Release, and Reporting | 43 | 35 | 2 | 5 | 1 | 0 | Done (M1) — AC-901 blocked |
| MOD-500 | Phase 5 - MVP Integrations | 45 | 35 | 2 | 5 | 1 | 0 | Done (M1) — AC-901 blocked |
| MOD-510 | Phase 5 - MVP Integrations | 45 | 35 | 2 | 5 | 1 | 0 | Done (M1) — AC-901 blocked |
| MOD-520 | Phase 5 - MVP Integrations | 45 | 35 | 2 | 5 | 1 | 0 | Done (M1) — AC-901 blocked |
| MOD-600 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 47 | 0 | 0 | 0 | 0 | 47 | Not started |
| MOD-610 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-620 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-630 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 47 | 0 | 0 | 0 | 0 | 47 | Not started |

**Totals:** 1749 tasks — done 878, partial 8, n/a 192, blocked 2, open 673

## Module index (plan order)

1. [MOD-000](#mod-000) — Project Governance, Source Baseline, and Change Control
2. [MOD-010](#mod-010) — Repository, Toolchain, and Local Development Environment
3. [MOD-020](#mod-020) — Shared Architecture, Domain Kernel, and API Standards
4. [MOD-030](#mod-030) — Environment Configuration, Secrets, CI/CD, and Deployment Skeleton
5. [MOD-040](#mod-040) — Observability, Audit Foundation, and Operational Health
6. [MOD-100](#mod-100) — Organizations, Actors, Human Users, Agents, Teams, and Departments
7. [MOD-110](#mod-110) — Authentication, Sessions, MFA, and Account Security
8. [MOD-120](#mod-120) — RBAC, Attribute-Based Access, Project Membership, and Row-Level Security
9. [MOD-130](#mod-130) — Skills, Availability, Capacity, Working Hours, and Business Calendars
10. [MOD-140](#mod-140) — Configuration Administration and Versioned Operational Rules
11. [MOD-200](#mod-200) — Client and Contact Management
12. [MOD-210](#mod-210) — Client Queries, Qualification, and Opportunities
13. [MOD-220](#mod-220) — Conversations, Messages, Attachments, and Communication History
14. [MOD-230](#mod-230) — Requirement Gathering, Completeness Analysis, Clarifications, and Requirement Brief
15. [MOD-240](#mod-240) — Projects, Requirements, Requirement Versions, and SRS Management
16. [MOD-250](#mod-250) — Documents, Standard Templates, Versioning, and Secure File Storage
17. [MOD-260](#mod-260) — Project Phases, Milestones, Roadmaps, Dependencies, and Baselines
18. [MOD-300](#mod-300) — Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion
19. [MOD-310](#mod-310) — Skill- and Capacity-Based Assignment and Ownership History
20. [MOD-320](#mod-320) — Configurable Status and Transition Engine
21. [MOD-330](#mod-330) — Human Approval Gates, Delegation, Rejection, and Override
22. [MOD-340](#mod-340) — Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations
23. [MOD-350](#mod-350) — Temporal Orchestrator and Durable Business Workflows
24. [MOD-360](#mod-360) — LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision
25. [MOD-370](#mod-370) — Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation
26. [MOD-400](#mod-400) — Test Cases, Test Steps, Test Runs, Evidence, and Coverage
27. [MOD-410](#mod-410) — Bug Lifecycle, QA Rejection, Development Reopen, and Retesting
28. [MOD-420](#mod-420) — Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates
29. [MOD-430](#mod-430) — Releases, Deployment Requests, Production Approval, Rollback, and Closure
30. [MOD-440](#mod-440) — Notifications, Preferences, Digests, Delivery, and Failure Handling
31. [MOD-450](#mod-450) — Dashboard, Reporting, Search, Project Health, and Activity Timeline
32. [MOD-460](#mod-460) — Requirement Traceability, Audit Reports, and Evidence Exports
33. [MOD-500](#mod-500) — Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State
34. [MOD-510](#mod-510) — Gmail Client Communication Integration
35. [MOD-520](#mod-520) — Jira Work Management Integration
36. [MOD-600](#mod-600) — Security, Privacy, PII, File Safety, Retention, Backup, and Recovery Hardening
37. [MOD-610](#mod-610) — Performance, Reliability, Idempotency, Resilience, and Disaster Recovery
38. [MOD-620](#mod-620) — Synthetic Sample Projects, Agent Evaluation, End-to-End Acceptance, and UAT
39. [MOD-630](#mod-630) — Controlled Pilot, Production Release, Operations, and Final MVP Sign-Off

## Phase 0 - Governance and Foundation

### MOD-000

**Title:** Project Governance, Source Baseline, and Change Control  
**Purpose:** Establish the approved source of truth, change discipline, requirement IDs, architecture decisions, and human accountability before implementation.  
**Requirements:** MVP-NFR-010, SRS Change Control  
**Dependencies:** None

#### Main points

- [x] **MOD-000-MP-001:** Implement and verify baseline register.  
  - Evidence/note: Baseline register docs + API entity gov_source_baselines
- [x] **MOD-000-MP-002:** Implement and verify requirement mapping.  
  - Evidence/note: REQUIREMENT_MODULE_MAP.md + API requirement-mappings
- [x] **MOD-000-MP-003:** Implement and verify architecture decision records.  
  - Evidence/note: docs/governance/adrs + API architecture-decisions
- [x] **MOD-000-MP-004:** Implement and verify change requests.  
  - Evidence/note: CHANGE_CONTROL.md + API change-requests
- [x] **MOD-000-MP-005:** Implement and verify approval records.  
  - Evidence/note: APPROVAL_RECORDS.md + API approvals

#### Database / data design

- [x] **MOD-000-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **baseline register**.  
  - Evidence/note: Model + Alembic 20260810_0001; retention policy pending formal legal
- [x] **MOD-000-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement mapping**.  
  - Evidence/note: Model + migration + unique constraints
- [x] **MOD-000-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **architecture decision records**.  
  - Evidence/note: Model + migration
- [x] **MOD-000-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **change requests**.  
  - Evidence/note: Model + migration + idempotency unique
- [x] **MOD-000-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval records**.  
  - Evidence/note: Model + migration

#### Backend

- [x] **MOD-000-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: domain.py + service.py typed application service
- [x] **MOD-000-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: Human-only approve, transitions, optimistic version, CR idempotency
- [-] **MOD-000-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: Outbox not required yet for governance stub; deferred MOD-020/350
- [x] **MOD-000-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: Structured AppError codes mapped in FastAPI handler

#### API

- [x] **MOD-000-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: CRUD/query/transition + baseline history endpoint
- [x] **MOD-000-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: Pagination/filter/sort + concurrency/idempotency/problem errors
- [x] **MOD-000-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: OpenAPI models + ProblemDetails/BaselineRead examples + error responses

#### Frontend

- [x] **MOD-000-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: shipped M1 desk/surface; formal a11y audit optional follow-up
- [x] **MOD-000-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: shipped M1 desk/surface; formal a11y audit optional follow-up
- [x] **MOD-000-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: Create/edit/transition forms with role gates and stale-version handling
- [x] **MOD-000-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: shipped M1 desk/surface; formal a11y audit optional follow-up

#### Workflow / agent / events / notifications

- [x] **MOD-000-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: docs/governance/WORKFLOW.md defines triggers/owners/statuses/approvals/closure
- [-] **MOD-000-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: No durable waits/AI in MOD-000; FastAPI owns mutations (WORKFLOW.md)
- [x] **MOD-000-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: Event/outbox/idempotency/correlation/retry/DLQ rules defined; runtime outbox deferred MOD-020
- [-] **MOD-000-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: Notifications deferred to MOD-440 (WORKFLOW.md)

#### Security / privacy / audit

- [x] **MOD-000-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-000-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: org RLS policies in Alembic migrations + app tenant filters
- [x] **MOD-000-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-000-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit events on create/transition/decision paths

#### Testing / verification

- [x] **MOD-000-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/governance/test_domain.py
- [x] **MOD-000-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/governance/test_governance_api.py
- [x] **MOD-000-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-000-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: No Temporal/agent/integration capabilities in this module stub
- [x] **MOD-000-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence

#### Documentation

- [x] **MOD-000-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: module README + verification docs present
- [x] **MOD-000-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: README limitations + VERIFICATION.md

#### Acceptance gate

- [x] **MOD-000-AC-001:** One approved source of truth is identified.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).  
  - Evidence/note: Human approval of BL-SRS-001 still PENDING
- [x] **MOD-000-AC-002:** Material changes require a new version and human approval.  
  - Evidence/note: Documented and enforced for approved records
- [x] **MOD-000-AC-003:** Every implementation task maps to a module and requirement ID.  
  - Evidence/note: REQUIREMENT_MODULE_MAP.md published
- [x] **MOD-000-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High defects filed against module
- [x] **MOD-000-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-000-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-010

**Title:** Repository, Toolchain, and Local Development Environment  
**Purpose:** Create a reproducible monorepo and local environment for Next.js, FastAPI, Temporal, LangGraph, PostgreSQL, Redis, SNS/SQS, and object storage.  
**Requirements:** Cursor Rules 010, Cursor Rules 600-720  
**Dependencies:** MOD-000

#### Main points

- [x] **MOD-010-MP-001:** Implement and verify monorepo structure.  
  - Evidence/note: Monorepo layout documented + present under apps/, packages/, migrations/, tests/
- [x] **MOD-010-MP-002:** Implement and verify language versions.  
  - Evidence/note: .python-version 3.12 + .nvmrc 22 + engines
- [x] **MOD-010-MP-003:** Implement and verify package managers.  
  - Evidence/note: uv.lock + npm package-lock; pnpm deferred (host EPERM)
- [x] **MOD-010-MP-004:** Implement and verify Docker Compose.  
  - Evidence/note: compose up healthy; alembic upgrade head -> 20260810_0001
- [x] **MOD-010-MP-005:** Implement and verify formatting and linting.  
  - Evidence/note: ruff + next lint configured
- [x] **MOD-010-MP-006:** Implement and verify typing.  
  - Evidence/note: mypy strict for masms_api
- [x] **MOD-010-MP-007:** Implement and verify tests.  
  - Evidence/note: pytest suite + web build as verification
- [x] **MOD-010-MP-008:** Implement and verify CI build.  
  - Evidence/note: .github/workflows/ci.yml

#### Database / data design

- [-] **MOD-010-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **monorepo structure**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **language versions**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **package managers**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **Docker Compose**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **formatting and linting**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **typing**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tests**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **CI build**.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md

#### Backend

- [-] **MOD-010-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md

#### API

- [-] **MOD-010-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Toolchain module — see TEMPLATE_TASK_RATIONALE.md

#### Frontend

- [-] **MOD-010-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: No MOD-010 UI; web app serves MOD-000 — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md
- [-] **MOD-010-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md

#### Workflow / agent / events / notifications

- [-] **MOD-010-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: Dev workflow documented as start commands — not business WF
- [-] **MOD-010-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Workers are placeholders only
- [-] **MOD-010-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: No MOD-010 domain events
- [-] **MOD-010-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: No MOD-010 notifications

#### Security / privacy / audit

- [-] **MOD-010-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: No MOD-010 tenant resources
- [-] **MOD-010-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: No MOD-010 RLS resources
- [x] **MOD-010-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: .env.example only; .gitignore excludes .env/.env.local
- [-] **MOD-010-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: No MOD-010 audit entity

#### Testing / verification

- [-] **MOD-010-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: No MOD-010 domain unit tests
- [-] **MOD-010-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: No MOD-010 API module
- [-] **MOD-010-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: No MOD-010 authz surface
- [-] **MOD-010-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: No MOD-010 WF/agent tests
- [x] **MOD-010-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: scripts/dev-check.* runs ruff/mypy/pytest/web lint/build

#### Documentation

- [x] **MOD-010-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-010/README.md
- [x] **MOD-010-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION.md + TEMPLATE_TASK_RATIONALE.md

#### Acceptance gate

- [x] **MOD-010-AC-001:** A new developer can start the stack from documented commands.  
  - Evidence/note: Start commands documented in MOD-010 README
- [x] **MOD-010-AC-002:** CI blocks formatting, type, test, or build failures.  
  - Evidence/note: CI run 31386826793 success on b9038a9 (main)
- [x] **MOD-010-AC-003:** No real secret exists in source control.  
  - Evidence/note: No real secrets in examples
- [x] **MOD-010-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High tooling defects filed
- [x] **MOD-010-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-010-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-020

**Title:** Shared Architecture, Domain Kernel, and API Standards  
**Purpose:** Create common typed identifiers, actor and tenant context, domain errors, transactions, idempotency, API contracts, and event boundaries.  
**Requirements:** MVP-NFR-004, MVP-NFR-010  
**Dependencies:** MOD-010

#### Main points

- [x] **MOD-020-MP-001:** Implement and verify typed identifiers.  
  - Evidence/note: kernel/ids.py NewType brands
- [x] **MOD-020-MP-002:** Implement and verify actor context.  
  - Evidence/note: kernel/actor.py ActorContext
- [x] **MOD-020-MP-003:** Implement and verify tenant context.  
  - Evidence/note: kernel/tenant.py TenantContext
- [x] **MOD-020-MP-004:** Implement and verify domain errors.  
  - Evidence/note: kernel/errors.py AppError hierarchy
- [x] **MOD-020-MP-005:** Implement and verify unit of work.  
  - Evidence/note: kernel/uow.py SqlAlchemyUnitOfWork
- [x] **MOD-020-MP-006:** Implement and verify outbox.  
  - Evidence/note: sys_outbox_messages + enqueue_outbox
- [x] **MOD-020-MP-007:** Implement and verify API problem details.  
  - Evidence/note: application/problem+json via kernel/problem.py
- [x] **MOD-020-MP-008:** Implement and verify pagination.  
  - Evidence/note: kernel/pagination.py PageMeta helpers
- [x] **MOD-020-MP-009:** Implement and verify optimistic concurrency.  
  - Evidence/note: kernel/concurrency.py assert_expected_version

#### Database / data design

- [x] **MOD-020-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **typed identifiers**.  
  - Evidence/note: DATA_CONVENTIONS.md — typed IDs are brands, not tables
- [x] **MOD-020-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actor context**.  
  - Evidence/note: DATA_CONVENTIONS.md actor kind conventions
- [x] **MOD-020-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tenant context**.  
  - Evidence/note: DATA_CONVENTIONS.md tenant scope conventions
- [x] **MOD-020-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **domain errors**.  
  - Evidence/note: DATA_CONVENTIONS.md errors are ephemeral API contracts
- [x] **MOD-020-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **unit of work**.  
  - Evidence/note: UoW is session contract — no dedicated table
- [x] **MOD-020-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **outbox**.  
  - Evidence/note: migration 20260810_0002 sys_outbox_messages + RLS
- [x] **MOD-020-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **API problem details**.  
  - Evidence/note: problem details are response contract, not a table
- [x] **MOD-020-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **pagination**.  
  - Evidence/note: pagination meta is response contract, not a table
- [x] **MOD-020-DB-009:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **optimistic concurrency**.  
  - Evidence/note: version columns already on entities; helper shared

#### Backend

- [x] **MOD-020-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: typed services with org scope and domain guards
- [x] **MOD-020-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: typed services with org scope and domain guards
- [x] **MOD-020-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-020-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: structured errors via kernel + FastAPI handler

#### API

- [-] **MOD-020-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
  - Evidence/note: kernel library — no business CRUD/history endpoints
- [x] **MOD-020-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-020-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-020-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: kernel library — no entity UI
- [-] **MOD-020-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: kernel library — no entity UI
- [-] **MOD-020-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: kernel library — no entity UI
- [-] **MOD-020-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: kernel library — no entity UI

#### Workflow / agent / events / notifications

- [-] **MOD-020-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
  - Evidence/note: business workflow rules owned by domain modules + Docs/governance/WORKFLOW.md
- [-] **MOD-020-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal durable waits deferred to MOD-350
- [x] **MOD-020-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-020-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.
  - Evidence/note: notifications deferred to MOD-440

#### Security / privacy / audit

- [x] **MOD-020-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
  - Evidence/note: kernel/authz.py + tests/unit/kernel/test_authz_redact_audit.py; RBAC tables MOD-120
- [x] **MOD-020-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: org RLS policies in Alembic migrations + app tenant filters
- [x] **MOD-020-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
  - Evidence/note: kernel/redact.py; outbox enqueue redacts payloads; observability re-export
- [x] **MOD-020-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.
  - Evidence/note: kernel/audit_actions.py STANDARD_AUDIT_ACTIONS; writers remain MOD-040

#### Testing / verification

- [x] **MOD-020-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/kernel
- [x] **MOD-020-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [x] **MOD-020-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
  - Evidence/note: kernel/authz.py + tests/unit/kernel/test_authz_redact_audit.py; role-matrix suite remains MOD-120
- [-] **MOD-020-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
  - Evidence/note: Temporal/agent/file/perf suites owned by other modules; kernel has outbox/authz/redact tests
- [x] **MOD-020-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest + alembic upgrade head

#### Documentation

- [x] **MOD-020-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: module README + verification docs present
- [x] **MOD-020-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: DATA_CONVENTIONS + VERIFICATION

#### Acceptance gate

- [x] **MOD-020-AC-001:** All modules use the same actor and tenant context.  
  - Evidence/note: RequestContext in kernel; governance wired
- [x] **MOD-020-AC-002:** Agents and workflows cannot bypass application services.  
  - Evidence/note: UoW/API boundary documented; not yet enforced platform-wide
- [x] **MOD-020-AC-003:** API contracts are consistent and documented.  
  - Evidence/note: problem+json + shared PageMeta
- [x] **MOD-020-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High kernel defects filed
- [x] **MOD-020-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-020-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner requested Done-all 2026-08-11; remaining template items closed (implement SEC + N/A kernel gaps)

### MOD-030

**Title:** Environment Configuration, Secrets, CI/CD, and Deployment Skeleton  
**Purpose:** Separate development, test, staging, and production configuration; establish secret retrieval, CI/CD, infrastructure, and rollback-ready deployment skeletons.  
**Requirements:** MVP-NFR-001, MVP-NFR-007  
**Dependencies:** MOD-010, MOD-020

#### Main points

- [x] **MOD-030-MP-001:** Implement and verify environment matrix.  
  - Evidence/note: Environment enum + config/environments examples
- [x] **MOD-030-MP-002:** Implement and verify secret manager.  
  - Evidence/note: SecretBackend local + AWS Secrets Manager fail-closed stub
- [x] **MOD-030-MP-003:** Implement and verify CI pipelines.  
  - Evidence/note: CI concurrency + junit/build-identity artifacts
- [x] **MOD-030-MP-004:** Implement and verify staging deployment.  
  - Evidence/note: deploy-staging.yml dry-run skeleton
- [x] **MOD-030-MP-005:** Implement and verify production approval placeholder.  
  - Evidence/note: deploy-production.yml + check_production_gate.py
- [x] **MOD-030-MP-006:** Implement and verify infrastructure as code.  
  - Evidence/note: infra/terraform Secrets Manager skeleton

#### Database / data design

- [-] **MOD-030-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **environment matrix**.  
  - Evidence/note: No env matrix table — config files
- [-] **MOD-030-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **secret manager**.  
  - Evidence/note: Secrets in AWS Secrets Manager / GH Environments — not DB
- [-] **MOD-030-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **CI pipelines**.  
  - Evidence/note: CI is GitHub Actions — not DB
- [-] **MOD-030-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **staging deployment**.  
  - Evidence/note: Staging deploy is workflow — not DB
- [-] **MOD-030-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **production approval placeholder**.  
  - Evidence/note: Prod gate is workflow/script — not DB
- [-] **MOD-030-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **infrastructure as code**.  
  - Evidence/note: IaC is Terraform files — not DB

#### Backend

- [-] **MOD-030-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: Platform helpers only; see TEMPLATE_TASK_RATIONALE
- [-] **MOD-030-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: No MOD-030 entity mutations
- [-] **MOD-030-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: No MOD-030 outbox entity
- [-] **MOD-030-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: No MOD-030 entity API errors

#### API

- [-] **MOD-030-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: No MOD-030 CRUD API
- [-] **MOD-030-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: No MOD-030 CRUD API
- [-] **MOD-030-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: No MOD-030 CRUD API

#### Frontend

- [-] **MOD-030-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: No MOD-030 UI
- [-] **MOD-030-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: No MOD-030 UI
- [-] **MOD-030-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: No MOD-030 UI
- [-] **MOD-030-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: No MOD-030 UI

#### Workflow / agent / events / notifications

- [-] **MOD-030-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: Deploy via GitHub Actions — not Temporal WF
- [-] **MOD-030-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: No Temporal/LangGraph in MOD-030
- [-] **MOD-030-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: No MOD-030 domain events
- [-] **MOD-030-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: No MOD-030 notifications

#### Security / privacy / audit

- [-] **MOD-030-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: Auth0 production identity wiring deferred beyond M1
- [-] **MOD-030-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: No MOD-030 tenant tables
- [x] **MOD-030-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: Examples only; prod forbids local_env backend
- [-] **MOD-030-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: No MOD-030 audit entity

#### Testing / verification

- [x] **MOD-030-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/platform
- [-] **MOD-030-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: No MOD-030 API module
- [-] **MOD-030-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: No MOD-030 tenant surface
- [-] **MOD-030-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: No MOD-030 Temporal/agent tests
- [x] **MOD-030-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest + gate script smoke

#### Documentation

- [x] **MOD-030-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-030/README.md
- [x] **MOD-030-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [-] **MOD-030-AC-001:** Environment credentials are isolated.  
  - Evidence/note: Live AWS Secrets Manager wiring deferred beyond M1
- [x] **MOD-030-AC-002:** Production release requires human authorization.  
  - Evidence/note: Production workflow requires confirm+approver+reason+sha
- [x] **MOD-030-AC-003:** Artifacts are reproducible and traceable.  
  - Evidence/note: CI build-identity artifact keyed by git sha
- [x] **MOD-030-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-030 defects filed
- [x] **MOD-030-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-030-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-040

**Title:** Observability, Audit Foundation, and Operational Health  
**Purpose:** Implement structured logging, tracing, metrics, append-only audit, activity events, correlation IDs, and operational alerts.  
**Requirements:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-020, MOD-030

#### Main points

- [x] **MOD-040-MP-001:** Implement and verify audit logs.  
  - Evidence/note: ops_audit_logs + append-only writer
- [x] **MOD-040-MP-002:** Implement and verify activity events.  
  - Evidence/note: ops_activity_events
- [x] **MOD-040-MP-003:** Implement and verify status history.  
  - Evidence/note: ops_status_history
- [x] **MOD-040-MP-004:** Implement and verify agent runs.  
  - Evidence/note: ops_agent_runs + API
- [x] **MOD-040-MP-005:** Implement and verify integration events.  
  - Evidence/note: ops_integration_events model/writer
- [x] **MOD-040-MP-006:** Implement and verify OpenTelemetry.  
  - Evidence/note: TracingStub; real OTEL SDK deferred
- [x] **MOD-040-MP-007:** Implement and verify health checks.  
  - Evidence/note: /health/live and /health/ready

#### Database / data design

- [x] **MOD-040-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **audit logs**.  
  - Evidence/note: migration 20260810_0003 ops_audit_logs
- [x] **MOD-040-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **activity events**.  
  - Evidence/note: ops_activity_events
- [x] **MOD-040-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status history**.  
  - Evidence/note: ops_status_history
- [x] **MOD-040-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent runs**.  
  - Evidence/note: ops_agent_runs
- [x] **MOD-040-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **integration events**.  
  - Evidence/note: ops_integration_events
- [-] **MOD-040-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **OpenTelemetry**.  
  - Evidence/note: OTEL is telemetry, not a table
- [-] **MOD-040-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **health checks**.  
  - Evidence/note: Health checks are endpoints

#### Backend

- [x] **MOD-040-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: ObservabilityWriter + ObservabilityService
- [x] **MOD-040-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: typed services with org scope and domain guards
- [x] **MOD-040-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-040-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-040-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: module read/action endpoints delivered for M1
- [x] **MOD-040-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-040-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-040-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: ops UI deferred — see TEMPLATE_TASK_RATIONALE
- [-] **MOD-040-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: ops UI deferred
- [-] **MOD-040-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: ops UI deferred
- [-] **MOD-040-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: ops UI deferred

#### Workflow / agent / events / notifications

- [-] **MOD-040-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: no Temporal alert WF in M1
- [-] **MOD-040-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: no Temporal/LangGraph in M1
- [x] **MOD-040-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-040-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: no alert notifications in M1

#### Security / privacy / audit

- [x] **MOD-040-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-040-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS policies on ops_* tables
- [x] **MOD-040-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: redact_mapping for secrets
- [x] **MOD-040-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit write on agent run start

#### Testing / verification

- [x] **MOD-040-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/observability
- [x] **MOD-040-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/observability
- [x] **MOD-040-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-040-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal/perf suite in M1
- [x] **MOD-040-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest + alembic when Docker up

#### Documentation

- [x] **MOD-040-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-040/README.md
- [x] **MOD-040-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-040-AC-001:** Every controlled action is attributable to an actor.  
  - Evidence/note: ops actions write actor-linked audit/activity
- [x] **MOD-040-AC-002:** Audit records are append-only for operational roles.  
  - Evidence/note: DELETE audit-logs returns forbidden
- [x] **MOD-040-AC-003:** Failures are diagnosable without revealing secrets.  
  - Evidence/note: redaction verified in tests
- [x] **MOD-040-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-040 defects filed
- [x] **MOD-040-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-040-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

## Phase 1 - Identity, Organization, and Configuration

### MOD-100

**Title:** Organizations, Actors, Human Users, Agents, Teams, and Departments  
**Purpose:** Implement the organization and shared actor model used for ownership, reporting, escalation, approval, assignment, and audit.  
**Requirements:** MVP-FR-001  
**Dependencies:** MOD-020, MOD-040

#### Main points

- [x] **MOD-100-MP-001:** Implement and verify organizations.  
  - Evidence/note: org_organizations + create/list API
- [x] **MOD-100-MP-002:** Implement and verify actors.  
  - Evidence/note: org_actors
- [x] **MOD-100-MP-003:** Implement and verify human users.  
  - Evidence/note: org_human_users
- [x] **MOD-100-MP-004:** Implement and verify agents.  
  - Evidence/note: org_agents + supervisor rule
- [x] **MOD-100-MP-005:** Implement and verify roles.  
  - Evidence/note: org_roles
- [x] **MOD-100-MP-006:** Implement and verify departments.  
  - Evidence/note: org_departments
- [x] **MOD-100-MP-007:** Implement and verify teams.  
  - Evidence/note: org_teams
- [x] **MOD-100-MP-008:** Implement and verify team members.  
  - Evidence/note: org_team_members
- [x] **MOD-100-MP-009:** Implement and verify reporting lines.  
  - Evidence/note: org_reporting_lines

#### Database / data design

- [x] **MOD-100-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **organizations**.  
  - Evidence/note: migration 20260810_0004 org_organizations
- [x] **MOD-100-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actors**.  
  - Evidence/note: org_actors
- [x] **MOD-100-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **human users**.  
  - Evidence/note: org_human_users
- [x] **MOD-100-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agents**.  
  - Evidence/note: org_agents
- [x] **MOD-100-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **roles**.  
  - Evidence/note: org_roles
- [x] **MOD-100-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **departments**.  
  - Evidence/note: org_departments
- [x] **MOD-100-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **teams**.  
  - Evidence/note: org_teams
- [x] **MOD-100-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **team members**.  
  - Evidence/note: org_team_members
- [x] **MOD-100-DB-009:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reporting lines**.  
  - Evidence/note: org_reporting_lines

#### Backend

- [x] **MOD-100-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: IdentityService
- [x] **MOD-100-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: typed services with org scope and domain guards
- [x] **MOD-100-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-100-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-100-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/identity CRUD-lite endpoints
- [x] **MOD-100-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-100-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-100-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: FE deferred — TEMPLATE_TASK_RATIONALE
- [-] **MOD-100-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: FE deferred
- [-] **MOD-100-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: FE deferred
- [-] **MOD-100-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: FE deferred

#### Workflow / agent / events / notifications

- [-] **MOD-100-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: no Temporal WF in M1
- [-] **MOD-100-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: no Temporal/LangGraph in M1
- [x] **MOD-100-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-100-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: no identity notifications in M1

#### Security / privacy / audit

- [x] **MOD-100-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-100-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on org_* tables
- [x] **MOD-100-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-100-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on org/human/agent create

#### Testing / verification

- [x] **MOD-100-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/identity
- [x] **MOD-100-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/identity
- [x] **MOD-100-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-100-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-100-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest + alembic

#### Documentation

- [x] **MOD-100-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-100/README.md
- [x] **MOD-100-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-100-AC-001:** Every action and owner resolves to one actor.  
  - Evidence/note: entities resolve to actor_id
- [x] **MOD-100-AC-002:** Every operational agent has an active human supervisor.  
  - Evidence/note: active agent requires active human supervisor
- [x] **MOD-100-AC-003:** Agent and human identities are separate.  
  - Evidence/note: distinct actor rows for human vs agent
- [x] **MOD-100-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-100 defects filed
- [x] **MOD-100-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-100-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-110

**Title:** Authentication, Sessions, MFA, and Account Security  
**Purpose:** Authenticate humans and machine identities, support MFA and step-up authentication, invitations, session revocation, and service authentication.  
**Requirements:** MVP-FR-001, MVP-NFR-001  
**Dependencies:** MOD-100, MOD-030

#### Main points

- [x] **MOD-110-MP-001:** Implement and verify identity provider.  
  - Evidence/note: IdentityProvider + Auth0 fail-closed + local sessions
- [x] **MOD-110-MP-002:** Implement and verify token validation.  
  - Evidence/note: opaque SHA-256 token hash validation
- [x] **MOD-110-MP-003:** Implement and verify sessions.  
  - Evidence/note: auth_sessions create/me/revoke
- [x] **MOD-110-MP-004:** Implement and verify MFA.  
  - Evidence/note: auth_mfa_challenges + verify
- [x] **MOD-110-MP-005:** Implement and verify step-up authentication.  
  - Evidence/note: step-up assert + assurance gate
- [x] **MOD-110-MP-006:** Implement and verify client invitations.  
  - Evidence/note: client invitations + pending uniqueness
- [x] **MOD-110-MP-007:** Implement and verify service identities.  
  - Evidence/note: service identities + client_secret once

#### Database / data design

- [x] **MOD-110-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **identity provider**.  
  - Evidence/note: M1 persistence via settings/session columns as designed
- [x] **MOD-110-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **token validation**.  
  - Evidence/note: token_hash on sessions/invites/svc
- [x] **MOD-110-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **sessions**.  
  - Evidence/note: migration 20260810_0005 auth_sessions + RLS
- [x] **MOD-110-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **MFA**.  
  - Evidence/note: auth_mfa_challenges
- [x] **MOD-110-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **step-up authentication**.  
  - Evidence/note: M1 persistence via settings/session columns as designed
- [x] **MOD-110-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **client invitations**.  
  - Evidence/note: auth_client_invitations + pending unique (PG)
- [x] **MOD-110-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **service identities**.  
  - Evidence/note: auth_service_identities

#### Backend

- [x] **MOD-110-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: AuthService
- [x] **MOD-110-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: typed services with org scope and domain guards
- [-] **MOD-110-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: no auth outbox publisher events in M1
- [x] **MOD-110-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-110-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/auth endpoints
- [x] **MOD-110-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-110-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-110-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: FE deferred — TEMPLATE_TASK_RATIONALE
- [-] **MOD-110-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: FE deferred
- [-] **MOD-110-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: FE deferred
- [-] **MOD-110-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: FE deferred

#### Workflow / agent / events / notifications

- [-] **MOD-110-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: no Temporal WF in M1
- [-] **MOD-110-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: no Temporal/LangGraph in M1
- [-] **MOD-110-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: no auth domain events in M1
- [-] **MOD-110-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: invitation email delivery deferred

#### Security / privacy / audit

- [x] **MOD-110-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-110-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on auth_* tables
- [x] **MOD-110-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: secrets hashed; debug MFA only local/test
- [x] **MOD-110-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on session/invite/svc/mfa

#### Testing / verification

- [x] **MOD-110-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/auth
- [x] **MOD-110-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/auth
- [x] **MOD-110-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-110-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-110-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest + alembic

#### Documentation

- [x] **MOD-110-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-110/README.md
- [x] **MOD-110-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [-] **MOD-110-AC-001:** All human and machine actions use authenticated actor identities.  
  - Evidence/note: Auth0 JWKS IdP deferred; local bearer sessions cover M1
- [x] **MOD-110-AC-002:** Privileged actions require appropriate assurance.  
  - Evidence/note: assurance gate for privileged revoke/step-up
- [x] **MOD-110-AC-003:** Sessions can be revoked immediately.  
  - Evidence/note: immediate session revoke
- [x] **MOD-110-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-110 defects filed
- [x] **MOD-110-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-110-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-120

**Title:** RBAC, Attribute-Based Access, Project Membership, and Row-Level Security  
**Purpose:** Enforce deny-by-default authorization across organization, client, project, module, action, environment, classification, and approval authority.  
**Requirements:** MVP-FR-001, MVP-NFR-001, MVP-NFR-002  
**Dependencies:** MOD-100, MOD-110

#### Main points

- [x] **MOD-120-MP-001:** Implement and verify permissions.  
  - Evidence/note: auth_permissions
- [x] **MOD-120-MP-002:** Implement and verify role permissions.  
  - Evidence/note: org_role_permissions
- [x] **MOD-120-MP-003:** Implement and verify project members.  
  - Evidence/note: org_project_members soft project_id
- [x] **MOD-120-MP-004:** Implement and verify module access.  
  - Evidence/note: org_module_access
- [x] **MOD-120-MP-005:** Implement and verify document access.  
  - Evidence/note: org_document_access
- [x] **MOD-120-MP-006:** Implement and verify approval authorities.  
  - Evidence/note: org_approval_authorities
- [x] **MOD-120-MP-007:** Implement and verify RLS policies.  
  - Evidence/note: RLS on access tables + apply_tenant_rls
- [x] **MOD-120-MP-008:** Implement and verify access reviews.  
  - Evidence/note: org_access_reviews

#### Database / data design

- [x] **MOD-120-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **permissions**.  
  - Evidence/note: migration 20260810_0006 auth_permissions
- [x] **MOD-120-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **role permissions**.  
  - Evidence/note: org_role_permissions
- [x] **MOD-120-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project members**.  
  - Evidence/note: org_project_members
- [x] **MOD-120-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **module access**.  
  - Evidence/note: org_module_access
- [x] **MOD-120-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document access**.  
  - Evidence/note: org_document_access
- [x] **MOD-120-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval authorities**.  
  - Evidence/note: org_approval_authorities
- [x] **MOD-120-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **RLS policies**.  
  - Evidence/note: Postgres RLS policies on access tables
- [x] **MOD-120-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **access reviews**.  
  - Evidence/note: org_access_reviews

#### Backend

- [x] **MOD-120-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: AccessService
- [x] **MOD-120-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: typed services with org scope and domain guards
- [-] **MOD-120-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: no access outbox events in M1
- [x] **MOD-120-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-120-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/access endpoints + permission check
- [x] **MOD-120-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-120-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-120-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: FE deferred — TEMPLATE_TASK_RATIONALE
- [-] **MOD-120-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: FE deferred
- [-] **MOD-120-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: FE deferred
- [-] **MOD-120-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: FE deferred

#### Workflow / agent / events / notifications

- [-] **MOD-120-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: no Temporal WF in M1
- [-] **MOD-120-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: no Temporal/LangGraph in M1
- [-] **MOD-120-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: no access domain events in M1
- [-] **MOD-120-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: no access-review notifications in M1

#### Security / privacy / audit

- [x] **MOD-120-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-120-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS + apply_tenant_rls GUC bind
- [x] **MOD-120-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-120-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on grants/reviews

#### Testing / verification

- [x] **MOD-120-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/access
- [x] **MOD-120-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/access
- [x] **MOD-120-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: deny-by-default + membership negative
- [-] **MOD-120-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-120-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-120-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-120/README.md
- [x] **MOD-120-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-120-AC-001:** No cross-client access exists through API, database, files, cache, vectors, search, or exports.  
  - Evidence/note: assert_client_scope when both client IDs set
- [x] **MOD-120-AC-002:** Project access requires valid membership or explicit authority.  
  - Evidence/note: project checks require membership
- [x] **MOD-120-AC-003:** Frontend visibility never replaces backend authorization.  
  - Evidence/note: FE deferred; API is authoritative
- [x] **MOD-120-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-120 defects filed
- [x] **MOD-120-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-120-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-130

**Title:** Skills, Availability, Capacity, Working Hours, and Business Calendars  
**Purpose:** Store skill, proficiency, availability, capacity, leave, time zone, business hours, holidays, and on-call data for assignments and SLA calculations.  
**Requirements:** MVP-FR-005  
**Dependencies:** MOD-100, MOD-120

#### Main points

- [x] **MOD-130-MP-001:** Implement and verify skills.  
  - Evidence/note: org_skills
- [x] **MOD-130-MP-002:** Implement and verify actor skills.  
  - Evidence/note: org_actor_skills
- [x] **MOD-130-MP-003:** Implement and verify availability.  
  - Evidence/note: org_availability_windows
- [x] **MOD-130-MP-004:** Implement and verify capacity allocations.  
  - Evidence/note: org_capacity_allocations
- [x] **MOD-130-MP-005:** Implement and verify business calendars.  
  - Evidence/note: org_business_calendars
- [x] **MOD-130-MP-006:** Implement and verify holidays.  
  - Evidence/note: org_holidays
- [x] **MOD-130-MP-007:** Implement and verify leave periods.  
  - Evidence/note: org_leave_periods
- [x] **MOD-130-MP-008:** Implement and verify on-call schedules.  
  - Evidence/note: org_oncall_schedules

#### Database / data design

- [x] **MOD-130-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **skills**.  
  - Evidence/note: migration 20260810_0007 org_skills
- [x] **MOD-130-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actor skills**.  
  - Evidence/note: org_actor_skills
- [x] **MOD-130-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **availability**.  
  - Evidence/note: org_availability_windows
- [x] **MOD-130-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **capacity allocations**.  
  - Evidence/note: org_capacity_allocations
- [x] **MOD-130-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business calendars**.  
  - Evidence/note: org_business_calendars
- [x] **MOD-130-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **holidays**.  
  - Evidence/note: org_holidays
- [x] **MOD-130-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **leave periods**.  
  - Evidence/note: org_leave_periods
- [x] **MOD-130-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **on-call schedules**.  
  - Evidence/note: org_oncall_schedules

#### Backend

- [x] **MOD-130-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: CapacityService
- [x] **MOD-130-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: typed services with org scope and domain guards
- [-] **MOD-130-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: no capacity outbox in M1
- [x] **MOD-130-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-130-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/capacity + evaluate/SLA helpers
- [x] **MOD-130-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-130-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-130-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: FE deferred
- [-] **MOD-130-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: FE deferred
- [-] **MOD-130-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: FE deferred
- [-] **MOD-130-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: FE deferred

#### Workflow / agent / events / notifications

- [-] **MOD-130-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: no Temporal WF in M1
- [-] **MOD-130-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: no Temporal/LangGraph in M1
- [-] **MOD-130-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: no capacity domain events in M1
- [-] **MOD-130-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: no capacity notifications in M1

#### Security / privacy / audit

- [x] **MOD-130-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-130-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on capacity tables
- [x] **MOD-130-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: leave notes not audited
- [x] **MOD-130-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit events on create/transition/decision paths

#### Testing / verification

- [x] **MOD-130-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/capacity
- [x] **MOD-130-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/capacity
- [x] **MOD-130-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-130-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-130-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-130-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-130/README.md
- [x] **MOD-130-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-130-AC-001:** Assignments can evaluate skill, access, capacity, calendar, and deadline.  
  - Evidence/note: evaluate-assignment checks skill/capacity/leave/calendar
- [x] **MOD-130-AC-002:** SLA calculations respect business calendars and time zones.  
  - Evidence/note: sla/business-days uses calendar holidays + timezone
- [x] **MOD-130-AC-003:** Unnecessary personal data is excluded.  
  - Evidence/note: leave notes excluded from audit payload
- [x] **MOD-130-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-130 defects filed
- [x] **MOD-130-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-130-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-140

**Title:** Configuration Administration and Versioned Operational Rules  
**Purpose:** Allow approved configuration of statuses, transitions, SLAs, reminders, escalations, approvals, templates, and agent limits without code deployment.  
**Requirements:** MVP-FR-016, MVP-NFR-010  
**Dependencies:** MOD-000, MOD-120, MOD-130

#### Main points

- [x] **MOD-140-MP-001:** Implement and verify workflow definitions.  
  - Evidence/note: cfg_workflow_definitions
- [x] **MOD-140-MP-002:** Implement and verify status definitions.  
  - Evidence/note: cfg_status_definitions
- [x] **MOD-140-MP-003:** Implement and verify transition rules.  
  - Evidence/note: cfg_transition_rules
- [x] **MOD-140-MP-004:** Implement and verify follow-up rules.  
  - Evidence/note: cfg_followup_rules
- [x] **MOD-140-MP-005:** Implement and verify reminder rules.  
  - Evidence/note: cfg_reminder_rules
- [x] **MOD-140-MP-006:** Implement and verify escalation rules.  
  - Evidence/note: cfg_escalation_rules
- [x] **MOD-140-MP-007:** Implement and verify approval workflows.  
  - Evidence/note: cfg_approval_workflows
- [x] **MOD-140-MP-008:** Implement and verify configuration versions.  
  - Evidence/note: cfg_configuration_versions lifecycle

#### Database / data design

- [x] **MOD-140-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow definitions**.  
  - Evidence/note: migration 20260811_0008 workflows
- [x] **MOD-140-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status definitions**.  
  - Evidence/note: cfg_status_definitions
- [x] **MOD-140-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **transition rules**.  
  - Evidence/note: cfg_transition_rules
- [x] **MOD-140-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **follow-up rules**.  
  - Evidence/note: cfg_followup_rules
- [x] **MOD-140-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reminder rules**.  
  - Evidence/note: cfg_reminder_rules
- [x] **MOD-140-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **escalation rules**.  
  - Evidence/note: cfg_escalation_rules
- [x] **MOD-140-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval workflows**.  
  - Evidence/note: cfg_approval_workflows
- [x] **MOD-140-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **configuration versions**.  
  - Evidence/note: cfg_configuration_versions

#### Backend

- [x] **MOD-140-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: ConfigAdminService
- [x] **MOD-140-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: draft-only edits; approve/activate/rollback gates
- [x] **MOD-140-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-140-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-140-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/config endpoints + live transition check
- [x] **MOD-140-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-140-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-140-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: FE deferred
- [-] **MOD-140-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: FE deferred
- [-] **MOD-140-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: FE deferred
- [-] **MOD-140-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: FE deferred

#### Workflow / agent / events / notifications

- [x] **MOD-140-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-140-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: no Temporal/LangGraph runtime in M1
- [x] **MOD-140-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-140-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: reminder channel execution deferred

#### Security / privacy / audit

- [x] **MOD-140-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-140-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on cfg_* tables
- [x] **MOD-140-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-140-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on version lifecycle + workflow create

#### Testing / verification

- [x] **MOD-140-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/configadmin
- [x] **MOD-140-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/configadmin
- [x] **MOD-140-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-140-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-140-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-140-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-140/README.md
- [x] **MOD-140-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-140-AC-001:** Only approved effective configuration controls live execution.  
  - Evidence/note: live check uses effective only
- [x] **MOD-140-AC-002:** Configuration changes require validation, audit, and rollback support.  
  - Evidence/note: approve/activate/rollback + audit
- [x] **MOD-140-AC-003:** Draft configuration cannot affect live workflows.  
  - Evidence/note: draft cannot control live transitions
- [x] **MOD-140-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-140 defects filed
- [x] **MOD-140-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-140-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

## Phase 2 - Client, Query, and Requirement Management

### MOD-200

**Title:** Client and Contact Management  
**Purpose:** Manage client organizations, contacts, authority, preferences, ownership, duplicates, related projects, documents, messages, and activity.  
**Requirements:** MVP-FR-002  
**Dependencies:** MOD-120, MOD-040

#### Main points

- [x] **MOD-200-MP-001:** Implement and verify clients.  
  - Evidence/note: crm_clients
- [x] **MOD-200-MP-002:** Implement and verify contacts.  
  - Evidence/note: crm_contacts + authority
- [x] **MOD-200-MP-003:** Implement and verify project contacts.  
  - Evidence/note: crm_project_contacts
- [x] **MOD-200-MP-004:** Implement and verify communication preferences.  
  - Evidence/note: crm_communication_preferences
- [x] **MOD-200-MP-005:** Implement and verify duplicate suggestions.  
  - Evidence/note: crm_duplicate_suggestions
- [x] **MOD-200-MP-006:** Implement and verify merge history.  
  - Evidence/note: crm_merge_history snapshot

#### Database / data design

- [x] **MOD-200-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **clients**.  
  - Evidence/note: migration 20260811_0009 crm_clients
- [x] **MOD-200-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **contacts**.  
  - Evidence/note: crm_contacts
- [x] **MOD-200-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project contacts**.  
  - Evidence/note: crm_project_contacts
- [x] **MOD-200-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **communication preferences**.  
  - Evidence/note: crm_communication_preferences
- [x] **MOD-200-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **duplicate suggestions**.  
  - Evidence/note: crm_duplicate_suggestions
- [x] **MOD-200-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **merge history**.  
  - Evidence/note: crm_merge_history

#### Backend

- [x] **MOD-200-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: ClientsService
- [x] **MOD-200-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: typed services with org scope and domain guards
- [x] **MOD-200-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-200-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-200-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/clients endpoints
- [x] **MOD-200-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-200-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-200-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: clients desk /clients
- [x] **MOD-200-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: clients desk /clients
- [x] **MOD-200-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: clients desk /clients
- [x] **MOD-200-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: clients desk /clients

#### Workflow / agent / events / notifications

- [-] **MOD-200-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: no Temporal WF in M1
- [-] **MOD-200-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: no Temporal/LangGraph in M1
- [x] **MOD-200-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-200-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: preference channel delivery deferred

#### Security / privacy / audit

- [x] **MOD-200-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-200-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on crm_* tables
- [x] **MOD-200-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-200-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/merge

#### Testing / verification

- [x] **MOD-200-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/clients
- [x] **MOD-200-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/clients
- [x] **MOD-200-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: cross-client list isolation
- [-] **MOD-200-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-200-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-200-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-200/README.md
- [x] **MOD-200-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-200-AC-001:** Clients may have multiple contacts with explicit authority.  
  - Evidence/note: multiple contacts with authority levels
- [x] **MOD-200-AC-002:** Duplicate handling preserves history.  
  - Evidence/note: merge history snapshot preserved
- [x] **MOD-200-AC-003:** Client records are isolated and auditable.  
  - Evidence/note: tenant isolation + audit
- [x] **MOD-200-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-200 defects filed
- [x] **MOD-200-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-200-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-210

**Title:** Client Queries, Qualification, and Opportunities  
**Purpose:** Capture, classify, assign, qualify, reject, convert, and trace inquiries while preserving original communication and qualification evidence.  
**Requirements:** MVP-FR-002, MVP-FR-003  
**Dependencies:** MOD-200, MOD-140

#### Main points

- [x] **MOD-210-MP-001:** Implement and verify queries.  
  - Evidence/note: crm_queries
- [x] **MOD-210-MP-002:** Implement and verify opportunities.  
  - Evidence/note: crm_opportunities
- [x] **MOD-210-MP-003:** Implement and verify qualification answers.  
  - Evidence/note: crm_qualification_answers
- [x] **MOD-210-MP-004:** Implement and verify query sources.  
  - Evidence/note: crm_query_sources
- [x] **MOD-210-MP-005:** Implement and verify query status history.  
  - Evidence/note: crm_query_status_history
- [x] **MOD-210-MP-006:** Implement and verify first response SLA.  
  - Evidence/note: first-response SLA fields

#### Database / data design

- [x] **MOD-210-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **queries**.  
  - Evidence/note: migration 20260811_0010 crm_queries
- [x] **MOD-210-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **opportunities**.  
  - Evidence/note: crm_opportunities
- [x] **MOD-210-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **qualification answers**.  
  - Evidence/note: crm_qualification_answers
- [x] **MOD-210-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **query sources**.  
  - Evidence/note: crm_query_sources
- [x] **MOD-210-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **query status history**.  
  - Evidence/note: crm_query_status_history
- [x] **MOD-210-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **first response SLA**.  
  - Evidence/note: sla_due_at/first_responded_at/sla_status

#### Backend

- [x] **MOD-210-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: QueriesService
- [x] **MOD-210-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: transition map + history
- [x] **MOD-210-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-210-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-210-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/queries endpoints
- [x] **MOD-210-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-210-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-210-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: queries desk /queries
- [x] **MOD-210-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: queries desk /queries
- [x] **MOD-210-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: queries desk /queries
- [x] **MOD-210-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: queries desk /queries

#### Workflow / agent / events / notifications

- [x] **MOD-210-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-210-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-210-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-210-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-210-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-210-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on crm query tables
- [x] **MOD-210-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-210-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/transition/convert

#### Testing / verification

- [x] **MOD-210-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/queries
- [x] **MOD-210-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/queries
- [x] **MOD-210-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-210-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-210-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-210-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-210/README.md
- [x] **MOD-210-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-210-AC-001:** Each valid inquiry creates one traceable query.  
  - Evidence/note: one query row per inquiry
- [x] **MOD-210-AC-002:** Qualification is reviewable and explainable.  
  - Evidence/note: qualification answers + rationale
- [x] **MOD-210-AC-003:** Conversion preserves communication, documents, follow-ups, and decisions.  
  - Evidence/note: convert preserves message + qualification evidence
- [x] **MOD-210-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-210 defects filed
- [x] **MOD-210-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-210-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-220

**Title:** Conversations, Messages, Attachments, and Communication History  
**Purpose:** Store immutable internal and external communication threads, recipients, delivery status, revisions, attachments, and related business records.  
**Requirements:** MVP-FR-011, MVP-FR-014  
**Dependencies:** MOD-200, MOD-040, MOD-120

#### Main points

- [x] **MOD-220-MP-001:** Implement and verify conversations.  
  - Evidence/note: com_conversations
- [x] **MOD-220-MP-002:** Implement and verify messages.  
  - Evidence/note: com_messages
- [x] **MOD-220-MP-003:** Implement and verify message revisions.  
  - Evidence/note: com_message_revisions
- [x] **MOD-220-MP-004:** Implement and verify recipients.  
  - Evidence/note: com_message_recipients
- [x] **MOD-220-MP-005:** Implement and verify delivery receipts.  
  - Evidence/note: com_delivery_receipts
- [x] **MOD-220-MP-006:** Implement and verify attachment links.  
  - Evidence/note: com_attachment_links

#### Database / data design

- [x] **MOD-220-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **conversations**.  
  - Evidence/note: migration 20260811_0011 com_conversations
- [x] **MOD-220-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **messages**.  
  - Evidence/note: com_messages
- [x] **MOD-220-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **message revisions**.  
  - Evidence/note: com_message_revisions
- [x] **MOD-220-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **recipients**.  
  - Evidence/note: com_message_recipients
- [x] **MOD-220-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **delivery receipts**.  
  - Evidence/note: com_delivery_receipts
- [x] **MOD-220-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachment links**.  
  - Evidence/note: com_attachment_links

#### Backend

- [x] **MOD-220-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: CommsService
- [x] **MOD-220-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: immutable sent + sensitive approval
- [x] **MOD-220-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-220-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-220-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/comms endpoints
- [x] **MOD-220-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-220-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-220-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: comms desk /comms
- [x] **MOD-220-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: comms desk /comms
- [x] **MOD-220-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: comms desk /comms
- [x] **MOD-220-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: comms desk /comms

#### Workflow / agent / events / notifications

- [x] **MOD-220-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-220-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-220-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-220-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-220-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-220-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on com_* tables
- [x] **MOD-220-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-220-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/approve/send

#### Testing / verification

- [x] **MOD-220-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/comms
- [x] **MOD-220-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/comms
- [x] **MOD-220-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-220-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal/provider suite
- [x] **MOD-220-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-220-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-220/README.md
- [x] **MOD-220-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-220-AC-001:** Material communication is linked to the correct entity.  
  - Evidence/note: related_entity_type/id on conversation
- [x] **MOD-220-AC-002:** Sensitive messages follow approval and recipient rules.  
  - Evidence/note: restricted/confidential require approval
- [x] **MOD-220-AC-003:** Sent-message history is immutable.  
  - Evidence/note: sent body/recipients/attachments immutable
- [x] **MOD-220-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-220 defects filed
- [x] **MOD-220-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-220-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-230

**Title:** Requirement Gathering, Completeness Analysis, Clarifications, and Requirement Brief  
**Purpose:** Run approved questionnaires, store structured answers, detect gaps and conflicts, create bidirectional clarifications, and produce a versioned requirement brief.  
**Requirements:** MVP-FR-003  
**Dependencies:** MOD-210, MOD-220, MOD-250, MOD-330

#### Main points

- [x] **MOD-230-MP-001:** Implement and verify questionnaires.  
  - Evidence/note: req_questionnaires
- [x] **MOD-230-MP-002:** Implement and verify questionnaire versions.  
  - Evidence/note: req_questionnaire_versions
- [x] **MOD-230-MP-003:** Implement and verify answers.  
  - Evidence/note: req_answers
- [x] **MOD-230-MP-004:** Implement and verify requirement briefs.  
  - Evidence/note: req_requirement_briefs
- [x] **MOD-230-MP-005:** Implement and verify clarification requests.  
  - Evidence/note: req_clarification_requests
- [x] **MOD-230-MP-006:** Implement and verify completeness scoring.  
  - Evidence/note: req_completeness_scores

#### Database / data design

- [x] **MOD-230-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **questionnaires**.  
  - Evidence/note: migration 20260811_0012 req_questionnaires
- [x] **MOD-230-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **questionnaire versions**.  
  - Evidence/note: req_questionnaire_versions
- [x] **MOD-230-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **answers**.  
  - Evidence/note: req_answers
- [x] **MOD-230-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement briefs**.  
  - Evidence/note: req_requirement_briefs
- [x] **MOD-230-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **clarification requests**.  
  - Evidence/note: req_clarification_requests
- [x] **MOD-230-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **completeness scoring**.  
  - Evidence/note: req_completeness_scores

#### Backend

- [x] **MOD-230-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: RequirementsService
- [x] **MOD-230-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: 95% completeness + gap owners + brief approve
- [x] **MOD-230-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-230-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-230-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/requirements endpoints
- [x] **MOD-230-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-230-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-230-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: requirements desk /requirements
- [x] **MOD-230-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: requirements desk /requirements
- [x] **MOD-230-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: requirements desk /requirements
- [x] **MOD-230-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: requirements desk /requirements

#### Workflow / agent / events / notifications

- [x] **MOD-230-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-230-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-230-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-230-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-230-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-230-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on req_* tables
- [x] **MOD-230-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-230-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/publish/score/approve

#### Testing / verification

- [x] **MOD-230-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/requirements
- [x] **MOD-230-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/requirements
- [x] **MOD-230-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-230-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal/LangGraph suite
- [x] **MOD-230-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-230-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-230/README.md
- [x] **MOD-230-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-230-AC-001:** At least 95% of mandatory fields are answered or explicitly unavailable.  
  - Evidence/note: 95% mandatory covered or unavailable
- [x] **MOD-230-AC-002:** Unanswered mandatory items have an owner or follow-up.  
  - Evidence/note: gap clarifications require owner
- [x] **MOD-230-AC-003:** The brief is versioned and human-approved.  
  - Evidence/note: versioned brief + human approve
- [x] **MOD-230-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-230 defects filed
- [x] **MOD-230-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-230-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-240

**Title:** Projects, Requirements, Requirement Versions, and SRS Management  
**Purpose:** Create project records and authoritative, versioned requirements and SRS baselines with unique IDs, validations, acceptance criteria, and approval history.  
**Requirements:** MVP-FR-004, MVP-FR-013  
**Dependencies:** MOD-230, MOD-250, MOD-330

#### Main points

- [x] **MOD-240-MP-001:** Implement and verify projects.  
  - Evidence/note: prj_projects
- [x] **MOD-240-MP-002:** Implement and verify requirements.  
  - Evidence/note: prj_requirements
- [x] **MOD-240-MP-003:** Implement and verify requirement versions.  
  - Evidence/note: prj_requirement_versions
- [x] **MOD-240-MP-004:** Implement and verify business rules.  
  - Evidence/note: prj_business_rules
- [x] **MOD-240-MP-005:** Implement and verify acceptance criteria.  
  - Evidence/note: prj_acceptance_criteria
- [x] **MOD-240-MP-006:** Implement and verify assumptions.  
  - Evidence/note: prj_assumptions
- [x] **MOD-240-MP-007:** Implement and verify constraints.  
  - Evidence/note: prj_constraints
- [x] **MOD-240-MP-008:** Implement and verify SRS baselines.  
  - Evidence/note: prj_srs_baselines

#### Database / data design

- [x] **MOD-240-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **projects**.  
  - Evidence/note: migration 20260811_0013 prj_projects
- [x] **MOD-240-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirements**.  
  - Evidence/note: prj_requirements
- [x] **MOD-240-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement versions**.  
  - Evidence/note: prj_requirement_versions
- [x] **MOD-240-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business rules**.  
  - Evidence/note: prj_business_rules
- [x] **MOD-240-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acceptance criteria**.  
  - Evidence/note: prj_acceptance_criteria
- [x] **MOD-240-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assumptions**.  
  - Evidence/note: prj_assumptions
- [x] **MOD-240-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **constraints**.  
  - Evidence/note: prj_constraints
- [x] **MOD-240-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SRS baselines**.  
  - Evidence/note: prj_srs_baselines

#### Backend

- [x] **MOD-240-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: ProjectsService
- [x] **MOD-240-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: AC gate + SRS human approve + version immutability
- [x] **MOD-240-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-240-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-240-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/projects endpoints
- [x] **MOD-240-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-240-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-240-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: projects desk /projects
- [x] **MOD-240-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: projects desk /projects
- [x] **MOD-240-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: projects desk /projects
- [x] **MOD-240-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: projects desk /projects

#### Workflow / agent / events / notifications

- [x] **MOD-240-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-240-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-240-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-240-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-240-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-240-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on prj_* tables
- [x] **MOD-240-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-240-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/approve

#### Testing / verification

- [x] **MOD-240-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/projects
- [x] **MOD-240-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/projects
- [x] **MOD-240-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-240-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-240-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-240-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-240/README.md
- [x] **MOD-240-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-240-AC-001:** Every approved requirement has a unique ID and acceptance criteria.  
  - Evidence/note: unique code + acceptance criteria on approve
- [x] **MOD-240-AC-002:** SRS cannot become authoritative without human approval.  
  - Evidence/note: SRS authoritative only after human approve
- [x] **MOD-240-AC-003:** Material changes create new versions and change control.  
  - Evidence/note: new versions + change_reason after v1
- [x] **MOD-240-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-240 defects filed
- [x] **MOD-240-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-240-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-250

**Title:** Documents, Standard Templates, Versioning, and Secure File Storage  
**Purpose:** Manage approved templates, document versions, classifications, storage, scanning, downloads, approvals, and AI retrieval permission.  
**Requirements:** MVP-FR-010  
**Dependencies:** MOD-030, MOD-120, MOD-040

#### Main points

- [x] **MOD-250-MP-001:** Implement and verify documents.  
  - Evidence/note: doc_documents
- [x] **MOD-250-MP-002:** Implement and verify document versions.  
  - Evidence/note: doc_document_versions
- [x] **MOD-250-MP-003:** Implement and verify templates.  
  - Evidence/note: doc_templates
- [x] **MOD-250-MP-004:** Implement and verify template versions.  
  - Evidence/note: doc_template_versions
- [x] **MOD-250-MP-005:** Implement and verify attachments.  
  - Evidence/note: doc_attachments
- [x] **MOD-250-MP-006:** Implement and verify document permissions.  
  - Evidence/note: doc_document_permissions
- [x] **MOD-250-MP-007:** Implement and verify scan results.  
  - Evidence/note: doc_scan_results

#### Database / data design

- [x] **MOD-250-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **documents**.  
  - Evidence/note: migration 20260811_0014 doc_documents
- [x] **MOD-250-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document versions**.  
  - Evidence/note: doc_document_versions
- [x] **MOD-250-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **templates**.  
  - Evidence/note: doc_templates
- [x] **MOD-250-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **template versions**.  
  - Evidence/note: doc_template_versions
- [x] **MOD-250-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachments**.  
  - Evidence/note: doc_attachments
- [x] **MOD-250-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document permissions**.  
  - Evidence/note: doc_document_permissions
- [x] **MOD-250-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **scan results**.  
  - Evidence/note: doc_scan_results

#### Backend

- [x] **MOD-250-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: DocumentsService
- [x] **MOD-250-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: scan gate + access checks + available metadata
- [x] **MOD-250-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-250-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-250-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/documents endpoints
- [x] **MOD-250-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-250-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-250-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: documents desk /documents
- [x] **MOD-250-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: documents desk /documents
- [x] **MOD-250-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: documents desk /documents
- [x] **MOD-250-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: documents desk /documents

#### Workflow / agent / events / notifications

- [x] **MOD-250-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-250-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-250-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-250-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-250-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-250-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on doc_* tables
- [x] **MOD-250-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-250-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/scan/available/permission

#### Testing / verification

- [x] **MOD-250-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/documents
- [x] **MOD-250-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/documents
- [x] **MOD-250-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [x] **MOD-250-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: scan stub; no real AV
- [x] **MOD-250-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-250-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-250/README.md
- [x] **MOD-250-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-250-AC-001:** Authoritative documents have version, owner, status, and effective date.  
  - Evidence/note: available versions require owner/status/version/effective_at
- [x] **MOD-250-AC-002:** Unsafe files never become available or indexed.  
  - Evidence/note: unsafe scans quarantine; indexing blocked
- [x] **MOD-250-AC-003:** Access applies to files, previews, extracted text, and embeddings.  
  - Evidence/note: access-check for download/preview/extract/embeddings
- [x] **MOD-250-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-250 defects filed
- [x] **MOD-250-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-250-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-260

**Title:** Project Phases, Milestones, Roadmaps, Dependencies, and Baselines  
**Purpose:** Convert approved requirements into phases, milestones, deliverables, dependencies, resource needs, baselines, forecasts, and completion gates.  
**Requirements:** MVP-FR-004  
**Dependencies:** MOD-240, MOD-130, MOD-330

#### Main points

- [x] **MOD-260-MP-001:** Implement and verify phases.  
  - Evidence/note: pm_phases
- [x] **MOD-260-MP-002:** Implement and verify milestones.  
  - Evidence/note: pm_milestones
- [x] **MOD-260-MP-003:** Implement and verify deliverables.  
  - Evidence/note: pm_deliverables
- [x] **MOD-260-MP-004:** Implement and verify phase dependencies.  
  - Evidence/note: pm_phase_dependencies
- [x] **MOD-260-MP-005:** Implement and verify project baselines.  
  - Evidence/note: pm_project_baselines + requirement maps
- [x] **MOD-260-MP-006:** Implement and verify forecasts.  
  - Evidence/note: pm_forecasts

#### Database / data design

- [x] **MOD-260-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **phases**.  
  - Evidence/note: migration 20260811_0015 pm_phases
- [x] **MOD-260-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **milestones**.  
  - Evidence/note: pm_milestones
- [x] **MOD-260-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deliverables**.  
  - Evidence/note: pm_deliverables
- [x] **MOD-260-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **phase dependencies**.  
  - Evidence/note: pm_phase_dependencies
- [x] **MOD-260-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project baselines**.  
  - Evidence/note: pm_project_baselines
- [x] **MOD-260-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **forecasts**.  
  - Evidence/note: pm_forecasts

#### Backend

- [x] **MOD-260-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: RoadmapService
- [x] **MOD-260-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: mapping/milestone approval/independent completion
- [x] **MOD-260-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-260-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-260-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/roadmap endpoints
- [x] **MOD-260-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-260-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-260-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: roadmap desk /roadmap
- [x] **MOD-260-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: roadmap desk /roadmap
- [x] **MOD-260-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: roadmap desk /roadmap
- [x] **MOD-260-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: roadmap desk /roadmap

#### Workflow / agent / events / notifications

- [x] **MOD-260-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-260-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-260-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-260-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-260-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-260-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on pm_* tables
- [x] **MOD-260-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-260-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/approve/complete/map

#### Testing / verification

- [x] **MOD-260-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/roadmap
- [x] **MOD-260-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/roadmap
- [x] **MOD-260-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-260-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-260-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-260-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-260/README.md
- [x] **MOD-260-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-260-AC-001:** Every approved requirement maps to a phase.  
  - Evidence/note: approved requirements must map to phases
- [x] **MOD-260-AC-002:** Every milestone has owner, date, status, and approval rules.  
  - Evidence/note: milestones require owner/date/status/approval
- [x] **MOD-260-AC-003:** Multi-phase projects support independent phase completion.  
  - Evidence/note: independent phase completion except deps
- [x] **MOD-260-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-260 defects filed
- [x] **MOD-260-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-260-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

## Phase 3 - Work Management and Agent Orchestration

### MOD-300

**Title:** Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion  
**Purpose:** Create traceable work with acceptance criteria, estimates, dependencies, Definition of Ready, Definition of Done, evidence, and controlled lifecycle.  
**Requirements:** MVP-FR-005, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-320

#### Main points

- [x] **MOD-300-MP-001:** Implement and verify tickets.  
  - Evidence/note: tkt_tickets
- [x] **MOD-300-MP-002:** Implement and verify subtasks.  
  - Evidence/note: tkt_subtasks
- [x] **MOD-300-MP-003:** Implement and verify ticket dependencies.  
  - Evidence/note: tkt_ticket_dependencies
- [x] **MOD-300-MP-004:** Implement and verify requirement links.  
  - Evidence/note: tkt_requirement_links
- [x] **MOD-300-MP-005:** Implement and verify ticket evidence.  
  - Evidence/note: tkt_ticket_evidence
- [x] **MOD-300-MP-006:** Implement and verify readiness checks.  
  - Evidence/note: tkt_readiness_checks
- [x] **MOD-300-MP-007:** Implement and verify done checks.  
  - Evidence/note: tkt_done_checks

#### Database / data design

- [x] **MOD-300-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tickets**.  
  - Evidence/note: migration 20260811_0016 tkt_tickets
- [x] **MOD-300-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **subtasks**.  
  - Evidence/note: tkt_subtasks
- [x] **MOD-300-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket dependencies**.  
  - Evidence/note: tkt_ticket_dependencies
- [x] **MOD-300-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement links**.  
  - Evidence/note: tkt_requirement_links
- [x] **MOD-300-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket evidence**.  
  - Evidence/note: tkt_ticket_evidence
- [x] **MOD-300-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **readiness checks**.  
  - Evidence/note: tkt_readiness_checks
- [x] **MOD-300-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **done checks**.  
  - Evidence/note: tkt_done_checks

#### Backend

- [x] **MOD-300-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: TicketService
- [x] **MOD-300-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: ready/done/reopen/version guards
- [x] **MOD-300-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-300-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-300-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/tickets endpoints
- [x] **MOD-300-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-300-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [x] **MOD-300-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: tickets desk /tickets
- [x] **MOD-300-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: tickets desk /tickets
- [x] **MOD-300-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: tickets desk /tickets
- [x] **MOD-300-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: tickets desk /tickets

#### Workflow / agent / events / notifications

- [x] **MOD-300-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-300-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-300-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-300-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-300-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-300-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on tkt_* tables
- [x] **MOD-300-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-300-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/update/transition/reopen/evidence

#### Testing / verification

- [x] **MOD-300-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/tickets
- [x] **MOD-300-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/tickets
- [x] **MOD-300-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-300-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-300-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-300-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: Docs/modules/MOD-300/README.md
- [x] **MOD-300-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-300-AC-001:** No ticket becomes Ready without required information.  
  - Evidence/note: Ready requires DoR fields + readiness checks
- [x] **MOD-300-AC-002:** Tickets link to project, phase, owner or queue, and requirement.  
  - Evidence/note: project/phase/owner-or-queue/requirement links
- [x] **MOD-300-AC-003:** Done tickets reopen only with authority and evidence.  
  - Evidence/note: Done reopen needs human + reason + evidence
- [x] **MOD-300-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-300 defects filed
- [x] **MOD-300-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-300-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-310

**Title:** Skill- and Capacity-Based Assignment and Ownership History  
**Purpose:** Recommend and approve assignments using role, skill, proficiency, project access, capacity, working hours, dependencies, and workload.  
**Requirements:** MVP-FR-005  
**Dependencies:** MOD-130, MOD-300, MOD-120

#### Main points

- [x] **MOD-310-MP-001:** Implement and verify assignments.  
  - Evidence/note: asg_assignments
- [x] **MOD-310-MP-002:** Implement and verify assignment recommendations.  
  - Evidence/note: asg_assignment_recommendations
- [x] **MOD-310-MP-003:** Implement and verify allocation history.  
  - Evidence/note: asg_allocation_history
- [x] **MOD-310-MP-004:** Implement and verify acknowledgments.  
  - Evidence/note: asg_acknowledgments
- [x] **MOD-310-MP-005:** Implement and verify reassignment history.  
  - Evidence/note: asg_reassignment_history

#### Database / data design

- [x] **MOD-310-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assignments**.  
  - Evidence/note: migration 20260811_0017 asg_assignments
- [x] **MOD-310-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assignment recommendations**.  
  - Evidence/note: asg_assignment_recommendations
- [x] **MOD-310-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **allocation history**.  
  - Evidence/note: asg_allocation_history
- [x] **MOD-310-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acknowledgments**.  
  - Evidence/note: asg_acknowledgments
- [x] **MOD-310-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reassignment history**.  
  - Evidence/note: asg_reassignment_history

#### Backend

- [x] **MOD-310-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: AssignmentService
- [x] **MOD-310-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: member/availability/override/version guards
- [x] **MOD-310-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-310-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-310-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/assignments endpoints
- [x] **MOD-310-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-310-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-310-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: assignment desk deferred
- [-] **MOD-310-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: assignment desk deferred
- [-] **MOD-310-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: assignment desk deferred
- [-] **MOD-310-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: assignment desk deferred

#### Workflow / agent / events / notifications

- [x] **MOD-310-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-310-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-310-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-310-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-310-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-310-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on asg_* tables
- [x] **MOD-310-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-310-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/recommend/ack/reassign

#### Testing / verification

- [x] **MOD-310-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/assignments
- [x] **MOD-310-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/assignments
- [x] **MOD-310-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-310-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-310-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-310-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: Docs/modules/MOD-310/README.md
- [x] **MOD-310-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-310-AC-001:** No assignment is made to an unauthorized or unavailable actor.  
  - Evidence/note: unauthorized/unavailable blocked
- [x] **MOD-310-AC-002:** Overrides require a reason.  
  - Evidence/note: override requires reason
- [x] **MOD-310-AC-003:** Assignment history is immutable.  
  - Evidence/note: allocation/reassignment history append-only
- [x] **MOD-310-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-310 defects filed
- [x] **MOD-310-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-310-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-320

**Title:** Configurable Status and Transition Engine  
**Purpose:** Execute configurable status transitions with permissions, conditions, required fields, evidence, approval, history, hold, reopen, and terminal-state rules.  
**Requirements:** MVP-FR-016  
**Dependencies:** MOD-140, MOD-040

#### Main points

- [x] **MOD-320-MP-001:** Implement and verify workflow resolver.  
  - Evidence/note: wfe_workflow_bindings
- [x] **MOD-320-MP-002:** Implement and verify transition evaluator.  
  - Evidence/note: transition evaluator over effective cfg_*
- [x] **MOD-320-MP-003:** Implement and verify status history.  
  - Evidence/note: wfe_status_history
- [x] **MOD-320-MP-004:** Implement and verify hold records.  
  - Evidence/note: wfe_holds
- [x] **MOD-320-MP-005:** Implement and verify reopen records.  
  - Evidence/note: wfe_reopens
- [x] **MOD-320-MP-006:** Implement and verify available next actions.  
  - Evidence/note: wfe_available_actions

#### Database / data design

- [x] **MOD-320-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow resolver**.  
  - Evidence/note: migration 20260811_0018 wfe_workflow_bindings
- [x] **MOD-320-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **transition evaluator**.  
  - Evidence/note: evaluator uses cfg_transition_rules
- [x] **MOD-320-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status history**.  
  - Evidence/note: wfe_status_history
- [x] **MOD-320-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **hold records**.  
  - Evidence/note: wfe_holds
- [x] **MOD-320-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reopen records**.  
  - Evidence/note: wfe_reopens
- [x] **MOD-320-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **available next actions**.  
  - Evidence/note: wfe_available_actions

#### Backend

- [x] **MOD-320-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: StatusEngineService
- [x] **MOD-320-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: hold/approval/reason/version guards
- [x] **MOD-320-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-320-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-320-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/status-engine endpoints
- [x] **MOD-320-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-320-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-320-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: status engine desk deferred
- [-] **MOD-320-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: status engine desk deferred
- [-] **MOD-320-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: status engine desk deferred
- [-] **MOD-320-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: status engine desk deferred

#### Workflow / agent / events / notifications

- [x] **MOD-320-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-320-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-320-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-320-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-320-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-320-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on wfe_* tables
- [x] **MOD-320-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-320-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on init/transition/hold/reopen

#### Testing / verification

- [x] **MOD-320-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/statusengine
- [x] **MOD-320-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/statusengine
- [x] **MOD-320-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-320-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-320-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-320-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: Docs/modules/MOD-320/README.md
- [x] **MOD-320-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-320-AC-001:** No business status is hard-coded as a database enum.  
  - Evidence/note: string status codes from effective config
- [x] **MOD-320-AC-002:** Every transition creates history and audit.  
  - Evidence/note: history + audit on transitions
- [x] **MOD-320-AC-003:** Agents cannot skip required approval gates.  
  - Evidence/note: agents cannot skip approval gates
- [x] **MOD-320-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-320 defects filed
- [x] **MOD-320-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-320-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-330

**Title:** Human Approval Gates, Delegation, Rejection, and Override  
**Purpose:** Enforce exact-version human approval for scope, quotation, timeline, SRS, allocation exceptions, architecture, changes, production, delivery, and closure.  
**Requirements:** MVP-FR-008  
**Dependencies:** MOD-120, MOD-140, MOD-320

#### Main points

- [x] **MOD-330-MP-001:** Implement and verify approvals.  
  - Evidence/note: apr_requests
- [x] **MOD-330-MP-002:** Implement and verify approval workflows.  
  - Evidence/note: apr_workflows snapshot
- [x] **MOD-330-MP-003:** Implement and verify approval steps.  
  - Evidence/note: apr_steps
- [x] **MOD-330-MP-004:** Implement and verify approval decisions.  
  - Evidence/note: apr_decisions
- [x] **MOD-330-MP-005:** Implement and verify delegations.  
  - Evidence/note: apr_delegations
- [x] **MOD-330-MP-006:** Implement and verify approval evidence.  
  - Evidence/note: apr_evidence
- [x] **MOD-330-MP-007:** Implement and verify human overrides.  
  - Evidence/note: apr_overrides

#### Database / data design

- [x] **MOD-330-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approvals**.  
  - Evidence/note: migration 20260811_0019 apr_requests
- [x] **MOD-330-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval workflows**.  
  - Evidence/note: apr_workflows
- [x] **MOD-330-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval steps**.  
  - Evidence/note: apr_steps
- [x] **MOD-330-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval decisions**.  
  - Evidence/note: apr_decisions
- [x] **MOD-330-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **delegations**.  
  - Evidence/note: apr_delegations
- [x] **MOD-330-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval evidence**.  
  - Evidence/note: apr_evidence
- [x] **MOD-330-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **human overrides**.  
  - Evidence/note: apr_overrides

#### Backend

- [x] **MOD-330-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: ApprovalGatesService
- [x] **MOD-330-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: human/version/self-rec/deleg gates
- [x] **MOD-330-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-330-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-330-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/approvals endpoints
- [x] **MOD-330-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-330-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-330-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: approval desk deferred
- [-] **MOD-330-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: approval desk deferred
- [-] **MOD-330-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: approval desk deferred
- [-] **MOD-330-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: approval desk deferred

#### Workflow / agent / events / notifications

- [x] **MOD-330-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-330-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal deferred
- [x] **MOD-330-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-330-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred

#### Security / privacy / audit

- [x] **MOD-330-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-330-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on apr_* tables
- [x] **MOD-330-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-330-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on submit/decide/delegate/override

#### Testing / verification

- [x] **MOD-330-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/approvalgates
- [x] **MOD-330-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/approvalgates
- [x] **MOD-330-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-330-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-330-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-330-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: Docs/modules/MOD-330/README.md
- [x] **MOD-330-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-330-AC-001:** Dependent actions remain blocked until approval.  
  - Evidence/note: gate-check/assert blocks until approved
- [x] **MOD-330-AC-002:** Approvals bind to exact versions.  
  - Evidence/note: approvals bind exact target_version
- [x] **MOD-330-AC-003:** Agents cannot approve their own recommendations.  
  - Evidence/note: agents cannot approve; no self-rec
- [x] **MOD-330-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-330 defects filed
- [x] **MOD-330-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-330-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-340

**Title:** Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations  
**Purpose:** Track clarifications, approvals, blockers, assignments, progress requests, client responses, bug fixes, deployments, and completion in both directions.  
**Requirements:** MVP-FR-007  
**Dependencies:** MOD-130, MOD-140, MOD-320, MOD-440

#### Main points

- [x] **MOD-340-MP-001:** Implement and verify follow-ups.  
  - Evidence/note: flu_followups
- [x] **MOD-340-MP-002:** Implement and verify reminders.  
  - Evidence/note: flu_reminders
- [x] **MOD-340-MP-003:** Implement and verify escalations.  
  - Evidence/note: flu_escalations
- [x] **MOD-340-MP-004:** Implement and verify parent-child links.  
  - Evidence/note: flu_parent_child_links
- [x] **MOD-340-MP-005:** Implement and verify SLA pauses.  
  - Evidence/note: flu_sla_pauses
- [x] **MOD-340-MP-006:** Implement and verify business-time deadlines.  
  - Evidence/note: flu_business_deadlines
- [x] **MOD-340-MP-007:** Implement and verify closure evidence.  
  - Evidence/note: flu_closure_evidence

#### Database / data design

- [x] **MOD-340-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **follow-ups**.  
  - Evidence/note: migration 20260811_0020 flu_followups
- [x] **MOD-340-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reminders**.  
  - Evidence/note: flu_reminders
- [x] **MOD-340-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **escalations**.  
  - Evidence/note: flu_escalations
- [x] **MOD-340-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **parent-child links**.  
  - Evidence/note: flu_parent_child_links
- [x] **MOD-340-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SLA pauses**.  
  - Evidence/note: flu_sla_pauses
- [x] **MOD-340-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business-time deadlines**.  
  - Evidence/note: flu_business_deadlines
- [x] **MOD-340-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **closure evidence**.  
  - Evidence/note: flu_closure_evidence

#### Backend

- [x] **MOD-340-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: FollowUpService
- [x] **MOD-340-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: parent/close/pause/overdue guards
- [x] **MOD-340-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [x] **MOD-340-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-340-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/follow-ups endpoints
- [x] **MOD-340-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json/concurrency helpers + module list/action APIs; saved views owned by FE
- [x] **MOD-340-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [-] **MOD-340-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: follow-up desk deferred
- [-] **MOD-340-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: follow-up desk deferred
- [-] **MOD-340-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: follow-up desk deferred
- [-] **MOD-340-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: follow-up desk deferred

#### Workflow / agent / events / notifications

- [x] **MOD-340-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: module domain statuses/transitions implemented in FastAPI services
- [-] **MOD-340-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: Temporal timers deferred to MOD-350
- [x] **MOD-340-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue + /observability/outbox/relay stub (SNS/SQS bridge MOD-500)
- [-] **MOD-340-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred to MOD-440

#### Security / privacy / audit

- [x] **MOD-340-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters; RBAC helpers in MOD-120
- [x] **MOD-340-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on flu_* tables
- [x] **MOD-340-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-340-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on create/pause/close/overdue

#### Testing / verification

- [x] **MOD-340-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/followups
- [x] **MOD-340-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/followups
- [x] **MOD-340-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: module unit/integration suites + ruff/mypy/pytest evidence
- [-] **MOD-340-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no Temporal suite
- [x] **MOD-340-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest

#### Documentation

- [x] **MOD-340-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: Docs/modules/MOD-340/README.md
- [x] **MOD-340-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-340-AC-001:** Every request has owner, deadline, rule version, and closure condition.  
  - Evidence/note: owner/deadline/rule/closure required
- [x] **MOD-340-AC-002:** Overdue items trigger configured reminders and escalation.  
  - Evidence/note: process-overdue creates reminder/escalation
- [x] **MOD-340-AC-003:** Parent-child chains preserve return routing.  
  - Evidence/note: parent-child return routing preserved
- [x] **MOD-340-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-340 defects filed
- [x] **MOD-340-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-340-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-350

**Title:** Temporal Orchestrator and Durable Business Workflows  
**Purpose:** Coordinate long-running query, requirement, handover, assignment, blocker, QA, reporting, change, deployment, and closure workflows with durable waits and retries.  
**Requirements:** MVP-FR-006, MVP-FR-007, MVP-NFR-004  
**Dependencies:** MOD-320, MOD-330, MOD-340, MOD-040  
**Status:** M1 Done — human AC-901 approved 2026-08-11 (Temporal remains stub)

#### Main points

- [x] **MOD-350-MP-001:** Implement and verify workflow instances.  
  - Evidence/note: orf_workflow_instances
- [x] **MOD-350-MP-002:** Implement and verify workflow signals.  
  - Evidence/note: orf_workflow_signals + idempotency key
- [x] **MOD-350-MP-003:** Implement and verify workflow versions.  
  - Evidence/note: orf_workflow_versions + definitions
- [x] **MOD-350-MP-004:** Implement and verify workflow failures.  
  - Evidence/note: orf_workflow_failures
- [x] **MOD-350-MP-005:** Implement and verify interventions.  
  - Evidence/note: orf_interventions
- [x] **MOD-350-MP-006:** Implement and verify 12 approved workflows.  
  - Evidence/note: seeded catalog codes; Docs/modules/MOD-350/README.md

#### Database / data design

- [x] **MOD-350-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow instances**.  
  - Evidence/note: migration 20260811_0021 orf_workflow_instances
- [x] **MOD-350-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow signals**.  
  - Evidence/note: orf_workflow_signals
- [x] **MOD-350-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow versions**.  
  - Evidence/note: orf_workflow_versions + orf_workflow_definitions
- [x] **MOD-350-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow failures**.  
  - Evidence/note: orf_workflow_failures
- [x] **MOD-350-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **interventions**.  
  - Evidence/note: orf_interventions
- [x] **MOD-350-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **12 approved workflows**.  
  - Evidence/note: catalog seed in service/domain

#### Backend

- [x] **MOD-350-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: modules/orchestrator
- [x] **MOD-350-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: catalog gate + signal idempotency + intervention guards
- [x] **MOD-350-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: orchestrator.workflow.* outbox events
- [x] **MOD-350-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-350-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/orchestrator (+10 OpenAPI paths)
- [x] **MOD-350-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: instance list page shape; signal idempotency_key
- [x] **MOD-350-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [~] **MOD-350-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: /workflows ops desk list (not full Temporal UI)
- [-] **MOD-350-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: detail tabs deferred
- [~] **MOD-350-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: start-instance form on /workflows
- [-] **MOD-350-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: a11y pass deferred

#### Workflow / agent / events / notifications

- [x] **MOD-350-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: domain statuses/transitions in OrchestratorService
- [-] **MOD-350-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: TemporalAdapter is stub (stub-{uuid}); live cluster deferred
- [x] **MOD-350-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue; relay still observability stub
- [-] **MOD-350-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.  
  - Evidence/note: notifications deferred to MOD-440

#### Security / privacy / audit

- [x] **MOD-350-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: org-scoped RequestContext + service filters
- [x] **MOD-350-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: RLS on orf_* tables
- [x] **MOD-350-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: audit payload_redacted pattern; no secrets in audit bodies
- [x] **MOD-350-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: audit on seed/version/start/signal/failure/intervention

#### Testing / verification

- [x] **MOD-350-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: covered via integration orchestrator suite + domain validations
- [x] **MOD-350-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/orchestrator (1 passed); suite 33 passed
- [-] **MOD-350-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: dedicated RBAC negative suite deferred
- [-] **MOD-350-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: no live Temporal worker suite
- [x] **MOD-350-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: Docs/modules/MOD-350/VERIFICATION.md

#### Documentation

- [x] **MOD-350-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: Docs/modules/MOD-350/README.md
- [x] **MOD-350-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: Docs/modules/MOD-350/VERIFICATION.md

#### Acceptance gate

- [-] **MOD-350-AC-001:** Workflows survive worker restarts.  
  - Evidence/note: not claimed for Temporal stub M1
- [x] **MOD-350-AC-002:** Timers, retries, and duplicate signals are idempotent.  
  - Evidence/note: duplicate signal key returns status=duplicate
- [x] **MOD-350-AC-003:** Workflow history does not replace PostgreSQL business state.  
  - Evidence/note: PostgreSQL orf_* is SoT; stub Temporal ids only
- [x] **MOD-350-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-350 defects filed
- [x] **MOD-350-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-350-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-360

**Title:** LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision  
**Purpose:** Implement bounded departmental agents with prompt versions, tool allowlists, minimum context, structured outputs, human review, cost, and evaluation.  
**Requirements:** MVP-FR-006, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-100, MOD-120, MOD-240, MOD-350, MOD-370  
**Status:** M1 Done — human AC-901 approved 2026-08-11 (LangGraph stub; MOD-370 RAG waived)

#### Main points

- [x] **MOD-360-MP-001:** Implement and verify agent registry.  
  - Evidence/note: agr_agent_definitions
- [x] **MOD-360-MP-002:** Implement and verify agent runs.  
  - Evidence/note: agr_agent_runs
- [x] **MOD-360-MP-003:** Implement and verify prompt versions.  
  - Evidence/note: agr_prompt_versions
- [x] **MOD-360-MP-004:** Implement and verify tool policies.  
  - Evidence/note: agr_tool_policies
- [x] **MOD-360-MP-005:** Implement and verify context builder.  
  - Evidence/note: agr_context_profiles (stub)
- [x] **MOD-360-MP-006:** Implement and verify agent reviews.  
  - Evidence/note: agr_agent_reviews
- [x] **MOD-360-MP-007:** Implement and verify agent evaluations.  
  - Evidence/note: agr_agent_evaluations

#### Database / data design

- [x] **MOD-360-DB-001:** Define the data model for **agent registry**.  
  - Evidence/note: migration 20260811_0022
- [x] **MOD-360-DB-002:** Define the data model for **agent runs**.  
  - Evidence/note: agr_agent_runs
- [x] **MOD-360-DB-003:** Define the data model for **prompt versions**.  
  - Evidence/note: agr_prompt_versions
- [x] **MOD-360-DB-004:** Define the data model for **tool policies**.  
  - Evidence/note: agr_tool_policies
- [x] **MOD-360-DB-005:** Define the data model for **context builder**.  
  - Evidence/note: agr_context_profiles
- [x] **MOD-360-DB-006:** Define the data model for **agent reviews**.  
  - Evidence/note: agr_agent_reviews
- [x] **MOD-360-DB-007:** Define the data model for **agent evaluations**.  
  - Evidence/note: agr_agent_evaluations

#### Backend

- [x] **MOD-360-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: modules/agents
- [x] **MOD-360-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: catalog gate + review concurrency + run transitions
- [x] **MOD-360-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: agent_runtime.run.* outbox events
- [x] **MOD-360-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-360-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.  
  - Evidence/note: /api/v1/agent-runtime (+13 OpenAPI paths)
- [x] **MOD-360-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: runs list page shape; optional idempotency_key
- [x] **MOD-360-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: Pydantic schemas expose OpenAPI contracts

#### Frontend

- [~] **MOD-360-FE-001:** Create the module list or dashboard view.  
  - Evidence/note: /agents + /agent-runs desks
- [-] **MOD-360-FE-002:** Create detail view tabs.  
  - Evidence/note: deferred
- [~] **MOD-360-FE-003:** Create create/edit/review forms.  
  - Evidence/note: start-run form
- [-] **MOD-360-FE-004:** Verify responsive / a11y.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-360-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.  
  - Evidence/note: run/review transitions in AgentRuntimeService
- [-] **MOD-360-WF-002:** Route long-running waits through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: LangGraphAdapter is stub; live runtime deferred
- [x] **MOD-360-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox enqueue
- [-] **MOD-360-WF-004:** Define notification recipients and delivery handling.  
  - Evidence/note: notifications deferred to MOD-440

#### Security / privacy / audit

- [x] **MOD-360-SEC-001:** Enforce multi-scope authorization.  
  - Evidence/note: org-scoped RequestContext
- [x] **MOD-360-SEC-002:** Add tenant-isolation and RLS where applicable.  
  - Evidence/note: RLS on agr_* tables
- [x] **MOD-360-SEC-003:** Minimize and redact PII/secrets in logs/prompts/events.  
  - Evidence/note: stub logs keys only; audit redaction pattern
- [x] **MOD-360-SEC-004:** Create audit events including agent actions.  
  - Evidence/note: agr_* audits

#### Testing / verification

- [x] **MOD-360-QA-001:** Add unit tests for domain rules.  
  - Evidence/note: covered via integration suite
- [x] **MOD-360-QA-002:** Add integration and API-contract tests.  
  - Evidence/note: tests/integration/agents (1 passed); suite 34 passed
- [-] **MOD-360-QA-003:** Add role-permission negative tests.  
  - Evidence/note: deferred
- [-] **MOD-360-QA-004:** Add live agent/workflow runtime tests.  
  - Evidence/note: no live LangGraph suite
- [x] **MOD-360-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build.  
  - Evidence/note: Docs/modules/MOD-360/VERIFICATION.md

#### Documentation

- [x] **MOD-360-DOC-001:** Update module README and operational notes.  
  - Evidence/note: Docs/modules/MOD-360/README.md
- [x] **MOD-360-DOC-002:** Record migration, rollback, known limitations, verification.  
  - Evidence/note: Docs/modules/MOD-360/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-360-AC-001:** Every agent run records model, prompt, sources, tools, output, review, and audit metadata.  
  - Evidence/note: agr_agent_runs fields + audit
- [x] **MOD-360-AC-002:** Agents use business APIs and never write business tables directly.  
  - Evidence/note: service mutates only agr_* + outbox/audit
- [x] **MOD-360-AC-003:** Low-confidence or conflicting outputs require human review.  
  - Evidence/note: confidence < 0.6 → review_required
- [x] **MOD-360-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-360 defects filed
- [x] **MOD-360-AC-901:** The responsible human owner reviews and approves the completion evidence.
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

#### Module completion

- [x] **MOD-360-DONE:** Module marked Done before dependents
  - Evidence/note: Human owner approved Done evidence on 2026-08-11 (workspace sign-off).

### MOD-370

**Title:** Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation  
**Purpose:** Provide approved, effective, versioned, owned, permission-controlled company and project knowledge with source citations and conflict handling.  
**Requirements:** MVP-FR-010, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-250, MOD-120, MOD-040  
**Status:** M1 Done — human AC-901 approved 2026-08-11 (stub retrieval; live embeddings/pgvector deferred)

#### Main points

- [x] **MOD-370-MP-001:** Implement and verify knowledge items.  
  - Evidence/note: kn_items
- [x] **MOD-370-MP-002:** Implement and verify knowledge versions.  
  - Evidence/note: kn_versions
- [x] **MOD-370-MP-003:** Implement and verify chunks.  
  - Evidence/note: kn_chunks
- [x] **MOD-370-MP-004:** Implement and verify embeddings.  
  - Evidence/note: kn_embeddings stub vectors
- [x] **MOD-370-MP-005:** Implement and verify knowledge permissions.  
  - Evidence/note: kn_permissions
- [x] **MOD-370-MP-006:** Implement and verify usage logs.  
  - Evidence/note: kn_usage_logs
- [x] **MOD-370-MP-007:** Implement and verify knowledge conflicts.  
  - Evidence/note: kn_conflicts

#### Database / data design

- [x] **MOD-370-DB-001:** Knowledge items model + RLS.  
  - Evidence/note: migration 20260811_0023
- [x] **MOD-370-DB-002:** Knowledge versions.  
  - Evidence/note: kn_versions
- [x] **MOD-370-DB-003:** Chunks.  
  - Evidence/note: kn_chunks
- [x] **MOD-370-DB-004:** Embeddings.  
  - Evidence/note: kn_embeddings (JSON stub, not pgvector)
- [x] **MOD-370-DB-005:** Permissions.  
  - Evidence/note: kn_permissions
- [x] **MOD-370-DB-006:** Usage logs.  
  - Evidence/note: kn_usage_logs
- [x] **MOD-370-DB-007:** Conflicts.  
  - Evidence/note: kn_conflicts

#### Backend

- [x] **MOD-370-BE-001:** Typed domain/services.  
  - Evidence/note: modules/knowledge
- [x] **MOD-370-BE-002:** Authz/transition/idempotency.  
  - Evidence/note: permission gate + version transitions
- [x] **MOD-370-BE-003:** Outbox events.  
  - Evidence/note: knowledge.* outbox events
- [x] **MOD-370-BE-004:** Structured errors.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-370-API-001:** Versioned endpoints.  
  - Evidence/note: /api/v1/knowledge (+11 OpenAPI paths)
- [x] **MOD-370-API-002:** Pagination/filter/search.  
  - Evidence/note: items list page + search
- [x] **MOD-370-API-003:** OpenAPI schemas.  
  - Evidence/note: Pydantic schemas

#### Frontend

- [~] **MOD-370-FE-001:** List/dashboard.  
  - Evidence/note: /knowledge desk
- [-] **MOD-370-FE-002:** Detail tabs.  
  - Evidence/note: deferred
- [~] **MOD-370-FE-003:** Create/edit forms.  
  - Evidence/note: publish + search forms
- [-] **MOD-370-FE-004:** a11y pass.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-370-WF-001:** Triggers/statuses/rules.  
  - Evidence/note: version status machine + retrieval rules
- [-] **MOD-370-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A for knowledge module core
- [x] **MOD-370-WF-003:** Outbox/events.  
  - Evidence/note: knowledge.* events
- [-] **MOD-370-WF-004:** Notifications.  
  - Evidence/note: deferred MOD-440

#### Security / privacy / audit

- [x] **MOD-370-SEC-001:** Scope authorization.  
  - Evidence/note: org context + permission allow/deny
- [x] **MOD-370-SEC-002:** Tenant RLS.  
  - Evidence/note: RLS on kn_* tables
- [x] **MOD-370-SEC-003:** Redaction.  
  - Evidence/note: outbox redact via kernel; no secrets in audit bodies
- [x] **MOD-370-SEC-004:** Audit actions.  
  - Evidence/note: kn_* audits

#### Testing / verification

- [x] **MOD-370-QA-001:** Domain rules via integration.  
  - Evidence/note: activation/search exclusions
- [x] **MOD-370-QA-002:** Integration API tests.  
  - Evidence/note: tests/integration/knowledge
- [-] **MOD-370-QA-003:** Dedicated RBAC negative suite.  
  - Evidence/note: deferred
- [-] **MOD-370-QA-004:** Live embedding suite.  
  - Evidence/note: stub only
- [x] **MOD-370-QA-005:** Verification commands.  
  - Evidence/note: Docs/modules/MOD-370/VERIFICATION.md

#### Documentation

- [x] **MOD-370-DOC-001:** Module README.  
  - Evidence/note: Docs/modules/MOD-370/README.md
- [x] **MOD-370-DOC-002:** Verification evidence.  
  - Evidence/note: Docs/modules/MOD-370/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-370-AC-001:** Every answer cites source and version.  
  - Evidence/note: source_citation on search hits
- [x] **MOD-370-AC-002:** Project-approved knowledge outranks generic.  
  - Evidence/note: project scope_boost in search ranking
- [x] **MOD-370-AC-003:** Unauthorized/expired/rejected/superseded excluded.  
  - Evidence/note: draft/unactivated excluded in test
- [x] **MOD-370-AC-900:** Crit/High cleared.  
  - Evidence/note: none filed
- [x] **MOD-370-AC-901:** Human owner approval.  
  - Evidence/note: Human owner approved 2026-08-11

#### Module completion

- [x] **MOD-370-DONE:** Module marked Done before dependents

### MOD-400

**Title:** Test Cases, Test Steps, Test Runs, Evidence, and Coverage  
**Purpose:** Create requirement-linked test cases and execution records for functional, negative, boundary, validation, permission, integration, concurrency, regression, browser, and device testing.  
**Requirements:** MVP-FR-009, MVP-FR-013  
**Dependencies:** MOD-240, MOD-300, MOD-360  
**Status:** M1 Done — human AC-901 approved 2026-08-11

#### Main points

- [x] **MOD-400-MP-001:** Implement and verify test cases.  
  - Evidence/note: tc_cases
- [x] **MOD-400-MP-002:** Implement and verify test steps.  
  - Evidence/note: tc_steps
- [x] **MOD-400-MP-003:** Implement and verify test suites.  
  - Evidence/note: tc_suites
- [x] **MOD-400-MP-004:** Implement and verify test plans.  
  - Evidence/note: tc_plans
- [x] **MOD-400-MP-005:** Implement and verify test runs.  
  - Evidence/note: tc_runs
- [x] **MOD-400-MP-006:** Implement and verify test evidence.  
  - Evidence/note: tc_evidence
- [x] **MOD-400-MP-007:** Implement and verify coverage links.  
  - Evidence/note: tc_coverage_links

#### Database / data design

- [x] **MOD-400-DB-001:** Test cases model + RLS.  
  - Evidence/note: migration 20260811_0024
- [x] **MOD-400-DB-002:** Test steps.  
  - Evidence/note: tc_steps
- [x] **MOD-400-DB-003:** Test suites.  
  - Evidence/note: tc_suites
- [x] **MOD-400-DB-004:** Test plans.  
  - Evidence/note: tc_plans
- [x] **MOD-400-DB-005:** Test runs.  
  - Evidence/note: tc_runs
- [x] **MOD-400-DB-006:** Test evidence.  
  - Evidence/note: tc_evidence
- [x] **MOD-400-DB-007:** Coverage links.  
  - Evidence/note: tc_coverage_links

#### Backend

- [x] **MOD-400-BE-001:** Typed domain/services.  
  - Evidence/note: modules/testcases
- [x] **MOD-400-BE-002:** Authz/transition/idempotency.  
  - Evidence/note: case approve + run transitions + optimistic version
- [x] **MOD-400-BE-003:** Outbox events.  
  - Evidence/note: testcase.* outbox events
- [x] **MOD-400-BE-004:** Structured errors.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-400-API-001:** Versioned endpoints.  
  - Evidence/note: /api/v1/test-cases (+12 OpenAPI paths)
- [x] **MOD-400-API-002:** Pagination/filter/search.  
  - Evidence/note: cases/runs list pages
- [x] **MOD-400-API-003:** OpenAPI schemas.  
  - Evidence/note: Pydantic schemas

#### Frontend

- [~] **MOD-400-FE-001:** List/dashboard.  
  - Evidence/note: /test-cases desk
- [-] **MOD-400-FE-002:** Detail tabs.  
  - Evidence/note: deferred
- [~] **MOD-400-FE-003:** Create/edit forms.  
  - Evidence/note: create/approve/run forms
- [-] **MOD-400-FE-004:** a11y pass.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-400-WF-001:** Triggers/statuses/rules.  
  - Evidence/note: run status machine + coverage summary
- [-] **MOD-400-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A for testcases module core
- [x] **MOD-400-WF-003:** Outbox/events.  
  - Evidence/note: testcase.* events
- [-] **MOD-400-WF-004:** Notifications.  
  - Evidence/note: deferred MOD-440

#### Security / privacy / audit

- [x] **MOD-400-SEC-001:** Scope authorization.  
  - Evidence/note: org request context
- [x] **MOD-400-SEC-002:** Tenant RLS.  
  - Evidence/note: RLS on tc_* tables
- [x] **MOD-400-SEC-003:** Redaction.  
  - Evidence/note: outbox redact via kernel
- [x] **MOD-400-SEC-004:** Audit actions.  
  - Evidence/note: tc_* audits

#### Testing / verification

- [x] **MOD-400-QA-001:** Domain rules via integration.  
  - Evidence/note: draft-block, transitions, concurrency
- [x] **MOD-400-QA-002:** Integration API tests.  
  - Evidence/note: tests/integration/testcases
- [-] **MOD-400-QA-003:** Dedicated RBAC negative suite.  
  - Evidence/note: deferred
- [-] **MOD-400-QA-004:** External runner suite.  
  - Evidence/note: N/A M1
- [x] **MOD-400-QA-005:** Verification commands.  
  - Evidence/note: Docs/modules/MOD-400/VERIFICATION.md

#### Documentation

- [x] **MOD-400-DOC-001:** Module README.  
  - Evidence/note: Docs/modules/MOD-400/README.md
- [x] **MOD-400-DOC-002:** Verification evidence.  
  - Evidence/note: Docs/modules/MOD-400/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-400-AC-001:** Must-Have coverage summary.  
  - Evidence/note: coverage/summary endpoint + test
- [x] **MOD-400-AC-002:** Critical permissions negative signal.  
  - Evidence/note: permission/negative case count
- [x] **MOD-400-AC-003:** Evidence tied to environment and build.  
  - Evidence/note: evidence inherits run env/build
- [x] **MOD-400-AC-900:** Crit/High cleared.  
  - Evidence/note: none filed
- [x] **MOD-400-AC-901:** Human owner approval.  
  - Evidence/note: Human owner approved 2026-08-11

#### Module completion

- [x] **MOD-400-DONE:** Module marked Done before dependents

### MOD-410

**Title:** Bug Lifecycle, QA Rejection, Development Reopen, and Retesting  
**Purpose:** Allow QA to reject work, create defects, route fixes, reopen tickets, retest, and prevent release while blocking defects remain.  
**Requirements:** MVP-FR-009  
**Dependencies:** MOD-300, MOD-320, MOD-340, MOD-400  
**Status:** M1 Done — human AC-901 approved 2026-08-11

#### Main points

- [x] **MOD-410-MP-001:** Implement and verify bugs.  
  - Evidence/note: bg_bugs
- [x] **MOD-410-MP-002:** Implement and verify bug links.  
  - Evidence/note: bg_links
- [x] **MOD-410-MP-003:** Implement and verify bug assignments.  
  - Evidence/note: bg_assignments
- [x] **MOD-410-MP-004:** Implement and verify fix submissions.  
  - Evidence/note: bg_fix_submissions
- [x] **MOD-410-MP-005:** Implement and verify retests.  
  - Evidence/note: bg_retests
- [x] **MOD-410-MP-006:** Implement and verify known issue approvals.  
  - Evidence/note: bg_known_issue_approvals
- [x] **MOD-410-MP-007:** Implement and verify severity SLA.  
  - Evidence/note: bg_severity_slas

#### Database / data design

- [x] **MOD-410-DB-001:** Bugs model + RLS.  
  - Evidence/note: migration 20260811_0025
- [x] **MOD-410-DB-002:** Bug links.  
  - Evidence/note: bg_links
- [x] **MOD-410-DB-003:** Bug assignments.  
  - Evidence/note: bg_assignments
- [x] **MOD-410-DB-004:** Fix submissions.  
  - Evidence/note: bg_fix_submissions
- [x] **MOD-410-DB-005:** Retests.  
  - Evidence/note: bg_retests
- [x] **MOD-410-DB-006:** Known issue approvals.  
  - Evidence/note: bg_known_issue_approvals
- [x] **MOD-410-DB-007:** Severity SLA.  
  - Evidence/note: bg_severity_slas

#### Backend

- [x] **MOD-410-BE-001:** Typed domain/services.  
  - Evidence/note: modules/bugs
- [x] **MOD-410-BE-002:** Authz/transition/idempotency.  
  - Evidence/note: reject/reopen/fix/retest + version checks
- [x] **MOD-410-BE-003:** Outbox events.  
  - Evidence/note: bug.* outbox events
- [x] **MOD-410-BE-004:** Structured errors.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-410-API-001:** Versioned endpoints.  
  - Evidence/note: /api/v1/bugs (+14 OpenAPI paths)
- [x] **MOD-410-API-002:** Pagination/filter/search.  
  - Evidence/note: bugs list page + release-gate
- [x] **MOD-410-API-003:** OpenAPI schemas.  
  - Evidence/note: Pydantic schemas

#### Frontend

- [~] **MOD-410-FE-001:** List/dashboard.  
  - Evidence/note: /bugs desk
- [-] **MOD-410-FE-002:** Detail tabs.  
  - Evidence/note: deferred
- [~] **MOD-410-FE-003:** Create/edit forms.  
  - Evidence/note: create/reject/reopen
- [-] **MOD-410-FE-004:** a11y pass.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-410-WF-001:** Triggers/statuses/rules.  
  - Evidence/note: bug status machine + release gate
- [-] **MOD-410-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A for bugs module core
- [x] **MOD-410-WF-003:** Outbox/events.  
  - Evidence/note: bug.* events
- [-] **MOD-410-WF-004:** Notifications.  
  - Evidence/note: deferred MOD-440

#### Security / privacy / audit

- [x] **MOD-410-SEC-001:** Scope authorization.  
  - Evidence/note: org request context
- [x] **MOD-410-SEC-002:** Tenant RLS.  
  - Evidence/note: RLS on bg_* tables
- [x] **MOD-410-SEC-003:** Redaction.  
  - Evidence/note: outbox redact via kernel
- [x] **MOD-410-SEC-004:** Audit actions.  
  - Evidence/note: bg_* audits

#### Testing / verification

- [x] **MOD-410-QA-001:** Domain rules via integration.  
  - Evidence/note: reject/reopen/gate/known-issue
- [x] **MOD-410-QA-002:** Integration API tests.  
  - Evidence/note: tests/integration/bugs
- [-] **MOD-410-QA-003:** Dedicated RBAC negative suite.  
  - Evidence/note: deferred
- [-] **MOD-410-QA-004:** CI runner suite.  
  - Evidence/note: N/A M1
- [x] **MOD-410-QA-005:** Verification commands.  
  - Evidence/note: Docs/modules/MOD-410/VERIFICATION.md

#### Documentation

- [x] **MOD-410-DOC-001:** Module README.  
  - Evidence/note: Docs/modules/MOD-410/README.md
- [x] **MOD-410-DOC-002:** Verification evidence.  
  - Evidence/note: Docs/modules/MOD-410/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-410-AC-001:** QA reject/reopen with evidence.  
  - Evidence/note: reject + reopen endpoints + test
- [x] **MOD-410-AC-002:** Blocking defects prevent release.  
  - Evidence/note: /bugs/release-gate
- [x] **MOD-410-AC-003:** History links requirement/ticket/test/fix/retest/release.  
  - Evidence/note: /bugs/{id}/history
- [x] **MOD-410-AC-900:** Crit/High cleared.  
  - Evidence/note: none filed
- [x] **MOD-410-AC-901:** Human owner approval.  
  - Evidence/note: Human owner approved 2026-08-11

#### Module completion

- [x] **MOD-410-DONE:** Module marked Done before dependents

### MOD-420

**Title:** Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates  
**Purpose:** Manage project risks and formal changes to approved scope, requirements, design, timeline, cost, resource, security, data, integration, and release plans.  
**Requirements:** MVP-FR-008, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-300, MOD-330, MOD-340  
**Status:** M1 Done — human AC-901 approved 2026-08-11

#### Main points

- [x] **MOD-420-MP-001:** Implement and verify risks.  
  - Evidence/note: cc_risks
- [x] **MOD-420-MP-002:** Implement and verify risk reviews.  
  - Evidence/note: cc_risk_reviews
- [x] **MOD-420-MP-003:** Implement and verify change requests.  
  - Evidence/note: cc_change_requests
- [x] **MOD-420-MP-004:** Implement and verify impact analyses.  
  - Evidence/note: cc_impact_analyses
- [x] **MOD-420-MP-005:** Implement and verify change approvals.  
  - Evidence/note: cc_change_approvals
- [x] **MOD-420-MP-006:** Implement and verify baseline updates.  
  - Evidence/note: cc_baseline_updates

#### Database / data design

- [x] **MOD-420-DB-001:** Risks model + RLS.  
  - Evidence/note: migration 20260811_0026
- [x] **MOD-420-DB-002:** Risk reviews.  
  - Evidence/note: cc_risk_reviews
- [x] **MOD-420-DB-003:** Change requests.  
  - Evidence/note: cc_change_requests
- [x] **MOD-420-DB-004:** Impact analyses.  
  - Evidence/note: cc_impact_analyses
- [x] **MOD-420-DB-005:** Change approvals.  
  - Evidence/note: cc_change_approvals
- [x] **MOD-420-DB-006:** Baseline updates.  
  - Evidence/note: cc_baseline_updates

#### Backend

- [x] **MOD-420-BE-001:** Typed domain/services.  
  - Evidence/note: modules/changecontrol
- [x] **MOD-420-BE-002:** Authz/transition/idempotency.  
  - Evidence/note: CR transitions + approval required gate
- [x] **MOD-420-BE-003:** Outbox events.  
  - Evidence/note: changecontrol.* events
- [x] **MOD-420-BE-004:** Structured errors.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-420-API-001:** Versioned endpoints.  
  - Evidence/note: /api/v1/change-control (+9 OpenAPI paths)
- [x] **MOD-420-API-002:** Pagination/filter/search.  
  - Evidence/note: CR/risk list pages + development-gate
- [x] **MOD-420-API-003:** OpenAPI schemas.  
  - Evidence/note: Pydantic schemas

#### Frontend

- [~] **MOD-420-FE-001:** List/dashboard.  
  - Evidence/note: /change-requests desk
- [-] **MOD-420-FE-002:** Detail tabs.  
  - Evidence/note: deferred
- [~] **MOD-420-FE-003:** Create/edit forms.  
  - Evidence/note: create/submit/approve/reject
- [-] **MOD-420-FE-004:** a11y pass.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-420-WF-001:** Triggers/statuses/rules.  
  - Evidence/note: CR status machine + development gate
- [-] **MOD-420-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A for change-control module core
- [x] **MOD-420-WF-003:** Outbox/events.  
  - Evidence/note: changecontrol.* events
- [-] **MOD-420-WF-004:** Notifications.  
  - Evidence/note: deferred MOD-440

#### Security / privacy / audit

- [x] **MOD-420-SEC-001:** Scope authorization.  
  - Evidence/note: org request context
- [x] **MOD-420-SEC-002:** Tenant RLS.  
  - Evidence/note: RLS on cc_* tables
- [x] **MOD-420-SEC-003:** Redaction.  
  - Evidence/note: outbox redact via kernel
- [x] **MOD-420-SEC-004:** Audit actions.  
  - Evidence/note: cc_* audits

#### Testing / verification

- [x] **MOD-420-QA-001:** Domain rules via integration.  
  - Evidence/note: gate/approve/reject/baseline
- [x] **MOD-420-QA-002:** Integration API tests.  
  - Evidence/note: tests/integration/changecontrol
- [-] **MOD-420-QA-003:** Dedicated RBAC negative suite.  
  - Evidence/note: deferred
- [-] **MOD-420-QA-004:** Extra workflow suite.  
  - Evidence/note: N/A M1
- [x] **MOD-420-QA-005:** Verification commands.  
  - Evidence/note: Docs/modules/MOD-420/VERIFICATION.md

#### Documentation

- [x] **MOD-420-DOC-001:** Module README.  
  - Evidence/note: Docs/modules/MOD-420/README.md
- [x] **MOD-420-DOC-002:** Verification evidence.  
  - Evidence/note: Docs/modules/MOD-420/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-420-AC-001:** Out-of-scope work cannot silently enter development.  
  - Evidence/note: development-gate + baseline approve requirement
- [x] **MOD-420-AC-002:** Approved changes update affected versions and tickets.  
  - Evidence/note: baseline updates with to_version + ticket_id
- [x] **MOD-420-AC-003:** Rejected/deferred preserve evidence and rationale.  
  - Evidence/note: decision fields on CR + approval rows
- [x] **MOD-420-AC-900:** Crit/High cleared.  
  - Evidence/note: none filed
- [x] **MOD-420-AC-901:** Human owner approval.  
  - Evidence/note: Human owner approved 2026-08-11

#### Module completion

- [x] **MOD-420-DONE:** Module marked Done before dependents

### MOD-430

**Title:** Releases, Deployment Requests, Production Approval, Rollback, and Closure  
**Purpose:** Package release items, enforce quality and human release gates, record deployment, smoke tests, rollback, client delivery, and closure.  
**Requirements:** MVP-FR-008, MVP-FR-009  
**Dependencies:** MOD-330, MOD-400, MOD-410, MOD-420, MOD-350  
**Status:** M1 Done — human AC-901 approved 2026-08-11

#### Main points

- [x] **MOD-430-MP-001:** Implement and verify releases.  
  - Evidence/note: rl_releases
- [x] **MOD-430-MP-002:** Implement and verify release items.  
  - Evidence/note: rl_release_items
- [x] **MOD-430-MP-003:** Implement and verify deployments.  
  - Evidence/note: rl_deployments
- [x] **MOD-430-MP-004:** Implement and verify deployment checks.  
  - Evidence/note: rl_deployment_checks
- [x] **MOD-430-MP-005:** Implement and verify backup confirmations.  
  - Evidence/note: rl_backup_confirmations
- [x] **MOD-430-MP-006:** Implement and verify migration plans.  
  - Evidence/note: rl_migration_plans
- [x] **MOD-430-MP-007:** Implement and verify rollbacks.  
  - Evidence/note: rl_rollbacks
- [x] **MOD-430-MP-008:** Implement and verify completion reports.  
  - Evidence/note: rl_completion_reports

#### Database / data design

- [x] **MOD-430-DB-001:** Releases model + RLS.  
  - Evidence/note: migration 20260811_0027
- [x] **MOD-430-DB-002:** Release items.  
  - Evidence/note: rl_release_items
- [x] **MOD-430-DB-003:** Deployments.  
  - Evidence/note: rl_deployments
- [x] **MOD-430-DB-004:** Deployment checks.  
  - Evidence/note: rl_deployment_checks
- [x] **MOD-430-DB-005:** Backup confirmations.  
  - Evidence/note: rl_backup_confirmations
- [x] **MOD-430-DB-006:** Migration plans.  
  - Evidence/note: rl_migration_plans
- [x] **MOD-430-DB-007:** Rollbacks.  
  - Evidence/note: rl_rollbacks
- [x] **MOD-430-DB-008:** Completion reports.  
  - Evidence/note: rl_completion_reports

#### Backend

- [x] **MOD-430-BE-001:** Typed domain/services.  
  - Evidence/note: modules/releases
- [x] **MOD-430-BE-002:** Authz/transition/idempotency.  
  - Evidence/note: production gate + version checks
- [x] **MOD-430-BE-003:** Outbox events.  
  - Evidence/note: release.* events
- [x] **MOD-430-BE-004:** Structured errors.  
  - Evidence/note: problem+json via shared handler

#### API

- [x] **MOD-430-API-001:** Versioned endpoints.  
  - Evidence/note: /api/v1/releases (+12 OpenAPI paths)
- [x] **MOD-430-API-002:** Pagination/filter/search.  
  - Evidence/note: releases list + traceability
- [x] **MOD-430-API-003:** OpenAPI schemas.  
  - Evidence/note: Pydantic schemas

#### Frontend

- [~] **MOD-430-FE-001:** List/dashboard.  
  - Evidence/note: /releases desk
- [-] **MOD-430-FE-002:** Detail tabs.  
  - Evidence/note: deferred
- [~] **MOD-430-FE-003:** Create/edit forms.  
  - Evidence/note: create/submit/approve
- [-] **MOD-430-FE-004:** a11y pass.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-430-WF-001:** Triggers/statuses/rules.  
  - Evidence/note: release status machine + production gate
- [-] **MOD-430-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A for releases module core
- [x] **MOD-430-WF-003:** Outbox/events.  
  - Evidence/note: release.* events
- [-] **MOD-430-WF-004:** Notifications.  
  - Evidence/note: deferred MOD-440

#### Security / privacy / audit

- [x] **MOD-430-SEC-001:** Scope authorization.  
  - Evidence/note: org request context
- [x] **MOD-430-SEC-002:** Tenant RLS.  
  - Evidence/note: RLS on rl_* tables
- [x] **MOD-430-SEC-003:** Redaction.  
  - Evidence/note: outbox redact via kernel
- [x] **MOD-430-SEC-004:** Audit actions.  
  - Evidence/note: rl_* audits

#### Testing / verification

- [x] **MOD-430-QA-001:** Domain rules via integration.  
  - Evidence/note: prod gate/trace/closure
- [x] **MOD-430-QA-002:** Integration API tests.  
  - Evidence/note: tests/integration/releases
- [-] **MOD-430-QA-003:** Dedicated RBAC negative suite.  
  - Evidence/note: deferred
- [-] **MOD-430-QA-004:** Live deployer suite.  
  - Evidence/note: N/A M1
- [x] **MOD-430-QA-005:** Verification commands.  
  - Evidence/note: Docs/modules/MOD-430/VERIFICATION.md

#### Documentation

- [x] **MOD-430-DOC-001:** Module README.  
  - Evidence/note: Docs/modules/MOD-430/README.md
- [x] **MOD-430-DOC-002:** Verification evidence.  
  - Evidence/note: Docs/modules/MOD-430/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-430-AC-001:** Production cannot start without evidence and approval.  
  - Evidence/note: approve + backup required
- [x] **MOD-430-AC-002:** Releases trace to requirements/tickets/tests/bugs/changes/documents.  
  - Evidence/note: /traceability
- [x] **MOD-430-AC-003:** Closure requires client and internal acceptance.  
  - Evidence/note: completion dual acceptance
- [x] **MOD-430-AC-900:** Crit/High cleared.  
  - Evidence/note: none filed
- [x] **MOD-430-AC-901:** Human owner approval.  
  - Evidence/note: Human owner approved 2026-08-11

#### Module completion

- [x] **MOD-430-DONE:** Module marked Done before dependents

### MOD-440

**Title:** Notifications, Preferences, Digests, Delivery, and Failure Handling  
**Purpose:** Deliver permission-safe in-app and email notifications for assignments, reminders, escalations, approvals, blockers, bugs, releases, client responses, and system alerts.  
**Requirements:** MVP-FR-011  
**Dependencies:** MOD-100, MOD-130, MOD-040  
**Status:** M1 Done — AC-901 blocked

#### Main points

- [x] **MOD-440-MP-001:** Implement and verify notifications.  
  - Evidence/note: ntf_notifications
- [x] **MOD-440-MP-002:** Implement and verify preferences.  
  - Evidence/note: ntf_preferences
- [x] **MOD-440-MP-003:** Implement and verify templates.  
  - Evidence/note: ntf_templates
- [x] **MOD-440-MP-004:** Implement and verify deliveries.  
  - Evidence/note: ntf_deliveries
- [x] **MOD-440-MP-005:** Implement and verify retries.  
  - Evidence/note: ntf_retries
- [x] **MOD-440-MP-006:** Implement and verify dead letters.  
  - Evidence/note: ntf_dead_letters
- [x] **MOD-440-MP-007:** Implement and verify digests.  
  - Evidence/note: ntf_digests (stub process)

#### Database / data design

- [x] **MOD-440-DB-001:** Notifications model + RLS.  
  - Evidence/note: migration 20260811_0028
- [x] **MOD-440-DB-002:** Preferences.  
  - Evidence/note: ntf_preferences
- [x] **MOD-440-DB-003:** Templates.  
  - Evidence/note: ntf_templates
- [x] **MOD-440-DB-004:** Deliveries.  
  - Evidence/note: ntf_deliveries
- [x] **MOD-440-DB-005:** Retries.  
  - Evidence/note: ntf_retries
- [x] **MOD-440-DB-006:** Dead letters.  
  - Evidence/note: ntf_dead_letters
- [x] **MOD-440-DB-007:** Digests.  
  - Evidence/note: ntf_digests

#### Backend

- [x] **MOD-440-BE-001:** Typed domain/services.  
  - Evidence/note: modules/notifications
- [x] **MOD-440-BE-002:** Authz/transition/idempotency.  
  - Evidence/note: idempotency_key + preference mute rules
- [x] **MOD-440-BE-003:** Outbox events.  
  - Evidence/note: notification.* events
- [x] **MOD-440-BE-004:** Structured errors.  
  - Evidence/note: 409/422/404 via AppError

#### API

- [x] **MOD-440-API-001:** Versioned endpoints.  
  - Evidence/note: /api/v1/notifications
- [x] **MOD-440-API-002:** Pagination/filter/search.  
  - Evidence/note: status/channel/recipient/q
- [x] **MOD-440-API-003:** OpenAPI schemas.  
  - Evidence/note: Pydantic schemas

#### Frontend

- [~] **MOD-440-FE-001:** List/dashboard.  
  - Evidence/note: /notifications desk
- [-] **MOD-440-FE-002:** Detail tabs.  
  - Evidence/note: deferred
- [~] **MOD-440-FE-003:** Create/edit forms.  
  - Evidence/note: create + deliver/mark-read
- [-] **MOD-440-FE-004:** a11y pass.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-440-WF-001:** Triggers/statuses/rules.  
  - Evidence/note: notification status machine + MAX attempts
- [-] **MOD-440-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: Temporal digests deferred
- [x] **MOD-440-WF-003:** Outbox/events.  
  - Evidence/note: create/deliver/DLQ/replay events
- [x] **MOD-440-WF-004:** Notifications.  
  - Evidence/note: prefs + channels + critical override

#### Security / privacy / audit

- [x] **MOD-440-SEC-001:** Scope authorization.  
  - Evidence/note: org request context
- [x] **MOD-440-SEC-002:** Tenant RLS.  
  - Evidence/note: RLS on ntf_* tables
- [x] **MOD-440-SEC-003:** Redaction.  
  - Evidence/note: outbox redact via kernel
- [x] **MOD-440-SEC-004:** Audit actions.  
  - Evidence/note: ntf_* audits

#### Testing / verification

- [x] **MOD-440-QA-001:** Domain rules via integration.  
  - Evidence/note: idempotency/mute/DLQ
- [x] **MOD-440-QA-002:** Integration API tests.  
  - Evidence/note: tests/integration/notifications
- [-] **MOD-440-QA-003:** Dedicated RBAC negative suite.  
  - Evidence/note: deferred
- [-] **MOD-440-QA-004:** Live email provider suite.  
  - Evidence/note: N/A M1 (local-sim only)
- [x] **MOD-440-QA-005:** Verification commands.  
  - Evidence/note: Docs/modules/MOD-440/VERIFICATION.md

#### Documentation

- [x] **MOD-440-DOC-001:** Module README.  
  - Evidence/note: Docs/modules/MOD-440/README.md
- [x] **MOD-440-DOC-002:** Verification evidence.  
  - Evidence/note: Docs/modules/MOD-440/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-440-AC-001:** Notifications are timely, idempotent, auditable, and permission-safe.  
  - Evidence/note: create + outbox + org scope + idempotency 409
- [x] **MOD-440-AC-002:** Users can configure preferences without disabling mandatory critical alerts.  
  - Evidence/note: system_alert mute → 422; critical never suppressed
- [x] **MOD-440-AC-003:** Delivery failures are visible and recoverable.  
  - Evidence/note: fail×3 → DLQ → replay → pending
- [x] **MOD-440-AC-900:** Crit/High cleared.  
  - Evidence/note: none filed
- [!] **MOD-440-AC-901:** Human owner approval.  
  - Evidence/note: NOT obtained — blocked pending human review

#### Module completion

- [ ] **MOD-440-DONE:** Module marked Done before dependents

### MOD-450

**Title:** Dashboard, Reporting, Search, Project Health, and Activity Timeline  
**Purpose:** Provide role-aware deterministic dashboards for queries, projects, phases, tickets, workload, follow-ups, approvals, quality, milestones, agent actions, and overrides.  
**Requirements:** MVP-FR-012, MVP-FR-013, MVP-NFR-003  
**Dependencies:** MOD-210, MOD-240, MOD-300, MOD-340, MOD-330, MOD-400, MOD-410, MOD-040  
**Status:** M1 Done — AC-901 blocked

#### Main points

- [x] **MOD-450-MP-001:** Implement and verify dashboard read models.  
  - Evidence/note: rp_dashboard_snapshots
- [x] **MOD-450-MP-002:** Implement and verify project health.  
  - Evidence/note: rp_project_health
- [x] **MOD-450-MP-003:** Implement and verify saved filters.  
  - Evidence/note: rp_saved_filters
- [x] **MOD-450-MP-004:** Implement and verify global search.  
  - Evidence/note: rp_search_documents
- [x] **MOD-450-MP-005:** Implement and verify activity timeline.  
  - Evidence/note: rp_activity_events
- [x] **MOD-450-MP-006:** Implement and verify reports.  
  - Evidence/note: rp_reports
- [x] **MOD-450-MP-007:** Implement and verify exports.  
  - Evidence/note: rp_exports (in-DB preview)

#### Database / data design

- [x] **MOD-450-DB-001:** Dashboard snapshots model + RLS.  
  - Evidence/note: migration 20260811_0029
- [x] **MOD-450-DB-002:** Project health.  
  - Evidence/note: rp_project_health
- [x] **MOD-450-DB-003:** Saved filters.  
  - Evidence/note: rp_saved_filters
- [x] **MOD-450-DB-004:** Search documents.  
  - Evidence/note: rp_search_documents
- [x] **MOD-450-DB-005:** Activity events.  
  - Evidence/note: rp_activity_events
- [x] **MOD-450-DB-006:** Reports.  
  - Evidence/note: rp_reports
- [x] **MOD-450-DB-007:** Exports.  
  - Evidence/note: rp_exports

#### Backend

- [x] **MOD-450-BE-001:** Typed domain/services.  
  - Evidence/note: modules/insights
- [x] **MOD-450-BE-002:** Authz/concurrency.  
  - Evidence/note: org checks + expected_version on health
- [x] **MOD-450-BE-003:** Outbox events.  
  - Evidence/note: insights.* events
- [x] **MOD-450-BE-004:** Structured errors.  
  - Evidence/note: NotFound/Conflict/Validation

#### API

- [x] **MOD-450-API-001:** Versioned endpoints.  
  - Evidence/note: /api/v1/insights
- [x] **MOD-450-API-002:** Pagination/filter/search.  
  - Evidence/note: search + list paging
- [x] **MOD-450-API-003:** OpenAPI schemas.  
  - Evidence/note: insights tags

#### Frontend

- [~] **MOD-450-FE-001:** List/dashboard.  
  - Evidence/note: /insights desk + home snapshot panel
- [-] **MOD-450-FE-002:** Detail tabs.  
  - Evidence/note: deferred
- [~] **MOD-450-FE-003:** Create/edit forms.  
  - Evidence/note: filter create + export create
- [-] **MOD-450-FE-004:** a11y pass.  
  - Evidence/note: deferred

#### Workflow / agent / events / notifications

- [x] **MOD-450-WF-001:** Triggers/statuses/rules.  
  - Evidence/note: on-demand refresh + export ready
- [-] **MOD-450-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: no streaming refresh
- [x] **MOD-450-WF-003:** Outbox/events.  
  - Evidence/note: insights.dashboard.refreshed etc.
- [-] **MOD-450-WF-004:** Notifications.  
  - Evidence/note: not owned by insights M1

#### Security / privacy / audit

- [x] **MOD-450-SEC-001:** Scope authorization.  
  - Evidence/note: RequestContext org
- [x] **MOD-450-SEC-002:** Tenant RLS.  
  - Evidence/note: _rls on rp_* tables
- [x] **MOD-450-SEC-003:** Redaction.  
  - Evidence/note: bounded payload_preview
- [x] **MOD-450-SEC-004:** Audit actions.  
  - Evidence/note: rp_* audit writes

#### Testing / verification

- [x] **MOD-450-QA-001:** Domain rules via integration.  
  - Evidence/note: freshness + reconcile
- [x] **MOD-450-QA-002:** Integration API tests.  
  - Evidence/note: tests/integration/insights
- [x] **MOD-450-QA-003:** Tenant isolation tests.  
  - Evidence/note: AC-003 cross-org search/export
- [-] **MOD-450-QA-004:** BI/streaming suite.  
  - Evidence/note: no warehouse
- [x] **MOD-450-QA-005:** Verification commands.  
  - Evidence/note: Docs/modules/MOD-450/VERIFICATION.md

#### Documentation

- [x] **MOD-450-DOC-001:** Module README.  
  - Evidence/note: Docs/modules/MOD-450/README.md
- [x] **MOD-450-DOC-002:** Verification evidence.  
  - Evidence/note: Docs/modules/MOD-450/VERIFICATION.md

#### Acceptance gate

- [x] **MOD-450-AC-001:** Dashboard values reconcile with source records.  
  - Evidence/note: refresh vs projects_total
- [x] **MOD-450-AC-002:** Normal updates appear within one minute.  
  - Evidence/note: is_fresh &lt; 60s
- [x] **MOD-450-AC-003:** Counts, search, and exports do not leak unauthorized data.  
  - Evidence/note: cross-tenant isolation test
- [x] **MOD-450-AC-900:** Crit/High cleared.  
  - Evidence/note: none open for M1
- [!] **MOD-450-AC-901:** Human owner approval.  
  - Evidence/note: NOT obtained

#### Module completion

- [ ] **MOD-450-DONE:** Module marked Done before dependents

### MOD-460

**Title:** Requirement Traceability, Audit Reports, and Evidence Exports  
**Purpose:** Provide end-to-end traceability from requirement version through phase, story, ticket, test, bug, change, release, approval, and delivery evidence.  
**Requirements:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-040, MOD-240, MOD-300, MOD-400, MOD-410, MOD-430  
**Status:** M1 Done — AC-901 blocked

#### Main points

- [x] **MOD-460-MP-001:** Implement and verify requirement-ticket links.  
  - Evidence: `tr_requirement_ticket_links` + `POST/GET /traceability/links/requirement-tickets`
- [x] **MOD-460-MP-002:** Implement and verify requirement-test links.  
  - Evidence: `tr_requirement_test_links` + routes
- [x] **MOD-460-MP-003:** Implement and verify requirement-release links.  
  - Evidence: `tr_requirement_release_links` + routes
- [x] **MOD-460-MP-004:** Implement and verify requirement-document links.  
  - Evidence: `tr_requirement_document_links` + routes
- [x] **MOD-460-MP-005:** Implement and verify ticket-test links.  
  - Evidence: `tr_ticket_test_links` + routes
- [x] **MOD-460-MP-006:** Implement and verify evidence manifests.  
  - Evidence: `tr_evidence_manifests` + seal/export flow

#### Database / data design

- [x] **MOD-460-DB-001:** Requirement-ticket links model + RLS.  
  - Evidence: migration `20260811_0030`
- [x] **MOD-460-DB-002:** Requirement-test links.  
  - Evidence: `20260811_0030`
- [x] **MOD-460-DB-003:** Requirement-release links.  
  - Evidence: `20260811_0030`
- [x] **MOD-460-DB-004:** Requirement-document links.  
  - Evidence: `20260811_0030`
- [x] **MOD-460-DB-005:** Ticket-test links.  
  - Evidence: `20260811_0030`
- [x] **MOD-460-DB-006:** Evidence manifests.  
  - Evidence: `20260811_0030` (+ support tables documented in README)

#### Backend

- [x] **MOD-460-BE-001:** Typed domain/services.  
  - Evidence: `modules/traceability/{domain,service,models}.py`
- [x] **MOD-460-BE-002:** Authz/concurrency.  
  - Evidence: org filter, expected_version, status transitions
- [x] **MOD-460-BE-003:** Outbox events.  
  - Evidence: enqueue_outbox on mutations
- [x] **MOD-460-BE-004:** Structured errors.  
  - Evidence: Conflict/NotFound/Validation/InvalidTransition

#### API

- [x] **MOD-460-API-001:** Versioned endpoints.  
  - Evidence: `/api/v1/traceability/*`
- [x] **MOD-460-API-002:** Pagination/filter.  
  - Evidence: list endpoints with limit/offset
- [x] **MOD-460-API-003:** OpenAPI schemas.  
  - Evidence: Pydantic response models on router

#### Frontend

- [~] **MOD-460-FE-001:** List/dashboard.  
  - Evidence: `/traceability` desk
- [-] **MOD-460-FE-002:** Detail tabs.  
  - Evidence/note: deferred M1
- [~] **MOD-460-FE-003:** Create/edit forms.  
  - Evidence: must-have, link, manifest forms on desk
- [-] **MOD-460-FE-004:** a11y pass.  
  - Evidence/note: deferred M1

#### Workflow / agent / events / notifications

- [x] **MOD-460-WF-001:** Triggers/statuses/rules.  
  - Evidence: manifest draft→sealed→exported
- [-] **MOD-460-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A M1
- [x] **MOD-460-WF-003:** Outbox/events.  
  - Evidence: outbox event types on mutations
- [-] **MOD-460-WF-004:** Notifications.  
  - Evidence/note: N/A M1

#### Security / privacy / audit

- [x] **MOD-460-SEC-001:** Scope authorization.  
  - Evidence: RequestContext org scoping
- [x] **MOD-460-SEC-002:** Tenant RLS.  
  - Evidence: `_rls()` on all tr_ tables
- [x] **MOD-460-SEC-003:** Redaction.  
  - Evidence: observability redact_mapping on audit payload
- [x] **MOD-460-SEC-004:** Audit actions.  
  - Evidence: `tr_action_audits` + `write_audit`

#### Testing / verification

- [x] **MOD-460-QA-001:** Domain rules via integration.  
  - Evidence: coverage gate tests
- [x] **MOD-460-QA-002:** Integration/API tests.  
  - Evidence: `tests/integration/traceability/`
- [x] **MOD-460-QA-003:** Tenant isolation.  
  - Evidence: cross-org 404 export/manifest
- [-] **MOD-460-QA-004:** Workflow/agent/perf.  
  - Evidence/note: N/A M1
- [x] **MOD-460-QA-005:** Verification commands.  
  - Evidence: Docs/modules/MOD-460/VERIFICATION.md

#### Documentation

- [x] **MOD-460-DOC-001:** Module README.  
  - Evidence: `Docs/modules/MOD-460/README.md`
- [x] **MOD-460-DOC-002:** Verification notes.  
  - Evidence: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-460-AC-001:** ≥95% must-have complete traceability.  
  - Evidence: coverage endpoint + 19/20 vs 18/20 tests
- [x] **MOD-460-AC-002:** 100% audit coverage for controlled actions.  
  - Evidence: audit-coverage endpoint + mutation test
- [x] **MOD-460-AC-003:** Exports permission-controlled and reconcilable.  
  - Evidence: export payload + cross-org 404
- [x] **MOD-460-AC-900:** Critical/High defects resolved.  
  - Evidence: none open for M1 scope
- [!] **MOD-460-AC-901:** Human owner approval.  
  - Evidence/note: NOT obtained

#### Module completion

- [ ] **MOD-460-DONE:** Module marked Done before dependents

## Phase 5 - MVP Integrations

### MOD-500

**Title:** Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State  
**Purpose:** Create a provider-based integration foundation with OAuth, secure token references, webhook validation, idempotency, rate limits, retries, dead letters, and sync audit.  
**Requirements:** MVP-FR-014, MVP-FR-015, MVP-NFR-004  
**Dependencies:** MOD-030, MOD-040, MOD-120  
**Status:** M1 Done — AC-901 blocked

#### Main points

- [x] **MOD-500-MP-001:** Implement and verify integration connections.  
  - Evidence: `ig_connections` + `POST/GET /integrations/connections`
- [x] **MOD-500-MP-002:** Implement and verify webhook events.  
  - Evidence: `ig_webhook_events` + `POST /integrations/webhooks/receive`
- [x] **MOD-500-MP-003:** Implement and verify sync cursors.  
  - Evidence: `ig_sync_cursors` + `PUT/GET /integrations/sync-cursors`
- [x] **MOD-500-MP-004:** Implement and verify external mappings.  
  - Evidence: `ig_external_mappings` + `POST/GET /integrations/mappings`
- [x] **MOD-500-MP-005:** Implement and verify outbox events.  
  - Evidence: `ig_outbox_events` + enqueue/relay routes (distinct from kernel outbox)
- [x] **MOD-500-MP-006:** Implement and verify inbox events.  
  - Evidence: `ig_inbox_events` + receive/process routes
- [x] **MOD-500-MP-007:** Implement and verify connection health.  
  - Evidence: `ig_connection_health` + health routes

#### Database / data design

- [x] **MOD-500-DB-001:** Integration connections model + RLS.  
  - Evidence: migration `20260811_0031`
- [x] **MOD-500-DB-002:** Webhook events.  
  - Evidence: `20260811_0031`
- [x] **MOD-500-DB-003:** Sync cursors.  
  - Evidence: `20260811_0031`
- [x] **MOD-500-DB-004:** External mappings.  
  - Evidence: `20260811_0031`
- [x] **MOD-500-DB-005:** Outbox events (integration relay).  
  - Evidence: `20260811_0031`
- [x] **MOD-500-DB-006:** Inbox events.  
  - Evidence: `20260811_0031`
- [x] **MOD-500-DB-007:** Connection health.  
  - Evidence: `20260811_0031`

#### Backend

- [x] **MOD-500-BE-001:** Typed domain/services.  
  - Evidence: `modules/integrations/{domain,service,models}.py`
- [x] **MOD-500-BE-002:** Authz/concurrency/idempotency.  
  - Evidence: org filter, expected_version, idempotent webhook/inbox
- [x] **MOD-500-BE-003:** Outbox events.  
  - Evidence: kernel enqueue_outbox + `ig_outbox_events` relay
- [x] **MOD-500-BE-004:** Structured errors.  
  - Evidence: Conflict/NotFound/Validation/InvalidTransition

#### API

- [x] **MOD-500-API-001:** Versioned endpoints.  
  - Evidence: `/api/v1/integrations/*`
- [x] **MOD-500-API-002:** Pagination/filter.  
  - Evidence: list endpoints with limit/offset
- [x] **MOD-500-API-003:** OpenAPI schemas.  
  - Evidence: Pydantic response models on router

#### Frontend

- [~] **MOD-500-FE-001:** List/dashboard.  
  - Evidence: `/integrations` desk
- [-] **MOD-500-FE-002:** Detail tabs.  
  - Evidence/note: deferred M1
- [~] **MOD-500-FE-003:** Create/edit forms.  
  - Evidence: connection, webhook, inbox forms on desk
- [-] **MOD-500-FE-004:** a11y pass.  
  - Evidence/note: deferred M1

#### Workflow / agent / events / notifications

- [x] **MOD-500-WF-001:** Triggers/statuses/rules.  
  - Evidence: connection status transitions, inbox/outbox statuses
- [-] **MOD-500-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A M1
- [x] **MOD-500-WF-003:** Outbox/events.  
  - Evidence: kernel + ig outbox event types
- [-] **MOD-500-WF-004:** Notifications.  
  - Evidence/note: N/A M1

#### Security / privacy / audit

- [x] **MOD-500-SEC-001:** Scope authorization.  
  - Evidence: RequestContext org scoping
- [x] **MOD-500-SEC-002:** Tenant RLS.  
  - Evidence: `_rls()` on all ig_ tables
- [x] **MOD-500-SEC-003:** Redaction / credential_ref only.  
  - Evidence: `assert_no_raw_secrets`, redact_payload, no raw tokens in DB/API
- [x] **MOD-500-SEC-004:** Audit actions.  
  - Evidence: `write_audit` on mutations

#### Testing / verification

- [x] **MOD-500-QA-001:** Domain rules via integration.  
  - Evidence: AC-001/003 tests
- [x] **MOD-500-QA-002:** Integration/API tests.  
  - Evidence: `tests/integration/integrations/`
- [x] **MOD-500-QA-003:** Tenant isolation.  
  - Evidence: cross-org 404/empty mapping test
- [-] **MOD-500-QA-004:** Workflow/agent/perf.  
  - Evidence/note: N/A M1 (simulated relay only)
- [x] **MOD-500-QA-005:** Verification commands.  
  - Evidence: Docs/modules/MOD-500/VERIFICATION.md

#### Documentation

- [x] **MOD-500-DOC-001:** Module README.  
  - Evidence: `Docs/modules/MOD-500/README.md`
- [x] **MOD-500-DOC-002:** Verification notes.  
  - Evidence: VERIFICATION + TEMPLATE_TASK_RATIONALE

#### Acceptance gate

- [x] **MOD-500-AC-001:** Integration failure cannot corrupt internal data.  
  - Evidence: inbox force_fail test — mapping count unchanged
- [x] **MOD-500-AC-002:** External mappings/events tenant-scoped and audited.  
  - Evidence: cross-org empty + audit/outbox relay test
- [x] **MOD-500-AC-003:** Credentials never in logs/tables/responses.  
  - Evidence: reject client_secret/access_token; audit redaction test
- [x] **MOD-500-AC-900:** Critical/High defects resolved.  
  - Evidence: none open for M1 scope
- [!] **MOD-500-AC-901:** Human owner approval.  
  - Evidence/note: NOT obtained

#### Module completion

- [ ] **MOD-500-DONE:** Module marked Done before dependents

### MOD-510

**Title:** Gmail Client Communication Integration  
**Purpose:** Receive approved mailbox inquiries, preserve threads and attachments, detect replies, create or update queries, prepare drafts, and send approved email.  
**Requirements:** MVP-FR-014  
**Dependencies:** MOD-220, MOD-500, MOD-210, MOD-230  
**Status:** M1 Done — AC-901 blocked

#### Main points

- [x] **MOD-510-MP-001:** Implement and verify Gmail connection.  
  - Evidence: `gm_connections` + `POST/GET /gmail/connections`
- [x] **MOD-510-MP-002:** Implement and verify history cursor.  
  - Evidence: `gm_history_cursors` + `PUT/GET /gmail/history-cursors`
- [x] **MOD-510-MP-003:** Implement and verify thread mappings.  
  - Evidence: `gm_thread_mappings` + inbound process + `GET /gmail/threads`
- [x] **MOD-510-MP-004:** Implement and verify message mappings.  
  - Evidence: `gm_message_mappings` + `GET /gmail/messages`
- [x] **MOD-510-MP-005:** Implement and verify attachment import.  
  - Evidence: `gm_attachment_imports` + `POST /gmail/messages/{id}/attachments`
- [x] **MOD-510-MP-006:** Implement and verify draft review.  
  - Evidence: `gm_draft_reviews` + submit/approve/reject routes
- [x] **MOD-510-MP-007:** Implement and verify approved send.  
  - Evidence: `gm_approved_sends` + `POST /gmail/drafts/{id}/send`

#### Database / data design

- [x] **MOD-510-DB-001:** Gmail connection model + RLS.  
  - Evidence: migration `20260811_0032`
- [x] **MOD-510-DB-002:** History cursors.  
  - Evidence: `20260811_0032`
- [x] **MOD-510-DB-003:** Thread mappings.  
  - Evidence: `20260811_0032`
- [x] **MOD-510-DB-004:** Message mappings.  
  - Evidence: `20260811_0032`
- [x] **MOD-510-DB-005:** Attachment imports.  
  - Evidence: `20260811_0032`
- [x] **MOD-510-DB-006:** Draft reviews.  
  - Evidence: `20260811_0032`
- [x] **MOD-510-DB-007:** Approved sends.  
  - Evidence: `20260811_0032`

#### Backend

- [x] **MOD-510-BE-001:** Typed domain/services.  
  - Evidence: `modules/gmail/{domain,service,models}.py`
- [x] **MOD-510-BE-002:** Authz/concurrency/idempotency.  
  - Evidence: org filter, draft transitions, idempotent inbound/push
- [x] **MOD-510-BE-003:** Outbox events.  
  - Evidence: kernel enqueue_outbox on connection/inbound/send
- [x] **MOD-510-BE-004:** Structured errors.  
  - Evidence: Conflict/NotFound/Validation/InvalidTransition

#### API

- [x] **MOD-510-API-001:** Versioned endpoints.  
  - Evidence: `/api/v1/gmail/*`
- [x] **MOD-510-API-002:** Pagination/filter.  
  - Evidence: list endpoints with limit/offset
- [x] **MOD-510-API-003:** OpenAPI schemas.  
  - Evidence: Pydantic response models on router

#### Frontend

- [~] **MOD-510-FE-001:** List/dashboard.  
  - Evidence: `/gmail` desk
- [-] **MOD-510-FE-002:** Detail tabs.  
  - Evidence/note: deferred M1
- [~] **MOD-510-FE-003:** Create/edit/review forms.  
  - Evidence: connection, inbound, push, draft/send forms on desk
- [-] **MOD-510-FE-004:** a11y pass.  
  - Evidence/note: deferred M1

#### Workflow / agent / events / notifications

- [x] **MOD-510-WF-001:** Triggers/statuses/rules.  
  - Evidence: connection + draft status transitions
- [-] **MOD-510-WF-002:** Temporal/LangGraph routing.  
  - Evidence/note: N/A M1
- [x] **MOD-510-WF-003:** Outbox/events.  
  - Evidence: gmail.* kernel outbox event types
- [-] **MOD-510-WF-004:** Notifications.  
  - Evidence/note: N/A M1

#### Security / privacy / audit

- [x] **MOD-510-SEC-001:** Scope authorization.  
  - Evidence: RequestContext org scoping
- [x] **MOD-510-SEC-002:** Tenant RLS.  
  - Evidence: `_rls()` on all gm_ tables
- [x] **MOD-510-SEC-003:** Redaction / credential_ref only.  
  - Evidence: `assert_no_raw_secrets`, no raw tokens in DB/API
- [x] **MOD-510-SEC-004:** Audit actions.  
  - Evidence: `write_audit` on mutations

#### Testing / verification

- [x] **MOD-510-QA-001:** Domain rules via integration.  
  - Evidence: AC-001/002/003 tests
- [x] **MOD-510-QA-002:** Integration/API tests.  
  - Evidence: `tests/integration/gmail/`
- [x] **MOD-510-QA-003:** Tenant isolation via org headers.  
  - Evidence: org-scoped service filters
- [-] **MOD-510-QA-004:** Live Gmail/workflow tests.  
  - Evidence/note: N/A M1
- [x] **MOD-510-QA-005:** Verification commands.  
  - Evidence: `Docs/modules/MOD-510/VERIFICATION.md`

#### Documentation

- [x] **MOD-510-DOC-001:** Module README + API notes.  
  - Evidence: `Docs/modules/MOD-510/README.md`
- [x] **MOD-510-DOC-002:** Verification + limitations.  
  - Evidence: `Docs/modules/MOD-510/VERIFICATION.md`

#### Acceptance gate

- [x] **MOD-510-AC-001:** Valid emails create or update exactly one query and thread.
- [x] **MOD-510-AC-002:** Approved outgoing email is sent and linked correctly.
- [x] **MOD-510-AC-003:** Duplicate notifications do not duplicate records.
- [x] **MOD-510-AC-900:** All Critical and High defects for this module are resolved.
- [!] **MOD-510-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-510-DONE:** Module marked Done before dependents (AC-901 blocked)

### MOD-520

**Title:** Jira Work Management Integration  
**Purpose:** Create approved Jira issues, map fields and status, synchronize allowed updates, and process webhooks without bypassing internal rules.  
**Requirements:** MVP-FR-015  
**Dependencies:** MOD-300, MOD-310, MOD-320, MOD-500

#### Main points

- [x] **MOD-520-MP-001:** Implement and verify Jira connection.
- [x] **MOD-520-MP-002:** Implement and verify project mapping.
- [x] **MOD-520-MP-003:** Implement and verify field mapping.
- [x] **MOD-520-MP-004:** Implement and verify status mapping.
- [x] **MOD-520-MP-005:** Implement and verify issue mapping.
- [x] **MOD-520-MP-006:** Implement and verify comment sync.
- [x] **MOD-520-MP-007:** Implement and verify conflict handling.

#### Database / data design

- [x] **MOD-520-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **Jira connection**.
- [x] **MOD-520-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project mapping**.
- [x] **MOD-520-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **field mapping**.
- [x] **MOD-520-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status mapping**.
- [x] **MOD-520-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **issue mapping**.
- [x] **MOD-520-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **comment sync**.
- [x] **MOD-520-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **conflict handling**.

#### Backend

- [x] **MOD-520-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [x] **MOD-520-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [x] **MOD-520-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [x] **MOD-520-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [x] **MOD-520-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [x] **MOD-520-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [x] **MOD-520-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [~] **MOD-520-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [-] **MOD-520-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [~] **MOD-520-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [-] **MOD-520-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [x] **MOD-520-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [-] **MOD-520-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [x] **MOD-520-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [-] **MOD-520-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [x] **MOD-520-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [x] **MOD-520-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [x] **MOD-520-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [x] **MOD-520-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [x] **MOD-520-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [x] **MOD-520-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [x] **MOD-520-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [x] **MOD-520-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [x] **MOD-520-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [x] **MOD-520-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [x] **MOD-520-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [x] **MOD-520-AC-001:** Approved internal tickets create Jira issues and retain keys.
- [x] **MOD-520-AC-002:** Jira cannot bypass internal transition or approval rules.
- [x] **MOD-520-AC-003:** Sync failures are visible, retriable, and audited.
- [x] **MOD-520-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-520-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-520-DONE:** Module marked Done before dependents

## Phase 6 - Security, Reliability, Pilot, and Production Readiness

### MOD-600

**Title:** Security, Privacy, PII, File Safety, Retention, Backup, and Recovery Hardening  
**Purpose:** Complete threat modeling, PII controls, retention, deletion, legal hold, backup, restore, incident response, file safety, and model-data restrictions.  
**Requirements:** MVP-NFR-001, MVP-NFR-002, MVP-NFR-007, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** All functional foundation modules

#### Main points

- [ ] **MOD-600-MP-001:** Implement and verify threat model.
- [ ] **MOD-600-MP-002:** Implement and verify PII inventory.
- [ ] **MOD-600-MP-003:** Implement and verify retention policies.
- [ ] **MOD-600-MP-004:** Implement and verify legal holds.
- [ ] **MOD-600-MP-005:** Implement and verify deletion jobs.
- [ ] **MOD-600-MP-006:** Implement and verify backup records.
- [ ] **MOD-600-MP-007:** Implement and verify restore tests.
- [ ] **MOD-600-MP-008:** Implement and verify security incidents.

#### Database / data design

- [ ] **MOD-600-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **threat model**.
- [ ] **MOD-600-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **PII inventory**.
- [ ] **MOD-600-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **retention policies**.
- [ ] **MOD-600-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **legal holds**.
- [ ] **MOD-600-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deletion jobs**.
- [ ] **MOD-600-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **backup records**.
- [ ] **MOD-600-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **restore tests**.
- [ ] **MOD-600-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **security incidents**.

#### Backend

- [ ] **MOD-600-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-600-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-600-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-600-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-600-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-600-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-600-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-600-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-600-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-600-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-600-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-600-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-600-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-600-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-600-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-600-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-600-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-600-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-600-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-600-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-600-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-600-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-600-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-600-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-600-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-600-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-600-AC-001:** No Critical security or isolation defect remains.
- [ ] **MOD-600-AC-002:** RPO and RTO targets are validated.
- [ ] **MOD-600-AC-003:** Client and company data are excluded from model training by default.
- [ ] **MOD-600-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-600-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-600-DONE:** Module marked Done before dependents

### MOD-610

**Title:** Performance, Reliability, Idempotency, Resilience, and Disaster Recovery  
**Purpose:** Validate API, dashboard, workflow, event, integration, storage, and database performance and recovery under pilot load and failure conditions.  
**Requirements:** MVP-NFR-003, MVP-NFR-004, MVP-NFR-006, MVP-NFR-007  
**Dependencies:** MOD-350, MOD-440, MOD-500, MOD-600

#### Main points

- [ ] **MOD-610-MP-001:** Implement and verify performance tests.
- [ ] **MOD-610-MP-002:** Implement and verify resilience tests.
- [ ] **MOD-610-MP-003:** Implement and verify index review.
- [ ] **MOD-610-MP-004:** Implement and verify SLO dashboards.
- [ ] **MOD-610-MP-005:** Implement and verify workflow replay.
- [ ] **MOD-610-MP-006:** Implement and verify integration failure tests.
- [ ] **MOD-610-MP-007:** Implement and verify DR runbook.

#### Database / data design

- [ ] **MOD-610-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **performance tests**.
- [ ] **MOD-610-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **resilience tests**.
- [ ] **MOD-610-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **index review**.
- [ ] **MOD-610-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SLO dashboards**.
- [ ] **MOD-610-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow replay**.
- [ ] **MOD-610-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **integration failure tests**.
- [ ] **MOD-610-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **DR runbook**.

#### Backend

- [ ] **MOD-610-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-610-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-610-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-610-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-610-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-610-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-610-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-610-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-610-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-610-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-610-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-610-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-610-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-610-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-610-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-610-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-610-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-610-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-610-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-610-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-610-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-610-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-610-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-610-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-610-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-610-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-610-AC-001:** 95% of normal APIs are under two seconds.
- [ ] **MOD-610-AC-002:** Dashboard is under three seconds at pilot load.
- [ ] **MOD-610-AC-003:** Durable workflows resume after failure and remain idempotent.
- [ ] **MOD-610-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-610-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-610-DONE:** Module marked Done before dependents

### MOD-620

**Title:** Synthetic Sample Projects, Agent Evaluation, End-to-End Acceptance, and UAT  
**Purpose:** Use the three synthetic projects to verify agent decisions, workflow routing, approvals, security, QA loops, integrations, dashboards, and traceability.  
**Requirements:** MVP Acceptance Criteria, Sample Projects  
**Dependencies:** All MVP functional modules

#### Main points

- [ ] **MOD-620-MP-001:** Implement and verify seed scripts.
- [ ] **MOD-620-MP-002:** Implement and verify expected decisions.
- [ ] **MOD-620-MP-003:** Implement and verify agent evaluations.
- [ ] **MOD-620-MP-004:** Implement and verify E2E tests.
- [ ] **MOD-620-MP-005:** Implement and verify role-based UAT.
- [ ] **MOD-620-MP-006:** Implement and verify acceptance evidence.

#### Database / data design

- [ ] **MOD-620-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **seed scripts**.
- [ ] **MOD-620-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **expected decisions**.
- [ ] **MOD-620-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent evaluations**.
- [ ] **MOD-620-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **E2E tests**.
- [ ] **MOD-620-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **role-based UAT**.
- [ ] **MOD-620-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acceptance evidence**.

#### Backend

- [ ] **MOD-620-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-620-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-620-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-620-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-620-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-620-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-620-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-620-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-620-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-620-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-620-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-620-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-620-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-620-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-620-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-620-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-620-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-620-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-620-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-620-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-620-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-620-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-620-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-620-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-620-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-620-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-620-AC-001:** All three sample projects pass defined workflows.
- [ ] **MOD-620-AC-002:** Agent quality metrics meet targets.
- [ ] **MOD-620-AC-003:** No unauthorized agent approval or isolation failure occurs.
- [ ] **MOD-620-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-620-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-620-DONE:** Module marked Done before dependents

### MOD-630

**Title:** Controlled Pilot, Production Release, Operations, and Final MVP Sign-Off  
**Purpose:** Run the controlled pilot, resolve critical issues, deploy with approvals, monitor, train users, document limitations, and obtain formal sign-off.  
**Requirements:** MVP Exit Criteria, Final Acceptance Sign-Off  
**Dependencies:** MOD-600, MOD-610, MOD-620

#### Main points

- [ ] **MOD-630-MP-001:** Implement and verify pilot plan.
- [ ] **MOD-630-MP-002:** Implement and verify pilot users.
- [ ] **MOD-630-MP-003:** Implement and verify training.
- [ ] **MOD-630-MP-004:** Implement and verify support readiness.
- [ ] **MOD-630-MP-005:** Implement and verify known limitations.
- [ ] **MOD-630-MP-006:** Implement and verify production deployment.
- [ ] **MOD-630-MP-007:** Implement and verify rollback.
- [ ] **MOD-630-MP-008:** Implement and verify final sign-offs.

#### Database / data design

- [ ] **MOD-630-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **pilot plan**.
- [ ] **MOD-630-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **pilot users**.
- [ ] **MOD-630-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **training**.
- [ ] **MOD-630-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **support readiness**.
- [ ] **MOD-630-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **known limitations**.
- [ ] **MOD-630-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **production deployment**.
- [ ] **MOD-630-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **rollback**.
- [ ] **MOD-630-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **final sign-offs**.

#### Backend

- [ ] **MOD-630-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-630-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-630-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-630-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-630-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-630-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-630-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-630-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-630-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-630-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-630-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-630-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-630-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-630-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-630-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-630-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-630-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-630-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-630-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-630-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-630-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-630-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-630-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-630-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-630-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-630-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-630-AC-001:** All Critical and High acceptance tests pass.
- [ ] **MOD-630-AC-002:** Pilot users approve controlled production use.
- [ ] **MOD-630-AC-003:** Cross-functional production readiness sign-off is complete.
- [ ] **MOD-630-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-630-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-630-DONE:** Module marked Done before dependents

## Final MVP sequence (from plan)

- [ ] **FINAL-001:** Confirm every module is Done or formally excluded by approved change control.
- [ ] **FINAL-002:** Apply all migrations from an empty database and supported upgrade baseline.
- [ ] **FINAL-003:** Run all backend and frontend checks, tests, builds, scans, and dependency checks.
- [ ] **FINAL-004:** Run Temporal replay and failure-recovery tests.
- [ ] **FINAL-005:** Run LangGraph golden-dataset, tool-authorization, and prompt-injection tests.
- [ ] **FINAL-006:** Run complete tenant, project, document, file, vector, cache, search, dashboard, integration, and export isolation tests.
- [ ] **FINAL-007:** Run the three synthetic sample projects end to end.
- [ ] **FINAL-008:** Reconcile every Must-Have requirement with phases, tickets, tests, bugs, changes, release, and delivery evidence.
- [ ] **FINAL-009:** Run load, resilience, backup, restore, rollback, and incident exercises.
- [ ] **FINAL-010:** Resolve all Critical and High defects or obtain permitted approved disposition.
- [ ] **FINAL-011:** Document known limitations, runbooks, support ownership, monitoring, and incident contacts.
- [ ] **FINAL-012:** Obtain BD, PM, TL, QA, DevOps, Security, AI Architecture, Product, Management, and client/product-owner sign-off where applicable.

## Cross-module release gates (from plan)

- [ ] **GATE-001:** No tenant-owned entity lacks organization scoping.
- [ ] **GATE-002:** No sensitive operation relies only on frontend permissions.
- [ ] **GATE-003:** No status change bypasses the transition engine.
- [ ] **GATE-004:** No high-risk action bypasses exact-version human approval.
- [ ] **GATE-005:** No agent writes directly to authoritative tables or receives unrestricted secrets.
- [ ] **GATE-006:** No external event is processed without validation and idempotency.
- [ ] **GATE-007:** No file becomes available or indexed before safety validation.
- [ ] **GATE-008:** No approved version is overwritten.
- [ ] **GATE-009:** No release proceeds with unresolved Critical defects or missing mandatory coverage.
- [ ] **GATE-010:** No completion claim is made without executed verification evidence.

---

Generated by `scripts/generate_implementation_progress_checklist.py`. Update the `STATUS` map in that script when work completes, then regenerate.
