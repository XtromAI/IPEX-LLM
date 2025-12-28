# Start Ollama Server with Intel GPU optimizations
# This script sets required environment variables and launches ollama serve
# The server will run until you close this window or press Ctrl+C

Write-Host "Starting Ollama server with Intel GPU optimizations..." -ForegroundColor Green
Write-Host ""

# Check if ollama is available
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaPath) {
    Write-Host "ERROR: ollama command not found!" -ForegroundColor Red
    Write-Host "Make sure you ran update-ollama.ps1 as Administrator first." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Ollama found at: $($ollamaPath.Source)" -ForegroundColor Green
Write-Host ""



Write-Host "No PATH update needed. Windows symbolic links provide access to all required binaries and DLLs."
Write-Host ""

Write-Host "Permanent environment variables already set. Ready to launch Ollama server." -ForegroundColor Cyan
Write-Host "  OLLAMA_NUM_GPU: $env:OLLAMA_NUM_GPU"
Write-Host "  ZES_ENABLE_SYSMAN: $env:ZES_ENABLE_SYSMAN"
Write-Host "  OLLAMA_HOST: $env:OLLAMA_HOST"
Write-Host ""
Write-Host "Server starting... (Keep this window open)" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor DarkGray
Write-Host ""

# Start ollama serve (this is a blocking operation)
& ollama serve

Write-Host ""
Write-Host "Server has stopped." -ForegroundColor Yellow
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
