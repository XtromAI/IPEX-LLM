---
description: "Task list for Initial Setup and Core Inference Engine"
---

# Tasks: Initial Setup and Core Inference Engine

**Input**: Design documents from `specs/001-core-inference-setup/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are included to verify the environment and engine logic.

**Organization**: Tasks are grouped by user story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (`src`, `scripts`, `tests`) per implementation plan
- [x] T002 Create `src/__init__.py` to make the directory a package

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 [P] Create `src/config.py` with `EnvironmentConfig` and `InferenceConfig` dataclasses

## Phase 3: User Story 1 - Environment Initialization (Priority: P1)

**Goal**: Automatically set up the development environment with IPEX-LLM and dependencies.

**Independent Test**: Run `scripts/setup-env.ps1` and verify `ipex-llm` environment exists.

### Implementation for User Story 1

- [x] T004 [US1] Create `scripts/setup-env.ps1` to handle Conda environment creation and dependency installation
- [x] T005 [US1] Create `tests/test_setup.py` to verify environment configuration (Python version, packages)

## Phase 4: User Story 2 - Ollama Inference Verification (Priority: P1)

**Goal**: Serve Llama 3.1 8B via Ollama and verify hardware acceleration using a Python inference engine.

**Independent Test**: Start Ollama and run inference; run `scripts/run-inference.py`.

### Implementation for User Story 2

- [x] T006 [P] [US2] Implement `InferenceEngine` class in `src/engine.py` (Model loading, Quantization, XPU move)
- [x] T007 [P] [US2] Create `scripts/run-inference.py` CLI script to invoke `InferenceEngine`
- [x] T008 [P] [US2] Create `tests/test_engine.py` for unit testing `InferenceEngine` logic
- [x] T009 [US2] Update/Verify `scripts/start-ollama.ps1` with correct Intel XPU environment variables

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and documentation

- [x] T010 Update `README.md` with usage instructions for new scripts
- [x] T011 Verify all scripts run on Windows 11 with Intel Arc 140V context

## Dependencies

1. **T001, T002, T003** (Setup/Foundational) must be done first.
2. **US1 (T004, T005)** can be done independently of US2.
3. **US2 (T006-T009)** depends on T003 (Config). T006/T007/T008 are the Python Engine. T009 is Ollama.

## Parallel Execution Examples

- **Developer A**: Works on **US1** (T004, T005) - Shell scripting.
- **Developer B**: Works on **US2** (T006, T007, T008) - Python development.
