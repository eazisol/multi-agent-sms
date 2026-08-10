# MASMS Implementation Progress Checklist

**Source:** `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md`
**Companion evidence gate checklist:** `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md`
**Last updated (workspace):** 2026-08-10
**Rule:** checkmarks reflect repository evidence only; human Done approval is separate.

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
| MOD-000 | Phase 0 - Governance and Foundation | 41 | 25 | 11 | 4 | 1 | 0 | In progress (human approval blocked) |
| MOD-010 | Phase 0 - Governance and Foundation | 47 | 16 | 0 | 30 | 1 | 0 | Blocked |
| MOD-020 | Phase 0 - Governance and Foundation | 49 | 23 | 13 | 4 | 1 | 8 | Blocked |
| MOD-030 | Phase 0 - Governance and Foundation | 43 | 14 | 2 | 26 | 1 | 0 | Blocked |
| MOD-040 | Phase 0 - Governance and Foundation | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-100 | Phase 1 - Identity, Organization, and Configuration | 49 | 0 | 0 | 0 | 0 | 49 | Not started |
| MOD-110 | Phase 1 - Identity, Organization, and Configuration | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-120 | Phase 1 - Identity, Organization, and Configuration | 47 | 0 | 0 | 0 | 0 | 47 | Not started |
| MOD-130 | Phase 1 - Identity, Organization, and Configuration | 47 | 0 | 0 | 0 | 0 | 47 | Not started |
| MOD-140 | Phase 1 - Identity, Organization, and Configuration | 47 | 0 | 0 | 0 | 0 | 47 | Not started |
| MOD-200 | Phase 2 - Client, Query, and Requirement Management | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-210 | Phase 2 - Client, Query, and Requirement Management | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-220 | Phase 2 - Client, Query, and Requirement Management | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-230 | Phase 2 - Client, Query, and Requirement Management | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-240 | Phase 2 - Client, Query, and Requirement Management | 47 | 0 | 0 | 0 | 0 | 47 | Not started |
| MOD-250 | Phase 2 - Client, Query, and Requirement Management | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-260 | Phase 2 - Client, Query, and Requirement Management | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-300 | Phase 3 - Work Management and Agent Orchestration | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-310 | Phase 3 - Work Management and Agent Orchestration | 41 | 0 | 0 | 0 | 0 | 41 | Not started |
| MOD-320 | Phase 3 - Work Management and Agent Orchestration | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-330 | Phase 3 - Work Management and Agent Orchestration | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-340 | Phase 3 - Work Management and Agent Orchestration | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-350 | Phase 3 - Work Management and Agent Orchestration | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-360 | Phase 3 - Work Management and Agent Orchestration | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-370 | Phase 3 - Work Management and Agent Orchestration | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-400 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-410 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-420 | Phase 4 - Quality, Change, Release, and Reporting | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-430 | Phase 4 - Quality, Change, Release, and Reporting | 47 | 0 | 0 | 0 | 0 | 47 | Not started |
| MOD-440 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-450 | Phase 4 - Quality, Change, Release, and Reporting | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-460 | Phase 4 - Quality, Change, Release, and Reporting | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-500 | Phase 5 - MVP Integrations | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-510 | Phase 5 - MVP Integrations | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-520 | Phase 5 - MVP Integrations | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-600 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 47 | 0 | 0 | 0 | 0 | 47 | Not started |
| MOD-610 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 45 | 0 | 0 | 0 | 0 | 45 | Not started |
| MOD-620 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 43 | 0 | 0 | 0 | 0 | 43 | Not started |
| MOD-630 | Phase 6 - Security, Reliability, Pilot, and Production Readiness | 47 | 0 | 0 | 0 | 0 | 47 | Not started |

**Totals:** 1749 tasks — done 78, partial 26, n/a 64, blocked 4, open 1577

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

- [~] **MOD-000-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.  
  - Evidence/note: Baselines list with filter/pagination/empty/loading/error; saved views not yet
- [~] **MOD-000-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.  
  - Evidence/note: Detail summary + audit history tabs; other related tabs deferred
- [x] **MOD-000-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.  
  - Evidence/note: Create/edit/transition forms with role gates and stale-version handling
- [~] **MOD-000-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.  
  - Evidence/note: Skip link, labels, UTC dates, responsive layout; formal a11y audit pending

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

- [~] **MOD-000-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: Org-scoped header principal + human-approve gate; full RBAC deferred MOD-110/120
- [~] **MOD-000-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: App-level org filter + RLS SQL in migration; live GUC/RLS tests not run
- [~] **MOD-000-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.  
  - Evidence/note: Audit payload_redacted + no secrets in .env.example; broader redaction plumbing later
- [~] **MOD-000-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.  
  - Evidence/note: Audit on create/update/transition/approval; not all action types yet

#### Testing / verification

- [x] **MOD-000-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/governance/test_domain.py
- [x] **MOD-000-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: tests/integration/governance/test_governance_api.py
- [~] **MOD-000-QA-003:** Add role-permission negative tests and tenant/project isolation tests.  
  - Evidence/note: Agent approve negative + org list isolation; full RBAC matrix pending
- [-] **MOD-000-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.  
  - Evidence/note: No Temporal/agent/integration capabilities in this module stub
- [~] **MOD-000-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: pytest/ruff/mypy passed; alembic/frontend/security scan not run

#### Documentation

- [~] **MOD-000-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: Module README, data dictionary, governance docs; full audit catalog pending
- [x] **MOD-000-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: README limitations + VERIFICATION.md

#### Acceptance gate

- [~] **MOD-000-AC-001:** One approved source of truth is identified.  
  - Evidence/note: SoT candidates registered; human approval of BL-SRS-001 still PENDING
- [x] **MOD-000-AC-002:** Material changes require a new version and human approval.  
  - Evidence/note: Documented and enforced for approved records
- [x] **MOD-000-AC-003:** Every implementation task maps to a module and requirement ID.  
  - Evidence/note: REQUIREMENT_MODULE_MAP.md published
- [x] **MOD-000-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High defects filed against module
- [!] **MOD-000-AC-901:** The responsible human owner reviews and approves the completion evidence.  
  - Evidence/note: Requires named human owner approval

#### Module completion

- [!] **MOD-000-DONE:** Module marked Done before dependents  
  - Evidence/note: Not Done — AC-901 human approval pending; FE deferred

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
- [!] **MOD-010-AC-901:** The responsible human owner reviews and approves the completion evidence.  
  - Evidence/note: Human owner approval required

#### Module completion

- [ ] **MOD-010-DONE:** Module marked Done before dependents

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

- [~] **MOD-020-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.  
  - Evidence/note: kernel + governance uses UoW/outbox/helpers
- [~] **MOD-020-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.  
  - Evidence/note: concurrency+approval rules via helpers; full authz later
- [~] **MOD-020-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.  
  - Evidence/note: outbox enqueue on baseline create; publisher runtime pending
- [x] **MOD-020-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.  
  - Evidence/note: structured errors via kernel + FastAPI handler

#### API

- [ ] **MOD-020-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [~] **MOD-020-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.  
  - Evidence/note: problem+json + paging/concurrency shared; full OpenAPI polish pending
- [~] **MOD-020-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.  
  - Evidence/note: ProblemDetails schema examples updated

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

- [ ] **MOD-020-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [~] **MOD-020-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.  
  - Evidence/note: boundary documented; Temporal/LangGraph not wired yet
- [~] **MOD-020-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.  
  - Evidence/note: outbox table+enqueue; consumer/publisher runtime pending
- [ ] **MOD-020-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-020-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [~] **MOD-020-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.  
  - Evidence/note: outbox RLS + tenant context shape
- [ ] **MOD-020-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-020-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [x] **MOD-020-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.  
  - Evidence/note: tests/unit/kernel
- [~] **MOD-020-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.  
  - Evidence/note: governance API still green with outbox/problem+json
- [ ] **MOD-020-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-020-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [x] **MOD-020-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.  
  - Evidence/note: ruff/mypy/pytest + alembic upgrade head

#### Documentation

- [~] **MOD-020-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.  
  - Evidence/note: docs/modules/MOD-020/README.md
- [x] **MOD-020-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.  
  - Evidence/note: DATA_CONVENTIONS + VERIFICATION

#### Acceptance gate

- [~] **MOD-020-AC-001:** All modules use the same actor and tenant context.  
  - Evidence/note: RequestContext in kernel; governance wired
- [~] **MOD-020-AC-002:** Agents and workflows cannot bypass application services.  
  - Evidence/note: UoW/API boundary documented; not yet enforced platform-wide
- [~] **MOD-020-AC-003:** API contracts are consistent and documented.  
  - Evidence/note: problem+json + shared PageMeta
- [x] **MOD-020-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High kernel defects filed
- [!] **MOD-020-AC-901:** The responsible human owner reviews and approves the completion evidence.  
  - Evidence/note: Human owner approval required

#### Module completion

- [ ] **MOD-020-DONE:** Module marked Done before dependents

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

- [~] **MOD-030-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.  
  - Evidence/note: GitHub Environment + prod gate; Auth0 later
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

- [~] **MOD-030-AC-001:** Environment credentials are isolated.  
  - Evidence/note: Matrix + secret backend rules; live Secrets Manager not wired
- [x] **MOD-030-AC-002:** Production release requires human authorization.  
  - Evidence/note: Production workflow requires confirm+approver+reason+sha
- [x] **MOD-030-AC-003:** Artifacts are reproducible and traceable.  
  - Evidence/note: CI build-identity artifact keyed by git sha
- [x] **MOD-030-AC-900:** All Critical and High defects for this module are resolved.  
  - Evidence/note: No Critical/High MOD-030 defects filed
- [!] **MOD-030-AC-901:** The responsible human owner reviews and approves the completion evidence.  
  - Evidence/note: Human owner approval required

#### Module completion

- [ ] **MOD-030-DONE:** Module marked Done before dependents

### MOD-040

**Title:** Observability, Audit Foundation, and Operational Health  
**Purpose:** Implement structured logging, tracing, metrics, append-only audit, activity events, correlation IDs, and operational alerts.  
**Requirements:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-020, MOD-030

#### Main points

- [ ] **MOD-040-MP-001:** Implement and verify audit logs.
- [ ] **MOD-040-MP-002:** Implement and verify activity events.
- [ ] **MOD-040-MP-003:** Implement and verify status history.
- [ ] **MOD-040-MP-004:** Implement and verify agent runs.
- [ ] **MOD-040-MP-005:** Implement and verify integration events.
- [ ] **MOD-040-MP-006:** Implement and verify OpenTelemetry.
- [ ] **MOD-040-MP-007:** Implement and verify health checks.

#### Database / data design

- [ ] **MOD-040-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **audit logs**.
- [ ] **MOD-040-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **activity events**.
- [ ] **MOD-040-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status history**.
- [ ] **MOD-040-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent runs**.
- [ ] **MOD-040-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **integration events**.
- [ ] **MOD-040-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **OpenTelemetry**.
- [ ] **MOD-040-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **health checks**.

#### Backend

- [ ] **MOD-040-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-040-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-040-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-040-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-040-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-040-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-040-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-040-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-040-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-040-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-040-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-040-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-040-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-040-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-040-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-040-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-040-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-040-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-040-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-040-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-040-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-040-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-040-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-040-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-040-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-040-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-040-AC-001:** Every controlled action is attributable to an actor.
- [ ] **MOD-040-AC-002:** Audit records are append-only for operational roles.
- [ ] **MOD-040-AC-003:** Failures are diagnosable without revealing secrets.
- [ ] **MOD-040-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-040-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-040-DONE:** Module marked Done before dependents

## Phase 1 - Identity, Organization, and Configuration

### MOD-100

**Title:** Organizations, Actors, Human Users, Agents, Teams, and Departments  
**Purpose:** Implement the organization and shared actor model used for ownership, reporting, escalation, approval, assignment, and audit.  
**Requirements:** MVP-FR-001  
**Dependencies:** MOD-020, MOD-040

#### Main points

- [ ] **MOD-100-MP-001:** Implement and verify organizations.
- [ ] **MOD-100-MP-002:** Implement and verify actors.
- [ ] **MOD-100-MP-003:** Implement and verify human users.
- [ ] **MOD-100-MP-004:** Implement and verify agents.
- [ ] **MOD-100-MP-005:** Implement and verify roles.
- [ ] **MOD-100-MP-006:** Implement and verify departments.
- [ ] **MOD-100-MP-007:** Implement and verify teams.
- [ ] **MOD-100-MP-008:** Implement and verify team members.
- [ ] **MOD-100-MP-009:** Implement and verify reporting lines.

#### Database / data design

- [ ] **MOD-100-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **organizations**.
- [ ] **MOD-100-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actors**.
- [ ] **MOD-100-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **human users**.
- [ ] **MOD-100-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agents**.
- [ ] **MOD-100-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **roles**.
- [ ] **MOD-100-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **departments**.
- [ ] **MOD-100-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **teams**.
- [ ] **MOD-100-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **team members**.
- [ ] **MOD-100-DB-009:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reporting lines**.

#### Backend

- [ ] **MOD-100-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-100-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-100-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-100-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-100-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-100-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-100-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-100-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-100-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-100-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-100-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-100-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-100-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-100-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-100-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-100-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-100-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-100-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-100-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-100-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-100-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-100-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-100-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-100-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-100-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-100-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-100-AC-001:** Every action and owner resolves to one actor.
- [ ] **MOD-100-AC-002:** Every operational agent has an active human supervisor.
- [ ] **MOD-100-AC-003:** Agent and human identities are separate.
- [ ] **MOD-100-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-100-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-100-DONE:** Module marked Done before dependents

### MOD-110

**Title:** Authentication, Sessions, MFA, and Account Security  
**Purpose:** Authenticate humans and machine identities, support MFA and step-up authentication, invitations, session revocation, and service authentication.  
**Requirements:** MVP-FR-001, MVP-NFR-001  
**Dependencies:** MOD-100, MOD-030

#### Main points

- [ ] **MOD-110-MP-001:** Implement and verify identity provider.
- [ ] **MOD-110-MP-002:** Implement and verify token validation.
- [ ] **MOD-110-MP-003:** Implement and verify sessions.
- [ ] **MOD-110-MP-004:** Implement and verify MFA.
- [ ] **MOD-110-MP-005:** Implement and verify step-up authentication.
- [ ] **MOD-110-MP-006:** Implement and verify client invitations.
- [ ] **MOD-110-MP-007:** Implement and verify service identities.

#### Database / data design

- [ ] **MOD-110-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **identity provider**.
- [ ] **MOD-110-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **token validation**.
- [ ] **MOD-110-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **sessions**.
- [ ] **MOD-110-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **MFA**.
- [ ] **MOD-110-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **step-up authentication**.
- [ ] **MOD-110-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **client invitations**.
- [ ] **MOD-110-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **service identities**.

#### Backend

- [ ] **MOD-110-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-110-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-110-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-110-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-110-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-110-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-110-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-110-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-110-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-110-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-110-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-110-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-110-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-110-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-110-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-110-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-110-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-110-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-110-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-110-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-110-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-110-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-110-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-110-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-110-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-110-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-110-AC-001:** All human and machine actions use authenticated actor identities.
- [ ] **MOD-110-AC-002:** Privileged actions require appropriate assurance.
- [ ] **MOD-110-AC-003:** Sessions can be revoked immediately.
- [ ] **MOD-110-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-110-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-110-DONE:** Module marked Done before dependents

### MOD-120

**Title:** RBAC, Attribute-Based Access, Project Membership, and Row-Level Security  
**Purpose:** Enforce deny-by-default authorization across organization, client, project, module, action, environment, classification, and approval authority.  
**Requirements:** MVP-FR-001, MVP-NFR-001, MVP-NFR-002  
**Dependencies:** MOD-100, MOD-110

#### Main points

- [ ] **MOD-120-MP-001:** Implement and verify permissions.
- [ ] **MOD-120-MP-002:** Implement and verify role permissions.
- [ ] **MOD-120-MP-003:** Implement and verify project members.
- [ ] **MOD-120-MP-004:** Implement and verify module access.
- [ ] **MOD-120-MP-005:** Implement and verify document access.
- [ ] **MOD-120-MP-006:** Implement and verify approval authorities.
- [ ] **MOD-120-MP-007:** Implement and verify RLS policies.
- [ ] **MOD-120-MP-008:** Implement and verify access reviews.

#### Database / data design

- [ ] **MOD-120-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **permissions**.
- [ ] **MOD-120-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **role permissions**.
- [ ] **MOD-120-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project members**.
- [ ] **MOD-120-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **module access**.
- [ ] **MOD-120-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document access**.
- [ ] **MOD-120-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval authorities**.
- [ ] **MOD-120-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **RLS policies**.
- [ ] **MOD-120-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **access reviews**.

#### Backend

- [ ] **MOD-120-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-120-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-120-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-120-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-120-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-120-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-120-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-120-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-120-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-120-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-120-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-120-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-120-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-120-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-120-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-120-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-120-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-120-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-120-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-120-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-120-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-120-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-120-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-120-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-120-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-120-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-120-AC-001:** No cross-client access exists through API, database, files, cache, vectors, search, or exports.
- [ ] **MOD-120-AC-002:** Project access requires valid membership or explicit authority.
- [ ] **MOD-120-AC-003:** Frontend visibility never replaces backend authorization.
- [ ] **MOD-120-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-120-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-120-DONE:** Module marked Done before dependents

### MOD-130

**Title:** Skills, Availability, Capacity, Working Hours, and Business Calendars  
**Purpose:** Store skill, proficiency, availability, capacity, leave, time zone, business hours, holidays, and on-call data for assignments and SLA calculations.  
**Requirements:** MVP-FR-005  
**Dependencies:** MOD-100, MOD-120

#### Main points

- [ ] **MOD-130-MP-001:** Implement and verify skills.
- [ ] **MOD-130-MP-002:** Implement and verify actor skills.
- [ ] **MOD-130-MP-003:** Implement and verify availability.
- [ ] **MOD-130-MP-004:** Implement and verify capacity allocations.
- [ ] **MOD-130-MP-005:** Implement and verify business calendars.
- [ ] **MOD-130-MP-006:** Implement and verify holidays.
- [ ] **MOD-130-MP-007:** Implement and verify leave periods.
- [ ] **MOD-130-MP-008:** Implement and verify on-call schedules.

#### Database / data design

- [ ] **MOD-130-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **skills**.
- [ ] **MOD-130-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actor skills**.
- [ ] **MOD-130-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **availability**.
- [ ] **MOD-130-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **capacity allocations**.
- [ ] **MOD-130-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business calendars**.
- [ ] **MOD-130-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **holidays**.
- [ ] **MOD-130-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **leave periods**.
- [ ] **MOD-130-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **on-call schedules**.

#### Backend

- [ ] **MOD-130-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-130-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-130-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-130-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-130-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-130-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-130-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-130-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-130-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-130-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-130-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-130-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-130-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-130-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-130-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-130-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-130-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-130-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-130-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-130-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-130-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-130-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-130-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-130-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-130-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-130-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-130-AC-001:** Assignments can evaluate skill, access, capacity, calendar, and deadline.
- [ ] **MOD-130-AC-002:** SLA calculations respect business calendars and time zones.
- [ ] **MOD-130-AC-003:** Unnecessary personal data is excluded.
- [ ] **MOD-130-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-130-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-130-DONE:** Module marked Done before dependents

### MOD-140

**Title:** Configuration Administration and Versioned Operational Rules  
**Purpose:** Allow approved configuration of statuses, transitions, SLAs, reminders, escalations, approvals, templates, and agent limits without code deployment.  
**Requirements:** MVP-FR-016, MVP-NFR-010  
**Dependencies:** MOD-000, MOD-120, MOD-130

#### Main points

- [ ] **MOD-140-MP-001:** Implement and verify workflow definitions.
- [ ] **MOD-140-MP-002:** Implement and verify status definitions.
- [ ] **MOD-140-MP-003:** Implement and verify transition rules.
- [ ] **MOD-140-MP-004:** Implement and verify follow-up rules.
- [ ] **MOD-140-MP-005:** Implement and verify reminder rules.
- [ ] **MOD-140-MP-006:** Implement and verify escalation rules.
- [ ] **MOD-140-MP-007:** Implement and verify approval workflows.
- [ ] **MOD-140-MP-008:** Implement and verify configuration versions.

#### Database / data design

- [ ] **MOD-140-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow definitions**.
- [ ] **MOD-140-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status definitions**.
- [ ] **MOD-140-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **transition rules**.
- [ ] **MOD-140-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **follow-up rules**.
- [ ] **MOD-140-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reminder rules**.
- [ ] **MOD-140-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **escalation rules**.
- [ ] **MOD-140-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval workflows**.
- [ ] **MOD-140-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **configuration versions**.

#### Backend

- [ ] **MOD-140-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-140-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-140-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-140-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-140-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-140-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-140-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-140-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-140-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-140-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-140-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-140-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-140-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-140-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-140-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-140-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-140-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-140-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-140-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-140-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-140-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-140-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-140-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-140-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-140-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-140-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-140-AC-001:** Only approved effective configuration controls live execution.
- [ ] **MOD-140-AC-002:** Configuration changes require validation, audit, and rollback support.
- [ ] **MOD-140-AC-003:** Draft configuration cannot affect live workflows.
- [ ] **MOD-140-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-140-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-140-DONE:** Module marked Done before dependents

## Phase 2 - Client, Query, and Requirement Management

### MOD-200

**Title:** Client and Contact Management  
**Purpose:** Manage client organizations, contacts, authority, preferences, ownership, duplicates, related projects, documents, messages, and activity.  
**Requirements:** MVP-FR-002  
**Dependencies:** MOD-120, MOD-040

#### Main points

- [ ] **MOD-200-MP-001:** Implement and verify clients.
- [ ] **MOD-200-MP-002:** Implement and verify contacts.
- [ ] **MOD-200-MP-003:** Implement and verify project contacts.
- [ ] **MOD-200-MP-004:** Implement and verify communication preferences.
- [ ] **MOD-200-MP-005:** Implement and verify duplicate suggestions.
- [ ] **MOD-200-MP-006:** Implement and verify merge history.

#### Database / data design

- [ ] **MOD-200-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **clients**.
- [ ] **MOD-200-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **contacts**.
- [ ] **MOD-200-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project contacts**.
- [ ] **MOD-200-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **communication preferences**.
- [ ] **MOD-200-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **duplicate suggestions**.
- [ ] **MOD-200-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **merge history**.

#### Backend

- [ ] **MOD-200-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-200-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-200-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-200-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-200-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-200-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-200-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-200-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-200-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-200-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-200-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-200-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-200-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-200-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-200-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-200-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-200-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-200-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-200-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-200-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-200-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-200-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-200-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-200-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-200-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-200-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-200-AC-001:** Clients may have multiple contacts with explicit authority.
- [ ] **MOD-200-AC-002:** Duplicate handling preserves history.
- [ ] **MOD-200-AC-003:** Client records are isolated and auditable.
- [ ] **MOD-200-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-200-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-200-DONE:** Module marked Done before dependents

### MOD-210

**Title:** Client Queries, Qualification, and Opportunities  
**Purpose:** Capture, classify, assign, qualify, reject, convert, and trace inquiries while preserving original communication and qualification evidence.  
**Requirements:** MVP-FR-002, MVP-FR-003  
**Dependencies:** MOD-200, MOD-140

#### Main points

- [ ] **MOD-210-MP-001:** Implement and verify queries.
- [ ] **MOD-210-MP-002:** Implement and verify opportunities.
- [ ] **MOD-210-MP-003:** Implement and verify qualification answers.
- [ ] **MOD-210-MP-004:** Implement and verify query sources.
- [ ] **MOD-210-MP-005:** Implement and verify query status history.
- [ ] **MOD-210-MP-006:** Implement and verify first response SLA.

#### Database / data design

- [ ] **MOD-210-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **queries**.
- [ ] **MOD-210-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **opportunities**.
- [ ] **MOD-210-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **qualification answers**.
- [ ] **MOD-210-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **query sources**.
- [ ] **MOD-210-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **query status history**.
- [ ] **MOD-210-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **first response SLA**.

#### Backend

- [ ] **MOD-210-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-210-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-210-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-210-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-210-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-210-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-210-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-210-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-210-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-210-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-210-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-210-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-210-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-210-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-210-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-210-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-210-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-210-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-210-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-210-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-210-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-210-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-210-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-210-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-210-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-210-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-210-AC-001:** Each valid inquiry creates one traceable query.
- [ ] **MOD-210-AC-002:** Qualification is reviewable and explainable.
- [ ] **MOD-210-AC-003:** Conversion preserves communication, documents, follow-ups, and decisions.
- [ ] **MOD-210-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-210-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-210-DONE:** Module marked Done before dependents

### MOD-220

**Title:** Conversations, Messages, Attachments, and Communication History  
**Purpose:** Store immutable internal and external communication threads, recipients, delivery status, revisions, attachments, and related business records.  
**Requirements:** MVP-FR-011, MVP-FR-014  
**Dependencies:** MOD-200, MOD-040, MOD-120

#### Main points

- [ ] **MOD-220-MP-001:** Implement and verify conversations.
- [ ] **MOD-220-MP-002:** Implement and verify messages.
- [ ] **MOD-220-MP-003:** Implement and verify message revisions.
- [ ] **MOD-220-MP-004:** Implement and verify recipients.
- [ ] **MOD-220-MP-005:** Implement and verify delivery receipts.
- [ ] **MOD-220-MP-006:** Implement and verify attachment links.

#### Database / data design

- [ ] **MOD-220-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **conversations**.
- [ ] **MOD-220-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **messages**.
- [ ] **MOD-220-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **message revisions**.
- [ ] **MOD-220-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **recipients**.
- [ ] **MOD-220-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **delivery receipts**.
- [ ] **MOD-220-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachment links**.

#### Backend

- [ ] **MOD-220-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-220-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-220-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-220-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-220-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-220-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-220-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-220-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-220-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-220-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-220-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-220-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-220-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-220-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-220-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-220-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-220-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-220-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-220-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-220-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-220-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-220-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-220-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-220-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-220-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-220-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-220-AC-001:** Material communication is linked to the correct entity.
- [ ] **MOD-220-AC-002:** Sensitive messages follow approval and recipient rules.
- [ ] **MOD-220-AC-003:** Sent-message history is immutable.
- [ ] **MOD-220-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-220-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-220-DONE:** Module marked Done before dependents

### MOD-230

**Title:** Requirement Gathering, Completeness Analysis, Clarifications, and Requirement Brief  
**Purpose:** Run approved questionnaires, store structured answers, detect gaps and conflicts, create bidirectional clarifications, and produce a versioned requirement brief.  
**Requirements:** MVP-FR-003  
**Dependencies:** MOD-210, MOD-220, MOD-250, MOD-330

#### Main points

- [ ] **MOD-230-MP-001:** Implement and verify questionnaires.
- [ ] **MOD-230-MP-002:** Implement and verify questionnaire versions.
- [ ] **MOD-230-MP-003:** Implement and verify answers.
- [ ] **MOD-230-MP-004:** Implement and verify requirement briefs.
- [ ] **MOD-230-MP-005:** Implement and verify clarification requests.
- [ ] **MOD-230-MP-006:** Implement and verify completeness scoring.

#### Database / data design

- [ ] **MOD-230-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **questionnaires**.
- [ ] **MOD-230-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **questionnaire versions**.
- [ ] **MOD-230-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **answers**.
- [ ] **MOD-230-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement briefs**.
- [ ] **MOD-230-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **clarification requests**.
- [ ] **MOD-230-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **completeness scoring**.

#### Backend

- [ ] **MOD-230-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-230-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-230-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-230-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-230-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-230-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-230-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-230-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-230-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-230-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-230-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-230-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-230-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-230-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-230-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-230-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-230-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-230-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-230-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-230-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-230-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-230-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-230-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-230-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-230-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-230-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-230-AC-001:** At least 95% of mandatory fields are answered or explicitly unavailable.
- [ ] **MOD-230-AC-002:** Unanswered mandatory items have an owner or follow-up.
- [ ] **MOD-230-AC-003:** The brief is versioned and human-approved.
- [ ] **MOD-230-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-230-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-230-DONE:** Module marked Done before dependents

### MOD-240

**Title:** Projects, Requirements, Requirement Versions, and SRS Management  
**Purpose:** Create project records and authoritative, versioned requirements and SRS baselines with unique IDs, validations, acceptance criteria, and approval history.  
**Requirements:** MVP-FR-004, MVP-FR-013  
**Dependencies:** MOD-230, MOD-250, MOD-330

#### Main points

- [ ] **MOD-240-MP-001:** Implement and verify projects.
- [ ] **MOD-240-MP-002:** Implement and verify requirements.
- [ ] **MOD-240-MP-003:** Implement and verify requirement versions.
- [ ] **MOD-240-MP-004:** Implement and verify business rules.
- [ ] **MOD-240-MP-005:** Implement and verify acceptance criteria.
- [ ] **MOD-240-MP-006:** Implement and verify assumptions.
- [ ] **MOD-240-MP-007:** Implement and verify constraints.
- [ ] **MOD-240-MP-008:** Implement and verify SRS baselines.

#### Database / data design

- [ ] **MOD-240-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **projects**.
- [ ] **MOD-240-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirements**.
- [ ] **MOD-240-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement versions**.
- [ ] **MOD-240-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business rules**.
- [ ] **MOD-240-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acceptance criteria**.
- [ ] **MOD-240-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assumptions**.
- [ ] **MOD-240-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **constraints**.
- [ ] **MOD-240-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SRS baselines**.

#### Backend

- [ ] **MOD-240-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-240-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-240-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-240-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-240-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-240-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-240-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-240-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-240-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-240-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-240-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-240-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-240-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-240-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-240-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-240-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-240-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-240-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-240-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-240-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-240-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-240-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-240-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-240-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-240-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-240-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-240-AC-001:** Every approved requirement has a unique ID and acceptance criteria.
- [ ] **MOD-240-AC-002:** SRS cannot become authoritative without human approval.
- [ ] **MOD-240-AC-003:** Material changes create new versions and change control.
- [ ] **MOD-240-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-240-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-240-DONE:** Module marked Done before dependents

### MOD-250

**Title:** Documents, Standard Templates, Versioning, and Secure File Storage  
**Purpose:** Manage approved templates, document versions, classifications, storage, scanning, downloads, approvals, and AI retrieval permission.  
**Requirements:** MVP-FR-010  
**Dependencies:** MOD-030, MOD-120, MOD-040

#### Main points

- [ ] **MOD-250-MP-001:** Implement and verify documents.
- [ ] **MOD-250-MP-002:** Implement and verify document versions.
- [ ] **MOD-250-MP-003:** Implement and verify templates.
- [ ] **MOD-250-MP-004:** Implement and verify template versions.
- [ ] **MOD-250-MP-005:** Implement and verify attachments.
- [ ] **MOD-250-MP-006:** Implement and verify document permissions.
- [ ] **MOD-250-MP-007:** Implement and verify scan results.

#### Database / data design

- [ ] **MOD-250-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **documents**.
- [ ] **MOD-250-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document versions**.
- [ ] **MOD-250-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **templates**.
- [ ] **MOD-250-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **template versions**.
- [ ] **MOD-250-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachments**.
- [ ] **MOD-250-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document permissions**.
- [ ] **MOD-250-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **scan results**.

#### Backend

- [ ] **MOD-250-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-250-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-250-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-250-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-250-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-250-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-250-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-250-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-250-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-250-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-250-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-250-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-250-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-250-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-250-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-250-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-250-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-250-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-250-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-250-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-250-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-250-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-250-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-250-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-250-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-250-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-250-AC-001:** Authoritative documents have version, owner, status, and effective date.
- [ ] **MOD-250-AC-002:** Unsafe files never become available or indexed.
- [ ] **MOD-250-AC-003:** Access applies to files, previews, extracted text, and embeddings.
- [ ] **MOD-250-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-250-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-250-DONE:** Module marked Done before dependents

### MOD-260

**Title:** Project Phases, Milestones, Roadmaps, Dependencies, and Baselines  
**Purpose:** Convert approved requirements into phases, milestones, deliverables, dependencies, resource needs, baselines, forecasts, and completion gates.  
**Requirements:** MVP-FR-004  
**Dependencies:** MOD-240, MOD-130, MOD-330

#### Main points

- [ ] **MOD-260-MP-001:** Implement and verify phases.
- [ ] **MOD-260-MP-002:** Implement and verify milestones.
- [ ] **MOD-260-MP-003:** Implement and verify deliverables.
- [ ] **MOD-260-MP-004:** Implement and verify phase dependencies.
- [ ] **MOD-260-MP-005:** Implement and verify project baselines.
- [ ] **MOD-260-MP-006:** Implement and verify forecasts.

#### Database / data design

- [ ] **MOD-260-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **phases**.
- [ ] **MOD-260-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **milestones**.
- [ ] **MOD-260-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deliverables**.
- [ ] **MOD-260-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **phase dependencies**.
- [ ] **MOD-260-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project baselines**.
- [ ] **MOD-260-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **forecasts**.

#### Backend

- [ ] **MOD-260-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-260-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-260-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-260-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-260-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-260-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-260-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-260-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-260-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-260-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-260-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-260-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-260-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-260-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-260-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-260-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-260-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-260-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-260-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-260-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-260-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-260-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-260-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-260-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-260-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-260-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-260-AC-001:** Every approved requirement maps to a phase.
- [ ] **MOD-260-AC-002:** Every milestone has owner, date, status, and approval rules.
- [ ] **MOD-260-AC-003:** Multi-phase projects support independent phase completion.
- [ ] **MOD-260-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-260-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-260-DONE:** Module marked Done before dependents

## Phase 3 - Work Management and Agent Orchestration

### MOD-300

**Title:** Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion  
**Purpose:** Create traceable work with acceptance criteria, estimates, dependencies, Definition of Ready, Definition of Done, evidence, and controlled lifecycle.  
**Requirements:** MVP-FR-005, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-320

#### Main points

- [ ] **MOD-300-MP-001:** Implement and verify tickets.
- [ ] **MOD-300-MP-002:** Implement and verify subtasks.
- [ ] **MOD-300-MP-003:** Implement and verify ticket dependencies.
- [ ] **MOD-300-MP-004:** Implement and verify requirement links.
- [ ] **MOD-300-MP-005:** Implement and verify ticket evidence.
- [ ] **MOD-300-MP-006:** Implement and verify readiness checks.
- [ ] **MOD-300-MP-007:** Implement and verify done checks.

#### Database / data design

- [ ] **MOD-300-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tickets**.
- [ ] **MOD-300-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **subtasks**.
- [ ] **MOD-300-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket dependencies**.
- [ ] **MOD-300-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement links**.
- [ ] **MOD-300-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket evidence**.
- [ ] **MOD-300-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **readiness checks**.
- [ ] **MOD-300-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **done checks**.

#### Backend

- [ ] **MOD-300-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-300-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-300-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-300-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-300-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-300-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-300-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-300-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-300-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-300-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-300-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-300-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-300-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-300-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-300-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-300-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-300-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-300-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-300-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-300-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-300-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-300-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-300-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-300-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-300-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-300-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-300-AC-001:** No ticket becomes Ready without required information.
- [ ] **MOD-300-AC-002:** Tickets link to project, phase, owner or queue, and requirement.
- [ ] **MOD-300-AC-003:** Done tickets reopen only with authority and evidence.
- [ ] **MOD-300-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-300-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-300-DONE:** Module marked Done before dependents

### MOD-310

**Title:** Skill- and Capacity-Based Assignment and Ownership History  
**Purpose:** Recommend and approve assignments using role, skill, proficiency, project access, capacity, working hours, dependencies, and workload.  
**Requirements:** MVP-FR-005  
**Dependencies:** MOD-130, MOD-300, MOD-120

#### Main points

- [ ] **MOD-310-MP-001:** Implement and verify assignments.
- [ ] **MOD-310-MP-002:** Implement and verify assignment recommendations.
- [ ] **MOD-310-MP-003:** Implement and verify allocation history.
- [ ] **MOD-310-MP-004:** Implement and verify acknowledgments.
- [ ] **MOD-310-MP-005:** Implement and verify reassignment history.

#### Database / data design

- [ ] **MOD-310-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assignments**.
- [ ] **MOD-310-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assignment recommendations**.
- [ ] **MOD-310-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **allocation history**.
- [ ] **MOD-310-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acknowledgments**.
- [ ] **MOD-310-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reassignment history**.

#### Backend

- [ ] **MOD-310-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-310-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-310-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-310-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-310-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-310-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-310-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-310-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-310-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-310-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-310-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-310-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-310-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-310-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-310-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-310-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-310-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-310-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-310-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-310-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-310-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-310-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-310-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-310-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-310-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-310-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-310-AC-001:** No assignment is made to an unauthorized or unavailable actor.
- [ ] **MOD-310-AC-002:** Overrides require a reason.
- [ ] **MOD-310-AC-003:** Assignment history is immutable.
- [ ] **MOD-310-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-310-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-310-DONE:** Module marked Done before dependents

### MOD-320

**Title:** Configurable Status and Transition Engine  
**Purpose:** Execute configurable status transitions with permissions, conditions, required fields, evidence, approval, history, hold, reopen, and terminal-state rules.  
**Requirements:** MVP-FR-016  
**Dependencies:** MOD-140, MOD-040

#### Main points

- [ ] **MOD-320-MP-001:** Implement and verify workflow resolver.
- [ ] **MOD-320-MP-002:** Implement and verify transition evaluator.
- [ ] **MOD-320-MP-003:** Implement and verify status history.
- [ ] **MOD-320-MP-004:** Implement and verify hold records.
- [ ] **MOD-320-MP-005:** Implement and verify reopen records.
- [ ] **MOD-320-MP-006:** Implement and verify available next actions.

#### Database / data design

- [ ] **MOD-320-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow resolver**.
- [ ] **MOD-320-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **transition evaluator**.
- [ ] **MOD-320-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status history**.
- [ ] **MOD-320-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **hold records**.
- [ ] **MOD-320-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reopen records**.
- [ ] **MOD-320-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **available next actions**.

#### Backend

- [ ] **MOD-320-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-320-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-320-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-320-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-320-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-320-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-320-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-320-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-320-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-320-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-320-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-320-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-320-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-320-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-320-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-320-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-320-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-320-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-320-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-320-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-320-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-320-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-320-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-320-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-320-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-320-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-320-AC-001:** No business status is hard-coded as a database enum.
- [ ] **MOD-320-AC-002:** Every transition creates history and audit.
- [ ] **MOD-320-AC-003:** Agents cannot skip required approval gates.
- [ ] **MOD-320-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-320-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-320-DONE:** Module marked Done before dependents

### MOD-330

**Title:** Human Approval Gates, Delegation, Rejection, and Override  
**Purpose:** Enforce exact-version human approval for scope, quotation, timeline, SRS, allocation exceptions, architecture, changes, production, delivery, and closure.  
**Requirements:** MVP-FR-008  
**Dependencies:** MOD-120, MOD-140, MOD-320

#### Main points

- [ ] **MOD-330-MP-001:** Implement and verify approvals.
- [ ] **MOD-330-MP-002:** Implement and verify approval workflows.
- [ ] **MOD-330-MP-003:** Implement and verify approval steps.
- [ ] **MOD-330-MP-004:** Implement and verify approval decisions.
- [ ] **MOD-330-MP-005:** Implement and verify delegations.
- [ ] **MOD-330-MP-006:** Implement and verify approval evidence.
- [ ] **MOD-330-MP-007:** Implement and verify human overrides.

#### Database / data design

- [ ] **MOD-330-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approvals**.
- [ ] **MOD-330-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval workflows**.
- [ ] **MOD-330-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval steps**.
- [ ] **MOD-330-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval decisions**.
- [ ] **MOD-330-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **delegations**.
- [ ] **MOD-330-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval evidence**.
- [ ] **MOD-330-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **human overrides**.

#### Backend

- [ ] **MOD-330-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-330-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-330-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-330-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-330-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-330-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-330-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-330-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-330-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-330-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-330-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-330-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-330-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-330-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-330-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-330-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-330-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-330-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-330-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-330-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-330-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-330-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-330-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-330-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-330-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-330-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-330-AC-001:** Dependent actions remain blocked until approval.
- [ ] **MOD-330-AC-002:** Approvals bind to exact versions.
- [ ] **MOD-330-AC-003:** Agents cannot approve their own recommendations.
- [ ] **MOD-330-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-330-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-330-DONE:** Module marked Done before dependents

### MOD-340

**Title:** Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations  
**Purpose:** Track clarifications, approvals, blockers, assignments, progress requests, client responses, bug fixes, deployments, and completion in both directions.  
**Requirements:** MVP-FR-007  
**Dependencies:** MOD-130, MOD-140, MOD-320, MOD-440

#### Main points

- [ ] **MOD-340-MP-001:** Implement and verify follow-ups.
- [ ] **MOD-340-MP-002:** Implement and verify reminders.
- [ ] **MOD-340-MP-003:** Implement and verify escalations.
- [ ] **MOD-340-MP-004:** Implement and verify parent-child links.
- [ ] **MOD-340-MP-005:** Implement and verify SLA pauses.
- [ ] **MOD-340-MP-006:** Implement and verify business-time deadlines.
- [ ] **MOD-340-MP-007:** Implement and verify closure evidence.

#### Database / data design

- [ ] **MOD-340-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **follow-ups**.
- [ ] **MOD-340-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reminders**.
- [ ] **MOD-340-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **escalations**.
- [ ] **MOD-340-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **parent-child links**.
- [ ] **MOD-340-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SLA pauses**.
- [ ] **MOD-340-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business-time deadlines**.
- [ ] **MOD-340-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **closure evidence**.

#### Backend

- [ ] **MOD-340-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-340-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-340-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-340-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-340-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-340-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-340-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-340-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-340-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-340-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-340-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-340-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-340-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-340-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-340-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-340-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-340-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-340-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-340-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-340-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-340-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-340-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-340-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-340-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-340-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-340-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-340-AC-001:** Every request has owner, deadline, rule version, and closure condition.
- [ ] **MOD-340-AC-002:** Overdue items trigger configured reminders and escalation.
- [ ] **MOD-340-AC-003:** Parent-child chains preserve return routing.
- [ ] **MOD-340-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-340-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-340-DONE:** Module marked Done before dependents

### MOD-350

**Title:** Temporal Orchestrator and Durable Business Workflows  
**Purpose:** Coordinate long-running query, requirement, handover, assignment, blocker, QA, reporting, change, deployment, and closure workflows with durable waits and retries.  
**Requirements:** MVP-FR-006, MVP-FR-007, MVP-NFR-004  
**Dependencies:** MOD-320, MOD-330, MOD-340, MOD-040

#### Main points

- [ ] **MOD-350-MP-001:** Implement and verify workflow instances.
- [ ] **MOD-350-MP-002:** Implement and verify workflow signals.
- [ ] **MOD-350-MP-003:** Implement and verify workflow versions.
- [ ] **MOD-350-MP-004:** Implement and verify workflow failures.
- [ ] **MOD-350-MP-005:** Implement and verify interventions.
- [ ] **MOD-350-MP-006:** Implement and verify 12 approved workflows.

#### Database / data design

- [ ] **MOD-350-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow instances**.
- [ ] **MOD-350-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow signals**.
- [ ] **MOD-350-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow versions**.
- [ ] **MOD-350-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow failures**.
- [ ] **MOD-350-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **interventions**.
- [ ] **MOD-350-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **12 approved workflows**.

#### Backend

- [ ] **MOD-350-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-350-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-350-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-350-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-350-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-350-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-350-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-350-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-350-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-350-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-350-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-350-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-350-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-350-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-350-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-350-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-350-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-350-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-350-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-350-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-350-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-350-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-350-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-350-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-350-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-350-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-350-AC-001:** Workflows survive worker restarts.
- [ ] **MOD-350-AC-002:** Timers, retries, and duplicate signals are idempotent.
- [ ] **MOD-350-AC-003:** Workflow history does not replace PostgreSQL business state.
- [ ] **MOD-350-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-350-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-350-DONE:** Module marked Done before dependents

### MOD-360

**Title:** LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision  
**Purpose:** Implement bounded departmental agents with prompt versions, tool allowlists, minimum context, structured outputs, human review, cost, and evaluation.  
**Requirements:** MVP-FR-006, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-100, MOD-120, MOD-240, MOD-350, MOD-370

#### Main points

- [ ] **MOD-360-MP-001:** Implement and verify agent registry.
- [ ] **MOD-360-MP-002:** Implement and verify agent runs.
- [ ] **MOD-360-MP-003:** Implement and verify prompt versions.
- [ ] **MOD-360-MP-004:** Implement and verify tool policies.
- [ ] **MOD-360-MP-005:** Implement and verify context builder.
- [ ] **MOD-360-MP-006:** Implement and verify agent reviews.
- [ ] **MOD-360-MP-007:** Implement and verify agent evaluations.

#### Database / data design

- [ ] **MOD-360-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent registry**.
- [ ] **MOD-360-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent runs**.
- [ ] **MOD-360-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **prompt versions**.
- [ ] **MOD-360-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tool policies**.
- [ ] **MOD-360-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **context builder**.
- [ ] **MOD-360-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent reviews**.
- [ ] **MOD-360-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent evaluations**.

#### Backend

- [ ] **MOD-360-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-360-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-360-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-360-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-360-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-360-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-360-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-360-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-360-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-360-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-360-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-360-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-360-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-360-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-360-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-360-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-360-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-360-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-360-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-360-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-360-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-360-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-360-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-360-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-360-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-360-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-360-AC-001:** Every run records model, prompt, sources, tools, output, review, and audit.
- [ ] **MOD-360-AC-002:** Agents use business APIs rather than direct database access.
- [ ] **MOD-360-AC-003:** Low-confidence or conflicting output creates human review.
- [ ] **MOD-360-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-360-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-360-DONE:** Module marked Done before dependents

### MOD-370

**Title:** Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation  
**Purpose:** Provide approved, effective, versioned, owned, permission-controlled company and project knowledge with source citations and conflict handling.  
**Requirements:** MVP-FR-010, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-250, MOD-120, MOD-040

#### Main points

- [ ] **MOD-370-MP-001:** Implement and verify knowledge items.
- [ ] **MOD-370-MP-002:** Implement and verify knowledge versions.
- [ ] **MOD-370-MP-003:** Implement and verify chunks.
- [ ] **MOD-370-MP-004:** Implement and verify embeddings.
- [ ] **MOD-370-MP-005:** Implement and verify knowledge permissions.
- [ ] **MOD-370-MP-006:** Implement and verify usage logs.
- [ ] **MOD-370-MP-007:** Implement and verify knowledge conflicts.

#### Database / data design

- [ ] **MOD-370-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge items**.
- [ ] **MOD-370-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge versions**.
- [ ] **MOD-370-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **chunks**.
- [ ] **MOD-370-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **embeddings**.
- [ ] **MOD-370-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge permissions**.
- [ ] **MOD-370-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **usage logs**.
- [ ] **MOD-370-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge conflicts**.

#### Backend

- [ ] **MOD-370-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-370-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-370-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-370-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-370-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-370-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-370-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-370-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-370-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-370-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-370-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-370-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-370-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-370-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-370-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-370-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-370-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-370-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-370-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-370-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-370-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-370-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-370-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-370-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-370-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-370-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-370-AC-001:** Agents cite the source and version used.
- [ ] **MOD-370-AC-002:** Project-approved knowledge outranks generic examples.
- [ ] **MOD-370-AC-003:** Unauthorized, expired, rejected, or superseded content is excluded.
- [ ] **MOD-370-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-370-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-370-DONE:** Module marked Done before dependents

## Phase 4 - Quality, Change, Release, and Reporting

### MOD-400

**Title:** Test Cases, Test Steps, Test Runs, Evidence, and Coverage  
**Purpose:** Create requirement-linked test cases and execution records for functional, negative, boundary, validation, permission, integration, concurrency, regression, browser, and device testing.  
**Requirements:** MVP-FR-009, MVP-FR-013  
**Dependencies:** MOD-240, MOD-300, MOD-360

#### Main points

- [ ] **MOD-400-MP-001:** Implement and verify test cases.
- [ ] **MOD-400-MP-002:** Implement and verify test steps.
- [ ] **MOD-400-MP-003:** Implement and verify test suites.
- [ ] **MOD-400-MP-004:** Implement and verify test plans.
- [ ] **MOD-400-MP-005:** Implement and verify test runs.
- [ ] **MOD-400-MP-006:** Implement and verify test evidence.
- [ ] **MOD-400-MP-007:** Implement and verify coverage links.

#### Database / data design

- [ ] **MOD-400-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test cases**.
- [ ] **MOD-400-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test steps**.
- [ ] **MOD-400-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test suites**.
- [ ] **MOD-400-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test plans**.
- [ ] **MOD-400-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test runs**.
- [ ] **MOD-400-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test evidence**.
- [ ] **MOD-400-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **coverage links**.

#### Backend

- [ ] **MOD-400-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-400-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-400-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-400-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-400-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-400-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-400-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-400-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-400-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-400-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-400-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-400-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-400-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-400-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-400-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-400-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-400-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-400-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-400-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-400-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-400-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-400-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-400-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-400-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-400-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-400-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-400-AC-001:** Every Must-Have requirement has approved test coverage.
- [ ] **MOD-400-AC-002:** Critical permissions have negative tests.
- [ ] **MOD-400-AC-003:** Test evidence is tied to environment and build.
- [ ] **MOD-400-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-400-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-400-DONE:** Module marked Done before dependents

### MOD-410

**Title:** Bug Lifecycle, QA Rejection, Development Reopen, and Retesting  
**Purpose:** Allow QA to reject work, create defects, route fixes, reopen tickets, retest, and prevent release while blocking defects remain.  
**Requirements:** MVP-FR-009  
**Dependencies:** MOD-300, MOD-320, MOD-340, MOD-400

#### Main points

- [ ] **MOD-410-MP-001:** Implement and verify bugs.
- [ ] **MOD-410-MP-002:** Implement and verify bug links.
- [ ] **MOD-410-MP-003:** Implement and verify bug assignments.
- [ ] **MOD-410-MP-004:** Implement and verify fix submissions.
- [ ] **MOD-410-MP-005:** Implement and verify retests.
- [ ] **MOD-410-MP-006:** Implement and verify known issue approvals.
- [ ] **MOD-410-MP-007:** Implement and verify severity SLA.

#### Database / data design

- [ ] **MOD-410-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **bugs**.
- [ ] **MOD-410-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **bug links**.
- [ ] **MOD-410-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **bug assignments**.
- [ ] **MOD-410-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **fix submissions**.
- [ ] **MOD-410-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **retests**.
- [ ] **MOD-410-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **known issue approvals**.
- [ ] **MOD-410-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **severity SLA**.

#### Backend

- [ ] **MOD-410-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-410-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-410-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-410-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-410-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-410-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-410-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-410-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-410-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-410-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-410-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-410-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-410-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-410-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-410-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-410-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-410-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-410-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-410-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-410-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-410-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-410-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-410-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-410-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-410-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-410-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-410-AC-001:** QA can reject and reopen work with evidence.
- [ ] **MOD-410-AC-002:** Blocking defects prevent release.
- [ ] **MOD-410-AC-003:** Bug history links requirement, ticket, test, fix, retest, and release.
- [ ] **MOD-410-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-410-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-410-DONE:** Module marked Done before dependents

### MOD-420

**Title:** Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates  
**Purpose:** Manage project risks and formal changes to approved scope, requirements, design, timeline, cost, resource, security, data, integration, and release plans.  
**Requirements:** MVP-FR-008, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-300, MOD-330, MOD-340

#### Main points

- [ ] **MOD-420-MP-001:** Implement and verify risks.
- [ ] **MOD-420-MP-002:** Implement and verify risk reviews.
- [ ] **MOD-420-MP-003:** Implement and verify change requests.
- [ ] **MOD-420-MP-004:** Implement and verify impact analyses.
- [ ] **MOD-420-MP-005:** Implement and verify change approvals.
- [ ] **MOD-420-MP-006:** Implement and verify baseline updates.

#### Database / data design

- [ ] **MOD-420-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **risks**.
- [ ] **MOD-420-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **risk reviews**.
- [ ] **MOD-420-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **change requests**.
- [ ] **MOD-420-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **impact analyses**.
- [ ] **MOD-420-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **change approvals**.
- [ ] **MOD-420-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **baseline updates**.

#### Backend

- [ ] **MOD-420-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-420-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-420-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-420-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-420-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-420-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-420-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-420-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-420-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-420-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-420-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-420-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-420-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-420-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-420-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-420-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-420-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-420-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-420-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-420-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-420-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-420-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-420-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-420-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-420-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-420-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-420-AC-001:** Out-of-scope work cannot silently enter development.
- [ ] **MOD-420-AC-002:** Approved changes update affected versions and tickets.
- [ ] **MOD-420-AC-003:** Rejected and deferred changes preserve evidence and rationale.
- [ ] **MOD-420-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-420-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-420-DONE:** Module marked Done before dependents

### MOD-430

**Title:** Releases, Deployment Requests, Production Approval, Rollback, and Closure  
**Purpose:** Package release items, enforce quality and human release gates, record deployment, smoke tests, rollback, client delivery, and closure.  
**Requirements:** MVP-FR-008, MVP-FR-009  
**Dependencies:** MOD-330, MOD-400, MOD-410, MOD-420, MOD-350

#### Main points

- [ ] **MOD-430-MP-001:** Implement and verify releases.
- [ ] **MOD-430-MP-002:** Implement and verify release items.
- [ ] **MOD-430-MP-003:** Implement and verify deployments.
- [ ] **MOD-430-MP-004:** Implement and verify deployment checks.
- [ ] **MOD-430-MP-005:** Implement and verify backup confirmations.
- [ ] **MOD-430-MP-006:** Implement and verify migration plans.
- [ ] **MOD-430-MP-007:** Implement and verify rollbacks.
- [ ] **MOD-430-MP-008:** Implement and verify completion reports.

#### Database / data design

- [ ] **MOD-430-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **releases**.
- [ ] **MOD-430-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **release items**.
- [ ] **MOD-430-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deployments**.
- [ ] **MOD-430-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deployment checks**.
- [ ] **MOD-430-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **backup confirmations**.
- [ ] **MOD-430-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **migration plans**.
- [ ] **MOD-430-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **rollbacks**.
- [ ] **MOD-430-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **completion reports**.

#### Backend

- [ ] **MOD-430-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-430-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-430-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-430-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-430-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-430-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-430-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-430-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-430-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-430-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-430-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-430-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-430-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-430-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-430-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-430-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-430-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-430-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-430-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-430-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-430-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-430-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-430-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-430-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-430-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-430-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-430-AC-001:** Production cannot start without evidence and approval.
- [ ] **MOD-430-AC-002:** Releases trace to requirements, tickets, tests, bugs, changes, and documents.
- [ ] **MOD-430-AC-003:** Closure requires client and internal acceptance.
- [ ] **MOD-430-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-430-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-430-DONE:** Module marked Done before dependents

### MOD-440

**Title:** Notifications, Preferences, Digests, Delivery, and Failure Handling  
**Purpose:** Deliver permission-safe in-app and email notifications for assignments, reminders, escalations, approvals, blockers, bugs, releases, client responses, and system alerts.  
**Requirements:** MVP-FR-011  
**Dependencies:** MOD-100, MOD-130, MOD-040

#### Main points

- [ ] **MOD-440-MP-001:** Implement and verify notifications.
- [ ] **MOD-440-MP-002:** Implement and verify preferences.
- [ ] **MOD-440-MP-003:** Implement and verify templates.
- [ ] **MOD-440-MP-004:** Implement and verify deliveries.
- [ ] **MOD-440-MP-005:** Implement and verify retries.
- [ ] **MOD-440-MP-006:** Implement and verify dead letters.
- [ ] **MOD-440-MP-007:** Implement and verify digests.

#### Database / data design

- [ ] **MOD-440-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **notifications**.
- [ ] **MOD-440-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **preferences**.
- [ ] **MOD-440-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **templates**.
- [ ] **MOD-440-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deliveries**.
- [ ] **MOD-440-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **retries**.
- [ ] **MOD-440-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **dead letters**.
- [ ] **MOD-440-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **digests**.

#### Backend

- [ ] **MOD-440-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-440-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-440-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-440-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-440-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-440-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-440-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-440-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-440-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-440-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-440-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-440-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-440-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-440-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-440-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-440-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-440-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-440-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-440-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-440-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-440-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-440-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-440-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-440-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-440-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-440-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-440-AC-001:** Notifications are timely, idempotent, auditable, and permission-safe.
- [ ] **MOD-440-AC-002:** Users can configure preferences without disabling mandatory critical alerts.
- [ ] **MOD-440-AC-003:** Delivery failures are visible and recoverable.
- [ ] **MOD-440-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-440-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-440-DONE:** Module marked Done before dependents

### MOD-450

**Title:** Dashboard, Reporting, Search, Project Health, and Activity Timeline  
**Purpose:** Provide role-aware deterministic dashboards for queries, projects, phases, tickets, workload, follow-ups, approvals, quality, milestones, agent actions, and overrides.  
**Requirements:** MVP-FR-012, MVP-FR-013, MVP-NFR-003  
**Dependencies:** MOD-210, MOD-240, MOD-300, MOD-340, MOD-330, MOD-400, MOD-410, MOD-040

#### Main points

- [ ] **MOD-450-MP-001:** Implement and verify dashboard read models.
- [ ] **MOD-450-MP-002:** Implement and verify project health.
- [ ] **MOD-450-MP-003:** Implement and verify saved filters.
- [ ] **MOD-450-MP-004:** Implement and verify global search.
- [ ] **MOD-450-MP-005:** Implement and verify activity timeline.
- [ ] **MOD-450-MP-006:** Implement and verify reports.
- [ ] **MOD-450-MP-007:** Implement and verify exports.

#### Database / data design

- [ ] **MOD-450-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **dashboard read models**.
- [ ] **MOD-450-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project health**.
- [ ] **MOD-450-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **saved filters**.
- [ ] **MOD-450-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **global search**.
- [ ] **MOD-450-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **activity timeline**.
- [ ] **MOD-450-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reports**.
- [ ] **MOD-450-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **exports**.

#### Backend

- [ ] **MOD-450-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-450-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-450-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-450-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-450-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-450-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-450-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-450-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-450-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-450-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-450-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-450-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-450-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-450-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-450-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-450-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-450-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-450-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-450-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-450-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-450-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-450-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-450-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-450-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-450-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-450-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-450-AC-001:** Dashboard values reconcile with source records.
- [ ] **MOD-450-AC-002:** Normal updates appear within one minute.
- [ ] **MOD-450-AC-003:** Counts, search, and exports do not leak unauthorized data.
- [ ] **MOD-450-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-450-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-450-DONE:** Module marked Done before dependents

### MOD-460

**Title:** Requirement Traceability, Audit Reports, and Evidence Exports  
**Purpose:** Provide end-to-end traceability from requirement version through phase, story, ticket, test, bug, change, release, approval, and delivery evidence.  
**Requirements:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-040, MOD-240, MOD-300, MOD-400, MOD-410, MOD-430

#### Main points

- [ ] **MOD-460-MP-001:** Implement and verify requirement-ticket links.
- [ ] **MOD-460-MP-002:** Implement and verify requirement-test links.
- [ ] **MOD-460-MP-003:** Implement and verify requirement-release links.
- [ ] **MOD-460-MP-004:** Implement and verify requirement-document links.
- [ ] **MOD-460-MP-005:** Implement and verify ticket-test links.
- [ ] **MOD-460-MP-006:** Implement and verify evidence manifests.

#### Database / data design

- [ ] **MOD-460-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-ticket links**.
- [ ] **MOD-460-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-test links**.
- [ ] **MOD-460-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-release links**.
- [ ] **MOD-460-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-document links**.
- [ ] **MOD-460-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket-test links**.
- [ ] **MOD-460-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **evidence manifests**.

#### Backend

- [ ] **MOD-460-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-460-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-460-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-460-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-460-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-460-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-460-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-460-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-460-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-460-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-460-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-460-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-460-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-460-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-460-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-460-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-460-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-460-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-460-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-460-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-460-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-460-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-460-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-460-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-460-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-460-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-460-AC-001:** At least 95% of Must-Have requirements have complete traceability before release.
- [ ] **MOD-460-AC-002:** Controlled actions have 100% audit coverage.
- [ ] **MOD-460-AC-003:** Exports are permission-controlled and independently reconcilable.
- [ ] **MOD-460-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-460-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-460-DONE:** Module marked Done before dependents

## Phase 5 - MVP Integrations

### MOD-500

**Title:** Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State  
**Purpose:** Create a provider-based integration foundation with OAuth, secure token references, webhook validation, idempotency, rate limits, retries, dead letters, and sync audit.  
**Requirements:** MVP-FR-014, MVP-FR-015, MVP-NFR-004  
**Dependencies:** MOD-030, MOD-040, MOD-120

#### Main points

- [ ] **MOD-500-MP-001:** Implement and verify integration connections.
- [ ] **MOD-500-MP-002:** Implement and verify webhook events.
- [ ] **MOD-500-MP-003:** Implement and verify sync cursors.
- [ ] **MOD-500-MP-004:** Implement and verify external mappings.
- [ ] **MOD-500-MP-005:** Implement and verify outbox events.
- [ ] **MOD-500-MP-006:** Implement and verify inbox events.
- [ ] **MOD-500-MP-007:** Implement and verify connection health.

#### Database / data design

- [ ] **MOD-500-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **integration connections**.
- [ ] **MOD-500-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **webhook events**.
- [ ] **MOD-500-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **sync cursors**.
- [ ] **MOD-500-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **external mappings**.
- [ ] **MOD-500-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **outbox events**.
- [ ] **MOD-500-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **inbox events**.
- [ ] **MOD-500-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **connection health**.

#### Backend

- [ ] **MOD-500-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-500-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-500-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-500-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-500-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-500-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-500-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-500-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-500-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-500-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-500-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-500-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-500-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-500-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-500-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-500-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-500-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-500-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-500-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-500-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-500-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-500-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-500-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-500-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-500-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-500-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-500-AC-001:** Integration failure cannot corrupt internal data.
- [ ] **MOD-500-AC-002:** External mappings and events are tenant-scoped and audited.
- [ ] **MOD-500-AC-003:** Credentials never appear in logs, prompts, tickets, or business tables.
- [ ] **MOD-500-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-500-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-500-DONE:** Module marked Done before dependents

### MOD-510

**Title:** Gmail Client Communication Integration  
**Purpose:** Receive approved mailbox inquiries, preserve threads and attachments, detect replies, create or update queries, prepare drafts, and send approved email.  
**Requirements:** MVP-FR-014  
**Dependencies:** MOD-220, MOD-500, MOD-210, MOD-230

#### Main points

- [ ] **MOD-510-MP-001:** Implement and verify Gmail connection.
- [ ] **MOD-510-MP-002:** Implement and verify history cursor.
- [ ] **MOD-510-MP-003:** Implement and verify thread mappings.
- [ ] **MOD-510-MP-004:** Implement and verify message mappings.
- [ ] **MOD-510-MP-005:** Implement and verify attachment import.
- [ ] **MOD-510-MP-006:** Implement and verify draft review.
- [ ] **MOD-510-MP-007:** Implement and verify approved send.

#### Database / data design

- [ ] **MOD-510-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **Gmail connection**.
- [ ] **MOD-510-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **history cursor**.
- [ ] **MOD-510-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **thread mappings**.
- [ ] **MOD-510-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **message mappings**.
- [ ] **MOD-510-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachment import**.
- [ ] **MOD-510-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **draft review**.
- [ ] **MOD-510-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approved send**.

#### Backend

- [ ] **MOD-510-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-510-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-510-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-510-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-510-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-510-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-510-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-510-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-510-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-510-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-510-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-510-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-510-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-510-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-510-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-510-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-510-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-510-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-510-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-510-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-510-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-510-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-510-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-510-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-510-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-510-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-510-AC-001:** Valid emails create or update exactly one query and thread.
- [ ] **MOD-510-AC-002:** Approved outgoing email is sent and linked correctly.
- [ ] **MOD-510-AC-003:** Duplicate notifications do not duplicate records.
- [ ] **MOD-510-AC-900:** All Critical and High defects for this module are resolved.
- [ ] **MOD-510-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### Module completion

- [ ] **MOD-510-DONE:** Module marked Done before dependents

### MOD-520

**Title:** Jira Work Management Integration  
**Purpose:** Create approved Jira issues, map fields and status, synchronize allowed updates, and process webhooks without bypassing internal rules.  
**Requirements:** MVP-FR-015  
**Dependencies:** MOD-300, MOD-310, MOD-320, MOD-500

#### Main points

- [ ] **MOD-520-MP-001:** Implement and verify Jira connection.
- [ ] **MOD-520-MP-002:** Implement and verify project mapping.
- [ ] **MOD-520-MP-003:** Implement and verify field mapping.
- [ ] **MOD-520-MP-004:** Implement and verify status mapping.
- [ ] **MOD-520-MP-005:** Implement and verify issue mapping.
- [ ] **MOD-520-MP-006:** Implement and verify comment sync.
- [ ] **MOD-520-MP-007:** Implement and verify conflict handling.

#### Database / data design

- [ ] **MOD-520-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **Jira connection**.
- [ ] **MOD-520-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project mapping**.
- [ ] **MOD-520-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **field mapping**.
- [ ] **MOD-520-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status mapping**.
- [ ] **MOD-520-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **issue mapping**.
- [ ] **MOD-520-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **comment sync**.
- [ ] **MOD-520-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **conflict handling**.

#### Backend

- [ ] **MOD-520-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- [ ] **MOD-520-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- [ ] **MOD-520-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- [ ] **MOD-520-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API

- [ ] **MOD-520-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- [ ] **MOD-520-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- [ ] **MOD-520-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend

- [ ] **MOD-520-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- [ ] **MOD-520-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- [ ] **MOD-520-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- [ ] **MOD-520-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow / agent / events / notifications

- [ ] **MOD-520-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- [ ] **MOD-520-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- [ ] **MOD-520-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- [ ] **MOD-520-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security / privacy / audit

- [ ] **MOD-520-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- [ ] **MOD-520-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- [ ] **MOD-520-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- [ ] **MOD-520-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing / verification

- [ ] **MOD-520-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- [ ] **MOD-520-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- [ ] **MOD-520-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- [ ] **MOD-520-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- [ ] **MOD-520-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation

- [ ] **MOD-520-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- [ ] **MOD-520-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance gate

- [ ] **MOD-520-AC-001:** Approved internal tickets create Jira issues and retain keys.
- [ ] **MOD-520-AC-002:** Jira cannot bypass internal transition or approval rules.
- [ ] **MOD-520-AC-003:** Sync failures are visible, retriable, and audited.
- [ ] **MOD-520-AC-900:** All Critical and High defects for this module are resolved.
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
