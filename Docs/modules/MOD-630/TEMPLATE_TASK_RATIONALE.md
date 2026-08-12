# MOD-630 M1 Task Rationale

## Why this M1 slice

This iteration establishes the minimum enforceable controlled-pilot and production-readiness **records** for MASMS:

- Critical and High acceptance-test results must not be failed or blocked before the acceptance gate is true.
- Every registered pilot user must approve controlled production use, with at least one registered user.
- Product, security, operations, and QA must each sign as a human actor.
- Production deployment and rollback APIs persist records only. They do not deploy, roll back infrastructure, or allow agents to finalize production.

## Governance and security alignment

- Tenant scoping is enforced with application-level org checks and RLS on all `pl_*` tables.
- Mutations emit audit events and transactional outbox messages.
- `assert_human_signoff` raises `ApprovalRequiredError` (409) when `actor_kind` is not human.
- `assert_production_may_record` requires all three gates plus non-empty `human_approval_evidence`.
- Optimistic concurrency helper `assert_expected_version` is available for versioned plan updates.

## Deferred scope

- Live production deployment, CI/CD promotion, or environment mutation
- Automated infrastructure rollback
- Live training delivery or support-desk integration
- Human AC-901 completion approval
