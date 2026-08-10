# scripts

- `generate_implementation_progress_checklist.py` — regenerates
  `MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md` from the module-wise plan and
  the evidence `STATUS` map.
- `mark_complete_checklist_evidence.py` — marks evidenced PRE/MOD-000 items in
  `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md` and writes the evidence log.

```bash
uv run python scripts/generate_implementation_progress_checklist.py
uv run python scripts/mark_complete_checklist_evidence.py
```

Update the `STATUS` / `MARKED` maps when work completes, then regenerate.
Operational scripts beyond this will be added with MOD-010+.
