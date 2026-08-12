# MOD-610 M1 Task Rationale

## Why this M1 slice

This iteration establishes the minimum enforceable reliability and recovery records for MASMS:

- API p95 must be at or under 2000 ms for the API SLO to pass.
- Dashboard p95 must be at or under 3000 ms for the dashboard SLO to pass.
- Durable workflow replay records resume after failure and reject duplicate idempotency keys.

## Governance and security alignment

- Tenant scoping is enforced with application-level org checks and RLS on all `rlb_*` tables.
- Mutations emit audit events and transactional outbox messages.
- Replay transitions are configuration-like domain rules (`pending→failed`, `failed→resumed`, `resumed→completed`, `pending→completed`).
- Optimistic concurrency uses `assert_expected_version` on replay and DR approval.

## Deferred scope

- Live k6 / load-generation against a running API
- Temporal workflow replay execution (registry only in M1)
- Executed disaster-recovery drills
- Human AC-901 obtained 2026-08-12
