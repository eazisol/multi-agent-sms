# Detect LAN IP, update env + status MD, then start Docker + API + Web for same-Wi-Fi access.
# Usage (repo root):
#   powershell -ExecutionPolicy Bypass -File scripts/start-lan-server.ps1

[CmdletBinding()]
param(
    [string]$RepoRoot = "",
    [int]$ApiPort = 8000,
    [int]$WebPort = 3000,
    [switch]$SkipDocker
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $RepoRoot) {
    $scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
    $RepoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
}

Set-Location $RepoRoot

Write-Host "==> Refreshing LAN IP / env / status MD"
& powershell -ExecutionPolicy Bypass -File (Join-Path $RepoRoot "scripts\update-lan-server.ps1") -RepoRoot $RepoRoot -ApiPort $ApiPort -WebPort $WebPort
if ($LASTEXITCODE -ne 0) {
    throw "update-lan-server.ps1 failed"
}

$statusPath = Join-Path $RepoRoot "Docs\local-wifi-server-status.md"
if (Test-Path $statusPath) {
    Write-Host ""
    Write-Host "---- share these URLs ----"
    Select-String -Path $statusPath -Pattern "Web \(share|Queries|API health" | ForEach-Object { $_.Line }
    Write-Host "--------------------------"
    Write-Host ""
}

if (-not $SkipDocker) {
    Write-Host "==> Starting Postgres + Redis"
    docker compose up -d postgres redis
}

Write-Host "==> Ensuring Python deps + migrations"
uv sync
uv run alembic upgrade head

function Stop-PortListeners {
    param([int[]]$Ports)
    foreach ($port in $Ports) {
        $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
        foreach ($c in $conns) {
            $procId = $c.OwningProcess
            if ($procId) {
                Write-Host "Stopping PID $procId on port $port"
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

Stop-PortListeners -Ports @($ApiPort, $WebPort)
Start-Sleep -Seconds 1

$apiCmd = "uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --host 0.0.0.0 --port $ApiPort"
$webCmd = "npm --prefix apps/web run dev -- --hostname 0.0.0.0 --port $WebPort"

Write-Host "==> Starting API on 0.0.0.0:$ApiPort"
Start-Process -FilePath "powershell.exe" -WorkingDirectory $RepoRoot -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command", $apiCmd
)

Write-Host "==> Starting Web on 0.0.0.0:$WebPort"
if (-not (Test-Path (Join-Path $RepoRoot "apps\web\node_modules"))) {
    npm --prefix apps/web install
}
Start-Process -FilePath "powershell.exe" -WorkingDirectory $RepoRoot -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command", $webCmd
)

Write-Host ""
Write-Host "PC backend (API) and optional local Web launched in new PowerShell windows."
Write-Host "Live UI: https://multi-agent-sms.vercel.app/queries"
Write-Host "If LAN IP changed: paste Docs\vercel-lan.env.txt into Vercel env vars and Redeploy."
Write-Host "Status file: $statusPath"
Write-Host "Guide: Docs\local-wifi-server.md"
