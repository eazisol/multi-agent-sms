# MASMS Testing Conventions

Use this file for every module guide. Do not invent buttons, APIs, credentials, or pass results.

## Status legend

| Label | Meaning | How testers treat it |
|---|---|---|
| **Implemented** | The action exists in current UI and/or API and can be exercised locally. | Follow the numbered steps. Record evidence. |
| **Stubbed** | The screen or API exists, but the real provider/runtime is simulated. | Test the stub contract. Never claim the live system worked. |
| **Planned** | Required by the product design, but not present yet. | Document the gap. Do not invent a click path. Mark **non-testable**. |
| **Blocked** | A human approval, secret, tenant, or environment is missing. | Stop. Record the blocker. Do not bypass gates. |

Honesty rules:

- M1 “Done” in checklists means the accepted slice only; it does not imply production readiness.
- Local mode still uses header identity (`X-Organization-Id`, `X-Actor-Id`, `X-Actor-Kind`).
  Auth0 mode validates JWT/JWKS, maps a pre-linked human, and rejects header identity.
- Temporal, OpenAI/LangGraph, pgvector, Gmail, and Jira now have opt-in local/sandbox
  implementations. Their default modes remain deterministic stubs, and live evidence requires
  the relevant service or credential to be configured.
- Playwright smoke is automated in `apps/web/e2e`. The Auth0 authenticated case is skipped
  unless an approved sandbox storage state is provided.
- Combined UI actions such as “Create & approve” are implemented shortcuts. The target design still requires a separate human approval on the exact version.

## Audiences

Read the same guide at different depth:

| Audience | Start with | Then |
|---|---|---|
| First-time user | “What this module is” and “Happy path” | Screens and buttons |
| QA tester | Numbered flows and pass/fail checklist | Negative, authz, and evidence |
| Developer | Files, APIs, migrations, tests | Concurrency, audit, outbox |
| Manager / owner | Purpose, human gates, remaining limits | Cross-module journeys |

## Shared environment

Default local identity (from [`.env.example`](../../.env.example) and [`apps/web/.env.example`](../../apps/web/.env.example)):

| Item | Value |
|---|---|
| Organization | `00000000-0000-4000-8000-000000000001` |
| Actor | `00000000-0000-4000-8000-000000000101` |
| Web | `http://localhost:3000` (or `3001` if 3000 is busy) |
| API | `http://127.0.0.1:8000` |
| Health | `GET /health/live` and `GET /health/ready` |
| OpenAPI | `http://127.0.0.1:8000/docs` |

Start:

```bash
docker compose up -d postgres redis
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --port 8000
```

In a second terminal:

```bash
cp apps/web/.env.example apps/web/.env.local
npm --prefix apps/web install
npm --prefix apps/web run dev
```

Quality commands (run when verifying a module, not as a substitute for the manual flow):

```bash
uv run ruff check apps/api/src tests
uv run mypy apps/api/src/masms_api
uv run pytest tests/unit/<package> tests/integration/<package> -q --tb=short
npm --prefix apps/web run lint
```

Do not claim these passed unless they were actually run.

## Shared chrome (every page)

File: [`apps/web/src/components/app-shell.tsx`](../../apps/web/src/components/app-shell.tsx)

| Control | What it does today | Status |
|---|---|---|
| Sidebar sections | Navigate to 39 desks | Implemented |
| Collapse sidebar | Desktop width toggle | Implemented |
| Open navigation | Mobile overlay | Implemented |
| Skip to content | Accessibility skip link | Implemented |
| Search anything / ⌘K | Opens command palette; navigates to modules only | Stubbed (no record search) |
| Create | No action | Planned |
| Notifications bell | No action | Planned (use `/notifications` and `/my-work`) |
| AI | No action | Planned (use `/agents` and `/agent-runs`) |
| Theme toggle | Light/dark | Implemented |
| Role selector | Viewer, Contributor, Baseline Approver, Admin, Agent (draft only) | Stubbed UI role; server still uses header actor |
| You / AI badge | Shows human vs agent kind | Stubbed |

Command palette file: [`apps/web/src/components/command-palette.tsx`](../../apps/web/src/components/command-palette.tsx)

Role file: [`apps/web/src/lib/roles.ts`](../../apps/web/src/lib/roles.ts)

Session file: [`apps/web/src/components/session-provider.tsx`](../../apps/web/src/components/session-provider.tsx)

Toasts: [`apps/web/src/lib/toast.ts`](../../apps/web/src/lib/toast.ts) via Sonner. Most desks show API errors as toasts, not page-level 403/404 (exception: baseline detail).

## Identity and authorization for testers

1. The web app sends `X-Organization-Id`, `X-Actor-Id`, and `X-Actor-Kind` on every API call ([`apps/web/src/lib/api.ts`](../../apps/web/src/lib/api.ts)).
2. Changing the Role dropdown changes **UI hiding** for some governance actions and sets `actorKind` to `agent` for Agent (draft only). It does **not** log in a different person.
3. Backend authorization is deny-by-default in domain services. MOD-120 permission checks exist at `/api/v1/access/checks/permission` and are **not** a universal router middleware.
4. PostgreSQL RLS policies exist in migrations. SQLite pytest does **not** prove RLS. Live RLS proof is still a target test, not a current CI result.
5. Agents must not be instructed to approve scope, quotations, SRS, production deploy, or project closure. Those are human-only.

## Evidence model

For every **Implemented** flow, capture:

| Evidence | Where |
|---|---|
| Screenshot or notes of the screen after the action | Tester log |
| Toast or inline message text | UI |
| Record id, status, version | UI list/detail or API JSON |
| Audit row | `/audit-logs` or `ops_audit_logs` / `gov_audit_events` |
| Outbox event name when the module publishes one | `kernel` outbox / observability relay |
| Automated test pointer | `tests/unit/...` and `tests/integration/...` |

Pass means: the numbered step produced the expected UI **and** the expected persisted status. Fail means either is missing. Skip means the step is Planned, Stubbed-as-non-executable, or Blocked.

## Standard flow IDs

Every module guide uses these IDs when the capability exists:

| ID | Intent |
|---|---|
| F-SETUP | Seed or locate required records from dependency modules |
| F-HAPPY | Primary successful path |
| F-VALIDATE | Missing/invalid fields |
| F-AUTHZ | Unauthorized role or agent-as-human |
| F-TENANT | Wrong organization or project |
| F-CONCUR | Stale `expected_version` / optimistic concurrency |
| F-TRANS | Invalid status transition |
| F-GATE | Human approval / exact-version gate |
| F-TERM | Terminal state and reopen rules |
| F-RECOVER | Retry, overdue processing, dead-letter, or failure path |
| F-CLEAN | Leave the environment understandable (do not delete append-only audit) |

If a flow does not apply, the guide marks it **N/A** with a one-line reason.

## API error contract

Expect `application/problem+json` with `code`, `message`, and optional `correlation_id`. Kernel: [`apps/api/src/masms_api/kernel/problem.py`](../../apps/api/src/masms_api/kernel/problem.py).

Typical codes testers will see: validation, forbidden, not found, conflict, invalid transition, approval required.

## Workspace IDs

The browser stores last-used ids in localStorage ([`apps/web/src/lib/workspace.ts`](../../apps/web/src/lib/workspace.ts)):

- `masms.workspace.projectId`
- `masms.workspace.queryId`
- `masms.workspace.documentId`
- `masms.workspace.conversationId`
- `masms.workspace.ticketId`
- `masms.workspace.questionnaireId`

If a desk “already knows” a project or query, check these keys before assuming a bug.

## Human-only actions (never finalize by an agent)

From project governance:

- Final project scope, quotation, or commercial terms
- Client-facing timeline commitment
- Final SRS baseline
- Resource allocation outside approved capacity
- Major architecture decision
- Scope-affecting change request
- Acceptance of critical/high-risk known issues
- Production deployment or rollback
- Client delivery acceptance
- Project cancellation or closure

Guides may show how to **open** the request. A named human must **decide**.

## Source-of-truth order

1. [`MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md`](../../MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md) — module catalog
2. [`Docs/modules/MOD-NNN/README.md`](../modules/) and `VERIFICATION.md` — what shipped
3. [`MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md`](../../MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md) — task evidence
4. This testing tree — how to exercise it

Known documentation contradictions testers should not “fix” by guessing:

- Some READMEs still say AC-901 pending while checklists mark M1 Done.
- Progress and plain checklists disagree slightly on done-task counts.
- Phase 4 modules (MOD-400–460) are Phase 4 in the plan; some checklists nest them under Phase 3 headings.
- “Done (M1)” is not production exit. FINAL/GATE items remain open.

## Guide file locations

| File | Purpose |
|---|---|
| [`Docs/testing/README.md`](README.md) | Master index |
| This file | Shared rules |
| [`Docs/testing/CROSS_MODULE_JOURNEYS.md`](CROSS_MODULE_JOURNEYS.md) | Business journeys spanning modules |
| [`Docs/modules/MOD-NNN/E2E_GUIDE.md`](../modules/) | Per-module deep guide |
| [`Docs/testing/GUIDE_TEMPLATE.md`](GUIDE_TEMPLATE.md) | Heading contract used by every module guide |
