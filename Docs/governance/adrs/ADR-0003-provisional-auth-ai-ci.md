# ADR-0003 — Provisional Auth0, OpenAI, GitHub Actions, and AWS

**Status:** Proposed (PENDING formal PRE approval)  
**Date (UTC):** 2026-08-10  
**Module:** MOD-000 / MOD-030 / MOD-110 / MOD-360  
**Requirements:** MVP-FR-001, MVP-NFR-001, MVP-NFR-008

## Context

Auth, model provider, CI, and cloud target must be chosen before production wiring. Session selection preferred Auth0 + OpenAI + GitHub Actions and an AWS deployment/secrets direction.

## Decision (provisional)

| Concern | Provisional choice | Not locked |
|---|---|---|
| Human authentication | Auth0 | Amazon Cognito remains an approved alternative pending final sign-off |
| AI provider | OpenAI | Amazon Bedrock remains an approved alternative |
| CI/CD | GitHub Actions | AWS CodePipeline remains an approved alternative |
| Deploy target | Amazon ECS/Fargate (or approved EKS) | Final cluster/service names PENDING |
| Secret store | AWS Secrets Manager | PENDING formal PRE-ENV |
| Object storage | Amazon S3 | PENDING |
| Async messaging | Amazon SNS/SQS | PENDING broker topology |

## Consequences

- No production credentials are introduced in this ADR  
- Integrations must use secret-manager references and sandbox credentials only  
- Provider-specific code should be behind interfaces (adapter pattern)  

## Security

- MFA and step-up requirements still apply for privileged and production actions  
- Client/company data must not be used for model training without written approval  

## Rollback

Replace via CR + new ADR; migrate identity tenants and CI definitions with dual-run period.
