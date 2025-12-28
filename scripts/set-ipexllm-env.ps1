# Permanently set environment variables for IPEX-LLM/Ollama workflow
$envVars = @{
    "OLLAMA_NUM_GPU" = "999"
    "ZES_ENABLE_SYSMAN" = "1"
    "OLLAMA_NUM_PARALLEL" = "2"
    "OLLAMA_KEEP_ALIVE" = "10m"
    "OLLAMA_HOST" = "127.0.0.1:11434"
    "SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS" = "1"
}

foreach ($key in $envVars.Keys) {
    [Environment]::SetEnvironmentVariable($key, $envVars[$key], "User")
    Write-Host "Set $key=$($envVars[$key]) (User scope)" -ForegroundColor Green
}

Write-Host "All environment variables set permanently for your user account." -ForegroundColor Cyan
