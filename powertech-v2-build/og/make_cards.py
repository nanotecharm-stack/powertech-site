# -*- coding: utf-8 -*-
"""Карточка ссылки (og:image) для обеих языковых версий.

Считается на МЕЛКОЕ превью, а не на полный размер. Причина измерена: в WhatsApp
превью около 160px при карточке 1200, то есть уменьшение в 7-8 раз.

Предел, из которого выросла вся раскладка: чтобы штрих пиксельной литеры держался
в 160px, нужно 22px в карточке; при таком штрихе плашка со словом GRIDEC вышла бы
1452px — шире карточки. Шесть пиксельных литер в мелком превью не помещаются
НИКОГДА, сколько их ни увеличивай. Прежние попытки шли в обратную сторону: знак
раздувался до половины карточки и в WhatsApp расползался кашей.

Отсюда разворот: знак — ПОДПИСЬ, а не вывеска; главным становится то, что сжатие
переживает — очень крупный заголовок сплошными штрихами. С 2026-09-14 знак — логотип
владельца (три плоскости + «gridec»), а не пиксельная плашка GRIDEC. Отраслевые руководства по og:image
советуют то же: крупные простые элементы, 5-7 слов, и не раздувать логотип.

Отклонённый вариант (владелец выбрал этот 20.08): чернильная карточка, где
главным была сама просадка крупно и белым, а знак уходил в подпись внизу. В
160px от неё оставалась только линия — чем занимается фирма, прочесть было нельзя.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont


HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, '..', 'brand')
S = 2
W, H = 1200, 630

CREAM = (246, 241, 233)
INK = (43, 39, 34)
MUTE = (96, 90, 83)
NAVY = (13, 36, 64)

# WhatsApp НЕ уменьшает карточку — он вырезает из неё КВАДРАТ ПО ЦЕНТРУ. Проверено
# на снимке владельца 20.08 и воспроизведено расчётом: из 1200x630 берётся 630x630,
# то есть x с 285 по 915. Прежняя раскладка была прижата к левому полю — знак
# уезжал за срез целиком, а от заголовка оставалось «r quality / toring».
# Отсюда всё по центру, и вся смысловая часть внутри 630 px.
SAFE = 630        # ширина квадрата, за которую нельзя выходить
PAD = 72          # поле для того, что обрезать не жалко
# Логотип владельца (2026-09-13: знак из трёх плоскостей + строчное «gridec»), малый вариант для
# светлого фона с широкими зазорами — он переживает сжатие превью. Отрисован из brand/gridec-logo-light-s.svg
# безголовым Chrome на 2x и уменьшен вдвое (og/logo-mark.png, 330 px по ширине, фон = CREAM).
LOGO_FILE = 'logo-mark.png'
LOGO_Y = 108

TEXT = {
    'en': {
        'head': ['Power quality', 'monitoring'],
        'sub': 'Yerevan  \u00b7  Armenia',
        'font': 'grotesk.ttf',
        'sub_font': 'grotesk.ttf',
        # 92 -> 573 px, внутри квадрата с запасом
        'head_px': 92, 'lead': 104,
    },
    'hy': {
        'head': ['\u0537\u056c\u0565\u056f\u057f\u0580\u0561\u0567\u0576\u0565\u0580\u0563\u056b\u0561\u0575\u056b',
                 '\u0578\u0580\u0561\u056f\u056b \u0574\u0578\u0576\u056b\u0569\u0578\u0580\u056b\u0576\u0563'],
        'sub': '\u0535\u0580\u0587\u0561\u0576  \u00b7  \u0540\u0561\u0575\u0561\u057d\u057f\u0561\u0576',
        'font': 'arian-bold.ttf',
        'sub_font': 'arian.ttf',
        # Армянские слова длиннее английских: на 92 первая строка вышла бы 773 px
        # и вылезла за срез. 62 -> 564 px. Кегли разные, но каждый заполняет свой
        # квадрат одинаково — это честнее, чем один кегль и обрезанное слово.
        'head_px': 62, 'lead': 78,
    },
}

def face(name, px, weight=None):
    f = ImageFont.truetype(os.path.join(HERE, name), px)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f

def sag(d, y0, x0, x1, amp, colour, width):
    """Ход измерения с просадкой — тот же рисунок, что в герое сайта.
    Точек мало намеренно: при большой толщине частые стыки дают бусины."""
    pts = []
    n = 200
    for i in range(n + 1):
        t = i / n
        v = math.sin(t * 9) * 0.05 + math.sin(t * 4.5 + 1.0) * 0.035
        dip = math.exp(-((t - 0.63) ** 2) / 0.0042) * 1.30
        pts.append((x0 + (x1 - x0) * t, y0 + (v + dip) * amp))
    d.line(pts, fill=colour, width=width, joint='curve')

def build(lang):
    t = TEXT[lang]
    big = Image.new('RGB', (W * S, H * S), CREAM)
    d = ImageDraw.Draw(big)

    fh = face(t['font'], t['head_px'] * S, 700 if t['font'] == 'grotesk.ttf' else None)
    fs = face(t['sub_font'], 30 * S, 400 if t['sub_font'] == 'grotesk.ttf' else None)

    def centred(text, font, y, fill):
        w = d.textlength(text, font=font)
        assert w <= SAFE * S, 'строка %d px шире квадрата %d' % (w / S, SAFE)
        d.text(((W * S - w) / 2, y * S), text, font=font, fill=fill)

    block = len(t['head']) * t['lead']
    y = 250 + (2 * 104 - block) / 2.0        # оба языка держат одну середину блока
    for line in t['head']:
        centred(line, fh, y, INK)
        y += t['lead']
    centred(t['sub'], fs, y + 20, MUTE)

    # След — единственное, что за срез выходить может: это фон, а не смысл.
    sag(d, int(560 * S), PAD * S, int((W - PAD) * S), int(28 * S), NAVY, int(5 * S))

    out = big.resize((W, H), Image.LANCZOS)
    # Знак вставляется ПОСЛЕ уменьшения, готовым растром на кремовом фоне.
    lg = Image.open(os.path.join(HERE, LOGO_FILE)).convert('RGB')
    out.paste(lg, ((W - lg.width) // 2, LOGO_Y))

    name = 'og-%s.png' % lang
    for path in (os.path.join(HERE, name), os.path.join(BRAND, name)):
        out.save(path, 'PNG', optimize=True)
    # Превью в те размеры, в которых карточку реально видят.
    for w in (300, 160):
        out.resize((w, round(H * w / W)), Image.LANCZOS).save(
            os.path.join(HERE, 'og-%s-%d.png' % (lang, w)), 'PNG', optimize=True)
    # И то, что реально видит WhatsApp: квадрат по центру.
    x0 = (W - H) // 2
    sq = out.crop((x0, 0, x0 + H, H))
    for w in (300, 96):
        sq.resize((w, w), Image.LANCZOS).save(
            os.path.join(HERE, 'sq-%s-%d.png' % (lang, w)), 'PNG', optimize=True)
    print('%-12s %d KB' % (name, os.path.getsize(os.path.join(HERE, name)) // 1024))

if __name__ == '__main__':
    for lang in ('en', 'hy'):
        build(lang)
