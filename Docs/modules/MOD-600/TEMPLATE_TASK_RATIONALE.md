# MOD-600 M1 Task Rationale

## Why this M1 slice

This iteration establishes the minimum enforceable security and recovery controls for MASMS:

- Critical open security incidents fail a release/security gate.
- Recovery objectives (RPO/RTO) are recorded on backups and validated by restore-test measurements.
- Client and company data stay out of model training by default unless a human records approval evidence.

## Governance and security alignment

- Tenant scoping is enforced with application-level org checks and RLS on all `sh_*` tables.
- Mutations emit audit events and transactional outbox messages with redacted payloads.
- Legal holds block deletion jobs for covered entity types.
- Training opt-in without evidence is rejected.

## Deferred scope

- Live backup/restore orchestration and infrastructure automation
- Automated PII discovery scanners and file AV pipelines
- Full Temporal deletion workflows and notification fan-out
- Human AC-901 obtained 2026-08-12
