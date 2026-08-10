# MASMS Web (`apps/web`)

Next.js 15 frontend for MASMS. Current scope: **MOD-000 baselines UI only**.

## Run

```bash
# API
uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --port 8000

# Web
cp apps/web/.env.example apps/web/.env.local
npm --prefix apps/web install
npm --prefix apps/web run dev
```

Open http://localhost:3000/governance/baselines

## Notes

- Uses provisional header-based identity (`X-Actor-*`) until Auth0 / MOD-110.
- UI role selector is for UX variants from `docs/governance/UI_ROLE_VARIANTS.md`.
- Server remains the authority for approve/reject and org isolation.
- Package manager: **npm** for this app (pnpm host activation blocked).
