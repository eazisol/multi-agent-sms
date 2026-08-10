# MASMS Agent Instructions

## Mission

Build a secure, traceable, human-governed multi-agent software-house management platform that manages client queries, requirements, projects, tickets, follow-ups, approvals, QA, releases, and reporting.

## Authoritative Inputs

1. Approved SRS and requirement versions
2. Approved change requests
3. Approved architecture decisions
4. Approved security and workflow policies
5. Existing repository patterns and tests

Do not invent requirements, pricing, deadlines, permissions, approval authority, or production behavior. Mark unsupported information as pending and create a clarification item.

## Architecture Boundary

- FastAPI owns deterministic validation, permissions, state changes, and APIs.
- Temporal owns long-running business workflows, timers, waits, retries, signals, and compensations.
- LangGraph owns bounded AI reasoning, drafting, classification, and recommendation flows.
- PostgreSQL is the transactional source of truth.
- Agents must not write directly to business tables or access raw secrets.

## Work Method

Before changing code:

1. Read the applicable rules in `.cursor/rules/`.
2. Inspect the affected modules, tests, migrations, and API contracts.
3. Identify requirement IDs, permissions, workflow transitions, approvals, audit events, and tenant boundaries.
4. Produce a concise implementation plan.
5. Change only files necessary for the requested outcome.

After changing code:

1. Run applicable format, lint, type-check, unit, integration, and security checks.
2. Report exactly what was run and the result.
3. Never claim a check passed unless it was executed successfully.
4. Summarize changed files, migrations, configuration, risks, and follow-up work.

## Safety

Never expose secrets, bypass approvals, disable audit logging, weaken authorization, access another tenant, use production data casually, or run destructive commands without explicit authorized approval.
