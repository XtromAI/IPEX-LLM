# Copilot Instructions for IPEX-LLM (Lunar Lake)

## Project Context
This repository contains a conda-based Ollama installation with IPEX-LLM optimizations for the Samsung Galaxy Book5 Pro (Intel Lunar Lake Series 2, Arc 140V iGPU, 32 GB unified memory, 18 GB available for inference). The original portable bundle has been superseded by a system-wide installation using symbolic links.

## Current Architecture
- **Ollama v0.9.3** installed via ipex-llm[cpp] conda package
- **System-wide access** via symbolic links in `C:\Windows\System32`
- **Conda environment:** `ipex-llm` with Python 3.11, IPEX-LLM 2.3.0b20251029
- **Intel oneAPI:** SYCL 2025.0.2, Level Zero 2025.0.2, oneDNN 2025.0.1
- **Model storage:** `%USERPROFILE%\.ollama\models` (persistent across updates)
- **Environment variables:** Set in PowerShell profile for automatic loading

## Guiding Principles
- **Conda-based installation:** All operations assume the conda environment exists and symbolic links are configured
- **System-wide ollama:** Commands work from any directory without `cd ollama-portable`
- **XPU-only inference:** Ensure `OLLAMA_NUM_GPU=999` and Level Zero toggles execute all prompts on Arc 140V
- **INT4 models only:** Recommend models ≤12B parameters (≤10 GB) to fit within 18 GB available memory
- **Automation scripts:** Use PowerShell scripts for server management and updates

## Repository Layout
- `start-ollama-server.ps1`, `update-ipex-llm.ps1`, `update-ollama.ps1` – Automation scripts
- `README.md` – Main documentation: setup, workflow, tested models
- `docs/ollama-commands.md` – Complete Ollama CLI reference
- `docs/portable-ollama.md` – Legacy portable bundle documentation
- `.github/` – This instruction file plus GitHub metadata
- `ollama-portable/` – Legacy bundle (superseded, kept for reference)

## Daily Workflow (mirrors README)
1. **Boot server** (Terminal 1)
    ```powershell
    .\start-ollama-server.ps1
    ```
    Leave this terminal open. The script sets Intel GPU environment variables and launches `ollama serve` on `127.0.0.1:11434`.

2. **Run models** (Terminal 2 - new window)
    ```powershell
    ollama run gemma3:12b          # Interactive chat
    ollama run phi4 "Quick prompt" # One-shot
    ollama pull gemma3:12b         # Download model
    ollama list                    # Show installed
    ollama ps                      # Show loaded
    ollama stop gemma3:12b         # Unload from memory
    ```
    No need to `cd` anywhere - `ollama` is in PATH system-wide.

3. **Use the REST API** when automation/testing is needed:
    ```powershell
    $body = @{ model = "gemma3:12b"; prompt = "Explain unified memory."; stream = $false } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/generate -Body $body -ContentType "application/json"
    ```

## Working Models (INT4 GGUF, Tested)
- `llama3.2:3b` (2 GB) – Fast smoke tests (~2 s first token)
- `gemma3:12b` (8.1 GB) – **Recommended default** for technical work (~6 s first token)
- `phi4` (9.1 GB) – Higher quality writing and reasoning (~8 s first token)

## Models That Don't Work
- `gemma3:27b` (17 GB) – **Out of device memory** (exceeds 18 GB available)
- `gpt-oss:20b` (14 GB) – Requires Ollama v0.10+ (current is v0.9.3)
- `llama3.3:70b` (42 GB) – Far too large for available memory

## Environment Variables (set in PowerShell profile)
- `OLLAMA_NUM_GPU=999` – Force all layers to iGPU
- `ZES_ENABLE_SYSMAN=1` – Enable Arc telemetry
- `SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1` – Performance optimization
- `OLLAMA_HOST=127.0.0.1:11434` – Server binding
- `OLLAMA_NUM_PARALLEL=2`, `OLLAMA_KEEP_ALIVE=10m`, `OLLAMA_CONTEXT_LENGTH=4096`

## Troubleshooting Reminders
- **Server not responding:** Ensure `start-ollama-server.ps1` is still running in its terminal
- **Out of memory:** Stick to models ≤12B parameters; use `ollama stop <model>` to free memory
- **Model missing:** Run `ollama pull <model>` first, then retry
- **Slow downloads:** Set `$env:OLLAMA_MODEL_SOURCE = "modelscope"` temporarily
- **Check GPU load:** Task Manager → Performance → GPU 0 should show activity during inference
- **Command not found:** User PATH should include `C:\Users\creks\miniconda3\envs\ipex-llm\Library\bin` for Intel DLLs
- **Version check:** `ollama --version` should show `0.9.3`

## System Footprint
**Conda Environment:**
- `C:\Users\creks\miniconda3\envs\ipex-llm\` - Python 3.11, IPEX-LLM, Intel oneAPI components

**System-Wide Binaries:**
- `C:\Windows\System32\` - Symbolic links: `ollama.exe`, `ollama-lib.exe`, 7 DLLs pointing to conda environment

**User Data:**
- `C:\Users\creks\.ollama\models\` - Model storage (persistent across updates)
- PowerShell profile: `$PROFILE` - Contains Ollama environment variables

**Modified:**
- User PATH: Added Intel DLL directory for system-wide DLL access
- PowerShell profile: Added Ollama environment variables for automatic loading

## Update Procedures
**Update IPEX-LLM:**
```powershell
.\update-ipex-llm.ps1  # Updates to latest nightly with new Ollama versions
```

**Update Ollama binaries:**
```powershell
.\update-ollama.ps1     # Requires Administrator - runs init-ollama.bat
```

**Current limitation:** Latest ipex-llm[cpp] with Ollama support is `2.3.0b20251029` (Ollama v0.9.3). Newer Ollama versions not yet available in IPEX-LLM releases.

## Expectations for Future Changes
- All operations assume conda environment `ipex-llm` exists with symbolic links configured
- Default to system-wide `ollama` commands rather than portable bundle paths
- When updating docs, reflect the two-terminal workflow (server + client)
- For automation, use PowerShell scripts in repo root or REST API calls
- Model recommendations should stay within 18 GB available memory limit (≤12B parameters)
- Document any new environment variables needed for Intel GPU optimization

These instructions should be updated whenever the conda/symbolic link setup changes or new Intel GPU optimizations become available.
