import subprocess
import pytest

def test_conda_environment_exists():
    """Verify that the ipex-llm environment exists."""
    try:
        result = subprocess.run(["conda", "env", "list"], capture_output=True, text=True, check=True)
        assert "ipex-llm" in result.stdout, "Conda environment 'ipex-llm' not found."
    except FileNotFoundError:
        pytest.fail("Conda command not found. Ensure Conda is installed and in PATH.")

def test_python_version():
    """Verify Python version in the environment is 3.10."""
    try:
        result = subprocess.run(
            ["conda", "run", "-n", "ipex-llm", "python", "--version"], 
            capture_output=True, 
            text=True,
            check=True
        )
        # Python version output can be in stdout or stderr depending on version/platform
        output = result.stdout + result.stderr
        assert "Python 3.10" in output, f"Expected Python 3.10, got: {output.strip()}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run python in conda env: {e}")

def test_packages_installed():
    """Verify required packages are installed."""
    try:
        result = subprocess.run(
            ["conda", "list", "-n", "ipex-llm"], 
            capture_output=True, 
            text=True,
            check=True
        )
        stdout = result.stdout
        
        # Note: Package names in conda list might differ slightly (e.g. underscores vs dashes)
        # but usually they match the pip name.
        required_packages = ["ipex-llm", "torch", "transformers", "accelerate"]
        for pkg in required_packages:
            assert pkg in stdout, f"Package '{pkg}' not found in environment."
            
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to list packages in conda env: {e}")
