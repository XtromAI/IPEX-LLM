# Copilot Instructions for IPEX-LLM (Lunar Lake)

## Project Context
This project builds a high-performance local inference environment for **Intel Lunar Lake (Series 2)** architecture, specifically targeting the **Samsung Galaxy Book5 Pro** with **Intel Arc 140V iGPU** and **32GB LPDDR5X unified memory**.

## Core Principles
- **XPU-First:** All inference code MUST target `device='xpu'` to utilize the Arc 140V iGPU. Do NOT use `cuda` or `cpu` for primary inference.
- **Memory Efficiency:** Default to **INT4** or **FP8** quantization. The goal is to fit 27B-32B parameter models into the 32GB shared memory.
- **Environment:** Assume execution within a dedicated **Conda** environment with Intel oneAPI/SYCL libraries.

## Coding Conventions

### Library Usage
- Use `ipex_llm` and `ipex_llm.transformers` for optimized model loading.
- Standard imports:
  ```python
  import torch
  import intel_extension_for_pytorch as ipex
  from ipex_llm.transformers import AutoModelForCausalLM
  ```

### Model Loading Pattern
- Always use low-bit optimization (`load_in_4bit=True` or `load_in_low_bit="sym_int4"`).
- Move model to XPU immediately after loading.
  ```python
  model = AutoModelForCausalLM.from_pretrained(
      model_path,
      load_in_4bit=True,
      trust_remote_code=True,
      use_cache=True
  )
  model = model.to('xpu')
  ```

### Inference Loop
- Ensure all inputs are on the XPU device.
  ```python
  input_ids = tokenizer.encode(prompt, return_tensors="pt").to('xpu')
  ```
- **JIT Compilation:** The first run will be slower due to kernel compilation. This is expected behavior.

## Environment Configuration
- **Variables:** The environment relies on specific variables for hardware acceleration:
  - `OLLAMA_NUM_GPU=999` (forces GPU usage in Ollama)
  - `ANY_ONEAPI_DEVICE_SELECTOR` (controls SYCL device selection)
- **Isolation:** Do not rely on system-wide Python packages.

## Architecture & Hardware
- **Target Device:** Intel Arc 140V iGPU (`xpu`).
- **NPU Usage:** The NPU is **NOT** the primary inference target. It is reserved for background monitoring or future power-efficiency experiments.
- **Unified Memory:** Be conscious of the 32GB limit. Aggressive quantization is mandatory for large models.

## Documentation
- Refer to `docs/devlog/` for architectural decisions and `specify/memory/constitution.md` for core principles.
