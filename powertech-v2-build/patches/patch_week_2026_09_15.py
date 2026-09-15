# -*- coding: utf-8 -*-
"""Раздел 03: «неделя записи» вместо крупных чисел и головки записи по прокрутке
(владелец, 2026-09-15: «текст с цифрами и анимация задачу не решают»).
Запуск из powertech-v2-build: python patches/patch_week_2026_09_15.py"""
import io, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- build.py ----------
p = os.path.join(HERE, 'build.py'); s = io.open(p, encoding='utf-8').read()
old = "    return ''.join('<div class=\"step\"><p>%s</p></div>' % p for _n, p in items)"
new = old + '''

def steps_tagged_html(items, tags):
    """Шаги с меткой места во времени (до записи / во время / после) — метка
    не номер, а привязка к неделе записи над рядом (2026-09-15)."""
    return ''.join('<div class="step"><span class="stag">%s</span><p>%s</p></div>' % (t, p)
                   for (_n, p), t in zip(items, tags))

def days_html(word):
    """Семь подписей над полем записи: «Day 1 … Day 7» / «Օր 1 … Օր 7»."""
    return ''.join('<span>%s %d</span>' % (word, i) for i in range(1, 8))'''
assert s.count(old) == 1; s = s.replace(old, new)
a = "'H1SIZE', 'H2SIZE', 'DISPSIZE', 'SVC_STATS', 'SVC_STEPS', 'REP_LIST',"
assert s.count(a) == 1
s = s.replace(a, "'H1SIZE', 'H2SIZE', 'DISPSIZE', 'SVC_STATS', 'SVC_STEPS', 'SVC_DAYS', 'REP_LIST',")

old_en = """ 'SVC_STEPS': steps_html([
    ('01', 'Before monitoring starts, we agree on the equipment to assess, the measurements required and the decision the results will support.'),
    ('02', 'We take measurements during the agreed operating conditions.'),
    ('03', 'We analyse the recorded data and present our conclusions and recommended next steps in the report.')]),"""
new_en = """ 'SVC_DAYS': days_html('Day'),
 'SVC_STEPS': steps_tagged_html([
    ('01', 'Before monitoring starts, we agree on the equipment to assess, the measurements required and the decision the results will support.'),
    ('02', 'We take measurements during the agreed operating conditions.'),
    ('03', 'We analyse the recorded data and present our conclusions and recommended next steps in the report.')],
    ['Before recording', 'During recording', 'After recording']),"""
assert s.count(old_en) == 1; s = s.replace(old_en, new_en)
old_hy = """ 'SVC_STEPS': steps_html([
    ('01', 'Նախ հստակեցնում ենք՝ ինչ ենք ստուգելու, որ սարքավորումների վրա և ինչ որոշում եք կայացնելու արդյունքների հիման վրա։'),
    ('02', 'Չափումները կատարում ենք համակարգի աշխատանքի ընթացքում՝ ընդգրկելով համաձայնեցված աշխատանքային ռեժիմները։'),
    ('03', 'Վերլուծում ենք գրանցված տվյալները և հաշվետվության մեջ ներկայացնում եզրակացություններն ու առաջարկվող քայլերը։')]),"""
new_hy = """ 'SVC_DAYS': days_html('Օր'),
 'SVC_STEPS': steps_tagged_html([
    ('01', 'Նախ հստակեցնում ենք՝ ինչ ենք ստուգելու, որ սարքավորումների վրա և ինչ որոշում եք կայացնելու արդյունքների հիման վրա։'),
    ('02', 'Չափումները կատարում ենք համակարգի աշխատանքի ընթացքում՝ ընդգրկելով համաձայնեցված աշխատանքային ռեժիմները։'),
    ('03', 'Վերլուծում ենք գրանցված տվյալները և հաշվետվության մեջ ներկայացնում եզրակացություններն ու առաջարկվող քայլերը։')],
    ['Գրանցումից առաջ', 'Գրանցման ընթացքում', 'Գրանցումից հետո']),"""
assert s.count(old_hy) == 1; s = s.replace(old_hy, new_hy)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# ---------- shell.html ----------
p = os.path.join(HERE, 'shell.html'); s = io.open(p, encoding='utf-8').read()
i0 = s.index('  <!-- ПОЛЕ НАБЛЮДЕНИЯ (бриф 2).'); i1 = s.index('  <a class="alink rv" href="#report">')
markup = '''  <!-- НЕДЕЛЯ ЗАПИСИ (2026-09-15, владелец: «цифры и анимация задачу не решают»).
       Поле — семь суток по 24 деления: 7 — это семь колонок, 24/7 — 168 часовых
       делений и непрерывная линия, 1 — документ в конце линии. Три факта стоят
       подписями к частям поля, три шага — под ним с метками «до / во время / после».
       Ничего не движется по прокрутке: поле статично, как чертёж. -->
  <div class="obs wk rv" id="obs">
    <div class="wk-days" aria-hidden="true">%%SVC_DAYS%%</div>
    <div class="obs-field" aria-hidden="true">
      <svg class="obs-svg" preserveAspectRatio="none">
        <g class="obs-ruler"></g>
        <path class="obs-rec" d=""/>
        <g class="obs-marks"></g>
      </svg>
    </div>
    <div class="stats">%%SVC_STATS%%</div>
    <div class="steps">%%SVC_STEPS%%</div>
  </div>
'''
s = s[:i0] + markup + s[i1:]

anchor = '''@media (prefers-reduced-motion:reduce){.obs .step p{color:rgba(239,237,234,.9);}
  .obs .step{border-left-color:var(--brand);}.obs .step::before{background:var(--brand);}}'''
assert s.count(anchor) == 1
css = '''
/* ---- Неделя записи (2026-09-15) — правила с #obs.wk перекрывают прежнюю шкалу
   с крупными числами и головкой записи, включая её мобильные правила ниже. ---- */
#obs.wk{display:block;}
#obs.wk .wk-days{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));
  font-family:%%MONOFONT%%;font-size:12px;letter-spacing:.08em;color:var(--on-dark-small);}
html[lang="hy"] #obs.wk .wk-days{font-family:%%BODYFONT%%;font-size:13px;letter-spacing:.02em;}
#obs.wk .wk-days span{display:block;padding-left:10px;border-left:1px solid rgba(239,237,234,.22);line-height:1;padding-bottom:12px;}
#obs.wk .obs-field{height:clamp(72px,8vw,104px);margin-top:0;}
#obs.wk .obs-ruler line{stroke:rgba(239,237,234,.2);stroke-width:1;}
#obs.wk .obs-ruler .obs-day{stroke:rgba(239,237,234,.38);}
#obs.wk .obs-rec{fill:none;stroke:var(--brand);stroke-width:1.6;stroke-dasharray:none;}
#obs.wk .obs-marks path{fill:none;stroke:var(--brand);stroke-width:1.4;}
#obs.wk .obs-marks .obs-dot{fill:var(--brand);stroke:none;}
/* Три факта — подписи к полю: число в строку с подписью, не витрина. */
#obs.wk .stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:var(--s5);margin-top:var(--s4);}
#obs.wk .stat,#obs.wk .stat:nth-child(1),#obs.wk .stat:nth-child(2),#obs.wk .stat:nth-child(3){grid-column:auto;display:flex;align-items:baseline;gap:10px;align-self:start;text-align:left;}
#obs.wk .stat:nth-child(2){justify-content:center;}
#obs.wk .stat:nth-child(3){justify-content:flex-end;text-align:right;}
#obs.wk .stat b,#obs.wk .stat:nth-child(1) b,#obs.wk .stat:nth-child(2) b,#obs.wk .stat:nth-child(3) b{display:inline;font-family:%%HEADFONT%%;font-weight:%%HEADWT%%;font-size:calc(26px * var(--hs));line-height:1;letter-spacing:0;color:#F4F3F1;}
#obs.wk .stat span{display:inline;margin:0;font-size:var(--t-note);line-height:1.4;color:var(--on-dark-small);}
/* Шаги — ряд под неделей, статичный. Метка места во времени вместо номера. */
#obs.wk .steps{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));column-gap:0;margin-top:clamp(40px,4.5vw,64px);}
#obs.wk .step,#obs.wk .step:nth-child(1),#obs.wk .step:nth-child(2),#obs.wk .step:nth-child(3){border-left:1px solid rgba(239,237,234,.22);padding:2px clamp(var(--s4),2vw,var(--s6)) 0 clamp(var(--s4),2vw,var(--s6));}
#obs.wk .step:nth-child(1){grid-column:1 / span 2;}
#obs.wk .step:nth-child(2){grid-column:3 / span 3;}
#obs.wk .step:nth-child(3){grid-column:6 / span 2;}
#obs.wk .step::before{display:none;}
#obs.wk .step .stag{display:block;font-family:%%MONOFONT%%;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--brand-ink);margin-bottom:12px;}
html[lang="hy"] #obs.wk .step .stag{font-family:%%BODYFONT%%;font-size:13px;letter-spacing:.02em;text-transform:none;}
#obs.wk .step p{color:rgba(239,237,234,.88);}
@media (max-width:767px){
  #obs.wk .wk-days span:nth-child(n+2){visibility:hidden;}
  #obs.wk .wk-days span:nth-child(7){visibility:visible;}
  #obs.wk .obs-field{height:56px;}
  #obs.wk .stats{grid-template-columns:1fr;row-gap:10px;}
  #obs.wk .stat:nth-child(2),#obs.wk .stat:nth-child(3){justify-content:flex-start;text-align:left;}
  #obs.wk .steps{grid-template-columns:1fr;row-gap:24px;}
  #obs.wk .step,#obs.wk .step:nth-child(1),#obs.wk .step:nth-child(2),#obs.wk .step:nth-child(3){grid-column:auto;}
}'''
s = s.replace(anchor, anchor + css)

j0 = s.index("var obsEl=document.getElementById('obs')")
j1 = s.index("addEventListener('resize',function(){requestAnimationFrame(function(){obsW=-1;buildObs();});});")
js = '''var obsEl=document.getElementById('obs'),obsSvg=obsEl?obsEl.querySelector('.obs-svg'):null,obsW=-1,obsH=-1;
/* Неделя записи: 7 суток × 24 часовых деления, непрерывная линия от точки
   включения до документа. Строится один раз и на resize; по прокрутке — ничего. */
function buildObs(){
  if(!obsSvg)return;
  var r=obsSvg.getBoundingClientRect(),W=r.width,H=r.height;
  if(!W||!H||(Math.abs(W-obsW)<0.5&&Math.abs(H-obsH)<0.5))return;obsW=W;obsH=H;
  var f=function(v){return (+v).toFixed(1);},yr=Math.round(H*0.46)+0.5,yb=H-0.5,i,x,g='';
  obsSvg.setAttribute('viewBox','0 0 '+f(W)+' '+f(H));
  for(i=0;i<=168;i++){x=W*i/168-0.5;var day=(i%24===0);if(i===0)x=0.5;if(i===168)x=W-0.5;
    g+='<line class="'+(day?'obs-day':'')+'" x1="'+f(x)+'" y1="'+f(yb-(day?16:5))+'" x2="'+f(x)+'" y2="'+f(yb)+'"/>';}
  g+='<line x1="0" y1="'+f(yb)+'" x2="'+f(W)+'" y2="'+f(yb)+'"/>';
  obsSvg.querySelector('.obs-ruler').innerHTML=g;
  var xe=W-14;
  obsSvg.querySelector('.obs-rec').setAttribute('d','M0 '+f(yr)+' H'+f(xe-2));
  /* включение — точка; конец — лист документа с загнутым углом */
  var m='<rect class="obs-dot" x="-3.5" y="'+f(yr-3.5)+'" width="7" height="7"/>'
       +'<path d="M'+f(xe)+' '+f(yr-9)+' h9 l5 5 v13 h-14 z M'+f(xe+9)+' '+f(yr-9)+' v5 h5"/>';
  obsSvg.querySelector('.obs-marks').innerHTML=m;
}
function mObs(){return null;}
function aObs(){}
function obsUpd(){buildObs();}
buildObs();
'''
s = s[:j0] + js + s[j1:]
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
