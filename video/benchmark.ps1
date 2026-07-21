[CmdletBinding()]
param(
  [int]$StartFrame = 1500,
  [int]$FrameCount = 60
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
if ($FrameCount -lt 2 -or $StartFrame -lt 0 -or ($StartFrame + $FrameCount - 1) -gt 4199) { throw 'Choose a contiguous benchmark range within 0..4199 with at least two frames.' }
$browserCandidates = @(
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
if (!$browserCandidates) { throw 'Microsoft Edge or Google Chrome is required for the capture benchmark.' }
& node (Join-Path $root 'verify.mjs')
if ($LASTEXITCODE -ne 0) { throw 'Static verification failed.' }
$endFrame = $StartFrame + $FrameCount - 1
foreach ($mode in @('gpu', 'software')) {
  $dir = Join-Path $root ("benchmark-" + $mode)
  if (Test-Path -LiteralPath $dir) { Remove-Item -LiteralPath $dir -Recurse -Force }
  $watch = [Diagnostics.Stopwatch]::StartNew()
  $captureArgs = @((Join-Path $root 'capture.mjs'), '--browser', $browserCandidates[0], '--start', $StartFrame, '--end', $endFrame, '--frames', $dir, '--verify-distinct')
  if ($mode -eq 'software') { $captureArgs += '--software' }
  & node @captureArgs
  if ($LASTEXITCODE -ne 0) { throw "$mode capture benchmark failed." }
  $watch.Stop()
  $fps = $FrameCount / $watch.Elapsed.TotalSeconds
  Write-Host ("BENCHMARK {0}: {1:N2} frames/sec ({2:N2}s for {3} frames)" -f $mode.ToUpperInvariant(), $fps, $watch.Elapsed.TotalSeconds, $FrameCount)
}
