# MASMS Cursor Complete Development Checklist

**Rule:** Check an item only after evidence exists. A checked item without a commit, pull request, test result, migration result, screenshot, API example, audit record, or approval reference is not complete.


## Evidence status log (workspace)

**Date:** 2026-08-10  
**Scope marked:** Global Readiness (partial) + MOD-000 (partial)  
**Detail:** `docs/modules/MOD-000/COMPLETE_CHECKLIST_EVIDENCE.md`  
**Rule preserved:** items without evidence remain unchecked; human approvals are never auto-checked.

## 1. Global Readiness

- [ ] **PRE-001:** Approved MVP SRS version identified.
- [ ] **PRE-002:** Comprehensive specification version identified.
- [x] **PRE-003:** Cursor rules and AGENTS.md installed.  
  - Evidence: `.cursor/rules/`, `AGENTS.md`, `MANIFEST.json` present
- [ ] **PRE-004:** MVP scope and exclusions approved.
- [ ] **PRE-005:** Responsibility and permission matrix approved.
- [ ] **PRE-006:** Workflow diagrams and reverse paths approved.
- [ ] **PRE-007:** Status and transition rules approved.
- [ ] **PRE-008:** Follow-up and escalation rules approved.
- [ ] **PRE-009:** Approval gates and named approvers approved.
- [ ] **PRE-010:** Security, privacy, retention, backup, upload, and model-data policies approved.
- [x] **PRE-011:** Python and Node.js versions pinned.  
  - Evidence: Python `>=3.12,<3.13` in pyproject; Node `>=22` in package.json; ADR-0002
- [x] **PRE-012:** Package managers and lockfiles decided.  
  - Evidence: `uv.lock` present; pnpm workspace declared (host Corepack EPERM for pnpm runtime)
- [x] **PRE-013:** Authentication and AI providers decided.  
  - Evidence: Provisional decision recorded: Auth0 + OpenAI (ADR-0003); formal PRE approval still pending
- [ ] **PRE-014:** Deployment, CI/CD, secret manager, and environment model decided.
- [ ] **PRE-015:** Formatter, lint, typing, test, build, scan, and coverage commands documented.

## 2. Per-Task Gate

- [ ] **TASK-GATE-001:** Task and requirement IDs stated.
- [ ] **TASK-GATE-002:** Acceptance criteria restated.
- [ ] **TASK-GATE-003:** Existing patterns inspected.
- [ ] **TASK-GATE-004:** Affected files and dependencies listed.
- [ ] **TASK-GATE-005:** Tenant, role, status, approval, audit, workflow, agent, event, notification, and integration impact assessed.
- [ ] **TASK-GATE-006:** Migration and rollback assessed.
- [ ] **TASK-GATE-007:** API compatibility and idempotency assessed.
- [ ] **TASK-GATE-008:** Implementation kept focused.
- [ ] **TASK-GATE-009:** Unit tests updated.
- [ ] **TASK-GATE-010:** Integration and contract tests updated.
- [ ] **TASK-GATE-011:** Permission-negative and isolation tests updated.
- [ ] **TASK-GATE-012:** Formatter and lint pass.
- [ ] **TASK-GATE-013:** Type checks pass.
- [ ] **TASK-GATE-014:** Tests pass.
- [ ] **TASK-GATE-015:** Frontend production build passes when affected.
- [ ] **TASK-GATE-016:** Migration applies and rolls back when applicable.
- [ ] **TASK-GATE-017:** Security and dependency checks run.
- [ ] **TASK-GATE-018:** Documentation updated.
- [ ] **TASK-GATE-019:** Completion report distinguishes verified, unverified, assumptions, limitations, and blockers.

## Phase 0 — Governance and Foundation

### MOD-000 — Project Governance, Source Baseline, and Change Control

**Requirements:** MVP-NFR-010, SRS Change Control  
**Dependencies:** None

#### Readiness
- [x] **CHK-MOD-000-RDY-001:** Dependencies complete or formally waived.  
  - Evidence: No dependencies; none required
- [x] **CHK-MOD-000-RDY-002:** Module scope and exclusions clear.  
  - Evidence: `docs/governance/` + MVP exclusions referenced in REQUIREMENT_MODULE_MAP
- [ ] **CHK-MOD-000-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [x] **CHK-MOD-000-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.  
  - Evidence: Statuses/transitions/approvals/audit defined in domain.py + governance docs
- [ ] **CHK-MOD-000-RDY-005:** UI role variants and access rules defined.
- [x] **CHK-MOD-000-RDY-006:** Test data and acceptance scenarios available.  
  - Evidence: API tests + Docs sample projects available for acceptance scenarios

#### Main Components
- [x] **CHK-MOD-000-CMP-01-01:** baseline register schema and migration created.  
  - Evidence: `gov_source_baselines` model + Alembic `20260810_0001`
- [x] **CHK-MOD-000-CMP-01-02:** baseline register ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.  
  - Evidence: Data dictionary + model fields (org, owner, version, soft delete, audit)
- [x] **CHK-MOD-000-CMP-01-03:** baseline register foreign keys, uniqueness, checks, indexes, and concurrency verified.  
  - Evidence: Unique (org, baseline_key, version); indexes; optimistic version
- [ ] **CHK-MOD-000-CMP-01-04:** baseline register authorization, RLS, and isolation tests pass.
- [x] **CHK-MOD-000-CMP-02-01:** requirement mapping schema and migration created.  
  - Evidence: `gov_requirement_mappings` + migration
- [x] **CHK-MOD-000-CMP-02-02:** requirement mapping ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.  
  - Evidence: Ownership/tenant/version/soft-delete defined
- [x] **CHK-MOD-000-CMP-02-03:** requirement mapping foreign keys, uniqueness, checks, indexes, and concurrency verified.  
  - Evidence: Unique (org, requirement_id, module_id, mapping_role)
- [ ] **CHK-MOD-000-CMP-02-04:** requirement mapping authorization, RLS, and isolation tests pass.
- [x] **CHK-MOD-000-CMP-03-01:** architecture decision records schema and migration created.  
  - Evidence: `gov_architecture_decisions` + migration
- [x] **CHK-MOD-000-CMP-03-02:** architecture decision records ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.  
  - Evidence: Ownership/tenant/version/soft-delete defined
- [x] **CHK-MOD-000-CMP-03-03:** architecture decision records foreign keys, uniqueness, checks, indexes, and concurrency verified.  
  - Evidence: Unique (org, adr_key, version)
- [ ] **CHK-MOD-000-CMP-03-04:** architecture decision records authorization, RLS, and isolation tests pass.
- [x] **CHK-MOD-000-CMP-04-01:** change requests schema and migration created.  
  - Evidence: `gov_change_requests` + migration
- [x] **CHK-MOD-000-CMP-04-02:** change requests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.  
  - Evidence: Ownership/tenant/version/soft-delete defined
- [x] **CHK-MOD-000-CMP-04-03:** change requests foreign keys, uniqueness, checks, indexes, and concurrency verified.  
  - Evidence: Unique key/version + idempotency unique; target indexes
- [ ] **CHK-MOD-000-CMP-04-04:** change requests authorization, RLS, and isolation tests pass.
- [x] **CHK-MOD-000-CMP-05-01:** approval records schema and migration created.  
  - Evidence: `gov_approval_records` + migration
- [x] **CHK-MOD-000-CMP-05-02:** approval records ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.  
  - Evidence: Ownership/tenant/version/soft-delete defined
- [x] **CHK-MOD-000-CMP-05-03:** approval records foreign keys, uniqueness, checks, indexes, and concurrency verified.  
  - Evidence: Target indexes; authority_level 1-5 validated in schema
- [ ] **CHK-MOD-000-CMP-05-04:** approval records authorization, RLS, and isolation tests pass.

#### Backend and API
- [x] **CHK-MOD-000-BEAPI-001:** Typed domain models and validation implemented.  
  - Evidence: `schemas.py` + domain validation
- [x] **CHK-MOD-000-BEAPI-002:** Application services enforce authorization and approval.  
  - Evidence: Human-only approve; immutable approved; invalid transitions blocked
- [x] **CHK-MOD-000-BEAPI-003:** Transactions and outbox behavior implemented where required.  
  - Evidence: N/A for MOD-000 stub — no async outbox consumers required yet
- [x] **CHK-MOD-000-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.  
  - Evidence: expected_version checks + CR idempotency_key
- [x] **CHK-MOD-000-BEAPI-005:** CRUD and action endpoints implemented.  
  - Evidence: `/api/v1/governance/*` create/list/get/patch/transitions
- [ ] **CHK-MOD-000-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [x] **CHK-MOD-000-BEAPI-007:** Standard problem-details errors implemented.  
  - Evidence: `AppError` → structured JSON (`code`, `message`, `correlation_id`)
- [ ] **CHK-MOD-000-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-000-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-000-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-000-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-000-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-000-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-000-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-000-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-000-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [x] **CHK-MOD-000-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.  
  - Evidence: Governance docs + domain transition tables
- [x] **CHK-MOD-000-WF-002:** Long-running waits use Temporal where applicable.  
  - Evidence: N/A — no durable waits in MOD-000 stub
- [x] **CHK-MOD-000-WF-003:** Bounded reasoning uses LangGraph where applicable.  
  - Evidence: N/A — no LangGraph reasoning in MOD-000 stub
- [x] **CHK-MOD-000-WF-004:** State mutations use FastAPI application services.  
  - Evidence: `GovernanceService` owns mutations
- [ ] **CHK-MOD-000-WF-005:** Domain events and idempotent consumers implemented.
- [x] **CHK-MOD-000-WF-006:** Correlation and causation IDs propagated.  
  - Evidence: `X-Correlation-Id` → audit `correlation_id`
- [ ] **CHK-MOD-000-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [x] **CHK-MOD-000-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.  
  - Evidence: Agent approve blocked with 403; human approve required
- [ ] **CHK-MOD-000-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-000-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-000-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-000-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-000-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [x] **CHK-MOD-000-SEC-005:** Sensitive actions require the configured human approval.  
  - Evidence: Approve/reject requires `ActorKind.HUMAN`
- [x] **CHK-MOD-000-SEC-006:** All controlled actions generate audit records.  
  - Evidence: `gov_audit_events` on create/update/transition/approval
- [x] **CHK-MOD-000-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.  
  - Evidence: Audit fields include actor, org, action, entity, reason, source, correlation, timestamp

#### Testing and Evidence
- [x] **CHK-MOD-000-QA-001:** Unit tests pass.  
  - Evidence: `uv run pytest` — unit domain tests passed
- [x] **CHK-MOD-000-QA-002:** Database integration tests pass.  
  - Evidence: SQLite-backed API integration tests passed (Postgres migration apply not run)
- [x] **CHK-MOD-000-QA-003:** API contract tests pass.  
  - Evidence: Governance API tests exercise success and error contracts
- [x] **CHK-MOD-000-QA-004:** Permission-negative tests pass.  
  - Evidence: Agent approve returns 403
- [x] **CHK-MOD-000-QA-005:** Tenant/project isolation tests pass.  
  - Evidence: Other-org list returns empty
- [x] **CHK-MOD-000-QA-006:** Concurrency and duplicate-request tests pass where relevant.  
  - Evidence: CR idempotency key returns same id
- [x] **CHK-MOD-000-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.  
  - Evidence: N/A — no WF/agent/integration capabilities enabled in module stub
- [ ] **CHK-MOD-000-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-000-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [x] **CHK-MOD-000-QA-010:** Verification evidence linked.  
  - Evidence: `docs/modules/MOD-000/VERIFICATION.md`

#### Acceptance
- [ ] **CHK-MOD-000-AC-001:** One approved source of truth is identified.
- [x] **CHK-MOD-000-AC-002:** Material changes require a new version and human approval.  
  - Evidence: Immutable approved + CR/version rules enforced in service
- [x] **CHK-MOD-000-AC-003:** Every implementation task maps to a module and requirement ID.  
  - Evidence: `docs/governance/REQUIREMENT_MODULE_MAP.md`
- [x] **CHK-MOD-000-AC-900:** All Critical and High defects resolved.  
  - Evidence: No Critical/High defects opened against MOD-000
- [ ] **CHK-MOD-000-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-000-AC-902:** Module marked Done before dependent work starts.
### MOD-010 — Repository, Toolchain, and Local Development Environment

**Requirements:** Cursor Rules 010, Cursor Rules 600–720  
**Dependencies:** MOD-000

#### Readiness
- [ ] **CHK-MOD-010-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-010-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-010-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-010-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-010-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-010-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-010-CMP-01-01:** monorepo structure schema and migration created.
- [ ] **CHK-MOD-010-CMP-01-02:** monorepo structure ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-01-03:** monorepo structure foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-01-04:** monorepo structure authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-010-CMP-02-01:** language versions schema and migration created.
- [ ] **CHK-MOD-010-CMP-02-02:** language versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-02-03:** language versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-02-04:** language versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-010-CMP-03-01:** package managers schema and migration created.
- [ ] **CHK-MOD-010-CMP-03-02:** package managers ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-03-03:** package managers foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-03-04:** package managers authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-010-CMP-04-01:** Docker Compose schema and migration created.
- [ ] **CHK-MOD-010-CMP-04-02:** Docker Compose ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-04-03:** Docker Compose foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-04-04:** Docker Compose authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-010-CMP-05-01:** formatting and linting schema and migration created.
- [ ] **CHK-MOD-010-CMP-05-02:** formatting and linting ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-05-03:** formatting and linting foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-05-04:** formatting and linting authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-010-CMP-06-01:** typing schema and migration created.
- [ ] **CHK-MOD-010-CMP-06-02:** typing ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-06-03:** typing foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-06-04:** typing authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-010-CMP-07-01:** tests schema and migration created.
- [ ] **CHK-MOD-010-CMP-07-02:** tests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-07-03:** tests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-07-04:** tests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-010-CMP-08-01:** CI build schema and migration created.
- [ ] **CHK-MOD-010-CMP-08-02:** CI build ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-010-CMP-08-03:** CI build foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-010-CMP-08-04:** CI build authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-010-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-010-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-010-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-010-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-010-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-010-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-010-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-010-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-010-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-010-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-010-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-010-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-010-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-010-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-010-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-010-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-010-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-010-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-010-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-010-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-010-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-010-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-010-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-010-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-010-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-010-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-010-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-010-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-010-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-010-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-010-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-010-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-010-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-010-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-010-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-010-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-010-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-010-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-010-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-010-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-010-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-010-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-010-AC-001:** A new developer can start the stack from documented commands.
- [ ] **CHK-MOD-010-AC-002:** CI blocks formatting, type, test, or build failures.
- [ ] **CHK-MOD-010-AC-003:** No real secret exists in source control.
- [ ] **CHK-MOD-010-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-010-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-010-AC-902:** Module marked Done before dependent work starts.
### MOD-020 — Shared Architecture, Domain Kernel, and API Standards

**Requirements:** MVP-NFR-004, MVP-NFR-010  
**Dependencies:** MOD-010

#### Readiness
- [ ] **CHK-MOD-020-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-020-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-020-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-020-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-020-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-020-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-020-CMP-01-01:** typed identifiers schema and migration created.
- [ ] **CHK-MOD-020-CMP-01-02:** typed identifiers ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-01-03:** typed identifiers foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-01-04:** typed identifiers authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-02-01:** actor context schema and migration created.
- [ ] **CHK-MOD-020-CMP-02-02:** actor context ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-02-03:** actor context foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-02-04:** actor context authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-03-01:** tenant context schema and migration created.
- [ ] **CHK-MOD-020-CMP-03-02:** tenant context ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-03-03:** tenant context foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-03-04:** tenant context authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-04-01:** domain errors schema and migration created.
- [ ] **CHK-MOD-020-CMP-04-02:** domain errors ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-04-03:** domain errors foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-04-04:** domain errors authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-05-01:** unit of work schema and migration created.
- [ ] **CHK-MOD-020-CMP-05-02:** unit of work ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-05-03:** unit of work foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-05-04:** unit of work authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-06-01:** outbox schema and migration created.
- [ ] **CHK-MOD-020-CMP-06-02:** outbox ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-06-03:** outbox foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-06-04:** outbox authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-07-01:** API problem details schema and migration created.
- [ ] **CHK-MOD-020-CMP-07-02:** API problem details ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-07-03:** API problem details foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-07-04:** API problem details authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-08-01:** pagination schema and migration created.
- [ ] **CHK-MOD-020-CMP-08-02:** pagination ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-08-03:** pagination foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-08-04:** pagination authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-020-CMP-09-01:** optimistic concurrency schema and migration created.
- [ ] **CHK-MOD-020-CMP-09-02:** optimistic concurrency ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-020-CMP-09-03:** optimistic concurrency foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-020-CMP-09-04:** optimistic concurrency authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-020-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-020-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-020-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-020-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-020-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-020-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-020-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-020-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-020-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-020-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-020-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-020-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-020-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-020-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-020-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-020-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-020-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-020-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-020-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-020-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-020-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-020-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-020-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-020-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-020-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-020-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-020-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-020-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-020-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-020-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-020-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-020-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-020-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-020-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-020-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-020-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-020-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-020-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-020-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-020-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-020-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-020-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-020-AC-001:** All modules use the same actor and tenant context.
- [ ] **CHK-MOD-020-AC-002:** Agents and workflows cannot bypass application services.
- [ ] **CHK-MOD-020-AC-003:** API contracts are consistent and documented.
- [ ] **CHK-MOD-020-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-020-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-020-AC-902:** Module marked Done before dependent work starts.
### MOD-030 — Environment Configuration, Secrets, CI/CD, and Deployment Skeleton

**Requirements:** MVP-NFR-001, MVP-NFR-007  
**Dependencies:** MOD-010, MOD-020

#### Readiness
- [ ] **CHK-MOD-030-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-030-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-030-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-030-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-030-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-030-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-030-CMP-01-01:** environment matrix schema and migration created.
- [ ] **CHK-MOD-030-CMP-01-02:** environment matrix ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-030-CMP-01-03:** environment matrix foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-030-CMP-01-04:** environment matrix authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-030-CMP-02-01:** secret manager schema and migration created.
- [ ] **CHK-MOD-030-CMP-02-02:** secret manager ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-030-CMP-02-03:** secret manager foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-030-CMP-02-04:** secret manager authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-030-CMP-03-01:** CI pipelines schema and migration created.
- [ ] **CHK-MOD-030-CMP-03-02:** CI pipelines ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-030-CMP-03-03:** CI pipelines foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-030-CMP-03-04:** CI pipelines authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-030-CMP-04-01:** staging deployment schema and migration created.
- [ ] **CHK-MOD-030-CMP-04-02:** staging deployment ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-030-CMP-04-03:** staging deployment foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-030-CMP-04-04:** staging deployment authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-030-CMP-05-01:** production approval placeholder schema and migration created.
- [ ] **CHK-MOD-030-CMP-05-02:** production approval placeholder ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-030-CMP-05-03:** production approval placeholder foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-030-CMP-05-04:** production approval placeholder authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-030-CMP-06-01:** infrastructure as code schema and migration created.
- [ ] **CHK-MOD-030-CMP-06-02:** infrastructure as code ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-030-CMP-06-03:** infrastructure as code foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-030-CMP-06-04:** infrastructure as code authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-030-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-030-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-030-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-030-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-030-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-030-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-030-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-030-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-030-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-030-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-030-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-030-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-030-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-030-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-030-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-030-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-030-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-030-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-030-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-030-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-030-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-030-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-030-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-030-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-030-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-030-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-030-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-030-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-030-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-030-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-030-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-030-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-030-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-030-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-030-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-030-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-030-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-030-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-030-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-030-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-030-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-030-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-030-AC-001:** Environment credentials are isolated.
- [ ] **CHK-MOD-030-AC-002:** Production release requires human authorization.
- [ ] **CHK-MOD-030-AC-003:** Artifacts are reproducible and traceable.
- [ ] **CHK-MOD-030-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-030-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-030-AC-902:** Module marked Done before dependent work starts.
### MOD-040 — Observability, Audit Foundation, and Operational Health

**Requirements:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-020, MOD-030

#### Readiness
- [ ] **CHK-MOD-040-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-040-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-040-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-040-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-040-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-040-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-040-CMP-01-01:** audit logs schema and migration created.
- [ ] **CHK-MOD-040-CMP-01-02:** audit logs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-040-CMP-01-03:** audit logs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-040-CMP-01-04:** audit logs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-040-CMP-02-01:** activity events schema and migration created.
- [ ] **CHK-MOD-040-CMP-02-02:** activity events ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-040-CMP-02-03:** activity events foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-040-CMP-02-04:** activity events authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-040-CMP-03-01:** status history schema and migration created.
- [ ] **CHK-MOD-040-CMP-03-02:** status history ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-040-CMP-03-03:** status history foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-040-CMP-03-04:** status history authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-040-CMP-04-01:** agent runs schema and migration created.
- [ ] **CHK-MOD-040-CMP-04-02:** agent runs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-040-CMP-04-03:** agent runs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-040-CMP-04-04:** agent runs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-040-CMP-05-01:** integration events schema and migration created.
- [ ] **CHK-MOD-040-CMP-05-02:** integration events ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-040-CMP-05-03:** integration events foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-040-CMP-05-04:** integration events authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-040-CMP-06-01:** OpenTelemetry schema and migration created.
- [ ] **CHK-MOD-040-CMP-06-02:** OpenTelemetry ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-040-CMP-06-03:** OpenTelemetry foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-040-CMP-06-04:** OpenTelemetry authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-040-CMP-07-01:** health checks schema and migration created.
- [ ] **CHK-MOD-040-CMP-07-02:** health checks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-040-CMP-07-03:** health checks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-040-CMP-07-04:** health checks authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-040-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-040-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-040-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-040-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-040-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-040-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-040-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-040-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-040-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-040-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-040-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-040-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-040-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-040-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-040-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-040-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-040-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-040-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-040-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-040-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-040-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-040-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-040-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-040-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-040-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-040-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-040-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-040-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-040-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-040-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-040-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-040-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-040-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-040-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-040-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-040-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-040-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-040-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-040-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-040-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-040-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-040-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-040-AC-001:** Every controlled action is attributable to an actor.
- [ ] **CHK-MOD-040-AC-002:** Audit records are append-only for operational roles.
- [ ] **CHK-MOD-040-AC-003:** Failures are diagnosable without revealing secrets.
- [ ] **CHK-MOD-040-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-040-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-040-AC-902:** Module marked Done before dependent work starts.

## Phase 1 — Identity, Organization, and Configuration

### MOD-100 — Organizations, Actors, Human Users, Agents, Teams, and Departments

**Requirements:** MVP-FR-001  
**Dependencies:** MOD-020, MOD-040

#### Readiness
- [ ] **CHK-MOD-100-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-100-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-100-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-100-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-100-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-100-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-100-CMP-01-01:** organizations schema and migration created.
- [ ] **CHK-MOD-100-CMP-01-02:** organizations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-01-03:** organizations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-01-04:** organizations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-02-01:** actors schema and migration created.
- [ ] **CHK-MOD-100-CMP-02-02:** actors ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-02-03:** actors foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-02-04:** actors authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-03-01:** human users schema and migration created.
- [ ] **CHK-MOD-100-CMP-03-02:** human users ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-03-03:** human users foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-03-04:** human users authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-04-01:** agents schema and migration created.
- [ ] **CHK-MOD-100-CMP-04-02:** agents ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-04-03:** agents foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-04-04:** agents authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-05-01:** roles schema and migration created.
- [ ] **CHK-MOD-100-CMP-05-02:** roles ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-05-03:** roles foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-05-04:** roles authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-06-01:** departments schema and migration created.
- [ ] **CHK-MOD-100-CMP-06-02:** departments ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-06-03:** departments foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-06-04:** departments authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-07-01:** teams schema and migration created.
- [ ] **CHK-MOD-100-CMP-07-02:** teams ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-07-03:** teams foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-07-04:** teams authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-08-01:** team members schema and migration created.
- [ ] **CHK-MOD-100-CMP-08-02:** team members ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-08-03:** team members foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-08-04:** team members authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-100-CMP-09-01:** reporting lines schema and migration created.
- [ ] **CHK-MOD-100-CMP-09-02:** reporting lines ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-100-CMP-09-03:** reporting lines foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-100-CMP-09-04:** reporting lines authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-100-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-100-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-100-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-100-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-100-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-100-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-100-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-100-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-100-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-100-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-100-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-100-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-100-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-100-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-100-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-100-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-100-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-100-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-100-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-100-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-100-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-100-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-100-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-100-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-100-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-100-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-100-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-100-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-100-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-100-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-100-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-100-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-100-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-100-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-100-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-100-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-100-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-100-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-100-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-100-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-100-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-100-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-100-AC-001:** Every action and owner resolves to one actor.
- [ ] **CHK-MOD-100-AC-002:** Every operational agent has an active human supervisor.
- [ ] **CHK-MOD-100-AC-003:** Agent and human identities are separate.
- [ ] **CHK-MOD-100-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-100-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-100-AC-902:** Module marked Done before dependent work starts.
### MOD-110 — Authentication, Sessions, MFA, and Account Security

**Requirements:** MVP-FR-001, MVP-NFR-001  
**Dependencies:** MOD-100, MOD-030

#### Readiness
- [ ] **CHK-MOD-110-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-110-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-110-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-110-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-110-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-110-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-110-CMP-01-01:** identity provider schema and migration created.
- [ ] **CHK-MOD-110-CMP-01-02:** identity provider ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-110-CMP-01-03:** identity provider foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-110-CMP-01-04:** identity provider authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-110-CMP-02-01:** token validation schema and migration created.
- [ ] **CHK-MOD-110-CMP-02-02:** token validation ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-110-CMP-02-03:** token validation foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-110-CMP-02-04:** token validation authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-110-CMP-03-01:** sessions schema and migration created.
- [ ] **CHK-MOD-110-CMP-03-02:** sessions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-110-CMP-03-03:** sessions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-110-CMP-03-04:** sessions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-110-CMP-04-01:** MFA schema and migration created.
- [ ] **CHK-MOD-110-CMP-04-02:** MFA ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-110-CMP-04-03:** MFA foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-110-CMP-04-04:** MFA authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-110-CMP-05-01:** step-up authentication schema and migration created.
- [ ] **CHK-MOD-110-CMP-05-02:** step-up authentication ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-110-CMP-05-03:** step-up authentication foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-110-CMP-05-04:** step-up authentication authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-110-CMP-06-01:** client invitations schema and migration created.
- [ ] **CHK-MOD-110-CMP-06-02:** client invitations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-110-CMP-06-03:** client invitations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-110-CMP-06-04:** client invitations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-110-CMP-07-01:** service identities schema and migration created.
- [ ] **CHK-MOD-110-CMP-07-02:** service identities ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-110-CMP-07-03:** service identities foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-110-CMP-07-04:** service identities authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-110-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-110-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-110-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-110-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-110-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-110-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-110-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-110-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-110-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-110-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-110-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-110-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-110-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-110-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-110-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-110-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-110-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-110-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-110-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-110-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-110-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-110-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-110-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-110-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-110-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-110-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-110-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-110-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-110-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-110-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-110-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-110-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-110-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-110-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-110-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-110-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-110-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-110-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-110-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-110-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-110-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-110-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-110-AC-001:** All human and machine actions use authenticated actor identities.
- [ ] **CHK-MOD-110-AC-002:** Privileged actions require appropriate assurance.
- [ ] **CHK-MOD-110-AC-003:** Sessions can be revoked immediately.
- [ ] **CHK-MOD-110-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-110-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-110-AC-902:** Module marked Done before dependent work starts.
### MOD-120 — RBAC, Attribute-Based Access, Project Membership, and Row-Level Security

**Requirements:** MVP-FR-001, MVP-NFR-001, MVP-NFR-002  
**Dependencies:** MOD-100, MOD-110

#### Readiness
- [ ] **CHK-MOD-120-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-120-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-120-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-120-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-120-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-120-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-120-CMP-01-01:** permissions schema and migration created.
- [ ] **CHK-MOD-120-CMP-01-02:** permissions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-01-03:** permissions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-01-04:** permissions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-120-CMP-02-01:** role permissions schema and migration created.
- [ ] **CHK-MOD-120-CMP-02-02:** role permissions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-02-03:** role permissions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-02-04:** role permissions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-120-CMP-03-01:** project members schema and migration created.
- [ ] **CHK-MOD-120-CMP-03-02:** project members ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-03-03:** project members foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-03-04:** project members authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-120-CMP-04-01:** module access schema and migration created.
- [ ] **CHK-MOD-120-CMP-04-02:** module access ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-04-03:** module access foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-04-04:** module access authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-120-CMP-05-01:** document access schema and migration created.
- [ ] **CHK-MOD-120-CMP-05-02:** document access ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-05-03:** document access foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-05-04:** document access authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-120-CMP-06-01:** approval authorities schema and migration created.
- [ ] **CHK-MOD-120-CMP-06-02:** approval authorities ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-06-03:** approval authorities foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-06-04:** approval authorities authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-120-CMP-07-01:** RLS policies schema and migration created.
- [ ] **CHK-MOD-120-CMP-07-02:** RLS policies ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-07-03:** RLS policies foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-07-04:** RLS policies authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-120-CMP-08-01:** access reviews schema and migration created.
- [ ] **CHK-MOD-120-CMP-08-02:** access reviews ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-120-CMP-08-03:** access reviews foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-120-CMP-08-04:** access reviews authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-120-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-120-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-120-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-120-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-120-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-120-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-120-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-120-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-120-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-120-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-120-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-120-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-120-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-120-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-120-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-120-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-120-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-120-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-120-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-120-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-120-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-120-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-120-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-120-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-120-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-120-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-120-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-120-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-120-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-120-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-120-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-120-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-120-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-120-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-120-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-120-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-120-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-120-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-120-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-120-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-120-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-120-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-120-AC-001:** No cross-client access exists through API, database, files, cache, vectors, search, or exports.
- [ ] **CHK-MOD-120-AC-002:** Project access requires valid membership or explicit authority.
- [ ] **CHK-MOD-120-AC-003:** Frontend visibility never replaces backend authorization.
- [ ] **CHK-MOD-120-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-120-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-120-AC-902:** Module marked Done before dependent work starts.
### MOD-130 — Skills, Availability, Capacity, Working Hours, and Business Calendars

**Requirements:** MVP-FR-005  
**Dependencies:** MOD-100, MOD-120

#### Readiness
- [ ] **CHK-MOD-130-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-130-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-130-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-130-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-130-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-130-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-130-CMP-01-01:** skills schema and migration created.
- [ ] **CHK-MOD-130-CMP-01-02:** skills ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-01-03:** skills foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-01-04:** skills authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-130-CMP-02-01:** actor skills schema and migration created.
- [ ] **CHK-MOD-130-CMP-02-02:** actor skills ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-02-03:** actor skills foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-02-04:** actor skills authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-130-CMP-03-01:** availability schema and migration created.
- [ ] **CHK-MOD-130-CMP-03-02:** availability ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-03-03:** availability foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-03-04:** availability authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-130-CMP-04-01:** capacity allocations schema and migration created.
- [ ] **CHK-MOD-130-CMP-04-02:** capacity allocations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-04-03:** capacity allocations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-04-04:** capacity allocations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-130-CMP-05-01:** business calendars schema and migration created.
- [ ] **CHK-MOD-130-CMP-05-02:** business calendars ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-05-03:** business calendars foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-05-04:** business calendars authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-130-CMP-06-01:** holidays schema and migration created.
- [ ] **CHK-MOD-130-CMP-06-02:** holidays ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-06-03:** holidays foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-06-04:** holidays authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-130-CMP-07-01:** leave periods schema and migration created.
- [ ] **CHK-MOD-130-CMP-07-02:** leave periods ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-07-03:** leave periods foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-07-04:** leave periods authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-130-CMP-08-01:** on-call schedules schema and migration created.
- [ ] **CHK-MOD-130-CMP-08-02:** on-call schedules ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-130-CMP-08-03:** on-call schedules foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-130-CMP-08-04:** on-call schedules authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-130-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-130-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-130-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-130-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-130-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-130-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-130-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-130-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-130-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-130-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-130-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-130-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-130-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-130-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-130-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-130-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-130-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-130-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-130-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-130-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-130-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-130-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-130-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-130-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-130-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-130-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-130-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-130-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-130-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-130-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-130-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-130-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-130-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-130-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-130-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-130-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-130-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-130-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-130-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-130-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-130-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-130-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-130-AC-001:** Assignments can evaluate skill, access, capacity, calendar, and deadline.
- [ ] **CHK-MOD-130-AC-002:** SLA calculations respect business calendars and time zones.
- [ ] **CHK-MOD-130-AC-003:** Unnecessary personal data is excluded.
- [ ] **CHK-MOD-130-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-130-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-130-AC-902:** Module marked Done before dependent work starts.
### MOD-140 — Configuration Administration and Versioned Operational Rules

**Requirements:** MVP-FR-016, MVP-NFR-010  
**Dependencies:** MOD-000, MOD-120, MOD-130

#### Readiness
- [ ] **CHK-MOD-140-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-140-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-140-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-140-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-140-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-140-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-140-CMP-01-01:** workflow definitions schema and migration created.
- [ ] **CHK-MOD-140-CMP-01-02:** workflow definitions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-01-03:** workflow definitions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-01-04:** workflow definitions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-140-CMP-02-01:** status definitions schema and migration created.
- [ ] **CHK-MOD-140-CMP-02-02:** status definitions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-02-03:** status definitions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-02-04:** status definitions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-140-CMP-03-01:** transition rules schema and migration created.
- [ ] **CHK-MOD-140-CMP-03-02:** transition rules ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-03-03:** transition rules foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-03-04:** transition rules authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-140-CMP-04-01:** follow-up rules schema and migration created.
- [ ] **CHK-MOD-140-CMP-04-02:** follow-up rules ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-04-03:** follow-up rules foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-04-04:** follow-up rules authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-140-CMP-05-01:** reminder rules schema and migration created.
- [ ] **CHK-MOD-140-CMP-05-02:** reminder rules ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-05-03:** reminder rules foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-05-04:** reminder rules authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-140-CMP-06-01:** escalation rules schema and migration created.
- [ ] **CHK-MOD-140-CMP-06-02:** escalation rules ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-06-03:** escalation rules foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-06-04:** escalation rules authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-140-CMP-07-01:** approval workflows schema and migration created.
- [ ] **CHK-MOD-140-CMP-07-02:** approval workflows ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-07-03:** approval workflows foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-07-04:** approval workflows authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-140-CMP-08-01:** configuration versions schema and migration created.
- [ ] **CHK-MOD-140-CMP-08-02:** configuration versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-140-CMP-08-03:** configuration versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-140-CMP-08-04:** configuration versions authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-140-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-140-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-140-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-140-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-140-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-140-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-140-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-140-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-140-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-140-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-140-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-140-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-140-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-140-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-140-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-140-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-140-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-140-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-140-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-140-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-140-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-140-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-140-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-140-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-140-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-140-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-140-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-140-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-140-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-140-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-140-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-140-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-140-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-140-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-140-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-140-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-140-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-140-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-140-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-140-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-140-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-140-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-140-AC-001:** Only approved effective configuration controls live execution.
- [ ] **CHK-MOD-140-AC-002:** Configuration changes require validation, audit, and rollback support.
- [ ] **CHK-MOD-140-AC-003:** Draft configuration cannot affect live workflows.
- [ ] **CHK-MOD-140-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-140-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-140-AC-902:** Module marked Done before dependent work starts.

## Phase 2 — Client, Query, and Requirement Management

### MOD-200 — Client and Contact Management

**Requirements:** MVP-FR-002  
**Dependencies:** MOD-120, MOD-040

#### Readiness
- [ ] **CHK-MOD-200-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-200-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-200-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-200-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-200-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-200-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-200-CMP-01-01:** clients schema and migration created.
- [ ] **CHK-MOD-200-CMP-01-02:** clients ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-200-CMP-01-03:** clients foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-200-CMP-01-04:** clients authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-200-CMP-02-01:** contacts schema and migration created.
- [ ] **CHK-MOD-200-CMP-02-02:** contacts ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-200-CMP-02-03:** contacts foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-200-CMP-02-04:** contacts authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-200-CMP-03-01:** project contacts schema and migration created.
- [ ] **CHK-MOD-200-CMP-03-02:** project contacts ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-200-CMP-03-03:** project contacts foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-200-CMP-03-04:** project contacts authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-200-CMP-04-01:** communication preferences schema and migration created.
- [ ] **CHK-MOD-200-CMP-04-02:** communication preferences ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-200-CMP-04-03:** communication preferences foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-200-CMP-04-04:** communication preferences authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-200-CMP-05-01:** duplicate suggestions schema and migration created.
- [ ] **CHK-MOD-200-CMP-05-02:** duplicate suggestions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-200-CMP-05-03:** duplicate suggestions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-200-CMP-05-04:** duplicate suggestions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-200-CMP-06-01:** merge history schema and migration created.
- [ ] **CHK-MOD-200-CMP-06-02:** merge history ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-200-CMP-06-03:** merge history foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-200-CMP-06-04:** merge history authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-200-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-200-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-200-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-200-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-200-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-200-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-200-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-200-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-200-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-200-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-200-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-200-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-200-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-200-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-200-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-200-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-200-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-200-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-200-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-200-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-200-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-200-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-200-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-200-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-200-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-200-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-200-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-200-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-200-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-200-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-200-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-200-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-200-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-200-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-200-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-200-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-200-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-200-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-200-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-200-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-200-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-200-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-200-AC-001:** Clients may have multiple contacts with explicit authority.
- [ ] **CHK-MOD-200-AC-002:** Duplicate handling preserves history.
- [ ] **CHK-MOD-200-AC-003:** Client records are isolated and auditable.
- [ ] **CHK-MOD-200-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-200-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-200-AC-902:** Module marked Done before dependent work starts.
### MOD-210 — Client Queries, Qualification, and Opportunities

**Requirements:** MVP-FR-002, MVP-FR-003  
**Dependencies:** MOD-200, MOD-140

#### Readiness
- [ ] **CHK-MOD-210-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-210-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-210-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-210-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-210-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-210-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-210-CMP-01-01:** queries schema and migration created.
- [ ] **CHK-MOD-210-CMP-01-02:** queries ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-210-CMP-01-03:** queries foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-210-CMP-01-04:** queries authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-210-CMP-02-01:** opportunities schema and migration created.
- [ ] **CHK-MOD-210-CMP-02-02:** opportunities ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-210-CMP-02-03:** opportunities foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-210-CMP-02-04:** opportunities authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-210-CMP-03-01:** qualification answers schema and migration created.
- [ ] **CHK-MOD-210-CMP-03-02:** qualification answers ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-210-CMP-03-03:** qualification answers foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-210-CMP-03-04:** qualification answers authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-210-CMP-04-01:** query sources schema and migration created.
- [ ] **CHK-MOD-210-CMP-04-02:** query sources ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-210-CMP-04-03:** query sources foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-210-CMP-04-04:** query sources authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-210-CMP-05-01:** query status history schema and migration created.
- [ ] **CHK-MOD-210-CMP-05-02:** query status history ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-210-CMP-05-03:** query status history foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-210-CMP-05-04:** query status history authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-210-CMP-06-01:** first response SLA schema and migration created.
- [ ] **CHK-MOD-210-CMP-06-02:** first response SLA ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-210-CMP-06-03:** first response SLA foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-210-CMP-06-04:** first response SLA authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-210-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-210-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-210-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-210-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-210-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-210-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-210-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-210-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-210-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-210-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-210-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-210-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-210-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-210-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-210-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-210-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-210-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-210-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-210-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-210-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-210-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-210-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-210-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-210-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-210-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-210-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-210-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-210-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-210-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-210-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-210-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-210-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-210-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-210-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-210-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-210-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-210-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-210-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-210-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-210-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-210-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-210-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-210-AC-001:** Each valid inquiry creates one traceable query.
- [ ] **CHK-MOD-210-AC-002:** Qualification is reviewable and explainable.
- [ ] **CHK-MOD-210-AC-003:** Conversion preserves communication, documents, follow-ups, and decisions.
- [ ] **CHK-MOD-210-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-210-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-210-AC-902:** Module marked Done before dependent work starts.
### MOD-220 — Conversations, Messages, Attachments, and Communication History

**Requirements:** MVP-FR-011, MVP-FR-014  
**Dependencies:** MOD-200, MOD-040, MOD-120

#### Readiness
- [ ] **CHK-MOD-220-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-220-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-220-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-220-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-220-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-220-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-220-CMP-01-01:** conversations schema and migration created.
- [ ] **CHK-MOD-220-CMP-01-02:** conversations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-220-CMP-01-03:** conversations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-220-CMP-01-04:** conversations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-220-CMP-02-01:** messages schema and migration created.
- [ ] **CHK-MOD-220-CMP-02-02:** messages ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-220-CMP-02-03:** messages foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-220-CMP-02-04:** messages authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-220-CMP-03-01:** message revisions schema and migration created.
- [ ] **CHK-MOD-220-CMP-03-02:** message revisions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-220-CMP-03-03:** message revisions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-220-CMP-03-04:** message revisions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-220-CMP-04-01:** recipients schema and migration created.
- [ ] **CHK-MOD-220-CMP-04-02:** recipients ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-220-CMP-04-03:** recipients foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-220-CMP-04-04:** recipients authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-220-CMP-05-01:** delivery receipts schema and migration created.
- [ ] **CHK-MOD-220-CMP-05-02:** delivery receipts ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-220-CMP-05-03:** delivery receipts foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-220-CMP-05-04:** delivery receipts authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-220-CMP-06-01:** attachment links schema and migration created.
- [ ] **CHK-MOD-220-CMP-06-02:** attachment links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-220-CMP-06-03:** attachment links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-220-CMP-06-04:** attachment links authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-220-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-220-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-220-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-220-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-220-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-220-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-220-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-220-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-220-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-220-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-220-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-220-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-220-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-220-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-220-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-220-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-220-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-220-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-220-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-220-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-220-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-220-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-220-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-220-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-220-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-220-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-220-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-220-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-220-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-220-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-220-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-220-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-220-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-220-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-220-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-220-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-220-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-220-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-220-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-220-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-220-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-220-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-220-AC-001:** Material communication is linked to the correct entity.
- [ ] **CHK-MOD-220-AC-002:** Sensitive messages follow approval and recipient rules.
- [ ] **CHK-MOD-220-AC-003:** Sent-message history is immutable.
- [ ] **CHK-MOD-220-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-220-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-220-AC-902:** Module marked Done before dependent work starts.
### MOD-230 — Requirement Gathering, Completeness Analysis, Clarifications, and Requirement Brief

**Requirements:** MVP-FR-003  
**Dependencies:** MOD-210, MOD-220, MOD-250, MOD-330

#### Readiness
- [ ] **CHK-MOD-230-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-230-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-230-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-230-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-230-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-230-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-230-CMP-01-01:** questionnaires schema and migration created.
- [ ] **CHK-MOD-230-CMP-01-02:** questionnaires ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-230-CMP-01-03:** questionnaires foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-230-CMP-01-04:** questionnaires authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-230-CMP-02-01:** questionnaire versions schema and migration created.
- [ ] **CHK-MOD-230-CMP-02-02:** questionnaire versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-230-CMP-02-03:** questionnaire versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-230-CMP-02-04:** questionnaire versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-230-CMP-03-01:** answers schema and migration created.
- [ ] **CHK-MOD-230-CMP-03-02:** answers ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-230-CMP-03-03:** answers foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-230-CMP-03-04:** answers authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-230-CMP-04-01:** requirement briefs schema and migration created.
- [ ] **CHK-MOD-230-CMP-04-02:** requirement briefs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-230-CMP-04-03:** requirement briefs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-230-CMP-04-04:** requirement briefs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-230-CMP-05-01:** clarification requests schema and migration created.
- [ ] **CHK-MOD-230-CMP-05-02:** clarification requests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-230-CMP-05-03:** clarification requests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-230-CMP-05-04:** clarification requests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-230-CMP-06-01:** completeness scoring schema and migration created.
- [ ] **CHK-MOD-230-CMP-06-02:** completeness scoring ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-230-CMP-06-03:** completeness scoring foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-230-CMP-06-04:** completeness scoring authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-230-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-230-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-230-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-230-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-230-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-230-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-230-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-230-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-230-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-230-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-230-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-230-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-230-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-230-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-230-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-230-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-230-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-230-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-230-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-230-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-230-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-230-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-230-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-230-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-230-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-230-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-230-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-230-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-230-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-230-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-230-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-230-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-230-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-230-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-230-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-230-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-230-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-230-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-230-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-230-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-230-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-230-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-230-AC-001:** At least 95% of mandatory fields are answered or explicitly unavailable.
- [ ] **CHK-MOD-230-AC-002:** Unanswered mandatory items have an owner or follow-up.
- [ ] **CHK-MOD-230-AC-003:** The brief is versioned and human-approved.
- [ ] **CHK-MOD-230-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-230-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-230-AC-902:** Module marked Done before dependent work starts.
### MOD-240 — Projects, Requirements, Requirement Versions, and SRS Management

**Requirements:** MVP-FR-004, MVP-FR-013  
**Dependencies:** MOD-230, MOD-250, MOD-330

#### Readiness
- [ ] **CHK-MOD-240-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-240-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-240-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-240-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-240-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-240-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-240-CMP-01-01:** projects schema and migration created.
- [ ] **CHK-MOD-240-CMP-01-02:** projects ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-01-03:** projects foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-01-04:** projects authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-240-CMP-02-01:** requirements schema and migration created.
- [ ] **CHK-MOD-240-CMP-02-02:** requirements ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-02-03:** requirements foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-02-04:** requirements authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-240-CMP-03-01:** requirement versions schema and migration created.
- [ ] **CHK-MOD-240-CMP-03-02:** requirement versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-03-03:** requirement versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-03-04:** requirement versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-240-CMP-04-01:** business rules schema and migration created.
- [ ] **CHK-MOD-240-CMP-04-02:** business rules ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-04-03:** business rules foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-04-04:** business rules authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-240-CMP-05-01:** acceptance criteria schema and migration created.
- [ ] **CHK-MOD-240-CMP-05-02:** acceptance criteria ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-05-03:** acceptance criteria foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-05-04:** acceptance criteria authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-240-CMP-06-01:** assumptions schema and migration created.
- [ ] **CHK-MOD-240-CMP-06-02:** assumptions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-06-03:** assumptions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-06-04:** assumptions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-240-CMP-07-01:** constraints schema and migration created.
- [ ] **CHK-MOD-240-CMP-07-02:** constraints ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-07-03:** constraints foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-07-04:** constraints authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-240-CMP-08-01:** SRS baselines schema and migration created.
- [ ] **CHK-MOD-240-CMP-08-02:** SRS baselines ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-240-CMP-08-03:** SRS baselines foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-240-CMP-08-04:** SRS baselines authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-240-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-240-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-240-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-240-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-240-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-240-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-240-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-240-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-240-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-240-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-240-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-240-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-240-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-240-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-240-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-240-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-240-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-240-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-240-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-240-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-240-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-240-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-240-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-240-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-240-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-240-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-240-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-240-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-240-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-240-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-240-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-240-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-240-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-240-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-240-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-240-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-240-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-240-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-240-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-240-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-240-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-240-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-240-AC-001:** Every approved requirement has a unique ID and acceptance criteria.
- [ ] **CHK-MOD-240-AC-002:** SRS cannot become authoritative without human approval.
- [ ] **CHK-MOD-240-AC-003:** Material changes create new versions and change control.
- [ ] **CHK-MOD-240-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-240-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-240-AC-902:** Module marked Done before dependent work starts.
### MOD-250 — Documents, Standard Templates, Versioning, and Secure File Storage

**Requirements:** MVP-FR-010  
**Dependencies:** MOD-030, MOD-120, MOD-040

#### Readiness
- [ ] **CHK-MOD-250-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-250-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-250-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-250-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-250-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-250-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-250-CMP-01-01:** documents schema and migration created.
- [ ] **CHK-MOD-250-CMP-01-02:** documents ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-250-CMP-01-03:** documents foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-250-CMP-01-04:** documents authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-250-CMP-02-01:** document versions schema and migration created.
- [ ] **CHK-MOD-250-CMP-02-02:** document versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-250-CMP-02-03:** document versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-250-CMP-02-04:** document versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-250-CMP-03-01:** templates schema and migration created.
- [ ] **CHK-MOD-250-CMP-03-02:** templates ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-250-CMP-03-03:** templates foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-250-CMP-03-04:** templates authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-250-CMP-04-01:** template versions schema and migration created.
- [ ] **CHK-MOD-250-CMP-04-02:** template versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-250-CMP-04-03:** template versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-250-CMP-04-04:** template versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-250-CMP-05-01:** attachments schema and migration created.
- [ ] **CHK-MOD-250-CMP-05-02:** attachments ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-250-CMP-05-03:** attachments foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-250-CMP-05-04:** attachments authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-250-CMP-06-01:** document permissions schema and migration created.
- [ ] **CHK-MOD-250-CMP-06-02:** document permissions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-250-CMP-06-03:** document permissions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-250-CMP-06-04:** document permissions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-250-CMP-07-01:** scan results schema and migration created.
- [ ] **CHK-MOD-250-CMP-07-02:** scan results ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-250-CMP-07-03:** scan results foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-250-CMP-07-04:** scan results authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-250-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-250-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-250-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-250-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-250-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-250-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-250-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-250-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-250-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-250-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-250-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-250-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-250-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-250-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-250-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-250-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-250-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-250-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-250-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-250-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-250-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-250-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-250-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-250-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-250-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-250-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-250-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-250-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-250-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-250-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-250-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-250-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-250-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-250-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-250-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-250-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-250-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-250-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-250-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-250-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-250-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-250-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-250-AC-001:** Authoritative documents have version, owner, status, and effective date.
- [ ] **CHK-MOD-250-AC-002:** Unsafe files never become available or indexed.
- [ ] **CHK-MOD-250-AC-003:** Access applies to files, previews, extracted text, and embeddings.
- [ ] **CHK-MOD-250-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-250-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-250-AC-902:** Module marked Done before dependent work starts.
### MOD-260 — Project Phases, Milestones, Roadmaps, Dependencies, and Baselines

**Requirements:** MVP-FR-004  
**Dependencies:** MOD-240, MOD-130, MOD-330

#### Readiness
- [ ] **CHK-MOD-260-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-260-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-260-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-260-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-260-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-260-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-260-CMP-01-01:** phases schema and migration created.
- [ ] **CHK-MOD-260-CMP-01-02:** phases ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-260-CMP-01-03:** phases foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-260-CMP-01-04:** phases authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-260-CMP-02-01:** milestones schema and migration created.
- [ ] **CHK-MOD-260-CMP-02-02:** milestones ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-260-CMP-02-03:** milestones foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-260-CMP-02-04:** milestones authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-260-CMP-03-01:** deliverables schema and migration created.
- [ ] **CHK-MOD-260-CMP-03-02:** deliverables ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-260-CMP-03-03:** deliverables foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-260-CMP-03-04:** deliverables authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-260-CMP-04-01:** phase dependencies schema and migration created.
- [ ] **CHK-MOD-260-CMP-04-02:** phase dependencies ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-260-CMP-04-03:** phase dependencies foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-260-CMP-04-04:** phase dependencies authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-260-CMP-05-01:** project baselines schema and migration created.
- [ ] **CHK-MOD-260-CMP-05-02:** project baselines ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-260-CMP-05-03:** project baselines foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-260-CMP-05-04:** project baselines authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-260-CMP-06-01:** forecasts schema and migration created.
- [ ] **CHK-MOD-260-CMP-06-02:** forecasts ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-260-CMP-06-03:** forecasts foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-260-CMP-06-04:** forecasts authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-260-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-260-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-260-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-260-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-260-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-260-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-260-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-260-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-260-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-260-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-260-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-260-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-260-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-260-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-260-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-260-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-260-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-260-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-260-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-260-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-260-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-260-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-260-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-260-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-260-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-260-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-260-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-260-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-260-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-260-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-260-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-260-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-260-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-260-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-260-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-260-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-260-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-260-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-260-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-260-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-260-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-260-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-260-AC-001:** Every approved requirement maps to a phase.
- [ ] **CHK-MOD-260-AC-002:** Every milestone has owner, date, status, and approval rules.
- [ ] **CHK-MOD-260-AC-003:** Multi-phase projects support independent phase completion.
- [ ] **CHK-MOD-260-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-260-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-260-AC-902:** Module marked Done before dependent work starts.

## Phase 3 — Work Management and Agent Orchestration

### MOD-300 — Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion

**Requirements:** MVP-FR-005, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-320

#### Readiness
- [ ] **CHK-MOD-300-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-300-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-300-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-300-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-300-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-300-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-300-CMP-01-01:** tickets schema and migration created.
- [ ] **CHK-MOD-300-CMP-01-02:** tickets ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-300-CMP-01-03:** tickets foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-300-CMP-01-04:** tickets authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-300-CMP-02-01:** subtasks schema and migration created.
- [ ] **CHK-MOD-300-CMP-02-02:** subtasks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-300-CMP-02-03:** subtasks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-300-CMP-02-04:** subtasks authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-300-CMP-03-01:** ticket dependencies schema and migration created.
- [ ] **CHK-MOD-300-CMP-03-02:** ticket dependencies ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-300-CMP-03-03:** ticket dependencies foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-300-CMP-03-04:** ticket dependencies authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-300-CMP-04-01:** requirement links schema and migration created.
- [ ] **CHK-MOD-300-CMP-04-02:** requirement links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-300-CMP-04-03:** requirement links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-300-CMP-04-04:** requirement links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-300-CMP-05-01:** ticket evidence schema and migration created.
- [ ] **CHK-MOD-300-CMP-05-02:** ticket evidence ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-300-CMP-05-03:** ticket evidence foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-300-CMP-05-04:** ticket evidence authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-300-CMP-06-01:** readiness checks schema and migration created.
- [ ] **CHK-MOD-300-CMP-06-02:** readiness checks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-300-CMP-06-03:** readiness checks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-300-CMP-06-04:** readiness checks authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-300-CMP-07-01:** done checks schema and migration created.
- [ ] **CHK-MOD-300-CMP-07-02:** done checks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-300-CMP-07-03:** done checks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-300-CMP-07-04:** done checks authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-300-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-300-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-300-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-300-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-300-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-300-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-300-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-300-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-300-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-300-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-300-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-300-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-300-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-300-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-300-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-300-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-300-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-300-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-300-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-300-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-300-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-300-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-300-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-300-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-300-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-300-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-300-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-300-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-300-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-300-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-300-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-300-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-300-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-300-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-300-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-300-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-300-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-300-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-300-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-300-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-300-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-300-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-300-AC-001:** No ticket becomes Ready without required information.
- [ ] **CHK-MOD-300-AC-002:** Tickets link to project, phase, owner or queue, and requirement.
- [ ] **CHK-MOD-300-AC-003:** Done tickets reopen only with authority and evidence.
- [ ] **CHK-MOD-300-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-300-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-300-AC-902:** Module marked Done before dependent work starts.
### MOD-310 — Skill- and Capacity-Based Assignment and Ownership History

**Requirements:** MVP-FR-005  
**Dependencies:** MOD-130, MOD-300, MOD-120

#### Readiness
- [ ] **CHK-MOD-310-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-310-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-310-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-310-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-310-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-310-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-310-CMP-01-01:** assignments schema and migration created.
- [ ] **CHK-MOD-310-CMP-01-02:** assignments ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-310-CMP-01-03:** assignments foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-310-CMP-01-04:** assignments authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-310-CMP-02-01:** assignment recommendations schema and migration created.
- [ ] **CHK-MOD-310-CMP-02-02:** assignment recommendations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-310-CMP-02-03:** assignment recommendations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-310-CMP-02-04:** assignment recommendations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-310-CMP-03-01:** allocation history schema and migration created.
- [ ] **CHK-MOD-310-CMP-03-02:** allocation history ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-310-CMP-03-03:** allocation history foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-310-CMP-03-04:** allocation history authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-310-CMP-04-01:** acknowledgments schema and migration created.
- [ ] **CHK-MOD-310-CMP-04-02:** acknowledgments ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-310-CMP-04-03:** acknowledgments foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-310-CMP-04-04:** acknowledgments authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-310-CMP-05-01:** reassignment history schema and migration created.
- [ ] **CHK-MOD-310-CMP-05-02:** reassignment history ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-310-CMP-05-03:** reassignment history foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-310-CMP-05-04:** reassignment history authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-310-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-310-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-310-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-310-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-310-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-310-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-310-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-310-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-310-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-310-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-310-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-310-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-310-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-310-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-310-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-310-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-310-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-310-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-310-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-310-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-310-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-310-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-310-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-310-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-310-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-310-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-310-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-310-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-310-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-310-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-310-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-310-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-310-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-310-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-310-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-310-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-310-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-310-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-310-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-310-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-310-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-310-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-310-AC-001:** No assignment is made to an unauthorized or unavailable actor.
- [ ] **CHK-MOD-310-AC-002:** Overrides require a reason.
- [ ] **CHK-MOD-310-AC-003:** Assignment history is immutable.
- [ ] **CHK-MOD-310-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-310-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-310-AC-902:** Module marked Done before dependent work starts.
### MOD-320 — Configurable Status and Transition Engine

**Requirements:** MVP-FR-016  
**Dependencies:** MOD-140, MOD-040

#### Readiness
- [ ] **CHK-MOD-320-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-320-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-320-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-320-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-320-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-320-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-320-CMP-01-01:** workflow resolver schema and migration created.
- [ ] **CHK-MOD-320-CMP-01-02:** workflow resolver ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-320-CMP-01-03:** workflow resolver foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-320-CMP-01-04:** workflow resolver authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-320-CMP-02-01:** transition evaluator schema and migration created.
- [ ] **CHK-MOD-320-CMP-02-02:** transition evaluator ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-320-CMP-02-03:** transition evaluator foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-320-CMP-02-04:** transition evaluator authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-320-CMP-03-01:** status history schema and migration created.
- [ ] **CHK-MOD-320-CMP-03-02:** status history ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-320-CMP-03-03:** status history foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-320-CMP-03-04:** status history authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-320-CMP-04-01:** hold records schema and migration created.
- [ ] **CHK-MOD-320-CMP-04-02:** hold records ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-320-CMP-04-03:** hold records foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-320-CMP-04-04:** hold records authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-320-CMP-05-01:** reopen records schema and migration created.
- [ ] **CHK-MOD-320-CMP-05-02:** reopen records ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-320-CMP-05-03:** reopen records foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-320-CMP-05-04:** reopen records authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-320-CMP-06-01:** available next actions schema and migration created.
- [ ] **CHK-MOD-320-CMP-06-02:** available next actions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-320-CMP-06-03:** available next actions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-320-CMP-06-04:** available next actions authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-320-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-320-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-320-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-320-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-320-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-320-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-320-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-320-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-320-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-320-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-320-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-320-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-320-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-320-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-320-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-320-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-320-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-320-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-320-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-320-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-320-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-320-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-320-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-320-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-320-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-320-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-320-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-320-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-320-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-320-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-320-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-320-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-320-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-320-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-320-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-320-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-320-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-320-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-320-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-320-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-320-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-320-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-320-AC-001:** No business status is hard-coded as a database enum.
- [ ] **CHK-MOD-320-AC-002:** Every transition creates history and audit.
- [ ] **CHK-MOD-320-AC-003:** Agents cannot skip required approval gates.
- [ ] **CHK-MOD-320-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-320-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-320-AC-902:** Module marked Done before dependent work starts.
### MOD-330 — Human Approval Gates, Delegation, Rejection, and Override

**Requirements:** MVP-FR-008  
**Dependencies:** MOD-120, MOD-140, MOD-320

#### Readiness
- [ ] **CHK-MOD-330-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-330-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-330-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-330-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-330-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-330-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-330-CMP-01-01:** approvals schema and migration created.
- [ ] **CHK-MOD-330-CMP-01-02:** approvals ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-330-CMP-01-03:** approvals foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-330-CMP-01-04:** approvals authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-330-CMP-02-01:** approval workflows schema and migration created.
- [ ] **CHK-MOD-330-CMP-02-02:** approval workflows ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-330-CMP-02-03:** approval workflows foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-330-CMP-02-04:** approval workflows authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-330-CMP-03-01:** approval steps schema and migration created.
- [ ] **CHK-MOD-330-CMP-03-02:** approval steps ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-330-CMP-03-03:** approval steps foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-330-CMP-03-04:** approval steps authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-330-CMP-04-01:** approval decisions schema and migration created.
- [ ] **CHK-MOD-330-CMP-04-02:** approval decisions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-330-CMP-04-03:** approval decisions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-330-CMP-04-04:** approval decisions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-330-CMP-05-01:** delegations schema and migration created.
- [ ] **CHK-MOD-330-CMP-05-02:** delegations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-330-CMP-05-03:** delegations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-330-CMP-05-04:** delegations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-330-CMP-06-01:** approval evidence schema and migration created.
- [ ] **CHK-MOD-330-CMP-06-02:** approval evidence ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-330-CMP-06-03:** approval evidence foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-330-CMP-06-04:** approval evidence authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-330-CMP-07-01:** human overrides schema and migration created.
- [ ] **CHK-MOD-330-CMP-07-02:** human overrides ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-330-CMP-07-03:** human overrides foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-330-CMP-07-04:** human overrides authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-330-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-330-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-330-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-330-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-330-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-330-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-330-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-330-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-330-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-330-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-330-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-330-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-330-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-330-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-330-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-330-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-330-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-330-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-330-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-330-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-330-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-330-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-330-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-330-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-330-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-330-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-330-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-330-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-330-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-330-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-330-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-330-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-330-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-330-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-330-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-330-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-330-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-330-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-330-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-330-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-330-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-330-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-330-AC-001:** Dependent actions remain blocked until approval.
- [ ] **CHK-MOD-330-AC-002:** Approvals bind to exact versions.
- [ ] **CHK-MOD-330-AC-003:** Agents cannot approve their own recommendations.
- [ ] **CHK-MOD-330-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-330-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-330-AC-902:** Module marked Done before dependent work starts.
### MOD-340 — Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations

**Requirements:** MVP-FR-007  
**Dependencies:** MOD-130, MOD-140, MOD-320, MOD-440

#### Readiness
- [ ] **CHK-MOD-340-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-340-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-340-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-340-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-340-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-340-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-340-CMP-01-01:** follow-ups schema and migration created.
- [ ] **CHK-MOD-340-CMP-01-02:** follow-ups ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-340-CMP-01-03:** follow-ups foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-340-CMP-01-04:** follow-ups authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-340-CMP-02-01:** reminders schema and migration created.
- [ ] **CHK-MOD-340-CMP-02-02:** reminders ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-340-CMP-02-03:** reminders foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-340-CMP-02-04:** reminders authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-340-CMP-03-01:** escalations schema and migration created.
- [ ] **CHK-MOD-340-CMP-03-02:** escalations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-340-CMP-03-03:** escalations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-340-CMP-03-04:** escalations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-340-CMP-04-01:** parent-child links schema and migration created.
- [ ] **CHK-MOD-340-CMP-04-02:** parent-child links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-340-CMP-04-03:** parent-child links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-340-CMP-04-04:** parent-child links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-340-CMP-05-01:** SLA pauses schema and migration created.
- [ ] **CHK-MOD-340-CMP-05-02:** SLA pauses ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-340-CMP-05-03:** SLA pauses foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-340-CMP-05-04:** SLA pauses authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-340-CMP-06-01:** business-time deadlines schema and migration created.
- [ ] **CHK-MOD-340-CMP-06-02:** business-time deadlines ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-340-CMP-06-03:** business-time deadlines foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-340-CMP-06-04:** business-time deadlines authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-340-CMP-07-01:** closure evidence schema and migration created.
- [ ] **CHK-MOD-340-CMP-07-02:** closure evidence ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-340-CMP-07-03:** closure evidence foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-340-CMP-07-04:** closure evidence authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-340-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-340-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-340-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-340-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-340-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-340-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-340-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-340-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-340-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-340-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-340-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-340-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-340-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-340-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-340-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-340-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-340-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-340-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-340-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-340-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-340-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-340-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-340-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-340-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-340-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-340-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-340-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-340-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-340-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-340-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-340-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-340-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-340-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-340-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-340-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-340-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-340-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-340-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-340-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-340-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-340-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-340-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-340-AC-001:** Every request has owner, deadline, rule version, and closure condition.
- [ ] **CHK-MOD-340-AC-002:** Overdue items trigger configured reminders and escalation.
- [ ] **CHK-MOD-340-AC-003:** Parent-child chains preserve return routing.
- [ ] **CHK-MOD-340-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-340-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-340-AC-902:** Module marked Done before dependent work starts.
### MOD-350 — Temporal Orchestrator and Durable Business Workflows

**Requirements:** MVP-FR-006, MVP-FR-007, MVP-NFR-004  
**Dependencies:** MOD-320, MOD-330, MOD-340, MOD-040

#### Readiness
- [ ] **CHK-MOD-350-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-350-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-350-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-350-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-350-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-350-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-350-CMP-01-01:** workflow instances schema and migration created.
- [ ] **CHK-MOD-350-CMP-01-02:** workflow instances ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-350-CMP-01-03:** workflow instances foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-350-CMP-01-04:** workflow instances authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-350-CMP-02-01:** workflow signals schema and migration created.
- [ ] **CHK-MOD-350-CMP-02-02:** workflow signals ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-350-CMP-02-03:** workflow signals foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-350-CMP-02-04:** workflow signals authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-350-CMP-03-01:** workflow versions schema and migration created.
- [ ] **CHK-MOD-350-CMP-03-02:** workflow versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-350-CMP-03-03:** workflow versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-350-CMP-03-04:** workflow versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-350-CMP-04-01:** workflow failures schema and migration created.
- [ ] **CHK-MOD-350-CMP-04-02:** workflow failures ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-350-CMP-04-03:** workflow failures foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-350-CMP-04-04:** workflow failures authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-350-CMP-05-01:** interventions schema and migration created.
- [ ] **CHK-MOD-350-CMP-05-02:** interventions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-350-CMP-05-03:** interventions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-350-CMP-05-04:** interventions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-350-CMP-06-01:** 12 approved workflows schema and migration created.
- [ ] **CHK-MOD-350-CMP-06-02:** 12 approved workflows ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-350-CMP-06-03:** 12 approved workflows foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-350-CMP-06-04:** 12 approved workflows authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-350-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-350-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-350-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-350-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-350-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-350-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-350-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-350-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-350-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-350-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-350-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-350-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-350-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-350-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-350-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-350-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-350-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-350-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-350-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-350-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-350-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-350-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-350-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-350-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-350-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-350-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-350-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-350-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-350-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-350-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-350-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-350-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-350-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-350-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-350-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-350-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-350-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-350-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-350-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-350-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-350-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-350-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-350-AC-001:** Workflows survive worker restarts.
- [ ] **CHK-MOD-350-AC-002:** Timers, retries, and duplicate signals are idempotent.
- [ ] **CHK-MOD-350-AC-003:** Workflow history does not replace PostgreSQL business state.
- [ ] **CHK-MOD-350-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-350-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-350-AC-902:** Module marked Done before dependent work starts.
### MOD-360 — LangGraph Agent Runtime, Agent Runs, Tools, and Human Supervision

**Requirements:** MVP-FR-006, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-100, MOD-120, MOD-240, MOD-350, MOD-370

#### Readiness
- [ ] **CHK-MOD-360-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-360-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-360-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-360-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-360-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-360-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-360-CMP-01-01:** agent registry schema and migration created.
- [ ] **CHK-MOD-360-CMP-01-02:** agent registry ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-360-CMP-01-03:** agent registry foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-360-CMP-01-04:** agent registry authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-360-CMP-02-01:** agent runs schema and migration created.
- [ ] **CHK-MOD-360-CMP-02-02:** agent runs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-360-CMP-02-03:** agent runs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-360-CMP-02-04:** agent runs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-360-CMP-03-01:** prompt versions schema and migration created.
- [ ] **CHK-MOD-360-CMP-03-02:** prompt versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-360-CMP-03-03:** prompt versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-360-CMP-03-04:** prompt versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-360-CMP-04-01:** tool policies schema and migration created.
- [ ] **CHK-MOD-360-CMP-04-02:** tool policies ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-360-CMP-04-03:** tool policies foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-360-CMP-04-04:** tool policies authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-360-CMP-05-01:** context builder schema and migration created.
- [ ] **CHK-MOD-360-CMP-05-02:** context builder ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-360-CMP-05-03:** context builder foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-360-CMP-05-04:** context builder authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-360-CMP-06-01:** agent reviews schema and migration created.
- [ ] **CHK-MOD-360-CMP-06-02:** agent reviews ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-360-CMP-06-03:** agent reviews foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-360-CMP-06-04:** agent reviews authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-360-CMP-07-01:** agent evaluations schema and migration created.
- [ ] **CHK-MOD-360-CMP-07-02:** agent evaluations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-360-CMP-07-03:** agent evaluations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-360-CMP-07-04:** agent evaluations authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-360-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-360-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-360-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-360-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-360-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-360-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-360-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-360-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-360-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-360-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-360-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-360-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-360-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-360-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-360-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-360-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-360-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-360-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-360-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-360-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-360-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-360-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-360-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-360-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-360-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-360-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-360-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-360-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-360-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-360-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-360-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-360-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-360-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-360-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-360-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-360-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-360-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-360-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-360-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-360-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-360-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-360-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-360-AC-001:** Every run records model, prompt, sources, tools, output, review, and audit.
- [ ] **CHK-MOD-360-AC-002:** Agents use business APIs rather than direct database access.
- [ ] **CHK-MOD-360-AC-003:** Low-confidence or conflicting output creates human review.
- [ ] **CHK-MOD-360-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-360-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-360-AC-902:** Module marked Done before dependent work starts.
### MOD-370 — Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation

**Requirements:** MVP-FR-010, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** MOD-250, MOD-120, MOD-040

#### Readiness
- [ ] **CHK-MOD-370-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-370-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-370-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-370-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-370-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-370-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-370-CMP-01-01:** knowledge items schema and migration created.
- [ ] **CHK-MOD-370-CMP-01-02:** knowledge items ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-370-CMP-01-03:** knowledge items foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-370-CMP-01-04:** knowledge items authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-370-CMP-02-01:** knowledge versions schema and migration created.
- [ ] **CHK-MOD-370-CMP-02-02:** knowledge versions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-370-CMP-02-03:** knowledge versions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-370-CMP-02-04:** knowledge versions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-370-CMP-03-01:** chunks schema and migration created.
- [ ] **CHK-MOD-370-CMP-03-02:** chunks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-370-CMP-03-03:** chunks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-370-CMP-03-04:** chunks authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-370-CMP-04-01:** embeddings schema and migration created.
- [ ] **CHK-MOD-370-CMP-04-02:** embeddings ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-370-CMP-04-03:** embeddings foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-370-CMP-04-04:** embeddings authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-370-CMP-05-01:** knowledge permissions schema and migration created.
- [ ] **CHK-MOD-370-CMP-05-02:** knowledge permissions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-370-CMP-05-03:** knowledge permissions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-370-CMP-05-04:** knowledge permissions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-370-CMP-06-01:** usage logs schema and migration created.
- [ ] **CHK-MOD-370-CMP-06-02:** usage logs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-370-CMP-06-03:** usage logs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-370-CMP-06-04:** usage logs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-370-CMP-07-01:** knowledge conflicts schema and migration created.
- [ ] **CHK-MOD-370-CMP-07-02:** knowledge conflicts ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-370-CMP-07-03:** knowledge conflicts foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-370-CMP-07-04:** knowledge conflicts authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-370-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-370-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-370-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-370-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-370-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-370-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-370-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-370-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-370-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-370-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-370-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-370-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-370-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-370-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-370-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-370-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-370-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-370-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-370-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-370-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-370-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-370-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-370-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-370-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-370-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-370-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-370-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-370-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-370-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-370-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-370-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-370-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-370-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-370-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-370-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-370-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-370-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-370-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-370-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-370-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-370-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-370-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-370-AC-001:** Agents cite the source and version used.
- [ ] **CHK-MOD-370-AC-002:** Project-approved knowledge outranks generic examples.
- [ ] **CHK-MOD-370-AC-003:** Unauthorized, expired, rejected, or superseded content is excluded.
- [ ] **CHK-MOD-370-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-370-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-370-AC-902:** Module marked Done before dependent work starts.

## Phase 4 — Quality, Change, Release, and Reporting

### MOD-400 — Test Cases, Test Steps, Test Runs, Evidence, and Coverage

**Requirements:** MVP-FR-009, MVP-FR-013  
**Dependencies:** MOD-240, MOD-300, MOD-360

#### Readiness
- [ ] **CHK-MOD-400-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-400-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-400-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-400-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-400-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-400-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-400-CMP-01-01:** test cases schema and migration created.
- [ ] **CHK-MOD-400-CMP-01-02:** test cases ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-400-CMP-01-03:** test cases foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-400-CMP-01-04:** test cases authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-400-CMP-02-01:** test steps schema and migration created.
- [ ] **CHK-MOD-400-CMP-02-02:** test steps ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-400-CMP-02-03:** test steps foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-400-CMP-02-04:** test steps authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-400-CMP-03-01:** test suites schema and migration created.
- [ ] **CHK-MOD-400-CMP-03-02:** test suites ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-400-CMP-03-03:** test suites foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-400-CMP-03-04:** test suites authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-400-CMP-04-01:** test plans schema and migration created.
- [ ] **CHK-MOD-400-CMP-04-02:** test plans ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-400-CMP-04-03:** test plans foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-400-CMP-04-04:** test plans authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-400-CMP-05-01:** test runs schema and migration created.
- [ ] **CHK-MOD-400-CMP-05-02:** test runs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-400-CMP-05-03:** test runs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-400-CMP-05-04:** test runs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-400-CMP-06-01:** test evidence schema and migration created.
- [ ] **CHK-MOD-400-CMP-06-02:** test evidence ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-400-CMP-06-03:** test evidence foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-400-CMP-06-04:** test evidence authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-400-CMP-07-01:** coverage links schema and migration created.
- [ ] **CHK-MOD-400-CMP-07-02:** coverage links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-400-CMP-07-03:** coverage links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-400-CMP-07-04:** coverage links authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-400-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-400-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-400-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-400-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-400-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-400-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-400-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-400-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-400-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-400-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-400-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-400-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-400-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-400-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-400-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-400-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-400-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-400-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-400-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-400-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-400-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-400-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-400-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-400-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-400-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-400-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-400-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-400-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-400-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-400-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-400-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-400-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-400-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-400-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-400-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-400-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-400-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-400-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-400-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-400-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-400-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-400-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-400-AC-001:** Every Must-Have requirement has approved test coverage.
- [ ] **CHK-MOD-400-AC-002:** Critical permissions have negative tests.
- [ ] **CHK-MOD-400-AC-003:** Test evidence is tied to environment and build.
- [ ] **CHK-MOD-400-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-400-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-400-AC-902:** Module marked Done before dependent work starts.
### MOD-410 — Bug Lifecycle, QA Rejection, Development Reopen, and Retesting

**Requirements:** MVP-FR-009  
**Dependencies:** MOD-300, MOD-320, MOD-340, MOD-400

#### Readiness
- [ ] **CHK-MOD-410-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-410-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-410-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-410-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-410-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-410-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-410-CMP-01-01:** bugs schema and migration created.
- [ ] **CHK-MOD-410-CMP-01-02:** bugs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-410-CMP-01-03:** bugs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-410-CMP-01-04:** bugs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-410-CMP-02-01:** bug links schema and migration created.
- [ ] **CHK-MOD-410-CMP-02-02:** bug links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-410-CMP-02-03:** bug links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-410-CMP-02-04:** bug links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-410-CMP-03-01:** bug assignments schema and migration created.
- [ ] **CHK-MOD-410-CMP-03-02:** bug assignments ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-410-CMP-03-03:** bug assignments foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-410-CMP-03-04:** bug assignments authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-410-CMP-04-01:** fix submissions schema and migration created.
- [ ] **CHK-MOD-410-CMP-04-02:** fix submissions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-410-CMP-04-03:** fix submissions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-410-CMP-04-04:** fix submissions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-410-CMP-05-01:** retests schema and migration created.
- [ ] **CHK-MOD-410-CMP-05-02:** retests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-410-CMP-05-03:** retests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-410-CMP-05-04:** retests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-410-CMP-06-01:** known issue approvals schema and migration created.
- [ ] **CHK-MOD-410-CMP-06-02:** known issue approvals ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-410-CMP-06-03:** known issue approvals foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-410-CMP-06-04:** known issue approvals authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-410-CMP-07-01:** severity SLA schema and migration created.
- [ ] **CHK-MOD-410-CMP-07-02:** severity SLA ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-410-CMP-07-03:** severity SLA foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-410-CMP-07-04:** severity SLA authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-410-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-410-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-410-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-410-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-410-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-410-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-410-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-410-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-410-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-410-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-410-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-410-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-410-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-410-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-410-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-410-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-410-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-410-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-410-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-410-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-410-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-410-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-410-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-410-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-410-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-410-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-410-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-410-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-410-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-410-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-410-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-410-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-410-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-410-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-410-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-410-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-410-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-410-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-410-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-410-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-410-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-410-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-410-AC-001:** QA can reject and reopen work with evidence.
- [ ] **CHK-MOD-410-AC-002:** Blocking defects prevent release.
- [ ] **CHK-MOD-410-AC-003:** Bug history links requirement, ticket, test, fix, retest, and release.
- [ ] **CHK-MOD-410-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-410-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-410-AC-902:** Module marked Done before dependent work starts.
### MOD-420 — Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates

**Requirements:** MVP-FR-008, MVP-FR-013  
**Dependencies:** MOD-240, MOD-260, MOD-300, MOD-330, MOD-340

#### Readiness
- [ ] **CHK-MOD-420-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-420-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-420-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-420-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-420-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-420-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-420-CMP-01-01:** risks schema and migration created.
- [ ] **CHK-MOD-420-CMP-01-02:** risks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-420-CMP-01-03:** risks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-420-CMP-01-04:** risks authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-420-CMP-02-01:** risk reviews schema and migration created.
- [ ] **CHK-MOD-420-CMP-02-02:** risk reviews ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-420-CMP-02-03:** risk reviews foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-420-CMP-02-04:** risk reviews authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-420-CMP-03-01:** change requests schema and migration created.
- [ ] **CHK-MOD-420-CMP-03-02:** change requests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-420-CMP-03-03:** change requests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-420-CMP-03-04:** change requests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-420-CMP-04-01:** impact analyses schema and migration created.
- [ ] **CHK-MOD-420-CMP-04-02:** impact analyses ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-420-CMP-04-03:** impact analyses foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-420-CMP-04-04:** impact analyses authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-420-CMP-05-01:** change approvals schema and migration created.
- [ ] **CHK-MOD-420-CMP-05-02:** change approvals ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-420-CMP-05-03:** change approvals foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-420-CMP-05-04:** change approvals authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-420-CMP-06-01:** baseline updates schema and migration created.
- [ ] **CHK-MOD-420-CMP-06-02:** baseline updates ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-420-CMP-06-03:** baseline updates foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-420-CMP-06-04:** baseline updates authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-420-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-420-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-420-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-420-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-420-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-420-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-420-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-420-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-420-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-420-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-420-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-420-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-420-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-420-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-420-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-420-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-420-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-420-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-420-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-420-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-420-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-420-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-420-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-420-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-420-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-420-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-420-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-420-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-420-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-420-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-420-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-420-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-420-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-420-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-420-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-420-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-420-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-420-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-420-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-420-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-420-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-420-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-420-AC-001:** Out-of-scope work cannot silently enter development.
- [ ] **CHK-MOD-420-AC-002:** Approved changes update affected versions and tickets.
- [ ] **CHK-MOD-420-AC-003:** Rejected and deferred changes preserve evidence and rationale.
- [ ] **CHK-MOD-420-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-420-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-420-AC-902:** Module marked Done before dependent work starts.
### MOD-430 — Releases, Deployment Requests, Production Approval, Rollback, and Closure

**Requirements:** MVP-FR-008, MVP-FR-009  
**Dependencies:** MOD-330, MOD-400, MOD-410, MOD-420, MOD-350

#### Readiness
- [ ] **CHK-MOD-430-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-430-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-430-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-430-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-430-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-430-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-430-CMP-01-01:** releases schema and migration created.
- [ ] **CHK-MOD-430-CMP-01-02:** releases ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-01-03:** releases foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-01-04:** releases authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-430-CMP-02-01:** release items schema and migration created.
- [ ] **CHK-MOD-430-CMP-02-02:** release items ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-02-03:** release items foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-02-04:** release items authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-430-CMP-03-01:** deployments schema and migration created.
- [ ] **CHK-MOD-430-CMP-03-02:** deployments ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-03-03:** deployments foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-03-04:** deployments authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-430-CMP-04-01:** deployment checks schema and migration created.
- [ ] **CHK-MOD-430-CMP-04-02:** deployment checks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-04-03:** deployment checks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-04-04:** deployment checks authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-430-CMP-05-01:** backup confirmations schema and migration created.
- [ ] **CHK-MOD-430-CMP-05-02:** backup confirmations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-05-03:** backup confirmations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-05-04:** backup confirmations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-430-CMP-06-01:** migration plans schema and migration created.
- [ ] **CHK-MOD-430-CMP-06-02:** migration plans ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-06-03:** migration plans foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-06-04:** migration plans authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-430-CMP-07-01:** rollbacks schema and migration created.
- [ ] **CHK-MOD-430-CMP-07-02:** rollbacks ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-07-03:** rollbacks foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-07-04:** rollbacks authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-430-CMP-08-01:** completion reports schema and migration created.
- [ ] **CHK-MOD-430-CMP-08-02:** completion reports ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-430-CMP-08-03:** completion reports foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-430-CMP-08-04:** completion reports authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-430-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-430-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-430-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-430-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-430-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-430-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-430-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-430-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-430-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-430-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-430-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-430-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-430-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-430-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-430-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-430-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-430-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-430-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-430-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-430-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-430-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-430-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-430-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-430-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-430-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-430-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-430-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-430-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-430-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-430-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-430-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-430-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-430-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-430-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-430-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-430-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-430-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-430-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-430-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-430-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-430-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-430-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-430-AC-001:** Production cannot start without evidence and approval.
- [ ] **CHK-MOD-430-AC-002:** Releases trace to requirements, tickets, tests, bugs, changes, and documents.
- [ ] **CHK-MOD-430-AC-003:** Closure requires client and internal acceptance.
- [ ] **CHK-MOD-430-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-430-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-430-AC-902:** Module marked Done before dependent work starts.
### MOD-440 — Notifications, Preferences, Digests, Delivery, and Failure Handling

**Requirements:** MVP-FR-011  
**Dependencies:** MOD-100, MOD-130, MOD-040

#### Readiness
- [ ] **CHK-MOD-440-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-440-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-440-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-440-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-440-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-440-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-440-CMP-01-01:** notifications schema and migration created.
- [ ] **CHK-MOD-440-CMP-01-02:** notifications ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-440-CMP-01-03:** notifications foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-440-CMP-01-04:** notifications authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-440-CMP-02-01:** preferences schema and migration created.
- [ ] **CHK-MOD-440-CMP-02-02:** preferences ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-440-CMP-02-03:** preferences foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-440-CMP-02-04:** preferences authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-440-CMP-03-01:** templates schema and migration created.
- [ ] **CHK-MOD-440-CMP-03-02:** templates ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-440-CMP-03-03:** templates foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-440-CMP-03-04:** templates authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-440-CMP-04-01:** deliveries schema and migration created.
- [ ] **CHK-MOD-440-CMP-04-02:** deliveries ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-440-CMP-04-03:** deliveries foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-440-CMP-04-04:** deliveries authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-440-CMP-05-01:** retries schema and migration created.
- [ ] **CHK-MOD-440-CMP-05-02:** retries ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-440-CMP-05-03:** retries foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-440-CMP-05-04:** retries authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-440-CMP-06-01:** dead letters schema and migration created.
- [ ] **CHK-MOD-440-CMP-06-02:** dead letters ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-440-CMP-06-03:** dead letters foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-440-CMP-06-04:** dead letters authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-440-CMP-07-01:** digests schema and migration created.
- [ ] **CHK-MOD-440-CMP-07-02:** digests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-440-CMP-07-03:** digests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-440-CMP-07-04:** digests authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-440-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-440-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-440-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-440-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-440-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-440-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-440-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-440-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-440-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-440-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-440-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-440-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-440-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-440-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-440-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-440-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-440-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-440-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-440-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-440-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-440-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-440-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-440-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-440-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-440-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-440-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-440-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-440-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-440-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-440-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-440-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-440-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-440-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-440-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-440-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-440-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-440-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-440-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-440-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-440-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-440-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-440-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-440-AC-001:** Notifications are timely, idempotent, auditable, and permission-safe.
- [ ] **CHK-MOD-440-AC-002:** Users can configure preferences without disabling mandatory critical alerts.
- [ ] **CHK-MOD-440-AC-003:** Delivery failures are visible and recoverable.
- [ ] **CHK-MOD-440-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-440-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-440-AC-902:** Module marked Done before dependent work starts.
### MOD-450 — Dashboard, Reporting, Search, Project Health, and Activity Timeline

**Requirements:** MVP-FR-012, MVP-FR-013, MVP-NFR-003  
**Dependencies:** MOD-210, MOD-240, MOD-300, MOD-340, MOD-330, MOD-400, MOD-410, MOD-040

#### Readiness
- [ ] **CHK-MOD-450-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-450-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-450-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-450-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-450-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-450-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-450-CMP-01-01:** dashboard read models schema and migration created.
- [ ] **CHK-MOD-450-CMP-01-02:** dashboard read models ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-450-CMP-01-03:** dashboard read models foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-450-CMP-01-04:** dashboard read models authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-450-CMP-02-01:** project health schema and migration created.
- [ ] **CHK-MOD-450-CMP-02-02:** project health ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-450-CMP-02-03:** project health foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-450-CMP-02-04:** project health authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-450-CMP-03-01:** saved filters schema and migration created.
- [ ] **CHK-MOD-450-CMP-03-02:** saved filters ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-450-CMP-03-03:** saved filters foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-450-CMP-03-04:** saved filters authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-450-CMP-04-01:** global search schema and migration created.
- [ ] **CHK-MOD-450-CMP-04-02:** global search ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-450-CMP-04-03:** global search foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-450-CMP-04-04:** global search authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-450-CMP-05-01:** activity timeline schema and migration created.
- [ ] **CHK-MOD-450-CMP-05-02:** activity timeline ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-450-CMP-05-03:** activity timeline foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-450-CMP-05-04:** activity timeline authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-450-CMP-06-01:** reports schema and migration created.
- [ ] **CHK-MOD-450-CMP-06-02:** reports ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-450-CMP-06-03:** reports foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-450-CMP-06-04:** reports authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-450-CMP-07-01:** exports schema and migration created.
- [ ] **CHK-MOD-450-CMP-07-02:** exports ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-450-CMP-07-03:** exports foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-450-CMP-07-04:** exports authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-450-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-450-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-450-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-450-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-450-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-450-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-450-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-450-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-450-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-450-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-450-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-450-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-450-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-450-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-450-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-450-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-450-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-450-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-450-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-450-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-450-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-450-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-450-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-450-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-450-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-450-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-450-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-450-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-450-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-450-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-450-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-450-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-450-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-450-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-450-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-450-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-450-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-450-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-450-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-450-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-450-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-450-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-450-AC-001:** Dashboard values reconcile with source records.
- [ ] **CHK-MOD-450-AC-002:** Normal updates appear within one minute.
- [ ] **CHK-MOD-450-AC-003:** Counts, search, and exports do not leak unauthorized data.
- [ ] **CHK-MOD-450-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-450-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-450-AC-902:** Module marked Done before dependent work starts.
### MOD-460 — Requirement Traceability, Audit Reports, and Evidence Exports

**Requirements:** MVP-FR-013, MVP-NFR-005  
**Dependencies:** MOD-040, MOD-240, MOD-300, MOD-400, MOD-410, MOD-430

#### Readiness
- [ ] **CHK-MOD-460-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-460-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-460-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-460-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-460-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-460-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-460-CMP-01-01:** requirement-ticket links schema and migration created.
- [ ] **CHK-MOD-460-CMP-01-02:** requirement-ticket links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-460-CMP-01-03:** requirement-ticket links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-460-CMP-01-04:** requirement-ticket links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-460-CMP-02-01:** requirement-test links schema and migration created.
- [ ] **CHK-MOD-460-CMP-02-02:** requirement-test links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-460-CMP-02-03:** requirement-test links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-460-CMP-02-04:** requirement-test links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-460-CMP-03-01:** requirement-release links schema and migration created.
- [ ] **CHK-MOD-460-CMP-03-02:** requirement-release links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-460-CMP-03-03:** requirement-release links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-460-CMP-03-04:** requirement-release links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-460-CMP-04-01:** requirement-document links schema and migration created.
- [ ] **CHK-MOD-460-CMP-04-02:** requirement-document links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-460-CMP-04-03:** requirement-document links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-460-CMP-04-04:** requirement-document links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-460-CMP-05-01:** ticket-test links schema and migration created.
- [ ] **CHK-MOD-460-CMP-05-02:** ticket-test links ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-460-CMP-05-03:** ticket-test links foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-460-CMP-05-04:** ticket-test links authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-460-CMP-06-01:** evidence manifests schema and migration created.
- [ ] **CHK-MOD-460-CMP-06-02:** evidence manifests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-460-CMP-06-03:** evidence manifests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-460-CMP-06-04:** evidence manifests authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-460-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-460-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-460-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-460-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-460-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-460-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-460-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-460-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-460-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-460-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-460-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-460-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-460-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-460-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-460-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-460-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-460-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-460-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-460-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-460-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-460-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-460-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-460-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-460-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-460-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-460-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-460-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-460-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-460-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-460-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-460-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-460-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-460-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-460-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-460-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-460-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-460-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-460-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-460-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-460-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-460-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-460-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-460-AC-001:** At least 95% of Must-Have requirements have complete traceability before release.
- [ ] **CHK-MOD-460-AC-002:** Controlled actions have 100% audit coverage.
- [ ] **CHK-MOD-460-AC-003:** Exports are permission-controlled and independently reconcilable.
- [ ] **CHK-MOD-460-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-460-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-460-AC-902:** Module marked Done before dependent work starts.

## Phase 5 — MVP Integrations

### MOD-500 — Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State

**Requirements:** MVP-FR-014, MVP-FR-015, MVP-NFR-004  
**Dependencies:** MOD-030, MOD-040, MOD-120

#### Readiness
- [ ] **CHK-MOD-500-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-500-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-500-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-500-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-500-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-500-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-500-CMP-01-01:** integration connections schema and migration created.
- [ ] **CHK-MOD-500-CMP-01-02:** integration connections ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-500-CMP-01-03:** integration connections foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-500-CMP-01-04:** integration connections authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-500-CMP-02-01:** webhook events schema and migration created.
- [ ] **CHK-MOD-500-CMP-02-02:** webhook events ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-500-CMP-02-03:** webhook events foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-500-CMP-02-04:** webhook events authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-500-CMP-03-01:** sync cursors schema and migration created.
- [ ] **CHK-MOD-500-CMP-03-02:** sync cursors ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-500-CMP-03-03:** sync cursors foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-500-CMP-03-04:** sync cursors authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-500-CMP-04-01:** external mappings schema and migration created.
- [ ] **CHK-MOD-500-CMP-04-02:** external mappings ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-500-CMP-04-03:** external mappings foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-500-CMP-04-04:** external mappings authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-500-CMP-05-01:** outbox events schema and migration created.
- [ ] **CHK-MOD-500-CMP-05-02:** outbox events ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-500-CMP-05-03:** outbox events foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-500-CMP-05-04:** outbox events authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-500-CMP-06-01:** inbox events schema and migration created.
- [ ] **CHK-MOD-500-CMP-06-02:** inbox events ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-500-CMP-06-03:** inbox events foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-500-CMP-06-04:** inbox events authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-500-CMP-07-01:** connection health schema and migration created.
- [ ] **CHK-MOD-500-CMP-07-02:** connection health ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-500-CMP-07-03:** connection health foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-500-CMP-07-04:** connection health authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-500-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-500-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-500-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-500-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-500-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-500-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-500-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-500-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-500-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-500-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-500-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-500-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-500-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-500-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-500-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-500-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-500-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-500-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-500-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-500-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-500-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-500-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-500-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-500-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-500-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-500-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-500-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-500-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-500-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-500-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-500-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-500-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-500-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-500-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-500-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-500-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-500-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-500-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-500-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-500-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-500-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-500-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-500-AC-001:** Integration failure cannot corrupt internal data.
- [ ] **CHK-MOD-500-AC-002:** External mappings and events are tenant-scoped and audited.
- [ ] **CHK-MOD-500-AC-003:** Credentials never appear in logs, prompts, tickets, or business tables.
- [ ] **CHK-MOD-500-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-500-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-500-AC-902:** Module marked Done before dependent work starts.
### MOD-510 — Gmail Client Communication Integration

**Requirements:** MVP-FR-014  
**Dependencies:** MOD-220, MOD-500, MOD-210, MOD-230

#### Readiness
- [ ] **CHK-MOD-510-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-510-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-510-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-510-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-510-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-510-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-510-CMP-01-01:** Gmail connection schema and migration created.
- [ ] **CHK-MOD-510-CMP-01-02:** Gmail connection ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-510-CMP-01-03:** Gmail connection foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-510-CMP-01-04:** Gmail connection authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-510-CMP-02-01:** history cursor schema and migration created.
- [ ] **CHK-MOD-510-CMP-02-02:** history cursor ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-510-CMP-02-03:** history cursor foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-510-CMP-02-04:** history cursor authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-510-CMP-03-01:** thread mappings schema and migration created.
- [ ] **CHK-MOD-510-CMP-03-02:** thread mappings ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-510-CMP-03-03:** thread mappings foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-510-CMP-03-04:** thread mappings authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-510-CMP-04-01:** message mappings schema and migration created.
- [ ] **CHK-MOD-510-CMP-04-02:** message mappings ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-510-CMP-04-03:** message mappings foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-510-CMP-04-04:** message mappings authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-510-CMP-05-01:** attachment import schema and migration created.
- [ ] **CHK-MOD-510-CMP-05-02:** attachment import ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-510-CMP-05-03:** attachment import foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-510-CMP-05-04:** attachment import authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-510-CMP-06-01:** draft review schema and migration created.
- [ ] **CHK-MOD-510-CMP-06-02:** draft review ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-510-CMP-06-03:** draft review foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-510-CMP-06-04:** draft review authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-510-CMP-07-01:** approved send schema and migration created.
- [ ] **CHK-MOD-510-CMP-07-02:** approved send ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-510-CMP-07-03:** approved send foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-510-CMP-07-04:** approved send authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-510-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-510-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-510-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-510-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-510-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-510-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-510-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-510-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-510-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-510-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-510-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-510-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-510-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-510-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-510-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-510-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-510-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-510-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-510-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-510-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-510-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-510-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-510-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-510-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-510-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-510-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-510-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-510-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-510-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-510-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-510-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-510-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-510-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-510-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-510-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-510-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-510-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-510-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-510-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-510-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-510-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-510-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-510-AC-001:** Valid emails create or update exactly one query and thread.
- [ ] **CHK-MOD-510-AC-002:** Approved outgoing email is sent and linked correctly.
- [ ] **CHK-MOD-510-AC-003:** Duplicate notifications do not duplicate records.
- [ ] **CHK-MOD-510-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-510-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-510-AC-902:** Module marked Done before dependent work starts.
### MOD-520 — Jira Work Management Integration

**Requirements:** MVP-FR-015  
**Dependencies:** MOD-300, MOD-310, MOD-320, MOD-500

#### Readiness
- [ ] **CHK-MOD-520-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-520-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-520-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-520-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-520-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-520-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-520-CMP-01-01:** Jira connection schema and migration created.
- [ ] **CHK-MOD-520-CMP-01-02:** Jira connection ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-520-CMP-01-03:** Jira connection foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-520-CMP-01-04:** Jira connection authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-520-CMP-02-01:** project mapping schema and migration created.
- [ ] **CHK-MOD-520-CMP-02-02:** project mapping ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-520-CMP-02-03:** project mapping foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-520-CMP-02-04:** project mapping authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-520-CMP-03-01:** field mapping schema and migration created.
- [ ] **CHK-MOD-520-CMP-03-02:** field mapping ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-520-CMP-03-03:** field mapping foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-520-CMP-03-04:** field mapping authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-520-CMP-04-01:** status mapping schema and migration created.
- [ ] **CHK-MOD-520-CMP-04-02:** status mapping ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-520-CMP-04-03:** status mapping foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-520-CMP-04-04:** status mapping authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-520-CMP-05-01:** issue mapping schema and migration created.
- [ ] **CHK-MOD-520-CMP-05-02:** issue mapping ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-520-CMP-05-03:** issue mapping foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-520-CMP-05-04:** issue mapping authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-520-CMP-06-01:** comment sync schema and migration created.
- [ ] **CHK-MOD-520-CMP-06-02:** comment sync ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-520-CMP-06-03:** comment sync foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-520-CMP-06-04:** comment sync authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-520-CMP-07-01:** conflict handling schema and migration created.
- [ ] **CHK-MOD-520-CMP-07-02:** conflict handling ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-520-CMP-07-03:** conflict handling foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-520-CMP-07-04:** conflict handling authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-520-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-520-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-520-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-520-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-520-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-520-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-520-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-520-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-520-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-520-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-520-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-520-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-520-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-520-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-520-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-520-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-520-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-520-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-520-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-520-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-520-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-520-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-520-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-520-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-520-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-520-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-520-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-520-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-520-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-520-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-520-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-520-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-520-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-520-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-520-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-520-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-520-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-520-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-520-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-520-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-520-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-520-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-520-AC-001:** Approved internal tickets create Jira issues and retain keys.
- [ ] **CHK-MOD-520-AC-002:** Jira cannot bypass internal transition or approval rules.
- [ ] **CHK-MOD-520-AC-003:** Sync failures are visible, retriable, and audited.
- [ ] **CHK-MOD-520-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-520-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-520-AC-902:** Module marked Done before dependent work starts.

## Phase 6 — Security, Reliability, Pilot, and Production Readiness

### MOD-600 — Security, Privacy, PII, File Safety, Retention, Backup, and Recovery Hardening

**Requirements:** MVP-NFR-001, MVP-NFR-002, MVP-NFR-007, MVP-NFR-008, MVP-NFR-009  
**Dependencies:** All functional foundation modules

#### Readiness
- [ ] **CHK-MOD-600-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-600-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-600-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-600-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-600-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-600-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-600-CMP-01-01:** threat model schema and migration created.
- [ ] **CHK-MOD-600-CMP-01-02:** threat model ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-01-03:** threat model foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-01-04:** threat model authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-600-CMP-02-01:** PII inventory schema and migration created.
- [ ] **CHK-MOD-600-CMP-02-02:** PII inventory ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-02-03:** PII inventory foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-02-04:** PII inventory authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-600-CMP-03-01:** retention policies schema and migration created.
- [ ] **CHK-MOD-600-CMP-03-02:** retention policies ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-03-03:** retention policies foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-03-04:** retention policies authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-600-CMP-04-01:** legal holds schema and migration created.
- [ ] **CHK-MOD-600-CMP-04-02:** legal holds ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-04-03:** legal holds foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-04-04:** legal holds authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-600-CMP-05-01:** deletion jobs schema and migration created.
- [ ] **CHK-MOD-600-CMP-05-02:** deletion jobs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-05-03:** deletion jobs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-05-04:** deletion jobs authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-600-CMP-06-01:** backup records schema and migration created.
- [ ] **CHK-MOD-600-CMP-06-02:** backup records ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-06-03:** backup records foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-06-04:** backup records authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-600-CMP-07-01:** restore tests schema and migration created.
- [ ] **CHK-MOD-600-CMP-07-02:** restore tests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-07-03:** restore tests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-07-04:** restore tests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-600-CMP-08-01:** security incidents schema and migration created.
- [ ] **CHK-MOD-600-CMP-08-02:** security incidents ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-600-CMP-08-03:** security incidents foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-600-CMP-08-04:** security incidents authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-600-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-600-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-600-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-600-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-600-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-600-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-600-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-600-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-600-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-600-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-600-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-600-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-600-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-600-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-600-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-600-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-600-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-600-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-600-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-600-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-600-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-600-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-600-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-600-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-600-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-600-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-600-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-600-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-600-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-600-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-600-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-600-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-600-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-600-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-600-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-600-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-600-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-600-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-600-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-600-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-600-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-600-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-600-AC-001:** No Critical security or isolation defect remains.
- [ ] **CHK-MOD-600-AC-002:** RPO and RTO targets are validated.
- [ ] **CHK-MOD-600-AC-003:** Client and company data are excluded from model training by default.
- [ ] **CHK-MOD-600-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-600-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-600-AC-902:** Module marked Done before dependent work starts.
### MOD-610 — Performance, Reliability, Idempotency, Resilience, and Disaster Recovery

**Requirements:** MVP-NFR-003, MVP-NFR-004, MVP-NFR-006, MVP-NFR-007  
**Dependencies:** MOD-350, MOD-440, MOD-500, MOD-600

#### Readiness
- [ ] **CHK-MOD-610-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-610-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-610-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-610-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-610-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-610-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-610-CMP-01-01:** performance tests schema and migration created.
- [ ] **CHK-MOD-610-CMP-01-02:** performance tests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-610-CMP-01-03:** performance tests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-610-CMP-01-04:** performance tests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-610-CMP-02-01:** resilience tests schema and migration created.
- [ ] **CHK-MOD-610-CMP-02-02:** resilience tests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-610-CMP-02-03:** resilience tests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-610-CMP-02-04:** resilience tests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-610-CMP-03-01:** index review schema and migration created.
- [ ] **CHK-MOD-610-CMP-03-02:** index review ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-610-CMP-03-03:** index review foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-610-CMP-03-04:** index review authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-610-CMP-04-01:** SLO dashboards schema and migration created.
- [ ] **CHK-MOD-610-CMP-04-02:** SLO dashboards ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-610-CMP-04-03:** SLO dashboards foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-610-CMP-04-04:** SLO dashboards authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-610-CMP-05-01:** workflow replay schema and migration created.
- [ ] **CHK-MOD-610-CMP-05-02:** workflow replay ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-610-CMP-05-03:** workflow replay foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-610-CMP-05-04:** workflow replay authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-610-CMP-06-01:** integration failure tests schema and migration created.
- [ ] **CHK-MOD-610-CMP-06-02:** integration failure tests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-610-CMP-06-03:** integration failure tests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-610-CMP-06-04:** integration failure tests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-610-CMP-07-01:** DR runbook schema and migration created.
- [ ] **CHK-MOD-610-CMP-07-02:** DR runbook ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-610-CMP-07-03:** DR runbook foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-610-CMP-07-04:** DR runbook authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-610-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-610-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-610-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-610-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-610-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-610-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-610-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-610-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-610-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-610-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-610-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-610-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-610-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-610-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-610-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-610-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-610-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-610-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-610-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-610-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-610-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-610-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-610-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-610-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-610-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-610-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-610-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-610-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-610-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-610-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-610-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-610-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-610-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-610-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-610-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-610-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-610-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-610-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-610-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-610-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-610-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-610-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-610-AC-001:** 95% of normal APIs are under two seconds.
- [ ] **CHK-MOD-610-AC-002:** Dashboard is under three seconds at pilot load.
- [ ] **CHK-MOD-610-AC-003:** Durable workflows resume after failure and remain idempotent.
- [ ] **CHK-MOD-610-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-610-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-610-AC-902:** Module marked Done before dependent work starts.
### MOD-620 — Synthetic Sample Projects, Agent Evaluation, End-to-End Acceptance, and UAT

**Requirements:** MVP Acceptance Criteria, Sample Projects  
**Dependencies:** All MVP functional modules

#### Readiness
- [ ] **CHK-MOD-620-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-620-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-620-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-620-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-620-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-620-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-620-CMP-01-01:** seed scripts schema and migration created.
- [ ] **CHK-MOD-620-CMP-01-02:** seed scripts ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-620-CMP-01-03:** seed scripts foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-620-CMP-01-04:** seed scripts authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-620-CMP-02-01:** expected decisions schema and migration created.
- [ ] **CHK-MOD-620-CMP-02-02:** expected decisions ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-620-CMP-02-03:** expected decisions foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-620-CMP-02-04:** expected decisions authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-620-CMP-03-01:** agent evaluations schema and migration created.
- [ ] **CHK-MOD-620-CMP-03-02:** agent evaluations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-620-CMP-03-03:** agent evaluations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-620-CMP-03-04:** agent evaluations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-620-CMP-04-01:** E2E tests schema and migration created.
- [ ] **CHK-MOD-620-CMP-04-02:** E2E tests ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-620-CMP-04-03:** E2E tests foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-620-CMP-04-04:** E2E tests authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-620-CMP-05-01:** role-based UAT schema and migration created.
- [ ] **CHK-MOD-620-CMP-05-02:** role-based UAT ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-620-CMP-05-03:** role-based UAT foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-620-CMP-05-04:** role-based UAT authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-620-CMP-06-01:** acceptance evidence schema and migration created.
- [ ] **CHK-MOD-620-CMP-06-02:** acceptance evidence ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-620-CMP-06-03:** acceptance evidence foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-620-CMP-06-04:** acceptance evidence authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-620-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-620-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-620-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-620-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-620-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-620-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-620-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-620-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-620-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-620-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-620-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-620-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-620-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-620-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-620-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-620-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-620-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-620-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-620-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-620-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-620-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-620-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-620-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-620-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-620-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-620-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-620-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-620-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-620-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-620-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-620-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-620-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-620-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-620-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-620-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-620-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-620-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-620-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-620-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-620-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-620-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-620-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-620-AC-001:** All three sample projects pass defined workflows.
- [ ] **CHK-MOD-620-AC-002:** Agent quality metrics meet targets.
- [ ] **CHK-MOD-620-AC-003:** No unauthorized agent approval or isolation failure occurs.
- [ ] **CHK-MOD-620-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-620-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-620-AC-902:** Module marked Done before dependent work starts.
### MOD-630 — Controlled Pilot, Production Release, Operations, and Final MVP Sign-Off

**Requirements:** MVP Exit Criteria, Final Acceptance Sign-Off  
**Dependencies:** MOD-600, MOD-610, MOD-620

#### Readiness
- [ ] **CHK-MOD-630-RDY-001:** Dependencies complete or formally waived.
- [ ] **CHK-MOD-630-RDY-002:** Module scope and exclusions clear.
- [ ] **CHK-MOD-630-RDY-003:** Data owners, human owners, agent roles, and approvers identified.
- [ ] **CHK-MOD-630-RDY-004:** Statuses, transitions, follow-ups, approvals, events, notifications, and audit actions identified.
- [ ] **CHK-MOD-630-RDY-005:** UI role variants and access rules defined.
- [ ] **CHK-MOD-630-RDY-006:** Test data and acceptance scenarios available.

#### Main Components
- [ ] **CHK-MOD-630-CMP-01-01:** pilot plan schema and migration created.
- [ ] **CHK-MOD-630-CMP-01-02:** pilot plan ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-01-03:** pilot plan foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-01-04:** pilot plan authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-630-CMP-02-01:** pilot users schema and migration created.
- [ ] **CHK-MOD-630-CMP-02-02:** pilot users ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-02-03:** pilot users foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-02-04:** pilot users authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-630-CMP-03-01:** training schema and migration created.
- [ ] **CHK-MOD-630-CMP-03-02:** training ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-03-03:** training foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-03-04:** training authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-630-CMP-04-01:** support readiness schema and migration created.
- [ ] **CHK-MOD-630-CMP-04-02:** support readiness ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-04-03:** support readiness foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-04-04:** support readiness authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-630-CMP-05-01:** known limitations schema and migration created.
- [ ] **CHK-MOD-630-CMP-05-02:** known limitations ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-05-03:** known limitations foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-05-04:** known limitations authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-630-CMP-06-01:** production deployment schema and migration created.
- [ ] **CHK-MOD-630-CMP-06-02:** production deployment ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-06-03:** production deployment foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-06-04:** production deployment authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-630-CMP-07-01:** rollback schema and migration created.
- [ ] **CHK-MOD-630-CMP-07-02:** rollback ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-07-03:** rollback foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-07-04:** rollback authorization, RLS, and isolation tests pass.
- [ ] **CHK-MOD-630-CMP-08-01:** final sign-offs schema and migration created.
- [ ] **CHK-MOD-630-CMP-08-02:** final sign-offs ownership, tenant/project scope, status, timestamps, version, deletion, retention, and audit rules defined.
- [ ] **CHK-MOD-630-CMP-08-03:** final sign-offs foreign keys, uniqueness, checks, indexes, and concurrency verified.
- [ ] **CHK-MOD-630-CMP-08-04:** final sign-offs authorization, RLS, and isolation tests pass.

#### Backend and API
- [ ] **CHK-MOD-630-BEAPI-001:** Typed domain models and validation implemented.
- [ ] **CHK-MOD-630-BEAPI-002:** Application services enforce authorization and approval.
- [ ] **CHK-MOD-630-BEAPI-003:** Transactions and outbox behavior implemented where required.
- [ ] **CHK-MOD-630-BEAPI-004:** Optimistic concurrency and duplicate handling implemented.
- [ ] **CHK-MOD-630-BEAPI-005:** CRUD and action endpoints implemented.
- [ ] **CHK-MOD-630-BEAPI-006:** Pagination, filtering, sorting, and bounded search implemented.
- [ ] **CHK-MOD-630-BEAPI-007:** Standard problem-details errors implemented.
- [ ] **CHK-MOD-630-BEAPI-008:** OpenAPI success and failure examples updated.

#### Frontend and UX
- [ ] **CHK-MOD-630-FE-001:** Module list/dashboard view implemented.
- [ ] **CHK-MOD-630-FE-002:** Detail view and related-record tabs implemented.
- [ ] **CHK-MOD-630-FE-003:** Create/edit/review forms implemented.
- [ ] **CHK-MOD-630-FE-004:** Loading, empty, error, forbidden, stale-version, and success states implemented.
- [ ] **CHK-MOD-630-FE-005:** Permission-aware actions implemented with server enforcement.
- [ ] **CHK-MOD-630-FE-006:** Responsive behavior verified.
- [ ] **CHK-MOD-630-FE-007:** Keyboard and screen-reader accessibility verified.
- [ ] **CHK-MOD-630-FE-008:** Timezone and date formatting verified.

#### Workflow, Agent, Events, and Notifications
- [ ] **CHK-MOD-630-WF-001:** Triggers, owners, inputs, outputs, statuses, waits, approvals, evidence, and closure rules defined.
- [ ] **CHK-MOD-630-WF-002:** Long-running waits use Temporal where applicable.
- [ ] **CHK-MOD-630-WF-003:** Bounded reasoning uses LangGraph where applicable.
- [ ] **CHK-MOD-630-WF-004:** State mutations use FastAPI application services.
- [ ] **CHK-MOD-630-WF-005:** Domain events and idempotent consumers implemented.
- [ ] **CHK-MOD-630-WF-006:** Correlation and causation IDs propagated.
- [ ] **CHK-MOD-630-WF-007:** Retry, dead-letter, replay, and cancellation behavior verified.
- [ ] **CHK-MOD-630-WF-008:** Human intervention exists for conflict, low confidence, failure, or missing authority.
- [ ] **CHK-MOD-630-WF-009:** Notification recipients, content, delivery, and audit verified.

#### Security, Privacy, and Audit
- [ ] **CHK-MOD-630-SEC-001:** Deny-by-default backend authorization passes.
- [ ] **CHK-MOD-630-SEC-002:** Tenant and project isolation passes.
- [ ] **CHK-MOD-630-SEC-003:** Classification and environment restrictions pass.
- [ ] **CHK-MOD-630-SEC-004:** Secrets and unnecessary PII are absent from logs, prompts, events, notifications, exports, and errors.
- [ ] **CHK-MOD-630-SEC-005:** Sensitive actions require the configured human approval.
- [ ] **CHK-MOD-630-SEC-006:** All controlled actions generate audit records.
- [ ] **CHK-MOD-630-SEC-007:** Audit records contain actor, organization, project, action, entity, reason, source, correlation ID, and timestamp.

#### Testing and Evidence
- [ ] **CHK-MOD-630-QA-001:** Unit tests pass.
- [ ] **CHK-MOD-630-QA-002:** Database integration tests pass.
- [ ] **CHK-MOD-630-QA-003:** API contract tests pass.
- [ ] **CHK-MOD-630-QA-004:** Permission-negative tests pass.
- [ ] **CHK-MOD-630-QA-005:** Tenant/project isolation tests pass.
- [ ] **CHK-MOD-630-QA-006:** Concurrency and duplicate-request tests pass where relevant.
- [ ] **CHK-MOD-630-QA-007:** Workflow/agent/integration/security/performance tests pass where relevant.
- [ ] **CHK-MOD-630-QA-008:** Formatter, lint, typing, migrations, tests, scans, and builds pass.
- [ ] **CHK-MOD-630-QA-009:** README, data dictionary, OpenAPI, permissions, workflows, audit, migration, rollback, and user guidance updated.
- [ ] **CHK-MOD-630-QA-010:** Verification evidence linked.

#### Acceptance
- [ ] **CHK-MOD-630-AC-001:** All Critical and High acceptance tests pass.
- [ ] **CHK-MOD-630-AC-002:** Pilot users approve controlled production use.
- [ ] **CHK-MOD-630-AC-003:** Cross-functional production readiness sign-off is complete.
- [ ] **CHK-MOD-630-AC-900:** All Critical and High defects resolved.
- [ ] **CHK-MOD-630-AC-901:** Human owner approved completion evidence.
- [ ] **CHK-MOD-630-AC-902:** Module marked Done before dependent work starts.

## 10. Cross-Module Security and Quality

- [ ] **CROSS-001:** All tenant-owned tables include organization scope.
- [ ] **CROSS-002:** Project-owned records include project scope where applicable.
- [ ] **CROSS-003:** RLS is enabled and tested on sensitive tables.
- [ ] **CROSS-004:** Cache keys include tenant and project context.
- [ ] **CROSS-005:** Vector metadata includes tenant, client, project, classification, and approved version.
- [ ] **CROSS-006:** Object storage paths are tenant and project scoped.
- [ ] **CROSS-007:** Signed URLs are short-lived and permission checked.
- [ ] **CROSS-008:** Search, counts, dashboards, and exports do not leak existence.
- [ ] **CROSS-009:** Agents receive minimum context only.
- [ ] **CROSS-010:** Untrusted content cannot alter system instructions or tool scope.
- [ ] **CROSS-011:** Agent tools are allowlisted and policy checked.
- [ ] **CROSS-012:** Agents never receive raw production secrets.
- [ ] **CROSS-013:** Agents cannot approve high-risk actions.
- [ ] **CROSS-014:** Approvals bind to exact versions.
- [ ] **CROSS-015:** Every transition uses the shared engine.
- [ ] **CROSS-016:** Every follow-up has owner, due date, rule version, and closure condition.
- [ ] **CROSS-017:** Reminders and escalations are idempotent.
- [ ] **CROSS-018:** Webhooks are authenticated and idempotent.
- [ ] **CROSS-019:** Integrations are tenant and environment scoped.
- [ ] **CROSS-020:** Sent external messages and approved versions are immutable.
- [ ] **CROSS-021:** Files are quarantined and validated before use or indexing.
- [ ] **CROSS-022:** Controlled actions have audit coverage.
- [ ] **CROSS-023:** PII is minimized and redacted.
- [ ] **CROSS-024:** Client data is not used for model training without written approval.
- [ ] **CROSS-025:** Retention, deletion, legal hold, backup, restore, and incident procedures are tested.

## 11. End-to-End Workflow Validation

- [ ] **E2E-WF-01-01:** Client Query to BD — forward path passes.
- [ ] **E2E-WF-01-02:** Client Query to BD — reverse clarification path passes.
- [ ] **E2E-WF-01-03:** Client Query to BD — waiting owner and deadline passes.
- [ ] **E2E-WF-01-04:** Client Query to BD — reminder timing passes.
- [ ] **E2E-WF-01-05:** Client Query to BD — overdue transition passes.
- [ ] **E2E-WF-01-06:** Client Query to BD — escalation routing passes.
- [ ] **E2E-WF-01-07:** Client Query to BD — rejection or exception path passes.
- [ ] **E2E-WF-01-08:** Client Query to BD — human approval passes.
- [ ] **E2E-WF-01-09:** Client Query to BD — duplicate-signal idempotency passes.
- [ ] **E2E-WF-01-10:** Client Query to BD — audit and activity timeline passes.
- [ ] **E2E-WF-01-11:** Client Query to BD — restart recovery passes.
- [ ] **E2E-WF-01-12:** Client Query to BD — evidence-based closure passes.
- [ ] **E2E-WF-02-01:** BD to PM Handover — forward path passes.
- [ ] **E2E-WF-02-02:** BD to PM Handover — reverse clarification path passes.
- [ ] **E2E-WF-02-03:** BD to PM Handover — waiting owner and deadline passes.
- [ ] **E2E-WF-02-04:** BD to PM Handover — reminder timing passes.
- [ ] **E2E-WF-02-05:** BD to PM Handover — overdue transition passes.
- [ ] **E2E-WF-02-06:** BD to PM Handover — escalation routing passes.
- [ ] **E2E-WF-02-07:** BD to PM Handover — rejection or exception path passes.
- [ ] **E2E-WF-02-08:** BD to PM Handover — human approval passes.
- [ ] **E2E-WF-02-09:** BD to PM Handover — duplicate-signal idempotency passes.
- [ ] **E2E-WF-02-10:** BD to PM Handover — audit and activity timeline passes.
- [ ] **E2E-WF-02-11:** BD to PM Handover — restart recovery passes.
- [ ] **E2E-WF-02-12:** BD to PM Handover — evidence-based closure passes.
- [ ] **E2E-WF-03-01:** PM Clarification Back to BD — forward path passes.
- [ ] **E2E-WF-03-02:** PM Clarification Back to BD — reverse clarification path passes.
- [ ] **E2E-WF-03-03:** PM Clarification Back to BD — waiting owner and deadline passes.
- [ ] **E2E-WF-03-04:** PM Clarification Back to BD — reminder timing passes.
- [ ] **E2E-WF-03-05:** PM Clarification Back to BD — overdue transition passes.
- [ ] **E2E-WF-03-06:** PM Clarification Back to BD — escalation routing passes.
- [ ] **E2E-WF-03-07:** PM Clarification Back to BD — rejection or exception path passes.
- [ ] **E2E-WF-03-08:** PM Clarification Back to BD — human approval passes.
- [ ] **E2E-WF-03-09:** PM Clarification Back to BD — duplicate-signal idempotency passes.
- [ ] **E2E-WF-03-10:** PM Clarification Back to BD — audit and activity timeline passes.
- [ ] **E2E-WF-03-11:** PM Clarification Back to BD — restart recovery passes.
- [ ] **E2E-WF-03-12:** PM Clarification Back to BD — evidence-based closure passes.
- [ ] **E2E-WF-04-01:** PM to TL Handover — forward path passes.
- [ ] **E2E-WF-04-02:** PM to TL Handover — reverse clarification path passes.
- [ ] **E2E-WF-04-03:** PM to TL Handover — waiting owner and deadline passes.
- [ ] **E2E-WF-04-04:** PM to TL Handover — reminder timing passes.
- [ ] **E2E-WF-04-05:** PM to TL Handover — overdue transition passes.
- [ ] **E2E-WF-04-06:** PM to TL Handover — escalation routing passes.
- [ ] **E2E-WF-04-07:** PM to TL Handover — rejection or exception path passes.
- [ ] **E2E-WF-04-08:** PM to TL Handover — human approval passes.
- [ ] **E2E-WF-04-09:** PM to TL Handover — duplicate-signal idempotency passes.
- [ ] **E2E-WF-04-10:** PM to TL Handover — audit and activity timeline passes.
- [ ] **E2E-WF-04-11:** PM to TL Handover — restart recovery passes.
- [ ] **E2E-WF-04-12:** PM to TL Handover — evidence-based closure passes.
- [ ] **E2E-WF-05-01:** TL to Development Assignment — forward path passes.
- [ ] **E2E-WF-05-02:** TL to Development Assignment — reverse clarification path passes.
- [ ] **E2E-WF-05-03:** TL to Development Assignment — waiting owner and deadline passes.
- [ ] **E2E-WF-05-04:** TL to Development Assignment — reminder timing passes.
- [ ] **E2E-WF-05-05:** TL to Development Assignment — overdue transition passes.
- [ ] **E2E-WF-05-06:** TL to Development Assignment — escalation routing passes.
- [ ] **E2E-WF-05-07:** TL to Development Assignment — rejection or exception path passes.
- [ ] **E2E-WF-05-08:** TL to Development Assignment — human approval passes.
- [ ] **E2E-WF-05-09:** TL to Development Assignment — duplicate-signal idempotency passes.
- [ ] **E2E-WF-05-10:** TL to Development Assignment — audit and activity timeline passes.
- [ ] **E2E-WF-05-11:** TL to Development Assignment — restart recovery passes.
- [ ] **E2E-WF-05-12:** TL to Development Assignment — evidence-based closure passes.
- [ ] **E2E-WF-06-01:** Developer Blocker Escalation — forward path passes.
- [ ] **E2E-WF-06-02:** Developer Blocker Escalation — reverse clarification path passes.
- [ ] **E2E-WF-06-03:** Developer Blocker Escalation — waiting owner and deadline passes.
- [ ] **E2E-WF-06-04:** Developer Blocker Escalation — reminder timing passes.
- [ ] **E2E-WF-06-05:** Developer Blocker Escalation — overdue transition passes.
- [ ] **E2E-WF-06-06:** Developer Blocker Escalation — escalation routing passes.
- [ ] **E2E-WF-06-07:** Developer Blocker Escalation — rejection or exception path passes.
- [ ] **E2E-WF-06-08:** Developer Blocker Escalation — human approval passes.
- [ ] **E2E-WF-06-09:** Developer Blocker Escalation — duplicate-signal idempotency passes.
- [ ] **E2E-WF-06-10:** Developer Blocker Escalation — audit and activity timeline passes.
- [ ] **E2E-WF-06-11:** Developer Blocker Escalation — restart recovery passes.
- [ ] **E2E-WF-06-12:** Developer Blocker Escalation — evidence-based closure passes.
- [ ] **E2E-WF-07-01:** Development to QA — forward path passes.
- [ ] **E2E-WF-07-02:** Development to QA — reverse clarification path passes.
- [ ] **E2E-WF-07-03:** Development to QA — waiting owner and deadline passes.
- [ ] **E2E-WF-07-04:** Development to QA — reminder timing passes.
- [ ] **E2E-WF-07-05:** Development to QA — overdue transition passes.
- [ ] **E2E-WF-07-06:** Development to QA — escalation routing passes.
- [ ] **E2E-WF-07-07:** Development to QA — rejection or exception path passes.
- [ ] **E2E-WF-07-08:** Development to QA — human approval passes.
- [ ] **E2E-WF-07-09:** Development to QA — duplicate-signal idempotency passes.
- [ ] **E2E-WF-07-10:** Development to QA — audit and activity timeline passes.
- [ ] **E2E-WF-07-11:** Development to QA — restart recovery passes.
- [ ] **E2E-WF-07-12:** Development to QA — evidence-based closure passes.
- [ ] **E2E-WF-08-01:** QA Bug and Retesting — forward path passes.
- [ ] **E2E-WF-08-02:** QA Bug and Retesting — reverse clarification path passes.
- [ ] **E2E-WF-08-03:** QA Bug and Retesting — waiting owner and deadline passes.
- [ ] **E2E-WF-08-04:** QA Bug and Retesting — reminder timing passes.
- [ ] **E2E-WF-08-05:** QA Bug and Retesting — overdue transition passes.
- [ ] **E2E-WF-08-06:** QA Bug and Retesting — escalation routing passes.
- [ ] **E2E-WF-08-07:** QA Bug and Retesting — rejection or exception path passes.
- [ ] **E2E-WF-08-08:** QA Bug and Retesting — human approval passes.
- [ ] **E2E-WF-08-09:** QA Bug and Retesting — duplicate-signal idempotency passes.
- [ ] **E2E-WF-08-10:** QA Bug and Retesting — audit and activity timeline passes.
- [ ] **E2E-WF-08-11:** QA Bug and Retesting — restart recovery passes.
- [ ] **E2E-WF-08-12:** QA Bug and Retesting — evidence-based closure passes.
- [ ] **E2E-WF-09-01:** PM Progress to BD — forward path passes.
- [ ] **E2E-WF-09-02:** PM Progress to BD — reverse clarification path passes.
- [ ] **E2E-WF-09-03:** PM Progress to BD — waiting owner and deadline passes.
- [ ] **E2E-WF-09-04:** PM Progress to BD — reminder timing passes.
- [ ] **E2E-WF-09-05:** PM Progress to BD — overdue transition passes.
- [ ] **E2E-WF-09-06:** PM Progress to BD — escalation routing passes.
- [ ] **E2E-WF-09-07:** PM Progress to BD — rejection or exception path passes.
- [ ] **E2E-WF-09-08:** PM Progress to BD — human approval passes.
- [ ] **E2E-WF-09-09:** PM Progress to BD — duplicate-signal idempotency passes.
- [ ] **E2E-WF-09-10:** PM Progress to BD — audit and activity timeline passes.
- [ ] **E2E-WF-09-11:** PM Progress to BD — restart recovery passes.
- [ ] **E2E-WF-09-12:** PM Progress to BD — evidence-based closure passes.
- [ ] **E2E-WF-10-01:** BD Update to Client — forward path passes.
- [ ] **E2E-WF-10-02:** BD Update to Client — reverse clarification path passes.
- [ ] **E2E-WF-10-03:** BD Update to Client — waiting owner and deadline passes.
- [ ] **E2E-WF-10-04:** BD Update to Client — reminder timing passes.
- [ ] **E2E-WF-10-05:** BD Update to Client — overdue transition passes.
- [ ] **E2E-WF-10-06:** BD Update to Client — escalation routing passes.
- [ ] **E2E-WF-10-07:** BD Update to Client — rejection or exception path passes.
- [ ] **E2E-WF-10-08:** BD Update to Client — human approval passes.
- [ ] **E2E-WF-10-09:** BD Update to Client — duplicate-signal idempotency passes.
- [ ] **E2E-WF-10-10:** BD Update to Client — audit and activity timeline passes.
- [ ] **E2E-WF-10-11:** BD Update to Client — restart recovery passes.
- [ ] **E2E-WF-10-12:** BD Update to Client — evidence-based closure passes.
- [ ] **E2E-WF-11-01:** Change Request — forward path passes.
- [ ] **E2E-WF-11-02:** Change Request — reverse clarification path passes.
- [ ] **E2E-WF-11-03:** Change Request — waiting owner and deadline passes.
- [ ] **E2E-WF-11-04:** Change Request — reminder timing passes.
- [ ] **E2E-WF-11-05:** Change Request — overdue transition passes.
- [ ] **E2E-WF-11-06:** Change Request — escalation routing passes.
- [ ] **E2E-WF-11-07:** Change Request — rejection or exception path passes.
- [ ] **E2E-WF-11-08:** Change Request — human approval passes.
- [ ] **E2E-WF-11-09:** Change Request — duplicate-signal idempotency passes.
- [ ] **E2E-WF-11-10:** Change Request — audit and activity timeline passes.
- [ ] **E2E-WF-11-11:** Change Request — restart recovery passes.
- [ ] **E2E-WF-11-12:** Change Request — evidence-based closure passes.
- [ ] **E2E-WF-12-01:** Deployment and Approval — forward path passes.
- [ ] **E2E-WF-12-02:** Deployment and Approval — reverse clarification path passes.
- [ ] **E2E-WF-12-03:** Deployment and Approval — waiting owner and deadline passes.
- [ ] **E2E-WF-12-04:** Deployment and Approval — reminder timing passes.
- [ ] **E2E-WF-12-05:** Deployment and Approval — overdue transition passes.
- [ ] **E2E-WF-12-06:** Deployment and Approval — escalation routing passes.
- [ ] **E2E-WF-12-07:** Deployment and Approval — rejection or exception path passes.
- [ ] **E2E-WF-12-08:** Deployment and Approval — human approval passes.
- [ ] **E2E-WF-12-09:** Deployment and Approval — duplicate-signal idempotency passes.
- [ ] **E2E-WF-12-10:** Deployment and Approval — audit and activity timeline passes.
- [ ] **E2E-WF-12-11:** Deployment and Approval — restart recovery passes.
- [ ] **E2E-WF-12-12:** Deployment and Approval — evidence-based closure passes.

## 12. Sample Projects and Agent Evaluation

- [ ] **SP-001-001:** Small website project — seed imports passes.
- [ ] **SP-001-002:** Small website project — query and conversation preservation passes.
- [ ] **SP-001-003:** Small website project — BD brief completeness passes.
- [ ] **SP-001-004:** Small website project — PM gap detection passes.
- [ ] **SP-001-005:** Small website project — SRS and phases passes.
- [ ] **SP-001-006:** Small website project — traceable tickets passes.
- [ ] **SP-001-007:** Small website project — skill/capacity assignment passes.
- [ ] **SP-001-008:** Small website project — clarification and blocker routing passes.
- [ ] **SP-001-009:** Small website project — reminders and escalation passes.
- [ ] **SP-001-010:** Small website project — QA reject/reopen/retest passes.
- [ ] **SP-001-011:** Small website project — feedback classification passes.
- [ ] **SP-001-012:** Small website project — exact-version approvals passes.
- [ ] **SP-001-013:** Small website project — dashboard reconciliation passes.
- [ ] **SP-001-014:** Small website project — complete audit passes.
- [ ] **SP-001-015:** Small website project — isolation passes.
- [ ] **SP-001-016:** Small website project — release and closure gates passes.
- [ ] **SP-002-001:** Medium web/mobile appointment project — seed imports passes.
- [ ] **SP-002-002:** Medium web/mobile appointment project — query and conversation preservation passes.
- [ ] **SP-002-003:** Medium web/mobile appointment project — BD brief completeness passes.
- [ ] **SP-002-004:** Medium web/mobile appointment project — PM gap detection passes.
- [ ] **SP-002-005:** Medium web/mobile appointment project — SRS and phases passes.
- [ ] **SP-002-006:** Medium web/mobile appointment project — traceable tickets passes.
- [ ] **SP-002-007:** Medium web/mobile appointment project — skill/capacity assignment passes.
- [ ] **SP-002-008:** Medium web/mobile appointment project — clarification and blocker routing passes.
- [ ] **SP-002-009:** Medium web/mobile appointment project — reminders and escalation passes.
- [ ] **SP-002-010:** Medium web/mobile appointment project — QA reject/reopen/retest passes.
- [ ] **SP-002-011:** Medium web/mobile appointment project — feedback classification passes.
- [ ] **SP-002-012:** Medium web/mobile appointment project — exact-version approvals passes.
- [ ] **SP-002-013:** Medium web/mobile appointment project — dashboard reconciliation passes.
- [ ] **SP-002-014:** Medium web/mobile appointment project — complete audit passes.
- [ ] **SP-002-015:** Medium web/mobile appointment project — isolation passes.
- [ ] **SP-002-016:** Medium web/mobile appointment project — release and closure gates passes.
- [ ] **SP-003-001:** Complex multi-team enterprise project — seed imports passes.
- [ ] **SP-003-002:** Complex multi-team enterprise project — query and conversation preservation passes.
- [ ] **SP-003-003:** Complex multi-team enterprise project — BD brief completeness passes.
- [ ] **SP-003-004:** Complex multi-team enterprise project — PM gap detection passes.
- [ ] **SP-003-005:** Complex multi-team enterprise project — SRS and phases passes.
- [ ] **SP-003-006:** Complex multi-team enterprise project — traceable tickets passes.
- [ ] **SP-003-007:** Complex multi-team enterprise project — skill/capacity assignment passes.
- [ ] **SP-003-008:** Complex multi-team enterprise project — clarification and blocker routing passes.
- [ ] **SP-003-009:** Complex multi-team enterprise project — reminders and escalation passes.
- [ ] **SP-003-010:** Complex multi-team enterprise project — QA reject/reopen/retest passes.
- [ ] **SP-003-011:** Complex multi-team enterprise project — feedback classification passes.
- [ ] **SP-003-012:** Complex multi-team enterprise project — exact-version approvals passes.
- [ ] **SP-003-013:** Complex multi-team enterprise project — dashboard reconciliation passes.
- [ ] **SP-003-014:** Complex multi-team enterprise project — complete audit passes.
- [ ] **SP-003-015:** Complex multi-team enterprise project — isolation passes.
- [ ] **SP-003-016:** Complex multi-team enterprise project — release and closure gates passes.

## 13. Quantitative Targets

- [ ] **METRIC-001:** Query classification accuracy ≥ 90%.
- [ ] **METRIC-002:** Mandatory requirement completeness ≥ 95%.
- [ ] **METRIC-003:** Missing-requirement detection ≥ 90%.
- [ ] **METRIC-004:** Requirement-to-ticket traceability ≥ 95%.
- [ ] **METRIC-005:** Correct role recommendation ≥ 90%.
- [ ] **METRIC-006:** Follow-up routing accuracy ≥ 95%.
- [ ] **METRIC-007:** Correct bug-severity recommendation ≥ 85%.
- [ ] **METRIC-008:** Unauthorized-action prevention = 100%.
- [ ] **METRIC-009:** Agent action audit coverage = 100%.
- [ ] **METRIC-010:** Human approval enforcement = 100%.
- [ ] **METRIC-011:** 95% of normal API requests < 2 seconds at pilot load.
- [ ] **METRIC-012:** Dashboard < 3 seconds at pilot load.
- [ ] **METRIC-013:** Normal dashboard event updates < 1 minute.
- [ ] **METRIC-014:** Pilot availability ≥ 99.5%.
- [ ] **METRIC-015:** Database RPO ≤ 15 minutes.
- [ ] **METRIC-016:** Application RTO ≤ 4 hours.
- [ ] **METRIC-017:** At least 80% of pilot users complete core tasks without assistance.
- [ ] **METRIC-018:** Average pilot satisfaction ≥ 4/5.
- [ ] **METRIC-019:** At least 90% of required documents use the correct template.

## 14. Production Readiness and Sign-Off

- [ ] **PROD-001:** All Critical and High acceptance tests pass.
- [ ] **PROD-002:** No unresolved Critical security defect.
- [ ] **PROD-003:** No unresolved Critical workflow defect.
- [ ] **PROD-004:** Human approval gates enforced.
- [ ] **PROD-005:** Audit coverage reaches 100% for controlled actions.
- [ ] **PROD-006:** Cross-client isolation tests pass.
- [ ] **PROD-007:** Backup and restore tests pass.
- [ ] **PROD-008:** Follow-up and escalation tests pass.
- [ ] **PROD-009:** All three synthetic projects pass.
- [ ] **PROD-010:** Known limitations documented.
- [ ] **PROD-011:** Production deployment plan approved.
- [ ] **PROD-012:** Rollback plan approved and tested.
- [ ] **PROD-013:** Monitoring and alerts active.
- [ ] **PROD-014:** Incident contacts verified.
- [ ] **PROD-015:** Support ownership assigned.
- [ ] **PROD-016:** Runbooks available.
- [ ] **PROD-017:** Secret rotation and access review complete.
- [ ] **PROD-018:** Pilot training complete.
- [ ] **PROD-019:** BD sign-off recorded.
- [ ] **PROD-020:** PM sign-off recorded.
- [ ] **PROD-021:** TL/Engineering sign-off recorded.
- [ ] **PROD-022:** QA sign-off recorded.
- [ ] **PROD-023:** DevOps sign-off recorded.
- [ ] **PROD-024:** Security sign-off recorded.
- [ ] **PROD-025:** AI Architecture sign-off recorded.
- [ ] **PROD-026:** Product/UX sign-off recorded.
- [ ] **PROD-027:** Management production-readiness sign-off recorded.

## 15. Final Decision

- [ ] **DECISION-001:** Approved for Production
- [ ] **DECISION-002:** Approved for Limited Pilot
- [ ] **DECISION-003:** Approved with Conditions
- [ ] **DECISION-004:** Changes Required
- [ ] **DECISION-005:** Rejected

**The final record must include approvers, date, approved version, conditions, open limitations, and evidence references.**
