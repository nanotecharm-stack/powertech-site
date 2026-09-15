# -*- coding: utf-8 -*-
"""Раздел 03, шаг 2 (владелец, 2026-09-15: «слишком кричит текст, экран перегружен»):
крупный лозунг .display снят, его смысл — тихой подписью над полем записи.
Запуск из powertech-v2-build: python patches/patch_week2_2026_09_15.py"""
import io, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

p = os.path.join(HERE, 'build.py'); s = io.open(p, encoding='utf-8').read()
a = " 'SVC_DISPLAY': 'Measured<br>under actual<br><span class=\"ac\">load</span>',"
assert s.count(a) == 1
s = s.replace(a, a + "\n 'SVC_CAP': 'Measured under actual load',")
a = " 'SVC_DISPLAY': 'Չափումներ՝<br>փաստացի<br><span class=\"ac\">բեռնվածությամբ</span>',"
assert s.count(a) == 1
s = s.replace(a, a + "\n 'SVC_CAP': 'Չափումներ՝ փաստացի բեռնվածությամբ',")
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = os.path.join(HERE, 'shell.html'); s = io.open(p, encoding='utf-8').read()
old = '''    <p class="lede">%%SVC_P2%%</p></div>
    <div class="display rv">%%SVC_DISPLAY%%</div>
  </div>'''
new = '''    <p class="lede">%%SVC_P2%%</p></div>
  </div>'''
assert s.count(old) == 1; s = s.replace(old, new)
old = '''  <div class="obs wk rv" id="obs">
    <div class="wk-days" aria-hidden="true">%%SVC_DAYS%%</div>'''
new = '''  <div class="obs wk rv" id="obs">
    <div class="wk-cap">%%SVC_CAP%%</div>
    <div class="wk-days" aria-hidden="true">%%SVC_DAYS%%</div>'''
assert s.count(old) == 1; s = s.replace(old, new)
old = '''.svc-head{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);column-gap:clamp(32px,5vw,96px);align-items:end;}
.svc-head .display{margin:0;padding-bottom:4px;}
@media (max-width:960px){.svc-head{grid-template-columns:1fr;row-gap:28px;}.svc-head .display{padding-bottom:0;}}'''
new = '''/* Лозунг .display снят (владелец, 2026-09-15: «слишком кричит»); шапка раздела —
   одна колонка, как в остальных разделах. Его слова — подписью .wk-cap над полем. */
.svc-head{display:block;}'''
assert s.count(old) == 1; s = s.replace(old, new)
old = '#obs.wk{display:block;}\n'
new = '''#obs.wk{display:block;}
#obs.wk .wk-cap{font-family:%%MONOFONT%%;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--brand-ink);margin-bottom:22px;}
html[lang="hy"] #obs.wk .wk-cap{font-family:%%BODYFONT%%;font-size:13px;letter-spacing:.02em;text-transform:none;}
'''
assert s.count(old) == 1; s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
