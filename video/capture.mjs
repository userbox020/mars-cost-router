// Dependency-free persistent Chromium capture via the Chrome DevTools Protocol.
// Node 24 provides fetch; the small WebSocket client below avoids npm packages.
import { createServer, connect } from 'node:net';
import { spawn } from 'node:child_process';
import { mkdir, writeFile, access, readFile, rm } from 'node:fs/promises';
import { constants } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => v.startsWith('--') ? (a.push([v.slice(2), all[i + 1]]), a) : a, []));
const hasFlag = flag => process.argv.includes(flag);
const browser = args.browser, start = Number(args.start), end = Number(args.end), frames = args.frames ? resolve(args.frames) : resolve(root, 'frames');
const listedFrames = args['frame-list'] ? args['frame-list'].split(',').map(value => Number(value.trim())) : null;
const selectedFrames = listedFrames ?? Array.from({ length: end - start + 1 }, (_, index) => start + index);
if (!browser || (!listedFrames && (!Number.isInteger(start) || !Number.isInteger(end))) || !selectedFrames.length || selectedFrames.some(frame => !Number.isInteger(frame) || frame < 0 || frame > 4199) || new Set(selectedFrames).size !== selectedFrames.length) throw new Error('Usage: node capture.mjs --browser <path> --start 0 --end 4199 --frames <directory>, or --frame-list 123,300,1350,3150,3540,4050.');

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function freePort() { const server = createServer(); await new Promise(resolve => server.listen(0, '127.0.0.1', resolve)); const { port } = server.address(); await new Promise(resolve => server.close(resolve)); return port; }
async function exists(file) { try { await access(file, constants.F_OK); return true; } catch { return false; } }
const visualInputs = ['index.html', 'app.js', 'styles.css', '../assets/brand/mars-cost-router-hero.svg', '../assets/diagrams/delegation-flow.svg', '../assets/evidence/fixed-v1.2-performance.svg'];
async function visualFingerprint() { const hash = createHash('sha256'); for (const input of visualInputs) { const path = resolve(root, input); hash.update(input); hash.update(await readFile(path)); } return hash.digest('hex'); }
async function ensureFrameCache() {
  const fingerprint = await visualFingerprint(), manifest = resolve(frames, '.mars-frame-cache.json');
  let valid = false;
  if (await exists(manifest)) { try { valid = JSON.parse(await readFile(manifest, 'utf8')).visualFingerprint === fingerprint; } catch {} }
  if (!valid && await exists(frames)) { await rm(frames, { recursive: true, force: true }); process.stdout.write('Cleared stale frame cache because its visual source fingerprint does not match.\n'); }
  await mkdir(frames, { recursive: true });
  if (!valid) await writeFile(manifest, JSON.stringify({ visualFingerprint: fingerprint, width: 1920, height: 1080, fps: 30 }, null, 2));
}
class CDP {
  constructor(socket) { this.socket = socket; this.buffer = Buffer.alloc(0); this.id = 0; this.pending = new Map(); socket.on('data', data => this.receive(data)); socket.on('error', error => this.fail(error)); socket.on('close', () => this.fail(new Error('CDP socket closed'))); }
  fail(error) { for (const { reject } of this.pending.values()) reject(error); this.pending.clear(); }
  receive(data) { this.buffer = Buffer.concat([this.buffer, data]); while (this.buffer.length >= 2) { const first = this.buffer[0], second = this.buffer[1]; let offset = 2, length = second & 127; if (length === 126) { if (this.buffer.length < 4) return; length = this.buffer.readUInt16BE(2); offset = 4; } else if (length === 127) { if (this.buffer.length < 10) return; length = Number(this.buffer.readBigUInt64BE(2)); offset = 10; } if (this.buffer.length < offset + length) return; const payload = this.buffer.subarray(offset, offset + length); this.buffer = this.buffer.subarray(offset + length); if ((first & 15) !== 1) continue; const message = JSON.parse(payload.toString('utf8')); if (message.id && this.pending.has(message.id)) { const pending = this.pending.get(message.id); this.pending.delete(message.id); message.error ? pending.reject(new Error(message.error.message)) : pending.resolve(message.result); } } }
  send(method, params = {}) { const id = ++this.id, json = Buffer.from(JSON.stringify({ id, method, params })); const mask = Buffer.from([17, 93, 61, 201]); let header; if (json.length < 126) header = Buffer.from([129, 128 | json.length]); else if (json.length < 65536) { header = Buffer.alloc(4); header[0] = 129; header[1] = 254; header.writeUInt16BE(json.length, 2); } else throw new Error('CDP request too large'); const masked = Buffer.alloc(json.length); for (let i = 0; i < json.length; i++) masked[i] = json[i] ^ mask[i % 4]; this.socket.write(Buffer.concat([header, mask, masked])); return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject })); }
}
async function websocket(url) { const parsed = new URL(url); const socket = connect({ host: parsed.hostname, port: Number(parsed.port) }); await new Promise((resolve, reject) => { socket.once('error', reject); socket.once('connect', resolve); }); const key = Buffer.from('mars-cost-router-cdp').toString('base64'); socket.write(`GET ${parsed.pathname}${parsed.search} HTTP/1.1\r\nHost: ${parsed.host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`); let header = Buffer.alloc(0); await new Promise((resolve, reject) => { const onData = data => { header = Buffer.concat([header, data]); const marker = header.indexOf('\r\n\r\n'); if (marker >= 0) { socket.off('data', onData); if (!header.subarray(0, marker).toString().includes('101')) reject(new Error('CDP WebSocket handshake failed')); else { const rest = header.subarray(marker + 4); if (rest.length) socket.unshift(rest); resolve(); } } }; socket.on('data', onData); socket.once('error', reject); }); return new CDP(socket); }

const port = await freePort();
const profile = resolve(root, '.cdp-profile');
const software = hasFlag('--software');
const gpuFlags = software ? ['--disable-gpu'] : ['--enable-gpu-rasterization', '--enable-oop-rasterization', '--use-angle=d3d11'];
const processHandle = spawn(browser, [`--headless=new`, `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check', ...gpuFlags, '--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=1920,1080', 'about:blank'], { stdio: 'ignore', windowsHide: true });
let cdp;
try {
  let target;
  for (let attempt = 0; attempt < 80; attempt++) { try { const response = await fetch(`http://127.0.0.1:${port}/json/list`); const pages = await response.json(); target = pages.find(page => page.type === 'page'); if (target) break; } catch {} await delay(100); }
  if (!target) throw new Error('Headless browser did not expose a CDP page target.');
  cdp = await websocket(target.webSocketDebuggerUrl);
  await cdp.send('Page.enable'); await cdp.send('Runtime.enable');
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false, screenWidth: 1920, screenHeight: 1080 });
  // frame=0 prevents app.js from starting its interactive wall-clock loop.
  const page = pathToFileURL(resolve(root, 'index.html')).href + '?frame=0&clean=1';
  await cdp.send('Page.navigate', { url: page });
  for (let attempt = 0; attempt < 100; attempt++) { const ready = await cdp.send('Runtime.evaluate', { expression: 'document.readyState === "complete" && typeof window.setFrame === "function"', returnByValue: true }); if (ready.result.value) break; if (attempt === 99) throw new Error('Presentation did not become ready.'); await delay(50); }
  await cdp.send('Runtime.evaluate', { expression: 'Promise.all(Array.from(document.images).map(image => image.complete ? Promise.resolve() : new Promise(resolve => { image.onload = image.onerror = resolve; })))', awaitPromise: true });
  await ensureFrameCache();
  const total = selectedFrames.length; const started = Date.now(); const captures = [];
  for (const [index, frame] of selectedFrames.entries()) {
    const output = resolve(frames, `frame${String(frame).padStart(5, '0')}.png`);
    const state = await cdp.send('Runtime.evaluate', { expression: `(() => { const result = window.setFrame(${frame}); const tolerance = 2; const check = id => { const r = document.querySelector(id).getBoundingClientRect(); return { left:r.left, top:r.top, right:r.right, bottom:r.bottom, ok:r.left >= -tolerance && r.top >= -tolerance && r.right <= innerWidth + tolerance && r.bottom <= innerHeight + tolerance }; }; const caption = check('#caption'), scene = check('#scene'); return { frame: result.frame, clock: document.querySelector('#clock').textContent, chapter: document.querySelector('#chapter').textContent, viewport:{width:innerWidth,height:innerHeight}, bounds:{caption,scene,ok:innerWidth === 1920 && innerHeight === 1080 && caption.ok && scene.ok} }; })()`, returnByValue: true });
    const expectedSeconds = Math.floor(frame / 30), expectedClock = `${String(Math.floor(expectedSeconds / 60)).padStart(2, '0')}:${String(expectedSeconds % 60).padStart(2, '0')}`, expectedIndex = Math.min(9, Math.floor((frame / 30) < 12 ? 0 : [12,27,43,58,78,94,110,126,133].filter(boundary => frame / 30 >= boundary).length));
    const expectedChapter = `${String(expectedIndex + 1).padStart(2, '0')} / ${['POLICY','IDENTITY','LANES','INSTALL','FLOW','PAYLOAD','EVIDENCE','RECORD','CAVEAT','OUTRO'][expectedIndex]}`;
    const rendered = state.result.value;
    if (rendered.frame !== frame || rendered.clock !== expectedClock || rendered.chapter !== expectedChapter || !rendered.bounds?.ok) throw new Error(`Frame ${frame} state/bounds mismatch: got ${JSON.stringify(rendered)}, expected ${expectedClock} / ${expectedChapter} within 1920x1080.`);
    await cdp.send('Runtime.evaluate', { expression: 'new Promise(requestAnimationFrame)', awaitPromise: true });
    if (!await exists(output)) { const shot = await cdp.send('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false, optimizeForSpeed: true }); await writeFile(output, Buffer.from(shot.data, 'base64')); }
    captures.push({ frame, output, clock: rendered.clock, chapter: rendered.chapter });
    if (index % 100 === 0 || index === total - 1) process.stdout.write(`  ${index + 1}/${total} frame ${frame} — ${rendered.clock} / ${rendered.chapter}\n`);
  }
  if (hasFlag('--verify-distinct')) { const hashes = await Promise.all(captures.map(async capture => ({ ...capture, hash: createHash('sha256').update(await readFile(capture.output)).digest('hex') }))); if (new Set(hashes.map(item => item.hash)).size < 2) throw new Error('Sparse capture regression failed: all PNG hashes are equal.'); hashes.forEach(item => process.stdout.write(`  SHA-256 frame ${item.frame}: ${item.hash} (${item.clock} / ${item.chapter})\n`)); }
  process.stdout.write(`Captured ${total} frame(s) with one persistent ${software ? 'software' : 'GPU-composited'} browser in ${((Date.now() - started) / 1000).toFixed(2)}s.\n`);
} finally {
  try { if (cdp) { await cdp.send('Browser.close'); cdp.socket.end(); } } catch {}
  if (!processHandle.killed) processHandle.kill();
}
