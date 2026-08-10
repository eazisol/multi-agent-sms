# Pending Decisions (PRE / tooling)

**Artifact ID:** PENDING-001  
**Module:** MOD-000 / Global Readiness  
**Status:** Open  
**Owner:** PENDING Product + Engineering leads  
**Version:** 0.1.0

These items remain **PENDING formal human approval**. Working values below are **provisional scaffolding choices** only and must not be treated as production commitments.

| ID | Decision | Provisional working value | Formal status |
|---|---|---|---|
| PRE-PY | Exact Python version | **3.12** | PENDING |
| PRE-NODE | Exact Node.js version | **22 LTS** | PENDING |
| PRE-PKG | Package managers / lockfiles | **uv** (Python) + **pnpm** (Node) | PENDING — pnpm host activation blocked (EPERM on Corepack) |
| PRE-AUTH | Auth provider | **Auth0** | PENDING |
| PRE-AI | AI provider | **OpenAI** | PENDING |
| PRE-CI | CI/CD provider | **GitHub Actions** | PENDING |
| PRE-DEPLOY | Deploy target | Azure Container Apps or approved Kubernetes | PENDING — no provisional lock |
| PRE-FMT | Format/lint/typecheck commands | ruff + mypy (API); eslint/tsc (web when scaffolded) | PENDING thresholds |
| PRE-COV | Coverage thresholds | Not set | PENDING eng + QA leads |
| PRE-ENV | Environment names + secret store | `local` / `test` / `staging` / `production`; Azure Key Vault for runtime secrets | PENDING |
| PRE-APPR | Production release/rollback approvers | Unnamed | PENDING |
| PRE-SRS | Approve MVP SRS as functional baseline | BL-SRS-001 v1.0 | PENDING human approval |
| PRE-SCOPE | Formal MVP scope + exclusions sign-off | From MVP SRS exclusions section | PENDING |
| PRE-OWNERS | Named BD/PM/TL/QA/DevOps/Security/AI/Product owners | Unnamed | PENDING |

## Host blockers observed during MOD-000 scaffold

1. Repository is **not** initialized as a git repo yet (`NO_GIT_REPO`).  
2. `corepack enable` / pnpm activation failed with `EPERM` under `C:\Program Files\nodejs\`.  
3. Global Readiness checklist PRE-001… still unchecked — many require human sign-off, not agent action.

## Clarification required

Resolve the table above before treating MOD-010/MOD-030 production skeleton as Done.
