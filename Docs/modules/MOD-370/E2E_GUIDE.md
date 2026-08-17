# MOD-370 — Versioned Knowledge and Citation Search

> **Implementation update (2026-08-17):** Migration `20260817_0039` adds a pgvector
> embedding column and HNSW cosine index. With an approved OpenAI key/model, activation stores
> real embeddings and search applies tenant/project/permission filters before pgvector ranking.
> Without that configuration, token-overlap and JSON stub vectors remain the test fallback.

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Publish test knowledge and retrieve a citation. |
| QA | Test active-version filtering, tenant/project scope, and stub search. |
| Developer | Verify item/version/chunk/permission/usage APIs. |
| Owner | Understand the shortcut and missing approval workflow. |

## 2. What this module is

The knowledge base stores versioned content, permissions, chunks, retrieval artifacts, usage, conflicts, and source citations.

In this company it means an answer should point to an approved source such as `policy_change@v1#chunk-0`, not unsupported model memory.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/knowledge` desk | **Implemented** | Publish, list, paginate, search |
| Publish shortcut | **Implemented** | Creates item + version + activates |
| Citation search | **Stubbed** | Token overlap and deterministic vectors |
| Embeddings | **Stubbed** | JSON vectors, not pgvector |
| Live embedding model/pgvector | **Planned** | Not exercised |
| Separate exact-version approval | **Planned** | Target design requires MOD-330 workflow |
| Conflict/permission/usage UI | **Planned** | API only |
| Header identity | **Stubbed** | Not authentication |
| Human Done approval | **Implemented record** | Owner sign-off recorded 2026-08-11 |

## 4. Requirements and dependencies

- Item belongs to organization and optionally project.
- Activation creates chunks and stub embeddings and supersedes prior active version.
- Only active approved-equivalent content is retrieved; draft/rejected/superseded/expired versions are excluded.
- Permission deny blocks retrieval.
- Project scope may boost matching project content.

## 5. How to start

1. Start API/web and migrated PostgreSQL.
2. Optionally select a project so the Project id field is prefilled.
3. Open `/knowledge`.
4. Use synthetic content containing a unique phrase.
5. Open `/docs` for versions, permissions, conflicts, chunks, and usage.

## 6. Screens, buttons, and files

Desk: [`knowledge-desk-page.tsx`](../../../apps/web/src/components/knowledge-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Publish item | Opens combined publish form | Implemented | `knowledge-desk-page.tsx` |
| Code/Title/Body | Required content fields | Implemented | `knowledge-desk-page.tsx` |
| Project id | Optional project scope | Implemented | `knowledge-desk-page.tsx` |
| Publish | Creates item/version and immediately activates | Implemented shortcut | `knowledge-desk-page.tsx` |
| Stub search Query | Accepts retrieval query | Stubbed runtime | `knowledge-desk-page.tsx` |
| Search | Returns ranked cited hits | Stubbed runtime | `knowledge-desk-page.tsx` |
| Citation result | Shows title, score, citation, excerpt | Implemented display | `knowledge-desk-page.tsx` |
| Pagination | Changes item limit/offset | Implemented | `knowledge-desk-page.tsx` |
| Approve/activate separately | No controls | Planned | — |
| Permissions/conflicts/usage | No controls | Implemented API only | `router.py` |

## 7. API, data, and automated tests

Router: [`router.py`](../../../apps/api/src/masms_api/modules/knowledge/router.py)  
Prefix: `/api/v1/knowledge`

| Method | Path | Purpose |
|---|---|---|
| POST/GET | `/items` | Create/list |
| GET | `/items/{id}` | Read item |
| POST | `/items/{id}/versions` | Create version |
| GET | `/versions` | List versions |
| POST | `/versions/{id}/activate` | Activate/chunk |
| GET | `/versions/{id}/chunks` | Read chunks |
| POST/GET | `/items/{id}/permissions` | Permission rules |
| POST | `/search` | Stub retrieval with citations |
| POST/GET | `/conflicts`, `/conflicts/{id}/resolve` | Conflict lifecycle |
| GET | `/usage-logs` | Retrieval usage |

Test:

- `tests/integration/knowledge/test_knowledge_api.py`
- `uv run pytest tests/integration/knowledge -q --tb=short`

## 8. Test flows

Capture item/version/chunk IDs, active status, project scope, citation, score, `stub=true`, permission, usage, audit, and outbox.

### F-SETUP

1. Open `/knowledge`; click **Publish item**.
2. Choose unique code/title and body phrase, e.g. `E2E cobalt approval phrase`.
3. Decide whether item is org-generic or project-scoped.
4. **Expected:** form states it creates item + version and activates with stub embeddings.

### F-HAPPY

1. Click **Publish**.
2. Expect “Knowledge item published” and item in list.
3. Enter the unique phrase under **Stub search** and click **Search**.
4. Expect a hit with title, score, excerpt, and `code@vN#chunk-I`.
5. Inspect POST `/search`; expect `stub: true`.
6. Inspect version chunks and usage log through OpenAPI.

### F-VALIDATE

1. Submit blank Code, Title, or Body; browser required validation blocks.
2. Attempt duplicate code or invalid item/version ID through API.
3. Expect conflict/not-found and no partial active content.

### F-AUTHZ

1. Add a deny permission through API for a test actor/scope.
2. Search as denied actor.
3. Expect no hit/forbidden according to contract.
4. UI has no permission editor; backend result is authoritative.

### F-TENANT

1. List/read/search under another organization header.
2. Expect no item, chunk, citation, permission, or usage disclosure.
3. Never use another client’s content as test data.

### F-CONCUR

1. Create two versions and attempt competing activation.
2. Expect one current active version and prior active superseded.
3. No `expected_version` is exposed; record any dual-active defect.

### F-TRANS

1. Search while only a draft/unactivated version contains the phrase.
2. Expect no hit.
3. Search after prior version is superseded/rejected/expired.
4. Expect inactive content excluded.

### F-GATE

1. Observe that UI **Publish** immediately activates content.
2. Mark this an implemented shortcut, not separate human approval.
3. Target exact-version MOD-330 approval workflow is **Planned/non-testable**.
4. Do not treat button click as production publication approval.

### F-TERM

1. Activate a newer version.
2. Confirm prior version is superseded and not retrieved.
3. No delete/reactivate desk controls exist; preserve version history.

### F-RECOVER

1. Force one of the combined create/version/activate calls to fail in a test environment.
2. Reload item/version state before retrying to avoid duplicate code/version.
3. Resolve conflicts through API when applicable.
4. No embedding worker or pgvector recovery is claimed.

### F-CLEAN

Leave synthetic items clearly prefixed `E2E`. Preserve versions, chunks, permission, usage, conflict, audit, and outbox evidence.

## 9. Security, privacy, and approvals

- Tenant/project and permission filters apply before retrieval.
- Store only approved, sanitized content; never secrets.
- Citations support traceability but do not prove source approval.
- Stub retrieval quality is not an LLM/semantic-search evaluation.
- Production activation should require the planned exact-version human workflow.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Separate draft/review/approve/activate | Planned; combined Publish shortcut |
| Live embeddings | Stubbed |
| pgvector similarity | Planned; JSON vectors |
| Knowledge detail/version UI | Planned |
| Permission/conflict/usage UI | API only |

## 11. Related journeys

- MOD-330 should approve exact knowledge versions.
- MOD-360 may later consume permission-filtered RAG.
- MOD-120 and project membership constrain retrieval.

## 12. Pass / fail checklist

- [ ] Combined Publish creates item/version/active state
- [ ] Published item appears and paginates
- [ ] Search returns source citation
- [ ] Response says `stub=true`
- [ ] Draft/inactive content is excluded
- [ ] Superseded content is excluded
- [ ] Deny permission blocks retrieval
- [ ] Cross-tenant search does not leak
- [ ] Stub JSON embeddings documented
- [ ] Approval workflow marked Planned
- [ ] No live pgvector/model claim made
- [ ] Automated result recorded
