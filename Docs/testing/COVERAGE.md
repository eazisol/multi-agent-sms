# E2E documentation coverage (2026-08-17)

This began as a documentation check. A Playwright Chromium smoke suite now exists in
`apps/web/e2e`; it covers the local shell, Clients, Tickets, and the Auth0 entry page.
The Auth0 authenticated journey remains conditional on sandbox session evidence.

## Inventory

| Item | Result |
|---|---|
| Module `E2E_GUIDE.md` files | 39 / 39 (MOD-000 through MOD-630) |
| Handbook | [README.md](README.md) |
| Conventions | [TESTING_CONVENTIONS.md](TESTING_CONVENTIONS.md) |
| Journeys | [CROSS_MODULE_JOURNEYS.md](CROSS_MODULE_JOURNEYS.md) |
| Heading contract | [GUIDE_TEMPLATE.md](GUIDE_TEMPLATE.md) |

Each guide contains: audience, plain-language purpose, status honesty, requirements, how to start, screens/buttons/files, API/data/tests, F-* flows including F-HAPPY and F-AUTHZ, security, planned vs implemented, related journeys, pass/fail checklist.

## Route coverage

All 41 user-facing routes listed in the handbook route map are assigned to a module guide. Navigation source: `apps/web/src/lib/navigation.ts`.

## Honesty samples (must remain labelled non-live)

| Surface | Guide | Label |
|---|---|---|
| Header Create / Bell / AI | Conventions | Planned (no action) |
| Import with AI | MOD-200 | Planned, no handler |
| Generate clarifying questions | MOD-210 | Planned, no handler |
| Document scan / filename version | MOD-250 | Stubbed |
| Temporal start | MOD-350 | Stub by default; local `masms.query_intake` live worker implemented |
| LangGraph / LLM | MOD-360 | Stub by default; `query_intake_agent` OpenAI graph implemented, key required |
| Knowledge search | MOD-370 | Token fallback; OpenAI embeddings + pgvector implemented, key required |
| Gmail / Jira / integrations | MOD-500–520 | Simulation default; sandbox HTTP adapters implemented |
| UAT seed | MOD-620 | Evidence registry plus Playwright smoke |
| Pilot sign-off | MOD-630 | Records; not live production deploy |

## Known doc contradictions left visible (not silently “fixed”)

- Some module READMEs still say FE deferred or AC-901 pending while desks exist and checklists mark M1 Done.
- Progress vs plain checklist task totals still disagree.
- Phase 4 modules are Phase 4 in the plan; some checklists nest them under Phase 3 headings.

## Follow-up (product, not docs)

- Expand Playwright beyond smoke and provide approved Auth0 storage-state evidence.
- Auth0/OpenAI/Gmail/Jira live verification still requires human-provisioned sandbox credentials.
- S3 and SNS/SQS remain stubbed or pending PRE.
