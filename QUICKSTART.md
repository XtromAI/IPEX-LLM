# IPEX-LLM Quick Start Guide

## Successfully Installed! ✓

Your Intel Arc 140V GPU-accelerated LLM environment is ready.

## What Just Happened

1. **Downloaded** Intel's pre-built Ollama (108MB) with IPEX-LLM optimizations
2. **Extracted** to `ollama-portable/` with all Intel runtime DLLs (sycl8.dll, dnnl.dll, etc.)
3. **Started** Ollama server with Arc GPU environment variables
4. **Pulled** Llama 3.2 3B model (2GB)
5. **Tested** successfully - generating responses in ~2 seconds

## Daily Usage

### Start Server (Keep Running)
```powershell
cd C:\Users\creks\Documents\IPEX-LLM\ollama-portable
cmd /c start-ollama.bat
```
This opens a new window. Keep it open while using models.

### Run Models (New Terminal)
```powershell
cd C:\Users\creks\Documents\IPEX-LLM\ollama-portable
.\ollama.exe run llama3.2:3b
```

Or use one-shot queries:
```powershell
.\ollama.exe run llama3.2:3b "Your question here"
```

### Available Models

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| **llama3.2:3b** | 2GB | Fast | Quick tasks, testing |
| **qwen2.5:7b** | 4.7GB | Medium | General purpose |
| **deepseek-r1:7b** | 4.7GB | Medium | Reasoning tasks |
| **phi4** | 9.1GB | Slower | High quality output |

Pull new models with:
```powershell
.\ollama.exe pull qwen2.5:7b
```

## Tips

- **First Run**: Takes 2-5 minutes for GPU kernel compilation (one-time)
- **Subsequent Runs**: Near-instant startup
- **Memory**: 32GB RAM allows running up to 30B models with INT4 quantization
- **Check GPU Usage**: Open Task Manager → Performance → GPU 0 while running inference

## Troubleshooting

### Server Not Responding
```powershell
# Check if server is running
Get-Process ollama -ErrorAction SilentlyContinue

# Restart server: Close the CMD window and run start-ollama.bat again
```

### Slow Downloads
Add this to your PowerShell profile or before pulling models:
```powershell
$env:OLLAMA_MODEL_SOURCE = "modelscope"
```

### Verify Installation
```powershell
cd ollama-portable
.\ollama.exe list  # Should show downloaded models
.\ollama.exe ps    # Should show running models
```

## Environment Variables (Already Set)

The `ollama-serve.bat` configures:
- `OLLAMA_NUM_GPU=999` - Force GPU usage
- `ZES_ENABLE_SYSMAN=1` - Enable GPU monitoring
- `OLLAMA_NUM_PARALLEL=2` - Handle 2 concurrent requests
- `OLLAMA_KEEP_ALIVE=10m` - Keep models loaded for 10 minutes

## Next Steps

1. **Try Different Models**: Experiment with `qwen2.5:7b` or `phi4`
2. **Build Applications**: Ollama has REST API at `http://127.0.0.1:11434`
3. **Monitor Performance**: Use Intel Arc Control app to check GPU utilization
4. **Scale Up**: Try larger models like `qwen2.5:14b` (fits in 32GB RAM)

## Python/HuggingFace (Alternative)

If you need direct Python access to IPEX-LLM transformers, see [SETUP.md](docs/SETUP.md) for the conda environment approach. Note: This requires resolving Intel runtime dependencies and is more complex than Ollama.
