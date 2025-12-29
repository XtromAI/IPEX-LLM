# Ollama Command Line Reference

Complete reference for Ollama CLI commands on Intel Arc 140V with IPEX-LLM.

## Server Management

### Start Server
```powershell
# Using the automation script (recommended)
.\start-ollama-server.ps1

# Manual start
ollama serve
```

### Check Server Status
```powershell
# Server is running if this returns model info
ollama list

# Check running processes
Get-Process | Where-Object { $_.ProcessName -like '*ollama*' }
```

### Stop Server
Press `Ctrl+C` in the terminal where `start-ollama-server.ps1` is running, or use a command:
```powershell
Press `Ctrl+C` in the terminal where `start-ollama-server.ps1` is running to gracefully stop the server.

# If you need to automate or force stop:
Stop-Process -Name "ollama" -Force
```

## Model Management

### Pull (Download) Models
```powershell
ollama pull <model>                    # Download latest version
ollama pull llama3.2:3b               # Specific model
ollama pull gemma3:12b                # Tested working model
ollama pull phi4                      # Another tested model
```

### List Models
```powershell
ollama list                           # Show all installed models
```
Output shows: NAME, ID, SIZE, MODIFIED

### Show Model Details
```powershell
ollama show <model>                   # Display model information
ollama show gemma3:12b                # Show Gemma 3 12B details
ollama show phi4 --modelfile          # Show Modelfile configuration
```

### Delete Models
```powershell
ollama rm <model>                     # Remove a model
ollama rm gemma3:27b                  # Example: remove 27B model
```

### Copy Models
```powershell
ollama cp <source> <destination>      # Create a copy of a model
ollama cp gemma3:12b my-gemma         # Example: copy with new name
```

## Running Models

### Interactive Chat
```powershell
ollama run <model>                    # Start interactive session
ollama run gemma3:12b                 # Chat with Gemma 3 12B
ollama run phi4                       # Chat with Phi-4

# Exit interactive mode
/bye                                  # or Ctrl+D
```

### One-Shot Prompts
```powershell
ollama run <model> "prompt text"
ollama run phi4 "Explain quantum computing"
ollama run gemma3:12b "Write a Python function to sort a list"
```

### Multiline Prompts
```powershell
ollama run gemma3:12b "This is line 1
This is line 2
This is line 3"

# Or use heredoc syntax in PowerShell
@"
Explain the following:
1. Unified memory
2. SYCL runtime
3. INT4 quantization
"@ | ollama run phi4
```

### With Options
```powershell
# Set temperature (creativity)
ollama run gemma3:12b --temperature 0.8 "Write a creative story"

# Set context window
ollama run phi4 --context 8192 "Long conversation"

# Verbose mode
ollama run llama3.2:3b --verbose "Test prompt"
```

## Process Management

### Check Running Models
```powershell
ollama ps                             # Show currently loaded models
```
Output shows: NAME, ID, SIZE, PROCESSOR, UNTIL

### Stop (Unload) a Model
```powershell
ollama stop <model>                   # Unload model from memory
ollama stop gemma3:12b                # Free up memory
```

## Creating Custom Models

### Create from Modelfile
```powershell
ollama create <name> -f <Modelfile>   # Create custom model
ollama create my-assistant -f ./Modelfile
```

Example Modelfile:
```
FROM gemma3:12b
SYSTEM "You are a helpful coding assistant specialized in Python."
PARAMETER temperature 0.7
PARAMETER top_p 0.9
```

### Push to Registry (if configured)
```powershell
ollama push <model>                   # Upload model to registry
```

## REST API Usage

### Generate Completion
```powershell
# Non-streaming
$body = @{
    model = "gemma3:12b"
    prompt = "Explain AI"
    stream = $false
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/generate -Body $body -ContentType "application/json"

# Streaming
$body = @{
    model = "phi4"
    prompt = "Write a story"
    stream = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/generate -Body $body -ContentType "application/json"
```

### Chat Completion
```powershell
$body = @{
    model = "gemma3:12b"
    messages = @(
        @{ role = "system"; content = "You are a helpful assistant." }
        @{ role = "user"; content = "What is unified memory?" }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/chat -Body $body -ContentType "application/json"
```

### List Models (API)
```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:11434/api/tags
```

### Show Model Info (API)
```powershell
$body = @{ name = "gemma3:12b" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:11434/api/show -Body $body -ContentType "application/json"
```

### Check Running Models (API)
```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:11434/api/ps
```

## Environment Variables

Set these before starting the server (already configured in `start-ollama-server.ps1`):

```powershell
# Force all layers to GPU
$env:OLLAMA_NUM_GPU = "999"

# Enable Intel GPU telemetry
$env:ZES_ENABLE_SYSMAN = "1"

# SYCL optimization
$env:SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS = "1"

# Server host/port
$env:OLLAMA_HOST = "127.0.0.1:11434"

# Model storage location
$env:OLLAMA_MODELS = "C:\Users\<username>\.ollama\models"

# Keep models in memory for 10 minutes after last use
$env:OLLAMA_KEEP_ALIVE = "10m"

# Number of parallel requests
$env:OLLAMA_NUM_PARALLEL = "2"

# Context length
$env:OLLAMA_CONTEXT_LENGTH = "4096"

# Debug logging
$env:OLLAMA_DEBUG = "INFO"
```

## Interactive Mode Commands

When inside `ollama run <model>`:

```
/bye                # Exit chat session
/clear              # Clear conversation history
/set parameter      # Set a parameter (e.g., /set temperature 0.8)
/show               # Show model information
/load <model>       # Load a different model
/?                  # Show help
```

## Version & Help

```powershell
ollama --version                      # Show Ollama version
ollama --help                         # Show help
ollama <command> --help               # Help for specific command
```

## Troubleshooting Commands

### Check System Info
```powershell
# Verify Ollama version
ollama --version

# Check if server is responding
ollama list

# View server logs (if running in foreground)
# Logs appear in the terminal running start-ollama-server.ps1
```

### Memory and Performance
```powershell
# Check GPU usage in Task Manager
# Performance → GPU 0 (Intel Arc 140V)

# Check loaded models and memory usage
ollama ps

# Free memory by stopping models
ollama stop gemma3:12b
```

### Clear Model Cache
```powershell
# Stop all running models
ollama ps | ForEach-Object { ollama stop $_.Name }

# Remove downloaded models
ollama rm <model>

# Full reset: delete model directory
Remove-Item -Recurse -Force "$env:USERPROFILE\.ollama"
```

## Model Search & Discovery

Browse models at: https://ollama.com/library

Search by category:
- **Code:** codellama, deepseek-coder, starcoder
- **Chat:** llama3.2, gemma3, phi4
- **Vision:** llava, bakllava
- **Specialized:** mistral, mixtral, qwen

## Performance Tips

1. **First run is slow:** Kernel compilation can take minutes on first prompt
2. **Use appropriate model sizes:** Stick to ≤12B parameters (≤10 GB) for 18 GB memory
3. **Monitor GPU usage:** Task Manager → GPU 0 should show activity
4. **Stop unused models:** Run `ollama stop <model>` to free memory
5. **Keep server running:** Avoid restarting to preserve kernel cache
6. **Use streaming:** For long responses, use `stream=true` in API calls

## Common Workflows

### Quick Test
```powershell
ollama run llama3.2:3b "Test prompt"
```

### Development Session
```powershell
# Terminal 1: Start server
.\start-ollama-server.ps1

# Terminal 2: Interactive work
ollama run gemma3:12b
```

### Batch Processing
```powershell
$prompts = @("Prompt 1", "Prompt 2", "Prompt 3")
foreach ($prompt in $prompts) {
    ollama run phi4 $prompt > "output_$($prompts.IndexOf($prompt)).txt"
}
```

### Model Comparison
```powershell
$prompt = "Explain quantum computing in simple terms"
ollama run llama3.2:3b $prompt > llama_response.txt
ollama run gemma3:12b $prompt > gemma_response.txt
ollama run phi4 $prompt > phi_response.txt
```

## Additional Resources

- Official Ollama Docs: https://github.com/ollama/ollama/tree/main/docs
- Model Library: https://ollama.com/library
- API Reference: https://github.com/ollama/ollama/blob/main/docs/api.md
- Modelfile Reference: https://github.com/ollama/ollama/blob/main/docs/modelfile.md
