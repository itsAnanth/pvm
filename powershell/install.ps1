# PVM Installer for Windows
# Downloads pvm.exe and adds it to user PATH

param(
    [switch]$Update
)

# Check for update flag from environment variable or parameter
$isUpdate = $Update -or ($env:PVM_UPDATE -eq '1')

$url = "https://github.com/itsAnanth/pvm/releases/download/v1.0.0/pvm.exe"
$installDir = "$env:LOCALAPPDATA\.pvm"
$exePath = "$installDir\pvm.exe"

if ($isUpdate -and (Test-Path $exePath)) {
    Write-Host "Updating existing PVM installation..." -ForegroundColor Cyan
} elseif (-not $isUpdate) {
    Write-Host "Fresh installation of PVM..." -ForegroundColor Cyan
}

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

if ($isUpdate) {
    Write-Host "PVM updated and PATH modified successfully." -ForegroundColor Green
    Write-Host "`nUpdation complete! run 'pvm' to get started." -ForegroundColor Cyan
} else {
    Write-Host "PVM installed and added to PATH successfully." -ForegroundColor Green
    Write-Host "`nInstallation complete! Restart your terminal and run 'pvm' to get started." -ForegroundColor Cyan

}
