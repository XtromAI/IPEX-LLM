"""
OpenVINO GenAI REST API Server
Provides Ollama-compatible endpoints for local model serving

Usage:
    conda activate openvino-genai
    python serve_openvino.py

Default: http://127.0.0.1:8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import openvino_genai as ov_genai
import uvicorn
import json
import time
import asyncio
from contextlib import asynccontextmanager

# Global model pipeline
pipeline = None
model_name = None

class GenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False
    max_new_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: bool = False
    max_new_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class ListModelsResponse(BaseModel):
    models: List[Dict[str, Any]]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup"""
    global pipeline, model_name
    
    # Default model - change this to your model directory
    model_name = "TinyLlama-1.1B-ov"
    
    print(f"\n{'='*60}")
    print(f"OpenVINO GenAI Server")
    print(f"{'='*60}")
    print(f"Loading model: {model_name}")
    print(f"Device: GPU (Intel Arc 140V)")
    
    try:
        start = time.time()
        pipeline = ov_genai.LLMPipeline(model_name, "GPU")
        load_time = time.time() - start
        print(f"Model loaded in {load_time:.2f}s")
        print(f"\n✓ Server ready at http://127.0.0.1:11435")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Make sure the model directory exists!")
        raise
    
    yield
    
    # Cleanup on shutdown
    print("\nShutting down server...")

app = FastAPI(
    title="OpenVINO GenAI Server",
    description="REST API for OpenVINO GenAI models",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": model_name,
        "message": "OpenVINO GenAI Server is running"
    }

@app.get("/api/tags")
async def list_models():
    """List available models (Ollama-compatible)"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "models": [
            {
                "name": model_name,
                "model": model_name,
                "modified_at": "2025-12-28T00:00:00Z",
                "size": 0,  # Could calculate actual size
                "digest": "openvino-genai",
                "details": {
                    "format": "openvino",
                    "family": "llama",
                    "quantization_level": "int4"
                }
            }
        ]
    }

@app.post("/api/generate")
async def generate(request: GenerateRequest):
    """Generate text from prompt (Ollama-compatible)"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        start_time = time.time()
        
        # Generate response
        response_text = pipeline.generate(
            request.prompt,
            max_new_tokens=request.max_new_tokens
        )
        
        generation_time = time.time() - start_time
        
        if request.stream:
            # For streaming, return single response (true streaming would need callback support)
            async def stream_response():
                yield json.dumps({
                    "model": request.model,
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "response": response_text,
                    "done": True,
                    "total_duration": int(generation_time * 1e9),
                    "load_duration": 0,
                    "prompt_eval_count": len(request.prompt.split()),
                    "eval_count": len(response_text.split()),
                }) + "\n"
            
            return StreamingResponse(stream_response(), media_type="application/x-ndjson")
        else:
            # Non-streaming response
            return {
                "model": request.model,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "response": response_text,
                "done": True,
                "total_duration": int(generation_time * 1e9),
                "load_duration": 0,
                "prompt_eval_count": len(request.prompt.split()),
                "eval_count": len(response_text.split()),
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat completion endpoint (Ollama-compatible)"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert chat messages to prompt
        prompt_parts = []
        for msg in request.messages:
            if msg.role == "system":
                prompt_parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")
        
        prompt = "\n".join(prompt_parts) + "\nAssistant:"
        
        start_time = time.time()
        
        # Generate response
        response_text = pipeline.generate(
            prompt,
            max_new_tokens=request.max_new_tokens
        )
        
        # Clean up response
        if "Assistant:" in response_text:
            response_text = response_text.split("Assistant:")[-1].strip()
        if "User:" in response_text:
            response_text = response_text.split("User:")[0].strip()
        
        generation_time = time.time() - start_time
        
        if request.stream:
            async def stream_response():
                yield json.dumps({
                    "model": request.model,
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "done": True,
                    "total_duration": int(generation_time * 1e9),
                }) + "\n"
            
            return StreamingResponse(stream_response(), media_type="application/x-ndjson")
        else:
            return {
                "model": request.model,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "done": True,
                "total_duration": int(generation_time * 1e9),
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ps")
async def list_running():
    """List running models (Ollama-compatible)"""
    if pipeline is None:
        return {"models": []}
    
    return {
        "models": [
            {
                "name": model_name,
                "model": model_name,
                "size": 0,
                "digest": "openvino-genai",
                "expires_at": "0001-01-01T00:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    print("\nStarting OpenVINO GenAI Server...")
    print("Press Ctrl+C to stop\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=11435,
        log_level="info"
    )