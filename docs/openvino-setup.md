# OpenVINO GenAI Setup Guide

## ✅ Setup Status: COMPLETE (December 28, 2025)

Successfully migrated from IPEX-LLM (8 months old) to OpenVINO GenAI (2 weeks old). System verified working on Intel Arc 140V iGPU with TinyLlama-1.1B-Chat achieving ~70 words/s generation speed.

**Environment:** `openvino-genai` conda environment  
**Version:** OpenVINO GenAI 2025.4.1.0-2683  
**GPU Detection:** ✓ (CPU, GPU, NPU all available)  
**Test Model:** TinyLlama-1.1B-Chat-v1.0 (INT4, ~1.3 GB)  
**Performance:** 7.35s load time, 0.95s generation (67 words), ~70 words/s

## Overview
OpenVINO GenAI is Intel's official toolkit for running LLM inference on Intel hardware including your Arc 140V iGPU. It's actively maintained with the latest release (2025.4.1.0) from December 2025.

## Key Advantages Over IPEX-LLM
- **Active development**: Latest release 2 weeks old (vs 8 months for IPEX-LLM)
- **Direct Intel Arc GPU support**: Uses Level Zero backend natively
- **Simple API**: Similar ease-of-use to Ollama
- **INT4/INT8 quantization**: Built-in weight compression support
- **No Ollama dependency**: Direct Python/C++ inference API

## Installation

### Setup Completed on December 28, 2025

**Commands executed:**
```powershell
# 1. Created environment
conda create -n openvino-genai python=3.11 -y
conda activate openvino-genai

# 2. Installed packages
pip install openvino-genai optimum-intel
pip install nncf  # Required for INT4 quantization

# 3. Verified installation
python -c "import openvino_genai as ov_genai; print(f'OpenVINO GenAI version: {ov_genai.__version__}')"
# Output: OpenVINO GenAI version: 2025.4.1.0-2683-fc593653d77

# 4. Checked GPU detection
python -c "from openvino import Core; devices = Core().available_devices; print('Available devices:', devices)"
# Output: Available devices: ['CPU', 'GPU', 'NPU']
```

**Results:**
- ✓ Environment created with Python 3.11
- ✓ OpenVINO GenAI 2025.4.1.0 installed
- ✓ Intel Arc 140V GPU detected and available
- ✓ All dependencies installed successfully

### Fresh Installation (For Reference)

### 1. Create New Conda Environment
```powershell
conda create -n openvino-genai python=3.11 -y
conda activate openvino-genai
```

### 2. Install OpenVINO GenAI
```powershell
pip install openvino-genai
pip install optimum-intel  # For model conversion from HuggingFace
```

### 3. Verify Installation
```powershell
python -c "import openvino_genai as ov_genai; print(ov_genai.__version__)"
```

## Model Preparation

### Completed: TinyLlama-1.1B-Chat-v1.0

**Commands executed:**
```powershell
conda activate openvino-genai
optimum-cli export openvino --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --weight-format int4 --trust-remote-code TinyLlama-1.1B-ov
```

**Results:**
- ✓ Model downloaded: 2.20 GB from HuggingFace
- ✓ Converted to OpenVINO IR format
- ✓ Quantized to INT4 (final size: ~1.3 GB)
- ✓ Ready for inference at `C:\Users\creks\Documents\IPEX-LLM\TinyLlama-1.1B-ov`

**Files created:**
```
TinyLlama-1.1B-ov/
├── openvino_model.bin      # Model weights
├── openvino_model.xml      # Model graph
├── openvino_tokenizer.bin  # Tokenizer
├── openvino_tokenizer.xml
├── openvino_detokenizer.bin
├── openvino_detokenizer.xml
├── config.json
├── generation_config.json
├── openvino_config.json
├── chat_template.jinja
└── tokenizer files...
```

### Option 1: Convert from HuggingFace (Recommended)
Export models directly to OpenVINO IR format with INT4 quantization:

```powershell
# Export with INT4 quantization (recommended for 18 GB memory)
optimum-cli export openvino --model meta-llama/Llama-3.2-3B-Instruct --weight-format int4 --trust-remote-code llama3.2-3b-ov

# Export Phi-4 (if available on HuggingFace)
optimum-cli export openvino --model microsoft/phi-4 --weight-format int4 --trust-remote-code phi4-ov

# Export Gemma 3 12B (may exceed memory - test first)
optimum-cli export openvino --model google/gemma-3-12b --weight-format int4 --trust-remote-code gemma3-12b-ov
```

### Option 2: Use Pre-converted Models
Browse OpenVINO-optimized models on HuggingFace:
- Search for models with "OpenVINO" in the name
- Example: `OpenVINO/Llama-3.2-3B-Instruct-int4-ov`

## Basic Usage

### Verified Working: Test Script

Created and tested [test_openvino.py](../test_openvino.py):

```python
import openvino_genai as ov_genai
import time

model_path = "TinyLlama-1.1B-ov"
pipe = ov_genai.LLMPipeline(model_path, "GPU")

prompt = "Explain the benefits of unified memory architecture in 3 sentences."
start = time.time()
response = pipe.generate(prompt, max_new_tokens=256)
elapsed = time.time() - start

print(f"Response: {response}")
print(f"Time: {elapsed:.2f}s (~{len(response.split())/elapsed:.1f} words/s)")
```

**Actual Results:**
```
Model loaded in 7.35s
Generation time: 0.95s
Words generated: 67
Speed: ~70.5 words/s

Response: Unified memory architecture offers several benefits, including:
1. Improved performance: Unified memory architecture allows multiple threads 
   to access the same memory simultaneously, resulting in improved performance.
2. Reduced latency: Unified memory architecture eliminates the need for 
   separate memory controllers, reducing latency and improving overall system 
   performance.
3. Faster data transfer: Unified memory architecture allows for faster data 
   transfer between memory and CPU, resulting in faster system performance.
```

### Interactive Chat

Created [chat_openvino.py](../chat_openvino.py) for conversational use:

```powershell
conda activate openvino-genai
python chat_openvino.py
```

Features:
- Multi-turn conversation with history
- Commands: `exit`/`quit` to end, `clear` to reset conversation
- Maintains last 6 exchanges to avoid context overflow

### REST API Server

Created [serve_openvino.py](../serve_openvino.py) to make models accessible to other applications:

```powershell
# Start server
conda activate openvino-genai
python serve_openvino.py

# Test from another terminal (PowerShell)
$body = @{
    model = "TinyLlama-1.1B-ov"
    prompt = "What is unified memory?"
    stream = $false
    max_new_tokens = 128
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/generate" -Body $body -ContentType "application/json"
Write-Host $response.response
```

**API Endpoints:**
- `GET /` - Health check
- `GET /api/tags` - List models
- `POST /api/generate` - Text generation
- `POST /api/chat` - Chat completion
- `GET /api/ps` - List running models

**Performance:** ~0.6s for simple prompts (64 tokens)

See [docs/api-server.md](api-server.md) for complete API documentation and integration examples.

### Python Script (Simple Chat)
```python
import openvino_genai as ov_genai

# Initialize pipeline with GPU device
pipe = ov_genai.LLMPipeline("llama3.2-3b-ov", "GPU")

# Generate text
response = pipe.generate("Explain unified memory architecture.", max_new_tokens=256)
print(response)
```

### Interactive Chat Loop
```python
import openvino_genai as ov_genai

pipe = ov_genai.LLMPipeline("llama3.2-3b-ov", "GPU")

print("OpenVINO Chat (type 'exit' to quit)")
while True:
    prompt = input("\nYou: ")
    if prompt.lower() == 'exit':
        break
    
    response = pipe.generate(prompt, max_new_tokens=512)
    print(f"\nAssistant: {response}")
```

### Advanced Configuration
```python
import openvino_genai as ov_genai

# Configure generation parameters
config = ov_genai.GenerationConfig()
config.max_new_tokens = 512
config.temperature = 0.7
config.top_p = 0.9
config.do_sample = True

pipe = ov_genai.LLMPipeline("llama3.2-3b-ov", "GPU")
response = pipe.generate("Your prompt here", config)
```

## Device Configuration

### Force GPU Usage
```python
pipe = ov_genai.LLMPipeline("model_path", "GPU")
```

### CPU Fallback
```python
pipe = ov_genai.LLMPipeline("model_path", "CPU")
```

### Auto Device Selection
```python
pipe = ov_genai.LLMPipeline("model_path", "AUTO")  # Automatically picks best device
```

## Environment Variables

Add to your PowerShell profile for optimal Arc GPU performance:

```powershell
# Level Zero optimizations (same as IPEX-LLM)
$env:ZES_ENABLE_SYSMAN = "1"
$env:SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS = "1"

# OpenVINO-specific
$env:OV_CACHE_DIR = "$env:USERPROFILE\.cache\openvino"
```

## Recommended Models for Arc 140V (18 GB available)

| Model | Size (INT4) | Speed | Use Case |
|-------|-------------|-------|----------|
| Llama 3.2 3B | ~2 GB | Very Fast | Quick tests, simple queries |
| Phi-3.5 Mini (3.8B) | ~2.5 GB | Very Fast | Reasoning, coding |
| Mistral 7B | ~4 GB | Fast | General purpose |
| Llama 3.1 8B | ~5 GB | Fast | General purpose, instruction following |
| Gemma 2 9B | ~6 GB | Medium | High quality responses |
| Qwen 2.5 14B | ~9 GB | Medium | Technical/multilingual |

**Avoid:** Models >14B parameters (will exceed 18 GB memory limit)

## Performance Comparison Script

```python
import openvino_genai as ov_genai
import time

model_path = "llama3.2-3b-ov"
prompt = "Explain the benefits of unified memory in 3 sentences."

pipe = ov_genai.LLMPipeline(model_path, "GPU")

# Warm-up
pipe.generate("test", max_new_tokens=10)

# Benchmark
start = time.time()
response = pipe.generate(prompt, max_new_tokens=256)
elapsed = time.time() - start

print(f"Response: {response}\n")
print(f"Time: {elapsed:.2f}s")
print(f"Tokens: ~{len(response.split())}")
print(f"Speed: ~{len(response.split())/elapsed:.1f} tokens/s")
```

## Troubleshooting

### GPU Not Detected
```powershell
# Check available devices
python -c "from openvino import Core; print(Core().available_devices)"
```

Expected output should include `GPU` or `GPU.0`

### Out of Memory
- Use smaller models (≤14B parameters)
- Ensure no other GPU-intensive applications are running
- Try INT4 quantization if using INT8

### Slow First Inference
- Normal behavior - model compilation and caching
- Subsequent runs will be much faster
- Models cached in `%USERPROFILE%\.cache\openvino`

## Migration from IPEX-LLM/Ollama

### Key Differences

| Feature | IPEX-LLM + Ollama | OpenVINO GenAI |
|---------|-------------------|----------------|
| Installation | Conda + symlinks | Simple pip install |
| Model format | GGUF | OpenVINO IR |
| API style | REST + CLI | Python/C++ API |
| Server mode | Built-in (ollama serve) | Requires custom wrapper |
| Model management | `ollama pull/list` | Manual directory management |
| Arc GPU support | Via IPEX-LLM | Native Level Zero |
| Update frequency | 8 months old (Apr 2025) | 2 weeks old (Dec 2025) |
| Latest version | v2.2.0 | v2025.4.1.0 |

### Performance Comparison

**TinyLlama-1.1B-Chat:**
- OpenVINO GenAI: ~70 words/s (verified)
- IPEX-LLM: Not tested with this model

**Similar size models (Llama 3.2 3B):**
- IPEX-LLM: ~2s first token (from project notes)
- OpenVINO GenAI: Expected similar or better (pending test)

### Workflow Changes

**IPEX-LLM (Old):**
```powershell
# Terminal 1
.\start-ollama-server.ps1

# Terminal 2
ollama run gemma3:12b
```

**OpenVINO (New):**
```powershell
# Single terminal - direct execution
conda activate openvino-genai
python chat_openvino.py  # Interactive chat
python test_openvino.py  # Quick test
```

### Why We Migrated

1. **Stale releases**: IPEX-LLM last released April 2025 (8 months ago)
2. **Ollama version lock**: Stuck on Ollama v0.9.3, missing features from v0.13.5
3. **Active development**: OpenVINO GenAI updated every 2 weeks
4. **Official Intel support**: Direct from OpenVINO team
5. **Better documentation**: Comprehensive guides and examples

## Next Steps

### Immediate Actions

1. ✅ **Test installation**: Completed with TinyLlama-1.1B-Chat
2. ⏭️ **Convert larger models**: Llama 3.2 3B, Phi-4, Mistral 7B for better quality
3. ⏭️ **Benchmark performance**: Compare directly with IPEX-LLM's gemma3:12b
4. ⏭️ **Build a simple CLI**: Enhance chat_openvino.py with better formatting

### Recommended Next Models to Convert

```powershell
conda activate openvino-genai

# Llama 3.2 3B (2 GB, very fast)
optimum-cli export openvino --model meta-llama/Llama-3.2-3B-Instruct --weight-format int4 --trust-remote-code llama3.2-3b-ov

# Phi-3.5 Mini (2.5 GB, excellent for coding)
optimum-cli export openvino --model microsoft/Phi-3.5-mini-instruct --weight-format int4 --trust-remote-code phi3.5-mini-ov

# Mistral 7B (4 GB, general purpose)
optimum-cli export openvino --model mistralai/Mistral-7B-Instruct-v0.3 --weight-format int4 --trust-remote-code mistral-7b-ov

# Gemma 2 9B (6 GB, high quality)
optimum-cli export openvino --model google/gemma-2-9b-it --weight-format int4 --trust-remote-code gemma2-9b-ov
```

### Future Enhancements

- **REST API wrapper**: Create FastAPI server for Ollama-like REST interface
- **Model management CLI**: Build tool to list/switch/delete converted models
- **Automatic benchmarking**: Script to compare all models on standard prompts
- **Visual Language Models**: Test LLaVA or MiniCPM-V for image understanding

## Resources

- **Official Docs**: https://openvinotoolkit.github.io/openvino.genai/
- **GitHub Repo**: https://github.com/openvinotoolkit/openvino.genai
- **Model Zoo**: https://huggingface.co/models?other=openvino
- **Optimum Intel**: https://huggingface.co/docs/optimum/intel/openvino/export

## Notes

- OpenVINO GenAI does not include a built-in server like Ollama - you'll need to write Python scripts for inference
- Model conversion from HuggingFace is straightforward and takes only a few minutes per model
- Performance should be comparable or better than IPEX-LLM due to newer optimizations
- The API is more "low-level" than Ollama but offers more control and flexibility
