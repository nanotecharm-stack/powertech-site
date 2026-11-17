"""Два кадра «как выглядит отчёт» для раздела 04 (2026-11-17, владелец: «нужно разместить так,
чтобы лишь было понимание у посетителя, без возможности углядеть цифры»; вариант 2 — рисуем сами,
снимки брошюры Janitza не берём: чужие права и намёк на партнёрство).

В кадрах НЕТ ни одной цифры и ни одной буквы: подписи осей и строки таблицы — серые полоски.
Кадр 1 — тренд напряжения трёх фаз за 7 суток с допустимой полосой и одним провалом.
Кадр 2 — гармоники по порядкам с отметками предела и журнал событий.

Пишет разметку в shell.html между <!-- rep-figs:start --> и <!-- rep-figs:end -->.
Запуск: python rep_figs.py (затем python build.py).
"""
import io, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.join(HERE, 'shell.html')

INK = '#17241F'; GREEN = '#2F6B4F'; PALE = '#86C2A0'; COPPER = '#E08A4B'
GHOST = 'rgba(23,36,31,.16)'; GRID = 'rgba(23,36,31,.07)'; HAIR = 'rgba(23,36,31,.12)'
W, H = 500, 300


def bar(x, y, w, h=5, fill=GHOST):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1" fill="%s"/>' % (x, y, w, h, fill)


def head(legend):
    """Шапка кадра: метка, «заголовок» полоской, справа легенда (цвет + полоска)."""
    s = ['<rect x="24" y="22" width="9" height="9" rx="1" fill="%s"/>' % INK,
         bar(41, 24, 118, 6, 'rgba(23,36,31,.32)')]
    x = W - 24
    for col, wid in reversed(legend):
        x -= wid
        s.append(bar(x, 24.5, wid, 5))
        x -= 20
        s.append('<rect x="%.1f" y="26" width="14" height="2" fill="%s"/>' % (x + 1, col))
        x -= 14
    s.append('<line x1="24" y1="46" x2="%d" y2="46" stroke="%s"/>' % (W - 24, HAIR))
    return s


def svg(body):
    return ('<svg viewBox="0 0 %d %d" aria-hidden="true" focusable="false" '
            'xmlns="http://www.w3.org/2000/svg">' % (W, H) + ''.join(body) + '</svg>')


def frame_trend():
    rnd = random.Random(7)
    s = head([(INK, 22), (GREEN, 22), (PALE, 22)])
    x0, x1, y0, y1 = 44, W - 24, 66, 246
    for i in range(5):  # горизонтальная сетка
        y = y0 + (y1 - y0) * i / 4
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (x0, y, x1, y, GRID))
        s.append(bar(24, y - 2.5, 13))
    for d in range(8):  # границы суток и подписи-полоски
        x = x0 + (x1 - x0) * d / 7
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (x, y0, x, y1, GRID))
        if d < 7:
            s.append(bar(x + (x1 - x0) / 14 - 11, y1 + 14, 22))
    # допустимая полоса
    by0, by1 = 92, 222
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" fill-opacity=".16"/>' % (x0, by0, x1 - x0, by1 - by0, PALE))
    for y in (by0, by1):
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-opacity=".55" stroke-dasharray="4 4"/>' % (x0, y, x1, y, GREEN))
    ev = x0 + (x1 - x0) * 4.58 / 7  # провал на пятые сутки
    n = 260
    for col, off, ph in ((INK, -7, 0.0), (GREEN, 0, 0.35), (PALE, 6, 0.7)):
        pts, noise = [], 0.0
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            t = (x - x0) / (x1 - x0) * 7
            noise = noise * 0.8 + rnd.uniform(-1.4, 1.4)
            y = 150 + off + 9 * math.sin(2 * math.pi * (t - 0.3) + ph * 0.3) + 4 * math.sin(2 * math.pi * t * 0.43 + 1.1) + 1.6 * noise
            dx = x - ev
            if -2 < dx < 9:  # короткий глубокий провал и возврат
                y += 58 * math.exp(-((dx - 1.5) / 3.2) ** 2) * (1 - abs(off) / 30)
            pts.append('%.1f,%.1f' % (x, y))
        s.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.4" stroke-linejoin="round"/>' % (' '.join(pts), col))
    s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-dasharray="2 3"/>' % (ev + 1.5, y0, ev + 1.5, y1, COPPER))
    s.append('<circle cx="%.1f" cy="%d" r="3.5" fill="%s"/>' % (ev + 1.5, y0, COPPER))
    return svg(s)


def frame_harm():
    s = head([(INK, 26), (GREEN, 26)])
    x0, x1, y0, y1 = 44, W - 24, 64, 166
    for i in range(4):
        y = y0 + (y1 - y0) * i / 3
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (x0, y, x1, y, GRID))
        s.append(bar(24, y - 2.5, 13))
    orders = list(range(2, 26))
    lev = {3: .52, 5: .80, 7: .58, 9: .14, 11: .34, 13: .26, 15: .07, 17: .15, 19: .12, 21: .05, 23: .09, 25: .07}
    lim = {3: .92, 5: .95, 7: .74, 9: .30, 11: .56, 13: .48, 15: .18, 17: .34, 19: .30, 21: .14, 23: .25, 25: .23}
    step = (x1 - x0) / len(orders); bw = step * .5
    for k, o in enumerate(orders):
        cx = x0 + step * (k + .5)
        v = lev.get(o, .025 + .01 * (o % 3))
        h = (y1 - y0) * v
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s"/>' % (cx - bw / 2, y1 - h, bw, h, INK, '.85' if o % 2 else '.35'))
        L = lim.get(o, .12)
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="2" fill="%s"/>' % (cx - bw / 2 - 2, y1 - (y1 - y0) * L - 1, bw + 4, GREEN))
        if o % 5 == 0:
            s.append(bar(cx - 7, y1 + 8, 14))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (x0, y1, x1, y1, 'rgba(23,36,31,.3)'))
    # журнал событий
    ty = 196
    s.append('<line x1="24" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (ty - 8, W - 24, ty - 8, HAIR))
    rows = [(COPPER, 62, 150, 48), (PALE, 54, 120, 40), (PALE, 62, 168, 44), (PALE, 58, 104, 36)]
    for i, (c, a, b, d) in enumerate(rows):
        y = ty + i * 24
        s.append('<rect x="24" y="%d" width="8" height="8" rx="1" fill="%s"/>' % (y + 2, c))
        s.append(bar(44, y + 3.5, a))
        s.append(bar(140, y + 3.5, b))
        s.append(bar(W - 24 - d, y + 3.5, d))
        s.append('<line x1="24" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (y + 16, W - 24, y + 16, GRID))
    return svg(s)


def main():
    html = ('<!-- rep-figs:start -->\n'
            '    <div class="rep-figs" aria-hidden="true">'
            '<figure class="rep-fig">' + frame_trend() + '</figure>'
            '<figure class="rep-fig">' + frame_harm() + '</figure></div>\n'
            '    <!-- rep-figs:end -->')
    t = io.open(SHELL, encoding='utf-8').read()
    a, b = t.index('<!-- rep-figs:start -->'), t.index('<!-- rep-figs:end -->') + len('<!-- rep-figs:end -->')
    io.open(SHELL, 'w', encoding='utf-8', newline='').write(t[:a] + html + t[b:])
    print('rep-figs: %d bytes' % len(html))


if __name__ == '__main__':
    main()
