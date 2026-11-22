# Снимает с четырёх графиков армянского отчёта СТАРЫЕ подписи (легенду и названия осей),
# чтобы gen_hy_final.py поставил поверх исправленные. Линии, сетка, шкалы и числа не трогаются:
# полоса легенды заполняется соседней чистой строкой пикселей (так тонкие вертикальные метки
# событий и заливка остаются непрерывными), поля с названиями осей — белым.
# Запуск: python clean_figs_hy.py  → revised/img_hy_*_clean.png
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'revised')
# имя: (полоса легенды y0,y1, чистая строка-образец, правая граница поля названия оси Y, верх поля названия оси X или None)
JOBS = {'p4_1': (35, 55, 57, 45, None), 'p4_2': (35, 55, 56, 45, None),
        'p6_3': (35, 55, 57, 45, 618), 'p8_4': (40, 65, 67, 52, 553)}

for lang, name in [(l, n) for l in ('hy', 'en') for n in JOBS]:   # у EN и HY картинок одна геометрия (проверено замером)
    y0, y1, yr, xl, yb = JOBS[name]
    im = Image.open(os.path.join(SRC, 'img_%s_%s.png' % (lang, name))).convert('RGB')
    w, h = im.size
    px = im.load()
    for x in range(112, 1300):
        c = px[x, yr]
        for y in range(y0, y1 + 1):
            px[x, y] = c
    for x in range(0, xl + 1):
        for y in range(h):
            px[x, y] = (255, 255, 255)
    if yb:
        for x in range(w):
            for y in range(yb, h):
                px[x, y] = (255, 255, 255)
    im.save(os.path.join(SRC, 'img_%s_%s_clean.png' % (lang, name)), optimize=True)
    print(lang, name, w, h)
