# Сверка финальных PDF с текстами владельца (GRIDEC_EN_revised_text.md, GRIDEC_HY_revised_synced.md).
# Запуск: python check_final.py <папка с этими двумя md>
# Сравнивает мешки слов без учёта регистра и отдельно все числа. Ожидаемая разница — только служебные
# пометки md (Header:, Footer:, Legend:, «Էջատակի տեքստ՝» …), заголовки таблиц-пар «Item/Value»,
# подпись оси дат «08.06–15.06 (date)» (на графике это сама шкала) и номера страниц.
import collections, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
for L, mdn in (('EN', 'GRIDEC_EN_revised_text.md'), ('HY', 'GRIDEC_HY_revised_synced.md')):
    pdf = os.path.join(HERE, 'out', 'GRIDEC_Demonstration_Report_%s_FINAL.pdf' % L)
    raw = subprocess.run(['pdftotext', '-raw', '-enc', 'UTF-8', pdf, '-'], capture_output=True).stdout.decode('utf-8')
    md = open(os.path.join(sys.argv[1], mdn), encoding='utf-8').read().split('\n---\n', 1)[1]
    def bag(s):
        s = s.lower().replace('և', 'եվ').replace('u_b', 'ub').replace('u_a', 'ua').replace('’', "'")
        s = re.sub(r'[*#|>•]|:?-{3,}:?', ' ', s)
        return collections.Counter(w for w in re.split(r'[\s\-–—]+', s.replace(' ՝', '՝')) if w)
    a, b = bag(md), bag(raw)
    nums = lambda s: collections.Counter(re.findall(r'\d+(?:[,.:]\d+)*', s))
    na, nb = nums(md), nums(raw)
    print('==', L, 'pages', raw.count('\f'))
    print(' IN MD, NOT IN PDF:', dict(a - b))
    print(' IN PDF, NOT IN MD:', dict(b - a))
    print(' NUMBERS md-pdf:', dict(na - nb), '| pdf-md:', dict(nb - na))
    print(' old labels left:', [t for t in ('A–B, ', 'U>', 'երկու PDF', 'were available for this revision', '124.83', '124,83', 'FEEDER RISE') if t in raw])
