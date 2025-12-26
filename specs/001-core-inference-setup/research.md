# Research: Initial Setup and Core Inference Engine

**Feature**: Core Inference Setup
**Date**: 2025-12-26

## 1. Ollama Integration Strategy

**Question**: How do we serve models via Ollama using the Intel Arc 140V iGPU?

**Findings**:
- The repository already contains `scripts/start-ollama.ps1`.
- This script sets specific environment variables required for Intel XPU support:
  - `OLLAMA_NUM_GPU = 999`: Forces GPU offloading.
  - `ANY_ONEAPI_DEVICE_SELECTOR = "level_zero:0"`: Selects the Level Zero backend for the iGPU.
- **Decision**: We will utilize and enhance the existing `scripts/start-ollama.ps1` as the primary entry point for Ollama serving. No custom Ollama build is required, assuming the user has the Intel-optimized libraries or the standard Ollama build supports these flags (which is common for Intel forks).

## 2. IPEX-LLM Installation

**Question**: What is the correct installation procedure for Windows with Arc 140V?

**Findings**:
- The README specifies: `pip install --pre --upgrade ipex-llm[xpu] --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/`.
- This installs the pre-release version with XPU support.
- **Decision**: Use this exact command in the `setup-env.ps1` script. We will also ensure `torch` is installed from the same index to avoid version mismatches.

## 3. Model Loading & Quantization

**Question**: How do we ensure 4-bit quantization for the validation model (Llama 3.1 8B)?

**Findings**:
- `ipex_llm.transformers` provides `AutoModelForCausalLM`.
- The `load_in_4bit=True` parameter is the standard API for this.
- **Decision**: The `engine.py` module will wrap `AutoModelForCausalLM.from_pretrained` and hardcode `load_in_4bit=True` (or make it the default) to comply with the Constitution.

## 4. Validation Strategy

**Question**: How do we validate the setup without downloading a massive 27B model first?

**Findings**:
- Llama 3.1 8B is significantly smaller (~5GB quantized) than Gemma 2 27B (~15GB+).
- **Decision**: The `run-inference.py` script will default to `meta-llama/Meta-Llama-3.1-8B-Instruct` (or a similar open weight model if access is restricted, e.g., `microsoft/Phi-3-mini-4k-instruct`) for the initial test. *Correction*: Spec agreed on Llama 3.1 8B. We will use that.

## 5. Unknowns Resolved

- [x] Ollama configuration
- [x] Installation commands
- [x] Validation model choice
