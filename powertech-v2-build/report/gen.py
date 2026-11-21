# Собирает учебный отчёт Gridec «Отключения инвертора СЭС» на двух языках (EN, HY).
# Все цифры считаются из report/data/*.csv — в тексте нет ни одного числа «от руки»,
# кроме паспортных (длина и сечение кабеля, уставка U>). Шрифты и цвета — как на сайте
# (PALETTES['green'] в build.py): Overused Grotesk / Mardoto, показания — Departure Mono.
#
# Запуск:  python gen.py        → out/report-en.html, out/report-hy.html
# PDF печатает Chrome (см. make_pdf.sh рядом).
import base64, csv, math, os, re

from texts import T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(HERE, 'data')
OUT = os.path.join(HERE, 'out')
FONTS = os.path.join(ROOT, 'fonts')

INK, WARM, GREEN, COPPER = '#17241F', '#2B2722', '#2F6B4F', '#C86F33'
TINT, LINE, PAPER, MUTE = '#F4EFE7', '#DCD3C4', '#FFFFFF', '#6E6A62'
# Медь сайта #E08A4B рассчитана на тёмную плитку; на белом листе линия графика такой
# светлоты теряется при печати, поэтому здесь тот же тон темнее.

R_FEEDER, U_SET, T_SET, COSPHI = 0.095, 253.0, 2.0, 0.998


def rd(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), encoding='utf-8-sig')))


def b64(fn, mime='font/woff2'):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(os.path.join(FONTS, fn), 'rb').read()).decode())


def pct(vals, q=0.95):
    v = sorted(vals)
    return v[max(0, math.ceil(q * len(v)) - 1)]


# ── данные ──────────────────────────────────────────────────────────────────────────────
W = rd('GRIDEC_example_10min_data.csv')
EV = rd('GRIDEC_example_inverter_events.csv')
TR = rd('GRIDEC_example_E08_20ms_RMS.csv')
DIPS = rd('GRIDEC_example_other_PQ_events.csv')
col = lambda k: [float(r[k]) for r in W]
IDX = {r['time']: i for i, r in enumerate(W)}

for e in EV:
    e['b'] = float(e['u_pv_l2_max_20ms_v'])
    e['a'] = float(e['u_pcc_l2_at_event_v'])
    e['p'] = float(e['p_pv_pre_trip_kw'])
    e['dur'] = int(e['duration_sec'])
    e['du'] = round(e['b'] - e['a'], 1)
    e['lost'] = float(e['est_lost_kwh'])
    i = IDX[e['timestamp_local'].replace('T', ' ')[:15] + '0:00']
    e['row'] = i
    e['swell'] = e['a'] - float(W[i - 1]['u_pcc_l2'])

g = col('grid_import_kw')
E_PV, E_LOAD = sum(col('pv_kw')) / 6, sum(col('load_kw')) / 6
E_IMP, E_EXP = sum(x for x in g if x > 0) / 6, -sum(x for x in g if x < 0) / 6
DT = sum(e['dur'] for e in EV)
LOST = sum(e['lost'] for e in EV)
PST = col('pst_pcc')
PLT = [(sum(x ** 3 for x in PST[i:i + 12]) / 12) ** (1 / 3) for i in range(0, len(PST), 12)]

tr = [(float(r['relative_s']), float(r['u_pcc_l2_rms_20ms_v']), float(r['u_pv_l2_rms_20ms_v']),
       float(r['pv_kw_synthetic_interp'])) for r in TR]
at = lambda s: min(tr, key=lambda z: abs(z[0] - s))
# последний заход B выше уставки перед отключением
cross = 0.0
for s, a, b, p in reversed([x for x in tr if x[0] <= 0]):
    if b <= U_SET:
        break
    cross = s
E8 = EV[-1]
PRE, PEAK, POST = at(-10), at(0), at(10)
I_CALC = E8['p'] * 1000 / (math.sqrt(3) * 400 * COSPHI)
DU_CALC = I_CALC * R_FEEDER * COSPHI
K_VKW = sum(e['du'] / e['p'] for e in EV) / len(EV)
B_HYP = max(e['a'] + 3.0 * e['p'] / max(x['p'] for x in EV) for e in EV)


# ── форматирование по языкам ────────────────────────────────────────────────────────────
class Fmt:
    def __init__(self, lang):
        self.lang = lang

    def n(self, x, d=1):
        s = '{:,.{}f}'.format(x, d)
        if self.lang == 'hy':
            s = s.replace(',', ' ').replace('.', ',')
        return s.replace('-', '−')

    def rng(self, a, b, d=1):
        return self.n(a, d) + '–' + self.n(b, d)

    def mmss(self, sec):
        return '%d:%02d' % divmod(int(sec), 60)

    def date(self, ts, time=True):
        d, t = ts.replace('T', ' ').split(' ')
        return '%s.%s%s' % (d[8:10], d[5:7], (' ' + t) if time else '')


def values(F):
    n, rng = F.n, F.rng
    u2 = col('u_pcc_l2')
    bb = {k: col('u_pv_' + k) for k in ('l1', 'l2', 'l3')}
    bmax = max(bb['l2'])
    return dict(
        n_trips=len(EV), dt=F.mmss(DT), bmax=n(max(e['b'] for e in EV)),
        du_rng=rng(min(e['du'] for e in EV), max(e['du'] for e in EV)),
        du_lo=n(math.floor(min(e['du'] for e in EV)), 0), du_hi=n(math.floor(max(e['du'] for e in EV)), 0),
        p_rng=rng(min(e['p'] for e in EV), max(e['p'] for e in EV)),
        p_lo=n(min(e['p'] for e in EV), 0), p_hi=n(max(e['p'] for e in EV), 0),
        sw_lo=n(math.floor(min(e['swell'] for e in EV)), 0), sw_hi=n(round(max(e['swell'] for e in EV)), 0),
        load_rng=rng(min(col('load_kw')), max(col('load_kw'))),
        rows=n(len(W), 0), r=n(R_FEEDER, 3), uset=n(U_SET, 0), tset=n(T_SET, 1),
        e_pv=n(E_PV), e_load=n(E_LOAD), e_imp=n(E_IMP), e_exp=n(E_EXP),
        lost=n(LOST), lost_pct=n(100 * LOST / E_PV),
        b10_lo=n(250, 0), b10_hi=n(math.ceil(bmax), 0), b10max=n(bmax), b10gap=n(U_SET - bmax),
        e8_p=n(E8['p']), e8_b=n(E8['b']), e8_a=n(E8['a']), e8_du=n(E8['du']),
        e8_pct=n(100 * E8['du'] / 230), e8_pre_du=n(PRE[2] - PRE[1]),
        e8_swell=n(PEAK[1] - PRE[1]), e8_above=n(-cross), e8_post_du=n(POST[2] - POST[1]),
        e8_drop=n(round(PRE[1] - POST[1]), 0),
        i_calc=n(I_CALC, 0), i_calc1=n(I_CALC), du_calc=n(DU_CALC), p_w=n(E8['p'] * 1000, 0),
        cosphi=n(COSPHI, 3), k=n(K_VKW, 3), b_hyp=n(math.ceil(B_HYP), 0),
        r20=n(0.443 * 0.185, 3), rkm=n(0.443, 3), lkm=n(0.185, 3),
        dip1_u=n(float(DIPS[0]['min_rms_20ms_v'])), dip1_ms=DIPS[0]['duration_ms'],
        dip2_u=n(float(DIPS[1]['min_rms_20ms_v'])), dip2_ms=DIPS[1]['duration_ms'],
        dip1_t=DIPS[0]['timestamp_local'][11:], dip2_t=DIPS[1]['timestamp_local'][11:],
    )


# ── графики ─────────────────────────────────────────────────────────────────────────────
def chart(series, x0, x1, y0, y1, xt, yt, w=696, h=200, ylab='', xlab='', extra='', hline=None):
    L, Rm, Tm, B = 40, 16, 18, 28 if xlab else 20
    pw, ph = w - L - Rm, h - Tm - B
    X = lambda x: L + (x - x0) / (x1 - x0) * pw
    Y = lambda y: Tm + (y1 - y) / (y1 - y0) * ph
    o = ['<svg viewBox="0 0 %d %d" class="ch" role="img">' % (w, h)]
    for v, lab in yt:
        o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s" stroke-width=".5"/>' % (L, w - Rm, Y(v), Y(v), LINE))
        o.append('<text x="%d" y="%.1f" text-anchor="end" class="tk">%s</text>' % (L - 6, Y(v) + 3, lab))
    for v, lab in xt:
        o.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="%s" stroke-width=".5"/>' % (X(v), X(v), Tm + ph, Tm + ph + 4, MUTE))
        o.append('<text x="%.1f" y="%d" text-anchor="middle" class="tk">%s</text>' % (X(v), Tm + ph + 14, lab))
    if hline is not None:
        o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s" stroke-width=".8" stroke-dasharray="4 3"/>'
                 % (L, w - Rm, Y(hline), Y(hline), INK))
    o.append(extra(X, Y, Tm, ph) if callable(extra) else extra)
    for pts, colr, sw in series:
        o.append('<polyline fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" points="%s"/>'
                 % (colr, sw, ' '.join('%.1f,%.1f' % (X(x), Y(y)) for x, y in pts)))
    o.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="%s" stroke-width=".8"/>' % (L, w - Rm, Tm + ph, Tm + ph, INK))
    if ylab:
        o.append('<text x="%d" y="%d" class="tk">%s</text>' % (2, 8, ylab))
    if xlab:
        o.append('<text x="%d" y="%d" text-anchor="end" class="tk">%s</text>' % (w - Rm, h - 2, xlab))
    o.append('</svg>')
    return ''.join(o)


def legend(items):
    return '<div class="lg">%s</div>' % ''.join(
        '<span><i style="border-top:%s"></i>%s</span>' % (st, lab) for st, lab in items)


def week_charts(F, t):
    n = len(W)
    days = [(i * 144, '%02d.06' % (8 + i)) for i in range(8)]
    xs = range(n)

    def marks(X, Y, Tm, ph):
        o = []
        for e in EV:
            sec = e['row'] + (int(e['timestamp_local'][15:16]) * 60 + int(e['timestamp_local'][17:19])) / 600
            x = X(sec)
            o.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="%s" stroke-width=".7"/>' % (x, x, Tm, Tm + ph, COPPER))
        return ''.join(o)

    c1 = chart([(list(zip(xs, col('u_pcc_l2'))), GREEN, '1'), (list(zip(xs, col('u_pv_l2'))), COPPER, '1')],
               0, n, 224, 256, days, [(v, str(v)) for v in (225, 230, 235, 240, 245, 250)], h=178,
               ylab=t('u_v'), hline=U_SET, extra=lambda X, Y, Tm, ph: marks(X, Y, Tm, ph).replace('stroke-width=".7"', 'stroke-width=".7" opacity=".45"'))
    c2 = chart([(list(zip(xs, col('load_kw'))), GREEN, '1'), (list(zip(xs, col('pv_kw'))), COPPER, '1')],
               0, n, 0, 100, days, [(v, str(v)) for v in (0, 25, 50, 75, 100)], h=160, ylab=t('u_kw'))
    return c1, c2


def e08_chart(F, t):
    pts = [x for x in tr if -10 <= x[0] <= 10]

    def band(X, Y, Tm, ph):
        return ('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s" opacity=".16"/>'
                '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="%s" stroke-width=".8"/>'
                '<text x="%.1f" y="%d" text-anchor="middle" class="tk" fill="%s">%s</text>'
                '<text x="%.1f" y="%.1f" text-anchor="end" class="tk">U&gt; %s</text>'
                % (X(cross), Tm, X(0) - X(cross), ph, COPPER, X(0), X(0), Tm, Tm + ph, INK,
                   (X(cross) + X(0)) / 2, Tm + ph - 6, WARM, F.n(-cross) + ' ' + t('u_s'),
                   X(10) - 4, Y(U_SET) - 4, F.n(U_SET, 0) + ' ' + t('u_volt')))

    return chart([([(x[0], x[1]) for x in pts], GREEN, '1.3'), ([(x[0], x[2]) for x in pts], COPPER, '1.3')],
                 -10, 10, 226, 258, [(v, F.n(v, 0)) for v in range(-10, 11, 2)],
                 [(v, str(v)) for v in range(230, 260, 5)], h=250, ylab=t('u_v'), xlab=t('ax_time'),
                 hline=U_SET, extra=band)


def diagram(t):
    def box(x, y, w, h, title, sub='', dark=False):
        return ('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width=".8"/>'
                '<text x="%d" y="%d" class="dg-t" fill="%s">%s</text>'
                '<text x="%d" y="%d" class="dg-s" fill="%s">%s</text>'
                % (x, y, w, h, INK if dark else PAPER, INK, x + 10, y + 22, PAPER if dark else INK, title,
                   x + 10, y + 38, '#C5C4BD' if dark else MUTE, sub))

    def meter(x, y, lab):
        return ('<circle cx="%d" cy="%d" r="10" fill="%s"/><text x="%d" y="%d" text-anchor="middle" '
                'class="dg-m" fill="#fff">%s</text>' % (x, y, COPPER, x, y + 3.8, lab))

    ln = lambda x1, y1, x2, y2, w='1.2', d='': '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s" %s/>' % (
        x1, y1, x2, y2, INK, w, ('stroke-dasharray="%s"' % d) if d else '')
    o = ['<svg viewBox="0 0 696 190" class="ch" role="img">']
    o += [box(0, 34, 100, 52, t('dg_grid'), t('dg_grid_s')),
          ln(100, 60, 170, 60),
          box(170, 34, 210, 52, t('dg_a'), t('dg_a_s'), dark=True),
          ln(380, 60, 520, 60, '2'),
          box(520, 34, 110, 52, t('dg_b'), t('dg_b_s'), dark=True),
          ln(630, 60, 652, 60),
          box(652, 34, 44, 52, 'PV', ''),
          ln(275, 86, 275, 128),
          box(185, 128, 180, 52, t('dg_load'), t('dg_load_s')),
          meter(135, 60, 'A'), meter(494, 60, 'B'),
          '<text x="437" y="50" text-anchor="middle" class="dg-s" fill="%s">%s</text>' % (INK, t('dg_cable')),
          '<text x="437" y="78" text-anchor="middle" class="dg-s" fill="%s">%s</text>' % (MUTE, t('dg_cable_s')),
          '<text x="494" y="26" text-anchor="middle" class="dg-s" fill="%s">%s</text>' % (COPPER, t('dg_meter')),
          '<text x="135" y="26" text-anchor="middle" class="dg-s" fill="%s">%s</text>' % (COPPER, t('dg_meter'))]
    o.append('</svg>')
    return ''.join(o)


# ── вёрстка ─────────────────────────────────────────────────────────────────────────────
def logo(dark):
    """Логотип сайта: те же файлы, что в шапке gridec.am (brand/), вшиты в страницу."""
    fn = 'gridec-logo-dark.svg' if dark else 'gridec-logo-light-s.svg'
    raw = open(os.path.join(ROOT, 'brand', fn), 'rb').read()
    return '<img class="logo" alt="Gridec" src="data:image/svg+xml;base64,%s">' % base64.b64encode(raw).decode()


CSS = '''
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:%(body)s;color:%(warm)s;font-size:%(fs)s;line-height:%(lh)s;background:#fff;
  font-variant-numeric:tabular-nums}
.page{width:210mm;height:297mm;padding:15mm 18mm 18mm;position:relative;overflow:hidden;
  page-break-after:always;display:flex;flex-direction:column}
.logo{height:6.4mm;width:auto;display:block}
.hd{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:3.2mm;
  border-bottom:.3mm solid %(ink)s;margin-bottom:9mm}
.hd span,.ft,.kick,.lbl,.tk,th{font-family:%(mono)s;font-size:6.6pt;letter-spacing:.06em;text-transform:uppercase;color:%(mute)s}
.ft{position:absolute;left:18mm;right:18mm;bottom:9mm;display:flex;justify-content:space-between;
  border-top:.2mm solid %(line)s;padding-top:2.4mm}
h1{font-family:%(head)s;font-weight:%(hw)s;font-size:21pt;line-height:1.14;color:%(ink)s;margin-bottom:7mm;letter-spacing:0}
h2{font-family:%(head)s;font-weight:%(hw)s;font-size:11pt;line-height:1.25;color:%(ink)s;margin:6.5mm 0 2mm}
h2:first-child{margin-top:0}
p{margin-bottom:2mm}
.m{font-family:%(mono)s;font-size:.92em}
.note{font-size:8.6pt;color:%(mute)s;line-height:1.45}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:0 10mm}
.facts div{padding:2.6mm 0;border-bottom:.2mm solid %(line)s}
.facts b,.kv b{display:block;font-weight:%(bw)s;color:%(ink)s}
.lbl{display:block;margin-bottom:.8mm}
.box{background:%(tint)s;padding:4.5mm 5mm;margin-top:6mm}
.box h2{margin-top:0}.box p:last-child{margin-bottom:0}
.box.g{border-left:.8mm solid %(green)s}.box.c{border-left:.8mm solid %(copper)s}
table{width:100%%;border-collapse:collapse;font-size:%(ts)s;margin-top:1mm}
th{text-align:left;font-weight:400;padding:0 2mm 1.8mm 0;border-bottom:.3mm solid %(ink)s;vertical-align:bottom;line-height:1.35}
td{padding:2.3mm 2mm 2.3mm 0;border-bottom:.2mm solid %(line)s;vertical-align:top}
td.n,th.n{text-align:right;padding-right:4mm}
td.n,td.v{font-family:%(mono)s;font-size:8.4pt;color:%(ink)s;white-space:nowrap}
td.ok{color:%(green)s}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:.3mm solid %(ink)s;border-bottom:.3mm solid %(ink)s;margin:9mm 0 0}
.kpi div{padding:4mm 3mm 4mm 0}.kpi div+div{padding-left:4mm;border-left:.2mm solid %(line)s}
.kpi b{display:block;font-family:%(mono)s;font-weight:400;font-size:17pt;color:%(ink)s;line-height:1.1;margin-bottom:1.6mm;white-space:nowrap}
.kpi div:first-child b{color:%(copper)s}
.kpi span{font-size:8pt;line-height:1.3;display:block;color:%(mute)s}
.ch{width:100%%;height:auto;display:block}
.tk{font-size:8.5px;letter-spacing:.04em;fill:%(mute)s;text-transform:none}
.dg-t{font-family:%(mono)s;font-size:9.5px;letter-spacing:.05em}
.dg-s{font-family:%(body)s;font-size:9.5px}.dg-m{font-family:%(mono)s;font-size:10px}
.lg{display:flex;gap:6mm;font-size:8pt;margin:1mm 0 1.5mm;color:%(warm)s}
.lg i{display:inline-block;width:6mm;height:0;vertical-align:middle;margin-right:1.8mm}
.cap{font-family:%(head)s;font-weight:%(hw)s;font-size:9.6pt;color:%(ink)s;margin-top:5mm}
.cap:first-of-type{margin-top:0}
.eq{font-family:%(mono)s;font-size:8.4pt;color:%(ink)s;line-height:1.9;margin:1mm 0 2mm}
.big{display:grid;grid-template-columns:repeat(4,1fr);border-top:.3mm solid %(ink)s;border-bottom:.2mm solid %(line)s}
.big div{padding:3.4mm 3mm 3.4mm 0}.big small{font-size:.58em}.big b{display:block;font-family:%(mono)s;font-weight:400;font-size:15pt;color:%(ink)s;line-height:1.15}
.big.hl div:nth-child(3) b{color:%(copper)s}
.steps{counter-reset:s}
.step{display:grid;grid-template-columns:12mm 1fr;padding:3.6mm 0;border-bottom:.2mm solid %(line)s}
.step:first-child{border-top:.3mm solid %(ink)s}
.step i{font-family:%(mono)s;font-style:normal;font-size:9pt;color:%(copper)s;padding-top:.4mm}
.step b{display:block;font-family:%(head)s;font-weight:%(hw)s;font-size:10.4pt;color:%(ink)s;margin-bottom:1mm}
.step p{margin:0}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm}
.three b{display:block;color:%(ink)s;font-weight:%(bw)s;margin-bottom:1mm}
.three div{border-top:.3mm solid %(ink)s;padding-top:2.6mm}
.three .v{font-family:%(mono)s;font-size:13pt;color:%(ink)s;display:block;margin-bottom:1.4mm}
ol.pts{list-style:none;counter-reset:p}
ol.pts li{counter-increment:p;display:grid;grid-template-columns:8mm 1fr;margin-bottom:1.8mm}
ol.pts li:before{content:counter(p);font-family:%(mono)s;font-size:8.4pt;color:%(copper)s;padding-top:.3mm}
dl{display:grid;grid-template-columns:%(dlw)s 1fr;gap:0}
dt,dd{padding:%(dlp)s 0;border-bottom:.2mm solid %(line)s}
dt{font-family:%(mono)s;font-size:8pt;color:%(ink)s}
ul.pl{list-style:none}ul.pl li{padding-left:4mm;position:relative;margin-bottom:.9mm}
ul.pl li:before{content:"";position:absolute;left:0;top:.62em;width:2mm;border-top:.25mm solid %(green)s}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:6.5mm}
.two h2:first-child{margin-top:0}
table.pq td:first-child{width:25%%}table.pq td:last-child{padding-right:0}
/* обложка */
.cover{padding:0}
.plate{background:%(ink)s;color:#fff;padding:15mm 18mm 13mm}
.plate .logo{height:10mm}
.cv{padding:14mm 18mm 0;flex:1}
.kick{color:%(green)s;font-size:7.4pt;display:block;margin-bottom:4mm}
.cover h1{font-size:28pt;margin-bottom:4mm}
.sub{font-size:11.5pt;line-height:1.45;max-width:140mm;color:%(warm)s}
.cover .facts{margin-top:10mm;border-top:.2mm solid %(line)s}
.sample{background:%(tint)s;border-left:.8mm solid %(copper)s;padding:4mm 5mm;margin-top:6mm}
.sample b{font-family:%(mono)s;font-weight:400;font-size:7pt;letter-spacing:.06em;text-transform:uppercase;color:%(copper)s;display:block;margin-bottom:1.4mm}
.sample p{margin:0;font-size:8.6pt}
'''


def build(lang):
    F = Fmt(lang)
    V = values(F)
    hy = lang == 'hy'

    def t(k, **kw):
        s = T[k][1 if hy else 0]
        return s.format(**dict(V, **kw)) if '{' in s else s

    fonts = []
    ff = lambda fam, wt, fn: fonts.append(
        "@font-face{font-family:'%s';font-weight:%s;src:url(%s) format('woff2')}" % (fam, wt, b64(fn)))
    ff('Departure Mono', '100 900', 'departure-mono.woff2')
    if hy:
        ff('Mardoto', '400', 'mardoto-400.woff2'); ff('Mardoto', '500', 'mardoto-500.woff2')
        ff('Mardoto', '700', 'mardoto-700.woff2')
        body = head = "'Mardoto',Arial,sans-serif"; hw, bw = '500', '700'
        mono = "'Departure Mono','Mardoto',monospace"
    else:
        ff('Overused Grotesk', '300 900', 'overused-grotesk-latin.woff2')
        ff('Overused Grotesk Head', '300 900', 'overused-grotesk-head.woff2')
        body = "'Overused Grotesk',Arial,sans-serif"; head = "'Overused Grotesk Head',Arial,sans-serif"
        hw, bw = '600', '600'
        mono = "'Departure Mono',monospace"
    css = CSS % dict(body=body, head=head, mono=mono, hw=hw, bw=bw, ink=INK, warm=WARM, green=GREEN,
                     copper=COPPER, tint=TINT, line=LINE, mute=MUTE,
                     fs='9.1pt' if hy else '9.9pt', ts='8.3pt' if hy else '8.8pt', lh='1.45' if hy else '1.5',
                     dlw='46mm' if hy else '30mm', dlp='1.15mm' if hy else '1.7mm')

    TOTAL = 10
    pages = []

    def page(no, sect, inner, cover=False):
        ft = '<div class="ft"><span>GRIDEC · GR-PQ-EX-001 · %s</span><span>%02d / %02d</span></div>' % (t('ft'), no, TOTAL)
        if cover:
            pages.append('<section class="page cover">%s%s</section>' % (inner, ft))
        else:
            hd = '<div class="hd">%s<span>%02d / %s</span></div>' % (logo(False), no - 1, sect)
            pages.append('<section class="page">%s%s%s</section>' % (hd, inner, ft))

    P = lambda k, **kw: '<p>%s</p>' % t(k, **kw)
    H2 = lambda k: '<h2>%s</h2>' % t(k)
    ul = lambda k: '<ul class="pl">%s</ul>' % ''.join('<li>%s</li>' % x for x in t(k).split('|'))
    fact = lambda a, b: '<div><span class="lbl">%s</span><b>%s</b></div>' % (t(a), t(b))

    # 01 обложка
    kp = lambda v, lab: '<div><b>%s</b><span>%s</span></div>' % (v, t(lab))
    pages_cover = (
        '<div class="plate">%s</div><div class="cv"><span class="kick">%s</span><h1>%s</h1><p class="sub">%s</p>'
        '<div class="facts">%s%s%s%s</div>'
        '<div class="kpi">%s%s%s%s</div>'
        '<div class="box g"><h2>%s</h2>%s%s</div>'
        '<div class="sample"><b>%s</b><p>%s</p></div></div>'
        % (logo(True), t('kick'), t('title'), t('sub'),
           fact('m_site', 'm_site_v'), fact('m_period', 'm_period_v'), fact('m_pv', 'm_pv_v'), fact('m_supply', 'm_supply_v'),
           kp('%02d' % V['n_trips'], 'k1'), kp(V['dt'], 'k2'), kp(V['bmax'] + ' ' + t('u_volt'), 'k3'),
           kp(V['du_rng'] + ' ' + t('u_volt'), 'k4'),
           t('find_h'), P('find_1'), P('find_2'), t('smp_h'), t('smp_p')))
    page(1, '', pages_cover, cover=True)

    # 02 установка
    page(2, t('s1'),
         '<h1>%s</h1><div class="facts">%s</div><h2>%s</h2>%s<p class="note">%s</p>%s%s'
         % (t('h1_1'), ''.join(fact('f%d' % i, 'f%dv' % i) for i in range(1, 9)),
            t('dg_h'), diagram(t), t('dg_note'),
            '<div class="box g">%s%s</div>' % (H2('chk_h'), ul('chk_l')), ''))

    # 03 программа измерений
    rows = ''.join('<tr><td class="v">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                   % tuple(t('mt%d' % i).split('|')) for i in (1, 2, 3))
    page(3, t('s2'),
         '<h1>%s</h1><table><tr>%s</tr>%s</table><div class="two"><div>%s%s%s%s</div><div>%s%s%s%s</div></div>'
         '<div class="box g">%s%s</div>'
         % (t('h1_2'), ''.join('<th>%s</th>' % x for x in t('mt_h').split('|')), rows,
            H2('win_h'), P('win_p'), H2('meth_h'), P('meth_p'), H2('pre_h'), ul('pre_l'), '', '',
            H2('why_h'), P('why_p')))

    # 04 неделя
    c1, c2 = week_charts(F, t)
    en = lambda v, lab: '<div><span class="v">%s</span>%s</div>' % (v + ' ' + t('u_kwh'), t(lab))
    page(4, t('s3'),
         '<h1>%s</h1><div class="cap">%s</div>%s%s<div class="cap">%s</div>%s%s<p class="note">%s</p>'
         '<h2>%s</h2><div class="big" style="border-bottom:0">%s%s%s%s</div><p class="note">%s</p>'
         % (t('h1_3'), t('c1_h'),
            legend([('2px solid ' + GREEN, t('lg_a')), ('2px solid ' + COPPER, t('lg_b')),
                    ('1.5px dashed ' + INK, 'U> ' + V['uset'] + ' ' + t('u_volt'))]), c1,
            t('c2_h'), legend([('2px solid ' + COPPER, t('lg_pv')), ('2px solid ' + GREEN, t('lg_load'))]), c2,
            t('wk_note'), t('en_h'),
            *['<div><b>%s <small>%s</small></b><span class="note">%s</span></div>' % (V[k], t('u_kwh'), t(lab))
              for k, lab in (('e_pv', 'en1'), ('e_load', 'en2'), ('e_imp', 'en3'), ('e_exp', 'en4'))],
            t('en_note')))

    # 05 журнал отключений
    th = t('tl_h').split('|')
    rows = ''.join(
        '<tr><td class="v">%s</td><td class="v">%s</td><td class="n">%s</td><td class="n">%s</td>'
        '<td class="n">%s</td><td class="n">%s</td><td class="n">%s</td></tr>'
        % (e['event_id'], F.date(e['timestamp_local']), F.n(e['b']), F.n(e['a']), F.n(e['du']), F.n(e['p']), F.mmss(e['dur']))
        for e in EV)
    page(5, t('s4'),
         '<h1>%s</h1><table><tr>%s</tr>%s</table><p class="note" style="margin-top:2.5mm">%s</p>'
         '<div class="box g">%s%s</div><div class="box c">%s%s</div>'
         % (t('h1_4'), ''.join('<th%s>%s</th>' % (' class="n"' if i > 1 else '', x) for i, x in enumerate(th)), rows,
            t('tl_note'), H2('com_h'), '<ol class="pts">%s</ol>' % ''.join('<li><span>%s</span></li>' % x for x in t('com_l').split('|')),
            '<h2>%s · %s</h2>' % (t('lost_h'), V['lost'] + ' ' + t('u_kwh')), P('lost_p')))

    # 06 событие E-08
    def trow(s, lab, st, vals=True):
        x = at(s)
        return ('<tr><td class="v">%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td><td>%s</td></tr>'
                % (lab, F.n(x[2]) if vals else '—', F.n(x[1]) if vals else '—', F.n(x[2] - x[1]) if vals else '—', st))
    cr = 38 + cross
    rows = (trow(-10, '13:11:28', t('st1')) + trow(cross, '13:11:%04.1f' % cr if not hy else ('13:11:%04.1f' % cr).replace('.', ','), t('st2'))
            + trow(0, '13:11:38', t('st3')) + trow(10, '13:11:48', t('st4')) + trow(0, '13:17:48', t('st5'), False))
    th = t('ev_h').split('|')
    page(6, t('s5'),
         '<h1>%s</h1><div class="cap">%s</div>%s%s<p class="note">%s</p><table style="margin-top:4mm"><tr>%s</tr>%s</table>'
         '<div class="box g">%s<ol class="pts">%s</ol></div>'
         % (t('h1_5'), t('c3_h'),
            legend([('2px solid ' + GREEN, t('lg_a')), ('2px solid ' + COPPER, t('lg_b')),
                    ('1.5px dashed ' + INK, 'U> ' + V['uset'] + ' ' + t('u_volt'))]),
            e08_chart(F, t), t('c3_note'),
            ''.join('<th%s>%s</th>' % (' class="n"' if 0 < i < 4 else '', x) for i, x in enumerate(th)), rows,
            H2('rec_h'), ''.join('<li><span>%s</span></li>' % x for x in t('rec_l').split('|'))))

    # 07 качество электроэнергии в точке A
    uV, uP, uHz = ' ' + t('u_volt'), ' %', ' ' + t('u_hz')
    ok, inf = '<td class="ok">%s</td>' % t('ok'), '<td>%s</td>' % t('inf')
    row = lambda name, lo, p95, hi, l95, l100, res: (
        '<tr><td>%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td><td class="v">%s</td>'
        '<td class="v">%s</td>%s</tr>' % (name, lo, p95, hi, l95, l100, res))
    rows = ''
    for k in ('l1', 'l2', 'l3'):
        v = col('u_pcc_' + k)
        rows += row('U %s–N · %s' % (k.upper(), t('t10')), F.n(min(v)) + uV, F.n(pct(v)) + uV, F.n(max(v)) + uV,
                    '—', F.rng(207, 253, 0) + uV, ok)
    v = col('thdu_pcc_pct'); rows += row('THD(U) · ' + t('t10'), F.n(min(v)) + uP, F.n(pct(v)) + uP, F.n(max(v)) + uP, '≤ ' + F.n(8, 0) + uP, '≤ ' + F.n(12, 0) + uP, ok)
    v = col('unbalance_pcc_pct'); rows += row(t('unb') + ' · ' + t('t10'), F.n(min(v), 2) + uP, F.n(pct(v), 2) + uP, F.n(max(v), 2) + uP, '≤ ' + F.n(2, 0) + uP, '≤ ' + F.n(4, 0) + uP, ok)
    rows += row('Pst · ' + t('t10'), F.n(min(PST), 2), F.n(pct(PST), 2), F.n(max(PST), 2), '—', '≤ ' + F.n(1.38, 2), ok)
    rows += row('Plt · ' + t('t2h'), F.n(min(PLT), 2), F.n(pct(PLT), 2), F.n(max(PLT), 2), '—', '≤ ' + F.n(1.0, 1), ok)
    v = col('freq_hz'); rows += row(t('freq') + ' · ' + t('t10'), F.n(min(v), 2) + uHz, F.n(pct(v), 2) + uHz, F.n(max(v), 2) + uHz, '50 ± ' + F.n(0.2) + uHz, '50 ± ' + F.n(0.4) + uHz, inf)
    rb = ''.join('<tr><td>U %s–N</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td></tr>'
                 % (k.upper(), F.n(min(col('u_pv_' + k))) + uV, F.n(pct(col('u_pv_' + k))) + uV, F.n(max(col('u_pv_' + k))) + uV)
                 for k in ('l1', 'l2', 'l3'))
    th = t('pq_h').split('|')
    page(7, t('s6'),
         '<h1>%s</h1><table class="pq"><tr>%s</tr>%s</table><p class="note" style="margin-top:2.5mm">%s</p>'
         '<div class="two"><div>%s<table><tr>%s</tr>%s</table></div><div>%s%s</div></div>%s%s'
         % (t('h1_6'), ''.join('<th%s>%s</th>' % (' class="n"' if 0 < i < 4 else '', x) for i, x in enumerate(th)), rows,
            t('pq_note'), H2('pb_h'),
            ''.join('<th%s>%s</th>' % (' class="n"' if i else '', x) for i, x in enumerate(t('pb_th').split('|'))), rb,
            '<h2>&nbsp;</h2>', P('pb_p'), H2('dip_h'), P('dip_p')))

    # 08 причина
    bg = lambda v, lab: '<div><b>%s</b><span class="note">%s</span></div>' % (v, t(lab))
    three = ''.join('<div><span class="v">%s</span><b>%s</b>%s</div>' % (v, t(a), t(b)) for v, a, b in (
        (V['du_lo'] + '–' + V['du_hi'] + uV, 'c1t', 'c1p'), ('≈ ' + V['e8_drop'] + uV, 'c2t', 'c2p'),
        (V['sw_lo'] + '–' + V['sw_hi'] + uV, 'c3t', 'c3p')))
    page(8, t('s7'),
         '<h1>%s</h1><div class="big hl">%s%s%s%s</div>%s<div class="eq">%s<br>%s</div>%s<p class="note">%s</p>'
         '%s<div class="three">%s</div><div class="box g">%s%s</div><div class="two"><div>%s%s</div><div>%s%s</div></div>'
         % (t('h1_7'), bg('B ' + V['e8_b'] + uV, 'bg1'), bg('A ' + V['e8_a'] + uV, 'bg2'),
            bg('ΔU ' + V['e8_du'] + uV, 'bg3'), bg(V['e8_pct'] + uP, 'bg4'),
            H2('calc_h'), t('eq1'), t('eq2'), P('calc_p'), t('calc_r'),
            H2('three_h'), three, H2('concl_h'), P('concl_p'),
            H2('open_h'), ul('open_l'), H2('other_h'), P('other_p')))

    # 09 шаги
    steps = ''.join('<div class="step"><i>%02d</i><div><b>%s</b><p>%s</p></div></div>' % (i, t('a%dt' % i), t('a%dp' % i))
                    for i in range(1, 6))
    page(9, t('s8'),
         '<h1>%s</h1><p style="margin-bottom:5mm;max-width:150mm">%s</p><div class="steps">%s</div><div class="box g">%s%s</div>'
         % (t('h1_8'), t('act_intro'), steps, H2('acc_h'), ul('acc_l')))

    # 10 рамки
    dl = ''.join('<dt>%s</dt><dd>%s</dd>' % tuple(x.split('=', 1)) for x in t('terms').split('|'))
    st = ''.join('<dt>%s</dt><dd>%s</dd>' % tuple(x.split('=', 1)) for x in t('stds').split('|'))
    page(10, t('s9'),
         '<h1>%s</h1><div class="two"><div>%s%s</div><div>%s%s</div></div>%s<dl>%s</dl>%s<dl>%s</dl>'
         '<div class="sample"><b>%s</b><p>%s</p></div>'
         % (t('h1_9'), H2('del_h'), ul('del_l'), H2('out_h'), ul('out_l'), H2('terms_h'), dl, H2('stds_h'), st,
            t('smp_h'), t('about_p')))

    html = ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title><style>%s%s</style></head>'
            '<body>%s</body></html>' % (lang, t('doc_title'), '\n'.join(fonts), css, ''.join(pages)))
    os.makedirs(OUT, exist_ok=True)
    fn = os.path.join(OUT, 'report-%s.html' % lang)
    open(fn, 'w', encoding='utf-8').write(html)
    return fn, V


if __name__ == '__main__':
    for lang in ('en', 'hy'):
        fn, V = build(lang)
        print(fn)
    print({k: v for k, v in V.items()})
