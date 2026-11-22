#!/bin/sh
# Печатает финальные отчёты EN и HY (gen_en_final.py, gen_hy_final.py) в PDF через Chrome
# и пишет, сколько места осталось до низа на каждой странице (gap<0 = текст не влез).
# Запуск: sh make_pdf_final.sh
set -e
cd "$(dirname "$0")"
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
for L in en hy; do
  U=$(echo "$L" | tr a-z A-Z)
  python gen_${L}_final.py > /dev/null
  "$CH" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=4000 \
    --print-to-pdf="$(cygpath -w "$PWD/out/GRIDEC_Demonstration_Report_${U}_FINAL.pdf")" \
    "file:///$(cygpath -m "$PWD/out/report-$L-final.html")" 2>/dev/null
  CHECK=1 python gen_${L}_final.py > /dev/null
  "$CH" --headless=new --disable-gpu --virtual-time-budget=4000 --dump-dom \
    "file:///$(cygpath -m "$PWD/out/report-$L-final-check.html")" 2>/dev/null \
    | python -c "import sys,re;d=sys.stdin.buffer.read().decode('utf-8');m=re.search(r'<pre id=\"ovf\">(.*?)</pre>',d,re.S);print('$U',m.group(1) if m else 'NO CHECK')"
  rm -f "out/report-$L-final-check.html"
done
ls -la out/GRIDEC_Demonstration_Report_*_FINAL.pdf
