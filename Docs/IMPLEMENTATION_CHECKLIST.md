# Implementation Checklist

## Requirement and Scope

- [ ] Approved ticket and requirement version identified
- [ ] Acceptance criteria are complete
- [ ] In-scope and out-of-scope behavior are clear
- [ ] Clarifications are recorded instead of guessed

## Architecture

- [ ] Business rule is in the correct layer
- [ ] Durable workflow logic is in Temporal
- [ ] AI reasoning is bounded in LangGraph
- [ ] No direct agent database mutation
- [ ] Existing repository patterns were followed

## Security

- [ ] Tenant/client/project isolation enforced
- [ ] Backend authorization enforced
- [ ] Approval gate checked
- [ ] Secrets and PII protected
- [ ] Untrusted content treated as data
- [ ] Audit event included

## Data and API

- [ ] Constraints, indexes, transactions, concurrency considered
- [ ] Migration is safe and tested
- [ ] Idempotency and retries considered
- [ ] API contract and OpenAPI updated
- [ ] Backward compatibility assessed

## Quality

- [ ] Unit tests
- [ ] Integration/contract tests
- [ ] Permission and negative tests
- [ ] Tenant isolation tests
- [ ] Workflow/agent tests where applicable
- [ ] Performance impact assessed
- [ ] Documentation updated

## Delivery

- [ ] Formatter, lint, type-check, tests, and build executed
- [ ] Security/dependency scans executed where applicable
- [ ] Rollout, monitoring, and rollback documented
- [ ] Required human approvals identified
- [ ] Completion report is truthful and evidence-based
