# Cursor Rules Catalog

| Rule | Purpose | Scope | Always Apply |
|---|---|---|---|
| `000-project-governance.mdc` | Enforce MASMS source-of-truth, architecture boundaries, human accountability, traceability, and safe implementation behavior for every task. | `Intelligent / requestable` | true |
| `010-task-execution.mdc` | Use a professional inspect-plan-implement-verify-report workflow whenever creating, changing, reviewing, debugging, or refactoring code. | `Intelligent / requestable` | true |
| `020-domain-invariants.mdc` | Preserve MASMS domain invariants whenever implementing business entities, workflows, services, APIs, agents, dashboards, or tests. | `Intelligent / requestable` | true |
| `030-security-and-privacy.mdc` | Apply least privilege, tenant isolation, secure secret handling, PII minimization, agent safety, and audit controls to every implementation decision. | `Intelligent / requestable` | true |
| `040-human-approval-gates.mdc` | Enforce exact-version, authorized-human approval gates for commercial, scope, architecture, quality, deployment, delivery, and closure actions. | `Intelligent / requestable` | true |
| `100-backend-python-fastapi.mdc` | Apply Python, FastAPI, Pydantic, SQLAlchemy, modular architecture, typing, transaction, and service-layer standards when editing backend Python code. | `"**/*.py"` | false |
| `110-database-postgresql.mdc` | Apply PostgreSQL, SQLAlchemy model, indexing, constraints, RLS, versioning, audit, and migration-safe data design standards. | `"**/*.{py,sql}"` | false |
| `120-api-contracts.mdc` | Apply versioned REST, validation, authorization, idempotency, pagination, error, concurrency, and OpenAPI contract standards to API work. | `"**/*.{py,ts,tsx}"` | false |
| `200-frontend-nextjs.mdc` | Apply strict TypeScript, Next.js, React, Tailwind, shadcn/ui, API-boundary, state, permission, and maintainability standards to frontend code. | `"**/*.{ts,tsx,js,jsx}"` | false |
| `210-ui-ux-accessibility.mdc` | Apply consistent, responsive, accessible, professional UI and interaction standards to pages, components, forms, dashboards, and design changes. | `"**/*.{tsx,jsx,css,scss,mdx}"` | false |
| `300-langgraph-agents.mdc` | Apply bounded LangGraph agent design, typed state, tool authorization, structured output, human supervision, knowledge provenance, and prompt safety standards. | `"**/agents/**/*.py"` | false |
| `310-temporal-workflows.mdc` | Apply deterministic, durable, version-safe Temporal workflow and activity standards for waits, timers, approvals, follow-ups, retries, and long-running processes. | `"**/workflows/temporal/**/*.py"` | false |
| `320-events-service-bus.mdc` | Apply domain-event envelope, outbox, schema-versioning, idempotent consumer, dead-letter, correlation, and privacy standards to asynchronous messaging. | `"**/*.{py,json,yaml,yml}"` | false |
| `330-integrations.mdc` | Apply provider-adapter, OAuth, webhook, source-of-truth, sandbox, rate-limit, retry, mapping, and reconciliation standards to external integrations. | `"**/integrations/**/*.py"` | false |
| `340-knowledge-base-rag.mdc` | Apply approved-version, permission-filtered, provenance-rich, conflict-aware, privacy-safe knowledge ingestion and retrieval standards. | `"**/*.{py,md,mdx}"` | false |
| `400-testing-and-qa.mdc` | Apply requirement-linked unit, integration, contract, workflow, end-to-end, regression, negative, security, and QA evidence standards to all changes. | `"**/*test*.{py,ts,tsx,js,jsx}"` | false |
| `410-security-testing.mdc` | Apply mandatory authorization, isolation, upload, webhook, prompt-injection, secret, audit, dependency, and production-safety verification to security-sensitive work. | `"**/*.{py,ts,tsx,yaml,yml,json}"` | false |
| `420-performance-reliability.mdc` | Apply measurable performance, availability, load, caching, query, worker, timeout, degradation, and recovery standards to performance-sensitive changes. | `"**/*.{py,ts,tsx}"` | false |
| `500-observability-audit.mdc` | Apply structured logging, OpenTelemetry, metrics, tracing, health, alerting, immutable audit, correlation, and privacy standards. | `"**/*.{py,ts,tsx}"` | false |
| `510-errors-retries-idempotency.mdc` | Apply explicit error taxonomy, safe messages, bounded retries, exponential backoff, idempotency, compensation, and dead-letter handling. | `"**/*.{py,ts,tsx}"` | false |
| `520-file-storage-uploads.mdc` | Apply private object storage, quarantine, allowlist validation, malware scanning, signed URL, checksum, permission, retention, and AI-indexing controls to files. | `"**/*.{py,ts,tsx}"` | false |
| `600-git-ci-cd.mdc` | Apply protected-branch, focused-commit, pull-request, automated quality gate, artifact, release, and deployment approval standards. | `"**/*.{yml,yaml,json,toml,md}"` | false |
| `610-dependencies-configuration.mdc` | Apply dependency minimization, version pinning, lockfile, license, vulnerability, environment, secret, feature flag, and startup validation standards. | `"**/*.{toml,json,yaml,yml,env,py,ts}"` | false |
| `620-documentation.mdc` | Apply requirement-linked, versioned, accurate, concise architecture, API, runbook, decision, setup, and operational documentation standards. | `"**/*.{md,mdx,rst,py,ts,tsx}"` | false |
| `700-code-review.mdc` | Use the MASMS professional code-review checklist whenever reviewing or preparing a pull request. | `Intelligent / requestable` | false |
| `710-migrations-seeding.mdc` | Apply additive, reversible, zero-downtime-aware, reviewed migration and idempotent sanitized seed-data standards. | `"**/migrations/**/*.{py,sql}"` | false |
| `720-definition-ready-done.mdc` | Enforce MASMS Definition of Ready and Definition of Done before starting, reviewing, testing, closing, or releasing work. | `Intelligent / requestable` | false |
| `800-cursor-output-standards.mdc` | Require Cursor to communicate plans, changes, verification, risks, and limitations professionally and truthfully without exposing hidden reasoning. | `Intelligent / requestable` | true |
