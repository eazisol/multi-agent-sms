# Infrastructure as Code (MOD-030-MP-006)

Skeleton only. No cloud resources are provisioned by this repository yet.

## Layout

| Path | Purpose |
|---|---|
| `bicep/main.bicep` | Naming + Key Vault + placeholder App Service / Container Apps params |
| `bicep/parameters.*.json.example` | Staging/production parameter shapes without secrets |
| GitHub Environments `staging` / `production` | Required for deploy workflows (configure protection rules in GitHub UI) |

## Rules

- Secrets never live in parameter files committed to git.
- Production deploys require human authorization via `Deploy production` workflow inputs + GitHub Environment reviewers.
- Prefer managed identity for Key Vault access once Azure landing zone is approved.

## Next (not MOD-030 M1)

- Wire real Azure subscription IDs after PRE infrastructure approval.
- Add rollback runbooks with slot swap / previous revision.
