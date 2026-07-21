# Mars Cost Router — animated explainer

A local, dependency-light, frame-addressable 3:00 presentation. It uses the
project's existing SVG assets and the approved script, shot list, captions, and
evidence wording. Nothing is fetched from the network.

## Requirements

- Windows PowerShell 5.1+
- Node.js 24+ (static verification and the dependency-free CDP frame capture)
- Microsoft Edge or Google Chrome (headless frame capture)
- FFmpeg on `PATH` (encoding and optional audio/subtitle muxing)
- The installed Windows desktop voice **Microsoft Zira Desktop** (local
  `System.Speech`; no cloud voice service)

## Preview

Open `index.html` in a browser, or use a local static server. Add
`?frame=3000` to inspect an exact frame; render time is always `frame / 30`.
`?clean=1` hides the safe-area and timecode preview guides.

Every visual motion state is calculated from the requested frame, not from
wall-clock CSS animation. For deterministic browser automation, the page also
exposes `window.setFrame(frameNumber)`.

## Sparse capture regression smoke test

```powershell
powershell -ExecutionPolicy Bypass -File .\smoke.ps1
```

This starts one browser and captures frames `123`, `127`, `300`, `1350`, `3150`, `4350`, and `4950`
without rendering the intervening frames. The CDP renderer asserts the requested
frame identity, clock, and chapter before each screenshot, then fails if the PNG hashes
are all equal. Captures are kept in ignored `sparse-smoke/` for inspection.
It also checks the centered caption and main scene viewport bounds at every
requested frame (2 px tolerance); the selected frames cover the long captions
at 10, 45, 105, 145, and 165 seconds.

## GPU capture and encoding

GPU compositing is the default for frame capture. The persistent Chromium launch
uses conservative Windows ANGLE/D3D11 and GPU-rasterization flags, while each
CDP PNG request uses `optimizeForSpeed: true`; frame addressing and PNG output
remain unchanged. Use the explicit CPU fallback only when a driver/browser
problem requires it:

```powershell
powershell -ExecutionPolicy Bypass -File .\render.ps1 -SoftwareCapture
```

Run the representative 60-frame GPU-versus-software benchmark without making a
video:

```powershell
powershell -ExecutionPolicy Bypass -File .\benchmark.ps1
```

It captures a contiguous mid-film range into ignored `benchmark-gpu/` and
`benchmark-software/`, reports end-to-end frames per second, asserts the frame
states, and checks that captured PNG hashes are not all equal.

Final encoding defaults to `auto`: after PNG capture, `render.ps1` runs an
actual one-frame `h264_nvenc` encode probe. It selects NVENC only on success;
otherwise it retains `libx264`. Both paths produce 30 FPS `yuv420p` output. To
force a safe CPU encoder, use `-VideoEncoder libx264`; `-VideoEncoder nvenc`
fails closed if the hardware probe cannot pass.

Frame PNG reuse is source-bound. `capture.mjs` records a visual fingerprint for
the page, motion script, stylesheet, and presentation SVGs beside the frame
cache. A missing or mismatched fingerprint clears that cache before capture, so
stale frames cannot be mixed into a new render. Matching fingerprints continue
to support interrupted-render resume.

## Verify and render

```powershell
node verify.mjs
powershell -ExecutionPolicy Bypass -File .\render.ps1
```

`render.ps1` produces `out/mars-cost-router-explainer.mp4` at **1920×1080,
30 FPS, exactly 180 seconds**. It keeps one headless Edge/Chrome process alive,
uses Node's built-in Chrome DevTools Protocol client to set every exact frame
and capture its PNG, then encodes with FFmpeg. No npm package, remote service,
or network asset is used. The default video has no audio track.

Useful render options:

```powershell
# Quick persistent-browser visual smoke render
powershell -ExecutionPolicy Bypass -File .\render.ps1 -StartFrame 3600 -EndFrame 3630 -Output out\smoke.mp4

# Full render with the locally generated audio and approved subtitles
powershell -ExecutionPolicy Bypass -File .\render.ps1 -Narration inputs\narration.wav -BackgroundAudio inputs\background.wav -Subtitles
```

## Audio and subtitle contract

### Generate the local audio inputs

```powershell
powershell -ExecutionPolicy Bypass -File .\audio.ps1
# or: npm run audio
```

`audio.ps1` reads the ten exact cue texts and boundaries from
`../demo/CAPTIONS.vtt`, verifies every cue is an exact substring of the
approved `../demo/VIDEO_SCRIPT.md`, then speaks each cue separately using the
installed local **Microsoft Zira Desktop** voice. Each cue is paced only with
FFmpeg `atempo` stages between `0.5` and `2.0`, then padded or trimmed to its
approved boundary: `0/15/35/55/75/100/120/140/160/170/180`. It writes ignored,
48 kHz stereo PCM WAV files to `inputs/narration.wav` and
`inputs/background.wav`, and fails if FFprobe does not report exact 180.000 s,
stereo, and 48 kHz for both outputs.

The background is original deterministic procedural audio generated locally by
FFmpeg: low sine-based drone layers, filtered pink-noise “dust,” and subtle
non-melodic changes at approved chapter boundaries. It has no external media,
vocals, sampled material, or copyrighted melody, and is limited for narration
headroom. The local Zira desktop voice and this generated bed are the complete
audio provenance.

- `inputs/narration.wav` begins at 00:00:00 and contains the exact approved
  narration cue copy.
- `inputs/background.wav` begins at 00:00:00 and is exactly 180 seconds.
- `-Subtitles` muxes the unchanged `../demo/CAPTIONS.vtt` as a selectable
  subtitle track. The visual captions in the animation use that same approved
  cue text. No captions are burned in by default.

The renderer intentionally types installation commands without showing output:
this avoids fabricated results and personal or local paths. The payload is
explicitly labeled a *requested* shape, not effective-routing evidence.

## Files

- `index.html`, `styles.css`, `app.js` — the presentation
- `render.ps1` — Windows frame renderer, encoder, and audio/subtitle hooks
- `capture.mjs` — built-in Node CDP client; one persistent browser per render
- `smoke.ps1` — sparse frame/clock/chapter/hash regression test
- `benchmark.ps1` — GPU versus software capture benchmark
- `audio.ps1` — local Zira narration, procedural ambient bed, and FFprobe gate
- `verify.mjs` — static timing, source, and claim-boundary checks
- `package.json` — convenience scripts; no dependencies

`out/`, `frames/`, and `inputs/` are local render artifacts and are ignored by
the included `.gitignore`.
