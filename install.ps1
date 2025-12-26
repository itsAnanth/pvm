# PVM Installer for Windows
# Downloads pvm.exe and adds it to user PATH

$url = "https://github.com/itsAnanth/pvm/releases/download/v1.0.0/pvm.exe"
$installDir = "$env:LOCALAPPDATA\.pvm"
$exePath = "$installDir\pvm.exe"

Write-Host "Installing PVM (Python Version Manager)..." -ForegroundColor Cyan

# Create installation directory
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Host "Created directory: $installDir" -ForegroundColor Green
}

# Download pvm.exe
Write-Host "Downloading pvm.exe from $url..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri $url -OutFile $exePath -UseBasicParsing
    Write-Host "Downloaded successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to download: $_" -ForegroundColor Red
    exit 1
}

$olduserpath = [Environment]::GetEnvironmentVariable("Path", "User")

$existingPaths = @()
if (-not [string]::IsNullOrEmpty($olduserpath)) {
    $existingPaths = $olduserpath -split ';'
}

$pathstoadd = @($installDir)

$newPaths = @($existingPaths)

foreach ($pathtoadd in $pathstoadd) {
    if (-not ($newPaths | Where-Object { $_.TrimEnd('\') -ieq $pathtoadd.TrimEnd('\') })) {
        $newPaths += $pathtoadd
    }
}

$newuserpath = ($newPaths -join ';')

if ([string]::IsNullOrEmpty($newuserpath)) {
    Write-Error "New PATH is empty - aborting to prevent damage" -ForegroundColor Red
    exit 1
}

# Backup existing PATH
$olduserpath | Out-File (Join-Path $PSScriptRoot "path_backup.txt")


$confirmation = Read-Host "Do you want to set the new Path as:`n$newuserpath`n(y/n)" -ForegroundColor Yellow
if ($confirmation -ne "y") {
    Write-Host "Operation cancelled by user." -ForegroundColor Red
    exit 0
}

[Environment]::SetEnvironmentVariable("Path", $newuserpath, "User")
Write-Host "PVM installed and added to PATH successfully." -ForegroundColor Green

Write-Host "`nInstallation complete! Run 'pvm' to get started." -ForegroundColor Cyan