# Packaging the app

To package, run from the project root:

`packaging\build_msix.ps1 -CertPath packaging\CRD.pfx -CertPassword X -Version X.X.X.X`

Replace X as required.

Notes:

- pw is standard
- when updating, version must be higher than previous or installation will fail
- distribute certificate (.cer) with app first time; no need to repeat when updating