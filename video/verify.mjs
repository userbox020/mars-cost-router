import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)));
const read = path => readFileSync(resolve(root, path), 'utf8');
const app = read('app.js');
const capture = read('capture.mjs');
const render = read('render.ps1');
const captions = read('../demo/CAPTIONS.vtt');
const script = read('../demo/VIDEO_SCRIPT.md');
const shotList = read('../demo/SHOT_LIST.md');
const required = [
  '../assets/brand/mars-cost-router-hero.svg',
  '../assets/diagrams/delegation-flow.svg',
  '../assets/evidence/fixed-v1.2-performance.svg',
  '../assets/evidence/rate-index.svg',
  '../demo/CAPTIONS.vtt', '../demo/VIDEO_SCRIPT.md', '../demo/SHOT_LIST.md', '../docs/EVIDENCE.md'
];
for (const file of required) if (!existsSync(resolve(root, file))) throw new Error(`Missing approved source: ${file}`);
const cues = [...captions.matchAll(/(\d\d):(\d\d):(\d\d)\.\d{3} --> (\d\d):(\d\d):(\d\d)\.\d{3}\r?\n([^\r\n]+)/g)];
if (cues.length !== 10) throw new Error(`Expected 10 caption cues, found ${cues.length}.`);
const appCues = [...app.matchAll(/^\s*\[(\d+),(\d+),"([^"]+)"\],?$/gm)];
const scriptCues = [...script.matchAll(/^\| ([0-9:]+)–([0-9:]+) \| \d+s \| “([^”]+)” \|$/gm)];
if (appCues.length !== 10 || scriptCues.length !== 10) throw new Error(`Expected 10 app and script cues, found ${appCues.length} and ${scriptCues.length}.`);
const seconds = ([h,m,s]) => +h * 3600 + +m * 60 + +s;
const shortSeconds = value => value.split(':').reduce((total, part) => total * 60 + Number(part), 0);
let end = 0;
for (const [index, cue] of cues.entries()) {
  const start = seconds(cue.slice(1,4)), finish = seconds(cue.slice(4,7)), text = cue[7];
  if (start !== end) throw new Error(`Caption gap or overlap at ${text}`);
  const appCue = appCues[index], scriptCue = scriptCues[index];
  if (+appCue[1] !== start || +appCue[2] !== finish || appCue[3] !== text) throw new Error(`Caption cue ${index + 1} is not exact in app.js.`);
  if (shortSeconds(scriptCue[1]) !== start || shortSeconds(scriptCue[2]) !== finish || scriptCue[3] !== text) throw new Error(`Caption cue ${index + 1} is not exact in VIDEO_SCRIPT.md.`);
  end = finish;
}
const boundaries = [0,12,27,43,58,78,94,110,126,133,140];
if (end !== 140) throw new Error(`Caption duration must end at 140 seconds, got ${end}.`);
if (cues.some((cue, index) => seconds(cue.slice(1,4)) !== boundaries[index] || seconds(cue.slice(4,7)) !== boundaries[index + 1])) throw new Error('Caption cues do not match the approved 2:20 boundaries.');
const synchronizedVideoSources = { app, captions, script };
for (const phrase of [
  'Delegation should be deliberate',
  'guides explicit model, effort, and context choices',
  'calls for bounded child tasks',
  'independent, unofficial delegation policy',
  'requested model lanes',
  'instruction-only and fully inspectable',
  'guides the root to request explicit child settings',
  'Each lane template calls for',
  'privacy-safe task label',
  'requested route intent stays visible for review',
  'root-owned verification',
  'final verification',
  'Remote installation succeeded',
  'hosted CI passes',
  'twelve of twelve deterministic checks',
  'zero observed automatic retries and reroutes',
  '356,116',
  '356,494',
  'minus 0.11 percent',
  'Using the dated Standard API listed rates',
  'published comparison indexes Terra at 50 and Sol at 100',
  'Terra at 50',
  'Sol at 100',
  'fixed-series record and dated rate comparison separate',
  'Requested settings stay explicit and reviewable',
  'See Evidence for scope and methodology'
]) {
  for (const [sourceName, source] of Object.entries(synchronizedVideoSources)) {
    if (!source.toLowerCase().includes(phrase.toLowerCase())) throw new Error(`Required affirmative video phrase missing from ${sourceName}: ${phrase}`);
  }
}
const videoPresentation = [app, captions, script, shotList].join('\n');
for (const phrase of ['fixed-series observations', 'dated listed-rate index', 'Evidence link']) if (!shotList.toLowerCase().includes(phrase.toLowerCase())) throw new Error(`METHOD shot list must retain separate public-record framing: ${phrase}`);
for (const [label, pattern] of [
  ['optimized routing', /\boptimized routing\b/i],
  ['faster', /\bfaster\b/i],
  ['same/equal quality', /\b(?:same|equal)[ -]quality\b/i],
  ['equivalent quality', /\bequivalent[ -]quality\b/i],
  ['quality equivalence', /\bquality[ -]equivalence\b/i],
  ['quality retention', /\bquality[ -]retention\b/i],
  ['retains quality', /\bretains[ -]quality\b/i],
  ['quality-compromise claim', /\bwithout compromising[ -]quality\b/i],
  ['saves', /\bsav(?:e|es|ed|ing|ings)\b/i],
  ['guaranteed', /\bguaranteed\b/i],
  ['proven effective route', /\bproven effective route\b/i],
  ['effective routing verified', /\beffective routing verified\b/i],
  ['effective route confirmed', /\beffective route confirmed\b/i],
  ['effective model confirmed', /\beffective model confirmed\b/i],
  ['reduces tokens', /\breduces tokens\b/i],
  ['cuts tokens', /\bcuts tokens\b/i],
  ['lower latency', /\blower latency\b/i],
  ['improves latency', /\bimproves latency\b/i],
  ['half price', /\bhalf price\b/i],
  ['50% cheaper', /\b50\s*%\s*cheaper\b/i],
  ['lower cost', /\blower cost\b/i],
  ['lower bill', /\blower bill\b/i],
  ['cuts cost', /\bcuts cost\b/i],
  ['bill reduction', /\bbill reduction\b/i],
  ['billing savings', /\bbilling savings\b/i]
]) if (pattern.test(videoPresentation)) throw new Error(`Unsupported phrase found in video presentation sources: ${label}`);
const payloadSource = app.slice(app.indexOf('function payload()'), app.indexOf('function evidence()'));
if (!payloadSource.includes('Do not delegate or spawn another agent.')) throw new Error('Payload must retain the exact nested-delegation prohibition.');
if (!app.includes('4200') || !app.includes('duration = 140') || !app.includes('fps = 30')) throw new Error('Frame timing constants are missing.');
for (const phrase of ['window.setFrame', 'applyMotion', 'Page.captureScreenshot']) {
  const source = phrase === 'Page.captureScreenshot' ? capture : app;
  if (!source.includes(phrase)) throw new Error(`Frame-addressed motion/capture contract missing: ${phrase}`);
}
for (const phrase of ['currentFrame=normalizeFrame(Number(n))', 'String(currentFrame).padStart(4', 't=currentFrame/fps']) if (!app.replaceAll(' ', '').includes(phrase)) throw new Error(`Exact frame-identity contract missing: ${phrase}`);
if (app.includes('return {frame:Math.floor(t*fps)')) throw new Error('setFrame must not recompute integer identity from floating-point time.');
for (const phrase of ['captionMotion', 'translate(-50%,${y.toFixed(2)}px)', 'captionMotion(presence']) if (!app.includes(phrase)) throw new Error(`Centered caption-motion contract missing: ${phrase}`);
if (!app.includes('exit=c[1]===duration?1')) throw new Error('The final outro must remain visible through frame 4199.');
if (!capture.includes("'?frame=0&clean=1'")) throw new Error('Capture navigation must include frame=0 to disable wall-clock playback.');
if (capture.includes("href + '?clean=1'")) throw new Error('Capture navigation can re-enable wall-clock playback.');
for (const phrase of ['--frame-list', 'verify-distinct', 'state/bounds mismatch', 'all PNG hashes are equal']) if (!capture.includes(phrase)) throw new Error(`Sparse capture regression contract missing: ${phrase}`);
for (const phrase of ['getBoundingClientRect()', 'bounds:{caption,scene', 'visualFingerprint', 'Cleared stale frame cache']) if (!capture.includes(phrase)) throw new Error(`Viewport/cache safety contract missing: ${phrase}`);
if (!read('smoke.ps1').includes("'123,127,300,1350,3150,3540,3840,4050,4199'")) throw new Error('Sparse smoke must cover the recalculated long-caption and final-frame review points.');
for (const phrase of ['--enable-gpu-rasterization', '--use-angle=d3d11', 'optimizeForSpeed: true', '--software']) if (!capture.includes(phrase)) throw new Error(`GPU/software capture contract missing: ${phrase}`);
for (const phrase of ['tmpdir()', 'mars-cost-router-cdp-']) if (!capture.includes(phrase)) throw new Error(`Temporary browser-profile contract missing: ${phrase}`);
if (capture.includes("resolve(root, '.cdp-profile')")) throw new Error('Browser profiles must not be generated inside the public repository.');
for (const phrase of ['Test-Nvenc', 'h264_nvenc', 'Resolve-MediaInput', 'Join-Path $root $Path']) if (!render.includes(phrase)) throw new Error(`Render portability/encoding contract missing: ${phrase}`);
if (read('styles.css').includes('@keyframes') || read('styles.css').includes('animation:')) throw new Error('Wall-clock CSS animation is not allowed in frame-addressed rendering.');
const banned = /synthetic[ ,\-]+read(?:-| )only (?:tasks|series|workspace)/i;
for (const directory of [root, resolve(root, '../demo')]) {
  for (const entry of readdirSync(directory)) { const file = resolve(directory, entry); if (statSync(file).isFile() && /\.(?:md|vtt|js|mjs|ps1|html|json)$/i.test(file) && banned.test(readFileSync(file, 'utf8'))) throw new Error(`Forbidden synthetic wording found in owned file: ${file}`); }
}
console.log('PASS: 10 contiguous approved cues, 0:00–2:20 / 4,200 frames; deterministic GPU/software capture, NVENC probe, and sparse-state regression contracts present.');
