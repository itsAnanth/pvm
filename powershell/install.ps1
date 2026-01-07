# PVM Installer for Windows
# Downloads pvm.exe and adds it to user PATH

# Fetch latest release from GitHub API
Write-Host "Fetching latest release information..." -ForegroundColor Yellow
try {
    $apiUrl = "https://api.github.com/repos/itsAnanth/pvm/releases/latest"
    $releaseInfo = Invoke-RestMethod -Uri $apiUrl -UseBasicParsing
    $version = $releaseInfo.tag_name
    
    # Find the pvm.exe asset
    $asset = $releaseInfo.assets | Where-Object { $_.name -eq "pvm.exe" }
    if (-not $asset) {
        throw "pvm.exe not found in latest release assets"
    }
    
    $url = $asset.browser_download_url
    Write-Host "Latest version: $version" -ForegroundColor Green
} catch {
    Write-Host "Failed to fetch latest release info: $_" -ForegroundColor Red
    exit 1
}

$installDir = "$env:LOCALAPPDATA\.pvm"
$exePath = "$installDir\pvm.exe"

Write-Host "Installing PVM..." -ForegroundColor Cyan

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
    $existingPaths = ($olduserpath -split ';') | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
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
$olduserpath | Out-File (Join-Path $installDir "path_backup.txt")


# Write-Host "Do you want to set the new Path as:" -ForegroundColor Yellow
# Write-Host "$newuserpath" -ForegroundColor Cyan
# Write-Host "(y/n): " -ForegroundColor Yellow -NoNewline
# $confirmation = Read-Host
# if ($confirmation -ne "y") {
#     Write-Host "Operation cancelled by user." -ForegroundColor Red
#     exit 0
# }

[Environment]::SetEnvironmentVariable("Path", $newuserpath, "User")

Write-Host "PVM installed and added to PATH successfully." -ForegroundColor Green
Write-Host "`nInstallation complete! PVM $version installed. Restart your terminal and run 'pvm' to get started." -ForegroundColor Cyan
