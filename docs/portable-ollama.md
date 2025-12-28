# Intel Ollama Portable Documentation

This documentation covers the usage, updates, and configuration of the Intel Ollama Portable bundle optimized for Intel GPUs (Lunar Lake, Arc, etc.) using `ipex-llm`.

## Overview
The Ollama Portable bundle is a pre-packaged distribution of Ollama that includes all necessary Intel oneAPI and IPEX-LLM dependencies. It allows you to run LLMs on Intel iGPUs and dGPUs without a complex manual installation process.

## Getting the Latest Release
The portable bundle is maintained as part of the `ipex-llm` project.

- **Release Page:** [Intel IPEX-LLM Releases](https://github.com/intel-analytics/ipex-llm/releases)
- **Latest Nightly (Recommended):** [v2.3.0-nightly](https://github.com/ipex-llm/ipex-llm/releases/tag/v2.3.0-nightly)
- **Download File:** Look for `ollama-portable-windows-v2.3.0bXXXXXXXX.zip`.

## How to Update
To update your local installation:
1. Download the latest `.zip` from the release page above.
2. Close any running Ollama server windows.
3. Extract the contents of the new zip file.
4. Copy and replace all files in your local `ollama-portable/` directory with the new ones.
5. Your downloaded models (stored in `%USERPROFILE%\.ollama`) will persist across updates.

## Key Configuration (Environment Variables)
These variables are typically handled by `start-ollama.bat`, but can be customized:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_NUM_GPU` | `999` | Forces all model layers onto the Intel GPU. |
| `ZES_ENABLE_SYSMAN` | `1` | Enables Intel Arc telemetry and system management. |
| `OLLAMA_MODEL_SOURCE` | `ollama` | Set to `modelscope` for faster downloads in some regions. |
| `OLLAMA_NUM_CTX` | `2048` | Sets the context window size (e.g., `8192`, `16384`). |
| `OLLAMA_NUM_PARALLEL` | `4` | Set to `1` to save VRAM on memory-constrained systems. |
| `ONEAPI_DEVICE_SELECTOR` | `level_zero:0` | Selects which GPU to use if multiple are present. |
| `SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS` | `1` | Performance tuning for Level Zero task submission. |

## Troubleshooting
- **SYCL Error / Weight Copy Failure:** Ensure `start-ollama.bat` is running in a separate window. If errors persist, restart the server window to reinitialize the Level Zero driver.
- **Model Not Found:** Run `.\ollama.exe list` to see available models. Use `.\ollama.exe pull <model>` to download new ones.
- **Slow Performance:** Ensure your Intel GPU drivers are up to date ([Intel Arc Graphics Driver](https://www.intel.com/content/www/us/en/download/785597/intel-arc-iris-xe-graphics-windows.html)).
