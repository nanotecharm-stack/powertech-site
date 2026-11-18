# -*- coding: utf-8 -*-
"""Заголовочная копия Overused Grotesk: overused-grotesk-head.woff2.

Зачем (2026-11-18, бриф владельца «аудит типографики всех заголовков»): в исходном
шрифте пара «любая буква + t/f» сведена на постоянные -55 единиц (при 2000 на кегль),
пара «s + t/f» — на -37. У этих значений нет поправки по оси веса: на светлом
начертании они верны, на жирном 700 буквы слипаются («ct» в electrical, «st» в system),
а соседние «al», «ri» рядом читаются разреженными. У остальных пар (Te, ow…) поправка
по весу есть — их не трогаем.

Копия нужна, чтобы обычный текст (вес 400) остался точно прежним: правится только
шрифт заголовков. Запуск:  python fonts/make_head.py   (нужен fonttools + brotli)
"""
import os
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'overused-grotesk-latin.woff2')
DST = os.path.join(HERE, 'overused-grotesk-head.woff2')
SOFTEN = {-55: -16, -37: -10}   # было -> стало, в единицах шрифта

t = TTFont(SRC)
gt = t.getBestCmap()[ord('t')]
n = 0
for lk in t['GPOS'].table.LookupList.Lookup:
    for st in lk.SubTable:
        st = getattr(st, 'ExtSubTable', st)
        if st.__class__.__name__ != 'PairPos' or st.Format != 2:
            continue
        c2 = st.ClassDef2.classDefs.get(gt, 0)
        if not c2:
            continue
        for rec in st.Class1Record:
            v = rec.Class2Record[c2].Value1
            if v and v.XAdvance in SOFTEN and getattr(v, 'XAdvDevice', None) is None:
                v.XAdvance = SOFTEN[v.XAdvance]
                n += 1
assert n == 3, 'ожидалось 3 записи, найдено %d — исходный шрифт изменился' % n
t.flavor = 'woff2'
t.save(DST)
print('ok', DST, os.path.getsize(DST), 'bytes;', n, 'records')
