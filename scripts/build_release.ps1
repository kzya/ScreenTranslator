param(
    [string]$PythonLauncher = "py -3.11",
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
Set-Location $repoRoot

Write-Host "==> Repo root: $repoRoot"

if (-not $SkipTests) {
    Write-Host "==> Running tests"
    & powershell -NoProfile -Command "$PythonLauncher -m unittest discover -s tests -v"
}

Write-Host "==> Cleaning old build artifacts"
Remove-Item build, dist, release -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path release -Force | Out-Null

Write-Host "==> Building exe with PyInstaller"
& powershell -NoProfile -Command "$PythonLauncher -m PyInstaller build.spec --clean --noconfirm"

$distPath = Join-Path $repoRoot "dist\ScreenTranslator"
$zipPath = Join-Path $repoRoot "release\ScreenTranslator-win-x64.zip"

if (-not (Test-Path $distPath)) {
    throw "Build output not found: $distPath"
}

Write-Host "==> Creating release zip"
Compress-Archive -Path (Join-Path $distPath "*") -DestinationPath $zipPath -Force

Write-Host "==> Done"
Write-Host "Release archive: $zipPath"
