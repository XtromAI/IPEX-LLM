# Devlog: Constitution Ratification & Architecture Decisions

**Date**: 2025-12-26

## 1. Constitution Ratified (v1.0.0)
The project constitution has been formally ratified at `.specify/memory/constitution.md`.

**Key Principles**:
- **XPU-First**: Explicit targeting of Intel Arc 140V iGPU.
- **Memory Efficiency**: Mandatory INT4/FP8 quantization to fit 32B models in 32GB RAM.
- **Local & Private**: No cloud dependencies.
- **Environment Isolation**: Conda required.

## 2. Architecture Clarifications

### Conda vs. Pure Python
**Question**: Is Conda necessary?
**Decision**: Yes, highly recommended and currently mandated by Constitution (Principle IV).
**Reasoning**:
- Avoids "DLL Hell" with Intel oneAPI/SYCL libraries.
- Simplifies management of `xpu` optimized PyTorch versions.
- Pure Python is possible but requires manual path/driver management.

### Understanding "XPU"
**Definition**: Intel's "Cross-Processing Unit" abstraction.
**Context**: In this project, `device='xpu'` specifically targets the **Arc 140V iGPU**. It allows standard PyTorch code to utilize the integrated graphics for tensor operations.

### NPU vs. GPU Strategy
**Question**: Are we using the NPU?
**Decision**: **No**, we are sticking with the **iGPU (XPU)** for primary inference.
**Reasoning**:
- **Performance**: The iGPU (Arc 140V) offers better memory bandwidth and compute for large models (27B-32B).
- **Maturity**: IPEX-LLM support for interactive LLMs is more mature on XPU.
- **Role of NPU**: Relegated to background monitoring or future power-efficiency experiments, not the main inference engine.
