# Test that all required environment variables are set
$requiredVars = @(
    "OLLAMA_NUM_GPU",
    "ZES_ENABLE_SYSMAN",
    "OLLAMA_NUM_PARALLEL",
    "OLLAMA_KEEP_ALIVE",
    "OLLAMA_HOST",
    "SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS"
)

foreach ($var in $requiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var, "User")
    if ($null -eq $value -or $value -eq "") {
        Write-Host "$var is NOT set!" -ForegroundColor Red
    } else {
        Write-Host "$var=$value" -ForegroundColor Green
    }
}
