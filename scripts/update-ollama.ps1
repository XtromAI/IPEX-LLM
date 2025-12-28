# Update Ollama binaries with Intel GPU support
# This script must be run as Administrator

Write-Host "Updating Ollama binaries..." -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then try again." -ForegroundColor Yellow
    exit 1
}


Write-Host "Activating global ipex-llm environment..." -ForegroundColor Cyan
conda activate ipex-llm

# Run init-ollama.bat to create symbolic links
Write-Host "Running init-ollama.bat to update Ollama binaries..." -ForegroundColor Cyan
init-ollama.bat

Write-Host ""
Write-Host "Ollama binaries updated successfully!" -ForegroundColor Green
Write-Host "You can now use the latest Ollama version with Intel GPU support." -ForegroundColor Yellow
