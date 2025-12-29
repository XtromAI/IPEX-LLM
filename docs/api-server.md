# OpenVINO GenAI REST API Server

## Overview

REST API server that makes OpenVINO GenAI models accessible to other applications on your computer via HTTP requests. Compatible with Ollama API endpoints.

**Status:** ✅ Working on Intel Arc 140V  
**Port:** 8000 (to avoid conflict with IPEX-LLM on 11434)  
**Performance:** ~0.6s generation for simple prompts  

## Quick Start

### Start the Server

**Terminal 1 (Server):**
```powershell
conda activate openvino-genai
python serve_openvino.py
```

Expected output:
```
============================================================
OpenVINO GenAI Server
============================================================
Loading model: TinyLlama-1.1B-ov
Device: GPU (Intel Arc 140V)
Model loaded in 2.02s

✓ Server ready at http://127.0.0.1:8000
============================================================
```

### Test from Another Application

**Terminal 2 (Client):**
```powershell
# Quick test
$body = @{
    model = "TinyLlama-1.1B-ov"
    prompt = "Explain unified memory in one sentence."
    stream = $false
    max_new_tokens = 64
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/generate" -Body $body -ContentType "application/json"

Write-Host "Response:" $response.response
```

**Result:**
```
Response: Unified memory is a memory architecture that allows multiple threads to 
access the same memory simultaneously, reducing the overhead of synchronization and 
improving performance.

Generation time: 0.62 seconds
```

## API Endpoints

### 1. Health Check
```http
GET http://127.0.0.1:8000/
```

**Response:**
```json
{
  "status": "ok",
  "model": "TinyLlama-1.1B-ov",
  "message": "OpenVINO GenAI Server is running"
}
```

### 2. List Models
```http
GET http://127.0.0.1:8000/api/tags
```

**Response:**
```json
{
  "models": [
    {
      "name": "TinyLlama-1.1B-ov",
      "model": "TinyLlama-1.1B-ov",
      "modified_at": "2025-12-28T00:00:00Z",
      "size": 0,
      "digest": "openvino-genai",
      "details": {
        "format": "openvino",
        "family": "llama",
        "quantization_level": "int4"
      }
    }
  ]
}
```

### 3. Generate Text
```http
POST http://127.0.0.1:8000/api/generate
```

**Request Body:**
```json
{
  "model": "TinyLlama-1.1B-ov",
  "prompt": "What is artificial intelligence?",
  "stream": false,
  "max_new_tokens": 256,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**Response:**
```json
{
  "model": "TinyLlama-1.1B-ov",
  "created_at": "2025-12-28T12:34:56Z",
  "response": "Artificial intelligence (AI) is...",
  "done": true,
  "total_duration": 620000000,
  "load_duration": 0,
  "prompt_eval_count": 5,
  "eval_count": 67
}
```

### 4. Chat Completion
```http
POST http://127.0.0.1:8000/api/chat
```

**Request Body:**
```json
{
  "model": "TinyLlama-1.1B-ov",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are the benefits of Intel Arc GPUs?"}
  ],
  "stream": false,
  "max_new_tokens": 256
}
```

**Response:**
```json
{
  "model": "TinyLlama-1.1B-ov",
  "created_at": "2025-12-28T12:34:56Z",
  "message": {
    "role": "assistant",
    "content": "Intel Arc GPUs offer several benefits..."
  },
  "done": true,
  "total_duration": 750000000
}
```

### 5. List Running Models
```http
GET http://127.0.0.1:8000/api/ps
```

**Response:**
```json
{
  "models": [
    {
      "name": "TinyLlama-1.1B-ov",
      "model": "TinyLlama-1.1B-ov",
      "size": 0,
      "digest": "openvino-genai",
      "expires_at": "0001-01-01T00:00:00Z"
    }
  ]
}
```

## Usage Examples

### PowerShell

```powershell
# Simple generation
$body = @{
    model = "TinyLlama-1.1B-ov"
    prompt = "Write a haiku about AI."
    stream = $false
    max_new_tokens = 128
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/generate" -Body $body -ContentType "application/json"
Write-Host $response.response
```

```powershell
# Chat conversation
$body = @{
    model = "TinyLlama-1.1B-ov"
    messages = @(
        @{ role = "user"; content = "Hello! How are you?" }
    )
    stream = $false
    max_new_tokens = 128
} | ConvertTo-Json -Depth 10

$response = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/chat" -Body $body -ContentType "application/json"
Write-Host $response.message.content
```

### Python

```python
import requests

# Generate text
response = requests.post("http://127.0.0.1:8000/api/generate", json={
    "model": "TinyLlama-1.1B-ov",
    "prompt": "Explain quantum computing.",
    "stream": False,
    "max_new_tokens": 256
})

print(response.json()["response"])
```

```python
# Chat
response = requests.post("http://127.0.0.1:8000/api/chat", json={
    "model": "TinyLlama-1.1B-ov",
    "messages": [
        {"role": "user", "content": "What is Python?"}
    ],
    "stream": False,
    "max_new_tokens": 256
})

print(response.json()["message"]["content"])
```

### curl

```bash
# Generate text
curl -X POST http://127.0.0.1:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TinyLlama-1.1B-ov",
    "prompt": "What is machine learning?",
    "stream": false,
    "max_new_tokens": 256
  }'
```

## Python Test Client

Run the included test script to verify all endpoints:

```powershell
conda activate openvino-genai
python test_api_client.py
```

This will test:
1. Health check
2. List models
3. Text generation
4. Chat completion
5. Show PowerShell examples

## Configuration

### Change Model

Edit `serve_openvino.py` line 31:
```python
model_name = "TinyLlama-1.1B-ov"  # Change to your model directory
```

### Change Port

Edit `serve_openvino.py` line 261:
```python
port=8000,  # Change to desired port
```

### Change Host (Allow External Access)

Edit `serve_openvino.py` line 260:
```python
host="0.0.0.0",  # Allow access from other computers
```

**Warning:** Only do this on trusted networks!

## Performance

| Metric | Value |
|--------|-------|
| Model load time | ~2 seconds |
| Simple prompt (64 tokens) | ~0.6 seconds |
| Complex prompt (256 tokens) | ~1.5 seconds |
| Concurrent requests | Serialized (one at a time) |

## Limitations

1. **Single model at a time**: Server loads one model. To use different models, restart the server.
2. **No streaming**: Currently returns full response (not incremental tokens).
3. **No concurrent requests**: Requests are processed sequentially.
4. **No model caching**: Server must run continuously or model reloads on restart.

## Integration with Other Applications

### VS Code / Cursor

Configure as OpenAI-compatible endpoint:
```json
{
  "openai.apiBase": "http://127.0.0.1:8000",
  "openai.model": "TinyLlama-1.1B-ov"
}
```

### Continue (VS Code extension)

Add to `config.json`:
```json
{
  "models": [
    {
      "title": "OpenVINO Local",
      "provider": "openai",
      "model": "TinyLlama-1.1B-ov",
      "apiBase": "http://127.0.0.1:8000"
    }
  ]
}
```

### Custom Applications

Any application that can make HTTP requests can use this API:
- Python scripts with `requests`
- PowerShell scripts with `Invoke-RestMethod`
- JavaScript/Node.js with `fetch` or `axios`
- C# applications with `HttpClient`
- Postman or other API testing tools

## Troubleshooting

### Port Already in Use

```
ERROR: [Errno 10048] error while attempting to bind on address
```

**Solution:** Change port in `serve_openvino.py` or stop the conflicting service (e.g., IPEX-LLM Ollama on port 11434).

### Model Not Found

```
Error loading model: [Errno 2] No such file or directory
```

**Solution:** Ensure the model directory exists and update `model_name` in `serve_openvino.py`.

### GPU Not Detected

Check available devices:
```python
from openvino import Core
print(Core().available_devices)
```

Should include `'GPU'`.

### Slow First Request

**Normal behavior** - First request triggers model compilation. Subsequent requests are much faster.

## Next Steps

1. **Convert larger models** for better quality responses
2. **Add streaming support** for real-time token generation
3. **Add authentication** for production use
4. **Add model switching** endpoint to change models without restart
5. **Add request queuing** for concurrent request handling
6. **Create Docker container** for easier deployment

## Files

- `serve_openvino.py` - FastAPI server implementation
- `test_api_client.py` - Python test client
- `docs/api-server.md` - This documentation
