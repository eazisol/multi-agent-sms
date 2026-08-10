# scripts

- `generate_implementation_progress_checklist.py` — detailed plan-ID progress checklist
- `generate_plain_module_checklist.py` — easy Module → M1 → M1-1 plain checklist
- `mark_complete_checklist_evidence.py` — marks evidenced items in the complete checklist

```bash
uv run python scripts/generate_implementation_progress_checklist.py
uv run python scripts/generate_plain_module_checklist.py
uv run python scripts/mark_complete_checklist_evidence.py
```

Update STATUS / MARKED maps when work completes, then regenerate.
