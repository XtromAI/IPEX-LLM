# IPEX-LLM Portable (Lunar Lake)

This repository is now scoped exclusively to the proven solution: Intel's Ollama Portable bundle tuned for the Samsung Galaxy Book5 Pro with the Intel Arc 140V iGPU. Everything else was removed so the repo only contains the assets required to download, launch, and operate the portable runtime.

## Goal
Run the largest possible INT4 GGUF models on this hardware while sustaining at least 15 tokens per minute of generation throughput.

## Strategy
- **Hardware/Software lockstep:** Everything is tuned for the Intel Arc 140V iGPU on Lunar Lake laptops. The Level Zero + SYCL runtime bundled inside `ollama-portable/` ensures every kernel lands on the XPU, not the CPU.
- **One-time JIT compile:** The first request triggers Intel's kernel compilation pipeline so subsequent prompts reuse optimized binaries tailored to the Arc execution units.
- **Unified memory leverage:** With 32 GB shared LPDDR5X, INT4 GGUF builds of models up to ~32B parameters (Phi-4, Gemma 3 27B, etc.) comfortably fit while leaving headroom for Windows.
- **Aggressive low-bit loading:** Default to INT4; only reach for FP8/INT8 if a workload demands more fidelity. This keeps thermals in check while hitting the 15 tokens/min throughput floor.
- **Environment enforcement:** `start-ollama.bat` exports `OLLAMA_NUM_GPU=999`, `ZES_ENABLE_SYSMAN=1`, and related toggles so every layer executes on the Arc iGPU with telemetry available.

## Target Hardware
- Intel Lunar Lake Series 2 laptops (Galaxy Book5 Pro reference)
- Intel Arc 140V iGPU with 32 GB unified LPDDR5X memory
- Windows 11 with PowerShell

## What You Get
- `ollama-portable/`: Intel's prebuilt Ollama distribution with IPEX-LLM optimizations, runtime DLLs, and helper batch files (`start-ollama.bat`, `ollama-serve.bat`).
- `.github/`: Copilot/automation guidance.
- `README.md`: All instructions, model notes, and troubleshooting (no separate quickstart file).

There are no Python projects, specs, or alternative setups left in the tree.

## Daily Workflow

### 1. Boot the Server
```powershell
cd ollama-portable
cmd /c start-ollama.bat
```
The batch file opens a new window, exports the Arc GPU environment variables, and launches `ollama serve`. Leave that window running while you work.

### 2. Run Models
Open a second terminal for interactive work.
```powershell
cd ollama-portable
.\ollama.exe run gemma3:12b
```

One-shot prompts:
```powershell
.\ollama.exe run gemma3:27b "Answer this math question"
```

Model management:
```powershell
.\ollama.exe pull gemma3:27b   # download Gemma 3 27B INT4
.\ollama.exe pull gpt-oss:20b  # download GPT-OSS INT4
.\ollama.exe list              # installed models
.\ollama.exe ps                # models currently loaded
```

### 3. Use the REST API
When the server is running you can post to `http://127.0.0.1:11434/api/generate`.
```powershell
$body = @{ model = "llama3.2:3b"; prompt = "Explain unified memory."; stream = $false } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/generate -Body $body -ContentType "application/json"
```

### 4. Tips & Troubleshooting
- First prompt after a reboot can take a few minutes because kernels compile on the Arc GPU; subsequent prompts are fast.
- Try `llama3.2:3b` for smoke tests, `gemma3:12b` for everyday chat, and `gpt-oss:20b` when you need a larger generalist while staying within the thermal budget.
- Watch Task Manager → Performance → GPU 0 to confirm the load sits on the Intel Arc 140V.
- Server window closed? Rerun `cmd /c start-ollama.bat`.
- Model missing? `ollama.exe pull <model>` and retry.
- Downloads slow? Temporarily set `$env:OLLAMA_MODEL_SOURCE = "modelscope"` before pulling.
- Verify status with `ollama.exe list` (installed) and `ollama.exe ps` (active).

## Recommended INT4 Models

| Model | Size | Typical Speed | Notes |
|-------|------|---------------|-------|
| llama3.2:3b | 2 GB | ~2 s/token burst | Smoke tests, small tools |
| gemma3:12b | ~8 GB | ~6 s first token | Default assistant, multilingual |
| gemma3:27b | ~16 GB | ~12 s first token | Largest model that still clears 15 tok/min |
| phi4 | 9.1 GB | ~8 s first token | Higher quality writing |
| gpt-oss:20b | ~13 GB | ~12 s first token | Open OSS generalist tuned for reasoning |

## Operation Notes
- The batch files export `OLLAMA_NUM_GPU=999`, `ZES_ENABLE_SYSMAN=1`, and other Level Zero toggles so every prompt runs on the Arc GPU.
- First prompt after a cold start compiles kernels and can take a few minutes; subsequent prompts are fast thanks to caching.
- Unified memory means you can load any INT4 model up to roughly 20 GB while keeping the desktop usable.

## Repository Layout
- `README.md` (this file)
- `ollama-portable/`
- `.github/` (automation/copilot guidance)

If you clone this repo, launch the server, and pull a model, you are fully set up. There is nothing else to configure.
