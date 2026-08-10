# ADR-0001 — System architecture boundaries

**Status:** Proposed (PENDING human approval — major architecture gate)  
**Date (UTC):** 2026-08-10  
**Module:** MOD-000  
**Requirements:** MVP-NFR-004, MVP-NFR-010, Tech Stack Doc  
**Decision makers:** PENDING Engineering Lead / Architect / Product Owner

## Context

MASMS needs deterministic business control, durable long-running workflows, and bounded AI reasoning without conflating those concerns.

## Options considered

1. Single FastAPI process handling business state, timers, and agent reasoning  
2. Separate FastAPI / Temporal / LangGraph boundaries with PostgreSQL as SoT  
3. Event-sourced system of record with no transactional PostgreSQL primary store  

## Decision (provisional for implementation scaffolding)

Adopt option 2:

| Concern | Owner |
|---|---|
| Deterministic validation, permissions, mutations, audit | FastAPI |
| Durable waits, timers, retries, signals, escalations, approval pauses | Temporal |
| Bounded AI reasoning and recommendations | LangGraph |
| Authoritative transactional state | PostgreSQL |
| Permission-filtered semantic retrieval | pgvector (never SoT) |
| Async domain/integration events | Azure Service Bus or approved broker + transactional outbox |

Agents must not write business tables directly or receive raw secrets.

## Consequences

- Clear module ownership and safer approvals  
- More moving parts (workers) and operational complexity  
- Requires MOD-020 kernel and MOD-030/MOD-040 operational foundations  

## Security / rollback

- Deny-by-default authorization remains in FastAPI  
- Rollback of this ADR requires a new ADR + human approval; do not silently collapse boundaries
