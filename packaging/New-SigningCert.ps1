<#
One-time setup: creates a self-signed code-signing certificate for PBCal MSIX packages
and exports it to a .pfx (private key, for build_msix.ps1) and a .cer (public key, for
trusting the package on other machines). -Subject must match AppxManifest.xml's
Publisher field exactly, and should stay the same across rebuilds - a signing identity
that changes invalidates trust already granted on install targets.

Usage:
  .\packaging\New-SigningCert.ps1 -Password <pw>
#>
param(
    [string]$Subject = "CN=Cambridge Reactor Design",
    [string]$OutFile = "$PSScriptRoot\PBCal.pfx",
    [Parameter(Mandatory)][string]$Password
)

$ErrorActionPreference = "Stop"
$securePassword = ConvertTo-SecureString -String $Password -Force -AsPlainText

$cert = New-SelfSignedCertificate -Type Custom -Subject $Subject `
    -KeyUsage DigitalSignature -FriendlyName "PBCal MSIX signing" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

Export-PfxCertificate -Cert $cert -FilePath $OutFile -Password $securePassword | Out-Null
$cerFile = [System.IO.Path]::ChangeExtension($OutFile, "cer")
Export-Certificate -Cert $cert -FilePath $cerFile | Out-Null

Write-Host "Private key (keep secret): $OutFile"
Write-Host "Public certificate (distribute): $cerFile"
Write-Host ""
Write-Host "To trust the package on an install target, run there as admin:"
Write-Host "  Import-Certificate -FilePath <path to $cerFile> -CertStoreLocation Cert:\LocalMachine\TrustedPeople"
