[CmdletBinding()]
param(
  [int]$StartFrame = 0,
  [int]$EndFrame = 4199,
  [string]$Output = "out\mars-cost-router-explainer.mp4",
  [string]$Narration,
  [string]$BackgroundAudio,
  [switch]$Subtitles,
  [switch]$KeepFrames,
  [switch]$SoftwareCapture,
  [ValidateSet('auto', 'libx264', 'nvenc')]
  [string]$VideoEncoder = 'auto'
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$fps = 30
$lastFrame = 4199
if ($StartFrame -lt 0 -or $EndFrame -gt $lastFrame -or $EndFrame -lt $StartFrame) { throw "Frame range must be within 0..$lastFrame." }
& node (Join-Path $root 'verify.mjs')
if ($LASTEXITCODE -ne 0) { throw 'Static verification failed.' }

$browserCandidates = @(
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
if (!$browserCandidates) { throw 'Microsoft Edge or Google Chrome is required for headless frame capture.' }
$browser = $browserCandidates[0]
if (!(Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw 'FFmpeg must be available on PATH.' }

$frames = Join-Path $root 'frames'
$outPath = if ([IO.Path]::IsPathRooted($Output)) { $Output } else { Join-Path $root $Output }
$outDir = Split-Path -Parent $outPath
if (!(Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
if (!(Test-Path -LiteralPath $frames)) { New-Item -ItemType Directory -Path $frames | Out-Null }
Write-Host "Capturing frames $StartFrame through $EndFrame at 1920x1080 / 30 FPS with one persistent browser..."
$captureArgs = @((Join-Path $root 'capture.mjs'), '--browser', $browser, '--start', $StartFrame, '--end', $EndFrame, '--frames', $frames)
if ($SoftwareCapture) { $captureArgs += '--software' }
& node @captureArgs
if ($LASTEXITCODE -ne 0) { throw 'Persistent browser capture failed.' }

$frameCount = $EndFrame - $StartFrame + 1
$seconds = $frameCount / $fps
$imagePattern = Join-Path $frames 'frame%05d.png'
$ff = @('-y','-framerate',$fps,'-start_number',$StartFrame,'-i',$imagePattern)
$audioInputs = @()
if ($Narration) {
  if (!(Test-Path -LiteralPath $Narration)) { throw "Narration file was not found: $Narration" }
  $ff += @('-i',(Resolve-Path -LiteralPath $Narration)); $audioInputs += 'narration'
}
if ($BackgroundAudio) {
  if (!(Test-Path -LiteralPath $BackgroundAudio)) { throw "Background audio file was not found: $BackgroundAudio" }
  $ff += @('-stream_loop','-1','-i',(Resolve-Path -LiteralPath $BackgroundAudio)); $audioInputs += 'background'
}
if ($Subtitles) { $ff += @('-i',(Join-Path $root '..\demo\CAPTIONS.vtt')) }
function Test-Nvenc([string]$Pattern, [int]$ProbeStart) {
  $encoders = (& ffmpeg -hide_banner -encoders 2>&1) -join "`n"
  if ($encoders -notmatch '\bh264_nvenc\b') { return $false }
  $probe = Join-Path $root 'out\nvenc-probe.mp4'
  try {
    & ffmpeg -y -v error -framerate $fps -start_number $ProbeStart -i $Pattern -frames:v 1 -c:v h264_nvenc -preset p6 -tune hq -rc:v vbr -cq:v 19 -b:v 0 -pix_fmt yuv420p $probe
    return ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $probe))
  } finally {
    if (Test-Path -LiteralPath $probe) { Remove-Item -LiteralPath $probe -Force }
  }
}
$useNvenc = $false
if ($VideoEncoder -ne 'libx264') { $useNvenc = Test-Nvenc $imagePattern $StartFrame }
if ($VideoEncoder -eq 'nvenc' -and !$useNvenc) { throw 'Requested h264_nvenc, but the actual one-frame hardware encode probe failed.' }
if ($useNvenc) { Write-Host 'Using h264_nvenc after a successful one-frame hardware probe.'; $ff += @('-frames:v',$frameCount,'-map','0:v:0','-c:v','h264_nvenc','-preset','p6','-tune','hq','-rc:v','vbr','-cq:v','19','-b:v','0','-pix_fmt','yuv420p','-r',$fps) }
else { Write-Host 'Using libx264 (NVENC unavailable or probe failed).'; $ff += @('-frames:v',$frameCount,'-map','0:v:0','-c:v','libx264','-pix_fmt','yuv420p','-r',$fps) }
if ($audioInputs.Count -eq 1 -and $audioInputs[0] -eq 'narration') { $ff += @('-map','1:a:0','-c:a','aac','-af',"atrim=0:$seconds") }
elseif ($audioInputs.Count -eq 1) { $ff += @('-map','1:a:0','-c:a','aac','-af',"atrim=0:$seconds,volume=0.16") }
elseif ($audioInputs.Count -eq 2) { $ff += @('-filter_complex',"[1:a]atrim=0:$seconds[n];[2:a]atrim=0:$seconds,volume=0.16[b];[n][b]amix=inputs=2:duration=first:normalize=0[a]",'-map','[a]','-c:a','aac') }
if ($Subtitles) { $subtitleInput = 1 + $audioInputs.Count; $ff += @('-map',"$subtitleInput`:s:0",'-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata:s:s:0','title=Approved captions') }
$ff += @('-t',$seconds,'-movflags','+faststart',$outPath)
Write-Host "Encoding $seconds seconds to $outPath..."
& ffmpeg @ff
if ($LASTEXITCODE -ne 0) { throw 'FFmpeg encoding failed.' }
if (!$KeepFrames) { Remove-Item -LiteralPath $frames -Recurse -Force }
Write-Host "Done: $outPath"
