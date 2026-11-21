#!/bin/sh
# Печатает переверстанный отчёт владельца (gen2.py) в PDF через Chrome. Запуск: sh make_pdf2.sh
set -e
cd "$(dirname "$0")"
python gen2.py > /dev/null
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
for L in en hy; do
  U=$(echo "$L" | tr a-z A-Z)
  "$CH" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=4000 \
    --print-to-pdf="$(cygpath -w "$PWD/out/GRIDEC_Demonstration_Report_$U.pdf")" \
    "file:///$(cygpath -m "$PWD/out/report2-$L.html")" 2>/dev/null
done
ls -la out/GRIDEC_Demonstration_Report_*.pdf
