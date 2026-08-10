# Infrastructure as Code (MOD-030-MP-006)

Skeleton only. No cloud resources are provisioned by this repository yet.

## Layout

| Path | Purpose |
|---|---|
| `terraform/main.tf` | Naming + AWS Secrets Manager + placeholder tags |
| `terraform/variables.tf` | Staging/production input shapes without secrets |
| `terraform/terraform.staging.tfvars.example` | Example staging values |
| `terraform/terraform.production.tfvars.example` | Example production values |
| GitHub Environments `staging` / `production` | Required for deploy workflows (configure protection rules in GitHub UI) |

## Rules

- Secrets never live in tfvars files committed to git.
- Production deploys require human authorization via `Deploy production` workflow inputs + GitHub Environment reviewers.
- Prefer IAM roles (ECS task role / IRSA) for Secrets Manager access once the AWS landing zone is approved.

## Next (not MOD-030 M1)

- Wire real AWS account IDs after PRE infrastructure approval.
- Add rollback runbooks with previous ECS task definition / previous AMI revision.
