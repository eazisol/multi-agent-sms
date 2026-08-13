# scripts

- `generate_implementation_progress_checklist.py` — detailed plan-ID progress checklist
- `generate_plain_module_checklist.py` — easy Module → M1 → M1-1 plain checklist
- `mark_complete_checklist_evidence.py` — marks evidenced items in the complete checklist
- `load_dummy_data.py` — wipe local Postgres and load up to 20 realistic dummy records per entity via the running API
- `dummy_catalogs.py` — synthetic client/people/project catalogs used by the loader
- `update-lan-server.ps1` — detect Wi‑Fi/LAN IP, update CORS + web API URL, regenerate `Docs/local-wifi-server-status.md`
- `start-lan-server.ps1` — run update script, then start Docker + API (`0.0.0.0:8000`) + Web (`0.0.0.0:3000`) for same‑Wi‑Fi sharing

```bash
uv run python scripts/generate_implementation_progress_checklist.py
uv run python scripts/generate_plain_module_checklist.py
uv run python scripts/mark_complete_checklist_evidence.py
# API must be running against Postgres
uv run python scripts/load_dummy_data.py --count 20
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/update-lan-server.ps1
powershell -ExecutionPolicy Bypass -File scripts/start-lan-server.ps1
```

Guide: `Docs/local-wifi-server.md`

Update STATUS / MARKED maps when work completes, then regenerate.
