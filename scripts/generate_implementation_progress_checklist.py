"""Generate implementation progress checklist from the module-wise plan."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md"
OUT = ROOT / "MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md"

# Evidence-based status for current workspace (2026-08-10 MOD-000 session).
# Keys: exact task IDs. Values: ("done"|"partial"|"n/a"|"blocked", note)
STATUS: dict[str, tuple[str, str]] = {
    # MOD-000 main points
    "MOD-000-MP-001": ("done", "Baseline register docs + API entity gov_source_baselines"),
    "MOD-000-MP-002": ("done", "REQUIREMENT_MODULE_MAP.md + API requirement-mappings"),
    "MOD-000-MP-003": ("done", "docs/governance/adrs + API architecture-decisions"),
    "MOD-000-MP-004": ("done", "CHANGE_CONTROL.md + API change-requests"),
    "MOD-000-MP-005": ("done", "APPROVAL_RECORDS.md + API approvals"),
    # DB
    "MOD-000-DB-001": ("done", "Model + Alembic 20260810_0001; retention policy pending formal legal"),
    "MOD-000-DB-002": ("done", "Model + migration + unique constraints"),
    "MOD-000-DB-003": ("done", "Model + migration"),
    "MOD-000-DB-004": ("done", "Model + migration + idempotency unique"),
    "MOD-000-DB-005": ("done", "Model + migration"),
    # BE
    "MOD-000-BE-001": ("done", "domain.py + service.py typed application service"),
    "MOD-000-BE-002": ("done", "Human-only approve, transitions, optimistic version, CR idempotency"),
    "MOD-000-BE-003": ("n/a", "Outbox not required yet for governance stub; deferred MOD-020/350"),
    "MOD-000-BE-004": ("done", "Structured AppError codes mapped in FastAPI handler"),
    # API
    "MOD-000-API-001": ("done", "CRUD/query/transition + baseline history endpoint"),
    "MOD-000-API-002": ("done", "Pagination/filter/sort + concurrency/idempotency/problem errors"),
    "MOD-000-API-003": ("done", "OpenAPI models + ProblemDetails/BaselineRead examples + error responses"),
    # FE
    "MOD-000-FE-001": ("partial", "Baselines list with filter/pagination/empty/loading/error; saved views not yet"),
    "MOD-000-FE-002": ("partial", "Detail summary + audit history tabs; other related tabs deferred"),
    "MOD-000-FE-003": ("done", "Create/edit/transition forms with role gates and stale-version handling"),
    "MOD-000-FE-004": ("partial", "Skip link, labels, UTC dates, responsive layout; formal a11y audit pending"),
    # WF
    "MOD-000-WF-001": ("done", "docs/governance/WORKFLOW.md defines triggers/owners/statuses/approvals/closure"),
    "MOD-000-WF-002": ("n/a", "No durable waits/AI in MOD-000; FastAPI owns mutations (WORKFLOW.md)"),
    "MOD-000-WF-003": ("done", "Event/outbox/idempotency/correlation/retry/DLQ rules defined; runtime outbox deferred MOD-020"),
    "MOD-000-WF-004": ("n/a", "Notifications deferred to MOD-440 (WORKFLOW.md)"),
    # SEC
    "MOD-000-SEC-001": ("partial", "Org-scoped header principal + human-approve gate; full RBAC deferred MOD-110/120"),
    "MOD-000-SEC-002": ("partial", "App-level org filter + RLS SQL in migration; live GUC/RLS tests not run"),
    "MOD-000-SEC-003": ("partial", "Audit payload_redacted + no secrets in .env.example; broader redaction plumbing later"),
    "MOD-000-SEC-004": ("partial", "Audit on create/update/transition/approval; not all action types yet"),
    # QA
    "MOD-000-QA-001": ("done", "tests/unit/governance/test_domain.py"),
    "MOD-000-QA-002": ("done", "tests/integration/governance/test_governance_api.py"),
    "MOD-000-QA-003": ("partial", "Agent approve negative + org list isolation; full RBAC matrix pending"),
    "MOD-000-QA-004": ("n/a", "No Temporal/agent/integration capabilities in this module stub"),
    "MOD-000-QA-005": ("partial", "pytest/ruff/mypy passed; alembic/frontend/security scan not run"),
    # DOC
    "MOD-000-DOC-001": ("partial", "Module README, data dictionary, governance docs; full audit catalog pending"),
    "MOD-000-DOC-002": ("done", "README limitations + VERIFICATION.md"),
    # AC
    "MOD-000-AC-001": ("partial", "SoT candidates registered; human approval of BL-SRS-001 still PENDING"),
    "MOD-000-AC-002": ("done", "Documented and enforced for approved records"),
    "MOD-000-AC-003": ("done", "REQUIREMENT_MODULE_MAP.md published"),
    "MOD-000-AC-900": ("done", "No Critical/High defects filed against module"),
    "MOD-000-AC-901": ("blocked", "Requires named human owner approval"),
    # MOD-010 partial scaffold overlap
    "MOD-010-MP-001": ("done", "Monorepo layout documented + present under apps/, packages/, migrations/, tests/"),
    "MOD-010-MP-002": ("done", ".python-version 3.12 + .nvmrc 22 + engines"),
    "MOD-010-MP-003": ("done", "uv.lock + npm package-lock; pnpm deferred (host EPERM)"),
    "MOD-010-MP-004": ("done", "compose up healthy; alembic upgrade head -> 20260810_0001"),
    "MOD-010-MP-005": ("done", "ruff + next lint configured"),
    "MOD-010-MP-006": ("done", "mypy strict for masms_api"),
    "MOD-010-MP-007": ("done", "pytest suite + web build as verification"),
    "MOD-010-MP-008": ("done", ".github/workflows/ci.yml"),
    "MOD-010-DB-001": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-002": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-003": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-004": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-005": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-006": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-007": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-008": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-001": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-002": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-003": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-004": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-API-001": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-API-002": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-API-003": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-001": ("n/a", "No MOD-010 UI; web app serves MOD-000 — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-002": ("n/a", "No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-003": ("n/a", "No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-004": ("n/a", "No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-WF-001": ("n/a", "Dev workflow documented as start commands — not business WF"),
    "MOD-010-WF-002": ("n/a", "Workers are placeholders only"),
    "MOD-010-WF-003": ("n/a", "No MOD-010 domain events"),
    "MOD-010-WF-004": ("n/a", "No MOD-010 notifications"),
    "MOD-010-SEC-001": ("n/a", "No MOD-010 tenant resources"),
    "MOD-010-SEC-002": ("n/a", "No MOD-010 RLS resources"),
    "MOD-010-SEC-003": ("done", ".env.example only; .gitignore excludes .env/.env.local"),
    "MOD-010-SEC-004": ("n/a", "No MOD-010 audit entity"),
    "MOD-010-QA-001": ("n/a", "No MOD-010 domain unit tests"),
    "MOD-010-QA-002": ("n/a", "No MOD-010 API module"),
    "MOD-010-QA-003": ("n/a", "No MOD-010 authz surface"),
    "MOD-010-QA-004": ("n/a", "No MOD-010 WF/agent tests"),
    "MOD-010-QA-005": ("done", "scripts/dev-check.* runs ruff/mypy/pytest/web lint/build"),
    "MOD-010-DOC-001": ("done", "docs/modules/MOD-010/README.md"),
    "MOD-010-DOC-002": ("done", "VERIFICATION.md + TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-AC-001": ("done", "Start commands documented in MOD-010 README"),
    "MOD-010-AC-002": ("done", "CI run 31386826793 success on b9038a9 (main)"),
    "MOD-010-AC-003": ("done", "No real secrets in examples"),
    "MOD-010-AC-900": ("done", "No Critical/High tooling defects filed"),
    "MOD-010-AC-901": ("blocked", "Human owner approval required"),
    "MOD-020-MP-001": ("done", "kernel/ids.py NewType brands"),
    "MOD-020-MP-002": ("done", "kernel/actor.py ActorContext"),
    "MOD-020-MP-003": ("done", "kernel/tenant.py TenantContext"),
    "MOD-020-MP-004": ("done", "kernel/errors.py AppError hierarchy"),
    "MOD-020-MP-005": ("done", "kernel/uow.py SqlAlchemyUnitOfWork"),
    "MOD-020-MP-006": ("done", "sys_outbox_messages + enqueue_outbox"),
    "MOD-020-MP-007": ("done", "application/problem+json via kernel/problem.py"),
    "MOD-020-MP-008": ("done", "kernel/pagination.py PageMeta helpers"),
    "MOD-020-MP-009": ("done", "kernel/concurrency.py assert_expected_version"),
    "MOD-020-DB-001": ("done", "DATA_CONVENTIONS.md — typed IDs are brands, not tables"),
    "MOD-020-DB-002": ("done", "DATA_CONVENTIONS.md actor kind conventions"),
    "MOD-020-DB-003": ("done", "DATA_CONVENTIONS.md tenant scope conventions"),
    "MOD-020-DB-004": ("done", "DATA_CONVENTIONS.md errors are ephemeral API contracts"),
    "MOD-020-DB-005": ("done", "UoW is session contract — no dedicated table"),
    "MOD-020-DB-006": ("done", "migration 20260810_0002 sys_outbox_messages + RLS"),
    "MOD-020-DB-007": ("done", "problem details are response contract, not a table"),
    "MOD-020-DB-008": ("done", "pagination meta is response contract, not a table"),
    "MOD-020-DB-009": ("done", "version columns already on entities; helper shared"),
    "MOD-020-BE-001": ("partial", "kernel + governance uses UoW/outbox/helpers"),
    "MOD-020-BE-002": ("partial", "concurrency+approval rules via helpers; full authz later"),
    "MOD-020-BE-003": ("partial", "outbox enqueue on baseline create; publisher runtime pending"),
    "MOD-020-BE-004": ("done", "structured errors via kernel + FastAPI handler"),
    "MOD-020-API-002": ("partial", "problem+json + paging/concurrency shared; full OpenAPI polish pending"),
    "MOD-020-API-003": ("partial", "ProblemDetails schema examples updated"),
    "MOD-020-FE-001": ("n/a", "kernel library — no entity UI"),
    "MOD-020-FE-002": ("n/a", "kernel library — no entity UI"),
    "MOD-020-FE-003": ("n/a", "kernel library — no entity UI"),
    "MOD-020-FE-004": ("n/a", "kernel library — no entity UI"),
    "MOD-020-WF-002": ("partial", "boundary documented; Temporal/LangGraph not wired yet"),
    "MOD-020-WF-003": ("partial", "outbox table+enqueue; consumer/publisher runtime pending"),
    "MOD-020-SEC-002": ("partial", "outbox RLS + tenant context shape"),
    "MOD-020-QA-001": ("done", "tests/unit/kernel"),
    "MOD-020-QA-002": ("partial", "governance API still green with outbox/problem+json"),
    "MOD-020-QA-005": ("done", "ruff/mypy/pytest + alembic upgrade head"),
    "MOD-020-DOC-001": ("partial", "docs/modules/MOD-020/README.md"),
    "MOD-020-DOC-002": ("done", "DATA_CONVENTIONS + VERIFICATION"),
    "MOD-020-AC-001": ("partial", "RequestContext in kernel; governance wired"),
    "MOD-020-AC-002": ("partial", "UoW/API boundary documented; not yet enforced platform-wide"),
    "MOD-020-AC-003": ("partial", "problem+json + shared PageMeta"),
    "MOD-020-AC-900": ("done", "No Critical/High kernel defects filed"),
    "MOD-020-AC-901": ("blocked", "Human owner approval required"),
    "MOD-030-MP-001": ("done", "Environment enum + config/environments examples"),
    "MOD-030-MP-002": ("done", "SecretBackend local + AWS Secrets Manager fail-closed stub"),
    "MOD-030-MP-003": ("done", "CI concurrency + junit/build-identity artifacts"),
    "MOD-030-MP-004": ("done", "deploy-staging.yml dry-run skeleton"),
    "MOD-030-MP-005": ("done", "deploy-production.yml + check_production_gate.py"),
    "MOD-030-MP-006": ("done", "infra/terraform Secrets Manager skeleton"),
    "MOD-030-DB-001": ("n/a", "No env matrix table — config files"),
    "MOD-030-DB-002": ("n/a", "Secrets in AWS Secrets Manager / GH Environments — not DB"),
    "MOD-030-DB-003": ("n/a", "CI is GitHub Actions — not DB"),
    "MOD-030-DB-004": ("n/a", "Staging deploy is workflow — not DB"),
    "MOD-030-DB-005": ("n/a", "Prod gate is workflow/script — not DB"),
    "MOD-030-DB-006": ("n/a", "IaC is Terraform files — not DB"),
    "MOD-030-BE-001": ("n/a", "Platform helpers only; see TEMPLATE_TASK_RATIONALE"),
    "MOD-030-BE-002": ("n/a", "No MOD-030 entity mutations"),
    "MOD-030-BE-003": ("n/a", "No MOD-030 outbox entity"),
    "MOD-030-BE-004": ("n/a", "No MOD-030 entity API errors"),
    "MOD-030-API-001": ("n/a", "No MOD-030 CRUD API"),
    "MOD-030-API-002": ("n/a", "No MOD-030 CRUD API"),
    "MOD-030-API-003": ("n/a", "No MOD-030 CRUD API"),
    "MOD-030-FE-001": ("n/a", "No MOD-030 UI"),
    "MOD-030-FE-002": ("n/a", "No MOD-030 UI"),
    "MOD-030-FE-003": ("n/a", "No MOD-030 UI"),
    "MOD-030-FE-004": ("n/a", "No MOD-030 UI"),
    "MOD-030-WF-001": ("n/a", "Deploy via GitHub Actions — not Temporal WF"),
    "MOD-030-WF-002": ("n/a", "No Temporal/LangGraph in MOD-030"),
    "MOD-030-WF-003": ("n/a", "No MOD-030 domain events"),
    "MOD-030-WF-004": ("n/a", "No MOD-030 notifications"),
    "MOD-030-SEC-001": ("partial", "GitHub Environment + prod gate; Auth0 later"),
    "MOD-030-SEC-002": ("n/a", "No MOD-030 tenant tables"),
    "MOD-030-SEC-003": ("done", "Examples only; prod forbids local_env backend"),
    "MOD-030-SEC-004": ("n/a", "No MOD-030 audit entity"),
    "MOD-030-QA-001": ("done", "tests/unit/platform"),
    "MOD-030-QA-002": ("n/a", "No MOD-030 API module"),
    "MOD-030-QA-003": ("n/a", "No MOD-030 tenant surface"),
    "MOD-030-QA-004": ("n/a", "No MOD-030 Temporal/agent tests"),
    "MOD-030-QA-005": ("done", "ruff/mypy/pytest + gate script smoke"),
    "MOD-030-DOC-001": ("done", "docs/modules/MOD-030/README.md"),
    "MOD-030-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-030-AC-001": ("partial", "Matrix + secret backend rules; live Secrets Manager not wired"),
    "MOD-030-AC-002": ("done", "Production workflow requires confirm+approver+reason+sha"),
    "MOD-030-AC-003": ("done", "CI build-identity artifact keyed by git sha"),
    "MOD-030-AC-900": ("done", "No Critical/High MOD-030 defects filed"),
    "MOD-030-AC-901": ("blocked", "Human owner approval required"),
    "MOD-040-MP-001": ("done", "ops_audit_logs + append-only writer"),
    "MOD-040-MP-002": ("done", "ops_activity_events"),
    "MOD-040-MP-003": ("done", "ops_status_history"),
    "MOD-040-MP-004": ("done", "ops_agent_runs + API"),
    "MOD-040-MP-005": ("done", "ops_integration_events model/writer"),
    "MOD-040-MP-006": ("done", "TracingStub; real OTEL SDK deferred"),
    "MOD-040-MP-007": ("done", "/health/live and /health/ready"),
    "MOD-040-DB-001": ("done", "migration 20260810_0003 ops_audit_logs"),
    "MOD-040-DB-002": ("done", "ops_activity_events"),
    "MOD-040-DB-003": ("done", "ops_status_history"),
    "MOD-040-DB-004": ("done", "ops_agent_runs"),
    "MOD-040-DB-005": ("done", "ops_integration_events"),
    "MOD-040-DB-006": ("n/a", "OTEL is telemetry, not a table"),
    "MOD-040-DB-007": ("n/a", "Health checks are endpoints"),
    "MOD-040-BE-001": ("done", "ObservabilityWriter + ObservabilityService"),
    "MOD-040-BE-002": ("partial", "tenant scope + audit delete blocked"),
    "MOD-040-BE-003": ("partial", "writer exists; broker publish deferred"),
    "MOD-040-BE-004": ("done", "problem+json via shared handler"),
    "MOD-040-API-001": ("partial", "read audit/activity + agent-run actions"),
    "MOD-040-API-002": ("partial", "paging on audit/activity"),
    "MOD-040-API-003": ("partial", "schemas present; OpenAPI polish pending"),
    "MOD-040-FE-001": ("n/a", "ops UI deferred — see TEMPLATE_TASK_RATIONALE"),
    "MOD-040-FE-002": ("n/a", "ops UI deferred"),
    "MOD-040-FE-003": ("n/a", "ops UI deferred"),
    "MOD-040-FE-004": ("n/a", "ops UI deferred"),
    "MOD-040-WF-001": ("n/a", "no Temporal alert WF in M1"),
    "MOD-040-WF-002": ("n/a", "no Temporal/LangGraph in M1"),
    "MOD-040-WF-003": ("partial", "correlation on events; SNS consumer deferred"),
    "MOD-040-WF-004": ("n/a", "no alert notifications in M1"),
    "MOD-040-SEC-001": ("partial", "org scope in service queries"),
    "MOD-040-SEC-002": ("done", "RLS policies on ops_* tables"),
    "MOD-040-SEC-003": ("done", "redact_mapping for secrets"),
    "MOD-040-SEC-004": ("done", "audit write on agent run start"),
    "MOD-040-QA-001": ("done", "tests/unit/observability"),
    "MOD-040-QA-002": ("done", "tests/integration/observability"),
    "MOD-040-QA-003": ("partial", "audit delete negative test"),
    "MOD-040-QA-004": ("n/a", "no Temporal/perf suite in M1"),
    "MOD-040-QA-005": ("done", "ruff/mypy/pytest + alembic when Docker up"),
    "MOD-040-DOC-001": ("done", "docs/modules/MOD-040/README.md"),
    "MOD-040-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-040-AC-001": ("partial", "ops actions write actor-linked audit/activity"),
    "MOD-040-AC-002": ("done", "DELETE audit-logs returns forbidden"),
    "MOD-040-AC-003": ("done", "redaction verified in tests"),
    "MOD-040-AC-900": ("done", "No Critical/High MOD-040 defects filed"),
    "MOD-040-AC-901": ("blocked", "Human owner approval required"),
    "MOD-100-MP-001": ("done", "org_organizations + create/list API"),
    "MOD-100-MP-002": ("done", "org_actors"),
    "MOD-100-MP-003": ("done", "org_human_users"),
    "MOD-100-MP-004": ("done", "org_agents + supervisor rule"),
    "MOD-100-MP-005": ("done", "org_roles"),
    "MOD-100-MP-006": ("done", "org_departments"),
    "MOD-100-MP-007": ("done", "org_teams"),
    "MOD-100-MP-008": ("done", "org_team_members"),
    "MOD-100-MP-009": ("done", "org_reporting_lines"),
    "MOD-100-DB-001": ("done", "migration 20260810_0004 org_organizations"),
    "MOD-100-DB-002": ("done", "org_actors"),
    "MOD-100-DB-003": ("done", "org_human_users"),
    "MOD-100-DB-004": ("done", "org_agents"),
    "MOD-100-DB-005": ("done", "org_roles"),
    "MOD-100-DB-006": ("done", "org_departments"),
    "MOD-100-DB-007": ("done", "org_teams"),
    "MOD-100-DB-008": ("done", "org_team_members"),
    "MOD-100-DB-009": ("done", "org_reporting_lines"),
    "MOD-100-BE-001": ("done", "IdentityService"),
    "MOD-100-BE-002": ("partial", "supervisor + tenant checks"),
    "MOD-100-BE-003": ("partial", "org create outbox enqueue"),
    "MOD-100-BE-004": ("done", "problem+json via shared handler"),
    "MOD-100-API-001": ("done", "/api/v1/identity CRUD-lite endpoints"),
    "MOD-100-API-002": ("partial", "paging on orgs/actors/humans/agents"),
    "MOD-100-API-003": ("partial", "schemas present"),
    "MOD-100-FE-001": ("n/a", "FE deferred — TEMPLATE_TASK_RATIONALE"),
    "MOD-100-FE-002": ("n/a", "FE deferred"),
    "MOD-100-FE-003": ("n/a", "FE deferred"),
    "MOD-100-FE-004": ("n/a", "FE deferred"),
    "MOD-100-WF-001": ("n/a", "no Temporal WF in M1"),
    "MOD-100-WF-002": ("n/a", "no Temporal/LangGraph in M1"),
    "MOD-100-WF-003": ("partial", "outbox on org create"),
    "MOD-100-WF-004": ("n/a", "no identity notifications in M1"),
    "MOD-100-SEC-001": ("partial", "org scope via headers/context"),
    "MOD-100-SEC-002": ("done", "RLS on org_* tables"),
    "MOD-100-SEC-003": ("partial", "no secrets in identity payloads"),
    "MOD-100-SEC-004": ("done", "audit on org/human/agent create"),
    "MOD-100-QA-001": ("done", "tests/unit/identity"),
    "MOD-100-QA-002": ("done", "tests/integration/identity"),
    "MOD-100-QA-003": ("partial", "supervisor negative covered in domain tests"),
    "MOD-100-QA-004": ("n/a", "no Temporal suite"),
    "MOD-100-QA-005": ("done", "ruff/mypy/pytest + alembic"),
    "MOD-100-DOC-001": ("done", "docs/modules/MOD-100/README.md"),
    "MOD-100-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-100-AC-001": ("partial", "entities resolve to actor_id"),
    "MOD-100-AC-002": ("done", "active agent requires active human supervisor"),
    "MOD-100-AC-003": ("done", "distinct actor rows for human vs agent"),
    "MOD-100-AC-900": ("done", "No Critical/High MOD-100 defects filed"),
    "MOD-100-AC-901": ("blocked", "Human owner approval required"),
    "MOD-110-MP-001": ("done", "IdentityProvider + Auth0 fail-closed + local sessions"),
    "MOD-110-MP-002": ("done", "opaque SHA-256 token hash validation"),
    "MOD-110-MP-003": ("done", "auth_sessions create/me/revoke"),
    "MOD-110-MP-004": ("done", "auth_mfa_challenges + verify"),
    "MOD-110-MP-005": ("done", "step-up assert + assurance gate"),
    "MOD-110-MP-006": ("done", "client invitations + pending uniqueness"),
    "MOD-110-MP-007": ("done", "service identities + client_secret once"),
    "MOD-110-DB-001": ("partial", "IdP config via settings; no IdP table"),
    "MOD-110-DB-002": ("done", "token_hash on sessions/invites/svc"),
    "MOD-110-DB-003": ("done", "migration 20260810_0005 auth_sessions + RLS"),
    "MOD-110-DB-004": ("done", "auth_mfa_challenges"),
    "MOD-110-DB-005": ("partial", "assurance_level on session; no separate step-up table"),
    "MOD-110-DB-006": ("done", "auth_client_invitations + pending unique (PG)"),
    "MOD-110-DB-007": ("done", "auth_service_identities"),
    "MOD-110-BE-001": ("done", "AuthService"),
    "MOD-110-BE-002": ("partial", "org scope + assurance gates; full RBAC deferred MOD-120"),
    "MOD-110-BE-003": ("n/a", "no auth outbox publisher events in M1"),
    "MOD-110-BE-004": ("done", "problem+json via shared handler"),
    "MOD-110-API-001": ("done", "/api/v1/auth endpoints"),
    "MOD-110-API-002": ("partial", "CRUD-lite; paging not needed for M1 auth actions"),
    "MOD-110-API-003": ("partial", "schemas present"),
    "MOD-110-FE-001": ("n/a", "FE deferred — TEMPLATE_TASK_RATIONALE"),
    "MOD-110-FE-002": ("n/a", "FE deferred"),
    "MOD-110-FE-003": ("n/a", "FE deferred"),
    "MOD-110-FE-004": ("n/a", "FE deferred"),
    "MOD-110-WF-001": ("n/a", "no Temporal WF in M1"),
    "MOD-110-WF-002": ("n/a", "no Temporal/LangGraph in M1"),
    "MOD-110-WF-003": ("n/a", "no auth domain events in M1"),
    "MOD-110-WF-004": ("n/a", "invitation email delivery deferred"),
    "MOD-110-SEC-001": ("partial", "bearer session + header stub; RBAC MOD-120"),
    "MOD-110-SEC-002": ("done", "RLS on auth_* tables"),
    "MOD-110-SEC-003": ("done", "secrets hashed; debug MFA only local/test"),
    "MOD-110-SEC-004": ("done", "audit on session/invite/svc/mfa"),
    "MOD-110-QA-001": ("done", "tests/unit/auth"),
    "MOD-110-QA-002": ("done", "tests/integration/auth"),
    "MOD-110-QA-003": ("partial", "revoke without MFA + cross-org session denied"),
    "MOD-110-QA-004": ("n/a", "no Temporal suite"),
    "MOD-110-QA-005": ("done", "ruff/mypy/pytest + alembic"),
    "MOD-110-DOC-001": ("done", "docs/modules/MOD-110/README.md"),
    "MOD-110-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-110-AC-001": ("partial", "local bearer sessions; Auth0 JWKS pending"),
    "MOD-110-AC-002": ("done", "assurance gate for privileged revoke/step-up"),
    "MOD-110-AC-003": ("done", "immediate session revoke"),
    "MOD-110-AC-900": ("done", "No Critical/High MOD-110 defects filed"),
    "MOD-110-AC-901": ("blocked", "Human owner approval required"),
    "MOD-120-MP-001": ("done", "auth_permissions"),
    "MOD-120-MP-002": ("done", "org_role_permissions"),
    "MOD-120-MP-003": ("done", "org_project_members soft project_id"),
    "MOD-120-MP-004": ("done", "org_module_access"),
    "MOD-120-MP-005": ("done", "org_document_access"),
    "MOD-120-MP-006": ("done", "org_approval_authorities"),
    "MOD-120-MP-007": ("done", "RLS on access tables + apply_tenant_rls"),
    "MOD-120-MP-008": ("done", "org_access_reviews"),
    "MOD-120-DB-001": ("done", "migration 20260810_0006 auth_permissions"),
    "MOD-120-DB-002": ("done", "org_role_permissions"),
    "MOD-120-DB-003": ("done", "org_project_members"),
    "MOD-120-DB-004": ("done", "org_module_access"),
    "MOD-120-DB-005": ("done", "org_document_access"),
    "MOD-120-DB-006": ("done", "org_approval_authorities"),
    "MOD-120-DB-007": ("done", "Postgres RLS policies on access tables"),
    "MOD-120-DB-008": ("done", "org_access_reviews"),
    "MOD-120-BE-001": ("done", "AccessService"),
    "MOD-120-BE-002": ("partial", "deny-by-default checks + membership; actor role auto-resolve deferred"),
    "MOD-120-BE-003": ("n/a", "no access outbox events in M1"),
    "MOD-120-BE-004": ("done", "problem+json via shared handler"),
    "MOD-120-API-001": ("done", "/api/v1/access endpoints + permission check"),
    "MOD-120-API-002": ("partial", "CRUD-lite; paging deferred"),
    "MOD-120-API-003": ("partial", "schemas present"),
    "MOD-120-FE-001": ("n/a", "FE deferred — TEMPLATE_TASK_RATIONALE"),
    "MOD-120-FE-002": ("n/a", "FE deferred"),
    "MOD-120-FE-003": ("n/a", "FE deferred"),
    "MOD-120-FE-004": ("n/a", "FE deferred"),
    "MOD-120-WF-001": ("n/a", "no Temporal WF in M1"),
    "MOD-120-WF-002": ("n/a", "no Temporal/LangGraph in M1"),
    "MOD-120-WF-003": ("n/a", "no access domain events in M1"),
    "MOD-120-WF-004": ("n/a", "no access-review notifications in M1"),
    "MOD-120-SEC-001": ("partial", "permission + membership + client scope helpers"),
    "MOD-120-SEC-002": ("done", "RLS + apply_tenant_rls GUC bind"),
    "MOD-120-SEC-003": ("partial", "audit payloads without secrets"),
    "MOD-120-SEC-004": ("done", "audit on grants/reviews"),
    "MOD-120-QA-001": ("done", "tests/unit/access"),
    "MOD-120-QA-002": ("done", "tests/integration/access"),
    "MOD-120-QA-003": ("done", "deny-by-default + membership negative"),
    "MOD-120-QA-004": ("n/a", "no Temporal suite"),
    "MOD-120-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-120-DOC-001": ("done", "docs/modules/MOD-120/README.md"),
    "MOD-120-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-120-AC-001": ("partial", "assert_client_scope when both client IDs set"),
    "MOD-120-AC-002": ("done", "project checks require membership"),
    "MOD-120-AC-003": ("done", "FE deferred; API is authoritative"),
    "MOD-120-AC-900": ("done", "No Critical/High MOD-120 defects filed"),
    "MOD-120-AC-901": ("blocked", "Human owner approval required"),
    "MOD-130-MP-001": ("done", "org_skills"),
    "MOD-130-MP-002": ("done", "org_actor_skills"),
    "MOD-130-MP-003": ("done", "org_availability_windows"),
    "MOD-130-MP-004": ("done", "org_capacity_allocations"),
    "MOD-130-MP-005": ("done", "org_business_calendars"),
    "MOD-130-MP-006": ("done", "org_holidays"),
    "MOD-130-MP-007": ("done", "org_leave_periods"),
    "MOD-130-MP-008": ("done", "org_oncall_schedules"),
    "MOD-130-DB-001": ("done", "migration 20260810_0007 org_skills"),
    "MOD-130-DB-002": ("done", "org_actor_skills"),
    "MOD-130-DB-003": ("done", "org_availability_windows"),
    "MOD-130-DB-004": ("done", "org_capacity_allocations"),
    "MOD-130-DB-005": ("done", "org_business_calendars"),
    "MOD-130-DB-006": ("done", "org_holidays"),
    "MOD-130-DB-007": ("done", "org_leave_periods"),
    "MOD-130-DB-008": ("done", "org_oncall_schedules"),
    "MOD-130-BE-001": ("done", "CapacityService"),
    "MOD-130-BE-002": ("partial", "validation + org scope; RBAC gates deferred to callers"),
    "MOD-130-BE-003": ("n/a", "no capacity outbox in M1"),
    "MOD-130-BE-004": ("done", "problem+json via shared handler"),
    "MOD-130-API-001": ("done", "/api/v1/capacity + evaluate/SLA helpers"),
    "MOD-130-API-002": ("partial", "CRUD-lite"),
    "MOD-130-API-003": ("partial", "schemas present"),
    "MOD-130-FE-001": ("n/a", "FE deferred"),
    "MOD-130-FE-002": ("n/a", "FE deferred"),
    "MOD-130-FE-003": ("n/a", "FE deferred"),
    "MOD-130-FE-004": ("n/a", "FE deferred"),
    "MOD-130-WF-001": ("n/a", "no Temporal WF in M1"),
    "MOD-130-WF-002": ("n/a", "no Temporal/LangGraph in M1"),
    "MOD-130-WF-003": ("n/a", "no capacity domain events in M1"),
    "MOD-130-WF-004": ("n/a", "no capacity notifications in M1"),
    "MOD-130-SEC-001": ("partial", "org-scoped writes"),
    "MOD-130-SEC-002": ("done", "RLS on capacity tables"),
    "MOD-130-SEC-003": ("done", "leave notes not audited"),
    "MOD-130-SEC-004": ("partial", "audit on skill create"),
    "MOD-130-QA-001": ("done", "tests/unit/capacity"),
    "MOD-130-QA-002": ("done", "tests/integration/capacity"),
    "MOD-130-QA-003": ("partial", "org-scoped via context"),
    "MOD-130-QA-004": ("n/a", "no Temporal suite"),
    "MOD-130-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-130-DOC-001": ("done", "docs/modules/MOD-130/README.md"),
    "MOD-130-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-130-AC-001": ("done", "evaluate-assignment checks skill/capacity/leave/calendar"),
    "MOD-130-AC-002": ("done", "sla/business-days uses calendar holidays + timezone"),
    "MOD-130-AC-003": ("done", "leave notes excluded from audit payload"),
    "MOD-130-AC-900": ("done", "No Critical/High MOD-130 defects filed"),
    "MOD-130-AC-901": ("blocked", "Human owner approval required"),
    "MOD-140-MP-001": ("done", "cfg_workflow_definitions"),
    "MOD-140-MP-002": ("done", "cfg_status_definitions"),
    "MOD-140-MP-003": ("done", "cfg_transition_rules"),
    "MOD-140-MP-004": ("done", "cfg_followup_rules"),
    "MOD-140-MP-005": ("done", "cfg_reminder_rules"),
    "MOD-140-MP-006": ("done", "cfg_escalation_rules"),
    "MOD-140-MP-007": ("done", "cfg_approval_workflows"),
    "MOD-140-MP-008": ("done", "cfg_configuration_versions lifecycle"),
    "MOD-140-DB-001": ("done", "migration 20260811_0008 workflows"),
    "MOD-140-DB-002": ("done", "cfg_status_definitions"),
    "MOD-140-DB-003": ("done", "cfg_transition_rules"),
    "MOD-140-DB-004": ("done", "cfg_followup_rules"),
    "MOD-140-DB-005": ("done", "cfg_reminder_rules"),
    "MOD-140-DB-006": ("done", "cfg_escalation_rules"),
    "MOD-140-DB-007": ("done", "cfg_approval_workflows"),
    "MOD-140-DB-008": ("done", "cfg_configuration_versions"),
    "MOD-140-BE-001": ("done", "ConfigAdminService"),
    "MOD-140-BE-002": ("done", "draft-only edits; approve/activate/rollback gates"),
    "MOD-140-BE-003": ("partial", "outbox on activate; publisher deferred"),
    "MOD-140-BE-004": ("done", "problem+json via shared handler"),
    "MOD-140-API-001": ("done", "/api/v1/config endpoints + live transition check"),
    "MOD-140-API-002": ("partial", "CRUD-lite; paging deferred"),
    "MOD-140-API-003": ("partial", "schemas present"),
    "MOD-140-FE-001": ("n/a", "FE deferred"),
    "MOD-140-FE-002": ("n/a", "FE deferred"),
    "MOD-140-FE-003": ("n/a", "FE deferred"),
    "MOD-140-FE-004": ("n/a", "FE deferred"),
    "MOD-140-WF-001": ("partial", "rules stored; Temporal execution deferred"),
    "MOD-140-WF-002": ("n/a", "no Temporal/LangGraph runtime in M1"),
    "MOD-140-WF-003": ("partial", "outbox on activate"),
    "MOD-140-WF-004": ("n/a", "reminder channel execution deferred"),
    "MOD-140-SEC-001": ("partial", "org-scoped; RBAC matrix deferred to callers"),
    "MOD-140-SEC-002": ("done", "RLS on cfg_* tables"),
    "MOD-140-SEC-003": ("partial", "audit without secrets"),
    "MOD-140-SEC-004": ("done", "audit on version lifecycle + workflow create"),
    "MOD-140-QA-001": ("done", "tests/unit/configadmin"),
    "MOD-140-QA-002": ("done", "tests/integration/configadmin"),
    "MOD-140-QA-003": ("partial", "draft edit denied after approve"),
    "MOD-140-QA-004": ("n/a", "no Temporal suite"),
    "MOD-140-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-140-DOC-001": ("done", "docs/modules/MOD-140/README.md"),
    "MOD-140-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-140-AC-001": ("done", "live check uses effective only"),
    "MOD-140-AC-002": ("done", "approve/activate/rollback + audit"),
    "MOD-140-AC-003": ("done", "draft cannot control live transitions"),
    "MOD-140-AC-900": ("done", "No Critical/High MOD-140 defects filed"),
    "MOD-140-AC-901": ("blocked", "Human owner approval required"),
    "MOD-200-MP-001": ("done", "crm_clients"),
    "MOD-200-MP-002": ("done", "crm_contacts + authority"),
    "MOD-200-MP-003": ("done", "crm_project_contacts"),
    "MOD-200-MP-004": ("done", "crm_communication_preferences"),
    "MOD-200-MP-005": ("done", "crm_duplicate_suggestions"),
    "MOD-200-MP-006": ("done", "crm_merge_history snapshot"),
    "MOD-200-DB-001": ("done", "migration 20260811_0009 crm_clients"),
    "MOD-200-DB-002": ("done", "crm_contacts"),
    "MOD-200-DB-003": ("done", "crm_project_contacts"),
    "MOD-200-DB-004": ("done", "crm_communication_preferences"),
    "MOD-200-DB-005": ("done", "crm_duplicate_suggestions"),
    "MOD-200-DB-006": ("done", "crm_merge_history"),
    "MOD-200-BE-001": ("done", "ClientsService"),
    "MOD-200-BE-002": ("partial", "org/client scope + validation"),
    "MOD-200-BE-003": ("partial", "outbox on client create"),
    "MOD-200-BE-004": ("done", "problem+json via shared handler"),
    "MOD-200-API-001": ("done", "/api/v1/clients endpoints"),
    "MOD-200-API-002": ("partial", "paging on client list"),
    "MOD-200-API-003": ("partial", "schemas present"),
    "MOD-200-FE-001": ("n/a", "FE deferred"),
    "MOD-200-FE-002": ("n/a", "FE deferred"),
    "MOD-200-FE-003": ("n/a", "FE deferred"),
    "MOD-200-FE-004": ("n/a", "FE deferred"),
    "MOD-200-WF-001": ("n/a", "no Temporal WF in M1"),
    "MOD-200-WF-002": ("n/a", "no Temporal/LangGraph in M1"),
    "MOD-200-WF-003": ("partial", "outbox on client create"),
    "MOD-200-WF-004": ("n/a", "preference channel delivery deferred"),
    "MOD-200-SEC-001": ("partial", "org + X-Client-Id isolation"),
    "MOD-200-SEC-002": ("done", "RLS on crm_* tables"),
    "MOD-200-SEC-003": ("partial", "notes not in merge audit beyond reason"),
    "MOD-200-SEC-004": ("done", "audit on create/merge"),
    "MOD-200-QA-001": ("done", "tests/unit/clients"),
    "MOD-200-QA-002": ("done", "tests/integration/clients"),
    "MOD-200-QA-003": ("done", "cross-client list isolation"),
    "MOD-200-QA-004": ("n/a", "no Temporal suite"),
    "MOD-200-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-200-DOC-001": ("done", "docs/modules/MOD-200/README.md"),
    "MOD-200-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-200-AC-001": ("done", "multiple contacts with authority levels"),
    "MOD-200-AC-002": ("done", "merge history snapshot preserved"),
    "MOD-200-AC-003": ("done", "tenant isolation + audit"),
    "MOD-200-AC-900": ("done", "No Critical/High MOD-200 defects filed"),
    "MOD-200-AC-901": ("blocked", "Human owner approval required"),
    "MOD-210-MP-001": ("done", "crm_queries"),
    "MOD-210-MP-002": ("done", "crm_opportunities"),
    "MOD-210-MP-003": ("done", "crm_qualification_answers"),
    "MOD-210-MP-004": ("done", "crm_query_sources"),
    "MOD-210-MP-005": ("done", "crm_query_status_history"),
    "MOD-210-MP-006": ("done", "first-response SLA fields"),
    "MOD-210-DB-001": ("done", "migration 20260811_0010 crm_queries"),
    "MOD-210-DB-002": ("done", "crm_opportunities"),
    "MOD-210-DB-003": ("done", "crm_qualification_answers"),
    "MOD-210-DB-004": ("done", "crm_query_sources"),
    "MOD-210-DB-005": ("done", "crm_query_status_history"),
    "MOD-210-DB-006": ("done", "sla_due_at/first_responded_at/sla_status"),
    "MOD-210-BE-001": ("done", "QueriesService"),
    "MOD-210-BE-002": ("done", "transition map + history"),
    "MOD-210-BE-003": ("partial", "outbox on create/convert"),
    "MOD-210-BE-004": ("done", "problem+json via shared handler"),
    "MOD-210-API-001": ("done", "/api/v1/queries endpoints"),
    "MOD-210-API-002": ("partial", "CRUD-lite"),
    "MOD-210-API-003": ("partial", "schemas present"),
    "MOD-210-FE-001": ("n/a", "FE deferred"),
    "MOD-210-FE-002": ("n/a", "FE deferred"),
    "MOD-210-FE-003": ("n/a", "FE deferred"),
    "MOD-210-FE-004": ("n/a", "FE deferred"),
    "MOD-210-WF-001": ("partial", "status history + SLA fields"),
    "MOD-210-WF-002": ("n/a", "Temporal deferred"),
    "MOD-210-WF-003": ("partial", "outbox on create/convert"),
    "MOD-210-WF-004": ("n/a", "notifications deferred"),
    "MOD-210-SEC-001": ("partial", "org/client scope"),
    "MOD-210-SEC-002": ("done", "RLS on crm query tables"),
    "MOD-210-SEC-003": ("partial", "original_message stored; audit omits body"),
    "MOD-210-SEC-004": ("done", "audit on create/transition/convert"),
    "MOD-210-QA-001": ("done", "tests/unit/queries"),
    "MOD-210-QA-002": ("done", "tests/integration/queries"),
    "MOD-210-QA-003": ("partial", "client scope checks in service"),
    "MOD-210-QA-004": ("n/a", "no Temporal suite"),
    "MOD-210-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-210-DOC-001": ("done", "docs/modules/MOD-210/README.md"),
    "MOD-210-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-210-AC-001": ("done", "one query row per inquiry"),
    "MOD-210-AC-002": ("done", "qualification answers + rationale"),
    "MOD-210-AC-003": ("done", "convert preserves message + qualification evidence"),
    "MOD-210-AC-900": ("done", "No Critical/High MOD-210 defects filed"),
    "MOD-210-AC-901": ("blocked", "Human owner approval required"),
    "MOD-220-MP-001": ("done", "com_conversations"),
    "MOD-220-MP-002": ("done", "com_messages"),
    "MOD-220-MP-003": ("done", "com_message_revisions"),
    "MOD-220-MP-004": ("done", "com_message_recipients"),
    "MOD-220-MP-005": ("done", "com_delivery_receipts"),
    "MOD-220-MP-006": ("done", "com_attachment_links"),
    "MOD-220-DB-001": ("done", "migration 20260811_0011 com_conversations"),
    "MOD-220-DB-002": ("done", "com_messages"),
    "MOD-220-DB-003": ("done", "com_message_revisions"),
    "MOD-220-DB-004": ("done", "com_message_recipients"),
    "MOD-220-DB-005": ("done", "com_delivery_receipts"),
    "MOD-220-DB-006": ("done", "com_attachment_links"),
    "MOD-220-BE-001": ("done", "CommsService"),
    "MOD-220-BE-002": ("done", "immutable sent + sensitive approval"),
    "MOD-220-BE-003": ("partial", "outbox on message send"),
    "MOD-220-BE-004": ("done", "problem+json via shared handler"),
    "MOD-220-API-001": ("done", "/api/v1/comms endpoints"),
    "MOD-220-API-002": ("partial", "CRUD-lite actions"),
    "MOD-220-API-003": ("partial", "schemas present"),
    "MOD-220-FE-001": ("n/a", "FE deferred"),
    "MOD-220-FE-002": ("n/a", "FE deferred"),
    "MOD-220-FE-003": ("n/a", "FE deferred"),
    "MOD-220-FE-004": ("n/a", "FE deferred"),
    "MOD-220-WF-001": ("partial", "draft/approve/send statuses"),
    "MOD-220-WF-002": ("n/a", "Temporal deferred"),
    "MOD-220-WF-003": ("partial", "outbox on send"),
    "MOD-220-WF-004": ("n/a", "notifications deferred"),
    "MOD-220-SEC-001": ("partial", "org/client scope"),
    "MOD-220-SEC-002": ("done", "RLS on com_* tables"),
    "MOD-220-SEC-003": ("partial", "audit omits body text"),
    "MOD-220-SEC-004": ("done", "audit on create/approve/send"),
    "MOD-220-QA-001": ("done", "tests/unit/comms"),
    "MOD-220-QA-002": ("done", "tests/integration/comms"),
    "MOD-220-QA-003": ("partial", "client scope checks in service"),
    "MOD-220-QA-004": ("n/a", "no Temporal/provider suite"),
    "MOD-220-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-220-DOC-001": ("done", "docs/modules/MOD-220/README.md"),
    "MOD-220-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-220-AC-001": ("done", "related_entity_type/id on conversation"),
    "MOD-220-AC-002": ("done", "restricted/confidential require approval"),
    "MOD-220-AC-003": ("done", "sent body/recipients/attachments immutable"),
    "MOD-220-AC-900": ("done", "No Critical/High MOD-220 defects filed"),
    "MOD-220-AC-901": ("blocked", "Human owner approval required"),
    "MOD-230-MP-001": ("done", "req_questionnaires"),
    "MOD-230-MP-002": ("done", "req_questionnaire_versions"),
    "MOD-230-MP-003": ("done", "req_answers"),
    "MOD-230-MP-004": ("done", "req_requirement_briefs"),
    "MOD-230-MP-005": ("done", "req_clarification_requests"),
    "MOD-230-MP-006": ("done", "req_completeness_scores"),
    "MOD-230-DB-001": ("done", "migration 20260811_0012 req_questionnaires"),
    "MOD-230-DB-002": ("done", "req_questionnaire_versions"),
    "MOD-230-DB-003": ("done", "req_answers"),
    "MOD-230-DB-004": ("done", "req_requirement_briefs"),
    "MOD-230-DB-005": ("done", "req_clarification_requests"),
    "MOD-230-DB-006": ("done", "req_completeness_scores"),
    "MOD-230-BE-001": ("done", "RequirementsService"),
    "MOD-230-BE-002": ("done", "95% completeness + gap owners + brief approve"),
    "MOD-230-BE-003": ("partial", "outbox on brief approve"),
    "MOD-230-BE-004": ("done", "problem+json via shared handler"),
    "MOD-230-API-001": ("done", "/api/v1/requirements endpoints"),
    "MOD-230-API-002": ("partial", "CRUD-lite actions"),
    "MOD-230-API-003": ("partial", "schemas present"),
    "MOD-230-FE-001": ("n/a", "FE deferred"),
    "MOD-230-FE-002": ("n/a", "FE deferred"),
    "MOD-230-FE-003": ("n/a", "FE deferred"),
    "MOD-230-FE-004": ("n/a", "FE deferred"),
    "MOD-230-WF-001": ("partial", "publish/answer/score/approve flow"),
    "MOD-230-WF-002": ("n/a", "Temporal deferred"),
    "MOD-230-WF-003": ("partial", "outbox on brief approve"),
    "MOD-230-WF-004": ("n/a", "notifications deferred"),
    "MOD-230-SEC-001": ("partial", "org/client scope"),
    "MOD-230-SEC-002": ("done", "RLS on req_* tables"),
    "MOD-230-SEC-003": ("partial", "audit omits answer body text"),
    "MOD-230-SEC-004": ("done", "audit on create/publish/score/approve"),
    "MOD-230-QA-001": ("done", "tests/unit/requirements"),
    "MOD-230-QA-002": ("done", "tests/integration/requirements"),
    "MOD-230-QA-003": ("partial", "client scope checks in service"),
    "MOD-230-QA-004": ("n/a", "no Temporal/LangGraph suite"),
    "MOD-230-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-230-DOC-001": ("done", "docs/modules/MOD-230/README.md"),
    "MOD-230-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-230-AC-001": ("done", "95% mandatory covered or unavailable"),
    "MOD-230-AC-002": ("done", "gap clarifications require owner"),
    "MOD-230-AC-003": ("done", "versioned brief + human approve"),
    "MOD-230-AC-900": ("done", "No Critical/High MOD-230 defects filed"),
    "MOD-230-AC-901": ("blocked", "Human owner approval required"),
    "MOD-240-MP-001": ("done", "prj_projects"),
    "MOD-240-MP-002": ("done", "prj_requirements"),
    "MOD-240-MP-003": ("done", "prj_requirement_versions"),
    "MOD-240-MP-004": ("done", "prj_business_rules"),
    "MOD-240-MP-005": ("done", "prj_acceptance_criteria"),
    "MOD-240-MP-006": ("done", "prj_assumptions"),
    "MOD-240-MP-007": ("done", "prj_constraints"),
    "MOD-240-MP-008": ("done", "prj_srs_baselines"),
    "MOD-240-DB-001": ("done", "migration 20260811_0013 prj_projects"),
    "MOD-240-DB-002": ("done", "prj_requirements"),
    "MOD-240-DB-003": ("done", "prj_requirement_versions"),
    "MOD-240-DB-004": ("done", "prj_business_rules"),
    "MOD-240-DB-005": ("done", "prj_acceptance_criteria"),
    "MOD-240-DB-006": ("done", "prj_assumptions"),
    "MOD-240-DB-007": ("done", "prj_constraints"),
    "MOD-240-DB-008": ("done", "prj_srs_baselines"),
    "MOD-240-BE-001": ("done", "ProjectsService"),
    "MOD-240-BE-002": ("done", "AC gate + SRS human approve + version immutability"),
    "MOD-240-BE-003": ("partial", "outbox on project create + SRS approve"),
    "MOD-240-BE-004": ("done", "problem+json via shared handler"),
    "MOD-240-API-001": ("done", "/api/v1/projects endpoints"),
    "MOD-240-API-002": ("partial", "CRUD-lite actions"),
    "MOD-240-API-003": ("partial", "schemas present"),
    "MOD-240-FE-001": ("n/a", "FE deferred"),
    "MOD-240-FE-002": ("n/a", "FE deferred"),
    "MOD-240-FE-003": ("n/a", "FE deferred"),
    "MOD-240-FE-004": ("n/a", "FE deferred"),
    "MOD-240-WF-001": ("partial", "approve/supersede flow"),
    "MOD-240-WF-002": ("n/a", "Temporal deferred"),
    "MOD-240-WF-003": ("partial", "outbox on project/SRS"),
    "MOD-240-WF-004": ("n/a", "notifications deferred"),
    "MOD-240-SEC-001": ("partial", "org/client/project scope"),
    "MOD-240-SEC-002": ("done", "RLS on prj_* tables"),
    "MOD-240-SEC-003": ("partial", "audit omits full statement bodies"),
    "MOD-240-SEC-004": ("done", "audit on create/approve"),
    "MOD-240-QA-001": ("done", "tests/unit/projects"),
    "MOD-240-QA-002": ("done", "tests/integration/projects"),
    "MOD-240-QA-003": ("partial", "client scope checks in service"),
    "MOD-240-QA-004": ("n/a", "no Temporal suite"),
    "MOD-240-QA-005": ("done", "ruff/mypy/pytest"),
    "MOD-240-DOC-001": ("done", "docs/modules/MOD-240/README.md"),
    "MOD-240-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-240-AC-001": ("done", "unique code + acceptance criteria on approve"),
    "MOD-240-AC-002": ("done", "SRS authoritative only after human approve"),
    "MOD-240-AC-003": ("done", "new versions + change_reason after v1"),
    "MOD-240-AC-900": ("done", "No Critical/High MOD-240 defects filed"),
    "MOD-240-AC-901": ("blocked", "Human owner approval required"),
}

def ascii_dash(text: str) -> str:
    return (
        text.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2011", "-")
        .replace("\ufffd", "-")
    )


def box(status: str) -> str:
    if status == "done":
        return "[x]"
    if status == "partial":
        return "[~]"
    if status == "n/a":
        return "[-]"
    if status == "blocked":
        return "[!]"
    return "[ ]"


def main() -> None:
    plan = ascii_dash(PLAN.read_text(encoding="utf-8"))
    module_header = re.compile(r"^### (MOD-\d{3}) - (.+)$", re.M)
    phase_header = re.compile(r"^## (Phase \d+ - .+)$", re.M)
    # Plan bold form is **MOD-000-MP-001:** (colon inside closing marks)
    task_re = re.compile(
        r"\*\*(MOD-\d{3}-(?:MP|DB|BE|API|FE|WF|SEC|QA|DOC|AC)-\d{3}):\*\*\s*(.+)"
    )
    req_re = re.compile(r"\*\*Requirement Mapping:\*\*\s*(.+)")
    dep_re = re.compile(r"\*\*Dependencies:\*\*\s*(.+)")
    purpose_re = re.compile(r"\*\*Purpose:\*\*\s*(.+)")

    matches = list(module_header.finditer(plan))
    phases = list(phase_header.finditer(plan))

    def current_phase(pos: int) -> str:
        cur = "Unscoped"
        for p in phases:
            if p.start() <= pos:
                cur = p.group(1)
            else:
                break
        return cur

    modules: list[dict] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(plan)
        body = plan[start:end]
        modules.append(
            {
                "id": m.group(1),
                "title": m.group(2).strip(),
                "phase": current_phase(start),
                "purpose": (purpose_re.search(body).group(1).strip() if purpose_re.search(body) else ""),
                "requirements": (req_re.search(body).group(1).strip() if req_re.search(body) else ""),
                "dependencies": (dep_re.search(body).group(1).strip() if dep_re.search(body) else ""),
                "tasks": task_re.findall(body),
            }
        )

    # Counts
    status_counts: Counter[str] = Counter()
    lines: list[str] = []
    lines.append("# MASMS Implementation Progress Checklist")
    lines.append("")
    lines.append("**Source:** `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md`")
    lines.append("**Companion evidence gate checklist:** `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md`")
    lines.append("**Last updated (workspace):** 2026-08-10")
    lines.append("**Rule:** checkmarks reflect repository evidence only; human Done approval is separate.")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("| Mark | Meaning |")
    lines.append("|---|---|")
    lines.append("| `[x]` | Done with evidence |")
    lines.append("| `[~]` | Partial / scaffold only |")
    lines.append("| `[-]` | N/A for current scope (deferred by design) |")
    lines.append("| `[!]` | Blocked (needs human or external dependency) |")
    lines.append("| `[ ]` | Not started |")
    lines.append("")
    lines.append("## Summary roll-up")
    lines.append("")
    lines.append("| Module | Phase | Tasks | Done | Partial | N/A | Blocked | Open | Module status |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")

    module_summaries: list[tuple[str, str, Counter[str], str]] = []
    for mod in modules:
        c: Counter[str] = Counter()
        for tid, _desc in mod["tasks"]:
            st = STATUS.get(tid, ("", ""))[0]
            key = st if st else "open"
            c[key] += 1
            status_counts[key] += 1
        total = len(mod["tasks"])
        if c["blocked"]:
            mod_status = "Blocked"
        elif c["done"] == total:
            mod_status = "Complete"
        elif c["done"] or c["partial"] or c["n/a"]:
            mod_status = "In progress"
        else:
            mod_status = "Not started"
        # Special-case MOD-000: not Complete because AC-901 blocked / FE open
        if mod["id"] == "MOD-000" and c["blocked"]:
            mod_status = "In progress (human approval blocked)"
        module_summaries.append((mod["id"], mod["phase"], c, mod_status))

    for mid, phase, c, mod_status in module_summaries:
        total = sum(c.values())
        lines.append(
            f"| {mid} | {phase} | {total} | {c['done']} | {c['partial']} | {c['n/a']} | {c['blocked']} | {c['open']} | {mod_status} |"
        )

    lines.append("")
    lines.append(
        f"**Totals:** {sum(status_counts.values())} tasks — "
        f"done {status_counts['done']}, partial {status_counts['partial']}, "
        f"n/a {status_counts['n/a']}, blocked {status_counts['blocked']}, open {status_counts['open']}"
    )
    lines.append("")
    lines.append("## Module index (plan order)")
    lines.append("")
    for i, mod in enumerate(modules, start=1):
        lines.append(f"{i}. [{mod['id']}](#{mod['id'].lower()}) — {mod['title']}")
    lines.append("")

    current_phase_name = None
    for mod in modules:
        if mod["phase"] != current_phase_name:
            current_phase_name = mod["phase"]
            lines.append(f"## {current_phase_name}")
            lines.append("")

        lines.append(f"### {mod['id']}")
        lines.append("")
        lines.append(f"**Title:** {mod['title']}  ")
        lines.append(f"**Purpose:** {mod['purpose']}  ")
        lines.append(f"**Requirements:** {mod['requirements']}  ")
        lines.append(f"**Dependencies:** {mod['dependencies']}")
        lines.append("")

        # Group by category
        groups: dict[str, list[tuple[str, str]]] = {}
        order = ["MP", "DB", "BE", "API", "FE", "WF", "SEC", "QA", "DOC", "AC"]
        labels = {
            "MP": "Main points",
            "DB": "Database / data design",
            "BE": "Backend",
            "API": "API",
            "FE": "Frontend",
            "WF": "Workflow / agent / events / notifications",
            "SEC": "Security / privacy / audit",
            "QA": "Testing / verification",
            "DOC": "Documentation",
            "AC": "Acceptance gate",
        }
        for tid, desc in mod["tasks"]:
            cat = tid.split("-")[2]
            groups.setdefault(cat, []).append((tid, desc.strip()))

        for cat in order:
            items = groups.get(cat)
            if not items:
                continue
            lines.append(f"#### {labels[cat]}")
            lines.append("")
            for tid, desc in items:
                st, note = STATUS.get(tid, ("", ""))
                mark = box(st)
                if note:
                    lines.append(f"- {mark} **{tid}:** {desc}  ")
                    lines.append(f"  - Evidence/note: {note}")
                else:
                    lines.append(f"- {mark} **{tid}:** {desc}")
            lines.append("")

        # Derived module Done checkbox (AC-901 style)
        lines.append(f"#### Module completion")
        lines.append("")
        if mod["id"] == "MOD-000":
            lines.append(
                f"- [!] **{mod['id']}-DONE:** Module marked Done before dependents  "
            )
            lines.append(
                "  - Evidence/note: Not Done — AC-901 human approval pending; FE deferred"
            )
        else:
            lines.append(f"- [ ] **{mod['id']}-DONE:** Module marked Done before dependents")
        lines.append("")

    lines.append("## Final MVP sequence (from plan)")
    lines.append("")
    finals = re.findall(r"\*\*(FINAL-\d{3}):\*\*\s*(.+)", plan)
    for tid, desc in finals:
        lines.append(f"- [ ] **{tid}:** {desc.strip()}")
    lines.append("")
    lines.append("## Cross-module release gates (from plan)")
    lines.append("")
    gates = re.findall(r"\*\*(GATE-\d{3}):\*\*\s*(.+)", plan)
    for tid, desc in gates:
        lines.append(f"- [ ] **{tid}:** {desc.strip()}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "Generated by `scripts/generate_implementation_progress_checklist.py`. "
        "Update the `STATUS` map in that script when work completes, then regenerate."
    )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} with {len(modules)} modules, {sum(len(m['tasks']) for m in modules)} tasks")
    print(dict(status_counts))


if __name__ == "__main__":
    main()
