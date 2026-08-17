# MOD-030 — Environment Configuration, Secrets, CI/CD, and Deployment Skeleton

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Learn why local, test, staging, and production settings differ. |
| QA | Verify dry-run workflows and fail-closed production/secret behavior. |
| Developer | Validate environment parsing, secret backend contracts, and workflow files. |
| Owner / operator | Configure GitHub Environments and preserve the human production gate. |

## 2. What this module is

This module is deployment scaffolding. It separates environment configuration, defines how code asks for secrets, adds CI/deployment workflows, and blocks production actions unless explicit evidence is supplied.

In this company it means local developers can use local environment values, while production must use the approved secret manager and a reviewed release request. The repository currently demonstrates that boundary; it does not deploy a production system.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Environment enum and example files | Implemented | Local/test/staging/production skeleton |
| Local environment secret backend | Implemented | Development use only |
| AWS Secrets Manager backend contract | Stubbed | Constructor checks region; reads always fail closed |
| CI concurrency/JUnit/build identity | Implemented | Workflow configuration |
| Staging and production workflows | Stubbed | Dry-run/default failure paths |
| Production gate script | Implemented | Deterministic placeholder gate |
| Terraform secret naming skeleton | Stubbed | No live apply |
| GitHub Environment reviewers | Blocked | Human repository setup required |
| Actual AWS resources/deploy | Planned / Blocked | Architecture, IAM, and approval required |
| Product CRUD desk/API | N/A | Infrastructure module |
| Human Done AC-901 | Blocked | Not obtained |

## 4. Requirements and dependencies

- Complete [MOD-010](../MOD-010/E2E_GUIDE.md).
- Config examples: [`config/environments/`](../../../config/environments/).
- Secret contract: [`platform/secrets.py`](../../../apps/api/src/masms_api/platform/secrets.py).
- Workflows: [`ci.yml`](../../../.github/workflows/ci.yml), [`deploy-staging.yml`](../../../.github/workflows/deploy-staging.yml), [`deploy-production.yml`](../../../.github/workflows/deploy-production.yml).
- Gate: [`scripts/check_production_gate.py`](../../../scripts/check_production_gate.py).
- Terraform: [`infra/terraform/`](../../../infra/terraform/).
- Do not create cloud resources during this guide.

## 5. How to start

Run repository checks locally and inspect workflow YAML. The safe production-gate negative check is:

```bash
set CONFIRM_PRODUCTION=false
uv run python scripts/check_production_gate.py
```

PowerShell:

```powershell
$env:CONFIRM_PRODUCTION = "false"
uv run python scripts/check_production_gate.py
```

Expected: non-zero exit and a `BLOCKED:` message. Do not supply invented approver/reason/SHA values just to force a green result.

## 6. Screens, buttons, and files

There is no product desk, form, filter, empty state, pagination control, or toast for MOD-030.

| Surface | What it does | Status | Source |
|---|---|---|---|
| Environment examples | Document non-secret configuration names | Implemented | [`config/environments/`](../../../config/environments/) |
| `SecretBackend` | Abstract secret retrieval contract | Implemented | [`platform/secrets.py`](../../../apps/api/src/masms_api/platform/secrets.py) |
| `LocalEnvSecretBackend` | Returns configured local values; rejects missing/empty | Implemented | same file |
| `AwsSecretsManagerSecretBackend` | Validates region, then refuses reads | Stubbed | same file |
| `create_secret_backend` | Rejects local backend in production | Implemented | same file |
| CI workflow | Quality/build evidence | Implemented | [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml) |
| Staging workflow dispatch | Dry-run deployment skeleton | Stubbed | [`deploy-staging.yml`](../../../.github/workflows/deploy-staging.yml) |
| Production workflow dispatch | Environment/reviewer/gate skeleton | Stubbed / Blocked | [`deploy-production.yml`](../../../.github/workflows/deploy-production.yml) |
| Production gate CLI | Requires confirmation, approver, reason, SHA | Implemented | [`check_production_gate.py`](../../../scripts/check_production_gate.py) |
| Terraform plan/apply | Secret naming scaffold only | Stubbed | [`infra/terraform/`](../../../infra/terraform/) |

## 7. API, data, and automated tests

MOD-030 owns no product HTTP routes, tables, or migration. Its persistent external configuration would live in GitHub Environments and AWS, but those are not provisioned by this test.

Key secret behaviors visible in source:

- Missing local value raises `SecretBackendError`.
- Production with `local_env` raises `SecretBackendError`.
- Secrets Manager without `MASMS_AWS_REGION` raises.
- Any Secrets Manager `get_secret` call raises because the SDK client is not enabled.
- Secret values must never be printed or logged.

Use the repository quality suite plus focused platform tests if present. [VERIFICATION.md](VERIFICATION.md) only records the negative gate as an earlier expected block; its broad checks say “see latest session” and are not current pass evidence.

## 8. Test flows

### F-SETUP

1. Work in a non-production local shell. Clear production confirmation variables. **Expected UI:** no product page. **Data/audit:** no cloud changes. **Evidence:** variable names/status, never values.
2. Confirm workflow and Terraform files parse during normal CI/static checks.

### F-HAPPY

1. Construct `LocalEnvSecretBackend` with a synthetic value and request its key. **Expected:** value returned to the caller only; no log.
2. Run CI locally through the MOD-010 commands. **Expected:** results are recorded separately.
3. Inspect staging workflow default. **Expected:** dry-run behavior; no claim of deployment.

### F-VALIDATE

1. Request a missing/empty local key. **Expected:** `SecretBackendError`; no fallback.
2. Select an unsupported backend. **Expected:** explicit unsupported-backend error.
3. Instantiate Secrets Manager without region. **Expected:** fail closed.

### F-AUTHZ

1. Inspect `production` GitHub Environment requirements. **Expected:** repository operators must configure required reviewers.
2. A workflow actor without reviewer approval must remain blocked. This is **Blocked** to test until the environment exists.

### F-TENANT

N/A — MOD-030 config is environment-scoped, not a business tenant record. Secret prefixes must still prevent environment collision.

### F-CONCUR

1. Inspect workflow concurrency configuration. **Expected:** overlapping runs use the declared group/cancellation policy.
2. Live concurrent deployment behavior is **Blocked** because no target is provisioned.

### F-TRANS

1. Treat deployment stages as `requested → reviewed → gate checked → dry-run/execute`.
2. Attempt to skip confirmation/reviewer evidence. **Expected:** blocked. This is workflow validation, not a product status API.

### F-GATE

1. Run with `CONFIRM_PRODUCTION=false`. **Expected UI:** `BLOCKED:` on stderr and exit `1`.
2. Leave approver, reason, or Git SHA absent. **Expected:** deterministic gate denial.
3. Even if the placeholder gate inputs are present, the script states deploy may still be dry-run; do not interpret it as production approval.

### F-TERM

N/A — no business record has a terminal state. Production deployment/rollback is not executed here.

### F-RECOVER

1. Correct a missing synthetic local value and retry. **Expected:** local retrieval succeeds without exposing it.
2. Secrets Manager retrieval remains **Blocked** until approved IAM/SDK wiring exists; do not substitute local secrets in production.
3. Rollback execution is **Planned**, not tested against AWS.

### F-CLEAN

1. Remove synthetic environment variables from the shell.
2. Delete no cloud resources because none should have been created.
3. Review logs/screenshots and redact values, account identifiers, tokens, and Terraform state content.

## 9. Security, privacy, and approvals

- Never place real secrets in source, prompts, logs, tickets, screenshots, or Terraform state committed to Git.
- Production rejects `local_env`; do not weaken that check.
- IAM roles and short-lived credentials are the target; no static AWS credential setup is authorized here.
- Production deploy/rollback is human-only, requires step-up where configured, and must preserve approver, reason, commit, and evidence.
- A Terraform plan is not approval to apply.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Environment-separated examples | Implemented |
| Local secret retrieval | Implemented |
| AWS Secrets Manager retrieval | Stubbed fail-closed |
| CI evidence | Implemented workflow |
| Staging deploy | Dry-run skeleton |
| Production deploy | Blocked skeleton; no apply |
| Terraform-managed AWS resources | Naming scaffold only |
| GitHub required reviewers | Human setup required |
| Product environment admin UI | N/A |

## 11. Related journeys

- [J-LEARN](../../testing/CROSS_MODULE_JOURNEYS.md#j-learn-first-hour) uses local configuration only.
- Release/deployment journeys must preserve the human-only actions listed in [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md#human-only-actions-never-finalize-by-an-agent).

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| No product UI/API was invented | |
| Environment examples inspected without secrets | |
| Local backend returns synthetic configured value | |
| Missing local secret fails closed | |
| Production local backend is rejected | |
| Secrets Manager missing region is rejected | |
| Secrets Manager read remains labeled Stubbed | |
| Production gate negative check exits non-zero | |
| GitHub reviewer setup recorded as Blocked/verified | |
| No Terraform apply or production deploy performed | |
| Logs and evidence contain no secret values | |
| Human AC-901 remains recorded accurately | |
