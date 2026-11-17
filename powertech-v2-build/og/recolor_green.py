# -*- coding: utf-8 -*-
"""Перекраска растровых знаков из синей палитры в зелёную (2026-11-17).

Знак и почтовые плашки — плоские цвета на ровном фоне, края сглажены. Каждый
пиксель раскладывается как смесь «цвет знака + фон»: берётся тот исходный цвет,
отрезок до фона от которого ближе всего к пикселю, и доля t вдоль отрезка.
Новый пиксель = та же доля между НОВЫМ цветом и тем же фоном. Сглаживание краёв
сохраняется, фон не трогается. Прозрачность (альфа) переносится как есть.

usage: python recolor_green.py <bg r,g,b> <in.png> <out.png>
"""
import sys
from PIL import Image

MAP = {  # синий -> зелёный, те же роли, что в build.py PALETTES['green']
    (13, 36, 64): (23, 36, 31),      # #0D2440 -> #17241F плашка/чернила знака
    (46, 94, 153): (47, 107, 79),    # #2E5E99 -> #2F6B4F марка
    (95, 140, 194): (95, 162, 126),  # #5F8CC2 -> #5FA27E светлая плоскость (light-s)
    (123, 164, 208): (134, 194, 160),  # #7BA4D0 -> #86C2A0 светлая плоскость
}


def recolor(im, bg):
    im = im.convert('RGBA')
    px = im.load()
    cache = {}
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            key = (r, g, b)
            if key not in cache:
                best = None
                for src, dst in MAP.items():
                    d = [src[i] - bg[i] for i in range(3)]
                    dd = sum(v * v for v in d)
                    t = sum((key[i] - bg[i]) * d[i] for i in range(3)) / dd
                    t = max(0.0, min(1.0, t))
                    err = sum((bg[i] + t * d[i] - key[i]) ** 2 for i in range(3))
                    if best is None or err < best[0]:
                        best = (err, t, dst)
                err, t, dst = best
                # пиксель, который не объясняется ни одним синим (чужой цвет) — не трогаем
                cache[key] = key if err > 900 else tuple(
                    round(bg[i] + t * (dst[i] - bg[i])) for i in range(3))
            px[x, y] = cache[key] + (a,)
    return im


if __name__ == '__main__':
    bg = tuple(int(v) for v in sys.argv[1].split(','))
    src, out = sys.argv[2], sys.argv[3]
    im = Image.open(src)
    mode = im.mode
    res = recolor(im, bg)
    if mode == 'RGB':
        res = res.convert('RGB')
    res.save(out, 'PNG', optimize=True)
    print(out, res.size)
