$ErrorActionPreference = "Stop"

# Check if Ollama is installed
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: 'ollama' command not found. Please install Ollama first." -ForegroundColor Red
    exit 1
}

# --- Configuration for Intel Arc 140V (Lunar Lake) ---

# Force Ollama to recognize the iGPU as a viable accelerator
# 999 is often used as a magic number in Intel-optimized builds to force offloading
$env:OLLAMA_NUM_GPU = 999

# Select the Level Zero backend (standard for Intel Arc)
# Device 0 is typically the iGPU on Lunar Lake
$env:ANY_ONEAPI_DEVICE_SELECTOR = "level_zero:0"

# Enable System Management (useful for monitoring tools)
$env:ZES_ENABLE_SYSMAN = 1

# Optional: OneAPI specific library paths (if not set globally)
# $env:ONEAPI_DEVICE_SELECTOR = "level_zero:0"

Write-Host "Starting Ollama with Intel Arc (XPU) configuration..." -ForegroundColor Green
Write-Host "  OLLAMA_NUM_GPU: $env:OLLAMA_NUM_GPU" -ForegroundColor Gray
Write-Host "  Device Selector: $env:ANY_ONEAPI_DEVICE_SELECTOR" -ForegroundColor Gray

# Start the server
ollama serve
