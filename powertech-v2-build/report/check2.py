# Сверка: каждое слово исходного PDF владельца должно стоять в переверстанном PDF, и наоборот.
# Допустимая разница одна: слово GRIDEC в шапке (там теперь логотип-картинка) — 10 раз.
import collections, re, subprocess, sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
import pypdfium2 as pdfium
bad = 0
for L in ('EN', 'HY'):
    new = os.path.join(HERE, 'out', 'GRIDEC_Demonstration_Report_%s.pdf' % L)
    raw = subprocess.run(['pdftotext', '-raw', '-enc', 'UTF-8', new, '-'], capture_output=True).stdout.decode('utf-8')
    src = open(os.path.join(HERE, 'revised', '%s_raw.txt' % L.lower()), encoding='utf-8').read()
    # дефис и тире тоже делят слово: перенос строки после них pdftotext отдаёт пробелом
    norm = lambda s: collections.Counter(re.split(r'[\s •\-–]+', s.replace(' ՝', '՝')))  # «՝» после «մ» pdftotext отрывает пробелом; на листе знак стоит вплотную (проверено увеличением)
    a, b = norm(src), norm(raw)
    chars = lambda s: collections.Counter(re.sub(r'[\s •]', '', s))
    ca, cb = chars(src), chars(raw)
    cdiff = dict(ca - cb), dict(cb - ca)
    miss, extra = a - b, b - a
    n = len(pdfium.PdfDocument(new))
    ok = dict(miss) == {'GRIDEC': 10} and not extra and n == 10
    bad += not ok
    print(L, 'chars missing/extra', cdiff, 'pages', n, 'source words', sum(a.values()), 'missing', dict(miss), 'extra', dict(extra), 'OK' if ok else 'FAIL')
sys.exit(bad)
