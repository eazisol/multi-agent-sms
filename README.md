# Multi-Agent Software House Management System (MASMS)

Hybrid human-and-agent software-house management platform.  
Authoritative product inputs live under `Docs/`. Engineering rules live under `.cursor/rules/` and `AGENTS.md`.

## Current implementation status

| Module | Status |
|---|---|
| MOD-000 Governance | In progress (API + baselines UI). Human Done approval pending |
| MOD-010 Toolchain | Implementation draft (CI, compose, pins, check scripts). AC-901 pending |
| MOD-020+ | Not started |

Detailed plan task IDs: `MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md`  
Easy hierarchy: `MASMS_PLAIN_MODULE_CHECKLIST.md`  
Toolchain start guide: `docs/modules/MOD-010/README.md`

## Quick start (API + web)

```bash
docker compose up -d postgres redis
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --port 8000

# other terminal
cp apps/web/.env.example apps/web/.env.local
npm --prefix apps/web install
npm --prefix apps/web run dev
```

Quality gate: `powershell -File scripts/dev-check.ps1`

---

# MASMS Cursor Rules — Professional Engineering Standard

This package configures Cursor for the **Multi-Agent Software House Management System (MASMS)**. It translates the approved MVP SRS and comprehensive specification into focused project rules for architecture, domain behavior, security, coding, testing, workflow orchestration, AI agents, integrations, documentation, and delivery quality.

## Source Baseline

The rules were derived from:

- `Multi_Agent_Software_House_Management_System_MVP_SRS_v1.0.docx`
- `Multi-Agent_Software_House_Management_System_Comprehensive_Specification_v1.1_Corrected.docx`
- Supporting workflow, security, data-model, escalation, integration, template, and acceptance-criteria documents

The SRS remains the functional source of truth. These rules guide implementation and must not be used to invent or silently change approved requirements.

## Installation

Copy the following items to the repository root:

```text
.cursor/
AGENTS.md
.cursorignore
.cursorindexingignore
```

Then open Cursor and verify the rules under **Cursor Settings → Rules**.

## Rule Strategy

- `000–040`: mandatory project governance, domain, security, and approval controls
- `100–210`: backend, database, API, frontend, and UI standards
- `300–340`: LangGraph, Temporal, eventing, integrations, and knowledge-base rules
- `400–520`: testing, performance, observability, reliability, and file controls
- `600–720`: Git, CI/CD, dependencies, documentation, reviews, migrations, and completion gates
- `800`: Cursor response and implementation behavior

Only a small set of rules uses `alwaysApply: true`. File-specific and task-specific rules use descriptions or glob patterns to keep the active context focused.

## Required Repository Decisions

Before production coding, confirm and document:

1. Exact Python and Node.js versions
2. Package managers and lockfiles
3. Authentication provider: Microsoft Entra ID, Auth0, or approved alternative
4. AI provider: OpenAI or Azure OpenAI
5. Deployment target: Azure Container Apps or approved Kubernetes platform
6. CI/CD provider: GitHub Actions or Azure DevOps
7. Code-formatting and type-checking commands
8. Test coverage thresholds approved by the engineering and QA leads
9. Environment naming and secret-store configuration
10. Production release and rollback approvers

## Non-Negotiable System Boundaries

```text
FastAPI     = deterministic business rules and data control
Temporal    = durable, long-running business workflow orchestration
LangGraph   = bounded AI reasoning and agent state
PostgreSQL  = authoritative transactional state
pgvector    = permission-filtered semantic retrieval
Service Bus = asynchronous domain and integration events
```

AI output is never authoritative by itself. Sensitive actions require deterministic validation and the configured human approval gate.
