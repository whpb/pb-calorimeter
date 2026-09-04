<#
Builds build\PBCal.msix from the Nuitka standalone dist folder.
Run from anywhere; every path resolves relative to the repo root via $PSScriptRoot.

Usage:
  .\packaging\build_msix.ps1                                  # rebuild + pack, unsigned
  .\packaging\build_msix.ps1 -SkipBuild                        # pack the existing dist folder only
  .\packaging\build_msix.ps1 -CertPath packaging\PBCal.pfx -CertPassword <pw>
#>
param(
    [switch]$SkipBuild,
    [string]$Version = "1.0.0.0",
    [string]$CertPath,
    [string]$CertPassword
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path "$PSScriptRoot\.."
$distDir = Join-Path $repoRoot "build\launcher.dist"
$outputMsix = Join-Path $repoRoot "build\PBCal.msix"

function Find-SdkTool([string]$Name) {
    $tool = Get-ChildItem "C:\Program Files (x86)\Windows Kits\10\bin\*\x64\$Name" -ErrorAction SilentlyContinue |
        Sort-Object FullName -Descending | Select-Object -First 1
    if (-not $tool) { throw "$Name not found - install the Windows 11 SDK" }
    return $tool.FullName
}

if (-not $SkipBuild) {
    Write-Host "Building standalone app with Nuitka..."
    Push-Location $repoRoot
    try {
        poetry run python -m nuitka launcher.py `
            --standalone --assume-yes-for-downloads `
            --output-dir=build --output-filename=PBCal.exe `
            --windows-console-mode=hide `
            --windows-icon-from-ico=assets/polarbear-logo.png `
            --enable-plugin=tk-inter --enable-plugin=matplotlib `
            --include-module=app --include-module=main `
            --include-module=force_run --include-module=reanalyse `
            --include-package=functions --include-package=pymodbus `
            --include-data-dir=assets=assets `
            --include-data-files=settings.default.json=settings.default.json `
            --include-data-files=pb_cooling_capacity.csv=pb_cooling_capacity.csv `
            --include-data-files=report_template.typ=report_template.typ `
            --include-data-files=README.md=README.md
        if ($LASTEXITCODE -ne 0) { throw "Nuitka build failed" }
    } finally { Pop-Location }
}

Write-Host "Generating MSIX logo assets..."
Push-Location $repoRoot
try {
    poetry run python packaging/generate_logos.py
    if ($LASTEXITCODE -ne 0) { throw "Logo generation failed" }
} finally { Pop-Location }

Write-Host "Writing manifest (version $Version)..."
$manifest = Get-Content (Join-Path $repoRoot "packaging\AppxManifest.xml") -Raw
$manifest = $manifest -creplace 'Version="[\d.]+"', "Version=`"$Version`""
Set-Content -Path (Join-Path $distDir "AppxManifest.xml") -Value $manifest -NoNewline

Write-Host "Packing MSIX..."
$makeappx = Find-SdkTool "makeappx.exe"
& $makeappx pack /d $distDir /p $outputMsix /o
if ($LASTEXITCODE -ne 0) { throw "makeappx failed" }

if ($CertPath) {
    Write-Host "Signing package..."
    $signtool = Find-SdkTool "signtool.exe"
    & $signtool sign /fd SHA256 /a /f $CertPath /p $CertPassword $outputMsix
    if ($LASTEXITCODE -ne 0) { throw "signtool failed" }
    Write-Host "Signed: $outputMsix"
} else {
    Write-Host "No -CertPath given - $outputMsix is unsigned and will not install." -ForegroundColor Yellow
    Write-Host "Run packaging\New-SigningCert.ps1 once, then pass -CertPath/-CertPassword." -ForegroundColor Yellow
}
