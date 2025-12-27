# Setup Ollama Portable Zip for Intel Arc GPU (Lunar Lake)
# This script downloads and configures Intel's pre-built Ollama with IPEX-LLM optimizations

param(
    [string]$InstallPath = "$PSScriptRoot\..\ollama-portable",
    [string]$DownloadUrl = "https://github.com/ipex-llm/ipex-llm/releases/download/v2.3.0-nightly/ollama-ipex-llm-2.3.0b20250725-win.zip"
)

$ErrorActionPreference = "Stop"

Write-Host "=== IPEX-LLM Ollama Portable Setup ===" -ForegroundColor Cyan
Write-Host "Target: Intel Arc 140V (Lunar Lake)" -ForegroundColor Cyan
Write-Host ""

# Create install directory
$InstallPath = [System.IO.Path]::GetFullPath($InstallPath)
if (-not (Test-Path $InstallPath)) {
    Write-Host "Creating installation directory: $InstallPath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
}

# Download Ollama Portable Zip
$ZipFile = Join-Path $env:TEMP "ollama-portable.zip"
Write-Host "Downloading Ollama Portable Zip (~500MB)..." -ForegroundColor Yellow
Write-Host "From: $DownloadUrl" -ForegroundColor Gray

try {
    # Use Invoke-WebRequest with progress
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipFile -UseBasicParsing
    $ProgressPreference = 'Continue'
    Write-Host "[OK] Download complete" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual download instructions:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://github.com/ipex-llm/ipex-llm/releases/tag/v2.3.0-nightly" -ForegroundColor Gray
    Write-Host "2. Download: ollama-windows-ipex-llm-*.zip" -ForegroundColor Gray
    Write-Host "3. Extract to: $InstallPath" -ForegroundColor Gray
    exit 1
}

# Extract
Write-Host "Extracting to $InstallPath..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $ZipFile -DestinationPath $InstallPath -Force
    Remove-Item $ZipFile -Force
    Write-Host "[OK] Extraction complete" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Extraction failed: $_" -ForegroundColor Red
    exit 1
}

# Create convenience launcher script
$LauncherScript = Join-Path $PSScriptRoot "start-ollama-server.ps1"
$LauncherContent = @"
# Start Ollama Server with IPEX-LLM optimizations
`$OllamaPath = "$InstallPath"

Write-Host "Starting Ollama Server (Intel Arc GPU)..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

Push-Location `$OllamaPath
& .\start-ollama.bat
Pop-Location
"@

Set-Content -Path $LauncherScript -Value $LauncherContent -Encoding UTF8
Write-Host "[OK] Created launcher: $LauncherScript" -ForegroundColor Green

# Create client helper script
$ClientScript = Join-Path $PSScriptRoot "ollama-cli.ps1"
$ClientContent = @"
# Ollama CLI Helper
# Usage: .\ollama-cli.ps1 run deepseek-r1:7b
param([Parameter(ValueFromRemainingArguments)]`$Args)

`$OllamaPath = "$InstallPath"
`$env:PATH = "`$OllamaPath;`$env:PATH"

& "`$OllamaPath\ollama.exe" `@Args
"@

Set-Content -Path $ClientScript -Value $ClientContent -Encoding UTF8
Write-Host "[OK] Created CLI helper: $ClientScript" -ForegroundColor Green

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Start the server:" -ForegroundColor White
Write-Host "   .\scripts\start-ollama-server.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. In a NEW terminal, run a model:" -ForegroundColor White
Write-Host "   cd $InstallPath" -ForegroundColor Gray
Write-Host "   .\ollama.exe run deepseek-r1:7b" -ForegroundColor Gray
Write-Host ""
Write-Host "   Or use the helper script:" -ForegroundColor White
Write-Host "   .\scripts\ollama-cli.ps1 run deepseek-r1:7b" -ForegroundColor Gray
Write-Host ""
Write-Host "Popular models to try:" -ForegroundColor Cyan
Write-Host "  • deepseek-r1:7b       (7B reasoning model)" -ForegroundColor Gray
Write-Host "  • qwen2.5:7b           (7B general purpose)" -ForegroundColor Gray
Write-Host "  • llama3.2:3b          (3B fast model)" -ForegroundColor Gray
Write-Host "  • phi4                 (14B high quality)" -ForegroundColor Gray
Write-Host ""
Write-Host "Note: First run will be slow due to GPU kernel compilation." -ForegroundColor Yellow
Write-Host "Subsequent runs will be much faster." -ForegroundColor Yellow
