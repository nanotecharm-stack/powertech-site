# Готовит файлы отчёта для сайта: две страницы-миниатюры на язык (WebP, 720 px) и копии
# PDF и ZIP в report/site. build.py кладёт эту папку в uploads/report.
# Запуск после make_pdf.sh:  python make_site_assets.py
import os, shutil
import pypdfium2 as pdfium
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT, SITE = os.path.join(HERE, 'out'), os.path.join(HERE, 'site')
PAGES = (4, 6)      # неделя с графиками и запись одного события
shutil.rmtree(SITE, ignore_errors=True)
os.makedirs(SITE, exist_ok=True)
for lang in ('EN', 'HY'):
    pdf = 'GRIDEC_Demonstration_Report_%s.pdf' % lang
    doc = pdfium.PdfDocument(os.path.join(OUT, pdf))
    for no in PAGES:
        im = doc[no - 1].render(scale=3).to_pil().convert('RGB')
        im = im.resize((720, round(720 * im.height / im.width)), Image.LANCZOS)
        fn = os.path.join(SITE, 'page-%s-%d.webp' % (lang.lower(), no))
        im.save(fn, 'WEBP', quality=82, method=6)
        print(fn, im.size, os.path.getsize(fn))
    doc.close()
    shutil.copyfile(os.path.join(OUT, pdf), os.path.join(SITE, pdf))
# ZIP с данными на сайт больше не идёт (2026-11-22): отчёт владельца собран из другой модели,
# её CSV не присылали, а прежний архив с этим отчётом не сходится.
