# MOD-520 Jira Work Management Integration (M1)

## Scope delivered in M1

- Approval-gated Jira issue push endpoint that only accepts approved internal tickets.
- Inbound Jira status webhook handling that records a conflict and blocks internal status mutation.
- Jira comment sync flow with visible failed attempts and explicit retry endpoint.
- Simulated Jira behavior for local/integration testing (`SIM-*` issue key support).

## Backend components

- Module: `apps/api/src/masms_api/modules/jira`
  - `models.py`: `jr_issue_pushes`, `jr_status_conflicts`, `jr_comment_syncs`
  - `service.py`: approval gate, webhook conflict, retryable comment sync
  - `router.py`: `/api/v1/jira/*` endpoints
  - `domain.py`: Jira-specific domain invariants
  - `schemas.py`: transport contracts

## Frontend components

- Desk page route: `apps/web/src/app/jira/page.tsx`
- Desk UI: `apps/web/src/components/jira-desk-page.tsx`
- API helpers: `apps/web/src/lib/api.ts`
- Navigation entry: `apps/web/src/lib/navigation.ts` (`ready: true`)

## API endpoints (M1)

- `POST /api/v1/jira/issues/push`
- `GET /api/v1/jira/issues/pushes`
- `POST /api/v1/jira/webhooks/status` (returns `409` with conflict payload)
- `POST /api/v1/jira/comments/sync`
- `GET /api/v1/jira/comments/sync`
- `POST /api/v1/jira/comments/sync/{sync_id}/retry`

## Notes

- Jira webhook status updates are intentionally non-authoritative for internal workflow state.
- Internal approvals remain the required gate for issue creation.
