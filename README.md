# Lunar-LLM (Galaxy Book5 Pro Edition)

A high-performance local inference environment optimized for **Intel Lunar Lake (Series 2)** architecture. This project uses **Intel's Ollama Portable Zip with IPEX-LLM** to run state-of-the-art models (DeepSeek-R1, Qwen, Phi-4) on the **Intel Arc 140V iGPU**.

## 🎯 Goal
Run 7B-30B parameter models locally at usable speeds on a laptop by utilizing the 32GB unified LPDDR5X memory and XPU acceleration with INT4 quantization.

## 💻 Hardware Requirements
- **Device:** Samsung Galaxy Book5 Pro (or similar Lunar Lake device)
- **GPU:** Intel Arc 140V (Xe2-LPG architecture)
- **RAM:** 32GB LPDDR5X (Unified Memory)
- **OS:** Windows 11

## 🚀 Quick Start

### 1. Download and Setup (One-Time)
```powershell
# Run the automated setup script
.\scripts\setup-ollama-portable.ps1
```

This downloads Intel's pre-configured Ollama (~500MB) with all runtime dependencies.

### 2. Start the Server
```powershell
.\scripts\start-ollama-server.ps1
```

### 3. Run Models
Open a **new** terminal and run:
```powershell
cd ollama-portable
.\ollama.exe run deepseek-r1:7b
```

**That's it!** No Python, no conda, no dependency management needed.

## 📚 Recommended Models

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| `llama3.2:3b` | 2GB | ⚡ Very Fast | Quick tasks, code completion |
| `qwen2.5:7b` | 4.5GB | ⚡ Fast | General purpose, balanced |
| `deepseek-r1:7b` | 4.7GB | ⚡ Fast | Reasoning, problem solving |
| `phi4` | 8.5GB | 🔥 Medium | High quality responses |
| `deepseek-r1:14b` | 9.4GB | 🔥 Medium | Complex reasoning |
| `qwen3:30b` | 19GB | 🐢 Slower | Maximum capability |

## 🧠 Core Principles
*   **XPU-First:** Models run on Intel Arc 140V iGPU with INT4 quantization
*   **Memory Efficiency:** 32GB unified memory allows models up to ~20GB
*   **Zero Config:** Ollama Portable bundles all Intel runtime dependencies
*   **JIT Compilation:** The first prompt response will be slower due to kernel compilation.

## 📂 Documentation
*   [Devlog](docs/devlog/): Architectural decisions and daily updates.
*   [Constitution](.specify/memory/constitution.md): Core project rules and hardware constraints.
