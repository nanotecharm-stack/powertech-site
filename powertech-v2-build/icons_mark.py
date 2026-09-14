# -*- coding: utf-8 -*-
"""Значки сайта из ЗНАКА владельца (favicon.svg в корне — три плоскости на синей плашке).

    python icons_mark.py

Пишет в корень репозитория: favicon.ico (кадры 16/32/48 PNG), favicon-96.png (Google берёт
PNG кратный 48), apple-touch-icon.png (180, плашка без скругления — iOS кладёт свою маску).
favicon.svg не трогает — он и есть исходник.

Почему не chrome --screenshot file.svg: Chrome рисует svg-файл в его собственном размере
в углу окна и не масштабирует — так в 2026-09-13 получились «спрайты» в углу (.ico и
apple-touch-icon были сломаны). Здесь SVG вкладывается в HTML ровно в px×px через
svg2png.mjs (CDP, прозрачный фон).
"""
import io, os, struct, subprocess, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
SVG = os.path.join(ROOT, 'favicon.svg')
TMP = tempfile.mkdtemp(prefix='gridec-icons-')

def render(svg_text, px, name):
    src = os.path.join(TMP, name + '.svg')
    io.open(src, 'w', encoding='utf-8').write(svg_text)
    out = os.path.join(TMP, '%s-%d.png' % (name, px))
    subprocess.run(['node', os.path.join(HERE, 'svg2png.mjs'), src, out, str(px)],
                   check=True, capture_output=True)
    im = Image.open(out).convert('RGBA')
    assert im.size == (px, px), im.size
    return im

svg = io.open(SVG, encoding='utf-8').read()
assert 'rx="12"' in svg, 'ожидалась плашка rx=12 (viewBox 64)'
square = svg.replace('rx="12"', 'rx="0"', 1)

frames = {px: render(svg, px, 'fav') for px in (16, 32, 48, 96)}
# .ico вручную: кадры PNG, заголовок по спецификации — без сюрпризов от библиотек.
out = io.BytesIO(); sizes = (16, 32, 48)
blobs = []
for px in sizes:
    b = io.BytesIO(); frames[px].save(b, format='PNG', optimize=True); blobs.append(b.getvalue())
out.write(struct.pack('<HHH', 0, 1, len(sizes)))
off = 6 + 16 * len(sizes)
for px, data in zip(sizes, blobs):
    out.write(struct.pack('<BBBBHHII', px, px, 0, 0, 1, 32, len(data), off)); off += len(data)
for data in blobs:
    out.write(data)
io.open(os.path.join(ROOT, 'favicon.ico'), 'wb').write(out.getvalue())
frames[96].save(os.path.join(ROOT, 'favicon-96.png'), 'PNG', optimize=True)
render(square, 180, 'apple').convert('RGB').save(os.path.join(ROOT, 'apple-touch-icon.png'), 'PNG', optimize=True)
for fn in ('favicon.ico', 'favicon-96.png', 'apple-touch-icon.png'):
    print('%-22s %5d B' % (fn, os.path.getsize(os.path.join(ROOT, fn))))
