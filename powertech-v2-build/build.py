# -*- coding: utf-8 -*-
"""Assemble Gridec one-page (EN+HY) from shell.html + exact site texts."""
import base64, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
# The site repo (a worktree) supplies the real fonts for the base64 preview build and
# receives the deploy pair. PT_SITE points at it.
#
# По умолчанию — своя папка, если шрифты лежат в ней: они были перенесены сюда,
# когда рабочая копия сайта перестала их отдавать, и сборка падала на первой же
# строке с FileNotFoundError. Прежний путь на соседний `assets` остаётся запасным.
_LOCAL = HERE if os.path.isdir(os.path.join(HERE, 'fonts')) else None
SITE = os.environ.get('PT_SITE') or _LOCAL or os.path.join(HERE, '..', 'assets')

FONTS = os.path.join(SITE, 'fonts')
IMGS = os.path.join(HERE, 'img')

# Счётчик посещений — Cloudflare Web Analytics. Сюда вставляется токен площадки
# из кабинета Cloudflare (Analytics & Logs → Web Analytics → gridec.am), строка
# из 32 шестнадцатеричных знаков.
#
# Пока строка пуста, скрипт в страницы НЕ попадает. Это сделано намеренно: текст
# политики конфиденциальности обещает посетителю, что аналитики нет, и обещание
# должно ломаться вместе с токеном, а не раньше. Меняя одно, проверьте другое —
# в обеих языковых версиях, раздел «Ինչ ենք հավաքում» / «Information we collect».
#
# Счётчик не ставит cookie и не собирает «отпечаток» браузера, поэтому баннера
# согласия не требует. Внешний скрипт единственный на сайте.
CF_BEACON = '7641c3a1338942c79099a92358824950'

def cf_beacon_tag():
    """Тег ровно в той форме, в какой его выдал кабинет Cloudflare.

    `type="module"` вместо `defer` — не описка: модуль и так откладывается до
    разбора документа, а форма взята у самого Cloudflare, чтобы наша сборка не
    расходилась с тем, что у них считается рабочим.
    """
    if not CF_BEACON:
        return ''
    return ('\n<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
            'data-cf-beacon=\'{"token": "%s"}\'></script>' % CF_BEACON)

def b64(path, mime):
    with open(path, 'rb') as f:
        return 'data:' + mime + ';base64,' + base64.b64encode(f.read()).decode()

def font_face(fam, weight, fn):
    return ("@font-face{font-family:'%s';font-weight:%s;font-display:swap;"
            "src:url(%s) format('woff2');}"
            % (fam, weight, b64(os.path.join(FONTS, fn), 'font/woff2')))

# Английская страница держится на двух начертаниях: Overused Grotesk на весь текст,
# заголовки и технические подписи, и пиксельный Departure Mono на показания.
# Начертание одно, ось веса 300–900 закрывает и 400, и 600, и 700 — объявляется
# диапазоном, иначе браузер начнёт подделывать жир.
#
# Archivo, Big Shoulders Display и Martian Mono больше не вшиваются: после замены на
# них не ссылается ни одно правило. Файлы оставлены в fonts на случай возврата.
FF_EN = font_face('Overused Grotesk', '300 900', 'overused-grotesk-latin.woff2')
# Departure Mono, пиксельный, SIL OFL — шрифт показаний. Вес объявлен диапазоном,
# хотя начертание одно: иначе на элементах с 600 браузер подделает жир и размажет
# пиксельные штрихи.
FF_DEP = (
    "@font-face{font-family:'Departure Mono';font-weight:100 900;font-display:swap;"
    "src:url(%s) format('woff2');}"
    % b64(os.path.join(FONTS, 'departure-mono.woff2'), 'font/woff2'))

# Правила показаний. Кегль 11 — сетка шрифта; ниже он теряет штрихи, выше мылится.
# Трекинг вдвое меньше прежнего: прежний рассчитан на узкий Martian Mono.
READOUT_EN = """
/* ============ ПОКАЗАНИЯ ============
   Пиксельный шрифт достаётся только тому, что является показанием прибора: номерам,
   счётчику и значениям. Слова остаются на прежнем — на длинных строках пиксельная
   сетка бледнеет и теряет вес рядом с основным текстом. */
.cnt,.ixp a .no,.mi .ix,.chsteps .n,.step .no,.list .n,.asg .no{
  font-family:'Departure Mono',monospace;font-size:11px;}
/* Кейс-пунктуация. Строки показаний набраны прописными, а «·» и дефис по
   умолчанию выровнены по строчным и проседают. У пиксельного шрифта функция
   case есть — включаем; у текстовой гарнитуры её нет, там не лечится. */
.cnt,.chsteps .n,.step .no,.list .n,.asg .no,.mi .ix,.ixp a .no{
  font-feature-settings:'case' 1;}
.cnt{letter-spacing:.11em;}
.ixb{letter-spacing:.05em;}
.ixp a .no,.mi .ix,.list .n,.asg .no{letter-spacing:.07em;}
.chsteps .n{letter-spacing:.09em;}
.step .no{letter-spacing:.08em;}
/* Подписи станций шкалы приборной гарнитуре НЕ достаются, хотя прежде
   доставались: 13px Departure Mono подбирались так, чтобы строчная совпала
   с основной на 16. Но это фразы, а не показания, и правило двух голосов
   говорит прямо — пиксельный шрифт не берёт предложение, которое произносит
   компания. Плюс читаемость: пиксельная сетка на 13 тяжелее грота на 16 для
   слабого зрения, сколько бы ни совпадала высота строчной. На армянской
   странице этого правила и не было — у шрифта ноль армянских знаков, — так
   что теперь обе версии набраны одинаково. */
.chsteps .inc-tag{font-family:'Departure Mono',monospace;font-size:11px;
  letter-spacing:.12em;}
/* число и слово лежат в одном элементе — слово возвращается прежнему шрифту */
.ixb .sheet{font-family:%(mono)s;font-size:12px;letter-spacing:.1em;}
"""

# На армянской странице — только цифровой слой: армянских букв у шрифта нет, поэтому
# кольцо остаётся на Arian AMU Serif, а в показании цифры берутся отдельно от слов.
READOUT_HY = """
/* ============ ПОКАЗАНИЯ ============
   Только цифры: армянского у пиксельного шрифта нет, слова остаются прежними. */
.cnt,.ixp a .no,.mi .ix,.chsteps .n,.step .no,.list .n,.asg .no,.ixb b,.ixb em{
  font-family:'Departure Mono',monospace;font-size:11px;}
/* Кейс-пунктуация. Строки показаний набраны прописными, а «·» и дефис по
   умолчанию выровнены по строчным и проседают. У пиксельного шрифта функция
   case есть — включаем; у текстовой гарнитуры её нет, там не лечится. */
.cnt,.chsteps .n,.step .no,.list .n,.asg .no,.mi .ix,.ixp a .no{
  font-feature-settings:'case' 1;}
.cnt{letter-spacing:.11em;}
.ixp a .no,.mi .ix,.list .n,.asg .no{letter-spacing:.07em;}
.chsteps .n{letter-spacing:.09em;}
.step .no{letter-spacing:.08em;}
"""

MONO_EN = "'Overused Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO_HY = "'Mardoto','Arian AMU','Helvetica Neue',sans-serif"
# У Arian AMU есть только Regular и Bold. Прежняя запись «400 500» отдавала Regular и на
# 500 под видом отдельного Medium; объявлено честно — 400. Запрос 500 берёт ближайший.
ARIAN_REG = '400'
# ---------------------------------------------------------------- typography (вариант A, 2026-09-13)
# Английские заголовки в обычном регистре (был сплошной капс), интерлиньяж 1.02 (был .92),
# уплотнение −.015em; крупные h2 разделов 01 и 08 — −.022em. Армянские заголовки без
# отрицательного трекинга. Числа прозы — в :root shell.html. Пробовался и Inter (вариант B);
# владелец выбрал сохранить Overused Grotesk.
_OG = "'Overused Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif"
# Трекинг заголовков 0 (было −.015/−.022em: владелец — «слишком близко буквы»), интерлиньяж 1.05.
TY = dict(EN_BODY=_OG, EN_HEAD=_OG, EN_TT='', EN_LH='1.05', EN_LS='0', EN_H1WT='700', EN_BIGLS='0', HY_LS='0')


# Аудит 2026-09-14: армянская страница целиком на Mardoto — 400 для прозы, 500 для
# заголовков и подписей, 700 для полужирного. Настоящие файлы (подмножества из
# github.com/vahanhovh/mardoto), браузер жир не подделывает. Arian AMU остаётся запасным
# семейством в стеке; Arian AMU Serif из интерфейсных подписей убран.
FF_HY = '\n'.join([
    font_face('Mardoto', '400', 'mardoto-400.woff2'),
    font_face('Mardoto', '700', 'mardoto-700.woff2'),
    font_face('Arian AMU', ARIAN_REG, 'arian-amu-400.woff2'),
    font_face('Arian AMU', '600 900', 'arian-amu-700.woff2'),
    # Mardoto Medium (SIL OFL, github.com/vahanhovh/mardoto) — заголовки армянской
    # страницы весом 500: владелец выбрал из проб 300/400/500 (2026-09-13). Подмножество:
    # латиница, армянский, пунктуация. Один вес, поэтому объявлен точкой 500.
    font_face('Mardoto', '500', 'mardoto-500.woff2'),
])

IMG_FILES = ['02_manufacturing_industrial_robot.jpg', '03_solar_power_plant.jpg',
             '06_healthcare_laboratory.jpg', '05_data_center.jpg',
             '04_commercial_building.jpg', '08_finance_investment.jpg']
# Карточка ленты показывает снимок в 378px, а файл лежит в 1536 — запас вчетверо,
# то есть вчетверо больше данных, чем нужно. Рядом кладём вариант в 756: ровно ×2
# под плотные экраны, и карточка выбирает его сама через srcset.
# Оригинал НЕ уменьшаем: модалка показывает его на 880, и там 1536 — это ×1.75,
# уже меньше нормы. Исправить это можно только более крупными исходниками.
IMG_SMALL_W = 756
IMG_SMALL = [os.path.splitext(f)[0] + '-756.jpg' for f in IMG_FILES]
# Готовые снимки лежат отдельно от исходников: в них ЗАПЕЧЁН дуотон, и путать их
# с оригиналами нельзя — повторное запекание сожмёт шкалу второй раз.
IMGS_OUT = os.path.join(IMGS, '_duo')

def make_small_images():
    """Готовит оба размера и ЗАПЕКАЕТ в них дуотон.

    Раньше дуотон собирался в браузере: фильтр на снимке, lighten над тёмной
    подложкой, darken светлым слоем сверху. Три действия на снимок, шесть снимков,
    и всё это заново НА КАЖДОМ КАДРЕ прокрутки — отсюда лаги. Теперь та же
    арифметика делается один раз здесь; вёрстка просто показывает картинку.
    """
    from PIL import Image
    import duotone
    if not os.path.isdir(IMGS_OUT):
        os.makedirs(IMGS_OUT)
    for src_name, small_name in zip(IMG_FILES, IMG_SMALL):
        src = os.path.join(IMGS, src_name)
        if not os.path.exists(src):
            continue
        big_out = os.path.join(IMGS_OUT, src_name)
        small_out = os.path.join(IMGS_OUT, small_name)
        fresh = (os.path.exists(big_out) and os.path.exists(small_out)
                 and min(os.path.getmtime(big_out), os.path.getmtime(small_out))
                 >= os.path.getmtime(src))
        if fresh:
            continue
        im = duotone.apply(Image.open(src))
        im.save(big_out, 'JPEG', quality=84, optimize=True, progressive=True)
        h = round(im.height * IMG_SMALL_W / im.width)
        im.resize((IMG_SMALL_W, h), Image.LANCZOS).save(
            small_out, 'JPEG', quality=82, optimize=True, progressive=True)
        print('  %s %dx%d + %dx%d, дуотон запечён'
              % (src_name, im.width, im.height, IMG_SMALL_W, h))
def b64_small(path, maxw=1800, quality=82):
    """Вшитая копия снимка, уменьшенная до maxw.

    Самый крупный вывод фотографии — модалка отрасли, 880x385 CSS, то есть 1760 px при
    экране 2x. Оригиналы 2400 px в base64 дают около 8 МБ на страницу без видимой
    разницы. Деплойная сборка ссылается на файлы и получает полный размер. Без Pillow
    вшиваем как есть, чтобы сборка не падала.
    """
    try:
        from PIL import Image
    except ImportError:
        return b64(path, 'image/jpeg')
    im = Image.open(path)
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')


IMGD = {'IMG%d' % i: b64_small(os.path.join(IMGS, f)) for i, f in enumerate(IMG_FILES)}

def stats_html(items):
    return ''.join('<div class="stat"><b>%s</b><span>%s</span></div>' % (b, s) for b, s in items)

# Указатель разделов в подвале собирается из тех же строк, что стоят на самих
# разделах: копия не разъедется с страницей и переводится сама.
FOOT_IDS = [('why', 'WHY_H2'), ('applications', 'APP_H2'), ('services', 'SVC_H2'),
            ('report', 'REP_H2'), ('assignments', 'ASG_H2'), ('measure', 'MEA_H2'),
            ('company', 'CO_H2')]  # 'contact' снят из списка разделов подвала — владелец (2026-09-14)

def foot_links(d):
    out = []
    for sid, tok in FOOT_IDS:
        t = re.sub(r'<[^>]+>', ' ', d[tok])
        t = re.sub(r'\s+', ' ', t).strip()
        # Номер из списка снят: рядом стоит название раздела, а ссылкой цифра
        # здесь не была — те же 01…08 печатались на странице трижды (счётчик,
        # панель, подвал), и от трёх копий ни одна не читается адресом.
        out.append('<li><a href="#%s"><span>%s</span></a></li>' % (sid, t))
    return ''.join(out)

# ---------------------------------------------------------------- висячие слова
# Встроенный в шрифт типограф работает внутри строки и переносить слова не умеет.
# Короткие служебные слова приклеиваются к следующему здесь, при сборке.
# Разметку не трогаем: строка режется на теги и текст, меняется только текст.
NB = ' '   # шаблон замены в re.sub не понимает \uXXXX
# Только служебные слова. Вопросительные и знаменательные («how», «what», «with»)
# не приклеиваем: в крупном заголовке это создаёт длинные неразрывные куски,
# а кончать ими строку не грех.
# Английский список пуст намеренно. Склейка после предлога — правило русской и
# армянской типографики; в английском его нет, и «the·system·is·operating» ломало
# переносы там, где браузер справляется сам. Число с единицей склеивает UNIT ниже —
# это правило языконезависимо и остаётся в силе.
GLUE_EN = ''
GLUE_HY = 'և ու թե որ կամ ըստ ի մեր ձեր այս այն'
UNIT = re.compile(r'(\d)\s+(?=[A-Za-z\u0530-\u058F%])')

def _glue(text, words):
    for w in words.split():
        text = re.sub(r'(?<![\w\u0530-\u058F])(' + w + r')\s+(?=[\w\u0530-\u058F(])',
                      '\\1' + NB, text, flags=re.IGNORECASE)
    return UNIT.sub('\\1' + NB, text)

def nbsp(value, lang):
    """Склеивает короткие слова с последующим и число с единицей."""
    if not isinstance(value, str) or '%%' in value:
        return value
    words = GLUE_HY if lang == 'hy' else GLUE_EN
    return ''.join(part if part.startswith('<') else _glue(part, words)
                   for part in re.split(r'(<[^>]*>)', value))

# Технические строки: пути, размеры, гарнитуры, готовые блоки разметки.
NO_GLUE = {'LANG', 'LANG_HREF', 'LANG_LABEL', 'FONTFACES', 'READOUT', 'BODYFONT',
           'HEADFONT', 'HEADWT', 'H1WT', 'BIGLS', 'MONOFONT', 'NAVFONT', 'HEADTT', 'HEADLH', 'HEADLS',
           'H1SIZE', 'H2SIZE', 'DISPSIZE', 'SVC_STATS', 'SVC_STEPS', 'REP_LIST',
           'CO_STORY', 'ASG_CARDS', 'ASG_PICS', 'MEA_CELLS', 'FOOT_LINKS', 'META_DESC',
           'REP_NOTE2', 'MEA_NOTE', 'IX_LABEL', 'IX_ARIA'}
# PP_BODY намеренно НЕ здесь: nbsp разбирает строку по тегам и правит только
# текст между ними, а числу с единицей («24 месяца», «30 дней») склейка нужна
# ровно так же, как в остальном наборе.

def steps_html(items):
    """Шаг — это фраза, без названия и без номера.

    Название повторяло первые слова самого абзаца: каждый из шести начинается
    с действия и читается сам по себе.

    Номер в разметку не идёт (см. «одна нумерация» в DESIGN.md): три шага стоят
    в ряд слева направо, и порядок виден без цифры. В данных он оставлен —
    он документирует последовательность, и решение обратимо одной строкой.
    """
    return ''.join('<div class="step"><p>%s</p></div>' % p for _n, p in items)

def list_html(items):
    return ''.join('<div><span>%s</span></div>' % x for x in items)

def intro_html(text):
    """Вводная строка формы. Пустое значение не оставляет пустого абзаца с полями."""
    return '<p class="intro">%s</p>' % text if text else ''

def lnote_html(text):
    """Строка под блоком. Пустое значение не печатает и самой обёртки.

    Нужна там, где утверждение вынесено из перечня: пункт списка читается
    услугой, а то же самое отдельной строкой — позицией. Армянская версия
    пока без неё, поэтому пустая строка обязана давать пустой вывод, а не
    висящий абзац с полями.
    """
    return '<p class="lnote">%s</p>' % text if text else ''

def pp_html(items):
    """Разделы политики: марка раздела и один-два абзаца под ней.

    Номеров нет намеренно. На странице одна система нумерации — счётчик
    разделов, — и заводить вторую внутри служебного окна значило бы её
    сломать: документ не является девятым разделом сайта.
    """
    return ''.join(
        '<section class="pps"><h4>%s</h4>%s</section>'
        % (head, ''.join('<p>%s</p>' % p for p in paras))
        for head, paras in items)

# Раздел 05 — вопросы владельца (бриф 2026-09-12). Пять иллюстраций типовых
# ситуаций — сгенерированные картинки, не фотографии выполненных проектов.
QA_IMGS = ['01-generator-ups', '02-lift-hvac-pumps', '03-production-expansion',
           '04-motor-monitoring', '05-baseline-measurements']

def qa_html(items):
    """Пять вопросов: кнопка (номер, вопрос, плюс) и ответ (абзац, подпись
    услуги, на телефоне — картинка). Открытый по умолчанию задаёт скрипт (02)."""
    out = []
    for i, (q, a, svc, alt) in enumerate(items):
        n = '%02d' % (i + 1); img = QA_IMGS[i]
        out.append(
            '<li class="qa-item">'
            '<button class="qa-q" type="button" id="qa-b%d" aria-expanded="false" aria-controls="qa-a%d">'
            '<span class="qa-n tag">%s</span><span class="qa-t">%s</span><span class="qa-pm" aria-hidden="true"></span></button>'
            '<div class="qa-a" id="qa-a%d" role="region" aria-labelledby="qa-b%d" hidden><div>'
            '<p>%s</p><span class="qa-svc tag">%s</span>'
            '<div class="qa-pic-m"><img src="./uploads/qa/%s-724.webp" width="724" height="543" alt="%s" loading="lazy" decoding="async"></div>'
            '</div></div></li>' % (i, i, n, q, i, i, a, svc, img, alt))
    return ''.join(out)

def qa_pics(items):
    """Стопка пяти картинок в левой колонке; видна одна — активная."""
    return ''.join('<img src="./uploads/qa/%s.webp" width="1448" height="1086" alt="%s" decoding="async"%s>'
                   % (QA_IMGS[k], it[3], ' fetchpriority="low"' if k != 1 else '') for k, it in enumerate(items))

# Each parameter gets its own measurement signature. Drawn to the owner's sketches
# (2026-07-28) in the site's own hairline language: one stroke weight, currentColor for
# the structure and var(--brand) for the single accent, so every icon inherits the page
# palette and inverts on the dark plates. No gradients, no fills, nothing that needs a
# raster. They render at 52x34 CSS pixels, which is what settles most of the detail
# decisions below.
MEAS_ICONS = [
 # 01 voltage & current — three linked loops crossing one axis, the middle phase lit
 '<g fill="none" stroke="currentColor" stroke-width="1.1">'
 '<ellipse cx="13" cy="15" rx="6.6" ry="10.4"/><ellipse cx="31" cy="15" rx="6.6" ry="10.4"/></g>'
 '<ellipse cx="22" cy="15" rx="6.6" ry="10.4" fill="none" stroke="var(--brand)" stroke-width="1.4"/>'
 '<g stroke="currentColor" stroke-width="1.1" stroke-linecap="round" opacity=".7">'
 '<path d="M2.5 15h10"/><path d="M31.5 15h10"/></g>'
 '<path d="M19 15h6" stroke="var(--brand)" stroke-width="1.7" stroke-linecap="round"/>',
 # 02 harmonics — a decaying spectrum, the third order carrying the accent
 '<path d="M2 21h40" stroke="currentColor" stroke-width="1" opacity=".5"/>'
 '<g fill="none" stroke="currentColor" stroke-width="1">'
 '<rect x="8" y="4" width="3" height="19"/><rect x="13" y="7" width="3" height="16"/>'
 '<rect x="23" y="13" width="3" height="10"/><rect x="28" y="16" width="3" height="7"/>'
 '<rect x="33" y="18.4" width="3" height="4.6"/></g>'
 '<rect x="18" y="10" width="3" height="13" fill="var(--brand)"/>',
 # 03 flicker — the fluctuation held between two limit lines
 '<g stroke="currentColor" stroke-width="1" opacity=".38" stroke-dasharray="3 3">'
 '<path d="M4 8h36"/><path d="M4 22h36"/></g>'
 '<path d="M4 15c2 4 4 4 6 0s4-6 6 0 4 8 6 0 4-6 6 0 4 4 6 0" fill="none" stroke="currentColor" stroke-width="1.4"/>'
 '<path d="M4 15c2 4 4 4 6 0s4-6 6 0 4 8 6 0" fill="none" stroke="var(--brand)" stroke-width="1.4"/>',
 # 04 voltage dip — a smooth sag that recovers short of where it started,
 #    with the accent marking the depth it reached
 '<path d="M2 10c6 0 7 13 13 13s6-6 12-6 9 1 15 1" fill="none" stroke="currentColor" '
 'stroke-width="1.4" stroke-linecap="round"/>'
 '<path d="M12.5 23h9" stroke="var(--brand)" stroke-width="2.2" stroke-linecap="round"/>',
 # 05 unbalance — a star point whose lit phase runs long
 '<g stroke="currentColor" stroke-width="1.4" stroke-linecap="round">'
 '<path d="M22 15.5 13.5 21"/><path d="M22 15.5 30.5 21"/></g>'
 '<g fill="currentColor"><circle cx="13.5" cy="21" r="1.9"/><circle cx="30.5" cy="21" r="1.9"/></g>'
 '<path d="M22 15.5V4" stroke="var(--brand)" stroke-width="1.6" stroke-linecap="round"/>'
 '<circle cx="22" cy="4" r="2" fill="var(--brand)"/>'
 '<circle cx="22" cy="15.5" r="2.1" fill="currentColor"/>',
 # 06 power & energy — the area accumulated under the curve, closed by the accent
 '<path d="M2 24c8 0 10-13 18-13s10 8 22 4v9z" fill="currentColor" opacity=".14"/>'
 '<path d="M2 24c8 0 10-13 18-13s10 8 22 4" fill="none" stroke="currentColor" stroke-width="1.4"/>'
 '<path d="M2 24h40" stroke="var(--brand)" stroke-width="1.6"/>',
 # 07 events — a transient on a quiet line, flagged
 '<path d="M2 18h14l3-13 3.4 22 2.6-9h17" fill="none" stroke="currentColor" '
 'stroke-width="1.4" stroke-linejoin="round"/>'
 '<rect x="27" y="10.5" width="3" height="5.4" rx=".9" fill="var(--brand)"/>',
 # 08 risk indicators — NOT an electrical parameter: a trend read off the baseline
 #    whose latest point is flagged. This is the one card that draws a conclusion
 #    rather than a measurement, which is why its cell is marked (.mi-alt).
 '<g stroke="currentColor" stroke-width=".8" opacity=".26">'
 '<path d="M8 21v5"/><path d="M14 18v8"/><path d="M20 20v6"/><path d="M26 14v12"/>'
 '<path d="M32 16v10"/></g>'
 '<path d="M3 24 8 21 14 18 20 20 26 14 32 16 37 11" fill="none" stroke="currentColor" '
 'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'
 '<g fill="currentColor"><circle cx="8" cy="21" r="1.4"/><circle cx="14" cy="18" r="1.4"/>'
 '<circle cx="20" cy="20" r="1.4"/><circle cx="26" cy="14" r="1.4"/><circle cx="32" cy="16" r="1.4"/></g>'
 '<circle cx="37" cy="11" r="2.5" fill="none" stroke="var(--brand)" stroke-width="1.6"/>'
 #    (the sketch's exclamation mark inside the triangle is dropped: at this size the
 #    notch would need the ground colour, which differs between the light and dark
 #    surfaces the grid can sit on, and a 1px sliver reads as dirt either way)
 '<path d="M37 1.4 40.1 6.8h-6.2z" fill="var(--brand)"/>',
]

def meas_html(items, alt=0):
    """`alt` = how many trailing cells are not electrical parameters. They get .mi-alt,
    which sets them apart from the measured quantities without inventing any copy."""
    out = []
    for i, label in enumerate(items):
        cls = 'mi mi-alt' if i >= len(items) - alt else 'mi'
        # Порядкового номера у ячейки нет: сетка величин не упорядочена, а её
        # 01–08 совпадали с 01–08 счётчиков разделов — на странице получалось
        # два разных «05» одним и тем же моно.
        out.append('<div class="%s">'
                   '<svg viewBox="0 0 44 30" aria-hidden="true">%s</svg>'
                   '<span class="mlb">%s</span></div>'
                   % (cls, MEAS_ICONS[i % len(MEAS_ICONS)], label))
    return ''.join(out)

def chips_html(items):
    return ''.join('<span>%s</span>' % x for x in items)

def story_html(items):
    """Глава истории компании: подпись с номером и абзац.

    Утверждения-заголовки сняты: они повторяли смысл абзаца, а три подряд
    читались шаблоном. Осталась подпись, которая сидит прямо на волосяной
    линии, и сам текст.
    """
    return ''.join('<div class="sb rv"><div class="lb"><span>%s</span></div>'
                   '<p>%s</p></div>' % (n, p) for n, p in items)

# ---------------------------------------------------------------- EN
EN = {
 # Страна в заголовке не для красоты: услугу ищут вместе с ней — «power quality
 # monitoring armenia», — а до сих пор в title стояли только два слова из трёх.
 # Армянский заголовок оставлен как был: тот, кто ищет по-армянски, страну не
 # набирает, а Google и без того обрезал его по ширине.
 'LANG': 'en', 'TITLE': 'Gridec | Power Quality Monitoring in Armenia',
 'META_DESC': 'Seven-day power quality monitoring in Armenia. We measure under representative load and report the findings.',
 'FONTFACES': FF_EN + '\n' + FF_DEP,
 'READOUT': READOUT_EN % dict(mono=MONO_EN),
 'BODYFONT': TY['EN_BODY'],
 'HEADFONT': TY['EN_HEAD'], 'HEADWT': '700',
 'MONOFONT': MONO_EN,
 'NAVFONT': 'inherit',
 'HEADTT': TY['EN_TT'], 'HEADLH': TY['EN_LH'], 'HEADLS': TY['EN_LS'], 'H1WT': TY['EN_H1WT'], 'BIGLS': TY['EN_BIGLS'],
 # Шкала умножена на 0,66: узкий Big Shoulders сменился нормальным по ширине
 # гротеском, и при прежнем кегле строка героя выходила из колонки в полтора раза.
 'H1SIZE': 'clamp(48px,4.6vw,74px)', 'H2SIZE': 'clamp(20px,3.17vw,48px)',
 'DISPSIZE': 'clamp(23px,3.96vw,55px)',
 # Латинский код, а не «ՀԱՅ»: в EN-сборку вшита только латинская подрезка Martian
 # Mono, армянские буквы падали в системную подмену и выглядели чужеродно. Пара
 # переключателя заодно стала симметричной — на HY-странице стоит «EN».
 'LANG_HREF': './hy.html', 'LANG_LABEL': 'ARM', 'LANG_ARIA': 'Հայերեն · Armenian',
 'NAV_SERVICES': 'Services', 'NAV_INDUSTRIES': 'Industries', 'NAV_COMPANY': 'Company',
 'IX_LABEL': 'Index', 'IX_ARIA': 'Section index',
 'CTA': 'Describe the issue', 'NAV_CTA': 'Get in touch',
 'HERO_EYEBROW': 'POWER QUALITY MONITORING',
 'HERO_H1': 'See how your<br>electrical system<br><span class="ac">performs</span>',
 'HERO_P': 'Gridec records power quality parameters while your electrical system is running, and inspects the installation on site. The report presents our findings and recommended next steps.',
 'HERO_CTA2': 'When measurements help',
 'HERO_PHOTO_ALT': 'Illustration of power quality monitoring with Rogowski coils and a portable analyzer at an electrical switchboard.',
 # Надпись на панели щита (бриф 2026-09-14): описание услуги, по одной строке.
 'HERO_MARK1': 'MEASURE', 'HERO_MARK2': 'ANALYSE', 'HERO_MARK3': 'RECOMMEND',
 # Поле героя: форма волны напряжения. Подписи по брифу владельца, дословно.
 'WHY_H2': 'Power supply problems are not always obvious',
 'WHY_P': 'A voltage dip can last only a few cycles. A later spot check may show normal readings. Continuous monitoring records the event and when it occurred, allowing us to analyse the measured conditions.',
 'APP_H2': 'Where monitoring helps',
 'APP_P': 'Monitoring helps when power quality affects equipment or operations, or when you need measurements to make a technical decision.',
 'OTHER_T': 'Other Critical Electrical Systems',
 'OTHER_P': 'Do not see your sector here? Describe the issue and the equipment affected. Monitoring is defined by the technical question, not by the sector alone.',
 'SVC_H2': 'Seven-day monitoring',
 'SVC_P1': 'Power quality data is recorded during actual operation and interpreted in the context of the issue being investigated.',
 'SVC_P2': 'The monitoring period is selected to obtain a representative record of operating conditions. We recommend a longer period when the issue is intermittent or the operating cycle needs more time.',
 # Ряд отвечает на три вопроса заказчика по порядку: сколько это длится, насколько
 # непрерывно и что он получит в конце. Третья ячейка — деливерабл, и «1» здесь не
 # затычка под ряд: она обещает один документ с выводами, а не выгрузку данных.
 #
 # Однажды на её месте стояло «200 ms» (базовое окно по IEC 61000-4-30). Число
 # честное, но оно с другой оси — разрешение прибора, — и ряд от него терял смысл:
 # владелец такого вопроса не задаёт. Место технического метода — примечание к
 # разделу 04, рядом с Class S, а не ряд, адресованный владельцу.
 'SVC_STATS': stats_html([('7', 'Days of monitoring'),
                          ('24/7', 'Continuous data recording'),
                          ('1', 'Engineering report')]),
 'SVC_DISPLAY': 'Measured<br>under actual<br><span class="ac">load</span>',
 'SVC_STEPS': steps_html([
    ('01', 'Before monitoring starts, we agree on the equipment to assess, the measurements required and the decision the results will support.'),
    ('02', 'We take measurements during the agreed operating conditions.'),
    ('03', 'We analyse the recorded data and present our conclusions and recommended next steps in the report.')]),
 'SVC_LINK': 'See what monitoring can reveal',
 'REP_H2': 'Report',
 'REP_P': 'Measurement results, engineering analysis and conclusions provide the basis for further technical decisions.',
 'REP_NOTE': 'Power quality parameters are measured using IEC 61000-4-30 Class S methods. Harmonic and interharmonic measurements are evaluated using IEC 61000-4-7 where applicable.',
 # «Limitations of the available evidence» из перечня снят: оговорка, стоящая
 # пунктом среди состава отчёта, читается страховкой. Тот же смысл строкой под
 # списком читается позицией — и заодно ломает ряд из шести одинаковых по длине
 # именных групп.
 'REP_LIST': list_html(['Measurement scope and points', 'Monitoring period and operating conditions',
                        'Recorded events and trends', 'Engineering interpretation',
                        'Recommended next steps']),
 'REP_NOTE2': lnote_html('Where the record does not support a conclusion, the report says so.'),
 # Раздел адресован владельцу, а не инженеру, и должен отвечать на «чем это полезно
 # мне», а не «что мы делаем». Отрасли уже названы в 02, запись и отчёт — в 01 и 04,
 # поэтому здесь ни то, ни другое не может быть сообщением: каждая карточка ставится
 # в момент, когда владелец вот-вот потратит деньги, и говорит, что измерение в этот
 # момент меняет. Отсюда сквозное «Before you ...» — четыре точки перед тратой.
 # Границы ролей соблюдены: цифры отдаются проектировщику, ответственность —
 # подрядчику, стоимость работ мы не считаем.
 'ASG_H2': 'Engineering challenges',
 'ASG_P': 'From capacity assessment to fault investigation.',
 'ASG_CARDS': qa_html([('Choosing a generator or UPS? What load will it need to support?', 'We measure the operating load and starting currents of the equipment that needs backup power under agreed operating conditions. These measurements help your supplier select the required capacity.', 'Temporary monitoring', 'Illustration: a standby generator and UPS cabinets in a plant room'), ('Installing a lift, air conditioning and pumps? How will they work together?', 'We record electrical loads and voltage changes as the systems start up and operate together under agreed test conditions. The results help assess whether changes are needed to the electrical system or start-up sequence.', 'Temporary monitoring', 'Illustration: a pump room with motors, pipework and control cabinets'), ('Adding a production line? Can your existing electrical system support it?', 'We measure the existing load and peak demand. Your electrical designer can use these findings alongside the new equipment’s requirements to assess available capacity and plan any necessary upgrades.', 'Temporary monitoring', 'Illustration: a production hall with a new machine line'), ('Your supplier says a power supply issue caused the failure. How can you check?', 'Permanent monitoring records electrical conditions before and during a failure. If monitoring was already in place when the failure occurred, Gridec can analyse the recorded data to help assess your supplier’s explanation.', 'Permanent monitoring', 'Illustration: an electric motor with a monitoring instrument connected'), ('Signing off on new equipment? What should you record at start-up?', 'We measure electrical parameters and load under agreed operating conditions. The report helps you review the results with your supplier before acceptance and provides a baseline for investigating future changes or faults.', 'Temporary monitoring', 'Illustration: measurements at the switchboard during equipment start-up')]),
 'ASG_PICS': qa_pics([('Choosing a generator or UPS? What load will it need to support?', 'We measure the operating load and starting currents of the equipment that needs backup power under agreed operating conditions. These measurements help your supplier select the required capacity.', 'Temporary monitoring', 'Illustration: a standby generator and UPS cabinets in a plant room'), ('Installing a lift, air conditioning and pumps? How will they work together?', 'We record electrical loads and voltage changes as the systems start up and operate together under agreed test conditions. The results help assess whether changes are needed to the electrical system or start-up sequence.', 'Temporary monitoring', 'Illustration: a pump room with motors, pipework and control cabinets'), ('Adding a production line? Can your existing electrical system support it?', 'We measure the existing load and peak demand. Your electrical designer can use these findings alongside the new equipment’s requirements to assess available capacity and plan any necessary upgrades.', 'Temporary monitoring', 'Illustration: a production hall with a new machine line'), ('Your supplier says a power supply issue caused the failure. How can you check?', 'Permanent monitoring records electrical conditions before and during a failure. If monitoring was already in place when the failure occurred, Gridec can analyse the recorded data to help assess your supplier’s explanation.', 'Permanent monitoring', 'Illustration: an electric motor with a monitoring instrument connected'), ('Signing off on new equipment? What should you record at start-up?', 'We measure electrical parameters and load under agreed operating conditions. The report helps you review the results with your supplier before acceptance and provides a baseline for investigating future changes or faults.', 'Temporary monitoring', 'Illustration: measurements at the switchboard during equipment start-up')]),
 'MEA_H2': 'What we measure',
 # «Voltage Dips» → «Dips & Swells»: кольцо в герое обещало и перенапряжения, а
 # сетка их не называла, и объём измерений не сходился сам с собой.
 'MEA_CHIPS': meas_html(['Voltage & Current', 'Harmonics & Interharmonics', 'Flicker',
                          'Dips & Swells', 'Unbalance', 'Power & Energy', 'Events',
                          'Risk Indicators'], alt=1),
 # Восьмая ячейка уже отделена начертанием (.mi-alt: штриховые линейки, засечка
 # в углу) — но подпись всё равно стоит в том же типографском гнезде, что и семь
 # величин, и читается восьмой измеряемой. Строка под сеткой договаривает то, что
 # оформление показывает.
 'MEA_NOTE': lnote_html('We assess potential equipment risks using the recorded data and operating conditions.'),
 'CO_H2': 'About us',
 'CO_P': 'Gridec is an independent electrical engineering company based in Yerevan. We are a small team focused on specialised engineering work and long-term cooperation with our partners.',
 # \u041f\u0435\u0440\u0435\u043d\u043e\u0441\u044b \u0432 \u0443\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f\u0445 \u0437\u0430\u0434\u0430\u043d\u044b \u0437\u0430\u043a\u0430\u0437\u0447\u0438\u043a\u043e\u043c \u043f\u043e\u0441\u0442\u0440\u043e\u0447\u043d\u043e \u0438 \u0441\u0442\u043e\u044f\u0442 \u0440\u0430\u0437\u043c\u0435\u0442\u043a\u043e\u0439, \u0430 \u043d\u0435
 # \u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u044b \u043d\u0430 \u0432\u043e\u043b\u044e \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f.
 # Номера «01 ·», «02 ·», «03 ·» с подписей сняты: на странице уже есть одна
 # система нумерации — счётчики разделов 01–08, — и вложенная вторая внутри
 # седьмого раздела читалась шаблоном, а не структурой.
 'CO_STORY': story_html([
    ('WHY WE STARTED',
     'Specialist measurements and analysis should not require a permanent in-house team or equipment that spends most of its time unused. Gridec gives companies access to both when the need arises.'),
    ('HOW WE WORK',
     'A useful investigation starts with the question that needs answering. We measure the system under real operating conditions and base the conclusion on what the data shows, whether that points to a problem or confirms normal operation.'),
    ('WHAT WE ARE BUILDING',
     'We are building Gridec in Armenia as a small engineering firm whose conclusions hold up when someone checks them. We would rather grow slowly than lose that.')]),
 'CT_H2': 'Start with what happened',
 # Кривая провала нарисована руками, а не снята прибором. Под подписью «TYPICAL
 # TRACE» «180 MS» читается примером и вопроса «где запись» не вызывает.
 'CT_CAP': 'RMS voltage · illustrative example', 'CT_NOM': 'NOMINAL', 'CT_DIP': 'VOLTAGE DIP · 180 MS',
 'CO_LEGAL': 'Gridec LLC',
 # ՀՎՀՀ — армянский учётный номер налогоплательщика. По-английски он
 # передаётся как TIN (Taxpayer Identification Number): именно так его
 # называет Комитет госдоходов в своих англоязычных документах.
 # НЕ «VAT»: регистрация по НДС в Армении отдельная и номер у неё другой.
 'CO_TIN_LB': 'TIN', 'CO_TIN': '08331059',
 'FOOT_ADDR': 'Davtashen 1, 13-25, Yerevan 0058, Armenia',
 'FOOT_SECTIONS': 'Sections', 'FOOT_CONTACT': 'Contact',
 'FOOT_HOURS': 'Mon-Fri 09:00-18:00 (UTC+4)',
 'IM_FINDLB': 'What the report can address',
 'F_H3': 'Describe the <span class="ac">electrical issue</span>',
 # Вводная строка снята: она слово в слово повторяла подсказку в поле «What
 # happened?» двумя сантиметрами ниже. Пустое значение не печатает и абзаца.
 'F_INTRO': intro_html(''),
 'F_CONTACT': 'Contact details',
 'F_NAME': 'Name', 'F_NAME_PH': 'Your name',
 'F_COMPANY': 'Company', 'F_COMPANY_PH': 'Company name',
 'F_EMAIL': 'Email', 'F_PHONE': 'Phone',
 'F_APP': 'Sector',
 'F_WHAT': 'What happened?',
 'F_MSG_PH': 'Briefly describe what happened, when you noticed it, and which equipment is involved.',
 'F_ATT': 'Attachments', 'F_ATT_OPT': 'optional',
 'F_DROP1': 'Attach a file or drop it here',
 'F_DROP2': 'Photos, diagrams, reports, or equipment data',
 'F_SIZE_ERR': 'Attachments exceed the 10 MB limit. Please remove some files.',
 'F_HINT0': 'Up to 10 MB',
 'F_FORM_ERR': 'Please check the highlighted fields.',
 # Аудит 2026-09-14: обязательны имя, описание и один контакт (почта ИЛИ телефон).
 'F_ONE_CONTACT': 'Email or phone: at least one, so that we can reply.',
 'F_SEND_ERR': 'Sending failed. Please check your connection and try again, or write to us directly: sales@gridec.am',
 'F_SEND': 'Send',
 # Имя кнопки закрытия: символ «×» экранный диктор читает как знак умножения
 'A_CLOSE': 'Close',
 'F_OK_T': 'Thank you.',
 'F_OK_P': 'We will review your enquiry and contact you to clarify the details.',
 'F_CLOSE': 'Close',
 # ---- политика конфиденциальности ----
 # Разделы взяты по образцу, который прислал владелец (earlyone.com/privacy-policy):
 # тот же порядок тем, принятый для армянской компании. Текст свой: у образца
 # платформа с приложением, аналитикой и интеграциями, у нас — статическая
 # страница с одной формой, и половина его разделов описывала бы то, чего нет.
 #
 # Два места, где мы сознательно строже образца. Срок хранения назван числом,
 # а не оборотом «сколько потребуется»: неопределённый срок проверить нельзя.
 # Закон назван по имени, и назван надзорный орган: именно это ищет читатель,
 # ради которого документ и заводился.
 'PP_LINK': 'Privacy',
 'PP_H3': 'Privacy Policy',
 'PP_LEDE': 'This policy explains what happens to information you send us through this '
            'website. It covers this site only, and it describes what the site actually '
            'does.',
 'PP_BODY': pp_html([
  ('Who we are', [
   'Gridec LLC, Davtashen 1, 13-25, Yerevan 0058, Armenia. Taxpayer identification '
   'number 08331059.',
   'Gridec LLC determines the purposes and the means of processing the personal data '
   'described here, and is the controller of that data.']),
  ('Information we collect', [
   'The site has one form. It collects your name, company, email address, phone number, '
   'the sector you select, your description of the issue, and any files you attach to it.',
   'Please do not attach identity documents, health records or other sensitive personal '
   'data unless your enquiry genuinely requires them.',
   'We count visits with Cloudflare Web Analytics. It sets no cookies, does not '
   'fingerprint visitors and does not follow you across other sites. What we see is '
   'aggregate — page views, referring sites, country, browser and device type — not '
   'individual people.',
   'We run no advertising systems and no other third-party trackers.',
   'While the site is served, our hosting provider may automatically record ordinary '
   'technical data such as the IP address, the time of a request or technical details '
   'about the browser. We do not use that to analyse visitor behaviour or for '
   'advertising.']),
  ('How we use it', [
   'To answer your enquiry, to clarify what needs measuring, to prepare a quotation, and '
   'to arrange the follow-up. We do not use your details for marketing, and we '
   "do not sell them or share them for anyone else's purposes."]),
  ('Legal basis', [
   'By completing and sending the form, you give us these details so that we can handle '
   'your enquiry and reply to you. That is what we use them for.',
   'Where the General Data Protection Regulation (GDPR) applies to you, the relevant '
   'legal bases may be Article 6(1)(b) and Article 6(1)(f).']),
  ('Data sharing', [
   'The form reaches us through FormSubmit (formsubmit.co). The contents of the form, '
   'including any attachments, are processed by that service to the extent needed to '
   'deliver your enquiry to our mailbox. FormSubmit is a third-party service, and that '
   'processing may take place outside Armenia. The resulting message is then held with '
   'our email provider.',
   'The technical data behind the visit count is processed by Cloudflare as our service '
   'provider.',
   'We do not pass your data to other people or organisations for their own purposes. '
   'Technical service providers have access to it only to the extent needed to provide '
   'their service.',
   'We also disclose information where Armenian law requires it, for example on a lawful '
   'request from a state authority.']),
  ('Data security', [
   'The site is served over an encrypted connection, so what you type into the form is '
   'encrypted in transit. Enquiries are held in a mailbox whose access is limited to the '
   'people who answer them.',
   'Ordinary email should not be treated as a '
   'confidential or end-to-end encrypted channel: if what you need to send is sensitive, '
   'say so first and we will agree a different way to receive it.']),
  ('Cookies and similar technologies', [
   'This site sets no cookies. One technical value is stored in your browser for a short '
   'time, to carry the visual transition between the two language versions. It holds no '
   'personal data and is discarded when you close the tab.']),
  ('Data retention', [
   'Where an enquiry does not lead to a contractual relationship, we keep it for up to '
   '24 months from our last contact with you, then delete it.',
   'Where an enquiry becomes a contract, we keep the related records for as long as the '
   'applicable accounting, tax or other legislation requires. You can ask us to delete '
   'your enquiry sooner.']),
  ('International data transfers', [
   'We are located and operate in Armenia. We receive and handle enquiries from Armenia, '
   'but the technical services used to transmit or store them may operate in other '
   'countries.',
   'The form service is a third-party service, so the data may be transferred outside '
   'Armenia when you send the form. You can also contact us directly '
   'at <a href="mailto:sales@gridec.am">sales@gridec.am</a>.']),
  ('Your rights', [
   'Where the law of the Republic of Armenia provides for it, you can obtain information '
   'about the processing of your data, access that data, and ask us to correct, block or '
   'destroy it.',
   'Where the GDPR applies to you, you may also have the right to restrict processing, '
   'to object to it, and to data portability.',
   'Write to <a href="mailto:sales@gridec.am">sales@gridec.am</a>. We will answer as '
   'quickly as we can and within the time limits the law sets.']),
  ('Complaints', [
   'If our answer does not satisfy you, you can complain to the Personal Data Protection '
   'Agency of the Ministry of Justice of the Republic of Armenia. If you are in the '
   'European Union, you may also complain to the supervisory authority of your country.']),
  ('Changes to this policy', [
   'If we change how enquiries are handled, we will update this page and the revision '
   'date below. We will describe any material changes on this page.']),
  ('Contact', [
   'Questions about this policy, or about the data we hold on you: '
   '<a href="mailto:sales@gridec.am">sales@gridec.am</a>, or by post to Gridec LLC, '
   'Davtashen 1, 13-25, Yerevan 0058, Armenia.']),
 ]),
 'PP_UPD': 'Last updated 14 September 2026',
 'F_PRIV': 'We use these details only to answer your enquiry. The form is delivered through '
           'FormSubmit, a third-party service. '
           '<button type="button" data-open-privacy>Privacy Policy</button>',
}
EN_DATA = {
 # подпись на схеме стыка: рисунок строится скриптом, поэтому она живёт в данных,
 # а не в токенах разметки
 'incident': 'Incident',
 'seq': [['01', 'Normal operation'], ['02', 'Electrical event'], ['03', 'Equipment trip or alarm'],
         ['04', 'System returns to normal'], ['05', 'The event record remains available for analysis']],
 'viewDetails': 'View details',
 'errName': 'Please enter your name.', 'errMsg': 'Please describe what happened.',
 'errEmail': 'Please enter a valid email address.', 'errPhone': 'Please enter a valid phone number.',
 'errContact': 'Enter an email or a phone number.',
 'hint1': ' file · ', 'hintN': ' files · ', 'hintSuf': ' of 10 MB', 'hint0': 'Up to 10 MB total.',
 'appTypes': ['Manufacturing', 'Solar PV', 'Healthcare / Laboratory',
              'Data Centre / IT', 'Commercial Building',
              'Investment / Technical Review', 'Other'],
 'cards': [
  {'title': 'Manufacturing', 'img': 'IMG0',
   'p1': 'Backup generation is designed for interruptions on a different time scale. A short voltage dip may affect equipment before transfer occurs, so the event must be recorded while it happens.',
   'findings': ['Timestamp, duration, minimum RMS voltage and affected phases of recorded dips.',
                'Voltage unbalance and current loading relevant to motor operation.',
                'Assessment of reactive power and harmonic distortion to determine whether further engineering investigation is needed.'],
   'statLabel': 'Technical note',
   'statText': 'Voltage sags and momentary interruptions can trip electronic and electromechanical devices and stop production lines.',
   'statSource': 'Source: EPRI'},
  {'title': 'Solar PV', 'img': 'IMG1',
   'p1': 'Measurements at relevant points can help distinguish plant-side from network-side factors.',
   'findings': ['Voltage conditions during inverter disconnection or active-power limitation.',
                'Voltage and harmonic distortion against applicable connection requirements.',
                'Independent measurement evidence for commissioning or EPC review.'],
   'note': 'Independent, time-aligned measurements give the owner, EPC contractor and network operator a common record of operating conditions.'},
  {'title': 'Healthcare and Laboratories', 'img': 'IMG2',
   'p1': 'Warranty or service review may require evidence of the supply conditions present while the equipment was operating. A spot measurement may miss intermittent events.',
   'findings': ['Recorded supply conditions compared with manufacturer requirements.',
                'Evidence relevant to distinguishing supply-related events from equipment faults.',
                'Recommended next checks prioritised by technical criticality and operational impact.'],
   'statLabel': 'Technical note',
   'statText': 'IEC 60601-1-2 includes immunity testing for voltage dips and short interruptions in medical electrical equipment.',
   'statSource': 'Source: IEC'},
  {'title': 'Data Centres and IT Infrastructure', 'img': 'IMG3',
   'p1': 'Generators start and transfer on a different time scale from millisecond-level disturbances. Time-stamped monitoring records can be compared with UPS and IT logs.',
   'findings': ['UPS input loading relative to rated capacity.',
                'Correlation between restarts, battery operation and recorded supply disturbances.',
                'Load profiles relevant to planned expansion.'],
   'stat': '57%', 'statLabel': 'Statistic',
   'statText': 'of respondents to Uptime&rsquo;s 2025 annual survey said their most recent major outage cost more than USD 100,000.',
   'statSource': 'Source: Uptime Institute, Annual Outage Analysis 2026'},
  {'title': 'Commercial Buildings', 'img': 'IMG4',
   'p1': 'Measurements can help distinguish upstream supply conditions from disturbances generated within the building or by tenant equipment.',
   'findings': ['Evidence relevant to the likely source of a disturbance.',
                'Electrical conditions associated with overheating or protective-device operation.',
                'Power factor, reactive power and load trends relevant to billing or capacity.'],
   'statLabel': 'Technical note',
   'statText': 'Power-quality events can originate on either side of the customer meter.',
   'statSource': 'Source: U.S. DOE / LBNL'},
  {'title': 'Investment and Technical Review', 'img': 'IMG5',
   'p1': 'Diagnostic or continuous monitoring provides an independent record under actual operation. The findings can support technical due diligence, handover, warranty review or performance assessment.',
   'findings': ['Observed loading and power quality at relevant points.',
                'Recorded conditions associated with interruptions or reduced output.',
                'Limitations, risks and recommended further checks.'],
   'note': 'Reports can be prepared in Armenian, Russian or English.'},
 ],
}

# ---------------------------------------------------------------- HY
HY = {
 'LANG': 'hy', 'TITLE': 'Gridec | Էլեկտրաէներգիայի որակի մոնիթորինգ',
 'FONTFACES': FF_HY + '\n' + FF_DEP,
 'READOUT': READOUT_HY % dict(mono=MONO_HY),
 'BODYFONT': "'Mardoto','Arian AMU','Helvetica Neue',sans-serif",
 'HEADFONT': "'Mardoto','Arian AMU',sans-serif", 'HEADWT': '500',
 'MONOFONT': MONO_HY,
 'NAVFONT': 'inherit',
 'HEADTT': '', 'HEADLH': '1.0', 'HEADLS': TY['HY_LS'], 'H1WT': '500', 'BIGLS': TY['HY_LS'],
 # Шкала та же, что в английской версии, буква в букву. Мерили не кегль, а
 # рост знака: у Arian AMU и Overused Grotesk доли прописной и строчной от
 # кегля совпадают (.72 и .53), поэтому одинаковые числа дают одинаковый
 # рост на экране. Прежняя шкала заголовков разделов была крупнее английской
 # на треть: прописная 43 против 33 на ширине 1440. Число строк проверено на
 # 1440, 1280, 1024, 768 и 375 — нигде не выросло, у заголовка героя везде
 # те же три строки.
 'H1SIZE': 'clamp(44px,4.3vw,70px)', 'H2SIZE': 'clamp(20px,3.17vw,48px)',
 'DISPSIZE': 'clamp(23px,3.96vw,55px)',   # та же шкала, что и в английской: прежние
 # 84 px давали блок выше английского в полтора раза
 'LANG_HREF': './index.html', 'LANG_LABEL': 'ENG', 'LANG_ARIA': 'English · Անգլերեն',
 'NAV_SERVICES': 'Ծառայություններ', 'NAV_INDUSTRIES': 'Ոլորտներ', 'NAV_COMPANY': 'Ընկերություն',
 'IX_LABEL': 'Բաժիններ', 'IX_ARIA': 'Բաժինների ցանկ',
 'CTA': 'Նկարագրել խնդիրը', 'NAV_CTA': 'Կապ մեզ հետ',
 'HERO_EYEBROW': 'Էլեկտրաէներգիայի որակի մոնիթորինգ',
 'HERO_H1': 'Ստուգեք, թե <span class="nb">ինչպես է</span> <br class="d">աշխատում ձեր <br class="d"><span class="ac">էլեկտրացանցը</span>',
 'HERO_P': 'Gridec-ը համակարգի աշխատանքի ընթացքում չափում և գրանցում է էլեկտրական պարամետրերը, ուսումնասիրում այն տեղում և վերլուծում ստացված տվյալները։ Չափումներն ու դիտարկումները համադրում ենք՝ հստակ ինժեներական գնահատական ներկայացնելու համար։',
 'HERO_CTA2': 'Ե՞րբ են պետք չափումները',
 'HERO_PHOTO_ALT': 'Էլեկտրաէներգիայի որակի չափումների պատկերազարդում՝ Ռոգովսկու կոճեր և շարժական չափիչ սարք էլեկտրական բաշխիչ վահանակի մոտ։',  # черновик — проверить владельцу
 'HERO_MARK1': 'Չափումներ', 'HERO_MARK2': 'Վերլուծություն', 'HERO_MARK3': 'Առաջարկություններ',

 # Поле героя: форма волны напряжения. Подписи по брифу владельца, дословно.
 'WHY_H2': 'Էլեկտրասնուցման խնդիրները միշտ չէ, որ նկատելի են',
 'WHY_P': 'Լարման անկումը կարող է տևել ընդամենը մի քանի պարբերություն։ Հետագա ստուգման պահին լարումն արդեն կարող է բնականոն լինել։ Անընդհատ մոնիթորինգը գրանցում է իրադարձությունը, դրա ժամանակը և չափված պարամետրերը՝ հետագա վերլուծության համար։',
 'APP_H2': 'Որտեղ է օգնում մոնիթորինգը',
 'APP_P': 'Մոնիթորինգն օգնում է, երբ էլեկտրաէներգիայի որակն ազդում է սարքավորումների կամ աշխատանքային գործընթացների վրա, կամ երբ տեխնիկական որոշում կայացնելու համար անհրաժեշտ են չափումների տվյալներ։',
 'OTHER_T': 'Այլ կարևոր էլեկտրական համակարգեր',
 'OTHER_P': 'Չե՞ք գտնում ձեր ոլորտն այստեղ։ Նկարագրեք խնդիրը և դրա ազդեցությունը սարքավորման աշխատանքի վրա։',
 'SVC_H2': '7-օրյա մոնիթորինգ',
 'SVC_P1': 'Էլեկտրաէներգիայի որակի տվյալները գրանցվում են համակարգի փաստացի աշխատանքի ընթացքում և վերլուծվում՝ ուսումնասիրվող խնդրի համատեքստում։',
 'SVC_P2': 'Մոնիթորինգի տևողությունն ընտրում ենք այնպես, որ գրանցենք համակարգի բնորոշ աշխատանքային ռեժիմները։ Եթե խնդիրը հազվադեպ կամ անկանոն է դրսևորվում, կամ աշխատանքային ցիկլն ավելի երկար է, առաջարկում ենք երկարացնել չափումների ժամանակահատվածը։',
 'SVC_STATS': stats_html([('7', 'օր մոնիթորինգ'),
                          ('24/7', 'անընդհատ տվյալների գրանցում'),
                          ('1', 'ինժեներական հաշվետվություն')]),
 'SVC_DISPLAY': 'Չափումներ՝<br>փաստացի<br><span class="ac">բեռնվածությամբ</span>',
 'SVC_STEPS': steps_html([
    ('01', 'Նախ հստակեցնում ենք՝ ինչ ենք ստուգելու, որ սարքավորումների վրա և ինչ որոշում եք կայացնելու արդյունքների հիման վրա։'),
    ('02', 'Չափումները կատարում ենք համակարգի աշխատանքի ընթացքում՝ ընդգրկելով համաձայնեցված աշխատանքային ռեժիմները։'),
    ('03', 'Վերլուծում ենք գրանցված տվյալները և հաշվետվության մեջ ներկայացնում եզրակացություններն ու առաջարկվող քայլերը։')]),
 'SVC_LINK': 'Տեսնել, թե ինչ կարող է բացահայտել մոնիթորինգը',
 'REP_H2': 'Հաշվետվություն',
 'REP_P': 'Ներկայացնում է չափման արդյունքները, դրանց ինժեներական վերլուծությունն ու եզրակացությունները՝ հետագա տեխնիկական որոշումների համար։',
 'REP_NOTE': 'Էլեկտրաէներգիայի որակի պարամետրերը չափվում են ԳՕՍՏ ԻԷԿ 61000-4-30-2017 ստանդարտով սահմանված S դասի մեթոդներով։ Հարմոնիկ և միջհարմոնիկ բաղադրիչները գնահատվում են ԻԷԿ 61000-4-7-ի համաձայն, երբ կիրառելի է։ Մատակարարման կետում արդյունքները կարող են համեմատվել Հայաստանում գործող ԳՕՍՏ 32144-2013-ի նորմերի հետ՝ չափման նպատակից և չափման կետից կախված։',
 'REP_LIST': list_html(['Չափումների շրջանակն ու կետերը', 'Մոնիթորինգի ժամանակահատվածն ու աշխատանքային ռեժիմները',
                        'Գրանցված իրադարձություններն ու միտումները', 'Ինժեներական մեկնաբանությունը',
                        'Առաջարկվող հաջորդ քայլերը']),
 # Оговорка вынесена из перечня строкой под ним — как в английской версии, чтобы
 # состав отчёта на двух языках не расходился числом пунктов.
 #
 # Именная группа «Առկա տվյալների սահմանափակումները», перенесённая из списка,
 # отдельной строкой не говорила ничего: пунктом перечня она называла раздел
 # отчёта, а под списком повисала обрывком. Заменена на то же утверждение, что
 # стоит в английской версии: «если записанных данных для вывода недостаточно,
 # отчёт это указывает».
 #
 # ⚠ ЧЕРНОВИК, ЖДЁТ ПРОВЕРКИ НОСИТЕЛЕМ. Собрано из слов, которые на странице
 # уже стоят: գրանցված, տվյալները, եզրակացություն, հաշվետվությունը, — но
 # армянскую формулировку должен утвердить владелец, а не я.
 'REP_NOTE2': lnote_html(
     # Формулировка владельца (2026-09-14).
     'Եթե գրանցված տվյալները բավարար չեն եզրակացություն անելու համար, '
     'դա հստակ նշվում է հաշվետվության մեջ։'),
 # Заголовок и названия карточек — обычным регистром, как во всех остальных разделах
 # армянской страницы: HEADTT здесь пуст, h1—h3 не переводятся в капс стилями (в
 # отличие от английской страницы), и капс в тексте выделял бы раздел 05 из ряда.
 # Категории остаются в верхнем регистре: .tag поднимает их сам, независимо от языка.
 'ASG_H2': 'Ինժեներական խնդիրներ',
 'ASG_P': 'Հզորության գնահատումից մինչև խափանումների պատճառների վերլուծություն։',
 'ASG_CARDS': qa_html([('Գեներատոր կամ UPS եք ընտրում։ Ի՞նչ հզորություն է անհրաժեշտ։', 'Չափում ենք պահուստային սնուցման ենթակա սարքավորումների բեռնվածությունն ու մեկնարկային հոսանքները՝ համաձայնեցված աշխատանքային ռեժիմներում։ Այս տվյալներն օգնում են մատակարարին ընտրել անհրաժեշտ հզորությունը։', 'Ժամանակավոր մոնիթորինգ', 'Գեներատոր և UPS'), ('Տեղադրում եք վերելակ, օդորակիչներ և պոմպեր։ Ինչպե՞ս կաշխատեն դրանք միասին։', 'Համաձայնեցված փորձարկումների ընթացքում գրանցում ենք էլեկտրական բեռնվածությունն ու լարման փոփոխությունները, երբ սարքավորումները գործարկվում և աշխատում են միաժամանակ։ Արդյունքներն օգնում են գնահատել՝ արդյոք պետք է փոփոխել էլեկտրասնուցման համակարգը կամ սարքավորումների գործարկման հերթականությունը։', 'Ժամանակավոր մոնիթորինգ', 'Վերելակ, օդորակիչներ և պոմպեր'), ('Նոր արտադրական գիծ եք ավելացնում։ Առկա էլեկտրասնուցման համակարգը կդիմանա՞ լրացուցիչ բեռնվածությանը։', 'Չափում ենք առկա բեռնվածությունն ու դրա առավելագույն արժեքները։ Նախագծողը կարող է այս տվյալները համադրել նոր սարքավորումների պահանջների հետ՝ գնահատելու հզորության պահուստը և նախատեսելու անհրաժեշտ փոփոխությունները։', 'Ժամանակավոր մոնիթորինգ', 'Նոր արտադրական գիծ'), ('Մատակարարը խափանումը կապում է էլեկտրասնուցման հետ։ Ինչպե՞ս ստուգել այդ վարկածը։', 'Մշտական մոնիթորինգը գրանցում և պահպանում է էլեկտրասնուցման տվյալները՝ խափանումից առաջ և դրա պահին։ Եթե այդ պահին մոնիթորինգն արդեն գործել է, Gridec-ը կարող է վերլուծել գրանցված տվյալներն ու օգնել ստուգել մատակարարի բացատրությունը։', 'Մշտական մոնիթորինգ', 'Մշտական մոնիթորինգ'), ('Ընդունում եք նոր սարքավորում։ Ի՞նչ է պետք գրանցել գործարկման պահին։', 'Չափում ենք էլեկտրասնուցման պարամետրերն ու բեռնվածությունը՝ համաձայնեցված աշխատանքային ռեժիմներում։ Հաշվետվությունն օգնում է մինչև սարքավորման ընդունումը մատակարարի հետ քննարկել չափումների արդյունքները։ Գրանցված տվյալները հետագայում ծառայում են որպես համեմատության հիմք՝ փոփոխությունների կամ խափանումների պատճառները պարզելիս։', 'Ժամանակավոր մոնիթորինգ', 'Նոր սարքավորման ընդունում')]),
 'ASG_PICS': qa_pics([('Գեներատոր կամ UPS եք ընտրում։ Ի՞նչ հզորություն է անհրաժեշտ։', 'Չափում ենք պահուստային սնուցման ենթակա սարքավորումների բեռնվածությունն ու մեկնարկային հոսանքները՝ համաձայնեցված աշխատանքային ռեժիմներում։ Այս տվյալներն օգնում են մատակարարին ընտրել անհրաժեշտ հզորությունը։', 'Ժամանակավոր մոնիթորինգ', 'Գեներատոր և UPS'), ('Տեղադրում եք վերելակ, օդորակիչներ և պոմպեր։ Ինչպե՞ս կաշխատեն դրանք միասին։', 'Համաձայնեցված փորձարկումների ընթացքում գրանցում ենք էլեկտրական բեռնվածությունն ու լարման փոփոխությունները, երբ սարքավորումները գործարկվում և աշխատում են միաժամանակ։ Արդյունքներն օգնում են գնահատել՝ արդյոք պետք է փոփոխել էլեկտրասնուցման համակարգը կամ սարքավորումների գործարկման հերթականությունը։', 'Ժամանակավոր մոնիթորինգ', 'Վերելակ, օդորակիչներ և պոմպեր'), ('Նոր արտադրական գիծ եք ավելացնում։ Առկա էլեկտրասնուցման համակարգը կդիմանա՞ լրացուցիչ բեռնվածությանը։', 'Չափում ենք առկա բեռնվածությունն ու դրա առավելագույն արժեքները։ Նախագծողը կարող է այս տվյալները համադրել նոր սարքավորումների պահանջների հետ՝ գնահատելու հզորության պահուստը և նախատեսելու անհրաժեշտ փոփոխությունները։', 'Ժամանակավոր մոնիթորինգ', 'Նոր արտադրական գիծ'), ('Մատակարարը խափանումը կապում է էլեկտրասնուցման հետ։ Ինչպե՞ս ստուգել այդ վարկածը։', 'Մշտական մոնիթորինգը գրանցում և պահպանում է էլեկտրասնուցման տվյալները՝ խափանումից առաջ և դրա պահին։ Եթե այդ պահին մոնիթորինգն արդեն գործել է, Gridec-ը կարող է վերլուծել գրանցված տվյալներն ու օգնել ստուգել մատակարարի բացատրությունը։', 'Մշտական մոնիթորինգ', 'Մշտական մոնիթորինգ'), ('Ընդունում եք նոր սարքավորում։ Ի՞նչ է պետք գրանցել գործարկման պահին։', 'Չափում ենք էլեկտրասնուցման պարամետրերն ու բեռնվածությունը՝ համաձայնեցված աշխատանքային ռեժիմներում։ Հաշվետվությունն օգնում է մինչև սարքավորման ընդունումը մատակարարի հետ քննարկել չափումների արդյունքները։ Գրանցված տվյալները հետագայում ծառայում են որպես համեմատության հիմք՝ փոփոխությունների կամ խափանումների պատճառները պարզելիս։', 'Ժամանակավոր մոնիթորինգ', 'Նոր սարքավորման ընդունում')]),
 'MEA_H2': 'Ինչ ենք չափում',
 'MEA_CHIPS': meas_html(['Լարում և հոսանք', 'Հարմոնիկներ և միջհարմոնիկներ', 'Ֆլիկեր',
                          'Լարման կարճատև անկումներ և բարձրացումներ', 'Լարման անհամաչափություն', 'Հզորություն և էներգիա',
                          'Իրադարձություններ', 'Ռիսկի ցուցանիշներ'], alt=1),
 'MEA_NOTE': lnote_html('Գրանցված տվյալների և աշխատանքային պայմանների հիման վրա գնահատում ենք սարքավորումների հնարավոր ռիսկերը։'),
 # Заголовки обычным регистром: на армянской странице стили не поднимают h1—h3 в
 # капс. Принудительных переносов нет — в этой редакции их не задавали, строки
 # раскладывает колонка.
 'CO_H2': 'Մեր մասին',
 'CO_P': 'Gridec-ը Երևանում գործող անկախ էլեկտրատեխնիկական ընկերություն է։ Չափում և վերլուծում ենք էլեկտրաէներգիայի որակը, օգնում պարզել խնդիրների պատճառները և ընտրել համապատասխան տեխնիկական լուծումներ։',
 'CO_STORY': story_html([
    # Тексты владельца (2026-09-15): два подблока вместо трёх.
    ('Ինչու սկսեցինք',
     'Gridec-ը հիմնել ենք՝ Հայաստանում ժամանակակից չափման տեխնոլոգիաները հասանելի դարձնելու համար։ Ուզում ենք, որ չափելն ու արդյունքները գրանցելը դառնան սովորական գործելակերպ, որպեսզի խնդիրների պատճառներն ու պատասխանատվությունը պարզվեն տվյալների հիման վրա։'),
    ('Ինչն ենք կարևորում',
     'Պատվիրատուն պետք է հասկանա՝ ինչ ենք չափել, ինչ ենք պարզել և ինչպես ենք հանգել մեր եզրակացություններին։ Արդյունքները ներկայացնում ենք այնպես, որ դրանք հնարավոր լինի ստուգել, քննարկել այլ մասնագետների հետ և օգտագործել հետագա որոշումների համար։')]),
 'CT_H2': 'Ներկայացրեք խնդիրը նախնական գնահատման համար',
 'CT_CAP': 'RMS լարում · պատկերային օրինակ', 'CT_NOM': 'Անվանական լարում', 'CT_DIP': 'Լարման անկում · 180 մվրկ',
 'CO_LEGAL': 'Գրիդեկ ՍՊԸ',
 'CO_TIN_LB': 'ՀՎՀՀ', 'CO_TIN': '08331059',
 'FOOT_ADDR': 'Դավթաշեն 1, 13-25, Երևան 0058, Հայաստան',
 'FOOT_SECTIONS': 'Բաժիններ', 'FOOT_CONTACT': 'Կապ',
 'FOOT_HOURS': 'Երկ-Ուրբ 09:00-18:00 (UTC+4)',
 'IM_FINDLB': 'Ինչ հարցերի կարող է պատասխանել հաշվետվությունը',
 'F_H3': 'Նկարագրեք <span class="ac">խնդիրը</span>',
 'F_INTRO': intro_html(''),
 'F_CONTACT': 'Կապի տվյալներ',
 'F_NAME': 'Անուն', 'F_NAME_PH': 'Ձեր անունը',
 'F_COMPANY': 'Ընկերություն', 'F_COMPANY_PH': 'Ընկերության անվանումը',
 'F_EMAIL': 'Էլ. փոստ', 'F_PHONE': 'Հեռախոս',
 'F_APP': 'Ոլորտ',
 'F_WHAT': 'Ի՞նչ է տեղի ունեցել',
 'F_MSG_PH': 'Նշեք՝ ինչ է տեղի ունեցել, երբ եք դա նկատել և որ սարքավորման աշխատանքում։',
 'F_ATT': 'Կցվող ֆայլեր', 'F_ATT_OPT': 'ըստ ցանկության',
 'F_DROP1': 'Կցեք ֆայլ կամ քաշեք այստեղ',
 'F_DROP2': 'Լուսանկարներ, սխեմաներ, հաշվետվություններ կամ սարքավորման տվյալներ',
 'F_SIZE_ERR': 'Կցված ֆայլերը գերազանցում են 10 ՄԲ սահմանը։ Հեռացրեք մի քանիսը։',
 'F_HINT0': 'Մինչև 10 ՄԲ',
 'F_FORM_ERR': 'Ստուգեք նշված դաշտերը։',
 # ⚠ ЧЕРНОВИК: армянские формулировки ошибок — на проверку владельцу.
 'F_ONE_CONTACT': 'Էլ. փոստ կամ հեռախոս՝ գոնե մեկը, որպեսզի կարողանանք պատասխանել։',
 'F_SEND_ERR': 'Հաղորդագրությունը չհաջողվեց ուղարկել։ Ստուգեք ինտերնետ կապը և փորձեք կրկին, կամ գրեք մեզ՝ sales@gridec.am հասցեով։',
 'F_SEND': 'Ուղարկել',
 'A_CLOSE': 'Փակել',
 'F_OK_T': 'Շնորհակալություն։',
 'F_OK_P': 'Կուսումնասիրենք ձեր հարցումը և կկապվենք ձեզ հետ՝ մանրամասները ճշտելու համար։',
 'F_CLOSE': 'Փակել',
 # ---- политика конфиденциальности ----
 # Перевод английского документа по смыслу, раздел в раздел. Юридические формулы
 # не изобретались: сказано ровно то же, что и в английской версии.
 'PP_LINK': 'Գաղտնիություն',
 'PP_H3': 'Գաղտնիության քաղաքականություն',
 'PP_LEDE': 'Այս քաղաքականությունը բացատրում է, թե ինչ է կատարվում կայքի միջոցով ձեր '
            'ուղարկած տեղեկատվության հետ։ Այն վերաբերում է միայն այս կայքին և '
            'նկարագրում է կայքի իրական աշխատանքը։',
 'PP_BODY': pp_html([
  ('Ովքեր ենք մենք', [
   '«Գրիդեկ» ՍՊԸ, Դավթաշեն 1, 13-25, Երևան 0058, Հայաստան։ ՀՎՀՀ 08331059։',
   '«Գրիդեկ» ՍՊԸ-ն որոշում է անձնական տվյալների մշակման նպատակներն ու միջոցները '
   'և հանդիսանում է տվյալները մշակողը։']),
  ('Ինչ ենք հավաքում', [
   'Կայքում կա մեկ ձև։ Այն հավաքում է ձեր անունը, ընկերությունը, էլ. փոստի հասցեն, '
   'հեռախոսահամարը, ընտրված ոլորտը, խնդրի ձեր նկարագրությունը և կցված ֆայլերը։',
   'Խնդրում ենք չկցել անձը հաստատող փաստաթղթեր, առողջական կամ այլ զգայուն անձնական '
   'տվյալներ, եթե դրանք անհրաժեշտ չեն ձեր հարցման համար։',
   'Այցելությունները հաշվում ենք Cloudflare Web Analytics-ով։ Այն cookie չի տեղադրում, '
   'չի կազմում այցելուի «մատնահետք» և չի հետևում ձեզ այլ կայքերում։ Մենք տեսնում ենք '
   'միայն ամփոփ թվեր՝ էջերի դիտումներ, ուղղորդող կայքեր, երկիր, դիտարկիչի և սարքի '
   'տեսակ, ոչ թե առանձին այցելուներ։',
   'Գովազդային համակարգեր և այլ երրորդ կողմի հետագծիչներ չունենք։',
   'Կայքի աշխատանքի ընթացքում հոսթինգի ծառայությունը կարող է ավտոմատ կերպով գրանցել '
   'սովորական տեխնիկական տվյալներ՝ օրինակ IP հասցեն, հարցման ժամը կամ դիտարկիչի '
   'մասին տեխնիկական տեղեկությունը։ Մենք դրանք չենք օգտագործում այցելուների '
   'վարքագիծը վերլուծելու կամ գովազդային նպատակներով։']),
  ('Ինչու ենք դրանք օգտագործում', [
   'Ձեր հարցմանը պատասխանելու, չափումների շրջանակը հստակեցնելու, առաջարկ '
   'պատրաստելու և հետագա կապը կազմակերպելու համար։ Տվյալները գովազդային '
   'նպատակով չենք օգտագործում, չենք վաճառում և երրորդ անձանց նպատակների համար '
   'չենք փոխանցում։']),
  ('Իրավական հիմքը', [
   'Ձևը լրացնելով և ուղարկելով՝ դուք մեզ տրամադրում եք տվյալները ձեր հարցումը '
   'մշակելու և ձեզ պատասխանելու համար։ Հենց այդ նպատակով էլ դրանք օգտագործում ենք։',
   'Եթե ձեր նկատմամբ կիրառելի է Տվյալների պաշտպանության ընդհանուր կանոնակարգը '
   '(GDPR), համապատասխան իրավական հիմքերը կարող են լինել դրա 6(1)(b) և 6(1)(f) '
   'հոդվածները։']),
  ('Ում ենք փոխանցում', [
   'Ձևի տվյալները մեզ փոխանցվում են FormSubmit (formsubmit.co) ծառայության միջոցով։ '
   'Ձևի պարունակությունը, ներառյալ կցված ֆայլերը, մշակվում է այդ ծառայության կողմից '
   'այնքանով, որքանով դա անհրաժեշտ է հարցումը մեր էլ. փոստին հասցնելու համար։ '
   'FormSubmit-ը երրորդ կողմի ծառայություն է, և տվյալների մշակումը կարող է '
   'իրականացվել նաև Հայաստանից դուրս։ Ստացված նամակն այնուհետև պահվում է մեր '
   'փոստային ծառայության մոտ։',
   'Այցելությունների հաշվառման տեխնիկական տվյալները մշակում է Cloudflare-ը՝ որպես '
   'մեզ ծառայություն մատուցող։',
   'Այլ անձանց կամ կազմակերպությունների ձեր տվյալները չենք փոխանցում նրանց սեփական '
   'նպատակներով։ Տեխնիկական ծառայություններ մատուցողները դրանց հասանելիություն '
   'ունեն միայն այնքանով, որքանով դա անհրաժեշտ է ծառայությունը մատուցելու համար։',
   'Տեղեկատվությունը բացահայտում ենք նաև այն դեպքում, երբ դա պահանջում է '
   'Հայաստանի օրենսդրությունը, օրինակ՝ պետական մարմնի իրավաչափ հարցման դեպքում։']),
  ('Տվյալների անվտանգությունը', [
   'Կայքը սպասարկվում է գաղտնագրված կապով, ուստի ձևում մուտքագրվածը փոխանցման '
   'ընթացքում գաղտնագրված է։ Հարցումները պահվում են փոստարկղում, որին հասանելիություն '
   'ունեն միայն դրանց պատասխանող աշխատակիցները։',
   'Սովորական էլեկտրոնային փոստը չպետք է դիտարկել '
   'որպես գաղտնի կամ վերջից վերջ գաղտնագրված կապուղի. եթե ուղարկելիքը զգայուն է, '
   'նախապես տեղեկացրեք, և կպայմանավորվենք ստանալու այլ եղանակի շուրջ։']),
  ('Cookie և նմանատիպ տեխնոլոգիաներ', [
   'Այս կայքը cookie չի տեղադրում։ Դիտարկիչում ժամանակավորապես պահվում է մեկ '
   'տեխնիկական արժեք՝ լեզվական տարբերակների միջև տեսողական անցումը ցուցադրելու '
   'համար։ Այն անձնական տվյալ չի պարունակում և ջնջվում է ներդիրը փակելիս։']),
  ('Որքան ենք պահում', [
   'Եթե հարցումը չի հանգեցնում պայմանագրային հարաբերությունների, այն պահում ենք '
   'ձեզ հետ վերջին կապից մինչև 24 ամիս, ապա ջնջում ենք։',
   'Եթե հարցման արդյունքում պայմանագիր է կնքվում, առնչվող փաստաթղթերը պահում ենք այնքան, '
   'որքան պահանջում է կիրառելի հաշվապահական, հարկային կամ այլ օրենսդրությունը։ '
   'Կարող եք խնդրել ջնջել ձեր հարցումն ավելի շուտ։']),
  ('Տվյալների միջսահմանային փոխանցում', [
   'Մենք գտնվում և գործում ենք Հայաստանում։ Հարցումները ստանում և մշակում ենք '
   'Հայաստանից, սակայն դրանց փոխանցման կամ պահպանման համար օգտագործվող տեխնիկական '
   'ծառայությունները կարող են գործել նաև այլ երկրներում։',
   'Ձևի ծառայությունը երրորդ կողմի ծառայություն է, ուստի ձևն ուղարկելիս տվյալները '
   'կարող են փոխանցվել Հայաստանից դուրս։ Մեզ կարող եք դիմել նաև ուղիղ՝ '
   '<a href="mailto:sales@gridec.am">sales@gridec.am</a> հասցեով։']),
  ('Ձեր իրավունքները', [
   'ՀՀ օրենսդրությամբ նախատեսված դեպքերում դուք կարող եք տեղեկություն ստանալ ձեր '
   'տվյալների մշակման մասին, ծանոթանալ դրանց և պահանջել ուղղել, ուղեփակել կամ '
   'ոչնչացնել դրանք։',
   'Եթե ձեր նկատմամբ կիրառելի է GDPR-ը, կարող եք ունենալ նաև տվյալների մշակումը '
   'սահմանափակելու, դրա դեմ առարկելու և տվյալների փոխանցելիության իրավունք։',
   'Գրեք <a href="mailto:sales@gridec.am">sales@gridec.am</a> հասցեին։ '
   'Կպատասխանենք հնարավորինս արագ և օրենքով սահմանված ժամկետներում։']),
  ('Բողոքները', [
   'Եթե մեր պատասխանը ձեզ չբավարարի, կարող եք բողոքել ՀՀ արդարադատության '
   'նախարարության Անձնական տվյալների պաշտպանության գործակալությանը։ Եվրոպական '
   'միությունում գտնվելու դեպքում կարող եք դիմել նաև ձեր երկրի վերահսկող մարմնին։']),
  ('Այս էջի փոփոխությունները', [
   'Եթե հարցումների մշակման կարգը փոխվի, կթարմացնենք այս էջը և ներքևի ամսաթիվը։ '
   'Էական փոփոխությունները կներկայացնենք այս էջում։']),
  ('Կապ', [
   'Այս քաղաքականության կամ ձեր տվյալների վերաբերյալ հարցերով՝ '
   '<a href="mailto:sales@gridec.am">sales@gridec.am</a>, կամ փոստով՝ '
   '«Գրիդեկ» ՍՊԸ, Դավթաշեն 1, 13-25, Երևան 0058, Հայաստան։']),
 ]),
 'PP_UPD': 'Թարմացվել է՝ 2026 թ. սեպտեմբերի 14',
 'F_PRIV': 'Այս տվյալներն օգտագործում ենք միայն ձեր հարցմանը պատասխանելու համար։ '
           'Ձեր հաղորդագրությունն ուղարկվում է FormSubmit ծառայության միջոցով։ '
           '<button type="button" data-open-privacy>Գաղտնիության քաղաքականություն</button>',
}
import copy
HY_DATA = copy.deepcopy(EN_DATA)
HY_DATA.update({
 'incident': 'Միջադեպ',
 'seq': [['01', 'Բնականոն աշխատանք'], ['02', 'Էլեկտրական համակարգում իրադարձություն'],
         ['03', 'Սարքավորման անջատում կամ ազդանշան'], ['04', 'Համակարգի աշխատանքի վերականգնում'],
         ['05', 'Գրանցումը պահպանվում է վերլուծության համար']],
 'viewDetails': 'Մանրամասներ',
 'errName': 'Նշեք ձեր անունը։', 'errMsg': 'Նկարագրեք՝ ինչ է տեղի ունեցել։',
 'errEmail': 'Նշեք վավեր էլ. փոստի հասցե։', 'errPhone': 'Նշեք վավեր հեռախոսահամար։',
 'errContact': 'Նշեք էլ. փոստ կամ հեռախոսահամար։',
 'hint1': ' ֆայլ · ', 'hintN': ' ֆայլ · ', 'hintSuf': ' / 10 ՄԲ', 'hint0': 'Առավելագույնը՝ 10 ՄԲ։',
 'appTypes': ['Արտադրություն', 'Արևային կայան', 'Բուժհաստատություն / լաբորատորիա',
              'Տվյալների կենտրոն / IT', 'Կոմերցիոն շենք',
              'Ներդրում / տեխնիկական գնահատում', 'Այլ'],
})
HY_CARDS = [
 {'title': 'Արտադրություն', 'img': 'IMG0',
  'p1': 'Լարման կարճատև անկումը կարող է ազդել սարքավորման վրա, ուստի իրադարձությունը պետք է գրանցվի հենց տեղի ունենալու պահին։',
  # «կորերը», а не «կորրերը»: слова «կորր» нет, кривая — «կոր».
  # Точка и двоеточие в третьем пункте заменены на армянскую точку «։»: в присланном
  # тексте стояли латинские знаки, а остальные пункты заканчиваются армянской.
  'findings': ['Գրանցված լարման անկումների ժամանակը, տևողությունը, նվազագույն RMS լարումը և այն ֆազերը, որոնցում դրանք գրանցվել են։',
               'Շարժիչների աշխատանքի համար նշանակալի լարման անհամաչափությունն ու բեռնվածության կորերը։',
               'Ռեակտիվ հզորության և հարմոնիկ աղավաղման գնահատում՝ պարզելու համար, թե արդյոք լրացուցիչ ինժեներական ուսումնասիրություն է անհրաժեշտ։'],
  'statLabel': 'Տեխնիկական նշում',
  'statText': 'Լարման անկումներն ու կարճատև ընդհատումները կարող են անջատել էլեկտրոնային և էլեկտրամեխանիկական սարքերը և կանգնեցնել արտադրական գծերը։',
  'statSource': 'Աղբյուր՝ EPRI'},
 {'title': 'Արևային կայաններ', 'img': 'IMG1',
  'p1': 'Համապատասխան կետերում կատարված չափումները օգնում են տարբերակել կայանի ներսում և արտաքին ցանցում առաջացող գործոնները։',
  'findings': ['Լարման պայմանները ինվերտորի անջատման կամ ակտիվ հզորության սահմանափակման պահին։',
               'Լարման և հարմոնիկ աղավաղման համապատասխանությունը միացման կիրառելի պահանջներին։',
               'Անկախ չափման տվյալներ՝ գործարկման ընդունման կամ EPC աշխատանքների գնահատման համար։'],
  'note': 'Ժամանակային նշումներով անկախ չափումները հնարավորություն են տալիս սեփականատիրոջը, EPC կապալառուին և ցանցի օպերատորին կայանի և միացման կետի էլեկտրական պայմանները գնահատել նույն տվյալների հիման վրա։'},
 {'title': 'Բժշկական կենտրոններ և լաբորատորիաներ', 'img': 'IMG2',
  'p1': 'Երաշխիքային կամ սպասարկման գնահատման համար կարող են պահանջվել տվյալներ այն էլեկտրասնուցման պայմանների մասին, որոնցում սարքավորումն աշխատել է։ Մեկանգամյա չափումը կարող է չգրանցել պարբերաբար ի հայտ եկող իրադարձությունները։',
  'findings': ['Գրանցված էլեկտրասնուցման պայմանների համեմատությունն արտադրողի պահանջների հետ։',
               'Տվյալներ՝ էլեկտրասնուցմամբ պայմանավորված իրադարձությունները սարքավորման խափանումներից տարբերակելու համար։',
               'Հաջորդ ստուգումների առաջարկվող հերթականությունը՝ ըստ տեխնիկական կարևորության և աշխատանքի վրա ազդեցության։'],
  'statLabel': 'Տեխնիկական նշում',
  'statText': 'IEC 60601-1-2-ը ներառում է բժշկական էլեկտրասարքավորումների՝ լարման անկումների և կարճատև ընդհատումների նկատմամբ խանգարումակայունության փորձարկումներ։',
  'statSource': 'Աղբյուր՝ IEC'},
 {'title': 'Տվյալների կենտրոններ և ՏՏ ենթակառուցվածք', 'img': 'IMG3',
  'p1': 'Գեներատորի գործարկումն ու սնուցման փոխանցումը կատարվում են այլ ժամանակային մասշտաբով, քան միլիվայրկյան տևող խանգարումները։ Ժամանակային նշումներով մոնիթորինգի տվյալները կարելի է համադրել UPS-ի և ՏՏ համակարգերի գրանցած իրադարձությունների հետ։',
  'findings': ['UPS-ի մուտքային բեռնվածությունը՝ անվանական հզորության համեմատ։',
               'Վերագործարկումների, մարտկոցից սնուցման ռեժիմի և գրանցված էլեկտրասնուցման խանգարումների միջև կապը։',
               'Պլանավորվող ընդլայնման համար նշանակալի բեռնվածության գրաֆիկները։'],
  'stat': '57%', 'statLabel': 'Վիճակագրություն',
  'statText': 'Uptime Institute-ի 2025 թ. տարեկան հարցման մասնակիցների այն բաժինը, որոնք նշել են, որ իրենց վերջին խոշոր խափանման արժեքը գերազանցել է 100 000 ԱՄՆ դոլարը։',
  'statSource': 'Աղբյուր՝ Uptime Institute, Annual Outage Analysis 2026'},
 {'title': 'Կոմերցիոն տարածքներ', 'img': 'IMG4',
  'p1': 'Չափումները կարող են օգնել տարբերակել արտաքին մատակարարման ցանցի պայմանները շենքի ներքին ցանցում կամ վարձակալների սարքավորումներից առաջացող խանգարումներից։',
  'findings': ['Տվյալներ խանգարման հավանական աղբյուրը գնահատելու համար։',
               'Գերտաքացման կամ պաշտպանիչ սարքերի գործարկման հետ կապված էլեկտրական պայմանները։',
               'Հզորության գործակիցը, ռեակտիվ հզորությունը և բեռնվածության միտումները՝ վճարների կամ հասանելի հզորության գնահատման համար։'],
  'statLabel': 'Տեխնիկական նշում',
  'statText': 'Էլեկտրաէներգիայի որակի իրադարձությունները կարող են առաջանալ սպառողի հաշվիչի երկու կողմում՝ մատակարարման կամ ներքին ցանցում։',
  'statSource': 'Աղբյուր՝ U.S. DOE / LBNL'},
 {'title': 'Ներդրումային և տեխնիկական գնահատում', 'img': 'IMG5',
  'p1': 'Ժամանակավոր կամ մշտական մոնիթորինգը հնարավորություն է տալիս անկախ կերպով գրանցել համակարգի փաստացի աշխատանքը։ Արդյունքները կարող են օգտագործվել տեխնիկական համալիր գնահատման, հանձնման, երաշխիքային ստուգման կամ աշխատանքի արդյունավետության գնահատման համար։',
  'findings': ['Համապատասխան կետերում դիտարկված բեռնվածությունն ու էլեկտրաէներգիայի որակը։',
               'Ընդհատումների կամ արտադրողականության նվազման հետ կապված գրանցված պայմանները։',
               'Սահմանափակումները, ռիսկերը և առաջարկվող լրացուցիչ ստուգումները։'],
  'note': 'Հաշվետվությունը կարող է պատրաստվել հայերեն, ռուսերեն կամ անգլերեն։'},
]
HY_DATA['cards'] = HY_CARDS

# the seventh plate in the industries rail reuses the existing invitation copy
EN_DATA['otherT'] = EN['OTHER_T']
EN_DATA['otherP'] = EN['OTHER_P']
HY_DATA['otherT'] = HY['OTHER_T']
HY_DATA['otherP'] = HY['OTHER_P']

for _d in (EN, HY):
    _d['FOOT_LINKS'] = foot_links(_d)

# ---------------------------------------------------------------- deploy variants (files by URL, not base64)
def font_face_url(fam, weight, fn):
    # Путь от страницы, а не от папки: деплойная пара лежит в КОРНЕ сайта, рядом
    # с fonts/ и uploads/. Прежний «../» достался от времени, когда пара жила в
    # подпапке v2/, и в корне уводил на уровень выше сайта — в никуда.
    return ("@font-face{font-family:'%s';font-weight:%s;font-display:swap;"
            "src:url(./fonts/%s) format('woff2');}" % (fam, weight, fn))

# Здесь объявляются РОВНО те начертания, на которые ссылаются правила. Блок
# отстал от замены гарнитур: объявлял Archivo, Big Shoulders Display и Martian
# Mono, которых в стилях уже нет, и не объявлял Overused Grotesk с Departure
# Mono, на которых держится вся страница. В превью-сборке шрифты вшиты в base64,
# поэтому на глаз это не ловилось — а выложенная страница уходила в системный.
FF_EN_D = '\n'.join([
    font_face_url('Overused Grotesk', '300 900', 'overused-grotesk-latin.woff2'),
    font_face_url('Departure Mono', '100 900', 'departure-mono.woff2'),
])

FF_HY_D = '\n'.join([
    font_face_url('Mardoto', '400', 'mardoto-400.woff2'),
    font_face_url('Mardoto', '700', 'mardoto-700.woff2'),
    font_face_url('Arian AMU', ARIAN_REG, 'arian-amu-400.woff2'),
    font_face_url('Arian AMU', '600 900', 'arian-amu-700.woff2'),
    # Пиксельная гарнитура показаний и счётчиков — та же, что на английской странице.
    font_face_url('Departure Mono', '100 900', 'departure-mono.woff2'),
    # Без этой строки выложенная страница не знала Mardoto и рисовала заголовки Arian AMU
    # Regular — так и было на gridec.am 2026-09-13 до этой правки (найдено аудитом
    # отрисованных шрифтов). Деплойный список объявляет ровно то, что вшито в превью.
    font_face_url('Mardoto', '500', 'mardoto-500.woff2'),
])
IMGD_D = {'IMG%d' % i: './uploads/img/' + f for i, f in enumerate(IMG_FILES)}

# ---------------------------------------------------------------- assemble
shell = io.open(os.path.join(HERE, 'shell.html'), encoding='utf-8').read()

# ------------------------------------------------------------ обозначения норм
# Обозначение стандарта — это не слово, а величина: набираем его приборной
# гарнитурой, как показания в остальных разделах. Берём только числовую часть:
# «ԳՕՍՏ» и «ԻԷԿ» написаны армянскими буквами, которых в пиксельном шрифте нет.
# Армянский падежный суффикс через дефис («61000-4-7-ի») остаётся снаружи —
# группа цифр после дефиса обязательна, а буква её не продолжает.
STD_NUM = re.compile(r'(?<![\w-])(\d{4,5}(?:-\d+){1,3})(?![\w])')


def mark_standards(text):
    return STD_NUM.sub(r'<span class="std">\1</span>', text)


def fill(tokens, data, ff, imgs):
    s = shell
    d = dict(data)
    d['imgs'] = imgs
    s = s.replace('%%DATA%%', json.dumps(d, ensure_ascii=False))
    t = dict(tokens); t['FONTFACES'] = ff
    lang = tokens.get('LANG', 'en')
    for k, v in t.items():
        if k == 'REP_NOTE':
            v = mark_standards(v)
        if k not in NO_GLUE:
            v = nbsp(v, lang)
        s = s.replace('%%' + k + '%%', v)
    left = re.findall(r'%%[A-Z0-9_]+%%', s)
    if left:
        raise SystemExit('UNFILLED TOKENS: %s' % sorted(set(left)))
    return s

def _strip_block_comments(code):
    """Убирает /* */ и // из кода, не трогая то, что стоит внутри строк.

    Сканер посимвольный, потому что регуляркой это делать нельзя: в скрипте
    есть 'https://formsubmit.co/…', и наивная замена «// до конца строки»
    съела бы половину вызова. Кавычки и экранирование отслеживаются; литералы
    регулярных выражений на странице (/\\s+/g и подобные) внутри себя ни //,
    ни /* не содержат, поэтому отдельного разбора не требуют.

    url(...) пропускается целиком, и это не перестраховка. Шрифты вшиваются как
    src:url(data:font/woff2;base64,…) БЕЗ кавычек, а в алфавите base64 есть косая
    черта: рано или поздно в теле шрифта встречаются подряд две — и без этой
    ветки сканер считал их началом комментария и срезал хвост объявления вместе
    со следующим за ним правилом. Первым таким правилом был :root со всей
    палитрой и шкалой отступов.
    """
    out, i, n, q = [], 0, len(code), ''
    while i < n:
        c = code[i]
        if q:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(code[i + 1]); i += 2; continue
            if c == q:
                q = ''
            i += 1; continue
        if (c in 'uU') and code[i:i + 4].lower() == 'url(':
            k = i + 4
            while k < n and code[k] in ' \t\n':
                k += 1
            if k < n and code[k] in '"\'':
                # Адрес в кавычках: дальше работает обычный разбор строки. Своей
                # ветке его отдавать нельзя — внутри data:image/svg+xml есть
                # filter='url(%23n2)', и поиск первой ')' обрывал бы адрес на
                # середине, после чего закрывающая кавычка читалась открывающей
                # и разъезжалась вся остальная таблица.
                out.append(code[i:k]); i = k; continue
            # Адрес без кавычек: по грамматике CSS неэкранированной ')' внутри
            # быть не может, поэтому первая же закрывает. Именно так вшиты шрифты.
            j = code.find(')', k)
            j = n if j < 0 else j + 1
            out.append(code[i:j]); i = j; continue
        if c in '"\'`':
            q = c; out.append(c); i += 1; continue
        if c == '/' and i + 1 < n and code[i + 1] == '*':
            j = code.find('*/', i + 2)
            i = n if j < 0 else j + 2
            continue
        if c == '/' and i + 1 < n and code[i + 1] == '/':
            j = code.find('\n', i)
            i = n if j < 0 else j
            continue
        out.append(c); i += 1
    # пустые строки, оставшиеся от снятых комментариев, схлопываются в одну
    return re.sub(r'\n[ \t]*(?=\n)', '', ''.join(out))

def strip_comments(html):
    """Комментарии живут в shell.html и build.py, а не в отгружаемой странице.

    Они написаны по-русски и объясняют историю решений — то есть адресованы тем,
    кто правит исходник, а не тем, кто открывает сайт. В собранном файле они
    только рассказывали читателю, как страница делалась.
    """
    # PT_NOSTRIP=1 собирает страницу с комментариями. Нужен, чтобы сверить две
    # сборки между собой: снятие комментариев обязано менять только их. Один раз
    # оно уже съело правило целиком, и проверять это на глаз нельзя.
    if os.environ.get('PT_NOSTRIP'):
        return html
    html = re.sub(r'<!--(?!\[if).*?-->', '', html, flags=re.S)
    def blk(m):
        return m.group(1) + _strip_block_comments(m.group(2)) + m.group(3)
    return re.sub(r'(<(?:style|script)[^>]*>)(.*?)(</(?:style|script)>)',
                  blk, html, flags=re.S)

def wrap(tokens, body, extra_head='', icons='../'):
    """\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b.

    \u0420\u0430\u043d\u044c\u0448\u0435 \u0431\u0440\u0430\u043b\u043e\u0441\u044c \u043d\u0430\u0447\u0430\u043b\u043e \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0430\u0431\u0437\u0430\u0446\u0430 \u0438 \u0440\u0435\u0437\u0430\u043b\u043e\u0441\u044c \u043f\u043e 175 \u0441\u0438\u043c\u0432\u043e\u043b\u0430\u043c \u2014 \u0432 \u0432\u044b\u0434\u0430\u0447\u0435
    \u043e\u043d\u043e \u043e\u0431\u0440\u044b\u0432\u0430\u043b\u043e\u0441\u044c \u043d\u0430 \u043f\u043e\u043b\u0443\u0441\u043b\u043e\u0432\u0435 (\u00ab\u2026to provide a clear\u2026\u00bb), \u0447\u0442\u043e \u0438 \u0432\u044b\u0434\u0430\u0432\u0430\u043b\u043e
    \u043c\u0430\u0448\u0438\u043d\u043d\u0443\u044e \u0441\u0431\u043e\u0440\u043a\u0443. \u042f\u0437\u044b\u043a, \u0443 \u043a\u043e\u0442\u043e\u0440\u043e\u0433\u043e \u0435\u0441\u0442\u044c \u0441\u0432\u043e\u0439 META_DESC, \u043e\u0442\u0434\u0430\u0451\u0442 \u0437\u0430\u043a\u043e\u043d\u0447\u0435\u043d\u043d\u043e\u0435
    \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0435; \u043e\u0431\u0440\u0435\u0437\u043a\u0430 \u043e\u0441\u0442\u0430\u043b\u0430\u0441\u044c \u043f\u0440\u0435\u0434\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u0435\u043b\u0435\u043c \u043d\u0430 \u0441\u043b\u0443\u0447\u0430\u0439 \u0434\u043b\u0438\u043d\u043d\u043e\u0439 \u0441\u0442\u0440\u043e\u043a\u0438.
    """
    desc = re.sub(r'<[^>]+>', '', tokens.get('META_DESC') or tokens['HERO_P'])
    if len(desc) > 175:
        desc = desc[:175].rsplit(' ', 1)[0] + '\u2026'
    head = ''.join([
        '<meta charset="utf-8">\n',
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n',
        # Ранний фон холста. Основная таблица стилей лежит в теле документа, и до
        # неё браузер красит белым — на каждой загрузке, а на стыке языков особенно
        # заметно. Одно правило здесь убирает это раньше, чем что-либо успеет
        # отрисоваться. Литералы терракотовые: их переводит палитровый проход.
        #
        # Класс wiping ставится, только если мы пришли своим переходом. Тогда первый
        # кадр уже фирменного цвета, а тело спрятано, чтобы страница не показалась
        # непокрытой до того, как плашки встанут. Предохранитель снимает маскировку
        # сам — иначе сбой скрипта оставил бы пустой экран.
        '<style>html{background:#EFEDEA}html.wiping{background:#AC4A29}'
        'html.wiping body{visibility:hidden}</style>\n',
        '<script>try{if(sessionStorage.getItem("ptwipe")==="1"){'
        'var _h=document.documentElement;_h.className+=" wiping";'
        'setTimeout(function(){_h.classList.remove("wiping")},2000);}}catch(e){}</script>\n',
        # Имя файла из адресной строки. Сервер отдаёт страницу и по «/», и по
        # «/index.html» — одна и та же, но вторая показывает устройство сайта, и
        # именно она остаётся в истории браузера и в закладках. Перенаправления у
        # статического хостинга нет, поэтому убирает хвост сама страница, в голове
        # документа: к моменту первой отрисовки адрес уже чистый.
        '<script>try{var _p=location.pathname;if(_p.slice(-10)==="index.html")'
        'history.replaceState(null,"",_p.slice(0,-10)+location.search+location.hash);}'
        'catch(e){}</script>\n',
        '<title>', tokens['TITLE'], '</title>\n',
        '<meta name="description" content="', desc, '">\n',
        '<meta name="theme-color" content="#C8603D">\n',
        # .ico объявлен ПЕРВЫМ и явно, хотя браузеры прекрасно берут svg. Причина
        # не в браузерах: поиск Google векторные значки не поддерживает вовсе, а
        # найдя в голове единственную иконку в svg, он не идёт искать /favicon.ico
        # по соглашению — и рисует в выдаче безликий глобус. В .ico есть кадр
        # 48×48, ровно тот размер, до которого Google всё приводит.
        '<link rel="icon" href="', icons, 'favicon.ico" sizes="48x48">\n',
        # PNG кратный 48 — то, что рекомендует Google для значка в выдаче (2026-09-14, icons_mark.py).
        '<link rel="icon" href="', icons, 'favicon-96.png" type="image/png" sizes="96x96">\n',
        '<link rel="icon" href="', icons, 'favicon.svg" type="image/svg+xml">\n',
        '<link rel="apple-touch-icon" href="', icons, 'apple-touch-icon.png">\n',
        '<meta property="og:type" content="website">\n',
        '<meta property="og:title" content="', tokens['TITLE'], '">\n',
        '<meta property="og:description" content="', desc, '">\n',
        '<meta property="og:locale" content="',
        'hy_AM' if tokens['LANG'] == 'hy' else 'en_US', '">\n',
    ])
    # data-nav повторяется скриптом в конце страницы, но там оно ставится уже
    # после первой отрисовки: полкадра шапка живёт без правил варианта 3 —
    # логотип выходит тёмным и без плашки, а потом перекрашивается на глазах.
    # В разметке атрибут есть с самого начала, и мигания не остаётся.
    # Счётчик идёт последним и с defer: он не должен задерживать ни отрисовку,
    # ни разбор страницы. Пустой токен не даёт ничего — см. CF_BEACON.
    return ('<!doctype html>\n<html lang="%s" data-nav="3">\n<head>\n%s%s</head>\n<body>\n%s%s\n</body>\n</html>\n'
            % (tokens['LANG'], head, extra_head, body, cf_beacon_tag()))

# ------------------------------------------------------------------- palettes
# REVIEW-ONLY palette passes. Each rewrites the FINISHED page, so index.html/hy.html
# keep the terracotta palette untouched and every variant is judged on the same markup.
#
# Both variants share one finding: an accent has to work on two very different grounds,
# and a single value rarely does. So each palette declares `light` (the accent for text
# and hairlines on paper) and `dark` (its twin on the graphite plates), and the extra CSS
# below wires them to --brand / --brand-ink / --brand-on so a fill always knows what
# colour of text belongs on top of it.
#
# mint: sky mint measures 1.11:1 on light paper, so it cannot carry a line, a dot or a
#   letter there at all — the light side has to use the deep mint and the mint itself
#   only appears on graphite.
# warm: the terracotta family kept, but taken down in chroma and depth. #9D5B43 reads
#   4.79:1 on its paper where the current #C8603D reads 3.70 — quieter AND more legible,
#   which is the answer to "терракота кричащий": the loudness was chroma, not hue.
PALETTES = {
    'mint': dict(
        paper='#F3F6F5', lo='#EBF0EE', tint='#EEF3F1', tint2='#F6F9F8',
        ph='#DBE1DF', offwhite='#F9FCFB',
        ink='#25272C', ink2='#2A2C32', ink3='#2E3138', ink4='#313439', ink5='#292B31',
        shadow='#1C1E22',
        light='#18624C', dark='#B8F7E4', glow='#35B68F', deep='#0F2A22', err='#9E2B25',
    ),
    'warm': dict(
        paper='#F4F5F5', lo='#ECEDEE', tint='#EFF0F1', tint2='#F7F8F8',
        ph='#DCDEE0', offwhite='#FBFCFC',
        ink='#25272C', ink2='#2A2C32', ink3='#2E3138', ink4='#313439', ink5='#292B31',
        shadow='#1C1E22',
        light='#9D5B43', dark='#C8856A', glow='#9D5B43', deep='#2A1610', err='#A8341F',
    ),
    # Четыре цвета заказчика: #2E5E99 акцент на светлом (5,74:1), #7BA4D0 акцент на
    # плашке (6,0:1), #0D2440 плашка. Средний синий на бумаге даёт 2,26:1, поэтому в
    # светлой роли он не появляется — ровно случай sky mint.
    #
    # Светлый грунт — тёплый нейтральный, а не синий: прежняя бумага #E7F0FA несла
    # насыщенность 6,0 при тоне 259°, и светлые страницы читались синеватыми (у
    # подложки снимков доходило до 12,6). Тон повёрнут к 75–85°, насыщенность срезана,
    # СВЕТЛОТА КАЖДОЙ РОЛИ СОХРАНЕНА с точностью до 0,05 — она задаёт яркость, из
    # которой считается контраст, поэтому читаемость не могла пострадать. Премиальность
    # тут берётся разностью температур: тёплая бумага против холодных чернил.
    'blue': dict(
        paper='#F6F1E9', lo='#EBE4D8', tint='#F0EAE0', tint2='#F9F5EE',
        ph='#DCD3C4', offwhite='#FDFAF4',
        # чернила ТЕКСТА и мелкой графики на светлом. Светлота та же, что у синих
        # (15%), поэтому контраст не падает.
        inkwarm='#2B2722',
        ink='#0D2440', ink2='#12294A', ink3='#162E52', ink4='#183256', ink5='#102745',
        shadow='#081A31',
        light='#2E5E99', dark='#7BA4D0', glow='#4C8ACB', deep='#0A1A2E', err='#A32C26',
    ),
}

def _mix(a, b, t):
    """Смешивает два цвета палитры. Нужен для тёмного близнеца акцента.

    Пара --brand / --brand-ink задумана как «акцент для заливок» и «акцент для
    ТЕКСТА и волосяных линий»: в терракотовой палитре это были #C8603D и #AC4A29,
    то есть один тон, но на десять единиц светлоты темнее. PAL_CSS присваивал
    обоим одно и то же значение light, и роль тёмного близнеца исчезла — все
    мелкие подписи сели на контрастный пол страницы: 5,88:1 в синей палитре,
    4,79:1 в тёплой. На армянской странице, где штрих тоньше, это и стало
    нечитаемым в первую очередь.

    Близнец берётся как 60 % акцента и 40 % самого тёмного цвета его же семьи
    (deep), поэтому ни одного нового тона не вводится: замер даёт тот же угол
    с точностью до градуса и ту же насыщенность, меняется только светлота.
    blue 5,88→8,94 | mint 6,68→9,08 | warm 4,79→7,92.
    """
    g = lambda h, i: int(h[i:i + 2], 16)
    v = [round(g(a, i) * t + g(b, i) * (1 - t)) for i in (1, 3, 5)]
    return '#%02X%02X%02X' % tuple(v)

def _rgb(h):
    h = h.lstrip('#')
    return '%d,%d,%d' % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def palette_map(p):
    """Source literals are the terracotta palette's own, so the list is the same for
    every variant — only the targets change."""
    return [
        # -- the dither bands: the accent cell follows the band's own ground
        # Тёмный квадрат светлой полосы — НЕ чернила, а цвет плашки, наползающий на
        # бумагу: полоса переводит светлый раздел в тёмный, и её квадраты обязаны
        # совпадать с тем, во что она переходит. Тёплый графит здесь рвал переход.
        ('#EFEDEA,#0D0E13,#C8603D', '%s,%s,%s' % (p['paper'], p['ink'], p['light'])),
        ('#14161C,#EFEDEA,#C8603D', '%s,%s,%s' % (p['ink3'], p['paper'], p['dark'])),
        # -- the section rails are drawn on both grounds, so they take the aware token
        ("tick.setAttribute('fill','#C8603D');", "tick.style.fill='var(--brand-ink)';"),
        ("pl.setAttribute('stroke','#C8603D');", "pl.style.stroke='var(--brand-ink)';"),
        # -- text sitting ON a brand fill: white is only right when the fill is dark
        ('background:var(--brand);color:#fff',
         'background:var(--brand);color:var(--brand-on)'),
        # -- the browser chrome reads as the darkest brand surface
        ('content="#C8603D"', 'content="%s"' % p['ink']),
        # -- grounds
        ('#EFEDEA', p['paper']), ('rgba(239,237,234', 'rgba(%s' % _rgb(p['paper'])),
        ('#F4F3F1', p['tint']), ('rgba(244,243,241', 'rgba(%s' % _rgb(p['tint'])),
        ('#F7F5F4', p['tint2']), ('#E9E6E2', p['lo']),
        ('#DDD9D2', p['ph']),
        ('#FFFBF9', p['offwhite']), ('rgba(255,251,249', 'rgba(%s' % _rgb(p['offwhite'])),
        ('rgba(252,251,250', 'rgba(%s' % _rgb(p['offwhite'])),
        ('#0D0E13', p['ink']), ('rgba(13,14,19', 'rgba(%s' % _rgb(p['ink'])),
        ('rgba(9,10,13', 'rgba(%s' % _rgb(p['shadow'])),
        ('#111318', p['ink2']),
        ('#14161C', p['ink3']), ('rgba(20,22,28', 'rgba(%s' % _rgb(p['ink3'])),
        ('#15171E', p['ink4']),
        ('#101218', p['ink5']), ('rgba(16,18,24', 'rgba(%s' % _rgb(p['ink5'])),
        # -- accent
        ('#C8603D', p['light']), ('rgba(200,96,61', 'rgba(%s' % _rgb(p['light'])),
        ('#AC4A29', p['light']), ('#D4714E', p['dark']),
        ('#F6573D', p['dark']), ('#C5280D', p['light']), ('#c5280d', p['light'].lower()),
        ('#2C1109', p['deep']),
        # -- a failed field must not read as brand
        ('#A8341F', p['err']),
        # -- the mark is single colour under either palette; no gradient tile survives
        ("logoSet(lm?lm[1]:(ls||'1'));", "logoSet(lm?lm[1]:'1');"),
    ]

PAL_CSS = """
/* ==================== %(name)s (review palette) ====================
   --brand      accent for graphics AND fills
   --brand-ink  accent for text and hairlines
   --brand-on   what sits on top of a --brand fill
   The light grounds and the graphite plates each get the depth that works on them. */
:root{--brand:%(light)s;--brand-ink:%(inkacc)s;--brand-on:%(paper)s;
  /* .78 и .76, а не .68 у обоих. Сайт читают в том числе люди с ослабленным
     зрением, и для вторичной прозы контраст значит не меньше кегля: .68
     давало 4,92:1 — норму AA, но впритык. Держим тот же приглушённый тон,
     просто не на самой границе. */
  --fg:%(inkw)s;--fg-mid:%(fgmid)s;--fg-soft:%(fgsoft)s;
  --hair:rgba(%(inkwrgb)s,.13);--hair2:rgba(%(inkwrgb)s,.07);}
.plate,.plate2,.chart,.icard,.rep-head{--brand:%(dark)s;--brand-ink:%(dark)s;--brand-on:%(ink)s;
  /* Заголовки на тёмных поверхностях светлые: общее правило h1–h3 берёт --fg-head, и без
     этой переменной названия карточек отраслей рисовались чернилами по чернилам (2026-09-13). */
  --fg-head:#F4F3F1;}
/* Заливки поверх бумаги героя нет ни в одной палитре: на светлом грунте она давала
   холодный налёт, и герой отличался цветом от панели указателя и от разделов. */
"""

def palette_pass(name):
    p = dict(PALETTES[name])
    p['inkacc'] = _mix(p['light'], p['deep'], .6)
    inkw = p.get('inkwarm', p['ink'])
    # Проза и подписи непрозрачные (#343A40 = 9,8:1, #62676D = 5,0:1 на бумаге #F6F1E9)
    # вместо чернил с прозрачностью .78/.76, которые читались тускло (2026-09-13).
    p['fgmid'] = '#343A40'
    p['fgsoft'] = '#62676D'
    css = PAL_CSS % dict(p, name=name, inkrgb=_rgb(p['ink']),
                         inkw=inkw, inkwrgb=_rgb(inkw),
                         darkrgb=_rgb(p['dark']), glowrgb=_rgb(p['glow']))
    rules = palette_map(p)

    def run(html):
        for a, b in rules:
            html = html.replace(a, b)
        for stale in ('#C8603D', '#EFEDEA', '#0D0E13'):
            if stale in html:
                raise SystemExit('%s: terracotta literal %s survived' % (name, stale))
        # В ПОСЛЕДНИЙ блок стилей, а не в первый. С появлением раннего фона в голове
        # документа блоков стало два, и палитра влилась в головной — то есть встала
        # ПЕРЕД основной таблицей и проиграла ей по порядку. Ломалось всё, что палитра
        # переопределяет: карточка-приглашение теряла чернильный текст, а шторка над
        # её артом стремилась не к тому синему, оставляя шов.
        i = html.rindex('</style>')
        return html[:i] + css + html[i:]
    return run

mintify = palette_pass('mint')
warmify = palette_pass('warm')
def render(tokens, data, out_body, out_full, post=None):
    s = fill(tokens, data, tokens['FONTFACES'], IMGD)
    # Переключатель языка ведёт на деплойные имена — в паре v2 это index.html и
    # hy.html. Отдельные страницы просмотра лежат рядом под своими именами, и без
    # этой подмены переключатель в них указывает в пустоту.
    s = s.replace('href="./hy.html"', 'href="./pt-hy.html"')
    s = s.replace('href="./index.html"', 'href="./pt-en.html"')
    io.open(os.path.join(HERE, out_body), 'w', encoding='utf-8').write(s)
    full = wrap(tokens, s)
    if post:
        full = post(full)
    # Снятие комментариев — последним шагом: палитровый проход отрабатывает ровно
    # так же, как раньше, и от прежней сборки страница отличается только тем,
    # чего в ней больше нет.
    full = strip_comments(full)
    io.open(os.path.join(HERE, out_full), 'w', encoding='utf-8').write(full)
    print(out_full, round(len(full) / 1024), 'KB')

SITE_URL = 'https://gridec.am'

# Адрес страницы — часть того, что видит посетитель. «/hy.html» показывает
# устройство сайта: расширение файла, папку, инструмент. Армянская страница
# лежит в hy/index.html и открывается как /hy/ — чистый адрес, которым не стыдно
# делиться.
#
# Плата за это одна: пути «./fonts» и «./uploads» отсчитываются от страницы, и из
# подпапки они увели бы в /hy/fonts — в пустоту. Поэтому в деплойной сборке все
# ссылки на файлы становятся корневыми. Считать их от корня — не прихоть: обе
# языковые страницы тогда описывают файлы ОДИНАКОВО, и глубина папки перестаёт
# что-либо значить.
#
# <base href="/"> сделал бы то же одной строкой, но заодно переписал бы якоря:
# «#services» стал бы «/#services», и переход по разделу уводил бы с армянской
# страницы на английскую. Замена адресов такого побочного действия не имеет.
def deploy_urls(html):
    for a, b in (('"./hy.html"', '"/hy/"'), ('"./index.html"', '"/"'),
                 ('./fonts/', '/fonts/'), ('./uploads/', '/uploads/'), ('./brand/', '/brand/'),
                 ('"./favicon', '"/favicon'), ('"./apple-touch-icon',
                                               '"/apple-touch-icon')):
        html = html.replace(a, b)
    return html

def render_deploy(tokens, data, ff, out_path, post=None):
    s = fill(tokens, data, ff, IMGD_D)
    # Две языковые версии одной страницы должны знать друг о друге, иначе поиск
    # считает их конкурентами и показывает не ту. Адреса абсолютные: домен назван,
    # а canonical и og:url относительный путь принимают, но склейку дубликатов
    # по нему поиск делает хуже — он не знает, какой хост считать главным.
    #
    # noindex снят. Он стоял, пока страница жила без домена и её незачем было
    # показывать; теперь запрет означал бы, что сайта нет ни в одном поиске.
    en, hy = SITE_URL + '/', SITE_URL + '/hy/'
    head = ('<link rel="canonical" href="%s">\n'
            '<meta property="og:url" content="%s">\n'
            '<link rel="alternate" hreflang="en" href="%s">\n'
            '<link rel="alternate" hreflang="hy" href="%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s">\n'
            % ((en if tokens['LANG'] == 'en' else hy,) * 2 + (en, hy, en)))
    # Ссылка без картинки разворачивается серой пустой строкой. Для конторы, к
    # которой приходят по рекомендации, это дороже позиций в поиске: рекомендация
    # и есть ссылка, отправленная в мессенджере.
    #
    # Карточка собрана КОДОМ — og/make_og.py, готовые файлы лежат в brand/.
    # Генератор картинок пробовали и забраковали: у этой картинки вся работа —
    # показать знак и одну строку, а генераторы вместо букв рисуют закорючки;
    # поле из наложенных дуг владелец отверг словами «как рыбный магазин».
    #
    # Знак вставлен готовым PNG, а не набран шрифтом: Departure Mono пиксельный,
    # и дробный пересчёт точек его размывает. Толщина линии и глубина просадки
    # посчитаны на МЕЛКИЙ размер: в чате карточка около 300px, и линия в два
    # пикселя там пропадала совсем.
    og_img = SITE_URL + ('/brand/og-hy.png' if tokens['LANG'] == 'hy'
                         else '/brand/og-en.png')
    og_alt = ('Gridec — Էլեկտրաէներգիայի որակի մոնիթորինգ'
              if tokens['LANG'] == 'hy'
              else 'Gridec — power quality monitoring in Armenia')
    head += ('<meta property="og:image" content="%s">\n'
             '<meta property="og:image:width" content="1200">\n'
             '<meta property="og:image:height" content="630">\n'
             '<meta property="og:image:type" content="image/png">\n'
             '<meta property="og:image:alt" content="%s">\n'
             '<meta name="twitter:card" content="summary_large_image">\n'
             % (og_img, og_alt))
    # Кто такие — машиночитаемо. Без этого поиск знает про сайт только домен и
    # подписывает выдачу «gridec.am», а не именем компании. Ни одного нового
    # утверждения здесь нет: имя, адрес, ՀՎՀՀ, почта и телефон уже стоят в подвале
    # обеих страниц, блок лишь называет их своими именами. Логотип дан пиксельным
    # PNG, а не svg: поиск векторные значки не читает.
    head += (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"Organization","@id":"%(u)s#org","name":"Gridec",'
        '"legalName":"Gridec LLC","url":"%(u)s","logo":"%(u)sapple-touch-icon.png",'
        '"email":"sales@gridec.am","telephone":"+374 41 00 00 14","taxID":"08331059",'
        '"address":{"@type":"PostalAddress","streetAddress":"Davtashen 1, 13-25",'
        '"addressLocality":"Yerevan","postalCode":"0058","addressCountry":"AM"}},'
        '{"@type":"WebSite","@id":"%(u)s#site","name":"Gridec","url":"%(u)s",'
        '"publisher":{"@id":"%(u)s#org"},"inLanguage":["en","hy"]}'
        ']}</script>\n' % {'u': SITE_URL + '/'})
    # Логотип теперь НАБОР, а не кривые. Пока гарнитура не пришла, слово рисуется
    # запасным моноширинным: другая ширина, другой рисунок — и шапка дёргается на
    # каждой первой загрузке, причём дёргается именно логотип. Предзагрузка ставит
    # файл в ту же очередь, что и разметку, и подмены на глазах не происходит.
    #
    # Прежде здесь стояла приписка, что остальные начертания появляются ниже сгиба
    # и предзагрузки не просят. Это неверно: ими набраны и заголовок героя, и
    # подзаголовок. Пока файл в пути, строки рисуются запасным шрифтом, а после
    # подмены пересчитывается ВСЯ страница — сдвигается и то, что далеко внизу.
    # На армянской это заметнее: запасная Georgia по ширине далека от Arian AMU.
    # Счётчик Cloudflare поймал ровно такой сдвиг на #contact (CLS 0.11).
    #
    # Список намеренно короткий — только то, что нужно первому экрану. Arian AMU
    # Serif 700 сюда не входит: им набрано выделение ниже сгиба, и держать ради
    # него ещё 20 КБ в высоком приоритете незачем.
    preload = {
        'en': ['overused-grotesk-latin.woff2'],
        'hy': ['mardoto-400.woff2', 'mardoto-500.woff2'],
    }.get(tokens['LANG'], [])
    for fn in ['departure-mono.woff2'] + preload:
        head += ('<link rel="preload" href="/fonts/%s" as="font" '
                 'type="font/woff2" crossorigin>\n' % fn)
    full = wrap(tokens, s, head, icons='./')
    if post:
        full = post(full)
    full = strip_comments(full)
    full = deploy_urls(full)
    io.open(out_path, 'w', encoding='utf-8').write(full)
    print(out_path, round(len(full) / 1024), 'KB')

# Синяя палитра — базовая, а не обзорный вариант: решение принято 2026-08-04.
# Тот же пост-проход, что делает mint и warm, только применён к основным сборкам,
# поэтому английская и армянская страницы получают её одинаково.
blueify = palette_pass('blue')

render(EN, EN_DATA, 'art-en.html', 'pt-en.html', blueify)
render(HY, HY_DATA, 'art-hy.html', 'pt-hy.html', blueify)
render(EN, EN_DATA, 'art-en-mint.html', 'pt-en-mint.html', mintify)
render(EN, EN_DATA, 'art-en-warm.html', 'pt-en-warm.html', warmify)

# ------------------------------------------------------------------- deploy
# `site/` в корне репозитория — это ровно то, что уходит в ветку main, файл в файл.
#
# Отдельный каталог, а не корень репозитория, по одной причине: ветка публикации
# отдаётся целиком, и всё, что в ней лежит, доступно по адресу. В корне сейчас
# рабочие файлы — брифы, планы, эта самая сборка; на сайте им делать нечего.
# Собирая ровно то, что должно быть видно, мы не полагаемся на память о том,
# какие файлы нельзя выкладывать.
#
# Прежняя цель — подпапка v2/ у соседнего репозитория. Она означала, что сайт
# открывается по адресу /v2/, а корень отдаёт что-то другое; и пути «../fonts»
# работали только оттуда. Разбор палитр остался в pt-en-mint.html и
# pt-en-warm.html: они самодостаточны, шрифты в них вшиты, и деплойные копии
# тех же вариантов были лишними.
import shutil
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DEPLOY = os.environ.get('PT_DEPLOY') or os.path.join(ROOT, 'site')

# Ровно те начертания, которые объявлены в FF_EN_D и FF_HY_D. Лишние не кладём:
# каждый файл в каталоге сайта — это то, что кто-то может скачать.
DEPLOY_FONTS = (['overused-grotesk-latin.woff2', 'departure-mono.woff2',
                 'arian-amu-400.woff2', 'arian-amu-700.woff2']
                + ['mardoto-400.woff2', 'mardoto-500.woff2', 'mardoto-700.woff2'])
DEPLOY_ICONS = ['favicon.svg', 'favicon.ico', 'favicon-96.png', 'apple-touch-icon.png']

def deploy_asset(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)

def write_text(rel, text):
    path = os.path.join(DEPLOY, rel)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(text)
    return path

os.makedirs(DEPLOY, exist_ok=True)
render_deploy(EN, EN_DATA, FF_EN_D, os.path.join(DEPLOY, 'index.html'), blueify)
os.makedirs(os.path.join(DEPLOY, 'hy'), exist_ok=True)
render_deploy(HY, HY_DATA, FF_HY_D, os.path.join(DEPLOY, 'hy', 'index.html'), blueify)
# Прежнее имя убираем: оставленный файл — это второй адрес той же страницы.
_stale = os.path.join(DEPLOY, 'hy.html')
if os.path.exists(_stale):
    os.remove(_stale)

for fn in DEPLOY_FONTS:
    deploy_asset(os.path.join(FONTS, fn), os.path.join(DEPLOY, 'fonts', fn))

make_small_images()
for fn in IMG_FILES + IMG_SMALL:
    deploy_asset(os.path.join(IMGS_OUT, fn), os.path.join(DEPLOY, 'uploads', 'img', fn))
# Иллюстрации раздела 05: WebP полного размера для настольной стопки и 724 px для
# телефона. PNG-оригиналы остаются в img/qa и на сайт не идут.
QA_DIR = os.path.join(IMGS, 'qa')
for fn in sorted(os.listdir(QA_DIR)):
    if fn.endswith('.webp'):
        deploy_asset(os.path.join(QA_DIR, fn), os.path.join(DEPLOY, 'uploads', 'qa', fn))
# Фото героя (2026-09-13): два WebP (2172 и 1086 по ширине, q84) из img/hero; PNG-исходник на сайт не идёт.
HERO_DIR = os.path.join(IMGS, 'hero')
for fn in sorted(os.listdir(HERO_DIR)):
    if fn.endswith('.webp'):
        deploy_asset(os.path.join(HERO_DIR, fn), os.path.join(DEPLOY, 'uploads', 'hero', fn))
# Логотип картинкой — для почтовой подписи и для всех, кто попросит знак файлом.
# Почтовые программы не знают ни наших шрифтов, ни нашей вёрстки: слово в подписи
# может жить ТОЛЬКО картинкой. Кладём её на сайт, потому что подпись подставляет
# адрес, а не файл: Gmail тянет её с gridec.am у каждого получателя.
# Тройной размер — под экраны с высокой плотностью; в подписи он показывается
# на треть, 121×46.
#
# Выкладываются ТОЛЬКО картинки. Каталог отдаётся по адресу целиком, и правило
# «копируем всё, что лежит» рано или поздно вынесло бы наружу черновик или
# заготовку подписи с личными данными. Список расширений — это замок.
BRAND = os.path.join(HERE, 'brand')
if os.path.isdir(BRAND):
    for fn in sorted(os.listdir(BRAND)):
        if os.path.splitext(fn)[1].lower() in ('.png', '.svg', '.jpg', '.webp'):
            deploy_asset(os.path.join(BRAND, fn), os.path.join(DEPLOY, 'brand', fn))

for fn in DEPLOY_ICONS:
    src = os.path.join(ROOT, fn)
    if os.path.exists(src):
        deploy_asset(src, os.path.join(DEPLOY, fn))

# CNAME — это и есть подключение домена к GitHub Pages. Отдельной настройки нет:
# что написано в файле, то Pages и обслуживает.
write_text('CNAME', 'gridec.am\n')
write_text('robots.txt',
           'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE_URL)
# Дата правки нужна карте сайта, но Date.now в сборке нет по той же причине,
# по которой его нет в скриптах: одинаковый вход обязан давать одинаковый выход.
# Значение берётся из окружения, иначе не печатается вовсе — тег необязательный.
_lastmod = os.environ.get('PT_LASTMOD', '')
_lm = '<lastmod>%s</lastmod>' % _lastmod if _lastmod else ''
write_text('sitemap.xml',
           '<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + ''.join(
               '  <url><loc>%s</loc>%s\n'
               '    <xhtml:link rel="alternate" hreflang="en" href="%s/"/>\n'
               '    <xhtml:link rel="alternate" hreflang="hy" href="%s/hy/"/>\n'
               '  </url>\n' % (loc, _lm, SITE_URL, SITE_URL)
               for loc in (SITE_URL + '/', SITE_URL + '/hy/'))
           + '</urlset>\n')
print(DEPLOY, '<- deploy tree')
print('done')
