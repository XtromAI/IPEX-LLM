# Implementation Plan: Initial Setup and Core Inference Engine

**Branch**: `001-core-inference-setup` | **Date**: 2025-12-26 | **Spec**: [specs/001-core-inference-setup/spec.md](../spec.md)
**Input**: Feature specification from `specs/001-core-inference-setup/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the core infrastructure for local LLM inference on Intel Lunar Lake hardware. This includes an automated setup script for the Conda environment, installation of IPEX-LLM with XPU support, and a Python-based inference engine capable of serving models via Ollama and running standalone inference scripts with 4-bit quantization.

## Technical Context

**Language/Version**: Python 3.10
**Primary Dependencies**: `ipex-llm[xpu]`, `torch`, `ollama`, `transformers`
**Storage**: Local file system (Hugging Face cache, model weights)
**Testing**: `pytest` for unit tests, manual verification for hardware integration
**Target Platform**: Windows 11 (Intel Arc 140V iGPU)
**Project Type**: Python Script/CLI
**Performance Goals**: 5-15+ tokens/sec on 27B models (via INT4)
**Constraints**: Max 32GB RAM usage, mandatory INT4 quantization, XPU execution
**Scale/Scope**: Single-user local environment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Hardware-Specific Optimization (XPU-First)**: PASS. Plan explicitly targets `ipex-llm[xpu]` and Arc 140V.
- **II. Memory Efficiency via Quantization**: PASS. Mandatory 4-bit quantization is a core requirement.
- **III. Local & Private Inference**: PASS. All inference is local; model download is the only external connection.
- **IV. Environment Isolation**: PASS. Automated Conda environment setup is the first deliverable.
- **V. Performance Monitoring**: PASS. Success criteria include performance metrics.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-inference-setup/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
scripts/
├── setup-env.ps1        # Environment creation script
├── run-inference.py     # Standalone inference script
└── start-ollama.ps1     # Existing script to be updated/verified

src/
├── __init__.py
├── config.py            # Configuration management
└── engine.py            # Core inference logic wrapping IPEX-LLM

tests/
├── test_setup.py        # Environment verification tests
└── test_engine.py       # Unit tests for engine logic
```

**Structure Decision**: Standard Python project structure with a `scripts` directory for user-facing executables and a `src` directory for reusable logic.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
