# MOD-370 — Knowledge Base, Approved Content, Permission-Filtered RAG, and Source Citation

**Status:** M1 Done (human AC-901 approved 2026-08-11; stub retrieval; live embeddings/pgvector deferred)
**Human Done (AC-901):** Obtained 2026-08-11

## Purpose

Persist approved, versioned, permission-controlled knowledge with chunking, stub embeddings, usage logs, conflicts, and citation-bearing search.

## Honesty (M1 limits)

- Live embedding model / pgvector cluster is **not** required.
- `KnowledgeRetrievalAdapter` uses token-overlap scoring + deterministic stub vectors in JSON.
- FE is list + publish + search — not a full knowledge studio.
- Notifications / Temporal / LangGraph wiring deferred.
- AC-901 obtained 2026-08-11 (human owner sign-off).

## M1 delivered

API: `/api/v1/knowledge`  
Migration: `20260811_0023`  
FE: `/knowledge`

| ID | Entity |
|---|---|
| MP-001 | `kn_items` |
| MP-002 | `kn_versions` |
| MP-003 | `kn_chunks` |
| MP-004 | `kn_embeddings` (stub vectors) |
| MP-005 | `kn_permissions` |
| MP-006 | `kn_usage_logs` |
| MP-007 | `kn_conflicts` |

## Acceptance behavior (M1)

- **AC-001:** Hits include `source_citation` = `{code}@v{n}#chunk-{i}`
- **AC-002:** Project-scoped items get a score boost when `project_id` is supplied
- **AC-003:** Draft / rejected / superseded / expired versions are not retrieved

## Key rules

- Activate builds chunks + stub embeddings; supersedes prior active version
- Default org allow permission on create; deny effect blocks retrieve
- Outbox: `knowledge.item.created`, `.version.activated`, `.search.completed`, `.conflict.opened`
