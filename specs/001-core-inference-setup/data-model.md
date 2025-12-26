# Data Model: Core Inference Setup

## Configuration Entities

### EnvironmentConfig
Defines the requirements for the isolated runtime environment.

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `env_name` | string | Name of the Conda environment | "ipex-llm" |
| `python_version` | string | Python version | "3.10" |
| `packages` | list[string] | List of pip packages to install | `["ipex-llm[xpu]", "torch", "transformers", "accelerate"]` |
| `extra_index_url` | string | URL for Intel-optimized wheels | "https://pytorch-extension.intel.com/release-whl/stable/xpu/us/" |

### InferenceConfig
Configuration for the inference engine execution.

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `model_id` | string | Hugging Face model identifier | "meta-llama/Meta-Llama-3.1-8B-Instruct" |
| `device` | string | Target hardware device | "xpu" |
| `precision` | string | Quantization precision | "sym_int4" |
| `max_new_tokens` | int | Maximum tokens to generate | 32 |
| `trust_remote_code` | boolean | Whether to trust remote code | true |

## Runtime Objects

### InferenceEngine
The main class responsible for managing the model lifecycle.

- **State**:
  - `model`: The loaded PyTorch model object (on XPU).
  - `tokenizer`: The associated tokenizer.
  - `config`: The `InferenceConfig` instance.

- **Lifecycle**:
  1. `__init__(config)`: Initializes configuration.
  2. `load_model()`: Downloads and loads model to RAM, quantizes (if needed), moves to XPU.
  3. `generate(prompt)`: Tokenizes input, runs inference, decodes output.
  4. `unload()`: Frees memory (if applicable).
