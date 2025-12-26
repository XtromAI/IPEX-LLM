from dataclasses import dataclass, field
from typing import List

@dataclass
class EnvironmentConfig:
    env_name: str = "ipex-llm"
    python_version: str = "3.10"
    packages: List[str] = field(default_factory=lambda: ["ipex-llm[xpu]", "torch", "transformers", "accelerate"])
    extra_index_url: str = "https://pytorch-extension.intel.com/release-whl/stable/xpu/us/"

@dataclass
class InferenceConfig:
    model_id: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    device: str = "xpu"
    precision: str = "sym_int4"
    max_new_tokens: int = 32
    trust_remote_code: bool = True
