# MOD-130 — Skills, Availability, Capacity, Working Hours, and Business Calendars

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Store skill, proficiency, availability, capacity, leave, time zone, business hours, holidays, and on-call data for assignment eligibility and SLA business-day math.

## M1 delivered

API prefix: `/api/v1/capacity`  
Migration: `20260810_0007`

| ID | Entity |
|---|---|
| MP-001…008 | skills, actor skills, availability, allocations, calendars, holidays, leave, on-call |

Helpers: `POST /evaluate-assignment`, `POST /sla/business-days`

## Limits

- FE deferred
- Leave notes may contain PII — treat as sensitive, do not log content in audit payload (audit has entity id only)
- Project FK soft UUID on allocations
