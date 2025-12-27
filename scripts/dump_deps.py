import os
import pefile

def dump(path: str):
    print(f"path: {path}")
    pe = pefile.PE(path)
    imports = [entry.dll.decode().lower() for entry in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', [])]
    delay = [entry.dll.decode().lower() for entry in getattr(pe, 'DIRECTORY_ENTRY_DELAY_IMPORT', [])]
    print(f"imports ({len(imports)}): {imports[:40]}")
    print(f"delay ({len(delay)}): {delay[:40]}")

if __name__ == "__main__":
    base = os.environ["CONDA_PREFIX"]
    target = os.path.join(base, "Lib", "site-packages", "intel_extension_for_pytorch", "bin", "intel-ext-pt-gpu.dll")
    dump(target)
