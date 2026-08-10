# Cursor Task Prompt Templates

Use these prompts with the SRS or ticket reference attached.

## Implement a Feature

```text
Implement [TICKET-ID / REQUIREMENT-ID].
First inspect the existing architecture and applicable Cursor rules. Provide a concise plan, then implement the smallest complete change. Include authorization, tenant isolation, validation, audit events, status/approval behavior, tests, API documentation, and migration impact. Run all applicable checks and report exact results.
```

## Fix a Bug

```text
Fix [BUG-ID]. Reproduce the defect first and identify the root cause. Confirm whether it is an approved-requirement failure or a change request. Add a regression test that fails before the fix and passes after it. Avoid unrelated refactoring. Report the root cause, changed files, test evidence, and any deployment or data-repair impact.
```

## Build a New Agent Capability

```text
Implement the [AGENT] capability for [REQUIREMENT-ID]. Define typed LangGraph state, bounded nodes, approved retrieval, schema-validated output, narrow tools, authority checks, human-review thresholds, audit fields, cost/time limits, prompt-injection controls, and tests. The agent must not directly mutate authoritative business state.
```

## Build a Temporal Workflow

```text
Implement the [WORKFLOW] workflow. Model durable waits, signals, reminders, escalations, approvals, retries, cancellation, compensation, versioning, and recovery. Keep workflow code deterministic and all side effects in idempotent activities. Add time-skipping and signal/retry tests.
```

## Add an Integration

```text
Implement the [PROVIDER] integration behind a provider interface. Document source of truth, OAuth scopes, sandbox setup, field/status mappings, webhook validation, idempotency, rate limits, retries, reconciliation, token revocation, audit, PII handling, and acceptance tests. Do not use production credentials for development.
```

## Security Review

```text
Review [MODULE/PR] against the MASMS security rules. Check tenant/project isolation, backend authorization, RLS, IDOR, secrets, PII, prompt injection, agent tools, file uploads, webhooks, audit completeness, error leakage, and destructive operations. Rank findings by severity and provide exact remediation locations.
```

## Code Review

```text
Review this change using `.cursor/rules/700-code-review.mdc`. Identify blocking issues first. Verify requirement correctness, architecture boundaries, security, data safety, API compatibility, reliability, performance, tests, observability, operations, and documentation. Do not approve based only on style.
```
