Write-Host "Building python-version-manager executable..."

# Set production mode (INFO level logging), 1 for development (DEBUG level logging)
$env:PVM_DEV = "0"

# Version from CI (fallback for local builds)
# during CI, version is exposed by github as github.ref_name instead

if (-not $env:PVM_VERSION) {
    $env:PVM_VERSION = "dev"
}

"VERSION = `"$env:PVM_VERSION`"" | Set-Content src/_version.py

Write-Host "Building version $($env:PVM_VERSION)"
uv run -m PyInstaller --onefile --clean --exclude-module tests --name pvm main.py
