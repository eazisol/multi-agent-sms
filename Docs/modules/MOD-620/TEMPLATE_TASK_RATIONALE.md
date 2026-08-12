# MOD-620 M1 Task Rationale

## Why this M1 slice

This iteration establishes the minimum enforceable UAT and agent-evaluation records for MASMS:

- Three synthetic sample projects (`SAMPLE-A`, `SAMPLE-B`, `SAMPLE-C`) must pass defined workflows before the sample gate is true.
- Agent quality must meet the 80% accuracy target from the latest recorded evaluation.
- Agents cannot accept or approve UAT/acceptance evidence; cross-organization reads return 404 or empty.

## Governance and security alignment

- Tenant scoping is enforced with application-level org checks and RLS on all `ua_*` tables.
- Mutations emit audit events and transactional outbox messages.
- `assert_human_approval_only` raises `ApprovalRequiredError` (409) when `actor_kind` is not human.
- Optimistic concurrency uses `assert_expected_version` on evidence acceptance.

## Deferred scope

- Full production-like seed of clients, tickets, and workflow history
- Playwright / live E2E execution (registry of recorded results only)
- Live agent evaluation jobs against model runs
- Human AC-901 completion approval
