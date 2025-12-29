# IPEX-LLM Repository

This repository contains AI inference solutions for Intel hardware, organized into two distinct sections:

## 🚀 Sections

### 1. [IPEX with Ollama](./ipex-ollama/)
**For Intel Arc GPU (Lunar Lake) workflows**

A complete Ollama setup optimized for Intel Arc 140V iGPU with IPEX-LLM optimizations. Ideal for running INT4 GGUF models on Samsung Galaxy Book5 Pro and similar Intel Lunar Lake laptops.

- **Target Hardware:** Intel Lunar Lake (Arc 140V iGPU, 32 GB unified memory)
- **Software Stack:** Ollama + IPEX-LLM + Intel oneAPI
- **Use Case:** Fast local inference with INT4 quantized models
- **Documentation:** [IPEX-Ollama README](./ipex-ollama/README.md)

**Quick Start:**
```powershell
cd ipex-ollama
.\scripts\start-ollama-server.ps1
```

### 2. [OpenVINO](./openvino/)
**For OpenVINO-based workflows**

OpenVINO toolkit integration for Intel CPU/GPU inference. This section is under development.

- **Target Hardware:** Intel CPUs and GPUs (various generations)
- **Software Stack:** OpenVINO toolkit
- **Use Case:** Optimized inference for Intel hardware
- **Documentation:** [OpenVINO README](./openvino/README.md)

## 📋 Choosing the Right Section

| Feature | IPEX-Ollama | OpenVINO |
|---------|-------------|----------|
| **Best For** | Arc GPU (Lunar Lake) | Intel CPUs/GPUs (general) |
| **Model Format** | GGUF (INT4) | IR, ONNX |
| **Setup Complexity** | Low (ready to run) | Medium |
| **Memory Efficiency** | High (unified memory) | Good |
| **Quantization** | INT4 default | FP16, INT8 |

## 🛠️ Repository Structure

```
IPEX-LLM/
├── ipex-ollama/           # IPEX + Ollama workflow
│   ├── README.md          # Detailed documentation
│   ├── scripts/           # PowerShell automation scripts
│   └── docs/              # Additional documentation
│
├── openvino/              # OpenVINO workflow
│   ├── README.md          # OpenVINO documentation
│   ├── scripts/           # OpenVINO scripts
│   └── docs/              # OpenVINO guides
│
└── README.md              # This file
```

## 🤝 Contributing

When contributing, please ensure changes are made to the appropriate section:
- IPEX/Ollama changes → `ipex-ollama/`
- OpenVINO changes → `openvino/`

## 📝 License

See individual section READMEs for license information.

## 🔗 Resources

- [Intel IPEX-LLM](https://github.com/intel-analytics/ipex-llm)
- [Ollama](https://ollama.com/)
- [OpenVINO Toolkit](https://github.com/openvinotoolkit/openvino)
- [Intel oneAPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/overview.html)
