# -*- coding: utf-8 -*-
"""UI refinement 2026-11-17 (brief «Gridec UI Refinement», владелец выбрал «Focused: 2, 4, 5»).

2  Alpha borders: тонкие линии на тёмном — два токена (--line-d .13 конструкция, --line-d2 .22
   шкалы), разнобой .13/.14 сведён; сплошная рамка карточек отраслей -> прозрачная --hair.
4  Icon weight: значки раздела 06 — одна толщина конструкции 1.25, акцент 1.6, вспомогательное 1.0
   (было 0.8 / 1 / 1.1 / 1.4 / 1.7 / 2.2).
5  Dark depth: ячейки раздела 06 на плашке получают первый слой поверхности --surf-d1 (.025);
   ячейка «Риски» остаётся вторым, более светлым слоем. Без теней (тени владелец отверг).
+  Радиус: токены --r 2px и --r-in 1px; квадрат стрелки ВНУТРИ кнопки — --r-in (концентрично).

Каждая замена проверяет, что исходный текст встречается ровно столько раз, сколько ожидается.
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')


def patch(fn, pairs):
    p = os.path.join(ROOT, fn)
    t = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    if 'UI refinement 2026-11-17' in t or 'stroke-width="1.25"' in t:
        print(fn, 'already applied'); return
    for a, b, n in pairs:
        a, b = a.replace('\n', nl), b.replace('\n', nl)
        c = t.count(a)
        assert c == n, (fn, a[:70], c, n)
        t = t.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(t)
    print(fn, len(pairs), 'ok')


TOKENS = (
    '/* UI refinement 2026-11-17: радиусы, линии на тёмном и первый слой поверхности плашки. */\n'
    ':root{--r:2px;--r-in:1px;--line-d:rgba(239,237,234,.13);--line-d2:rgba(239,237,234,.22);'
    '--surf-d1:rgba(239,237,234,.025);}\n')

patch('shell.html', [
    # tokens, right before the industry cards
    ('.icard{position:relative;display:flex;', TOKENS + '.icard{position:relative;display:flex;', 1),
    # 2: solid card frame -> alpha hairline; radius token
    ('background:#101218;color:#EFEDEA;border:1px solid #101218;border-radius:2px;}',
     'background:#101218;color:#EFEDEA;border:1px solid var(--hair);border-radius:var(--r);}', 1),
    # radius: chip inside a button is concentric
    ('.btn i{position:relative;z-index:1;display:grid;place-items:center;width:22px;height:22px;border-radius:2px',
     '.btn i{position:relative;z-index:1;display:grid;place-items:center;width:22px;height:22px;border-radius:var(--r-in)', 1),
    # 2: dark hairlines -> tokens
    ('.plate2 .meas{border-top-color:rgba(239,237,234,.13);}', '.plate2 .meas{border-top-color:var(--line-d);}', 1),
    ('.plate2 .mi{border-left-color:rgba(239,237,234,.13);}',
     '.plate2 .mi{border-left-color:var(--line-d);}\n'
     '/* 5: первый слой поверхности; «Риски» (.mi-alt) остаётся вторым, светлее */\n'
     '.plate2 .mi:not(.mi-alt){background:var(--surf-d1);}', 1),
    ('.plate2 .mi:nth-child(n+5){border-top-color:rgba(239,237,234,.13);}',
     '.plate2 .mi:nth-child(n+5){border-top-color:var(--line-d);}', 1),
    ('border-left:1px solid rgba(239,237,234,.22);', 'border-left:1px solid var(--line-d2);', 3),
    ('box-shadow:inset 0 1px 0 rgba(239,237,234,.14);', 'box-shadow:inset 0 1px 0 var(--line-d);', 1),
    ('height:1px;background:rgba(239,237,234,.14);}', 'height:1px;background:var(--line-d);}', 1),
    ('border-top:1px solid rgba(239,237,234,.14);', 'border-top:1px solid var(--line-d);', 1),
])

# 4: section 06 icons — one weight system
patch('build.py', [
    ("'<g fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.1\">'\n '<ellipse cx=\"13\"",
     "'<g fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.25\">'\n '<ellipse cx=\"13\"", 1),
    ('ry="10.4" fill="none" stroke="var(--brand)" stroke-width="1.4"/>',
     'ry="10.4" fill="none" stroke="var(--brand)" stroke-width="1.6"/>', 1),
    ('\'<g stroke="currentColor" stroke-width="1.1" stroke-linecap="round" opacity=".7">\'',
     '\'<g stroke="currentColor" stroke-width="1.25" stroke-linecap="round" opacity=".7">\'', 1),
    ('<path d="M19 15h6" stroke="var(--brand)" stroke-width="1.7"', '<path d="M19 15h6" stroke="var(--brand)" stroke-width="1.6"', 1),
    ('\'<g fill="none" stroke="currentColor" stroke-width="1">\'\n \'<rect x="8"',
     '\'<g fill="none" stroke="currentColor" stroke-width="1.25">\'\n \'<rect x="8"', 1),
    ('6 0 4 4 6 0" fill="none" stroke="currentColor" stroke-width="1.4"/>',
     '6 0 4 4 6 0" fill="none" stroke="currentColor" stroke-width="1.25"/>', 1),
    ('4 8 6 0" fill="none" stroke="var(--brand)" stroke-width="1.4"/>',
     '4 8 6 0" fill="none" stroke="var(--brand)" stroke-width="1.6"/>', 1),
    ('\'stroke-width="1.4" stroke-linecap="round"/>\'\n \'<path d="M12.5 23h9" stroke="var(--brand)" stroke-width="2.2"',
     '\'stroke-width="1.25" stroke-linecap="round"/>\'\n \'<path d="M12.5 23h9" stroke="var(--brand)" stroke-width="1.6"', 1),
    ('\'<g stroke="currentColor" stroke-width="1.4" stroke-linecap="round">\'\n \'<path d="M22 15.5 13.5 21"/>',
     '\'<g stroke="currentColor" stroke-width="1.25" stroke-linecap="round">\'\n \'<path d="M22 15.5 13.5 21"/>', 1),
    ('8 22 4" fill="none" stroke="currentColor" stroke-width="1.4"/>',
     '8 22 4" fill="none" stroke="currentColor" stroke-width="1.25"/>', 1),
    ('\'stroke-width="1.4" stroke-linejoin="round"/>\'\n \'<rect x="27"',
     '\'stroke-width="1.25" stroke-linejoin="round"/>\'\n \'<rect x="27"', 1),
    ('\'<g stroke="currentColor" stroke-width=".8" opacity=".26">\'',
     '\'<g stroke="currentColor" stroke-width="1" opacity=".26">\'', 1),
    ('\'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>\'\n \'<g fill="currentColor"><circle cx="8"',
     '\'stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>\'\n \'<g fill="currentColor"><circle cx="8"', 1),
])
