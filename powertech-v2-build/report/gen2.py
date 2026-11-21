# Переверстывает отчёт владельца «GRIDEC Demonstration Report (REVISED)» в стиле сайта.
#
# 2026-11-22, владелец: «используй эти данные, не меняй их, лишь если надо меняй визуал, чтобы
# всё было в стиле сайта: фонты, логотип, цвета. Не менять исходные данные, расчёты и всё, что
# связано с техническим обоснованием. Термины тоже не меняй».
#
# Поэтому здесь НЕТ ни одной строки текста отчёта: всё берётся из revised/en_raw.txt и
# revised/hy_raw.txt (это `pdftotext -raw` присланных PDF) по номерам строк. Графики — те же
# растровые картинки из присланных PDF (исходных CSV владелец не присылал, перерисовать
# их в шрифтах сайта не из чего). Схема на стр. 2 перерисована с теми же подписями.
# check2.py сверяет слова готового PDF с исходным.
#
# Запуск: python gen2.py  → out/report2-en.html, out/report2-hy.html; PDF — make_pdf2.sh
import base64, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, 'revised')
OUT = os.path.join(HERE, 'out')
FONTS = os.path.join(ROOT, 'fonts')

INK, WARM, GREEN, COPPER = '#17241F', '#2B2722', '#2F6B4F', '#C86F33'
TINT, LINE, MUTE = '#F4EFE7', '#DCD3C4', '#6E6A62'


def b64(path, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(path, 'rb').read()).decode())


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Doc:
    def __init__(self, lang):
        self.lang = lang
        self.lines = open(os.path.join(SRC, '%s_raw.txt' % lang), encoding='utf-8').read().split('\n')

    def L(self, n):
        return self.lines[n - 1].strip()

    def J(self, a, b):
        return ' '.join(self.L(i) for i in range(a, b + 1))

    def W(self, n):
        return self.L(n).split(' ')


def bullet(s):
    assert s.startswith('• '), s
    return s[2:]


# ── разметка страниц по номерам строк исходника ────────────────────────────────────────
def spec(d):
    en = d.lang == 'en'
    L, J, W = d.L, d.J, d.W
    sp = lambda t, a, b=None: ' '.join(t[a:b])
    P = []

    # 1 обложка
    if en:
        P.append(dict(head=sp(W(1), 1), foot=L(3), no=L(2), cover=True, blocks=[
            ('kick', L(4)), ('h1', L(5)), ('sub', L(6)),
            ('facts', [(L(7), L(8)), (L(9), L(10)), (L(11), L(12)), (L(13), L(14))]),
            ('kpi', [(L(15), L(16)), (L(17), L(18)), (L(19), L(20)), (L(21), L(22))]),
            ('find', L(23), [J(24, 26), J(27, 29)]), ('warn', J(30, 32))]))
    else:
        P.append(dict(head=sp(W(1), 1), foot=L(3), no=L(2), cover=True, blocks=[
            ('kick', L(4)), ('h1', L(5)), ('sub', J(6, 7)),
            ('facts', [(L(8), J(9, 10)), (L(11), L(12)), (L(13), L(14)), (L(15), L(16))]),
            ('kpi', [(L(17), L(18)), (J(19, 20), L(21)), (L(22), L(23)), (L(24), L(25))]),
            ('find', L(26), [J(27, 30), J(31, 34)]), ('warn', J(35, 37))]))

    # 2 установка
    if en:
        a, facts = 33, [(L(37), J(38, 40)), (L(41), J(42, 43)), (L(44), J(45, 47)), (L(48), J(49, 50))]
        dg = dict(ab=W(52), cable=L(53), grid=L(54), sw=W(55)[0], inv=W(55)[1], loads=L(56), pe=L(57))
        rest = [('lbl', L(51)), ('diagram', dg), ('p', J(58, 59)), ('lbl', L(60)), ('p', J(61, 62))]
    else:
        a, facts = 38, [(L(42), J(43, 46)), (L(47), J(48, 51)), (L(52), J(53, 55)), (L(56), J(57, 59))]
        dg = dict(ab=W(61), cable=L(62), grid=L(63), sw=sp(W(64), 0, 2), inv=W(64)[2], loads=L(65), pe=L(66))
        rest = [('lbl', L(60)), ('diagram', dg), ('p', J(67, 69)), ('lbl', L(70)), ('p', J(71, 73))]
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2),
                  blocks=[('h1', L(a + 3)), ('factsb', facts)] + rest))

    # 3 метод
    if en:
        a = 63
        hdr = [sp(W(70), 0, 1), sp(W(70), 1, 3), sp(W(70), 3)]
        rows = [[sp(W(71), 0, 3), sp(W(71), 3) + ' ' + L(72), J(73, 74)],
                [sp(W(75), 0, 3), sp(W(75), 3, -4), sp(W(75), -4) + ' ' + L(76)],
                [sp(W(77), 0, 2), sp(W(77), 2) + ' ' + L(78), J(79, 80)]]
        rest = [('lbl', L(81)), ('p', J(82, 85)), ('p', J(86, 88)), ('warn', J(89, 91))]
        top = [('h1', L(66)), ('lbl', L(67)), ('p', J(68, 69))]
    else:
        a = 74
        hdr = [sp(W(82), 0, 1), sp(W(82), 1, 3), sp(W(82), 3)]
        rows = [[sp(W(83), 0, 4), sp(W(83), 4) + ' ' + L(84), J(85, 86)],
                [sp(W(87), 0, 3), sp(W(87), 3) + ' ' + L(88), J(89, 90)],
                [sp(W(91), 0, 2), sp(W(91), 2) + ' ' + L(92), J(93, 94)]]
        rest = [('lbl', L(95)), ('p', J(96, 100)), ('p', J(101, 103)), ('warn', J(104, 106))]
        top = [('h1', L(77)), ('lbl', L(78)), ('p', J(79, 81))]
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2),
                  blocks=top + [('table', hdr, rows, 'lll', 'mt')] + rest))

    # 4 неделя
    a, c = (92, 99) if en else (107, 114)
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2), blocks=[
        ('h1', L(a + 3)), ('lbl', L(a + 4)), ('img', 'p4_1'), ('lbl', L(a + 5)), ('img', 'p4_2'),
        ('lbl', L(a + 6)), ('cards', [(L(c + 2 * i), L(c + 2 * i + 1)) for i in range(6)]),
        ('note', J(c + 12, c + 13))]))

    # 5 отключения
    if en:
        a, r0 = 113, 121
        hdr = [sp(W(117), 0, 4), sp(W(117), 4) + ' ' + L(118), sp(W(119), 0, 3), sp(W(119), 3, 5),
               sp(W(119), 5, 7), sp(W(119), 7, 9), sp(W(119), 9) + ' ' + L(120)]
        tail = [('note', J(129, 131)), ('lbl', L(132)),
                ('bul', [bullet(J(133, 134)), bullet(L(135)), bullet(J(136, 137))]),
                ('total', L(138)), ('note', L(139))]
        h1 = L(116)
    else:
        a, r0 = 128, 135
        hdr = [sp(W(132), 0, 4), sp(W(132), 4) + ' ' + L(133), sp(W(134), 0, 3), sp(W(134), 3, 5),
               sp(W(134), 5, 7), sp(W(134), 7, 9), sp(W(134), 9)]
        tail = [('note', J(143, 145)), ('lbl', L(146)),
                ('bul', [bullet(J(147, 148)), bullet(J(149, 150)), bullet(J(151, 152))]),
                ('total', L(153)), ('note', L(154))]
        h1 = L(131)
    rows = []
    for i in range(r0, r0 + 8):
        t = W(i)
        assert len(t) == 9, t
        rows.append([sp(t, 0, 3)] + t[3:])
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2),
                  blocks=[('h1', h1), ('table', hdr, rows, 'vnnnnnn', 'trips')] + tail))

    # 6 событие E-08
    if en:
        a, h, r0 = 140, W(145), 146
        hdr = [sp(h, 0, 3), sp(h, 3, 5), sp(h, 5, 7), sp(h, 7)]
        tail = [('lbl', L(150)), ('p', J(151, 153)), ('warn', J(154, 155))]
    else:
        a, h, r0 = 155, W(160), 161
        hdr = [sp(h, 0, 2), sp(h, 2, 4), sp(h, 4, 6), sp(h, 6)]
        tail = [('lbl', L(165)), ('p', J(166, 168)), ('warn', J(169, 171))]
    rows = [[sp(W(i), 0, 2), W(i)[2], W(i)[3], sp(W(i), 4)] for i in range(r0, r0 + 4)]
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2), blocks=[
        ('h1', L(a + 3)), ('sub2', L(a + 4)), ('img', 'p6_3'),
        ('table', hdr, rows, 'vnnl', 'ev')] + tail))

    # 7 качество
    def pq(i):
        t = W(i)
        ref = sp(t, -2) if t[-1] in ('V', 'Վ') else t[-1]
        t = t[:-2] if t[-1] in ('V', 'Վ') else t[:-1]
        k = 6 if not re.match(r'^[\d.,]+$', t[-1]) else 3
        v = t[-k:]
        vals = [v[0] + ' ' + v[1], v[2] + ' ' + v[3], v[4] + ' ' + v[5]] if k == 6 else v
        return [sp(t, 0, -k)] + vals + [ref]

    def pb(i):
        t = W(i)
        return [t[0], sp(t, 1, 3), sp(t, 3, 5), sp(t, 5, 7)]

    if en:
        a = 156
        b = [('h1', L(159)), ('lbl', L(160)), ('table', W(161), [pq(i) for i in range(162, 170)], 'lnnnn', 'pq'),
             ('note', J(170, 171)), ('lbl', L(172)), ('table', W(173), [pb(i) for i in range(174, 177)], 'lnnn', 'pb'),
             ('note', J(177, 178)), ('lbl', L(179)), ('p', J(180, 181)), ('warn', J(182, 183))]
    else:
        a = 172
        b = [('h1', L(175)), ('lbl', L(176)), ('table', W(177), [pq(i) for i in range(178, 186)], 'lnnnn', 'pq'),
             ('note', J(186, 188)), ('lbl', L(189)), ('table', W(190), [pb(i) for i in range(191, 194)], 'lnnn', 'pb'),
             ('note', J(194, 195)), ('lbl', L(196)), ('p', J(197, 199)), ('warn', J(200, 202))]
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2), blocks=b))

    # 8 расчёт
    if en:
        a = 184
        b = [('h1', L(187)), ('lbl', L(188)), ('eq', [L(i) for i in range(189, 193)]), ('note', J(193, 194)),
             ('lbl', L(195)), ('img', 'p8_4'), ('lbl', L(196)),
             ('bul', [bullet(L(197)), bullet(J(198, 199)), bullet(J(200, 201))])]
    else:
        a = 203
        b = [('h1', L(206)), ('lbl', L(207)), ('eq', [L(i) for i in range(208, 212)]), ('note', J(212, 214)),
             ('lbl', L(215)), ('img', 'p8_4'), ('lbl', L(216)),
             ('bul', [bullet(J(217, 218)), bullet(J(219, 220)), bullet(J(221, 222))])]
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2), blocks=b))

    # 9 рекомендации
    if en:
        a = 202
        st = [(L(206), J(207, 208)), (L(209), J(210, 212)), (L(213), J(214, 215)), (L(216), J(217, 218)),
              (L(219), J(220, 221))]
        b = [('h1', L(205)), ('steps', st), ('lbl', L(222)),
             ('bul', [bullet(L(223)), bullet(J(224, 225)), bullet(L(226))])]
    else:
        a = 223
        st = [(L(227), J(228, 230)), (L(231), J(232, 234)), (L(235), J(236, 238)), (L(239), J(240, 242)),
              (L(243), J(244, 246))]
        b = [('h1', L(226)), ('steps', st), ('lbl', L(247)),
             ('bul', [bullet(J(248, 249)), bullet(J(250, 251)), bullet(J(252, 253))])]
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2), blocks=b))

    # 10 рамки
    if en:
        a = 227
        b = [('h1', L(230)), ('lbl', L(231)), ('p', J(232, 234)), ('lbl', L(235)),
             ('bul', [bullet(L(236)), bullet(J(237, 238)), bullet(L(239)), bullet(L(240))]),
             ('lbl', L(241)), ('p', J(242, 243)), ('lbl', L(244)), ('p', J(245, 247)), ('warn', J(248, 250))]
    else:
        a = 254
        b = [('h1', L(257)), ('lbl', L(258)), ('p', J(259, 261)), ('lbl', L(262)),
             ('bul', [bullet(J(263, 264)), bullet(J(265, 266)), bullet(J(267, 268)), bullet(J(269, 270))]),
             ('lbl', L(271)), ('p', J(272, 273)), ('lbl', L(274)), ('p', J(275, 277)), ('warn', J(278, 281))]
    P.append(dict(head=sp(W(a), 1), no=L(a + 1), foot=L(a + 2), blocks=b))
    return P


# ── вёрстка ─────────────────────────────────────────────────────────────────────────────
def logo(dark):
    fn = 'gridec-logo-dark.svg' if dark else 'gridec-logo-light-s.svg'
    return '<img class="logo" alt="" src="%s">' % b64(os.path.join(ROOT, 'brand', fn), 'image/svg+xml')


def diagram(g):
    def box(x, y, w, h, title, dark=False):
        return ('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width=".8"/>'
                '<text x="%.1f" y="%d" text-anchor="middle" class="dg-b" fill="%s">%s</text>'
                % (x, y, w, h, INK if dark else '#fff', INK, x + w / 2, y + h / 2 + 7, '#fff' if dark else INK, esc(title)))
    ln = lambda x1, y1, x2, y2, c=INK, w='1.2', d='': '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s" %s/>' % (
        x1, y1, x2, y2, c, w, ('stroke-dasharray="%s"' % d) if d else '')
    tx = lambda x, y, s, c=MUTE, cls='dg-t', anc='middle': '<text x="%d" y="%d" text-anchor="%s" class="%s" fill="%s">%s</text>' % (x, y, anc, cls, c, esc(s))
    o = ['<svg viewBox="0 0 696 190" class="ch" role="img">']
    o += [tx(40, 58, g['grid'], INK, anc='start'), ln(40, 70, 190, 70),
          box(190, 44, 52, 52, g['ab'][0], True), ln(242, 70, 470, 70, COPPER, '2.2'),
          box(470, 44, 52, 52, g['ab'][1], True),
          tx(356, 60, g['cable'], COPPER), tx(216, 116, g['sw']), tx(496, 116, g['inv']),
          ln(216, 124, 216, 148), tx(216, 164, g['loads'], INK),
          ln(300, 148, 640, 148, MUTE, '1', '5 4'), tx(470, 166, g['pe'])]
    o.append('</svg>')
    return ''.join(o)


CSS = '''
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:%(body)s;color:%(warm)s;font-size:%(fs)s;line-height:1.5;background:#fff;font-variant-numeric:tabular-nums}
.page{width:210mm;height:297mm;padding:15mm 18mm 18mm;position:relative;overflow:hidden;page-break-after:always}
.logo{height:6.4mm;width:auto;display:block}
.hd{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:3.2mm;border-bottom:.3mm solid %(ink)s;margin-bottom:9mm}
.hd span,.ft,.kick,.lbl,th,.fl,.kl{font-family:%(mono)s;font-size:%(ls)s;letter-spacing:.05em;color:%(mute)s;line-height:1.4}
.ft{position:absolute;left:18mm;right:18mm;bottom:9mm;display:flex;justify-content:space-between;border-top:.2mm solid %(line)s;padding-top:2.4mm}
h1{font-family:%(head)s;font-weight:%(hw)s;font-size:21pt;line-height:1.14;color:%(ink)s;margin-bottom:7mm;letter-spacing:0}
h2{font-family:%(head)s;font-weight:%(hw)s;font-size:11pt;line-height:1.25;color:%(ink)s;margin-bottom:2mm}
p{margin-bottom:2.2mm}
.lbl{display:block;color:%(green)s;margin:7mm 0 2.4mm}
h1+.lbl,.sub2+.lbl{margin-top:0}
.sub2{color:%(mute)s;margin:-3mm 0 6mm}
.note{font-size:%(ns)s;color:%(mute)s;line-height:1.45;margin-top:2.4mm}
.facts,.factsb{display:grid;grid-template-columns:1fr 1fr;gap:0 10mm}
.facts div,.factsb div{padding:2.8mm 0;border-bottom:.2mm solid %(line)s}
.facts div:nth-child(-n+2),.factsb div:nth-child(-n+2){border-top:.2mm solid %(line)s}
.fl{display:block;margin-bottom:1mm}
.facts b{display:block;font-weight:%(bw)s;color:%(ink)s}
.factsb .fl{color:%(green)s;margin-bottom:1.4mm}
.box{background:%(tint)s;padding:4.5mm 5mm;margin-top:7mm;border-left:.8mm solid %(green)s}
.box p:last-child{margin-bottom:0}
.warn{background:%(tint)s;border-left:.8mm solid %(copper)s;padding:4mm 5mm;margin-top:7mm;font-size:%(ns)s;line-height:1.45}
.bottom{position:absolute;left:18mm;right:18mm;bottom:19mm}
table{width:100%%;border-collapse:collapse;font-size:%(ts)s;margin-top:1mm}
th{text-align:left;font-weight:400;padding:0 2mm 1.8mm 0;border-bottom:.3mm solid %(ink)s;vertical-align:bottom}
td{padding:2.3mm 2mm 2.3mm 0;border-bottom:.2mm solid %(line)s;vertical-align:top}
td.n,th.n{text-align:right;padding-right:5mm}
td.n,td.v{font-family:%(mono)s;font-size:.95em;color:%(ink)s;white-space:nowrap}
table.mt td:first-child{width:24%%;color:%(ink)s;font-weight:%(bw)s}table.mt td:last-child{width:26%%}
table.ev td:last-child{padding-left:4mm}table.ev th:last-child{padding-left:4mm}
table.pq td:first-child,table.pb td:first-child{color:%(ink)s}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);border-top:.3mm solid %(ink)s;border-bottom:.3mm solid %(ink)s;margin-top:9mm}
.kpi div{padding:3.6mm 3mm 4mm 0;display:flex;flex-direction:column;justify-content:space-between}
.kpi div+div{padding-left:4mm;border-left:.2mm solid %(line)s}
.kpi b{font-family:%(mono)s;font-weight:400;font-size:17pt;color:%(ink)s;line-height:1.1;margin-top:2.4mm;white-space:nowrap}
.kpi div:first-child b{color:%(copper)s}
.cards{display:grid;grid-template-columns:repeat(3,1fr);border-top:.3mm solid %(ink)s}
.cards div{padding:3.2mm 3mm 3.4mm 0;border-bottom:.2mm solid %(line)s}
.cards b{display:block;font-family:%(mono)s;font-weight:400;font-size:13pt;color:%(ink)s;line-height:1.2;margin-top:1.4mm}
.cards span{font-size:%(ns)s;color:%(mute)s}
.ch{width:100%%;height:auto;display:block}
img.fig{width:100%%;height:auto;display:block}
.dg-t{font-family:%(mono)s;font-size:11.5px;letter-spacing:.05em}.dg-b{font-family:%(mono)s;font-size:20px}
.eq{font-family:%(mono)s;font-size:%(es)s;color:%(ink)s;border-top:.3mm solid %(ink)s}
.eq div{padding:2.4mm 0;border-bottom:.2mm solid %(line)s}
ul.pl{list-style:none}ul.pl li{padding-left:5mm;position:relative;margin-bottom:1.6mm}
ul.pl li:before{content:"";position:absolute;left:0;top:.72em;width:2.4mm;border-top:.3mm solid %(copper)s}
.total{font-family:%(head)s;font-weight:%(hw)s;font-size:10.6pt;color:%(ink)s;border-top:.3mm solid %(ink)s;border-bottom:.2mm solid %(line)s;padding:3mm 0;margin-top:6mm}
.step{display:grid;grid-template-columns:1fr;padding:3.6mm 0;border-bottom:.2mm solid %(line)s}
.step:first-child{border-top:.3mm solid %(ink)s}
.step b{display:block;font-family:%(mono)s;font-weight:400;font-size:%(ls2)s;letter-spacing:.05em;color:%(green)s;margin-bottom:1.4mm}
.step p{margin:0}
.cover{padding:0}
.plate{background:%(ink)s;padding:15mm 18mm 13mm;display:flex;justify-content:space-between;align-items:flex-end}
.plate .logo{height:10mm}.plate span{font-family:%(mono)s;font-size:%(ls)s;letter-spacing:.05em;color:#C5C4BD}
.cv{padding:13mm 18mm 0}
.kick{color:%(copper)s;display:block;margin-bottom:4mm}
.cover h1{font-size:27pt;margin-bottom:4mm}
.sub{font-size:11pt;line-height:1.45;max-width:150mm;margin-bottom:9mm}
'''


def build(lang):
    d = Doc(lang)
    hy = lang == 'hy'
    ff = []
    add = lambda fam, wt, fn: ff.append("@font-face{font-family:'%s';font-weight:%s;src:url(%s) format('woff2')}"
                                        % (fam, wt, b64(os.path.join(FONTS, fn), 'font/woff2')))
    add('Departure Mono', '100 900', 'departure-mono.woff2')
    if hy:
        add('Mardoto', '400', 'mardoto-400.woff2'); add('Mardoto', '500', 'mardoto-500.woff2')
        add('Mardoto', '700', 'mardoto-700.woff2')
        body = head = "'Mardoto',Arial,sans-serif"
        mono = "'Departure Mono','Mardoto',Arial,monospace"
        k = dict(hw='500', bw='700', fs='9.2pt', ts='8.5pt', ns='8.3pt', ls='6.6pt', ls2='7.2pt', es='8.4pt')
    else:
        add('Overused Grotesk', '300 900', 'overused-grotesk-latin.woff2')
        add('Overused Grotesk Head', '300 900', 'overused-grotesk-head.woff2')
        body = "'Overused Grotesk',Arial,sans-serif"
        head = "'Overused Grotesk Head',Arial,sans-serif"
        mono = "'Departure Mono',Arial,monospace"
        k = dict(hw='600', bw='600', fs='9.9pt', ts='8.9pt', ns='8.6pt', ls='6.8pt', ls2='7.4pt', es='8.8pt')
    css = CSS % dict(k, body=body, head=head, mono=mono, ink=INK, warm=WARM, green=GREEN, copper=COPPER,
                     tint=TINT, line=LINE, mute=MUTE)

    def render(b):
        t = b[0]
        if t == 'h1': return '<h1>%s</h1>' % esc(b[1])
        if t == 'kick': return '<span class="kick">%s</span>' % esc(b[1])
        if t == 'sub': return '<p class="sub">%s</p>' % esc(b[1])
        if t == 'sub2': return '<p class="sub2">%s</p>' % esc(b[1])
        if t == 'lbl': return '<span class="lbl">%s</span>' % esc(b[1])
        if t == 'p': return '<p>%s</p>' % esc(b[1])
        if t == 'note': return '<p class="note">%s</p>' % esc(b[1])
        if t == 'warn': return '<div class="warn">%s</div>' % esc(b[1])
        if t == 'total': return '<div class="total">%s</div>' % esc(b[1])
        if t == 'facts':
            return '<div class="facts">%s</div>' % ''.join(
                '<div><span class="fl">%s</span><b>%s</b></div>' % (esc(a), esc(v)) for a, v in b[1])
        if t == 'factsb':
            return '<div class="factsb">%s</div>' % ''.join(
                '<div><span class="fl">%s</span>%s</div>' % (esc(a), esc(v)) for a, v in b[1])
        if t == 'kpi':
            return '<div class="kpi">%s</div>' % ''.join(
                '<div><span class="kl">%s</span><b>%s</b></div>' % (esc(a), esc(v)) for a, v in b[1])
        if t == 'cards':
            return '<div class="cards">%s</div>' % ''.join(
                '<div><span>%s</span><b>%s</b></div>' % (esc(a), esc(v)) for a, v in b[1])
        if t == 'find':
            return '<div class="box"><h2>%s</h2>%s</div>' % (esc(b[1]), ''.join('<p>%s</p>' % esc(x) for x in b[2]))
        if t == 'bul':
            return '<ul class="pl">%s</ul>' % ''.join('<li>%s</li>' % esc(x) for x in b[1])
        if t == 'eq':
            return '<div class="eq">%s</div>' % ''.join('<div>%s</div>' % esc(x) for x in b[1])
        if t == 'steps':
            return '<div class="steps">%s</div>' % ''.join(
                '<div class="step"><b>%s</b><p>%s</p></div>' % (esc(a), esc(v)) for a, v in b[1])
        if t == 'img':
            return '<img class="fig" alt="" src="%s">' % b64(os.path.join(SRC, 'img_%s_%s.png' % (lang, b[1])), 'image/png')
        if t == 'diagram': return diagram(b[1])
        if t == 'table':
            _, hdr, rows, al, cls = b
            c = lambda i: {'n': ' class="n"', 'v': ' class="v"', 'l': ''}[al[i]]
            return '<table class="%s"><tr>%s</tr>%s</table>' % (
                cls, ''.join('<th%s>%s</th>' % (' class="n"' if al[i] == 'n' else '', esc(x)) for i, x in enumerate(hdr)),
                ''.join('<tr>%s</tr>' % ''.join('<td%s>%s</td>' % (c(i), esc(x)) for i, x in enumerate(r)) for r in rows))
        raise ValueError(t)

    pages = []
    for pg in spec(d):
        ft = '<div class="ft"><span>%s</span><span>%s</span></div>' % (esc(pg['foot']), esc(pg['no']))
        bl = pg['blocks']
        # последняя оговорка страницы стоит у нижнего поля, как в исходнике
        last = ''
        if bl[-1][0] == 'warn' and not pg.get('cover'):
            last = '<div class="bottom">%s</div>' % render(bl[-1]).replace('margin-top:7mm', '')
            bl = bl[:-1]
        inner = ''.join(render(b) for b in bl)
        if pg.get('cover'):
            pages.append('<section class="page cover"><div class="plate">%s<span>%s</span></div><div class="cv">%s</div>%s</section>'
                         % (logo(True), esc(pg['head']), inner, ft))
        else:
            pages.append('<section class="page"><div class="hd">%s<span>%s</span></div>%s%s%s</section>'
                         % (logo(False), esc(pg['head']), inner, last, ft))
    html = ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>Gridec</title><style>%s%s</style></head>'
            '<body>%s</body></html>' % (lang, '\n'.join(ff), css, ''.join(pages)))
    os.makedirs(OUT, exist_ok=True)
    fn = os.path.join(OUT, 'report2-%s.html' % lang)
    open(fn, 'w', encoding='utf-8').write(html)
    return fn


if __name__ == '__main__':
    for lang in ('en', 'hy'):
        print(build(lang))
