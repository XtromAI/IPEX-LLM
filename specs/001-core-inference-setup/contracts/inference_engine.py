from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class InferenceConfig:
    """Configuration for the Ollama-backed inference engine.

    The engine forwards requests to a running Ollama server instead of
    loading models into the local Python process.
    """

    model: str
    host: str = "http://127.0.0.1:11434"
    stream: bool = False
    options: Dict[str, Any] = field(default_factory=dict)


class InferenceEngine(ABC):
    """Abstract base class for an Ollama-based inference engine."""

    @abstractmethod
    def __init__(self, config: InferenceConfig) -> None:
        """Initialize the engine with configuration."""

    @abstractmethod
    def load_model(self) -> None:
        """Perform any warm-up or health checks against the Ollama server."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text based on the input prompt via Ollama."""

