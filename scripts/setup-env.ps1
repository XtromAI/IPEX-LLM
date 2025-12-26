$ErrorActionPreference = "Stop"

# Check for Conda
if (-not (Get-Command "conda" -ErrorAction SilentlyContinue)) {
    Write-Error "Conda is not installed or not in PATH. Please install Miniconda or Anaconda."
    exit 1
}

# Configuration
$EnvName = "ipex-llm"
$PythonVersion = "3.10"
$ExtraIndexUrl = "https://pytorch-extension.intel.com/release-whl/stable/xpu/us/"
# Note: Using array for packages. PowerShell passes arrays to commands as separate arguments.
$Packages = "ipex-llm[xpu]", "torch", "transformers", "accelerate"

# Check if environment exists
Write-Host "Checking for Conda environment '$EnvName'..."
$EnvList = conda env list
if ($EnvList -match "^$EnvName\s") {
    Write-Host "Environment '$EnvName' already exists."
} else {
    Write-Host "Creating Conda environment '$EnvName' with Python $PythonVersion..."
    conda create -n $EnvName python=$PythonVersion -y
}

# Install packages
Write-Host "Installing/Updating packages in '$EnvName'..."
Write-Host "Packages: $Packages"
Write-Host "Index URL: $ExtraIndexUrl"

# Use conda run to execute pip install within the environment
# We join the packages with spaces for the command string
$PipArgs = "install", "--upgrade", $Packages, "--extra-index-url", $ExtraIndexUrl
conda run -n $EnvName pip $PipArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "Setup complete successfully." -ForegroundColor Green
    Write-Host "To activate the environment, run: conda activate $EnvName"
} else {
    Write-Error "Package installation failed."
}
