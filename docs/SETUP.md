# IPEX-LLM Setup for Intel Arc 140V (Lunar Lake)

## Recommended Approach: Ollama Portable Zip

The easiest way to run LLMs on Intel Arc 140V is using Intel's pre-configured Ollama Portable Zip. This avoids all runtime dependency issues.

### Quick Start

1. **Run the setup script:**
   ```powershell
   .\scripts\setup-ollama-portable.ps1
   ```

2. **Start the Ollama server:**
   ```powershell
   .\scripts\start-ollama-server.ps1
   ```

3. **In a new terminal, run a model:**
   ```powershell
   cd ollama-portable
   .\ollama.exe run deepseek-r1:7b
   ```

### What Gets Installed

- **Ollama Portable**: ~500MB download with all Intel GPU optimizations
- **IPEX-LLM Runtime**: Pre-configured Intel Extension for PyTorch
- **OneAPI Libraries**: All required Intel runtime DLLs bundled
- **No Python needed**: Runs standalone C++ binary

### Advantages

✅ **Zero dependency management** - Everything is pre-configured  
✅ **Works out-of-the-box** - No conda/pip/runtime version conflicts  
✅ **INT4 optimized** - Maximum speed on 32GB unified memory  
✅ **Standard Ollama API** - Compatible with all Ollama tools  
✅ **Verified on Lunar Lake** - Tested on Core Ultra Series 2

### Model Recommendations for 32GB System

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| `llama3.2:3b` | 2GB | ⚡ Very Fast | Quick tasks, coding assistance |
| `qwen2.5:7b` | 4.5GB | ⚡ Fast | General purpose, balanced |
| `deepseek-r1:7b` | 4.7GB | ⚡ Fast | Reasoning, problem solving |
| `phi4` | 8.5GB | 🔥 Medium | High quality responses |
| `qwen2.5:14b` | 9GB | 🔥 Medium | Advanced tasks |
| `deepseek-r1:14b` | 9.4GB | 🔥 Medium | Complex reasoning |
| `qwen3:30b` | 19GB | 🐢 Slow | Maximum capability (fits in 32GB!) |

### Environment Variables

The portable zip sets these automatically:
- `OLLAMA_NUM_GPU=999` - Force GPU usage
- `SYCL_CACHE_PERSISTENT=1` - Cache compiled kernels
- Runtime paths configured for Intel libraries

### Troubleshooting

**First run is slow?**
- Normal - GPU kernels compile on first use (~2-5 minutes)
- Subsequent runs are much faster
- Compilation cache persists across sessions

**Model download slow?**
```powershell
# Use ModelScope mirror (faster in some regions)
set OLLAMA_MODEL_SOURCE=modelscope
.\ollama.exe run deepseek-r1:7b
```

**Want to use multiple GPUs?**
```powershell
# Select specific GPU (if you have multiple)
set ONEAPI_DEVICE_SELECTOR=level_zero:0
.\scripts\start-ollama-server.ps1
```

---

## Alternative: Python/HuggingFace Setup (Advanced)

If you need Python integration for custom code, see [PYTHON_SETUP.md](PYTHON_SETUP.md).

⚠️ **Warning**: The Python setup has complex runtime dependency requirements and is not recommended unless you specifically need programmatic access to models.

The Python approach we attempted encountered:
- Runtime version mismatches (conda 2023.1 vs pip 2024.0.x)
- Missing DLL dependencies (sycl.dll, libuv, etc.)
- ABI compatibility issues between IPEX and Intel runtimes

**Ollama Portable avoids all these issues.**
