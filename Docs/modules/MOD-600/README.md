# MOD-600 Security, Privacy, Retention, Backup, and Recovery Hardening (M1)

## Scope delivered in M1

- Security gate (`GET /security/gate`) that fails while Critical incidents remain open.
- Backup records with RPO/RTO targets and restore-test measurement validation.
- Org-level model-training policy defaulting to `allow_model_training=false`, requiring human approval evidence to enable.
- Registries for threat models, PII inventory, retention policies, legal holds, deletion jobs, and security incidents.

## Backend components

- Module: `apps/api/src/masms_api/modules/securityhardening`
  - `models.py`: `sh_*` tables including `sh_training_policies`
  - `service.py`: gate, recovery validation, training opt-in, legal-hold blocked deletion
  - `router.py`: `/api/v1/security/*` endpoints
  - `domain.py`: severities, RPO/RTO, training opt-in invariants
  - `schemas.py`: transport contracts

## Frontend components

- Desk page route: `apps/web/src/app/security/page.tsx`
- Desk UI: `apps/web/src/components/security-desk-page.tsx`
- API helpers: `apps/web/src/lib/api.ts`
- Navigation entry: `apps/web/src/lib/navigation.ts` (`ready: true`)

## API endpoints (M1)

- `GET /api/v1/security/gate`
- `GET /api/v1/security/recovery-validation`
- `GET|PUT /api/v1/security/training-policy`
- `POST|GET /api/v1/security/threat-models`
- `POST|GET /api/v1/security/pii-inventory`
- `POST|GET /api/v1/security/retention-policies`
- `POST|GET /api/v1/security/legal-holds`
- `POST /api/v1/security/legal-holds/{id}/release`
- `POST|GET /api/v1/security/deletion-jobs`
- `POST|GET /api/v1/security/backups`
- `POST|GET /api/v1/security/restore-tests`
- `POST|GET /api/v1/security/incidents`
- `POST /api/v1/security/incidents/{id}/close`

## Honesty / known limitations

- No live backup infrastructure is provisioned in M1; backup rows are operational records.
- Restore tests store measured RPO/RTO values; they do not execute restores.
- Deletion jobs use simulated row counters and legal-hold blocking logic.
- Threat models are registry records, not automated threat scanners.
- AC-901 (human completion approval) is not obtained in this slice.
