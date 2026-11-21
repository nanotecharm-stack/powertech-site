#!/bin/sh
# Печатает оба отчёта в PDF через Chrome без окна. Запуск из папки report: sh make_pdf.sh
set -e
cd "$(dirname "$0")"
python gen.py > /dev/null
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
for L in en hy; do
  U=$(echo "$L" | tr a-z A-Z)
  "$CH" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=4000 \
    --print-to-pdf="$(cygpath -w "$PWD/out/GRIDEC_Sample_Report_PV_Trips_$U.pdf")" \
    "file:///$(cygpath -m "$PWD/out/report-$L.html")" 2>/dev/null
done
ls -la out/*.pdf
