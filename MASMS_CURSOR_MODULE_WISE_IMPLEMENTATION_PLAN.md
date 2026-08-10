# MASMS Cursor Module-Wise Implementation Plan

**Project:** Multi-Agent Software House Management System (MASMS)  
**Document Type:** Sequential Cursor Development Plan  
**Status:** Implementation Baseline Draft  
**Execution Rule:** Cursor must complete and verify one task ID before starting the next dependent task.

## 1. Architecture Boundaries

- **FastAPI:** deterministic business rules and authoritative data changes.
- **Temporal:** durable workflows, waits, timers, retries, reminders, escalations, and approval pauses.
- **LangGraph:** bounded AI reasoning and recommendations.
- **PostgreSQL:** authoritative transactional state.
- **pgvector:** permission-filtered semantic retrieval only.
- **Service Bus:** asynchronous domain and integration events; never a replacement for transactions.
- **Human approval:** mandatory for scope, quotation, timeline, SRS, material allocation, architecture, change requests, production, delivery, and closure.

## 2. ID Structure

| Item | Format | Example |
|---|---|---|
| Module | `MOD-NNN` | `MOD-340` |
| Database | `MOD-NNN-DB-NNN` | `MOD-340-DB-001` |
| Backend | `MOD-NNN-BE-NNN` | `MOD-340-BE-001` |
| API | `MOD-NNN-API-NNN` | `MOD-340-API-001` |
| Frontend | `MOD-NNN-FE-NNN` | `MOD-340-FE-001` |
| Workflow/Agent/Event | `MOD-NNN-WF-NNN` | `MOD-340-WF-001` |
| Security/Audit | `MOD-NNN-SEC-NNN` | `MOD-340-SEC-001` |
| Test | `MOD-NNN-QA-NNN` | `MOD-340-QA-001` |
| Documentation | `MOD-NNN-DOC-NNN` | `MOD-340-DOC-001` |
| Acceptance | `MOD-NNN-AC-NNN` | `MOD-340-AC-001` |

## 3. Cursor Task Lifecycle

1. Load the task ID, requirement IDs, dependencies, and acceptance criteria.
2. Inspect existing files, patterns, schemas, APIs, rules, tests, migrations, and documentation.
3. Identify permission, tenant, project, status, approval, audit, workflow, agent, event, notification, and integration impacts.
4. List expected file changes and verification commands.
5. Implement the smallest complete change.
6. Add tests, migration, OpenAPI, audit, events, documentation, and rollback notes.
7. Run formatter, lint, type checks, tests, builds, scans, and module-specific verification.
8. Report completed, failed, blocked, unverified, assumed, and follow-up items truthfully.
9. Move to the next task only after evidence-based completion or formal blocker recording.

## 4. Target Repository View

```text
masms/
├── .cursor/rules/
├── AGENTS.md
├── apps/
│   ├── web/
│   ├── api/
│   ├── temporal-worker/
│   ├── agent-worker/
│   └── integration-worker/
├── packages/
│   ├── ui/
│   ├── contracts/
│   ├── api-client/
│   └── config/
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── workflow/
│   ├── agent/
│   ├── security/
│   ├── performance/
│   └── e2e/
├── infrastructure/
├── docs/
└── scripts/
```

## 5. Module Index

| Seq. | ID | Module | Phase | Requirements |
|---:|---|---|---|---|
| 1 | MOD-000 | Project Governance, Source Baseline, and Change Control | Phase 0 — Governance and Foundation | MVP-NFR-010, SRS Change Control |
| 2 | MOD-010 | Repository, Toolchain, and Local Development Environment | Phase 0 — Governance and Foundation | Cursor Rules 010, Cursor Rules 600–720 |
| 3 | MOD-020 | Shared Architecture, Domain Kernel, and API Standards | Phase 0 — Governance and Foundation | MVP-NFR-004, MVP-NFR-010 |
| 4 | MOD-030 | Environment Configuration, Secrets, CI/CD, and Deployment Skeleton | Phase 0 — Governance and Foundation | MVP-NFR-001, MVP-NFR-007 |
| 5 | MOD-040 | Observability, Audit Foundation, and Operational Health | Phase 0 — Governance and Foundation | MVP-FR-013, MVP-NFR-005 |
| 6 | MOD-100 | Organizations, Actors, Human Users, Agents, Teams, and Departments | Phase 1 — Identity, Organization, and Configuration | MVP-FR-001 |
| 7 | MOD-110 | Authentication, Sessions, MFA, and Account Security | Phase 1 — Identity, Organization, and Configuration | MVP-FR-001, MVP-NFR-001 |
| 8 | MOD-120 | RBAC, Attribute-Based Access, Project Membership, and Row-Level Security | Phase 1 — Identity, Organization, and Configuration | MVP-FR-001, MVP-NFR-001, MVP-NFR-002 |
| 9 | MOD-130 | Skills, Availability, Capacity, Working Hours, and Business Calendars | Phase 1 — Identity, Organization, and Configuration | MVP-FR-005 |
| 10 | MOD-140 | Configuration Administration and Versioned Operational Rules | Phase 1 — Identity, Organization, and Configuration | MVP-FR-016, MVP-NFR-010 |
| 11 | MOD-200 | Client and Contact Management | Phase 2 — Client, Query, and Requirement Management | MVP-FR-002 |
| 12 | MOD-210 | Client Queries, Qualification, and Opportunities | Phase 2 — Client, Query, and Requirement Management | MVP-FR-002, MVP-FR-003 |
| 13 | MOD-220 | Conversations, Messages, Attachments, and Communication History | Phase 2 — Client, Query, and Requirement Management | MVP-FR-011, MVP-FR-014 |
| 14 | MOD-230 | Requirement Gathering, Completeness Analysis, Clarifications, and Requirement Brief | Phase 2 — Client, Query, and Requirement Management | MVP-FR-003 |
| 15 | MOD-240 | Projects, Requirements, Requirement Versions, and SRS Management | Phase 2 — Client, Query, and Requirement Management | MVP-FR-004, MVP-FR-013 |
| 16 | MOD-250 | Documents, Standard Templates, Versioning, and Secure File Storage | Phase 2 — Client, Query, and Requirement Management | MVP-FR-010 |
| 17 | MOD-260 | Project Phases, Milestones, Roadmaps, Dependencies, and Baselines | Phase 2 — Client, Query, and Requirement Management | MVP-FR-004 |
| 18 | MOD-300 | Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion | Phase 3 — Work Management and Agent Orchestration | MVP-FR-005, MVP-FR-013 |
| 19 | MOD-310 | Skill- and Capacity-Based Assignment and Ownership History | Phase 3 — Work Management and Agent Orchestration | MVP-FR-005 |
| 20 | MOD-320 | Configurable Status and Transition Engine | Phase 3 — Work Management and Agent Orchestration | MVP-FR-016 |
| 21 | MOD-330 | Human Approval Gates, Delegation, Rejection, and Override | Phase 3 — Work Management and Agent Orchestration | MVP-FR-008 |
| 22 | MOD-340 | Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations | Phase 3 — Work Management and Agent Orchestration | MVP-FR-007 |
| 23 | MOD-350 | Temporal Orchestrator and Durable Business Workflows | Phase 3 — Work Management and Agent Orchestration | MVP-FR-006, MVP-FR-007, MVP-NFR-004 |
| 24 | MOD-360 | LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision | Phase 3 — Work Management and Agent Orchestration | MVP-FR-006, MVP-NFR-008, MVP-NFR-009 |
| 25 | MOD-370 | Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation | Phase 3 — Work Management and Agent Orchestration | MVP-FR-010, MVP-NFR-008, MVP-NFR-009 |
| 26 | MOD-400 | Test Cases, Test Steps, Test Runs, Evidence, and Coverage | Phase 4 — Quality, Change, Release, and Reporting | MVP-FR-009, MVP-FR-013 |
| 27 | MOD-410 | Bug Lifecycle, QA Rejection, Development Reopen, and Retesting | Phase 4 — Quality, Change, Release, and Reporting | MVP-FR-009 |
| 28 | MOD-420 | Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates | Phase 4 — Quality, Change, Release, and Reporting | MVP-FR-008, MVP-FR-013 |
| 29 | MOD-430 | Releases, Deployment Requests, Production Approval, Rollback, and Closure | Phase 4 — Quality, Change, Release, and Reporting | MVP-FR-008, MVP-FR-009 |
| 30 | MOD-440 | Notifications, Preferences, Digests, Delivery, and Failure Handling | Phase 4 — Quality, Change, Release, and Reporting | MVP-FR-011 |
| 31 | MOD-450 | Dashboard, Reporting, Search, Project Health, and Activity Timeline | Phase 4 — Quality, Change, Release, and Reporting | MVP-FR-012, MVP-FR-013, MVP-NFR-003 |
| 32 | MOD-460 | Requirement Traceability, Audit Reports, and Evidence Exports | Phase 4 — Quality, Change, Release, and Reporting | MVP-FR-013, MVP-NFR-005 |
| 33 | MOD-500 | Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State | Phase 5 — MVP Integrations | MVP-FR-014, MVP-FR-015, MVP-NFR-004 |
| 34 | MOD-510 | Gmail Client Communication Integration | Phase 5 — MVP Integrations | MVP-FR-014 |
| 35 | MOD-520 | Jira Work Management Integration | Phase 5 — MVP Integrations | MVP-FR-015 |
| 36 | MOD-600 | Security, Privacy, PII, File Safety, Retention, Backup, and Recovery Hardening | Phase 6 — Security, Reliability, Pilot, and Production Readiness | MVP-NFR-001, MVP-NFR-002, MVP-NFR-007, MVP-NFR-008, MVP-NFR-009 |
| 37 | MOD-610 | Performance, Reliability, Idempotency, Resilience, and Disaster Recovery | Phase 6 — Security, Reliability, Pilot, and Production Readiness | MVP-NFR-003, MVP-NFR-004, MVP-NFR-006, MVP-NFR-007 |
| 38 | MOD-620 | Synthetic Sample Projects, Agent Evaluation, End-to-End Acceptance, and UAT | Phase 6 — Security, Reliability, Pilot, and Production Readiness | MVP Acceptance Criteria, Sample Projects |
| 39 | MOD-630 | Controlled Pilot, Production Release, Operations, and Final MVP Sign-Off | Phase 6 — Security, Reliability, Pilot, and Production Readiness | MVP Exit Criteria, Final Acceptance Sign-Off |

## Phase 0 — Governance and Foundation

### MOD-000 — Project Governance, Source Baseline, and Change Control

**Purpose:** Establish the approved source of truth, change discipline, requirement IDs, architecture decisions, and human accountability before implementation.

**Requirement Mapping:** MVP-NFR-010, SRS Change Control  
**Dependencies:** None

#### Main Points

1. **MOD-000-MP-001:** Implement and verify baseline register.
2. **MOD-000-MP-002:** Implement and verify requirement mapping.
3. **MOD-000-MP-003:** Implement and verify architecture decision records.
4. **MOD-000-MP-004:** Implement and verify change requests.
5. **MOD-000-MP-005:** Implement and verify approval records.

#### Database and Backend Tasks

- **MOD-000-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **baseline register**.
- **MOD-000-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement mapping**.
- **MOD-000-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **architecture decision records**.
- **MOD-000-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **change requests**.
- **MOD-000-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval records**.
- **MOD-000-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-000-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-000-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-000-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-000-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-000-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-000-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-000-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-000-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-000-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-000-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-000-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-000-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-000-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-000-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-000-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-000-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-000-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-000-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-000-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-000-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-000-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-000-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-000-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-000-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-000-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-000-AC-001:** One approved source of truth is identified.
- **MOD-000-AC-002:** Material changes require a new version and human approval.
- **MOD-000-AC-003:** Every implementation task maps to a module and requirement ID.
- **MOD-000-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-000-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-000-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-010 — Repository, Toolchain, and Local Development Environment

**Purpose:** Create a reproducible monorepo and local environment for Next.js, FastAPI, Temporal, LangGraph, PostgreSQL, Redis, Service Bus, and object storage.

**Requirement Mapping:** Cursor Rules 010, Cursor Rules 600–720  
**Dependencies:** MOD-000

#### Main Points

1. **MOD-010-MP-001:** Implement and verify monorepo structure.
2. **MOD-010-MP-002:** Implement and verify language versions.
3. **MOD-010-MP-003:** Implement and verify package managers.
4. **MOD-010-MP-004:** Implement and verify Docker Compose.
5. **MOD-010-MP-005:** Implement and verify formatting and linting.
6. **MOD-010-MP-006:** Implement and verify typing.
7. **MOD-010-MP-007:** Implement and verify tests.
8. **MOD-010-MP-008:** Implement and verify CI build.

#### Database and Backend Tasks

- **MOD-010-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **monorepo structure**.
- **MOD-010-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **language versions**.
- **MOD-010-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **package managers**.
- **MOD-010-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **Docker Compose**.
- **MOD-010-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **formatting and linting**.
- **MOD-010-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **typing**.
- **MOD-010-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tests**.
- **MOD-010-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **CI build**.
- **MOD-010-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-010-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-010-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-010-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-010-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-010-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-010-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-010-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-010-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-010-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-010-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-010-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-010-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-010-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-010-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-010-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-010-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-010-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-010-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-010-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-010-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-010-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-010-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-010-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-010-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-010-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-010-AC-001:** A new developer can start the stack from documented commands.
- **MOD-010-AC-002:** CI blocks formatting, type, test, or build failures.
- **MOD-010-AC-003:** No real secret exists in source control.
- **MOD-010-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-010-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-010-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-020 — Shared Architecture, Domain Kernel, and API Standards

**Purpose:** Create common typed identifiers, actor and tenant context, domain errors, transactions, idempotency, API contracts, and event boundaries.

**Requirement Mapping:** MVP-NFR-004, MVP-NFR-010  
**Dependencies:** MOD-010

#### Main Points

1. **MOD-020-MP-001:** Implement and verify typed identifiers.
2. **MOD-020-MP-002:** Implement and verify actor context.
3. **MOD-020-MP-003:** Implement and verify tenant context.
4. **MOD-020-MP-004:** Implement and verify domain errors.
5. **MOD-020-MP-005:** Implement and verify unit of work.
6. **MOD-020-MP-006:** Implement and verify outbox.
7. **MOD-020-MP-007:** Implement and verify API problem details.
8. **MOD-020-MP-008:** Implement and verify pagination.
9. **MOD-020-MP-009:** Implement and verify optimistic concurrency.

#### Database and Backend Tasks

- **MOD-020-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **typed identifiers**.
- **MOD-020-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actor context**.
- **MOD-020-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tenant context**.
- **MOD-020-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **domain errors**.
- **MOD-020-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **unit of work**.
- **MOD-020-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **outbox**.
- **MOD-020-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **API problem details**.
- **MOD-020-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **pagination**.
- **MOD-020-DB-009:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **optimistic concurrency**.
- **MOD-020-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-020-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-020-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-020-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-020-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-020-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-020-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-020-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-020-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-020-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-020-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-020-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-020-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-020-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-020-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-020-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-020-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-020-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-020-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-020-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-020-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-020-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-020-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-020-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-020-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-020-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-020-AC-001:** All modules use the same actor and tenant context.
- **MOD-020-AC-002:** Agents and workflows cannot bypass application services.
- **MOD-020-AC-003:** API contracts are consistent and documented.
- **MOD-020-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-020-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-020-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-030 — Environment Configuration, Secrets, CI/CD, and Deployment Skeleton

**Purpose:** Separate development, test, staging, and production configuration; establish secret retrieval, CI/CD, infrastructure, and rollback-ready deployment skeletons.

**Requirement Mapping:** MVP-NFR-001, MVP-NFR-007  
**Dependencies:** MOD-010, MOD-020

#### Main Points

1. **MOD-030-MP-001:** Implement and verify environment matrix.
2. **MOD-030-MP-002:** Implement and verify secret manager.
3. **MOD-030-MP-003:** Implement and verify CI pipelines.
4. **MOD-030-MP-004:** Implement and verify staging deployment.
5. **MOD-030-MP-005:** Implement and verify production approval placeholder.
6. **MOD-030-MP-006:** Implement and verify infrastructure as code.

#### Database and Backend Tasks

- **MOD-030-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **environment matrix**.
- **MOD-030-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **secret manager**.
- **MOD-030-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **CI pipelines**.
- **MOD-030-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **staging deployment**.
- **MOD-030-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **production approval placeholder**.
- **MOD-030-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **infrastructure as code**.
- **MOD-030-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-030-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-030-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-030-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-030-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-030-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-030-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-030-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-030-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-030-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-030-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-030-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-030-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-030-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-030-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-030-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-030-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-030-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-030-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-030-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-030-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-030-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-030-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-030-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-030-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-030-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-030-AC-001:** Environment credentials are isolated.
- **MOD-030-AC-002:** Production release requires human authorization.
- **MOD-030-AC-003:** Artifacts are reproducible and traceable.
- **MOD-030-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-030-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-030-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-040 — Observability, Audit Foundation, and Operational Health

**Purpose:** Implement structured logging, tracing, metrics, append-only audit, activity events, correlation IDs, and operational alerts.

**Requirement Mapping:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-020, MOD-030

#### Main Points

1. **MOD-040-MP-001:** Implement and verify audit logs.
2. **MOD-040-MP-002:** Implement and verify activity events.
3. **MOD-040-MP-003:** Implement and verify status history.
4. **MOD-040-MP-004:** Implement and verify agent runs.
5. **MOD-040-MP-005:** Implement and verify integration events.
6. **MOD-040-MP-006:** Implement and verify OpenTelemetry.
7. **MOD-040-MP-007:** Implement and verify health checks.

#### Database and Backend Tasks

- **MOD-040-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **audit logs**.
- **MOD-040-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **activity events**.
- **MOD-040-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status history**.
- **MOD-040-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent runs**.
- **MOD-040-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **integration events**.
- **MOD-040-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **OpenTelemetry**.
- **MOD-040-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **health checks**.
- **MOD-040-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-040-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-040-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-040-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-040-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-040-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-040-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-040-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-040-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-040-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-040-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-040-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-040-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-040-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-040-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-040-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-040-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-040-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-040-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-040-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-040-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-040-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-040-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-040-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-040-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-040-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-040-AC-001:** Every controlled action is attributable to an actor.
- **MOD-040-AC-002:** Audit records are append-only for operational roles.
- **MOD-040-AC-003:** Failures are diagnosable without revealing secrets.
- **MOD-040-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-040-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-040-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

## Phase 1 — Identity, Organization, and Configuration

### MOD-100 — Organizations, Actors, Human Users, Agents, Teams, and Departments

**Purpose:** Implement the organization and shared actor model used for ownership, reporting, escalation, approval, assignment, and audit.

**Requirement Mapping:** MVP-FR-001  
**Dependencies:** MOD-020, MOD-040

#### Main Points

1. **MOD-100-MP-001:** Implement and verify organizations.
2. **MOD-100-MP-002:** Implement and verify actors.
3. **MOD-100-MP-003:** Implement and verify human users.
4. **MOD-100-MP-004:** Implement and verify agents.
5. **MOD-100-MP-005:** Implement and verify roles.
6. **MOD-100-MP-006:** Implement and verify departments.
7. **MOD-100-MP-007:** Implement and verify teams.
8. **MOD-100-MP-008:** Implement and verify team members.
9. **MOD-100-MP-009:** Implement and verify reporting lines.

#### Database and Backend Tasks

- **MOD-100-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **organizations**.
- **MOD-100-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actors**.
- **MOD-100-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **human users**.
- **MOD-100-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agents**.
- **MOD-100-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **roles**.
- **MOD-100-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **departments**.
- **MOD-100-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **teams**.
- **MOD-100-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **team members**.
- **MOD-100-DB-009:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reporting lines**.
- **MOD-100-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-100-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-100-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-100-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-100-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-100-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-100-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-100-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-100-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-100-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-100-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-100-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-100-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-100-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-100-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-100-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-100-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-100-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-100-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-100-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-100-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-100-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-100-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-100-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-100-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-100-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-100-AC-001:** Every action and owner resolves to one actor.
- **MOD-100-AC-002:** Every operational agent has an active human supervisor.
- **MOD-100-AC-003:** Agent and human identities are separate.
- **MOD-100-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-100-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-100-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-110 — Authentication, Sessions, MFA, and Account Security

**Purpose:** Authenticate humans and machine identities, support MFA and step-up authentication, invitations, session revocation, and service authentication.

**Requirement Mapping:** MVP-FR-001, MVP-NFR-001  
**Dependencies:** MOD-100, MOD-030

#### Main Points

1. **MOD-110-MP-001:** Implement and verify identity provider.
2. **MOD-110-MP-002:** Implement and verify token validation.
3. **MOD-110-MP-003:** Implement and verify sessions.
4. **MOD-110-MP-004:** Implement and verify MFA.
5. **MOD-110-MP-005:** Implement and verify step-up authentication.
6. **MOD-110-MP-006:** Implement and verify client invitations.
7. **MOD-110-MP-007:** Implement and verify service identities.

#### Database and Backend Tasks

- **MOD-110-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **identity provider**.
- **MOD-110-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **token validation**.
- **MOD-110-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **sessions**.
- **MOD-110-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **MFA**.
- **MOD-110-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **step-up authentication**.
- **MOD-110-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **client invitations**.
- **MOD-110-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **service identities**.
- **MOD-110-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-110-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-110-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-110-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-110-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-110-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-110-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-110-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-110-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-110-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-110-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-110-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-110-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-110-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-110-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-110-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-110-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-110-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-110-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-110-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-110-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-110-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-110-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-110-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-110-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-110-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-110-AC-001:** All human and machine actions use authenticated actor identities.
- **MOD-110-AC-002:** Privileged actions require appropriate assurance.
- **MOD-110-AC-003:** Sessions can be revoked immediately.
- **MOD-110-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-110-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-110-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-120 — RBAC, Attribute-Based Access, Project Membership, and Row-Level Security

**Purpose:** Enforce deny-by-default authorization across organization, client, project, module, action, environment, classification, and approval authority.

**Requirement Mapping:** MVP-FR-001, MVP-NFR-001, MVP-NFR-002  
**Dependencies:** MOD-100, MOD-110

#### Main Points

1. **MOD-120-MP-001:** Implement and verify permissions.
2. **MOD-120-MP-002:** Implement and verify role permissions.
3. **MOD-120-MP-003:** Implement and verify project members.
4. **MOD-120-MP-004:** Implement and verify module access.
5. **MOD-120-MP-005:** Implement and verify document access.
6. **MOD-120-MP-006:** Implement and verify approval authorities.
7. **MOD-120-MP-007:** Implement and verify RLS policies.
8. **MOD-120-MP-008:** Implement and verify access reviews.

#### Database and Backend Tasks

- **MOD-120-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **permissions**.
- **MOD-120-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **role permissions**.
- **MOD-120-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project members**.
- **MOD-120-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **module access**.
- **MOD-120-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document access**.
- **MOD-120-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval authorities**.
- **MOD-120-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **RLS policies**.
- **MOD-120-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **access reviews**.
- **MOD-120-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-120-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-120-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-120-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-120-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-120-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-120-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-120-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-120-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-120-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-120-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-120-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-120-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-120-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-120-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-120-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-120-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-120-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-120-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-120-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-120-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-120-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-120-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-120-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-120-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-120-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-120-AC-001:** No cross-client access exists through API, database, files, cache, vectors, search, or exports.
- **MOD-120-AC-002:** Project access requires valid membership or explicit authority.
- **MOD-120-AC-003:** Frontend visibility never replaces backend authorization.
- **MOD-120-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-120-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-120-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-130 — Skills, Availability, Capacity, Working Hours, and Business Calendars

**Purpose:** Store skill, proficiency, availability, capacity, leave, time zone, business hours, holidays, and on-call data for assignments and SLA calculations.

**Requirement Mapping:** MVP-FR-005  
**Dependencies:** MOD-100, MOD-120

#### Main Points

1. **MOD-130-MP-001:** Implement and verify skills.
2. **MOD-130-MP-002:** Implement and verify actor skills.
3. **MOD-130-MP-003:** Implement and verify availability.
4. **MOD-130-MP-004:** Implement and verify capacity allocations.
5. **MOD-130-MP-005:** Implement and verify business calendars.
6. **MOD-130-MP-006:** Implement and verify holidays.
7. **MOD-130-MP-007:** Implement and verify leave periods.
8. **MOD-130-MP-008:** Implement and verify on-call schedules.

#### Database and Backend Tasks

- **MOD-130-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **skills**.
- **MOD-130-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **actor skills**.
- **MOD-130-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **availability**.
- **MOD-130-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **capacity allocations**.
- **MOD-130-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business calendars**.
- **MOD-130-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **holidays**.
- **MOD-130-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **leave periods**.
- **MOD-130-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **on-call schedules**.
- **MOD-130-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-130-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-130-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-130-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-130-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-130-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-130-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-130-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-130-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-130-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-130-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-130-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-130-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-130-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-130-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-130-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-130-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-130-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-130-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-130-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-130-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-130-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-130-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-130-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-130-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-130-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-130-AC-001:** Assignments can evaluate skill, access, capacity, calendar, and deadline.
- **MOD-130-AC-002:** SLA calculations respect business calendars and time zones.
- **MOD-130-AC-003:** Unnecessary personal data is excluded.
- **MOD-130-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-130-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-130-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-140 — Configuration Administration and Versioned Operational Rules

**Purpose:** Allow approved configuration of statuses, transitions, SLAs, reminders, escalations, approvals, templates, and agent limits without code deployment.

**Requirement Mapping:** MVP-FR-016, MVP-NFR-010  
**Dependencies:** MOD-000, MOD-120, MOD-130

#### Main Points

1. **MOD-140-MP-001:** Implement and verify workflow definitions.
2. **MOD-140-MP-002:** Implement and verify status definitions.
3. **MOD-140-MP-003:** Implement and verify transition rules.
4. **MOD-140-MP-004:** Implement and verify follow-up rules.
5. **MOD-140-MP-005:** Implement and verify reminder rules.
6. **MOD-140-MP-006:** Implement and verify escalation rules.
7. **MOD-140-MP-007:** Implement and verify approval workflows.
8. **MOD-140-MP-008:** Implement and verify configuration versions.

#### Database and Backend Tasks

- **MOD-140-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow definitions**.
- **MOD-140-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status definitions**.
- **MOD-140-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **transition rules**.
- **MOD-140-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **follow-up rules**.
- **MOD-140-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reminder rules**.
- **MOD-140-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **escalation rules**.
- **MOD-140-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval workflows**.
- **MOD-140-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **configuration versions**.
- **MOD-140-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-140-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-140-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-140-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-140-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-140-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-140-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-140-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-140-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-140-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-140-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-140-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-140-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-140-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-140-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-140-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-140-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-140-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-140-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-140-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-140-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-140-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-140-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-140-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-140-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-140-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-140-AC-001:** Only approved effective configuration controls live execution.
- **MOD-140-AC-002:** Configuration changes require validation, audit, and rollback support.
- **MOD-140-AC-003:** Draft configuration cannot affect live workflows.
- **MOD-140-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-140-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-140-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

## Phase 2 — Client, Query, and Requirement Management

### MOD-200 — Client and Contact Management

**Purpose:** Manage client organizations, contacts, authority, preferences, ownership, duplicates, related projects, documents, messages, and activity.

**Requirement Mapping:** MVP-FR-002  
**Dependencies:** MOD-120, MOD-040

#### Main Points

1. **MOD-200-MP-001:** Implement and verify clients.
2. **MOD-200-MP-002:** Implement and verify contacts.
3. **MOD-200-MP-003:** Implement and verify project contacts.
4. **MOD-200-MP-004:** Implement and verify communication preferences.
5. **MOD-200-MP-005:** Implement and verify duplicate suggestions.
6. **MOD-200-MP-006:** Implement and verify merge history.

#### Database and Backend Tasks

- **MOD-200-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **clients**.
- **MOD-200-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **contacts**.
- **MOD-200-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project contacts**.
- **MOD-200-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **communication preferences**.
- **MOD-200-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **duplicate suggestions**.
- **MOD-200-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **merge history**.
- **MOD-200-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-200-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-200-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-200-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-200-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-200-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-200-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-200-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-200-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-200-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-200-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-200-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-200-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-200-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-200-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-200-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-200-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-200-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-200-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-200-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-200-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-200-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-200-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-200-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-200-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-200-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-200-AC-001:** Clients may have multiple contacts with explicit authority.
- **MOD-200-AC-002:** Duplicate handling preserves history.
- **MOD-200-AC-003:** Client records are isolated and auditable.
- **MOD-200-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-200-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-200-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-210 — Client Queries, Qualification, and Opportunities

**Purpose:** Capture, classify, assign, qualify, reject, convert, and trace inquiries while preserving original communication and qualification evidence.

**Requirement Mapping:** MVP-FR-002, MVP-FR-003  
**Dependencies:** MOD-200, MOD-140

#### Main Points

1. **MOD-210-MP-001:** Implement and verify queries.
2. **MOD-210-MP-002:** Implement and verify opportunities.
3. **MOD-210-MP-003:** Implement and verify qualification answers.
4. **MOD-210-MP-004:** Implement and verify query sources.
5. **MOD-210-MP-005:** Implement and verify query status history.
6. **MOD-210-MP-006:** Implement and verify first response SLA.

#### Database and Backend Tasks

- **MOD-210-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **queries**.
- **MOD-210-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **opportunities**.
- **MOD-210-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **qualification answers**.
- **MOD-210-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **query sources**.
- **MOD-210-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **query status history**.
- **MOD-210-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **first response SLA**.
- **MOD-210-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-210-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-210-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-210-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-210-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-210-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-210-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-210-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-210-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-210-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-210-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-210-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-210-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-210-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-210-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-210-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-210-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-210-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-210-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-210-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-210-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-210-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-210-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-210-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-210-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-210-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-210-AC-001:** Each valid inquiry creates one traceable query.
- **MOD-210-AC-002:** Qualification is reviewable and explainable.
- **MOD-210-AC-003:** Conversion preserves communication, documents, follow-ups, and decisions.
- **MOD-210-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-210-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-210-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-220 — Conversations, Messages, Attachments, and Communication History

**Purpose:** Store immutable internal and external communication threads, recipients, delivery status, revisions, attachments, and related business records.

**Requirement Mapping:** MVP-FR-011, MVP-FR-014  
**Dependencies:** MOD-200, MOD-040, MOD-120

#### Main Points

1. **MOD-220-MP-001:** Implement and verify conversations.
2. **MOD-220-MP-002:** Implement and verify messages.
3. **MOD-220-MP-003:** Implement and verify message revisions.
4. **MOD-220-MP-004:** Implement and verify recipients.
5. **MOD-220-MP-005:** Implement and verify delivery receipts.
6. **MOD-220-MP-006:** Implement and verify attachment links.

#### Database and Backend Tasks

- **MOD-220-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **conversations**.
- **MOD-220-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **messages**.
- **MOD-220-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **message revisions**.
- **MOD-220-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **recipients**.
- **MOD-220-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **delivery receipts**.
- **MOD-220-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachment links**.
- **MOD-220-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-220-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-220-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-220-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-220-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-220-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-220-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-220-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-220-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-220-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-220-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-220-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-220-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-220-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-220-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-220-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-220-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-220-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-220-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-220-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-220-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-220-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-220-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-220-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-220-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-220-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-220-AC-001:** Material communication is linked to the correct entity.
- **MOD-220-AC-002:** Sensitive messages follow approval and recipient rules.
- **MOD-220-AC-003:** Sent-message history is immutable.
- **MOD-220-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-220-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-220-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-230 — Requirement Gathering, Completeness Analysis, Clarifications, and Requirement Brief

**Purpose:** Run approved questionnaires, store structured answers, detect gaps and conflicts, create bidirectional clarifications, and produce a versioned requirement brief.

**Requirement Mapping:** MVP-FR-003  
**Dependencies:** MOD-210, MOD-220, MOD-250, MOD-330

#### Main Points

1. **MOD-230-MP-001:** Implement and verify questionnaires.
2. **MOD-230-MP-002:** Implement and verify questionnaire versions.
3. **MOD-230-MP-003:** Implement and verify answers.
4. **MOD-230-MP-004:** Implement and verify requirement briefs.
5. **MOD-230-MP-005:** Implement and verify clarification requests.
6. **MOD-230-MP-006:** Implement and verify completeness scoring.

#### Database and Backend Tasks

- **MOD-230-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **questionnaires**.
- **MOD-230-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **questionnaire versions**.
- **MOD-230-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **answers**.
- **MOD-230-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement briefs**.
- **MOD-230-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **clarification requests**.
- **MOD-230-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **completeness scoring**.
- **MOD-230-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-230-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-230-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-230-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-230-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-230-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-230-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-230-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-230-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-230-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-230-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-230-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-230-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-230-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-230-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-230-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-230-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-230-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-230-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-230-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-230-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-230-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-230-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-230-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-230-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-230-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-230-AC-001:** At least 95% of mandatory fields are answered or explicitly unavailable.
- **MOD-230-AC-002:** Unanswered mandatory items have an owner or follow-up.
- **MOD-230-AC-003:** The brief is versioned and human-approved.
- **MOD-230-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-230-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-230-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-240 — Projects, Requirements, Requirement Versions, and SRS Management

**Purpose:** Create project records and authoritative, versioned requirements and SRS baselines with unique IDs, validations, acceptance criteria, and approval history.

**Requirement Mapping:** MVP-FR-004, MVP-FR-013  
**Dependencies:** MOD-230, MOD-250, MOD-330

#### Main Points

1. **MOD-240-MP-001:** Implement and verify projects.
2. **MOD-240-MP-002:** Implement and verify requirements.
3. **MOD-240-MP-003:** Implement and verify requirement versions.
4. **MOD-240-MP-004:** Implement and verify business rules.
5. **MOD-240-MP-005:** Implement and verify acceptance criteria.
6. **MOD-240-MP-006:** Implement and verify assumptions.
7. **MOD-240-MP-007:** Implement and verify constraints.
8. **MOD-240-MP-008:** Implement and verify SRS baselines.

#### Database and Backend Tasks

- **MOD-240-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **projects**.
- **MOD-240-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirements**.
- **MOD-240-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement versions**.
- **MOD-240-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business rules**.
- **MOD-240-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acceptance criteria**.
- **MOD-240-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assumptions**.
- **MOD-240-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **constraints**.
- **MOD-240-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SRS baselines**.
- **MOD-240-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-240-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-240-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-240-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-240-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-240-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-240-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-240-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-240-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-240-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-240-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-240-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-240-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-240-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-240-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-240-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-240-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-240-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-240-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-240-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-240-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-240-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-240-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-240-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-240-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-240-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-240-AC-001:** Every approved requirement has a unique ID and acceptance criteria.
- **MOD-240-AC-002:** SRS cannot become authoritative without human approval.
- **MOD-240-AC-003:** Material changes create new versions and change control.
- **MOD-240-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-240-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-240-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-250 — Documents, Standard Templates, Versioning, and Secure File Storage

**Purpose:** Manage approved templates, document versions, classifications, storage, scanning, downloads, approvals, and AI retrieval permission.

**Requirement Mapping:** MVP-FR-010  
**Dependencies:** MOD-030, MOD-120, MOD-040

#### Main Points

1. **MOD-250-MP-001:** Implement and verify documents.
2. **MOD-250-MP-002:** Implement and verify document versions.
3. **MOD-250-MP-003:** Implement and verify templates.
4. **MOD-250-MP-004:** Implement and verify template versions.
5. **MOD-250-MP-005:** Implement and verify attachments.
6. **MOD-250-MP-006:** Implement and verify document permissions.
7. **MOD-250-MP-007:** Implement and verify scan results.

#### Database and Backend Tasks

- **MOD-250-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **documents**.
- **MOD-250-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document versions**.
- **MOD-250-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **templates**.
- **MOD-250-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **template versions**.
- **MOD-250-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachments**.
- **MOD-250-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **document permissions**.
- **MOD-250-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **scan results**.
- **MOD-250-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-250-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-250-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-250-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-250-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-250-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-250-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-250-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-250-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-250-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-250-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-250-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-250-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-250-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-250-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-250-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-250-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-250-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-250-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-250-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-250-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-250-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-250-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-250-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-250-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-250-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-250-AC-001:** Authoritative documents have version, owner, status, and effective date.
- **MOD-250-AC-002:** Unsafe files never become available or indexed.
- **MOD-250-AC-003:** Access applies to files, previews, extracted text, and embeddings.
- **MOD-250-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-250-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-250-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-260 — Project Phases, Milestones, Roadmaps, Dependencies, and Baselines

**Purpose:** Convert approved requirements into phases, milestones, deliverables, dependencies, resource needs, baselines, forecasts, and completion gates.

**Requirement Mapping:** MVP-FR-004  
**Dependencies:** MOD-240, MOD-130, MOD-330

#### Main Points

1. **MOD-260-MP-001:** Implement and verify phases.
2. **MOD-260-MP-002:** Implement and verify milestones.
3. **MOD-260-MP-003:** Implement and verify deliverables.
4. **MOD-260-MP-004:** Implement and verify phase dependencies.
5. **MOD-260-MP-005:** Implement and verify project baselines.
6. **MOD-260-MP-006:** Implement and verify forecasts.

#### Database and Backend Tasks

- **MOD-260-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **phases**.
- **MOD-260-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **milestones**.
- **MOD-260-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deliverables**.
- **MOD-260-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **phase dependencies**.
- **MOD-260-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project baselines**.
- **MOD-260-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **forecasts**.
- **MOD-260-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-260-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-260-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-260-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-260-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-260-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-260-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-260-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-260-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-260-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-260-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-260-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-260-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-260-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-260-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-260-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-260-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-260-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-260-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-260-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-260-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-260-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-260-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-260-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-260-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-260-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-260-AC-001:** Every approved requirement maps to a phase.
- **MOD-260-AC-002:** Every milestone has owner, date, status, and approval rules.
- **MOD-260-AC-003:** Multi-phase projects support independent phase completion.
- **MOD-260-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-260-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-260-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

## Phase 3 — Work Management and Agent Orchestration

### MOD-300 — Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion

**Purpose:** Create traceable work with acceptance criteria, estimates, dependencies, Definition of Ready, Definition of Done, evidence, and controlled lifecycle.

**Requirement Mapping:** MVP-FR-005, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-320

#### Main Points

1. **MOD-300-MP-001:** Implement and verify tickets.
2. **MOD-300-MP-002:** Implement and verify subtasks.
3. **MOD-300-MP-003:** Implement and verify ticket dependencies.
4. **MOD-300-MP-004:** Implement and verify requirement links.
5. **MOD-300-MP-005:** Implement and verify ticket evidence.
6. **MOD-300-MP-006:** Implement and verify readiness checks.
7. **MOD-300-MP-007:** Implement and verify done checks.

#### Database and Backend Tasks

- **MOD-300-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tickets**.
- **MOD-300-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **subtasks**.
- **MOD-300-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket dependencies**.
- **MOD-300-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement links**.
- **MOD-300-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket evidence**.
- **MOD-300-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **readiness checks**.
- **MOD-300-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **done checks**.
- **MOD-300-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-300-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-300-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-300-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-300-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-300-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-300-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-300-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-300-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-300-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-300-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-300-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-300-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-300-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-300-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-300-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-300-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-300-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-300-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-300-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-300-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-300-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-300-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-300-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-300-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-300-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-300-AC-001:** No ticket becomes Ready without required information.
- **MOD-300-AC-002:** Tickets link to project, phase, owner or queue, and requirement.
- **MOD-300-AC-003:** Done tickets reopen only with authority and evidence.
- **MOD-300-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-300-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-300-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-310 — Skill- and Capacity-Based Assignment and Ownership History

**Purpose:** Recommend and approve assignments using role, skill, proficiency, project access, capacity, working hours, dependencies, and workload.

**Requirement Mapping:** MVP-FR-005  
**Dependencies:** MOD-130, MOD-300, MOD-120

#### Main Points

1. **MOD-310-MP-001:** Implement and verify assignments.
2. **MOD-310-MP-002:** Implement and verify assignment recommendations.
3. **MOD-310-MP-003:** Implement and verify allocation history.
4. **MOD-310-MP-004:** Implement and verify acknowledgments.
5. **MOD-310-MP-005:** Implement and verify reassignment history.

#### Database and Backend Tasks

- **MOD-310-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assignments**.
- **MOD-310-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **assignment recommendations**.
- **MOD-310-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **allocation history**.
- **MOD-310-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acknowledgments**.
- **MOD-310-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reassignment history**.
- **MOD-310-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-310-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-310-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-310-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-310-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-310-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-310-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-310-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-310-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-310-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-310-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-310-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-310-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-310-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-310-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-310-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-310-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-310-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-310-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-310-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-310-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-310-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-310-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-310-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-310-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-310-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-310-AC-001:** No assignment is made to an unauthorized or unavailable actor.
- **MOD-310-AC-002:** Overrides require a reason.
- **MOD-310-AC-003:** Assignment history is immutable.
- **MOD-310-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-310-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-310-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-320 — Configurable Status and Transition Engine

**Purpose:** Execute configurable status transitions with permissions, conditions, required fields, evidence, approval, history, hold, reopen, and terminal-state rules.

**Requirement Mapping:** MVP-FR-016  
**Dependencies:** MOD-140, MOD-040

#### Main Points

1. **MOD-320-MP-001:** Implement and verify workflow resolver.
2. **MOD-320-MP-002:** Implement and verify transition evaluator.
3. **MOD-320-MP-003:** Implement and verify status history.
4. **MOD-320-MP-004:** Implement and verify hold records.
5. **MOD-320-MP-005:** Implement and verify reopen records.
6. **MOD-320-MP-006:** Implement and verify available next actions.

#### Database and Backend Tasks

- **MOD-320-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow resolver**.
- **MOD-320-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **transition evaluator**.
- **MOD-320-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status history**.
- **MOD-320-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **hold records**.
- **MOD-320-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reopen records**.
- **MOD-320-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **available next actions**.
- **MOD-320-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-320-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-320-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-320-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-320-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-320-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-320-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-320-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-320-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-320-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-320-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-320-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-320-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-320-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-320-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-320-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-320-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-320-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-320-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-320-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-320-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-320-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-320-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-320-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-320-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-320-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-320-AC-001:** No business status is hard-coded as a database enum.
- **MOD-320-AC-002:** Every transition creates history and audit.
- **MOD-320-AC-003:** Agents cannot skip required approval gates.
- **MOD-320-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-320-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-320-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-330 — Human Approval Gates, Delegation, Rejection, and Override

**Purpose:** Enforce exact-version human approval for scope, quotation, timeline, SRS, allocation exceptions, architecture, changes, production, delivery, and closure.

**Requirement Mapping:** MVP-FR-008  
**Dependencies:** MOD-120, MOD-140, MOD-320

#### Main Points

1. **MOD-330-MP-001:** Implement and verify approvals.
2. **MOD-330-MP-002:** Implement and verify approval workflows.
3. **MOD-330-MP-003:** Implement and verify approval steps.
4. **MOD-330-MP-004:** Implement and verify approval decisions.
5. **MOD-330-MP-005:** Implement and verify delegations.
6. **MOD-330-MP-006:** Implement and verify approval evidence.
7. **MOD-330-MP-007:** Implement and verify human overrides.

#### Database and Backend Tasks

- **MOD-330-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approvals**.
- **MOD-330-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval workflows**.
- **MOD-330-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval steps**.
- **MOD-330-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval decisions**.
- **MOD-330-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **delegations**.
- **MOD-330-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approval evidence**.
- **MOD-330-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **human overrides**.
- **MOD-330-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-330-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-330-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-330-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-330-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-330-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-330-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-330-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-330-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-330-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-330-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-330-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-330-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-330-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-330-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-330-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-330-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-330-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-330-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-330-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-330-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-330-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-330-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-330-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-330-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-330-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-330-AC-001:** Dependent actions remain blocked until approval.
- **MOD-330-AC-002:** Approvals bind to exact versions.
- **MOD-330-AC-003:** Agents cannot approve their own recommendations.
- **MOD-330-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-330-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-330-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-340 — Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations

**Purpose:** Track clarifications, approvals, blockers, assignments, progress requests, client responses, bug fixes, deployments, and completion in both directions.

**Requirement Mapping:** MVP-FR-007  
**Dependencies:** MOD-130, MOD-140, MOD-320, MOD-440

#### Main Points

1. **MOD-340-MP-001:** Implement and verify follow-ups.
2. **MOD-340-MP-002:** Implement and verify reminders.
3. **MOD-340-MP-003:** Implement and verify escalations.
4. **MOD-340-MP-004:** Implement and verify parent-child links.
5. **MOD-340-MP-005:** Implement and verify SLA pauses.
6. **MOD-340-MP-006:** Implement and verify business-time deadlines.
7. **MOD-340-MP-007:** Implement and verify closure evidence.

#### Database and Backend Tasks

- **MOD-340-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **follow-ups**.
- **MOD-340-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reminders**.
- **MOD-340-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **escalations**.
- **MOD-340-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **parent-child links**.
- **MOD-340-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SLA pauses**.
- **MOD-340-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **business-time deadlines**.
- **MOD-340-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **closure evidence**.
- **MOD-340-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-340-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-340-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-340-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-340-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-340-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-340-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-340-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-340-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-340-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-340-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-340-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-340-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-340-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-340-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-340-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-340-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-340-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-340-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-340-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-340-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-340-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-340-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-340-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-340-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-340-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-340-AC-001:** Every request has owner, deadline, rule version, and closure condition.
- **MOD-340-AC-002:** Overdue items trigger configured reminders and escalation.
- **MOD-340-AC-003:** Parent-child chains preserve return routing.
- **MOD-340-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-340-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-340-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-350 — Temporal Orchestrator and Durable Business Workflows

**Purpose:** Coordinate long-running query, requirement, handover, assignment, blocker, QA, reporting, change, deployment, and closure workflows with durable waits and retries.

**Requirement Mapping:** MVP-FR-006, MVP-FR-007, MVP-NFR-004  
**Dependencies:** MOD-320, MOD-330, MOD-340, MOD-040

#### Main Points

1. **MOD-350-MP-001:** Implement and verify workflow instances.
2. **MOD-350-MP-002:** Implement and verify workflow signals.
3. **MOD-350-MP-003:** Implement and verify workflow versions.
4. **MOD-350-MP-004:** Implement and verify workflow failures.
5. **MOD-350-MP-005:** Implement and verify interventions.
6. **MOD-350-MP-006:** Implement and verify 12 approved workflows.

#### Database and Backend Tasks

- **MOD-350-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow instances**.
- **MOD-350-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow signals**.
- **MOD-350-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow versions**.
- **MOD-350-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow failures**.
- **MOD-350-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **interventions**.
- **MOD-350-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **12 approved workflows**.
- **MOD-350-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-350-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-350-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-350-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-350-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-350-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-350-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-350-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-350-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-350-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-350-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-350-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-350-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-350-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-350-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-350-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-350-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-350-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-350-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-350-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-350-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-350-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-350-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-350-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-350-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-350-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-350-AC-001:** Workflows survive worker restarts.
- **MOD-350-AC-002:** Timers, retries, and duplicate signals are idempotent.
- **MOD-350-AC-003:** Workflow history does not replace PostgreSQL business state.
- **MOD-350-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-350-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-350-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-360 — LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision

**Purpose:** Implement bounded departmental agents with prompt versions, tool allowlists, minimum context, structured outputs, human review, cost, and evaluation.

**Requirement Mapping:** MVP-FR-006, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-100, MOD-120, MOD-240, MOD-350, MOD-370

#### Main Points

1. **MOD-360-MP-001:** Implement and verify agent registry.
2. **MOD-360-MP-002:** Implement and verify agent runs.
3. **MOD-360-MP-003:** Implement and verify prompt versions.
4. **MOD-360-MP-004:** Implement and verify tool policies.
5. **MOD-360-MP-005:** Implement and verify context builder.
6. **MOD-360-MP-006:** Implement and verify agent reviews.
7. **MOD-360-MP-007:** Implement and verify agent evaluations.

#### Database and Backend Tasks

- **MOD-360-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent registry**.
- **MOD-360-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent runs**.
- **MOD-360-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **prompt versions**.
- **MOD-360-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **tool policies**.
- **MOD-360-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **context builder**.
- **MOD-360-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent reviews**.
- **MOD-360-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent evaluations**.
- **MOD-360-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-360-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-360-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-360-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-360-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-360-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-360-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-360-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-360-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-360-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-360-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-360-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-360-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-360-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-360-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-360-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-360-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-360-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-360-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-360-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-360-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-360-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-360-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-360-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-360-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-360-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-360-AC-001:** Every run records model, prompt, sources, tools, output, review, and audit.
- **MOD-360-AC-002:** Agents use business APIs rather than direct database access.
- **MOD-360-AC-003:** Low-confidence or conflicting output creates human review.
- **MOD-360-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-360-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-360-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-370 — Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation

**Purpose:** Provide approved, effective, versioned, owned, permission-controlled company and project knowledge with source citations and conflict handling.

**Requirement Mapping:** MVP-FR-010, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-250, MOD-120, MOD-040

#### Main Points

1. **MOD-370-MP-001:** Implement and verify knowledge items.
2. **MOD-370-MP-002:** Implement and verify knowledge versions.
3. **MOD-370-MP-003:** Implement and verify chunks.
4. **MOD-370-MP-004:** Implement and verify embeddings.
5. **MOD-370-MP-005:** Implement and verify knowledge permissions.
6. **MOD-370-MP-006:** Implement and verify usage logs.
7. **MOD-370-MP-007:** Implement and verify knowledge conflicts.

#### Database and Backend Tasks

- **MOD-370-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge items**.
- **MOD-370-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge versions**.
- **MOD-370-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **chunks**.
- **MOD-370-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **embeddings**.
- **MOD-370-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge permissions**.
- **MOD-370-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **usage logs**.
- **MOD-370-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **knowledge conflicts**.
- **MOD-370-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-370-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-370-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-370-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-370-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-370-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-370-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-370-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-370-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-370-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-370-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-370-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-370-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-370-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-370-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-370-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-370-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-370-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-370-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-370-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-370-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-370-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-370-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-370-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-370-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-370-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-370-AC-001:** Agents cite the source and version used.
- **MOD-370-AC-002:** Project-approved knowledge outranks generic examples.
- **MOD-370-AC-003:** Unauthorized, expired, rejected, or superseded content is excluded.
- **MOD-370-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-370-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-370-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

## Phase 4 — Quality, Change, Release, and Reporting

### MOD-400 — Test Cases, Test Steps, Test Runs, Evidence, and Coverage

**Purpose:** Create requirement-linked test cases and execution records for functional, negative, boundary, validation, permission, integration, concurrency, regression, browser, and device testing.

**Requirement Mapping:** MVP-FR-009, MVP-FR-013  
**Dependencies:** MOD-240, MOD-300, MOD-360

#### Main Points

1. **MOD-400-MP-001:** Implement and verify test cases.
2. **MOD-400-MP-002:** Implement and verify test steps.
3. **MOD-400-MP-003:** Implement and verify test suites.
4. **MOD-400-MP-004:** Implement and verify test plans.
5. **MOD-400-MP-005:** Implement and verify test runs.
6. **MOD-400-MP-006:** Implement and verify test evidence.
7. **MOD-400-MP-007:** Implement and verify coverage links.

#### Database and Backend Tasks

- **MOD-400-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test cases**.
- **MOD-400-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test steps**.
- **MOD-400-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test suites**.
- **MOD-400-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test plans**.
- **MOD-400-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test runs**.
- **MOD-400-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **test evidence**.
- **MOD-400-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **coverage links**.
- **MOD-400-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-400-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-400-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-400-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-400-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-400-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-400-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-400-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-400-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-400-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-400-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-400-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-400-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-400-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-400-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-400-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-400-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-400-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-400-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-400-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-400-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-400-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-400-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-400-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-400-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-400-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-400-AC-001:** Every Must-Have requirement has approved test coverage.
- **MOD-400-AC-002:** Critical permissions have negative tests.
- **MOD-400-AC-003:** Test evidence is tied to environment and build.
- **MOD-400-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-400-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-400-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-410 — Bug Lifecycle, QA Rejection, Development Reopen, and Retesting

**Purpose:** Allow QA to reject work, create defects, route fixes, reopen tickets, retest, and prevent release while blocking defects remain.

**Requirement Mapping:** MVP-FR-009  
**Dependencies:** MOD-300, MOD-320, MOD-340, MOD-400

#### Main Points

1. **MOD-410-MP-001:** Implement and verify bugs.
2. **MOD-410-MP-002:** Implement and verify bug links.
3. **MOD-410-MP-003:** Implement and verify bug assignments.
4. **MOD-410-MP-004:** Implement and verify fix submissions.
5. **MOD-410-MP-005:** Implement and verify retests.
6. **MOD-410-MP-006:** Implement and verify known issue approvals.
7. **MOD-410-MP-007:** Implement and verify severity SLA.

#### Database and Backend Tasks

- **MOD-410-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **bugs**.
- **MOD-410-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **bug links**.
- **MOD-410-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **bug assignments**.
- **MOD-410-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **fix submissions**.
- **MOD-410-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **retests**.
- **MOD-410-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **known issue approvals**.
- **MOD-410-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **severity SLA**.
- **MOD-410-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-410-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-410-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-410-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-410-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-410-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-410-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-410-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-410-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-410-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-410-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-410-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-410-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-410-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-410-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-410-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-410-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-410-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-410-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-410-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-410-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-410-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-410-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-410-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-410-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-410-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-410-AC-001:** QA can reject and reopen work with evidence.
- **MOD-410-AC-002:** Blocking defects prevent release.
- **MOD-410-AC-003:** Bug history links requirement, ticket, test, fix, retest, and release.
- **MOD-410-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-410-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-410-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-420 — Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates

**Purpose:** Manage project risks and formal changes to approved scope, requirements, design, timeline, cost, resource, security, data, integration, and release plans.

**Requirement Mapping:** MVP-FR-008, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-300, MOD-330, MOD-340

#### Main Points

1. **MOD-420-MP-001:** Implement and verify risks.
2. **MOD-420-MP-002:** Implement and verify risk reviews.
3. **MOD-420-MP-003:** Implement and verify change requests.
4. **MOD-420-MP-004:** Implement and verify impact analyses.
5. **MOD-420-MP-005:** Implement and verify change approvals.
6. **MOD-420-MP-006:** Implement and verify baseline updates.

#### Database and Backend Tasks

- **MOD-420-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **risks**.
- **MOD-420-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **risk reviews**.
- **MOD-420-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **change requests**.
- **MOD-420-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **impact analyses**.
- **MOD-420-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **change approvals**.
- **MOD-420-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **baseline updates**.
- **MOD-420-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-420-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-420-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-420-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-420-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-420-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-420-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-420-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-420-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-420-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-420-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-420-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-420-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-420-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-420-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-420-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-420-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-420-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-420-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-420-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-420-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-420-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-420-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-420-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-420-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-420-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-420-AC-001:** Out-of-scope work cannot silently enter development.
- **MOD-420-AC-002:** Approved changes update affected versions and tickets.
- **MOD-420-AC-003:** Rejected and deferred changes preserve evidence and rationale.
- **MOD-420-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-420-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-420-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-430 — Releases, Deployment Requests, Production Approval, Rollback, and Closure

**Purpose:** Package release items, enforce quality and human release gates, record deployment, smoke tests, rollback, client delivery, and closure.

**Requirement Mapping:** MVP-FR-008, MVP-FR-009  
**Dependencies:** MOD-330, MOD-400, MOD-410, MOD-420, MOD-350

#### Main Points

1. **MOD-430-MP-001:** Implement and verify releases.
2. **MOD-430-MP-002:** Implement and verify release items.
3. **MOD-430-MP-003:** Implement and verify deployments.
4. **MOD-430-MP-004:** Implement and verify deployment checks.
5. **MOD-430-MP-005:** Implement and verify backup confirmations.
6. **MOD-430-MP-006:** Implement and verify migration plans.
7. **MOD-430-MP-007:** Implement and verify rollbacks.
8. **MOD-430-MP-008:** Implement and verify completion reports.

#### Database and Backend Tasks

- **MOD-430-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **releases**.
- **MOD-430-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **release items**.
- **MOD-430-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deployments**.
- **MOD-430-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deployment checks**.
- **MOD-430-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **backup confirmations**.
- **MOD-430-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **migration plans**.
- **MOD-430-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **rollbacks**.
- **MOD-430-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **completion reports**.
- **MOD-430-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-430-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-430-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-430-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-430-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-430-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-430-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-430-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-430-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-430-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-430-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-430-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-430-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-430-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-430-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-430-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-430-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-430-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-430-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-430-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-430-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-430-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-430-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-430-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-430-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-430-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-430-AC-001:** Production cannot start without evidence and approval.
- **MOD-430-AC-002:** Releases trace to requirements, tickets, tests, bugs, changes, and documents.
- **MOD-430-AC-003:** Closure requires client and internal acceptance.
- **MOD-430-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-430-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-430-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-440 — Notifications, Preferences, Digests, Delivery, and Failure Handling

**Purpose:** Deliver permission-safe in-app and email notifications for assignments, reminders, escalations, approvals, blockers, bugs, releases, client responses, and system alerts.

**Requirement Mapping:** MVP-FR-011  
**Dependencies:** MOD-100, MOD-130, MOD-040

#### Main Points

1. **MOD-440-MP-001:** Implement and verify notifications.
2. **MOD-440-MP-002:** Implement and verify preferences.
3. **MOD-440-MP-003:** Implement and verify templates.
4. **MOD-440-MP-004:** Implement and verify deliveries.
5. **MOD-440-MP-005:** Implement and verify retries.
6. **MOD-440-MP-006:** Implement and verify dead letters.
7. **MOD-440-MP-007:** Implement and verify digests.

#### Database and Backend Tasks

- **MOD-440-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **notifications**.
- **MOD-440-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **preferences**.
- **MOD-440-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **templates**.
- **MOD-440-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deliveries**.
- **MOD-440-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **retries**.
- **MOD-440-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **dead letters**.
- **MOD-440-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **digests**.
- **MOD-440-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-440-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-440-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-440-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-440-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-440-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-440-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-440-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-440-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-440-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-440-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-440-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-440-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-440-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-440-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-440-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-440-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-440-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-440-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-440-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-440-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-440-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-440-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-440-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-440-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-440-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-440-AC-001:** Notifications are timely, idempotent, auditable, and permission-safe.
- **MOD-440-AC-002:** Users can configure preferences without disabling mandatory critical alerts.
- **MOD-440-AC-003:** Delivery failures are visible and recoverable.
- **MOD-440-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-440-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-440-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-450 — Dashboard, Reporting, Search, Project Health, and Activity Timeline

**Purpose:** Provide role-aware deterministic dashboards for queries, projects, phases, tickets, workload, follow-ups, approvals, quality, milestones, agent actions, and overrides.

**Requirement Mapping:** MVP-FR-012, MVP-FR-013, MVP-NFR-003  
**Dependencies:** MOD-210, MOD-240, MOD-300, MOD-340, MOD-330, MOD-400, MOD-410, MOD-040

#### Main Points

1. **MOD-450-MP-001:** Implement and verify dashboard read models.
2. **MOD-450-MP-002:** Implement and verify project health.
3. **MOD-450-MP-003:** Implement and verify saved filters.
4. **MOD-450-MP-004:** Implement and verify global search.
5. **MOD-450-MP-005:** Implement and verify activity timeline.
6. **MOD-450-MP-006:** Implement and verify reports.
7. **MOD-450-MP-007:** Implement and verify exports.

#### Database and Backend Tasks

- **MOD-450-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **dashboard read models**.
- **MOD-450-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project health**.
- **MOD-450-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **saved filters**.
- **MOD-450-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **global search**.
- **MOD-450-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **activity timeline**.
- **MOD-450-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **reports**.
- **MOD-450-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **exports**.
- **MOD-450-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-450-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-450-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-450-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-450-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-450-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-450-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-450-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-450-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-450-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-450-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-450-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-450-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-450-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-450-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-450-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-450-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-450-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-450-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-450-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-450-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-450-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-450-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-450-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-450-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-450-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-450-AC-001:** Dashboard values reconcile with source records.
- **MOD-450-AC-002:** Normal updates appear within one minute.
- **MOD-450-AC-003:** Counts, search, and exports do not leak unauthorized data.
- **MOD-450-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-450-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-450-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-460 — Requirement Traceability, Audit Reports, and Evidence Exports

**Purpose:** Provide end-to-end traceability from requirement version through phase, story, ticket, test, bug, change, release, approval, and delivery evidence.

**Requirement Mapping:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-040, MOD-240, MOD-300, MOD-400, MOD-410, MOD-430

#### Main Points

1. **MOD-460-MP-001:** Implement and verify requirement-ticket links.
2. **MOD-460-MP-002:** Implement and verify requirement-test links.
3. **MOD-460-MP-003:** Implement and verify requirement-release links.
4. **MOD-460-MP-004:** Implement and verify requirement-document links.
5. **MOD-460-MP-005:** Implement and verify ticket-test links.
6. **MOD-460-MP-006:** Implement and verify evidence manifests.

#### Database and Backend Tasks

- **MOD-460-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-ticket links**.
- **MOD-460-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-test links**.
- **MOD-460-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-release links**.
- **MOD-460-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **requirement-document links**.
- **MOD-460-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **ticket-test links**.
- **MOD-460-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **evidence manifests**.
- **MOD-460-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-460-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-460-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-460-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-460-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-460-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-460-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-460-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-460-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-460-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-460-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-460-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-460-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-460-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-460-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-460-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-460-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-460-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-460-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-460-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-460-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-460-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-460-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-460-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-460-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-460-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-460-AC-001:** At least 95% of Must-Have requirements have complete traceability before release.
- **MOD-460-AC-002:** Controlled actions have 100% audit coverage.
- **MOD-460-AC-003:** Exports are permission-controlled and independently reconcilable.
- **MOD-460-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-460-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-460-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

## Phase 5 — MVP Integrations

### MOD-500 — Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State

**Purpose:** Create a provider-based integration foundation with OAuth, secure token references, webhook validation, idempotency, rate limits, retries, dead letters, and sync audit.

**Requirement Mapping:** MVP-FR-014, MVP-FR-015, MVP-NFR-004  
**Dependencies:** MOD-030, MOD-040, MOD-120

#### Main Points

1. **MOD-500-MP-001:** Implement and verify integration connections.
2. **MOD-500-MP-002:** Implement and verify webhook events.
3. **MOD-500-MP-003:** Implement and verify sync cursors.
4. **MOD-500-MP-004:** Implement and verify external mappings.
5. **MOD-500-MP-005:** Implement and verify outbox events.
6. **MOD-500-MP-006:** Implement and verify inbox events.
7. **MOD-500-MP-007:** Implement and verify connection health.

#### Database and Backend Tasks

- **MOD-500-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **integration connections**.
- **MOD-500-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **webhook events**.
- **MOD-500-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **sync cursors**.
- **MOD-500-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **external mappings**.
- **MOD-500-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **outbox events**.
- **MOD-500-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **inbox events**.
- **MOD-500-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **connection health**.
- **MOD-500-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-500-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-500-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-500-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-500-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-500-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-500-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-500-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-500-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-500-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-500-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-500-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-500-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-500-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-500-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-500-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-500-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-500-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-500-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-500-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-500-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-500-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-500-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-500-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-500-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-500-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-500-AC-001:** Integration failure cannot corrupt internal data.
- **MOD-500-AC-002:** External mappings and events are tenant-scoped and audited.
- **MOD-500-AC-003:** Credentials never appear in logs, prompts, tickets, or business tables.
- **MOD-500-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-500-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-500-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-510 — Gmail Client Communication Integration

**Purpose:** Receive approved mailbox inquiries, preserve threads and attachments, detect replies, create or update queries, prepare drafts, and send approved email.

**Requirement Mapping:** MVP-FR-014  
**Dependencies:** MOD-220, MOD-500, MOD-210, MOD-230

#### Main Points

1. **MOD-510-MP-001:** Implement and verify Gmail connection.
2. **MOD-510-MP-002:** Implement and verify history cursor.
3. **MOD-510-MP-003:** Implement and verify thread mappings.
4. **MOD-510-MP-004:** Implement and verify message mappings.
5. **MOD-510-MP-005:** Implement and verify attachment import.
6. **MOD-510-MP-006:** Implement and verify draft review.
7. **MOD-510-MP-007:** Implement and verify approved send.

#### Database and Backend Tasks

- **MOD-510-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **Gmail connection**.
- **MOD-510-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **history cursor**.
- **MOD-510-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **thread mappings**.
- **MOD-510-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **message mappings**.
- **MOD-510-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **attachment import**.
- **MOD-510-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **draft review**.
- **MOD-510-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **approved send**.
- **MOD-510-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-510-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-510-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-510-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-510-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-510-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-510-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-510-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-510-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-510-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-510-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-510-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-510-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-510-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-510-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-510-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-510-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-510-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-510-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-510-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-510-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-510-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-510-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-510-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-510-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-510-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-510-AC-001:** Valid emails create or update exactly one query and thread.
- **MOD-510-AC-002:** Approved outgoing email is sent and linked correctly.
- **MOD-510-AC-003:** Duplicate notifications do not duplicate records.
- **MOD-510-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-510-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-510-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-520 — Jira Work Management Integration

**Purpose:** Create approved Jira issues, map fields and status, synchronize allowed updates, and process webhooks without bypassing internal rules.

**Requirement Mapping:** MVP-FR-015  
**Dependencies:** MOD-300, MOD-310, MOD-320, MOD-500

#### Main Points

1. **MOD-520-MP-001:** Implement and verify Jira connection.
2. **MOD-520-MP-002:** Implement and verify project mapping.
3. **MOD-520-MP-003:** Implement and verify field mapping.
4. **MOD-520-MP-004:** Implement and verify status mapping.
5. **MOD-520-MP-005:** Implement and verify issue mapping.
6. **MOD-520-MP-006:** Implement and verify comment sync.
7. **MOD-520-MP-007:** Implement and verify conflict handling.

#### Database and Backend Tasks

- **MOD-520-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **Jira connection**.
- **MOD-520-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **project mapping**.
- **MOD-520-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **field mapping**.
- **MOD-520-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **status mapping**.
- **MOD-520-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **issue mapping**.
- **MOD-520-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **comment sync**.
- **MOD-520-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **conflict handling**.
- **MOD-520-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-520-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-520-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-520-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-520-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-520-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-520-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-520-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-520-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-520-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-520-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-520-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-520-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-520-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-520-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-520-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-520-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-520-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-520-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-520-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-520-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-520-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-520-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-520-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-520-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-520-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-520-AC-001:** Approved internal tickets create Jira issues and retain keys.
- **MOD-520-AC-002:** Jira cannot bypass internal transition or approval rules.
- **MOD-520-AC-003:** Sync failures are visible, retriable, and audited.
- **MOD-520-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-520-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-520-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

## Phase 6 — Security, Reliability, Pilot, and Production Readiness

### MOD-600 — Security, Privacy, PII, File Safety, Retention, Backup, and Recovery Hardening

**Purpose:** Complete threat modeling, PII controls, retention, deletion, legal hold, backup, restore, incident response, file safety, and model-data restrictions.

**Requirement Mapping:** MVP-NFR-001, MVP-NFR-002, MVP-NFR-007, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** All functional foundation modules

#### Main Points

1. **MOD-600-MP-001:** Implement and verify threat model.
2. **MOD-600-MP-002:** Implement and verify PII inventory.
3. **MOD-600-MP-003:** Implement and verify retention policies.
4. **MOD-600-MP-004:** Implement and verify legal holds.
5. **MOD-600-MP-005:** Implement and verify deletion jobs.
6. **MOD-600-MP-006:** Implement and verify backup records.
7. **MOD-600-MP-007:** Implement and verify restore tests.
8. **MOD-600-MP-008:** Implement and verify security incidents.

#### Database and Backend Tasks

- **MOD-600-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **threat model**.
- **MOD-600-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **PII inventory**.
- **MOD-600-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **retention policies**.
- **MOD-600-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **legal holds**.
- **MOD-600-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **deletion jobs**.
- **MOD-600-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **backup records**.
- **MOD-600-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **restore tests**.
- **MOD-600-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **security incidents**.
- **MOD-600-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-600-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-600-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-600-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-600-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-600-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-600-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-600-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-600-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-600-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-600-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-600-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-600-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-600-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-600-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-600-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-600-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-600-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-600-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-600-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-600-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-600-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-600-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-600-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-600-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-600-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-600-AC-001:** No Critical security or isolation defect remains.
- **MOD-600-AC-002:** RPO and RTO targets are validated.
- **MOD-600-AC-003:** Client and company data are excluded from model training by default.
- **MOD-600-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-600-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-600-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-610 — Performance, Reliability, Idempotency, Resilience, and Disaster Recovery

**Purpose:** Validate API, dashboard, workflow, event, integration, storage, and database performance and recovery under pilot load and failure conditions.

**Requirement Mapping:** MVP-NFR-003, MVP-NFR-004, MVP-NFR-006, MVP-NFR-007  
**Dependencies:** MOD-350, MOD-440, MOD-500, MOD-600

#### Main Points

1. **MOD-610-MP-001:** Implement and verify performance tests.
2. **MOD-610-MP-002:** Implement and verify resilience tests.
3. **MOD-610-MP-003:** Implement and verify index review.
4. **MOD-610-MP-004:** Implement and verify SLO dashboards.
5. **MOD-610-MP-005:** Implement and verify workflow replay.
6. **MOD-610-MP-006:** Implement and verify integration failure tests.
7. **MOD-610-MP-007:** Implement and verify DR runbook.

#### Database and Backend Tasks

- **MOD-610-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **performance tests**.
- **MOD-610-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **resilience tests**.
- **MOD-610-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **index review**.
- **MOD-610-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **SLO dashboards**.
- **MOD-610-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **workflow replay**.
- **MOD-610-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **integration failure tests**.
- **MOD-610-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **DR runbook**.
- **MOD-610-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-610-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-610-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-610-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-610-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-610-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-610-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-610-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-610-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-610-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-610-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-610-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-610-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-610-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-610-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-610-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-610-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-610-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-610-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-610-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-610-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-610-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-610-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-610-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-610-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-610-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-610-AC-001:** 95% of normal APIs are under two seconds.
- **MOD-610-AC-002:** Dashboard is under three seconds at pilot load.
- **MOD-610-AC-003:** Durable workflows resume after failure and remain idempotent.
- **MOD-610-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-610-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-610-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-620 — Synthetic Sample Projects, Agent Evaluation, End-to-End Acceptance, and UAT

**Purpose:** Use the three synthetic projects to verify agent decisions, workflow routing, approvals, security, QA loops, integrations, dashboards, and traceability.

**Requirement Mapping:** MVP Acceptance Criteria, Sample Projects  
**Dependencies:** All MVP functional modules

#### Main Points

1. **MOD-620-MP-001:** Implement and verify seed scripts.
2. **MOD-620-MP-002:** Implement and verify expected decisions.
3. **MOD-620-MP-003:** Implement and verify agent evaluations.
4. **MOD-620-MP-004:** Implement and verify E2E tests.
5. **MOD-620-MP-005:** Implement and verify role-based UAT.
6. **MOD-620-MP-006:** Implement and verify acceptance evidence.

#### Database and Backend Tasks

- **MOD-620-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **seed scripts**.
- **MOD-620-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **expected decisions**.
- **MOD-620-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **agent evaluations**.
- **MOD-620-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **E2E tests**.
- **MOD-620-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **role-based UAT**.
- **MOD-620-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **acceptance evidence**.
- **MOD-620-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-620-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-620-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-620-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-620-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-620-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-620-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-620-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-620-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-620-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-620-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-620-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-620-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-620-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-620-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-620-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-620-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-620-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-620-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-620-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-620-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-620-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-620-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-620-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-620-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-620-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-620-AC-001:** All three sample projects pass defined workflows.
- **MOD-620-AC-002:** Agent quality metrics meet targets.
- **MOD-620-AC-003:** No unauthorized agent approval or isolation failure occurs.
- **MOD-620-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-620-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-620-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

### MOD-630 — Controlled Pilot, Production Release, Operations, and Final MVP Sign-Off

**Purpose:** Run the controlled pilot, resolve critical issues, deploy with approvals, monitor, train users, document limitations, and obtain formal sign-off.

**Requirement Mapping:** MVP Exit Criteria, Final Acceptance Sign-Off  
**Dependencies:** MOD-600, MOD-610, MOD-620

#### Main Points

1. **MOD-630-MP-001:** Implement and verify pilot plan.
2. **MOD-630-MP-002:** Implement and verify pilot users.
3. **MOD-630-MP-003:** Implement and verify training.
4. **MOD-630-MP-004:** Implement and verify support readiness.
5. **MOD-630-MP-005:** Implement and verify known limitations.
6. **MOD-630-MP-006:** Implement and verify production deployment.
7. **MOD-630-MP-007:** Implement and verify rollback.
8. **MOD-630-MP-008:** Implement and verify final sign-offs.

#### Database and Backend Tasks

- **MOD-630-DB-001:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **pilot plan**.
- **MOD-630-DB-002:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **pilot users**.
- **MOD-630-DB-003:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **training**.
- **MOD-630-DB-004:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **support readiness**.
- **MOD-630-DB-005:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **known limitations**.
- **MOD-630-DB-006:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **production deployment**.
- **MOD-630-DB-007:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **rollback**.
- **MOD-630-DB-008:** Define the data model, ownership, tenant/project scope, constraints, indexes, versioning, retention, RLS, audit, and migration behavior for **final sign-offs**.
- **MOD-630-BE-001:** Implement typed domain models, commands, queries, repositories, and application services for the approved scope.
- **MOD-630-BE-002:** Enforce authorization, approval, status-transition, concurrency, and idempotency rules before mutation.
- **MOD-630-BE-003:** Publish domain events through the transactionally safe outbox when asynchronous processing is required.
- **MOD-630-BE-004:** Return structured errors for validation, forbidden, not found, conflict, invalid transition, and approval required.

#### API Tasks

- **MOD-630-API-001:** Create versioned CRUD, query, transition, action, and history endpoints required by the module.
- **MOD-630-API-002:** Add pagination, filtering, sorting, bounded search, optimistic concurrency, idempotency, and standard problem-details errors.
- **MOD-630-API-003:** Document request, response, validation, authorization, conflict, approval-required, invalid-transition, and not-found examples in OpenAPI.

#### Frontend and Project View Tasks

- **MOD-630-FE-001:** Create the module list or dashboard view with role-aware columns, filters, sorting, pagination, saved views, and empty/loading/error/forbidden states.
- **MOD-630-FE-002:** Create detail view tabs for summary, ownership, status, related records, documents, messages, follow-ups, approvals, audit, and activity where applicable.
- **MOD-630-FE-003:** Create create/edit/review forms with field validation, permission-aware actions, stale-version handling, confirmation, and accessible error messages.
- **MOD-630-FE-004:** Verify responsive layout, keyboard navigation, focus order, contrast, timezone rendering, and screen-reader labels.

#### Workflow, Agent, Event, and Notification Tasks

- **MOD-630-WF-001:** Define triggers, owners, inputs, outputs, statuses, transitions, waits, reminders, escalations, approvals, evidence, and closure rules.
- **MOD-630-WF-002:** Route long-running waits and timers through Temporal; route bounded reasoning through LangGraph; keep state changes in FastAPI services.
- **MOD-630-WF-003:** Define domain events, outbox publication, idempotent consumers, correlation IDs, retries, dead-letter behavior, and replay rules.
- **MOD-630-WF-004:** Define notification recipients, channels, content classification, quiet hours, priority overrides, delivery audit, and failure handling.

#### Security, Privacy, and Audit Tasks

- **MOD-630-SEC-001:** Enforce organization, client, project, role, module, action, classification, environment, and effective-date authorization.
- **MOD-630-SEC-002:** Add tenant-isolation and project-isolation controls in application services and RLS where applicable.
- **MOD-630-SEC-003:** Minimize and redact PII, secrets, tokens, credentials, and restricted data in logs, prompts, notifications, events, exports, and errors.
- **MOD-630-SEC-004:** Create audit events for create, read-sensitive, update, delete, assignment, transition, approval, rejection, override, export, integration, and agent actions.

#### Testing and Verification Tasks

- **MOD-630-QA-001:** Add unit tests for domain rules, validation, conflicts, and invalid state.
- **MOD-630-QA-002:** Add integration and API-contract tests for transactions, persistence, errors, concurrency, and idempotency.
- **MOD-630-QA-003:** Add role-permission negative tests and tenant/project isolation tests.
- **MOD-630-QA-004:** Add workflow, agent, event, integration, file, security, or performance tests where the module uses those capabilities.
- **MOD-630-QA-005:** Run formatter, lint, type check, tests, migrations, frontend build, and relevant security or performance checks.

#### Documentation Tasks

- **MOD-630-DOC-001:** Update module README, data dictionary, API documentation, permissions, status rules, approvals, events, audit catalog, operational notes, and user guidance.
- **MOD-630-DOC-002:** Record migration, rollback, known limitations, verification commands, and evidence references.

#### Acceptance Gate

- **MOD-630-AC-001:** All Critical and High acceptance tests pass.
- **MOD-630-AC-002:** Pilot users approve controlled production use.
- **MOD-630-AC-003:** Cross-functional production readiness sign-off is complete.
- **MOD-630-AC-900:** All Critical and High defects for this module are resolved.
- **MOD-630-AC-901:** The responsible human owner reviews and approves the completion evidence.

#### One-by-One Cursor Order

1. Complete `MOD-630-DB-*`.
2. Complete `{mid}-BE-*`.
3. Complete `{mid}-API-*`.
4. Complete `{mid}-FE-*`.
5. Complete `{mid}-WF-*`.
6. Complete `{mid}-SEC-*`.
7. Complete `{mid}-QA-*`.
8. Complete documentation and acceptance evidence before starting a dependent module.

## 12. Cross-Module Release Gates

- **GATE-001:** No tenant-owned entity lacks organization scoping.
- **GATE-002:** No sensitive operation relies only on frontend permissions.
- **GATE-003:** No status change bypasses the transition engine.
- **GATE-004:** No high-risk action bypasses exact-version human approval.
- **GATE-005:** No agent writes directly to authoritative tables or receives unrestricted secrets.
- **GATE-006:** No external event is processed without validation and idempotency.
- **GATE-007:** No file becomes available or indexed before safety validation.
- **GATE-008:** No approved version is overwritten.
- **GATE-009:** No release proceeds with unresolved Critical defects or missing mandatory coverage.
- **GATE-010:** No completion claim is made without executed verification evidence.

## 13. Final MVP Sequence

1. **FINAL-001:** Confirm every module is Done or formally excluded by approved change control.
2. **FINAL-002:** Apply all migrations from an empty database and supported upgrade baseline.
3. **FINAL-003:** Run all backend and frontend checks, tests, builds, scans, and dependency checks.
4. **FINAL-004:** Run Temporal replay and failure-recovery tests.
5. **FINAL-005:** Run LangGraph golden-dataset, tool-authorization, and prompt-injection tests.
6. **FINAL-006:** Run complete tenant, project, document, file, vector, cache, search, dashboard, integration, and export isolation tests.
7. **FINAL-007:** Run the three synthetic sample projects end to end.
8. **FINAL-008:** Reconcile every Must-Have requirement with phases, tickets, tests, bugs, changes, release, and delivery evidence.
9. **FINAL-009:** Run load, resilience, backup, restore, rollback, and incident exercises.
10. **FINAL-010:** Resolve all Critical and High defects or obtain permitted approved disposition.
11. **FINAL-011:** Document known limitations, runbooks, support ownership, monitoring, and incident contacts.
12. **FINAL-012:** Obtain BD, PM, TL, QA, DevOps, Security, AI Architecture, Product, Management, and client/product-owner sign-off where applicable.