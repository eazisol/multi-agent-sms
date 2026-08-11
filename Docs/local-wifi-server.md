# Local Wi‑Fi backend for the Vercel live app

**Goal:** Your Windows PC runs the MASMS API (and DB). Teammates on the **same Wi‑Fi** use the live UI:

[https://multi-agent-sms.vercel.app/queries](https://multi-agent-sms.vercel.app/queries)

When the PC backend is up and the Vercel env points at your current LAN IP, the live app talks to your machine.

## How the live app reaches your PC

The web client can call the API in two ways (`apps/web/src/lib/api.ts` + `next.config.ts`):

| Mode | Vercel env | Who connects to your PC |
|---|---|---|
| **Browser direct (same Wi‑Fi)** | `NEXT_PUBLIC_API_USE_DIRECT=true` and `NEXT_PUBLIC_API_BASE_URL=http://YOUR-LAN-IP:8000` | Each teammate’s browser → your PC `:8000` |
| **Same-origin rewrite** | `MASMS_API_ORIGIN=https://…tunnel…` | Vercel’s servers → tunnel → your PC (needs HTTPS tunnel; private LAN IPs are not reachable from Vercel) |

For office/home Wi‑Fi demos, use **browser direct**. Keep CORS allowing the Vercel origin (the daily script does this).

## Daily workflow

### 1) Start your PC as the backend

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-lan-server.ps1
```

This:

1. Detects today’s Wi‑Fi / LAN IPv4
2. Updates `.env` → `MASMS_CORS_ORIGINS` (includes `https://multi-agent-sms.vercel.app`)
3. Updates `apps/web/.env.local` for local UI work
4. Writes `Docs/local-wifi-server-status.md` with the IP and the Vercel env values to set
5. Starts Postgres + Redis + API on `0.0.0.0:8000` (and local web on `:3000` if you want it)

IP refresh only:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/update-lan-server.ps1
```

### 2) Point Vercel at today’s IP

Open `Docs/local-wifi-server-status.md` and copy the **Vercel environment** block into the Vercel project (Settings → Environment Variables), then **redeploy** when the IP changes.

Required for same‑Wi‑Fi browser direct:

```text
NEXT_PUBLIC_API_USE_DIRECT=true
NEXT_PUBLIC_API_BASE_URL=http://YOUR-LAN-IP:8000
```

Optional CORS on your PC (already set by the script):

```text
MASMS_CORS_ORIGINS=...,https://multi-agent-sms.vercel.app
```

### 3) Share with the team

- UI: https://multi-agent-sms.vercel.app/queries  
- Everyone must be on the **same Wi‑Fi** as your PC  
- Your PC must stay on with `start-lan-server.ps1` (API) running  

## Windows Firewall (first time)

```powershell
New-NetFirewallRule -DisplayName "MASMS API 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

(Local Next on `:3000` is optional; only needed if someone uses `http://YOUR-LAN-IP:3000` instead of Vercel.)

## Task Scheduler (refresh IP daily)

1. Task Scheduler → Create Basic Task → Daily or At log on  
2. Program: `powershell.exe`  
3. Arguments:

```text
-ExecutionPolicy Bypass -File "C:\Eazisols\Multi-Agent Software House Management System\scripts\update-lan-server.ps1"
```

After DHCP changes your IP, update Vercel `NEXT_PUBLIC_API_BASE_URL` from the status file and redeploy (or use the Vercel CLI if you automate that separately).

## If the live site cannot reach the API

1. Confirm `http://YOUR-LAN-IP:8000/health` opens from another phone/laptop on the same Wi‑Fi  
2. Confirm firewall allows `8000`  
3. Confirm Vercel has `NEXT_PUBLIC_API_USE_DIRECT=true` and the matching `NEXT_PUBLIC_API_BASE_URL`  
4. Confirm PC `.env` CORS includes `https://multi-agent-sms.vercel.app`  
5. If a browser blocks HTTP from the HTTPS Vercel page, put an HTTPS tunnel in front of `:8000` and set `NEXT_PUBLIC_API_BASE_URL` to that `https://…` URL instead  

## Security

- Bind is `0.0.0.0` on the LAN only — do **not** port-forward `:8000` on the router to the public internet  
- Treat this as a trusted Wi‑Fi demo backend, not production  
- Stop the API when you are done sharing  
