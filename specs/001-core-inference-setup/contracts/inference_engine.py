from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class InferenceConfig:
    model_id: str
    device: str = "xpu"
    precision: str = "sym_int4"
    max_new_tokens: int = 32
    trust_remote_code: bool = True

class InferenceEngine(ABC):
    """
    Abstract base class for the IPEX-LLM inference engine.
    """

    @abstractmethod
    def __init__(self, config: InferenceConfig):
        """
        Initialize the engine with configuration.
        """
        pass

    @abstractmethod
    def load_model(self) -> None:
        """
        Load the model and tokenizer, apply quantization, and move to XPU.
        """
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate text based on the input prompt.
        
        Args:
            prompt: The input text string.
            
        Returns:
            The generated text string.
        """
        pass
