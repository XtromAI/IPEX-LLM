# Lunar-LLM (Galaxy Book5 Pro Edition)

A high-performance local inference environment optimized for **Intel Lunar Lake (Series 2)** architecture. This project leverages **IPEX-LLM** to run state-of-the-art models (Gemma 3, Phi-4) on the **Intel Arc 140V iGPU**.

## 🎯 Goal
Run 27B-32B parameter models locally at usable speeds (5-15+ tokens/sec) on a laptop by utilizing the 32GB unified LPDDR5X memory and XPU acceleration.

## 💻 Hardware Requirements
- **Device:** Samsung Galaxy Book5 Pro (or similar Lunar Lake device)
- **GPU:** Intel Arc 140V (Target: `xpu`)
- **RAM:** 32GB LPDDR5X (Unified Memory)
- **OS:** Windows 11 (WSL2 supported but native Windows preferred for driver access)

## 🚀 Quick Start

### 1. Prerequisites
- Install **Miniconda** or **Anaconda**.
- Ensure latest **Intel Graphics Drivers** are installed.

### 2. Automated Setup
Run the setup script to create the `ipex-llm` Conda environment and install all dependencies.

```powershell
.\scripts\setup-env.ps1
```

Activate the environment:
```powershell
conda activate ipex-llm
```

### 3. Running Inference (Python)
Run the CLI script to test inference on the Intel Arc 140V. This defaults to `meta-llama/Meta-Llama-3.1-8B-Instruct` with INT4 quantization.

```powershell
python scripts/run-inference.py --prompt "Why is the sky blue?"
```

### 4. Ollama Configuration
To use Ollama with Intel Arc acceleration, use the provided helper script which configures the necessary environment variables (`OLLAMA_NUM_GPU`, `ANY_ONEAPI_DEVICE_SELECTOR`).

1.  **Start the Server** (in a dedicated terminal):
    ```powershell
    .\scripts\start-ollama.ps1
    ```
    *Keep this terminal open. It hosts the model.*

2.  **Run a Model** (in a new terminal):
    ```powershell
    ollama run gemma2:27b
    ```

## 🧠 Core Principles
*   **XPU-First:** Always target `device='xpu'`. The NPU is reserved for monitoring.
*   **Memory Efficiency:** 32GB is the hard limit. Use `load_in_4bit=True` or `sym_int4` for all large models.
*   **JIT Compilation:** The first prompt response will be slower due to kernel compilation.

## 📂 Documentation
*   [Devlog](docs/devlog/): Architectural decisions and daily updates.
*   [Constitution](.specify/memory/constitution.md): Core project rules and hardware constraints.
