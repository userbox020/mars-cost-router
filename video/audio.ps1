[CmdletBinding()]
param(
  [string]$VoiceName = 'Microsoft Zira Desktop',
  [switch]$KeepWork
)

# Creates local-only narration and an original procedural ambient bed.
# Narration text and timing are read from the approved demo captions, then
# checked against the approved narration script before any audio is generated.
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$captionsPath = Join-Path $root '..\demo\CAPTIONS.vtt'
$scriptPath = Join-Path $root '..\demo\VIDEO_SCRIPT.md'
$inputs = Join-Path $root 'inputs'
$work = Join-Path $root 'audio-work'
$sampleRate = 48000
$totalSeconds = 140.0

function Get-AudioProbe([string]$Path) {
  $json = & ffprobe -v error -select_streams a:0 -show_entries stream=codec_type,sample_rate,channels:format=duration -of json $Path
  if ($LASTEXITCODE -ne 0) { throw "ffprobe failed for $Path." }
  $probe = $json | ConvertFrom-Json
  if (!$probe.streams -or $probe.streams.Count -ne 1) { throw "Expected one audio stream in $Path." }
  [pscustomobject]@{ Duration = [double]$probe.format.duration; SampleRate = [int]$probe.streams[0].sample_rate; Channels = [int]$probe.streams[0].channels; CodecType = $probe.streams[0].codec_type }
}

function Assert-Audio([string]$Path, [double]$ExpectedDuration, [string]$Label) {
  $p = Get-AudioProbe $Path
  if ($p.CodecType -ne 'audio' -or $p.SampleRate -ne $sampleRate -or $p.Channels -ne 2) { throw "$Label must be stereo $sampleRate Hz audio; got $($p.Channels) channels at $($p.SampleRate) Hz." }
  if ([math]::Abs($p.Duration - $ExpectedDuration) -gt 0.001) { throw "$Label must be $ExpectedDuration seconds; ffprobe reported $($p.Duration)." }
  return $p
}

function Get-AtempoChain([double]$Factor) {
  if ($Factor -le 0) { throw 'Narration source duration must be positive.' }
  $filters = @()
  while ($Factor -gt 2.0) { $filters += 'atempo=2.0'; $Factor /= 2.0 }
  while ($Factor -lt 0.5) { $filters += 'atempo=0.5'; $Factor /= 0.5 }
  # Each atempo stage stays inside FFmpeg's documented 0.5–2.0 safe range.
  $filters += ('atempo={0:F8}' -f $Factor).Replace(',', '.')
  return ($filters -join ',')
}

function Get-Cues {
  $vtt = [IO.File]::ReadAllText($captionsPath, [Text.Encoding]::UTF8)
  $approvedScript = [IO.File]::ReadAllText($scriptPath, [Text.Encoding]::UTF8)
  $matches = [regex]::Matches($vtt, '(?m)^(\d\d):(\d\d):(\d\d)\.\d{3}\s+-->\s+(\d\d):(\d\d):(\d\d)\.\d{3}\r?\n([^\r\n]+)$')
  if ($matches.Count -ne 10) { throw "Expected 10 approved caption cues; found $($matches.Count)." }
  $cues = @()
  $expectedStart = 0.0
  foreach ($match in $matches) {
    $start = [int]$match.Groups[1].Value * 3600 + [int]$match.Groups[2].Value * 60 + [int]$match.Groups[3].Value
    $end = [int]$match.Groups[4].Value * 3600 + [int]$match.Groups[5].Value * 60 + [int]$match.Groups[6].Value
    $text = $match.Groups[7].Value
    if ($start -ne $expectedStart -or $end -le $start) { throw "Caption boundaries are not contiguous at $text" }
    if (!$approvedScript.Contains($text)) { throw "Caption text is not an exact approved narration-script substring: $text" }
    $cues += [pscustomobject]@{ Start = [double]$start; End = [double]$end; Duration = [double]($end - $start); Text = $text }
    $expectedStart = $end
  }
  if ($expectedStart -ne $totalSeconds) { throw "Approved cues must end at $totalSeconds seconds; ended at $expectedStart." }
  return $cues
}

if (!(Get-Command ffmpeg -ErrorAction SilentlyContinue) -or !(Get-Command ffprobe -ErrorAction SilentlyContinue)) { throw 'FFmpeg and ffprobe must be available on PATH.' }
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$availableVoices = @($speaker.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name })
if ($availableVoices -notcontains $VoiceName) { throw "Required local voice '$VoiceName' is unavailable. Installed voices: $($availableVoices -join ', ')" }
$speaker.SelectVoice($VoiceName)
$speaker.Rate = -2
$cues = Get-Cues

if (!(Test-Path -LiteralPath $inputs)) { New-Item -ItemType Directory -Path $inputs | Out-Null }
if (Test-Path -LiteralPath $work) { Remove-Item -LiteralPath $work -Recurse -Force }
New-Item -ItemType Directory -Path $work | Out-Null

try {
  $cueFiles = @()
  for ($i = 0; $i -lt $cues.Count; $i++) {
    $cue = $cues[$i]
    $raw = Join-Path $work ("raw-{0:D2}.wav" -f ($i + 1))
    $paced = Join-Path $work ("cue-{0:D2}.wav" -f ($i + 1))
    Write-Host ("Narrating cue {0}/10: {1:N0}-{2:N0} seconds" -f ($i + 1), $cue.Start, $cue.End)
    $speaker.SetOutputToWaveFile($raw)
    $speaker.Speak($cue.Text)
    $speaker.SetOutputToNull()
    $rawProbe = Get-AudioProbe $raw
    $tempo = $rawProbe.Duration / $cue.Duration
    $chain = Get-AtempoChain $tempo
    & ffmpeg -y -i $raw -af "$chain,apad=pad_dur=$($cue.Duration),atrim=0:$($cue.Duration),asetpts=N/SR/TB" -ar $sampleRate -ac 2 -c:a pcm_s16le -t $cue.Duration $paced
    if ($LASTEXITCODE -ne 0) { throw "FFmpeg pacing failed for cue $($i + 1)." }
    Assert-Audio $paced $cue.Duration ("Cue $($i + 1)") | Out-Null
    $cueFiles += $paced
  }

  $concatList = Join-Path $work 'concat.txt'
  $concatEntries = foreach ($cueFile in $cueFiles) { "file '$cueFile'" }
  [IO.File]::WriteAllLines($concatList, $concatEntries, [Text.Encoding]::ASCII)
  $narration = Join-Path $inputs 'narration.wav'
  & ffmpeg -y -f concat -safe 0 -i $concatList -af "atrim=0:$totalSeconds,asetpts=N/SR/TB" -ar $sampleRate -ac 2 -c:a pcm_s16le -t $totalSeconds $narration
  if ($LASTEXITCODE -ne 0) { throw 'FFmpeg narration assembly failed.' }
  Assert-Audio $narration $totalSeconds 'Narration' | Out-Null

  # Original procedural atmosphere: deterministic low-frequency dunes, filtered
  # pink dust, and non-melodic chapter shifts at the approved cue transitions.
  $left = '0.026*sin(2*PI*55*t)+0.012*sin(2*PI*82.5*t)+0.006*sin(2*PI*(110+0.35*sin(2*PI*t/47))*t)+0.004*sin(2*PI*220*t)*(0.5+0.5*sin(2*PI*t/13))+0.005*(between(t,12,27)*sin(2*PI*61*t)+between(t,43,58)*sin(2*PI*73*t)+between(t,78,94)*sin(2*PI*65*t)+between(t,110,126)*sin(2*PI*69*t)+between(t,133,140)*sin(2*PI*58*t))'
  $right = '0.025*sin(2*PI*55*t+0.17)+0.011*sin(2*PI*82.5*t+0.41)+0.006*sin(2*PI*(110+0.31*sin(2*PI*t/53))*t+0.27)+0.004*sin(2*PI*220*t+0.5)*(0.5+0.5*sin(2*PI*t/17))+0.005*(between(t,12,27)*sin(2*PI*61*t+0.3)+between(t,43,58)*sin(2*PI*73*t+0.5)+between(t,78,94)*sin(2*PI*65*t+0.2)+between(t,110,126)*sin(2*PI*69*t+0.7)+between(t,133,140)*sin(2*PI*58*t+0.4))'
  $bedSource = "aevalsrc=exprs='${left}|${right}':s=${sampleRate}:d=${totalSeconds}"
  $background = Join-Path $inputs 'background.wav'
  & ffmpeg -y -f lavfi -i $bedSource -f lavfi -i "anoisesrc=color=pink:sample_rate=${sampleRate}:duration=${totalSeconds}:seed=1976" -filter_complex '[1:a]lowpass=f=900,highpass=f=70,volume=0.018[dust];[0:a][dust]amix=inputs=2:normalize=0,afade=t=in:st=0:d=3,afade=t=out:st=137:d=3,alimiter=limit=0.20,aformat=sample_rates=48000:channel_layouts=stereo' -ar $sampleRate -ac 2 -c:a pcm_s16le -t $totalSeconds $background
  if ($LASTEXITCODE -ne 0) { throw 'FFmpeg procedural background generation failed.' }
  Assert-Audio $background $totalSeconds 'Background audio' | Out-Null
  Write-Host "PASS: exact approved cue boundaries assembled; narration.wav and background.wav are stereo $sampleRate Hz, 140.000 seconds."
}
finally {
  $speaker.Dispose()
  if (!$KeepWork -and (Test-Path -LiteralPath $work)) { Remove-Item -LiteralPath $work -Recurse -Force }
}
