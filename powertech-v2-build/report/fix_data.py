# Приводит учебные данные к одному виду: 10-минутный файл — основа, журнал отключений
# и 20-мс запись E-08 пересчитаны под него. Исходники владельца лежат в data-src и не
# меняются. Запуск: python fix_data.py
#
# Что было не так (проверка 2026-11-21): в журнале мощность перед отключением 82–90 кВт,
# а в 10-минутном файле те же минуты дают 73–96,5 кВт; в 20-мс записи точка A стояла на
# 240 В и не реагировала на отключение, хотя по 10-минутным данным A падает вместе с
# выдачей СЭС. Колонка plt_pcc шла с шагом 10 минут — это Pst, Plt считается за 2 часа.
import csv, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, DST = os.path.join(HERE, 'data-src'), os.path.join(HERE, 'data')
K = 0.1382   # В на кВт: подъём напряжения на линии A–B, как он заложен в 10-минутном файле


def rd(n):
    return list(csv.DictReader(open(os.path.join(SRC, n), encoding='utf-8-sig')))


def wr(n, rows, cols):
    with open(os.path.join(DST, n), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])


t = rd('GRIDEC_example_10min_data.csv')
cols = [c if c != 'plt_pcc' else 'pst_pcc' for c in t[0].keys()]
for r in t:
    r['pst_pcc'] = r.pop('plt_pcc')
wr('GRIDEC_example_10min_data.csv', t, cols)
idx = {r['time']: i for i, r in enumerate(t)}

ev = rd('GRIDEC_example_inverter_events.csv')
for r in ev:
    i = idx[r['timestamp_local'].replace('T', ' ')[:15] + '0:00']
    rows = [t[i]] + ([t[i + 1]] if float(t[i + 1]['inv_off_sec']) > 0 else [])
    on = 600 * len(rows) - sum(float(x['inv_off_sec']) for x in rows)
    p = sum(float(x['pv_kw']) for x in rows) * 600 / on      # мощность, пока инвертор работал
    dur = int(r['duration_sec'])
    assert abs(sum(float(x['inv_off_sec']) for x in rows) - dur) < 1, r['event_id']
    r['p_pv_pre_trip_kw'] = '%.1f' % p
    r['u_pcc_l2_at_event_v'] = '%.1f' % (float(r['u_pv_l2_max_20ms_v']) - K * p)
    r['est_lost_kwh'] = '%.2f' % (float(r['p_pv_pre_trip_kw']) * dur / 3600)
wr('GRIDEC_example_inverter_events.csv', ev, list(ev[0].keys()))

# 20-мс запись E-08
e = ev[-1]
i = idx['2026-06-14 13:10:00']
p0 = float(e['p_pv_pre_trip_kw'])
a_pre = float(t[i - 1]['u_pcc_l2'])
b_peak, a_peak = float(e['u_pv_l2_max_20ms_v']), float(e['u_pcc_l2_at_event_v'])
swell = a_peak - a_pre
# уровень A при отключённой СЭС — из среднего за 10 минут с отключением
off = float(t[i]['inv_off_sec'])
on_before = 98.0
a_off = (float(t[i]['u_pcc_l2']) * 600 - on_before * a_pre
         - (600 - on_before - off) * float(t[i + 1]['u_pcc_l2'])) / off
drop = a_pre - a_off
pw = math.log((253.0 - (a_pre + K * p0)) / swell) / math.log(3.9 / 6)   # 253 В за 2,1 с до нуля
rnd = random.Random(8)
out = []
for n in range(-1000, 1001):
    s = n * 0.02
    if s <= -6:
        sw = 0.0
    elif s <= 0:
        sw = ((s + 6) / 6) ** pw
    else:
        sw = math.exp(-s / 1.5)
    pv = p0 if s <= 0 else max(0.0, p0 * (1 - s / 0.1))
    ns = 0 if n == 0 else rnd.gauss(0, 0.02)
    a = a_pre + swell * sw - drop * (1 - pv / p0) + ns
    b = a + K * pv + (0 if n == 0 else rnd.gauss(0, 0.015)) + (0.1 if pv == 0 else 0)
    ms = 38000 + n * 20
    out.append({'timestamp_local': '2026-06-14T13:11:%02d.%03d' % (ms // 1000, ms % 1000),
                'relative_s': '%.2f' % s, 'u_pcc_l2_rms_20ms_v': '%.3f' % a,
                'u_pv_l2_rms_20ms_v': '%.3f' % b, 'pv_kw_synthetic_interp': '%.1f' % pv})
wr('GRIDEC_example_E08_20ms_RMS.csv', out, list(out[0].keys()))

o = rd('GRIDEC_example_other_PQ_events.csv')
wr('GRIDEC_example_other_PQ_events.csv', o, list(o[0].keys()))
print('ok', a_pre, a_peak, a_off, pw)
for r in ev:
    print(r)
