# Copilot Instructions for IPEX-LLM (Lunar Lake)

## Project Context
This repository now contains only the files required to run Intel's Ollama Portable bundle on the Samsung Galaxy Book5 Pro (Intel Lunar Lake Series 2, Arc 140V iGPU, 32 GB unified memory). There is no longer a parallel Python/IPEX code path—everything flows through the portable distribution in `ollama-portable/` plus this documentation.

## Guiding Principles
- **Ollama Portable only:** All automation, docs, and code changes should assume users operate directly inside `ollama-portable/`. Do not recreate conda envs, HuggingFace pipelines, or spec workflows.
- **XPU-only inference:** Ensure every instruction keeps `OLLAMA_NUM_GPU=999` and related Level Zero toggles intact so prompts always execute on the Arc 140V.
- **INT4 first:** Recommend INT4 GGUF models sized to stay within the 32 GB unified memory budget (typical sweet spot 3B–32B params).
- **Minimal footprint:** Avoid reintroducing deleted specs, scripts, or doc trees. Any new files should justify their existence for the portable flow.

## Repository Layout
- `ollama-portable/` – Intel's prebuilt binaries, runtime DLLs, `start-ollama.bat`, and `ollama-serve.bat`.
- `README.md` – Single source of truth for workflow, tips, troubleshooting, and model suggestions.
- `.github/` – This instruction file plus GitHub metadata. No Speckit agents or prompts remain.

## Daily Workflow (mirrors README)
1. **Boot server**
    ```powershell
    cd ollama-portable
    cmd /c start-ollama.bat
    ```
    Leave the spawned window open; it exports GPU env vars and runs `ollama serve` on `127.0.0.1:11434`.

2. **Run models** from another terminal
    ```powershell
    cd ollama-portable
    .\ollama.exe run gemma3:12b
    .\ollama.exe pull gemma3:27b
    .\ollama.exe pull gpt-oss:20b
    .\ollama.exe list
    .\ollama.exe ps
    ```
    For one-shot prompts: `.\ollama.exe run gemma3:27b "Answer this math question"`.

3. **Use the REST API** when automation/testing is needed:
    ```powershell
    $body = @{ model = "llama3.2:3b"; prompt = "Explain unified memory."; stream = $false } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/generate -Body $body -ContentType "application/json"
    ```

## Recommended Models (INT4 GGUF)
- `llama3.2:3b` – Fast smoke tests (~2 s first token)
- `gemma3:12b` – Default assistant (~6 s first token)
- `gemma3:27b` – Largest model that still clears 15 tok/min (~12 s first token)
- `phi4` – Higher quality writing (~8 s first token)
- `gpt-oss:20b` – Open OSS generalist tuned for reasoning (~12 s first token)

## Environment Variables (already handled in batch files)
- `OLLAMA_NUM_GPU=999` – Force iGPU for all layers
- `ZES_ENABLE_SYSMAN=1` – Enable Arc telemetry
- `OLLAMA_NUM_PARALLEL=2`, `OLLAMA_KEEP_ALIVE=10m`, `OLLAMA_HOST=127.0.0.1:11434`

## Troubleshooting Reminders
- **Server window closed:** rerun `cmd /c start-ollama.bat`.
- **Model missing:** `ollama.exe pull <model>` then retry.
- **Slow downloads:** set `$env:OLLAMA_MODEL_SOURCE = "modelscope"` temporarily.
- **Check load:** Task Manager → Performance → GPU 0 should show activity during inference.

## Expectations for Future Changes
- Keep docs and code aligned with the portable-only scope.
- If automation is needed (tests, scripts, CI), operate directly on the files inside `ollama-portable/` or wrap existing batch files—do **not** replicate their logic elsewhere.
- When adding examples or snippets, default to PowerShell commands or REST examples that call the bundled `ollama.exe`.

These instructions should be updated whenever the portable workflow changes (e.g., new env vars, different batch entrypoints, or additional supported models).
