# IPEX-LLM Portable (Lunar Lake)

This repository contains a fully updated Ollama installation with IPEX-LLM optimizations for the Samsung Galaxy Book5 Pro with Intel Arc 140V iGPU. All workflows use the global `ipex-llm` conda environment.

## Current Setup
- **Ollama Version:** 0.9.3 (updated from portable v0.6.2)
- **IPEX-LLM:** 2.3.0b20251029 with Intel oneAPI 2025.0.1/2025.0.2
- **Installation Type:** Global `ipex-llm` conda environment
- **Location:** `C:\Users\creks\miniconda3\envs\ipex-llm\` (or your global conda env location)
- **Available Memory:** ~18 GB for inference (out of 32 GB unified LPDDR5X)

## Goal
Run INT4 GGUF models efficiently on the Intel Arc 140V iGPU while maintaining good throughput and staying within the unified memory budget.

## Strategy
- **Hardware/Software lockstep:** Everything is tuned for the Intel Arc 140V iGPU on Lunar Lake laptops. The SYCL + Level Zero runtime ensures every layer executes on the XPU, not the CPU.
- **One-time JIT compile:** The first request triggers Intel's kernel compilation pipeline so subsequent prompts reuse optimized binaries tailored to the Arc execution units.
- **Unified memory leverage:** With ~18 GB available for inference, INT4 GGUF models up to ~12B parameters (Phi-4, Gemma 3 12B, etc.) fit comfortably while leaving headroom for Windows.
- **Aggressive low-bit loading:** Default to INT4; only reach for FP8/INT8 if a workload demands more fidelity. This keeps thermals in check while maintaining good throughput.
- **Environment enforcement:** `start-ollama-server.ps1` exports `OLLAMA_NUM_GPU=999`, `ZES_ENABLE_SYSMAN=1`, and related toggles so every layer executes on the Arc iGPU with telemetry available.

## Target Hardware
- Intel Lunar Lake Series 2 laptops (Galaxy Book5 Pro reference)
- Intel Arc 140V iGPU with 32 GB unified LPDDR5X memory (18 GB available for inference)
- Windows 11 with PowerShell and Miniconda3

## What You Get
- **Global Conda Environment:** `ipex-llm` with Python 3.11, IPEX-LLM 2.3.0b20251029, and Intel oneAPI components
- **System-Wide Ollama:** Symbolic links in `C:\Windows\System32` pointing to binaries in the global conda environment
- **Automation Scripts:** PowerShell scripts for server management and updates
- **Model Storage:** `%USERPROFILE%\.ollama` (persistent across updates)

## Automation Scripts
All scripts are located in the `scripts/` directory.

- `scripts/start-ollama-server.ps1`: Start Ollama server with Intel GPU environment variables and required DLL paths (uses global conda env)
- `scripts/update-ipex-llm.ps1`: Update IPEX-LLM in the global conda environment
- `scripts/update-ollama.ps1`: Update Ollama binaries in the global conda environment by running init-ollama.bat (requires Administrator)

## Daily Workflow

### 1. Boot the Server
Open a terminal and run:
```powershell
.\scripts\start-ollama-server.ps1
```
This script:
- Adds Intel oneAPI DLLs to PATH
- Sets Arc GPU environment variables (`OLLAMA_NUM_GPU=999`, `ZES_ENABLE_SYSMAN=1`)
- Launches `ollama serve` on `127.0.0.1:11434`

**Keep this terminal window open** while you work.

### 2. Run Models
Open a **second terminal** for interactive work:
```powershell
ollama run gemma3:12b
```

One-shot prompts:
```powershell
ollama run phi4 "Answer this question"
```

Model management:
```powershell
ollama pull gemma3:12b   # download Gemma 3 12B INT4
ollama pull phi4         # download Phi-4 INT4
ollama list              # installed models
ollama ps                # models currently loaded
ollama stop gemma3:12b   # unload model from memory
```

### 3. Use the REST API
When the server is running you can post to `http://127.0.0.1:11434/api/generate`:
```powershell
$body = @{ model = "llama3.2:3b"; prompt = "Explain unified memory."; stream = $false } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/generate -Body $body -ContentType "application/json"
```

### 4. Tips & Troubleshooting
- **First prompt is slow:** Kernels compile on the Arc GPU the first time; subsequent prompts are fast (cached compilation).
- **Server not responding:** Check if `scripts/start-ollama-server.ps1` is still running. Restart it if needed.
- **Out of memory errors:** You have ~18 GB available. Stick to models ≤12B parameters. gemma3:27b is too large.
- **Model missing?** Run `ollama pull <model>` first, then retry.
- **Slow downloads?** Temporarily set `$env:OLLAMA_MODEL_SOURCE = "modelscope"` before pulling.
- **Check GPU load:** Task Manager → Performance → GPU 0 to confirm inference runs on Intel Arc 140V.
- **Model still loaded?** Use `ollama ps` to check, `ollama stop <model>` to unload.
- **Verify installation:** `ollama --version` should show `0.9.3`.

## Recommended INT4 Models (Tested & Working)

| Model | Size | First Token | Notes |
|-------|------|-------------|-------|
| llama3.2:3b | 2.0 GB | ~2 s | Fast smoke tests, simple queries |
| gemma3:12b | 8.1 GB | ~6 s | **Recommended default** - Excellent quality, technical explanations |
| phi4 | 9.1 GB | ~8 s | Higher quality creative writing, reasoning |

### Models That Don't Work
- **gemma3:27b** (17 GB): Out of device memory error - exceeds available 18 GB
- **gpt-oss:20b** (14 GB): Requires Ollama v0.10+ (current version is 0.9.3)
- **llama3.3:70b** (42 GB): Far too large for available memory

### Memory Guidelines
- Available for inference: ~18 GB (out of 32 GB total unified memory)
- Safe model size: ≤12 GB on disk, ≤10B parameters
- Multiple models can be stored but only one runs at a time

## Installation Details

### Global Conda Environment
```
Name: ipex-llm
Location: (global) C:\Users\creks\miniconda3\envs\ipex-llm\
Python: 3.11.14
IPEX-LLM: 2.3.0b20251029
```

### System-Wide Symbolic Links
Ollama binaries are accessible system-wide via symbolic links in `C:\Windows\System32`:
- `ollama.exe` → global conda environment ollama binary
- `ollama-lib.exe`, DLLs (`ggml-sycl.dll`, etc.) → global conda environment libraries

Created by: `init-ollama.bat` (requires Administrator privileges)

### Intel oneAPI Components
- SYCL Runtime: 2025.0.2
- Level Zero: 2025.0.2
- OpenCL: 2025.0.2
- oneDNN: 2025.0.1
- MKL: 2025.0.1

## Operation Notes
- The startup script exports `OLLAMA_NUM_GPU=999`, `ZES_ENABLE_SYSMAN=1`, and other Level Zero toggles so every prompt runs on the Arc GPU.
- First prompt after a cold start compiles kernels and can take a few minutes; subsequent prompts are fast thanks to caching.
- Unified memory means models share system RAM - larger models leave less for Windows and other apps.
- Models are stored in `%USERPROFILE%\.ollama\models` and persist across Ollama updates.

## Updating

### Update IPEX-LLM
```powershell
.\scripts\update-ipex-llm.ps1
```
This updates to the latest nightly build with new Ollama versions and Intel GPU optimizations.

### Update Ollama Binaries
```powershell
.\scripts\update-ollama.ps1
```
Requires Administrator privileges. Runs `init-ollama.bat` to refresh symbolic links.

**Current Version Limitation:** Latest ipex-llm with [cpp] extras is `2.3.0b20251029` (Ollama v0.9.3). Newer Ollama versions are not yet available in IPEX-LLM releases.

## Quick Start

If you clone this repo, navigate to the `ipex-ollama` directory, launch the server, and pull a model, you are fully set up. There is nothing else to configure.

```powershell
cd ipex-ollama
.\scripts\start-ollama-server.ps1
```
