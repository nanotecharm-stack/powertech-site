// usage: node svg2png.mjs <in.svg> <out.png> <px>  — прозрачный фон, SVG растянут ровно на px×px
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
const [svgPath, out, px = '48'] = process.argv.slice(2);
const V = Math.max(+px, 300); // Chrome не открывает окно меньше ~300 px — рисуем в большом окне и режем по clip
const svg = readFileSync(resolve(svgPath), 'utf8');
const html = 'data:text/html;charset=utf-8,' + encodeURIComponent(
  `<!doctype html><html><head><style>html,body{margin:0;background:transparent}svg{display:block;width:${px}px;height:${px}px}</style></head><body>${svg}</body></html>`);
const port = 9333 + Math.floor(Math.random() * 500);
const chrome = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe',
  ['--headless=new', `--remote-debugging-port=${port}`, '--no-first-run', '--hide-scrollbars',
   `--window-size=${V},${V}`, '--user-data-dir=' + process.env.TEMP + '/cdp-' + port, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let target;
for (let i = 0; i < 40; i++) { try { const l = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); target = l.find(t => t.type === 'page'); if (target) break; } catch {} await sleep(150); }
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: V, height: V, deviceScaleFactor: 1, mobile: false });
await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
await send('Page.navigate', { url: html });
await sleep(600);
const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: +px, height: +px, scale: 1 } });
writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
console.log(out, px);
ws.close(); chrome.kill();
