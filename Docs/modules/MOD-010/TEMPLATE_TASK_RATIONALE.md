# MOD-010 Template Task Rationale

The module-wise plan repeats DB/BE/API/FE/WF/SEC templates for every module. For **MOD-010 (toolchain)**, those product-entity tasks are marked **N/A** as follows.

## N/A — not applicable as business features

| Plan IDs | Why N/A |
|---|---|
| `MOD-010-DB-001`…`008` | No business tables for “monorepo/language/CI”. Tooling is files + config, not ORM entities. |
| `MOD-010-BE-001`…`004` | No governance/domain services owned by MOD-010. |
| `MOD-010-API-001`…`003` | No MOD-010 CRUD API. Health/meta live under `apps/api` from MOD-000. |
| `MOD-010-FE-001`…`004` | No MOD-010 admin UI. Next.js app exists for MOD-000 governance screens; toolchain is npm/Next config. |
| `MOD-010-WF-001`…`004` | No business workflow. Dev workflow is documented start commands + CI. |
| `MOD-010-SEC-001`…`002` | No new tenant resources. Secrets hygiene is AC-003 / `.gitignore`. |
| `MOD-010-SEC-004` | No MOD-010 audit entity. |
| `MOD-010-QA-001`…`004` | No MOD-010 domain tests; verification is toolchain QA-005 / CI. |

## In scope (must complete)

| Plan IDs | Meaning |
|---|---|
| `MOD-010-MP-001`…`008` | Structure, versions, packages, Compose, lint, types, tests, CI |
| `MOD-010-SEC-003` | No secrets in VCS / examples only |
| `MOD-010-QA-005` | Run formatter/lint/type/tests/web build |
| `MOD-010-DOC-001`…`002` | This module README + verification notes |
| `MOD-010-AC-*` | Start commands, CI gate, secrets, human Done |

This is a formal exclusion of template noise for MOD-010 only — not a waiver of those tasks on product modules (MOD-000, MOD-100, …).
