# Copilot Instructions for IPEX-LLM (Lunar Lake)

## Project Context
This project builds a high-performance local inference environment for **Intel Lunar Lake (Series 2)** architecture, specifically targeting the **Samsung Galaxy Book5 Pro** with **Intel Arc 140V iGPU** and **32GB LPDDR5X unified memory**.

## Architecture Overview

### Primary Approach: Ollama Portable (Recommended)
- **Method:** Pre-built Intel Ollama binaries with bundled IPEX-LLM optimizations
- **Location:** `ollama-portable/` directory
- **Advantages:** Zero dependency management, stable, officially supported
- **Use Cases:** Inference, chat applications, REST API integration
- **Model Format:** GGUF quantized models (INT4/INT8/FP16)

### Secondary Approach: Python/IPEX-LLM (Advanced)
- **Method:** Direct HuggingFace Transformers with IPEX-LLM extensions
- **Environment:** Conda environment with Intel runtime libraries
- **Status:** ⚠️ Complex setup due to Intel runtime ABI dependencies
- **Use Cases:** Custom training, fine-tuning, research workflows
- **When to Use:** Only when Ollama's capabilities are insufficient

## Core Principles
- **XPU-First:** All inference MUST utilize the Arc 140V iGPU. Do NOT use CPU-only modes.
- **Memory Efficiency:** Default to **INT4** quantization. Target 27B-32B parameter models within 32GB unified memory.
- **Simplicity:** Prefer Ollama Portable over Python unless programmatic model access is strictly required.

## Coding Conventions

### Ollama API Integration (Primary)
For building applications that use the inference engine:
```python
import requests

# Ollama REST API
response = requests.post('http://127.0.0.1:11434/api/generate', json={
    'model': 'llama3.2:3b',
    'prompt': 'Your prompt here',
    'stream': False
})
result = response.json()
```

Using official Python client:
```python
import ollama

response = ollama.generate(model='llama3.2:3b', prompt='Your prompt')
print(response['response'])
```

### Python/IPEX-LLM (Advanced Use Only)
If direct transformer access is required:
```python
import torch
import intel_extension_for_pytorch as ipex
from ipex_llm.transformers import AutoModelForCausalLM

# Load with INT4 quantization
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    load_in_4bit=True,
    trust_remote_code=True,
    use_cache=True
)
model = model.to('xpu')

# Inference with XPU tensors
input_ids = tokenizer.encode(prompt, return_tensors="pt").to('xpu')
output = model.generate(input_ids, max_new_tokens=512)
```

**Note:** Python approach requires resolving Intel OneAPI runtime dependencies. See `docs/SETUP.md` for details.

## Environment Configuration

### Ollama Server (Auto-Configured)
Environment variables set by `ollama-serve.bat`:
- `OLLAMA_NUM_GPU=999` - Force GPU usage (all layers on iGPU)
- `ZES_ENABLE_SYSMAN=1` - Enable Intel GPU system management
- `OLLAMA_NUM_PARALLEL=2` - Handle 2 concurrent requests
- `OLLAMA_KEEP_ALIVE=10m` - Keep models loaded for 10 minutes
- `OLLAMA_HOST=127.0.0.1:11434` - Local server binding

### Python Environment (If Used)
- `SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1` - Potential performance boost
- `ONEAPI_DEVICE_SELECTOR=level_zero:0` - Target Arc 140V specifically

## Architecture & Hardware
- **Target Device:** Intel Arc 140V iGPU (Xe2-LPG architecture)
- **Compute Interface:** SYCL/Level Zero via Intel Extension for PyTorch
- **NPU Status:** Not utilized in current builds; reserved for future power-efficiency experiments
- **Unified Memory:** 32GB LPDDR5X shared between CPU and GPU (zero-copy advantage)
- **Quantization:** INT4 primary, FP8/INT8 alternatives, FP16 for quality-critical tasks

## Model Recommendations

| Model | Size | Parameters | Speed | Best For |
|-------|------|------------|-------|----------|
| llama3.2:3b | 2GB | 3B | ~2s | Quick tasks, testing |
| qwen2.5:7b | 4.7GB | 7B | ~4s | General purpose |
| deepseek-r1:7b | 4.7GB | 7B | ~4s | Reasoning, math |
| phi4 | 9.1GB | 14B | ~8s | High quality output |
| qwen2.5:32b | 19GB | 32B | ~15s | Max capability (fits in 32GB) |

All sizes assume INT4 quantization. Speed estimates based on Arc 140V.

## Daily Workflow

### Starting Ollama Server
```powershell
cd C:\Users\creks\Documents\IPEX-LLM\ollama-portable
cmd /c start-ollama.bat  # Opens new window, keep it running
```

### Running Inference
```powershell
# Interactive mode
.\ollama.exe run llama3.2:3b

# One-shot query
.\ollama.exe run llama3.2:3b "Your prompt here"

# Pull new models
.\ollama.exe pull qwen2.5:7b
```

### Checking Status
```powershell
.\ollama.exe list  # Show downloaded models
.\ollama.exe ps    # Show running models in memory
```

## Performance Expectations
- **First Run:** 2-5 minutes (GPU kernel compilation, one-time)
- **Subsequent Runs:** Near-instant model loading from cache
- **Inference Speed:** ~2s for 3B models, ~15s for 32B models
- **GPU Utilization:** Check Task Manager → Performance → GPU 0 → 3D usage

## Documentation
- **DevLog:** `docs/devlog/2025-12-26_Ollama_Portable_Setup.md` - Implementation details
- **Quick Start:** `QUICKSTART.md` - Daily usage commands
- **Setup Guide:** `docs/SETUP.md` - Comprehensive installation and troubleshooting
- **Architecture Decisions:** `docs/devlog/2025-12-26_Constitution_and_Architecture.md` - Original design

## Troubleshooting

### Server Not Responding
```powershell
# Check if running
Get-Process ollama -ErrorAction SilentlyContinue

# Restart: Close CMD window and re-run start-ollama.bat
```

### Slow Downloads
```powershell
# Use ModelScope mirror (faster in some regions)
$env:OLLAMA_MODEL_SOURCE = "modelscope"
.\ollama.exe pull <model>
```

### Python Approach Issues
If attempting Python/IPEX-LLM:
- See `docs/SETUP.md` section "Alternative: Python/HuggingFace Setup"
- ⚠️ Requires Intel OneAPI runtime libraries with matching ABIs
- Conda/pip version conflicts are common; Ollama Portable avoids these entirely
