import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import torch
    import intel_extension_for_pytorch as ipex
    print(f"Torch Version: {torch.__version__}")
    print(f"IPEX Version: {ipex.__version__}")
    print(f"XPU Available: {torch.xpu.is_available()}")
    if torch.xpu.is_available():
        print(f"Device Name: {torch.xpu.get_device_name(0)}")
except ImportError as e:
    print(f"Import Error: {e}")
except Exception as e:
    print(f"Error: {e}")
