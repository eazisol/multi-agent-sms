#Requires -Version 5.1
$ErrorActionPreference = "Stop"
Write-Host "== uv sync =="
uv sync
Write-Host "== ruff =="
uv run ruff check apps/api/src tests
Write-Host "== mypy =="
uv run mypy apps/api/src/masms_api
Write-Host "== pytest =="
uv run pytest -q
Write-Host "== web lint =="
npm --prefix apps/web run lint
Write-Host "== web build =="
npm --prefix apps/web run build
Write-Host "All MOD-010 local quality gates passed."
