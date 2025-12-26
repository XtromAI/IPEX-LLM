import sys
import torch
from typing import Optional

try:
    import intel_extension_for_pytorch as ipex
    from ipex_llm.transformers import AutoModelForCausalLM
except ImportError:
    print("Warning: IPEX-LLM or Intel Extension for PyTorch not found. Ensure you are in the 'ipex-llm' environment.")
    # We don't exit here to allow unit tests to mock these imports if needed
    ipex = None
    AutoModelForCausalLM = None

from transformers import AutoTokenizer
from src.config import InferenceConfig

class InferenceEngine:
    def __init__(self, config: Optional[InferenceConfig] = None):
        self.config = config or InferenceConfig()
        self.model = None
        self.tokenizer = None

    def load_model(self):
        if AutoModelForCausalLM is None:
            raise ImportError("IPEX-LLM is not installed.")

        print(f"Loading model '{self.config.model_id}'...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_id, 
            trust_remote_code=self.config.trust_remote_code
        )
        
        # Load model with 4-bit optimization
        print(f"Loading model with load_in_4bit=True...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_id,
            load_in_4bit=True,
            trust_remote_code=self.config.trust_remote_code,
            use_cache=True
        )
        
        # Move to XPU
        if self.config.device == "xpu":
            if not hasattr(torch, 'xpu') and not (ipex and hasattr(ipex, 'xpu')):
                 print("Warning: 'xpu' device not found in torch. Using 'cpu' or checking availability.")
            
            print("Moving model to XPU...")
            self.model = self.model.to("xpu")
        
        print("Model loaded successfully.")

    def generate(self, prompt: str) -> str:
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        print(f"Generating response for prompt: '{prompt}'")

        # Encode input
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        
        # Move input to XPU
        if self.config.device == "xpu":
            input_ids = input_ids.to("xpu")

        # Generate
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=self.config.max_new_tokens,
                do_sample=False, # Deterministic for validation
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode output
        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output_text
