<!-- Sync Impact Report
- Version change: 0.0.0 -> 1.0.0 (Initial Ratification)
- Modified principles: N/A (New Constitution)
- Added sections: All Principles, Implementation Standards, Development Workflow, Governance
- Removed sections: N/A
- Templates requiring updates: None
- Follow-up TODOs: None
-->

# Lunar-LLM Galaxy Constitution

## Core Principles

### I. Hardware-Specific Optimization (XPU-First)
We explicitly target Intel Lunar Lake (Series 2) architecture and the Arc 140V iGPU. Code MUST utilize `xpu` device selectors and IPEX-LLM extensions, avoiding generic CUDA or CPU-only paths unless as a fallback. The system is designed to extract maximum performance from this specific hardware.

### II. Memory Efficiency via Quantization
To maximize the 32GB unified memory, models MUST use low-bit precision (INT4/FP8) by default. We prioritize fitting larger models (e.g., 32B) over full precision, ensuring no system crashes due to OOM. Memory management strategies like optimized KV caching are essential.

### III. Local & Private Inference
All inference runs locally. No data is sent to cloud APIs. The system MUST be self-contained and capable of running offline after initial setup. Privacy and local capability are paramount.

### IV. Environment Isolation
Dependencies MUST be managed in a dedicated Conda environment to prevent conflicts with system Python or other projects. Hardware acceleration environment variables (e.g., `OLLAMA_NUM_GPU`, `ANY_ONEAPI_DEVICE_SELECTOR`) MUST be explicitly configured within this environment.

### V. Performance Monitoring
We value measurable performance. Tools MUST be included to monitor NPU/iGPU load and token generation speed (tokens/sec). Optimization efforts should be guided by these metrics.

## Implementation Standards

**Technology Stack**:
- **Language**: Python 3.10+ (compatible with IPEX-LLM)
- **Core Library**: IPEX-LLM (Intel Extension for PyTorch)
- **Inference Engine**: Ollama (Intel-Optimized) or custom Python scripts using `ipex-llm`. Ollama MUST be launched via `scripts/start-ollama.ps1` to ensure XPU targeting.
- **Hardware Target**: Intel Arc 140V (Lunar Lake)

**Code Quality**:
- Scripts must include error handling for hardware initialization failures.
- Performance-critical sections should be commented with rationale.

## Development Workflow

**Testing & Validation**:
- All changes MUST be verified on actual Lunar Lake hardware.
- Performance regressions (drop in tokens/sec) must be investigated.

**Documentation**:
- Maintain a `devlog` for architectural decisions and performance benchmarks.
- Update `README.md` with setup instructions for the specific Conda environment.

## Governance

This constitution supersedes all other practices. Amendments require documentation and approval.

**Version**: 1.0.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-26
