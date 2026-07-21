import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)));
const read = path => readFileSync(resolve(root, path), 'utf8');
const app = read('app.js');
const capture = read('capture.mjs');
const captions = read('../demo/CAPTIONS.vtt');
const script = read('../demo/VIDEO_SCRIPT.md');
const shotList = read('../demo/SHOT_LIST.md');
const evidence = read('../docs/EVIDENCE.md');
const required = [
  '../assets/brand/mars-cost-router-hero.svg',
  '../assets/diagrams/delegation-flow.svg',
  '../assets/evidence/fixed-v1.2-performance.svg',
  '../demo/CAPTIONS.vtt', '../demo/VIDEO_SCRIPT.md', '../demo/SHOT_LIST.md', '../docs/EVIDENCE.md'
];
for (const file of required) if (!existsSync(resolve(root, file))) throw new Error(`Missing approved source: ${file}`);
const cues = [...captions.matchAll(/(\d\d):(\d\d):(\d\d)\.\d{3} --> (\d\d):(\d\d):(\d\d)\.\d{3}\r?\n([^\r\n]+)/g)];
if (cues.length !== 10) throw new Error(`Expected 10 caption cues, found ${cues.length}.`);
const seconds = ([h,m,s]) => +h * 3600 + +m * 60 + +s;
let end = 0;
for (const cue of cues) {
  const start = seconds(cue.slice(1,4)), finish = seconds(cue.slice(4,7)), text = cue[7];
  if (start !== end) throw new Error(`Caption gap or overlap at ${text}`);
  if (!app.includes(text)) throw new Error(`Caption copy is not exact in app.js: ${text}`);
  end = finish;
}
if (end !== 180) throw new Error(`Caption duration must end at 180 seconds, got ${end}.`);
for (const phrase of [
  'exact 3:00 narration', '180 seconds', 'descriptive', 'order- and cache-confounded',
  'not causal', 'not affiliated with or endorsed by OpenAI', 'not proof of the child’s effective route',
  '356,116', '356,494', '728,706', '768,912', '45.094', '53.328'
]) if (!(script + shotList + evidence + app).toLowerCase().includes(phrase.toLowerCase())) throw new Error(`Required source/claim phrase missing: ${phrase}`);
if (!app.includes('5400') || !app.includes('fps = 30')) throw new Error('Frame timing constants are missing.');
for (const phrase of ['window.setFrame', 'applyMotion', 'Page.captureScreenshot']) {
  const source = phrase === 'Page.captureScreenshot' ? capture : app;
  if (!source.includes(phrase)) throw new Error(`Frame-addressed motion/capture contract missing: ${phrase}`);
}
for (const phrase of ['currentFrame=requestedFrame', 'String(currentFrame).padStart(4', 't=currentFrame/fps']) if (!app.replaceAll(' ', '').includes(phrase)) throw new Error(`Exact frame-identity contract missing: ${phrase}`);
if (app.includes('return {frame:Math.floor(t*fps)')) throw new Error('setFrame must not recompute integer identity from floating-point time.');
for (const phrase of ['captionMotion', 'translate(-50%,${y.toFixed(2)}px)', 'captionMotion(presence']) if (!app.includes(phrase)) throw new Error(`Centered caption-motion contract missing: ${phrase}`);
if (!capture.includes("'?frame=0&clean=1'")) throw new Error('Capture navigation must include frame=0 to disable wall-clock playback.');
if (capture.includes("href + '?clean=1'")) throw new Error('Capture navigation can re-enable wall-clock playback.');
for (const phrase of ['--frame-list', 'verify-distinct', 'state/bounds mismatch', 'all PNG hashes are equal']) if (!capture.includes(phrase)) throw new Error(`Sparse capture regression contract missing: ${phrase}`);
for (const phrase of ['getBoundingClientRect()', 'bounds:{caption,scene', 'visualFingerprint', 'Cleared stale frame cache']) if (!capture.includes(phrase)) throw new Error(`Viewport/cache safety contract missing: ${phrase}`);
if (!read('smoke.ps1').includes("'123,127,300,1350,3150,4350,4950'")) throw new Error('Sparse smoke must cover every long-caption review frame.');
for (const phrase of ['--enable-gpu-rasterization', '--use-angle=d3d11', 'optimizeForSpeed: true', '--software']) if (!capture.includes(phrase)) throw new Error(`GPU/software capture contract missing: ${phrase}`);
if (!read('render.ps1').includes('Test-Nvenc') || !read('render.ps1').includes('h264_nvenc')) throw new Error('Conditional NVENC probe contract missing.');
if (read('styles.css').includes('@keyframes') || read('styles.css').includes('animation:')) throw new Error('Wall-clock CSS animation is not allowed in frame-addressed rendering.');
console.log('PASS: 10 contiguous approved cues, 0:00–3:00; deterministic GPU/software capture, NVENC probe, and sparse-state regression contracts present.');
