# Start Ollama Server with IPEX-LLM optimizations
$OllamaPath = "C:\Users\creks\Documents\IPEX-LLM\ollama-portable"

Write-Host "Starting Ollama Server (Intel Arc GPU)..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

Push-Location $OllamaPath
& .\start-ollama.bat
Pop-Location
