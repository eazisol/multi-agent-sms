#!/usr/bin/env bash
set -euo pipefail
echo "== uv sync =="
uv sync
echo "== ruff =="
uv run ruff check apps/api/src tests
echo "== mypy =="
uv run mypy apps/api/src/masms_api
echo "== pytest =="
uv run pytest -q
echo "== web lint =="
npm --prefix apps/web run lint
echo "== web build =="
npm --prefix apps/web run build
echo "All MOD-010 local quality gates passed."
