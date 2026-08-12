# MOD-520 M1 Task Rationale

## Why this M1 slice

This iteration establishes the minimum safe Jira integration path while preserving MASMS governance:

- Internal approval remains authoritative before Jira issue creation.
- External Jira status updates cannot bypass internal transition/approval rules.
- Comment synchronization failures are observable and operationally recoverable via retry.

## Governance and security alignment

- Tenant scoping is enforced with application-level tenant checks and RLS policies on `jr_*` tables.
- No secrets are stored in Jira module tables.
- M1 behavior is auditable through persisted push/conflict/sync records and deterministic status changes.

## Deferred scope

The following items remain for later MOD-520 increments:

- richer project/field/status mapping UX and workflows
- provider-authenticated Jira API adapters
- full reconciliation and background sync orchestration
