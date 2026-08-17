# temporal-worker

Local Temporal worker for MOD-350.

Implemented workflow type:

- `masms.query_intake`

Start the local server and worker:

```powershell
docker compose up -d postgres temporal temporal-ui
$env:MASMS_TEMPORAL_ADDRESS = "localhost:7233"
uv run python apps/temporal-worker/worker.py
```

The API selects the live adapter only while `MASMS_TEMPORAL_ADDRESS` is set.
Without it, existing deterministic stub behavior remains active.
