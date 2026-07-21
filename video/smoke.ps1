[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$browserCandidates = @(
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
if (!$browserCandidates) { throw 'Microsoft Edge or Google Chrome is required for the sparse capture smoke test.' }
$frames = Join-Path $root 'sparse-smoke'
if (Test-Path -LiteralPath $frames) { Remove-Item -LiteralPath $frames -Recurse -Force }
& node (Join-Path $root 'verify.mjs')
if ($LASTEXITCODE -ne 0) { throw 'Static verification failed.' }
& node (Join-Path $root 'capture.mjs') --browser $browserCandidates[0] --frame-list '123,127,300,1350,3150,4350,4950' --frames $frames --verify-distinct
if ($LASTEXITCODE -ne 0) { throw 'Sparse capture smoke test failed.' }
Write-Host "PASS: sparse frame states and distinct PNG hashes verified in $frames"
