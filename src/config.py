import os
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class InferenceConfig:
    """Configuration for calling the local Ollama server.

    This project treats Ollama Portable as the only inference backend.
    The model and host can be overridden via environment variables:

    - IPEX_LLM_MODEL: default model name (e.g. "llama3.2:3b")
    - OLLAMA_HOST:    base URL for the Ollama server (e.g. "http://127.0.0.1:11434")
    """

    model: str = os.getenv("IPEX_LLM_MODEL", "llama3.2:3b")
    host: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    stream: bool = False
    options: Dict[str, Any] = field(
        default_factory=lambda: {
            "temperature": 0.2,
            "num_ctx": 8192,
        }
    )

