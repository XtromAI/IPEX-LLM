# Update IPEX-LLM and Ollama to latest versions
# Run this script periodically to keep your installation up to date

Write-Host "Updating IPEX-LLM to latest version..." -ForegroundColor Green

# Activate the global ipex-llm conda environment
conda activate ipex-llm

# Update ipex-llm package in global env
Write-Host "Installing latest ipex-llm[cpp] in global env..." -ForegroundColor Cyan
pip install --pre --upgrade ipex-llm[cpp]

Write-Host ""
Write-Host "Update complete! (global env)" -ForegroundColor Green
Write-Host "To update Ollama binaries, run init-ollama.bat as Administrator." -ForegroundColor Yellow
