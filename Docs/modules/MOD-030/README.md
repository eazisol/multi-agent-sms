# MOD-030 — Environment Configuration, Secrets, CI/CD, and Deployment Skeleton

**Status:** Implementation draft (M1 complete for scaffold; live AWS apply not done)  
**Human Done (AC-901):** NOT obtained

## Purpose

Separate local/test/staging/production configuration; secret retrieval contract; CI/CD; rollback-ready deploy skeletons; production human gate.

## M1 delivered

| ID | Deliverable |
|---|---|
| MP-001 | `Environment` enum + `config/environments/*.env.example` |
| MP-002 | `SecretBackend` local + AWS Secrets Manager placeholder (fails closed) |
| MP-003 | CI concurrency, junit artifact, build-identity artifact |
| MP-004 | `deploy-staging.yml` (dry-run default, `environment: staging`) |
| MP-005 | `deploy-production.yml` + `scripts/check_production_gate.py` |
| MP-006 | `infra/terraform` Secrets Manager naming skeleton |

## Human setup required in GitHub

1. Create Environments named `staging` and `production`.
2. On `production`, enable required reviewers.
3. Do not store real secrets in the repo; use Environment secrets / AWS Secrets Manager.

## Not in this slice

- Actual AWS resource create/apply
- Working Secrets Manager SDK client (stub raises until PRE + IAM role)
- Product CRUD UI for “environments”

## Verification

See `VERIFICATION.md`.
