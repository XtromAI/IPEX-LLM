param(
    [switch]$Unregister
)

$ErrorActionPreference = "Stop"

$taskName = "IPEX-LLM Ollama Server"

if ($Unregister) {
    Write-Host "Removing scheduled task '$taskName'..." -ForegroundColor Yellow
    try {
        schtasks.exe /Delete /TN "$taskName" /F | Out-Null
        Write-Host "[OK] Autostart task removed." -ForegroundColor Green
    } catch {
        Write-Host "[WARN] Failed to remove scheduled task or task did not exist." -ForegroundColor Yellow
    }
    return
}

Write-Host "Registering scheduled task to start Ollama server at user logon..." -ForegroundColor Cyan

$scriptPath = Join-Path $PSScriptRoot "start-ollama-server.ps1"
if (-not (Test-Path $scriptPath)) {
    Write-Host "[ERROR] start-ollama-server.ps1 not found at $scriptPath" -ForegroundColor Red
    exit 1
}

$psExe = Join-Path $env:SystemRoot "System32\\WindowsPowerShell\\v1.0\\powershell.exe"
$command = "`"$psExe`" -NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

try {
    # Create or update the task
    schtasks.exe /Create /
        TN "$taskName" /
        TR "$command" /
        SC ONLOGON /
        RL HIGHEST /
        F | Out-Null

    Write-Host "[OK] Autostart task registered: $taskName" -ForegroundColor Green
    Write-Host "The Ollama server will start automatically at logon." -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Failed to register scheduled task: $_" -ForegroundColor Red
    exit 1
}
