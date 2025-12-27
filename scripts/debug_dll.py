import os
import sys
import ctypes
from ctypes import wintypes

# Define kernel32 functions for loading libraries with debug info
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

def check_dll(dll_path):
    print(f"Checking DLL: {dll_path}")
    if not os.path.exists(dll_path):
        print("  -> File does NOT exist.")
        return

    # Try to load the library to see if Windows can resolve dependencies
    # LOAD_LIBRARY_SEARCH_DEFAULT_DIRS | LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR
    try:
        # Standard load
        lib = ctypes.CDLL(dll_path)
        print("  -> Successfully loaded via ctypes.")
    except OSError as e:
        print(f"  -> Failed to load: {e}")
        print("     This usually means a dependency is missing.")

def main():
    # Path from your error message
    base_path = r"C:\Users\creks\miniconda3\envs\ipex-llm\lib\site-packages\torch\lib"
    target_dll = os.path.join(base_path, "backend_with_compiler.dll")
    
    print(f"--- DLL Diagnostic ---")
    print(f"Base Path: {base_path}")
    
    # 1. Check if the directory is in PATH
    in_path = False
    for p in os.environ['PATH'].split(';'):
        if os.path.normpath(p) == os.path.normpath(base_path):
            in_path = True
            break
    print(f"Is torch/lib in PATH? {in_path}")
    
    # 2. Add to PATH temporarily and try loading
    if not in_path:
        print("Adding torch/lib to PATH for testing...")
        os.environ['PATH'] = base_path + ';' + os.environ['PATH']
        
    # 3. Check specific known dependencies for IPEX
    # These are common culprits
    dependencies = [
        "sycl.dll", 
        "pi_level_zero.dll",
        "svml_dispmt.dll", 
        "libmmd.dll"
    ]
    
    print("\nChecking common dependencies in PATH:")
    for dep in dependencies:
        found = False
        for path in os.environ['PATH'].split(';'):
            full_path = os.path.join(path, dep)
            if os.path.exists(full_path):
                print(f"  [OK] Found {dep} in {path}")
                found = True
                break
        if not found:
            print(f"  [MISSING] Could not find {dep} in PATH")

    print("\nAttempting to load target DLL:")
    check_dll(target_dll)

if __name__ == "__main__":
    main()
