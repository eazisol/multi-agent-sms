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
uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --host 0.0.0.0 --port 8000

# Web
cp apps/web/.env.example apps/web/.env.local
npm --prefix apps/web install
npm --prefix apps/web run dev
```

Open http://localhost:3000/clients

If you see `/_next/static/...` **404** errors, run a clean dev start (then hard-refresh the browser):

```bash
npm --prefix apps/web run dev:clean
```

## Avoid `/_next/static` 404s permanently

Root cause: `next build` and `next dev` used to share one `.next` folder. Building while the browser still held old chunk URLs produced 404s.

Permanent guardrails in this app:

1. **Separate caches** — `next.dev` uses `.next-dev`; `next build` / `next start` use `.next` (`next.config.ts` `distDir`).
2. **`prebuild` guard** — `npm run build` refuses to start if a Next process is already running for `apps/web`.
3. **Clean restart** — `npm run dev:clean` deletes both caches then starts `next dev`.

Rules of thumb:

- Do not run `npm run build` while `npm run dev` is up.
- After any forced kill/restart of the web server, hard-refresh the tab (Ctrl+Shift+R) or close old tabs.
- For day-to-day local work, keep `NEXT_PUBLIC_API_USE_DIRECT` unset so the browser uses same-origin `/api` rewrites to port **8000** (not 8080).

## Notes

- Uses provisional header-based identity (`X-Actor-*`) until Auth0 wiring is forced in the UI.
- UI role selector is for UX variants; server remains the authority.
- Several Phase 2 APIs are CRUD-lite (no list); desks keep active ids in `localStorage`.
- Package manager: **npm** for this app.
