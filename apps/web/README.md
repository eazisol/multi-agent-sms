# MASMS Web (`apps/web`)

Next.js 15 frontend for MASMS.

## Current desks

- **Clients** (`/clients`) — MOD-200
- **Queries** (`/queries`) — MOD-210
- **Projects & SRS** (`/projects`) — MOD-240
- **Documents** (`/documents`) — MOD-250
- **Roadmap** (`/roadmap`) — MOD-260
- **Governance baselines** (`/governance/baselines`) — MOD-000

Comms (MOD-220) and requirement-gathering (MOD-230) desks are deferred to a later FE pass.

## Run

```bash
# API
uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --port 8000

# Web
cp apps/web/.env.example apps/web/.env.local
npm --prefix apps/web install
npm --prefix apps/web run dev
```

Open http://localhost:3000/clients

## Notes

- Uses provisional header-based identity (`X-Actor-*`) until Auth0 wiring is forced in the UI.
- UI role selector is for UX variants; server remains the authority.
- Several Phase 2 APIs are CRUD-lite (no list); desks keep active ids in `localStorage`.
- Package manager: **npm** for this app.
