# -*- coding: utf-8 -*-
"""UI/UX audit pass (2026-09-14) — applied to shell.html and build.py.

Brief of the owner, nine items:
  2  industries: sticky horizontal rail -> static 3x2 grid (2 cols tablet, 1 col phone),
     «Other critical electrical systems» as one compact row under the grid, cards are
     real buttons (heading button + stretched hit area);
  3  typography tokens: body 18 (17 phone), lede 19 (18), question 18 (17), notes 16,
     parameter names 16, nav/buttons 14-15, aux labels 13-14; Armenian: Mardoto for
     everything (400/500/700 real files), Arian AMU Serif removed from UI labels, less
     tracking, no forced caps;
  4  «Seven-day monitoring»: head in two columns (text | thesis), stats one uniform
     row; «About us»: three-column editorial grid instead of the diagonal; section
     spacing tightened;
  5  contact chart: line in the light accent, labels as HTML at 13px, dashed nominal
     line 3:1;
  6  accordion keeps the clicked heading in place; H1 decrypt and index letter
     animations removed; dither bands shorter and without the accent flash; reveals
     and hovers 150-500ms; parameter tiles have no hover (no action);
  7  form: no field numbers, 46px fields, 16px input text, 44px close and remove
     buttons, required = name + message + (email or phone), per-field errors;
  8  anchors offset by the fixed header (scroll-margin-top), modal focus return from
     the actual trigger.

Re-runnable: every replacement asserts the old text exists exactly once (or the
given count), so a second run fails loudly instead of double-patching.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
os.chdir(ROOT)

def load(fn):
    return io.open(fn, encoding='utf-8').read()

def save(fn, s):
    io.open(fn, 'w', encoding='utf-8', newline='\n').write(s)

class P:
    def __init__(self, fn):
        self.fn = fn; self.s = load(fn); self.n = 0
    def rep(self, old, new, count=1):
        c = self.s.count(old)
        if c != count:
            raise SystemExit('%s: expected %d, found %d for:\n%s' % (self.fn, count, c, old[:160]))
        self.s = self.s.replace(old, new); self.n += 1
    def done(self):
        save(self.fn, self.s); print(self.fn, self.n, 'replacements')

# ============================================================== shell.html
sh = P('shell.html')

# ---------------------------------------------------------------- 3 typography tokens
sh.rep(""":root{--t-p:17px;--t-p-lh:1.6;--t-lede:19px;--t-lede-lh:1.55;--t-hp:clamp(17px,1.45vw,20px);--t-hp-lh:1.55;
  --t-hp-hy:clamp(17px,1.45vw,20px);--t-small:15px;--t-small-lh:1.55;--t-tag:12px;--t-q:17px;""",
""":root{--t-p:18px;--t-p-lh:1.6;--t-lede:19px;--t-lede-lh:1.55;--t-hp:clamp(17px,1.45vw,20px);--t-hp-lh:1.55;
  --t-hp-hy:clamp(17px,1.45vw,20px);--t-small:16px;--t-small-lh:1.55;--t-tag:13px;--t-q:18px;
  /* Аудит 2026-09-14: единые роли. --t-note — технические примечания и названия величин (16),
     --t-ui — навигация и кнопки (14–15), --t-aux — вспомогательные подписи (13). 11–12 px
     остаются только у коротких приборных отметок (счётчик раздела, номера в указателе). */
  --t-note:16px;--t-note-lh:1.6;--t-ui:14px;--t-aux:13px;""")
sh.rep("""  --t-ls:.01em;}
body{""", """  --t-ls:.01em;}
@media (max-width:767px){:root{--t-p:17px;--t-lede:18px;--t-q:17px;}}
/* Якоря учитывают закреплённую шапку (62 px): раздел встаёт под ней, а не за ней. */
section[id],#end{scroll-margin-top:72px;}
body{""")

# .lede pair spacing
sh.rep(".lede + .lede{margin-top:34px;}", ".lede + .lede{margin-top:22px;}")
# reveals: shorter, smaller travel
sh.rep(".rv{opacity:0;transform:translateY(20px);transition:opacity .9s var(--e),transform .9s var(--e);}",
       ".rv{opacity:0;transform:translateY(12px);transition:opacity .5s var(--e),transform .5s var(--e);}")
# section counter run: keep 11px Departure Mono (short marker) — untouched.
sh.rep(".eyebrow{font-family:%%MONOFONT%%;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--brand-ink);}",
       ".eyebrow{font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.16em;text-transform:uppercase;color:var(--brand-ink);}")

# index panel: plain titles, no per-letter animation
sh.rep(""".ixp a .tl{font-size:16px;line-height:1.35;color:rgba(239,237,234,.86);
  display:inline-flex;flex-wrap:wrap;}
.ixp .tl .wd{display:inline-flex;white-space:nowrap;}
.ixp .tl .sp{display:inline-block;width:.31em;}
.ixp .tl .lt{display:inline-block;overflow:hidden;height:1.35em;}
/* Разбег стоит ТОЛЬКО на наведении. Когда он висел на самой букве, он
   отрабатывал и на уходе курсора: строка возвращалась ещё треть секунды после
   того, как указатель ушёл, и рядом уже начинала реагировать следующая — на
   экране всегда было две живых строки вместо одной. Обратный ход короче и без
   задержек: строка гаснет разом, как только курсор ушёл. */
.ixp .tl .lt i{display:block;height:1.35em;font-style:normal;
  transition:transform .3s var(--e);transition-delay:0s;}
.ixp a:hover .tl .lt i,.ixp a:focus-visible .tl .lt i{transform:translateY(-100%);
  transition:transform .6s var(--e);transition-delay:var(--d,0ms);}
.ixp a:hover .tl{color:#F4F3F1;}""",
""".ixp a .tl{font-size:17px;line-height:1.35;color:rgba(239,237,234,.88);transition:color .2s var(--e);}
/* Посимвольный разбег названий снят (аудит 2026-09-14): спокойная смена цвета. */
.ixp a:hover .tl{color:#F4F3F1;}""")
sh.rep(""".ixp{display:grid;grid-template-rows:0fr;opacity:0;
  transition:grid-template-rows .5s var(--e),opacity .34s var(--e);}
.ixp.on{grid-template-rows:1fr;opacity:1;
  transition:grid-template-rows .5s var(--e),opacity .2s var(--e);}""",
""".ixp{display:grid;grid-template-rows:0fr;opacity:0;
  transition:grid-template-rows .3s var(--e),opacity .25s var(--e);}
.ixp.on{grid-template-rows:1fr;opacity:1;
  transition:grid-template-rows .3s var(--e),opacity .2s var(--e);}""")
sh.rep(""".ixp li{opacity:0;transform:translateY(-9px);
  transition:opacity .4s var(--e),transform .4s var(--e);}
.ixp.on li{opacity:1;transform:none;
  transition-delay:calc(var(--i,0) * 34ms + 90ms);}""",
""".ixp li{opacity:0;transform:translateY(-6px);
  transition:opacity .25s var(--e),transform .25s var(--e);}
.ixp.on li{opacity:1;transform:none;
  transition-delay:calc(var(--i,0) * 18ms + 60ms);}""")
sh.rep("""  .ixp .tl .lt i{transition:none;}
  .ixp a:hover .tl .lt i{transform:none;}}""", """}""")

# language switch and header: 13px
sh.rep(".lang{display:inline-flex;align-items:center;gap:6px;font-family:%%BODYFONT%%;font-size:12px;font-weight:500;letter-spacing:.08em;padding:9px var(--s3);",
       ".lang{display:inline-flex;align-items:center;gap:6px;font-family:%%BODYFONT%%;font-size:var(--t-aux);font-weight:500;letter-spacing:.06em;padding:9px var(--s3);")
sh.rep("""html[data-nav="5"] .ixw{display:inline;align-self:center;font-size:13px;
  letter-spacing:.01em;text-transform:none;font-weight:500;}""",
"""html[data-nav="5"] .ixw{display:inline;align-self:center;font-size:var(--t-ui);
  letter-spacing:.01em;text-transform:none;font-weight:500;}""")
sh.rep("""html[data-nav="5"][lang="hy"] .ixw{font-family:%%BODYFONT%%;text-transform:none;
  font-size:13px;letter-spacing:.01em;}""",
"""html[data-nav="5"][lang="hy"] .ixw{font-family:%%BODYFONT%%;text-transform:none;
  font-size:var(--t-ui);letter-spacing:.01em;}""")
sh.rep("""html[data-nav="5"] .lang{padding:7px 9px;margin-right:-9px;position:relative;font-size:12px;}""",
       """html[data-nav="5"] .lang{padding:7px 9px;margin-right:-9px;position:relative;font-size:var(--t-aux);}""")
# hover transitions on buttons: shorter
sh.rep(".btn::before{content:\"\";position:absolute;inset:0;background:var(--brand);transform:scaleX(0);transform-origin:left;transition:transform .5s var(--e);}",
       ".btn::before{content:\"\";position:absolute;inset:0;background:var(--brand);transform:scaleX(0);transform-origin:left;transition:transform .25s var(--e);}")
sh.rep(".btn span{position:relative;z-index:1;transition:color .4s var(--e);}",
       ".btn span{position:relative;z-index:1;transition:color .2s var(--e);}")
sh.rep("""  background:color-mix(in srgb,var(--inv-fg) 16%,transparent);font-style:normal;font-size:12px;
  transition:transform .45s var(--e),background .4s var(--e);}""",
"""  background:color-mix(in srgb,var(--inv-fg) 16%,transparent);font-style:normal;font-size:12px;
  transition:transform .2s var(--e),background .2s var(--e);}""")

# hero: no decrypt styles, larger photo labels, secondary link 15px
sh.rep("""/* Расшифровка заголовка при загрузке — один прогон; при reduce текст стоит готовым. */
.hero h1 .dtw{display:inline-block;white-space:pre;}
.hero h1 [data-dt="s"]{color:color-mix(in srgb,var(--fg) 42%,var(--bg));}
.hero h1 [data-dt="l"]{animation:dtflash .42s cubic-bezier(.2,0,0,1);}
@keyframes dtflash{
  0%{color:var(--brand);text-shadow:0 0 24px color-mix(in srgb,var(--brand) 70%,transparent);}
  100%{text-shadow:0 0 0 transparent;}}
""", "")
sh.rep("""  font-size:14px;font-weight:500;color:var(--fg-mid);text-decoration:underline;text-underline-offset:4px;""",
       """  font-size:15px;font-weight:500;color:var(--fg-mid);text-decoration:underline;text-underline-offset:4px;""")
sh.rep(""".hmark{position:absolute;left:var(--hx);top:20%;margin:0;width:max-content;max-width:20%;
  font-family:%%MONOFONT%%;font-size:11px;line-height:2.1;letter-spacing:.15em;font-weight:500;
  color:#17334A;opacity:.85;}""",
""".hmark{position:absolute;left:var(--hx);top:20%;margin:0;width:max-content;max-width:22%;
  font-family:%%MONOFONT%%;font-size:var(--t-aux);line-height:2;letter-spacing:.12em;font-weight:500;
  color:#17334A;}""")
sh.rep("""  .hmark{font-size:10px;}
}""", """  .hmark{font-size:12px;}
}""")
sh.rep("""  .hmark{position:static;width:auto;max-width:none;padding:12px clamp(20px,4vw,24px) 0;font-size:11px;line-height:1.7;letter-spacing:.12em;}""",
       """  .hmark{position:static;width:auto;max-width:none;padding:12px clamp(20px,4vw,24px) 0;font-size:var(--t-aux);line-height:1.7;letter-spacing:.1em;}""")

# ---------------------------------------------------------------- 2 industries grid
i0 = sh.s.index("/* industries — horizontal rail, detail opens on click */")
i1 = sh.s.index("/* what we measure — signatures in a table of cells.")
sh.s = sh.s[:i0] + """/* ============ 02 — ОТРАСЛИ: СЕТКА (аудит 2026-09-14) ============
   Прежняя закреплённая лента (4300 px прокрутки при 1363) снята. Шесть карточек —
   сетка 3×2 на настольном, 2 колонки на планшете, 1 на телефоне (кадр шире и ниже).
   Карточка — фотография с названием; действие — настоящая кнопка в заголовке с
   растянутой зоной нажатия, кольцо фокуса рисуется на всей карточке.
   «Другие критические электрические системы» — отдельная компактная строка под сеткой. */
.igrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,1.6vw,22px);
  margin-top:clamp(24px,3vw,40px);}
.icard{position:relative;display:flex;flex-direction:column;overflow:hidden;
  background:#101218;color:#EFEDEA;border:1px solid #101218;border-radius:2px;}
.ic-art{position:relative;aspect-ratio:4/3;overflow:hidden;background:#15171E;}
.ic-art img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;
  transform:scale(1.04);transform-origin:52% 45%;transition:transform .3s var(--e);}
.icard:hover .ic-art img,.icard:focus-within .ic-art img{transform:scale(1.07);}
.ic-art::after{content:"";position:absolute;pointer-events:none;z-index:2;inset:-1px;
  background:linear-gradient(180deg,rgba(13,14,19,.35) 0%,rgba(13,14,19,.04) 40%,rgba(16,18,24,.9) 82%,#101218 100%);}
.ic-foot{position:absolute;left:0;right:0;bottom:0;z-index:3;display:flex;align-items:flex-end;
  justify-content:space-between;gap:14px;padding:0 18px 18px;}
.ic-foot h3{margin:0;font-size:clamp(18px,1.55vw,23px);line-height:1.2;letter-spacing:.005em;}
.ic-open{appearance:none;background:none;border:0;padding:0;margin:0;font:inherit;color:inherit;
  text-align:left;cursor:pointer;}
/* растянутая зона: вся карточка нажимается, а семантика остаётся у кнопки */
.ic-open::after{content:"";position:absolute;inset:0;z-index:4;}
.ic-open:focus-visible{outline:none;}
.icard:focus-within{outline:2px solid var(--brand-ink);outline-offset:3px;}
.ic-go{width:40px;height:40px;border-radius:2px;background:#EFEDEA;color:#101218;flex:0 0 auto;
  display:grid;place-items:center;transition:background .2s var(--e),color .2s var(--e);}
.ic-go svg{width:19px;height:19px;display:block;}
.icard:hover .ic-go,.icard:focus-within .ic-go{background:var(--brand);color:var(--brand-on);}
/* строка «другие системы»: волосяные линии, без плашки и скруглений */
.iother{margin-top:clamp(22px,2.6vw,36px);padding:clamp(18px,2vw,26px) 0;
  border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);
  display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:clamp(20px,3vw,48px);align-items:center;}
.iother h3{font-size:clamp(18px,1.6vw,22px);margin:0 0 6px;}
.iother p{font-size:var(--t-note);line-height:var(--t-note-lh);color:var(--fg-mid);max-width:62ch;}
.iother .btn{white-space:nowrap;}
.rail-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,38%);
  align-items:start;gap:26px;}
.rail-head .lede{margin-top:0;max-width:none;padding-top:clamp(28px,3.4vw,52px);}
@media (max-width:1024px){.igrid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media(max-width:900px){.rail-head{grid-template-columns:1fr;gap:14px;}}
@media (max-width:600px){
  .igrid{grid-template-columns:1fr;gap:12px;}
  .ic-art{aspect-ratio:2/1;}
  .ic-foot{padding:0 16px 14px;}
  .iother{grid-template-columns:1fr;row-gap:16px;}
}

""" + sh.s[i1:]
sh.n += 1

# ---------------------------------------------------------------- 06 tiles: no hover, 16px labels
sh.rep(""".mi{position:relative;padding:clamp(20px,2.2vw,30px) clamp(var(--s4),1.8vw,26px);
  display:flex;flex-direction:column;gap:var(--s4);
  border-left:1px solid var(--hair2);transition:background .45s var(--e);}""",
""".mi{position:relative;padding:clamp(20px,2.2vw,30px) clamp(var(--s4),1.8vw,26px);
  display:flex;flex-direction:column;gap:var(--s4);
  border-left:1px solid var(--hair2);}""")
sh.rep(""".mi svg{width:52px;height:34px;display:block;overflow:visible;color:var(--fg);
  transition:color .45s var(--e),transform .5s var(--e);}
.mi .mlb{font-size:14px;line-height:1.42;color:var(--fg);}
.mi:hover{background:rgba(13,14,19,.04);}
.mi:hover svg{transform:translateY(-2px);}""",
""".mi svg{width:52px;height:34px;display:block;overflow:visible;color:var(--fg);}
/* Плитки без действия — без отклика на наведение (аудит 2026-09-14). */
.mi .mlb{font-size:var(--t-note);line-height:1.4;color:var(--fg);}""")
sh.rep(".mi-alt:hover{background:var(--alt-wash-h);}\n", "")
sh.rep(".plate2 .mi:hover{background:rgba(239,237,234,.05);}\n", "")

# ---------------------------------------------------------------- section spacing
sh.rep(".sec{padding:clamp(56px,7vw,104px) 0 clamp(var(--s8),8vw,120px);}",
       ".sec{padding:clamp(52px,6.2vw,92px) 0 clamp(52px,6.2vw,92px);}")
sh.rep("#company{padding-top:clamp(76px,10.5vw,158px);}", "#company{padding-top:clamp(64px,7.5vw,112px);}")
sh.rep(""".alink{display:inline-flex;align-items:center;gap:9px;margin-top:34px;
  padding-block:9px;margin-bottom:-9px;font-family:%%MONOFONT%%;font-size:14px;""",
""".alink{display:inline-flex;align-items:center;gap:9px;margin-top:34px;
  padding-block:9px;margin-bottom:-9px;font-family:%%MONOFONT%%;font-size:var(--t-ui);""")

# ---------------------------------------------------------------- 03 seven-day monitoring
sh.rep(""".display{font-family:%%HEADFONT%%;font-weight:%%HEADWT%%;font-size:%%DISPSIZE%%;line-height:.96;%%HEADTT%%color:var(--fg);margin:clamp(36px,5vw,var(--s8)) 0 0;}""",
""".display{font-family:%%HEADFONT%%;font-weight:%%HEADWT%%;font-size:%%DISPSIZE%%;line-height:.96;%%HEADTT%%color:var(--fg);margin:clamp(36px,5vw,var(--s8)) 0 0;}
/* Шапка раздела в две колонки (аудит 2026-09-14): слева номер, заголовок и два вводных
   абзаца, справа крупный тезис по нижней линии текста. Пустое поле справа ушло. */
.svc-head{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);column-gap:clamp(32px,5vw,96px);align-items:end;}
.svc-head .display{margin:0;padding-bottom:4px;}
@media (max-width:960px){.svc-head{grid-template-columns:1fr;row-gap:28px;}.svc-head .display{padding-bottom:0;}}""")
sh.rep(""".obs{--ocol:clamp(16px,1.8vw,24px);margin-top:clamp(40px,5.5vw,72px);""",
       """.obs{--ocol:clamp(16px,1.8vw,24px);margin-top:clamp(36px,4.5vw,60px);""")
# stats: one uniform row
sh.rep(""".obs .stat{background:none;box-shadow:none;padding:0;border-radius:0;align-self:end;}
.obs .stat:nth-child(1){grid-column:1 / span 4;}
.obs .stat:nth-child(2){grid-column:5 / span 4;text-align:center;}
.obs .stat:nth-child(3){grid-column:9 / span 4;text-align:right;}
.obs .stat b{display:block;font-family:%%HEADFONT%%;font-weight:%%HEADWT%%;line-height:.92;letter-spacing:-.02em;color:#F4F3F1;}
.obs .stat:nth-child(1) b{font-size:clamp(64px,9vw,128px);}
.obs .stat:nth-child(2) b{font-size:clamp(30px,3.6vw,52px);}
.obs .stat:nth-child(3) b{font-size:clamp(48px,6.4vw,92px);}
.obs .stat span{display:block;margin-top:var(--s2);font-size:14px;line-height:1.5;color:var(--on-dark-small);}""",
""".obs .stat{background:none;box-shadow:none;padding:0;border-radius:0;align-self:end;}
/* Три показателя — один ряд одним кеглем, каждый над своей третью поля (аудит 2026-09-14). */
.obs .stat:nth-child(1){grid-column:1 / span 4;}
.obs .stat:nth-child(2){grid-column:5 / span 4;}
.obs .stat:nth-child(3){grid-column:9 / span 4;}
.obs .stat b{display:block;font-family:%%HEADFONT%%;font-weight:%%HEADWT%%;line-height:.92;letter-spacing:-.02em;color:#F4F3F1;
  font-size:clamp(44px,5.2vw,76px);}
.obs .stat span{display:block;margin-top:var(--s2);font-size:var(--t-note);line-height:1.5;color:var(--on-dark-small);}""")
sh.rep(""".obs .step p{color:rgba(239,237,234,.62);transition:color .5s var(--e);}""",
       """.obs .step p{color:rgba(239,237,234,.78);transition:color .3s var(--e);}""")

# ---------------------------------------------------------------- 04 report notes 16px
sh.rep(""".note{font-size:14px;line-height:1.75;color:var(--fg-soft);""", """.note{font-size:var(--t-note);line-height:var(--t-note-lh);color:var(--fg-soft);""")
sh.rep(""".lnote{font-size:14px;line-height:1.75;color:var(--fg-soft);""", """.lnote{font-size:var(--t-note);line-height:var(--t-note-lh);color:var(--fg-soft);""")
sh.rep("""  font-size:16px;line-height:calc(var(--row) / 2);
  color:var(--fg);""", """  font-size:17px;line-height:calc(var(--row) / 2);
  color:var(--fg);""")
sh.rep("""  color:#EFEDEA;padding:clamp(72px,7vw,104px) 0 var(--rep-over);}""",
       """  color:#EFEDEA;padding:clamp(56px,6.2vw,92px) 0 var(--rep-over);}""")
sh.rep("""  align-items:start;padding-bottom:clamp(64px,8vw,120px);}""", """  align-items:start;padding-bottom:clamp(48px,6vw,96px);}""")
sh.rep(""".list div>*{opacity:0;transform:translateY(5px);
  transition:opacity .6s var(--e),transform .6s var(--e);
  transition-delay:calc(var(--i) * 34ms);}""",
""".list div>*{opacity:0;transform:translateY(4px);
  transition:opacity .35s var(--e),transform .35s var(--e);
  transition-delay:calc(var(--i) * 25ms);}""")
sh.rep("""  background:var(--hair2);transform:scaleX(0);transform-origin:left;
  transition:transform .8s var(--e),background-color .3s var(--e);
  transition-delay:calc(var(--i) * 34ms);}""",
"""  background:var(--hair2);transform:scaleX(0);transform-origin:left;
  transition:transform .5s var(--e),background-color .2s var(--e);
  transition-delay:calc(var(--i) * 25ms);}""")

# ---------------------------------------------------------------- 05 accordion
sh.rep(""".qa-q:hover .qa-t{color:var(--brand-ink);}""", """.qa-q:hover .qa-t,.qa-q:focus-visible .qa-t{color:var(--brand-ink);}""")
sh.rep(""".qa-t{transition:color .3s var(--e);}""", """.qa-t{transition:color .2s var(--e);}""")
sh.rep(""".qa-a{display:grid;grid-template-rows:0fr;transition:grid-template-rows .22s var(--e);}""",
       """.qa-a{display:grid;grid-template-rows:0fr;transition:grid-template-rows .22s var(--e);}
.qa-a.still{transition:none;}
/* hidden — настоящее display:none: авторский display:grid перебивал правило браузера, и
   «скрытый» ответ оставался в раскладке и анимировался. */
.qa-a[hidden]{display:none;}""")

# ---------------------------------------------------------------- 07 company grid
sh.rep(""".story{margin-top:clamp(var(--s7),6vw,var(--s9));display:grid;
  grid-template-columns:repeat(12,minmax(0,1fr));
  column-gap:clamp(var(--s4),1.8vw,var(--s5));row-gap:clamp(var(--s8),7vw,var(--s10));}
.story .sb{position:relative;display:block;grid-column:1 / span 6;
  border-top:1px solid var(--hair);}
.story .sb:nth-child(2){grid-column:4 / span 6;}
.story .sb:nth-child(3){grid-column:7 / span 6;}""",
"""/* Аудит 2026-09-14: диагональ снята — три главы стоят в ряд, читаются слева направо,
   подпись сидит на общей линейке. На телефоне — одна колонка. */
.story{margin-top:clamp(40px,5vw,72px);display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  column-gap:clamp(24px,3vw,48px);row-gap:clamp(32px,4vw,48px);}
.story .sb{position:relative;display:block;grid-column:auto;
  border-top:1px solid var(--hair);}""")
sh.rep(""".story .lb{font-family:%%MONOFONT%%;font-size:12px;letter-spacing:.16em;""",
       """.story .lb{font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.14em;""")
sh.rep("""@media (max-width:860px){.story{grid-template-columns:1fr;row-gap:clamp(var(--s6),8vw,var(--s8));}
  .story .sb,.story .sb:nth-child(2),.story .sb:nth-child(3){grid-column:1 / -1;}
  .story p{max-width:none;}
}""", """@media (max-width:860px){.story{grid-template-columns:1fr;row-gap:clamp(28px,6vw,40px);}
  .story p{max-width:none;}
}""")

# ---------------------------------------------------------------- 08 contact + chart
sh.rep(""".plate .wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,70px);align-items:center;padding-top:clamp(70px,9vw,130px);padding-bottom:clamp(70px,9vw,130px);}""",
       """.plate .wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,70px);align-items:center;padding-top:clamp(64px,7.5vw,108px);padding-bottom:clamp(64px,7.5vw,108px);}""")
sh.rep(""".chart{position:relative;}
.chart svg{width:100%;height:auto;display:block;}
.chart .cap{font-family:%%MONOFONT%%;font-size:11px;letter-spacing:.12em;color:rgba(239,237,234,.58);margin-bottom:var(--s3);}""",
""".chart{position:relative;}
/* Аудит 2026-09-14: линия — светлый акцент плиты (#7BA4D0, ≈6:1 на #0D2440), подписи —
   HTML-текст 13 px поверх SVG, а не текст внутри viewBox (тот масштабировался до 8–10 px).
   Пунктир номинала .44 — 3,4:1 на самом светлом тоне плиты. */
.chart svg{width:100%;height:auto;display:block;overflow:visible;}
.chart .cap{font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.1em;color:var(--on-dark-small);margin-bottom:var(--s4);}
.chart-box{position:relative;}
.chart .nom{stroke:rgba(239,237,234,.44);stroke-dasharray:3 5;}
.chart .trace{stroke:var(--brand);stroke-width:2.2;stroke-linecap:round;fill:none;}
.chart .dipm{stroke:rgba(239,237,234,.5);}
.chart .lb{position:absolute;font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.1em;
  color:#E8E3DB;line-height:1.3;white-space:nowrap;}
.chart .lb-nom{left:0;top:calc(40 / 200 * 100% - 24px);}
.chart .lb-dip{left:calc(178 / 520 * 100%);top:calc(128 / 200 * 100% + 8px);}
@media (max-width:420px){.chart .lb{font-size:12px;letter-spacing:.06em;}}""")
sh.rep("""html[lang="hy"] .chart .cap{font-family:%%BODYFONT%%;}""", """html[lang="hy"] .chart .cap,html[lang="hy"] .chart .lb{font-family:%%BODYFONT%%;}""")

# ---------------------------------------------------------------- footer sizes
sh.rep("""footer .fbrand p{margin-top:20px;font-family:%%MONOFONT%%;font-size:11px;
  letter-spacing:.2em;text-transform:uppercase;color:rgba(239,237,234,.5);max-width:24ch;
  line-height:1.9;}""",
"""footer .fbrand p{margin-top:20px;font-family:%%MONOFONT%%;font-size:var(--t-aux);
  letter-spacing:.14em;text-transform:uppercase;color:rgba(239,237,234,.62);max-width:26ch;
  line-height:1.8;}""")
sh.rep(""":lang(hy) footer .fbrand p{letter-spacing:.1em;max-width:28ch;}""",
       """:lang(hy) footer .fbrand p{letter-spacing:.04em;max-width:30ch;text-transform:none;}""")
sh.rep("""footer h3{font-family:%%MONOFONT%%;font-size:11px;letter-spacing:.18em;font-weight:400;
  text-transform:uppercase;color:rgba(239,237,234,.5);margin-bottom:20px;""",
"""footer h3{font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.14em;font-weight:400;
  text-transform:uppercase;color:rgba(239,237,234,.62);margin-bottom:20px;""")
sh.rep("""footer .flist a{display:block;
  font-size:14px;line-height:1.5;color:var(--on-dark-link);""", """footer .flist a{display:block;
  font-size:15px;line-height:1.5;color:var(--on-dark-link);""")
sh.rep("""  font-family:%%MONOFONT%%;font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:rgba(239,237,234,.42);}""", """  font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.1em;text-transform:uppercase;
  color:rgba(239,237,234,.62);}""")
sh.rep("""footer .fpp{font:inherit;letter-spacing:inherit;text-transform:inherit;padding:0;
  color:rgba(239,237,234,.6);""", """footer .fpp{font:inherit;letter-spacing:inherit;text-transform:inherit;padding:6px 0;
  color:rgba(239,237,234,.7);""")
sh.rep("""footer .flang{color:rgba(239,237,234,.6);padding:7px 11px;""", """footer .flang{color:rgba(239,237,234,.75);padding:9px 13px;""")

# ---------------------------------------------------------------- modals: 44px close, 16px notes
sh.rep(""".md .x{position:absolute;top:14px;right:14px;width:34px;height:34px;border-radius:2px;
  background:#14161C;color:#EFEDEA;z-index:5;font-size:15px;line-height:1;""",
""".md .x{position:absolute;top:12px;right:12px;width:44px;height:44px;border-radius:2px;
  background:#14161C;color:#EFEDEA;z-index:5;font-size:18px;line-height:1;""")
sh.rep("""#imd .lb{font-family:%%MONOFONT%%;font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--brand-ink);margin:26px 0 var(--s1);}""",
       """#imd .lb{font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.12em;text-transform:uppercase;color:var(--brand-ink);margin:26px 0 var(--s1);}""")
sh.rep("""#imd .fi{display:flex;gap:var(--s3);align-items:baseline;font-size:14px;line-height:1.65;padding:11px 0;border-top:1px solid var(--hair2);}""",
       """#imd .fi{display:flex;gap:var(--s3);align-items:baseline;font-size:var(--t-note);line-height:1.6;padding:11px 0;border-top:1px solid var(--hair2);}""")
sh.rep("""#imd .st .sx{font-size:14px;line-height:1.62;color:var(--fg-mid);max-width:48ch;}
#imd .st .ss{font-family:%%MONOFONT%%;font-size:11px;color:var(--fg-soft);margin-top:7px;}""",
"""#imd .st .sx{font-size:var(--t-note);line-height:1.6;color:var(--fg-mid);max-width:48ch;}
#imd .st .ss{font-family:%%MONOFONT%%;font-size:var(--t-aux);color:var(--fg-soft);margin-top:7px;}""")
sh.rep("""#fmd .fpriv{margin-top:16px;font-size:12px;line-height:1.65;max-width:56ch;""",
       """#fmd .fpriv{margin-top:16px;font-size:14px;line-height:1.6;max-width:56ch;""")
sh.rep("""#pmd .lede{font-size:14px;line-height:1.7;margin:0 0 var(--s4);max-width:56ch;""",
       """#pmd .lede{font-size:var(--t-note);line-height:1.6;margin:0 0 var(--s4);max-width:56ch;""")
sh.rep("""#pmd .pps h4{font-family:%%MONOFONT%%;font-size:11px;font-weight:500;letter-spacing:.18em;""",
       """#pmd .pps h4{font-family:%%MONOFONT%%;font-size:var(--t-aux);font-weight:500;letter-spacing:.14em;""")
sh.rep("""#pmd .pps p{font-size:14px;line-height:1.72;color:var(--fg-mid);max-width:62ch;margin:0 0 10px;}""",
       """#pmd .pps p{font-size:var(--t-note);line-height:1.6;color:var(--fg-mid);max-width:62ch;margin:0 0 10px;}""")
sh.rep("""  font-family:%%MONOFONT%%;font-size:11px;font-weight:500;letter-spacing:.13em;
  text-transform:uppercase;color:var(--fg-soft);}""", """  font-family:%%MONOFONT%%;font-size:var(--t-aux);font-weight:500;letter-spacing:.1em;
  text-transform:uppercase;color:var(--fg-soft);}""")

# ---------------------------------------------------------------- 7 form
sh.rep("""#fmd .intro{font-size:14px;line-height:1.7;margin-bottom:28px;max-width:56ch;""",
       """#fmd .intro{font-size:var(--t-note);line-height:1.6;margin-bottom:28px;max-width:56ch;""")
sh.rep("""#fmd form{counter-reset:fld;}
""", "")
sh.rep("""#fmd .ghd{font-family:%%MONOFONT%%;font-size:11px;letter-spacing:.18em;""",
       """#fmd .ghd{font-family:%%MONOFONT%%;font-size:var(--t-aux);letter-spacing:.14em;""")
sh.rep("""#fmd .gl,#fmd label{display:flex;align-items:baseline;gap:var(--s3);
  font-family:%%BODYFONT%%;font-size:13px;font-weight:500;letter-spacing:0;
  text-transform:none;color:var(--fg);margin:0 0 10px;}
#fmd .gl::before,#fmd label::before{counter-increment:fld;
  content:counter(fld,decimal-leading-zero);
  font-family:'Departure Mono',monospace;font-size:11px;letter-spacing:.1em;
  color:var(--brand-ink);flex:0 0 auto;}""",
"""/* Нумерация полей снята (аудит 2026-09-14): подпись 14 px, поле 46 px, текст ввода 16 px. */
#fmd .gl,#fmd label{display:flex;align-items:baseline;gap:var(--s2);
  font-family:%%BODYFONT%%;font-size:14px;font-weight:500;letter-spacing:0;
  text-transform:none;color:var(--fg);margin:0 0 6px;}
#fmd .fr .opt,#fmd .gl small{font-weight:400;color:var(--fg-soft);font-size:var(--t-aux);}
#fmd .ghd-note{font-size:14px;line-height:1.5;color:var(--fg-soft);margin:-8px 0 18px;}
/* Ошибка у своего поля: появляется только с текстом, читается диктором как alert. */
#fmd .ferr{display:none;font-size:14px;line-height:1.45;color:#A8341F;margin-top:6px;}
#fmd .ferr.on{display:block;}""")
sh.rep("""#fmd .gl small{font-weight:400;text-transform:none;letter-spacing:0;color:var(--fg-soft);font-size:12px;}
#fmd .fr{display:grid;grid-template-columns:1fr 1fr;gap:30px 40px;margin-top:6px;}""",
       """#fmd .fr{display:grid;grid-template-columns:1fr 1fr;gap:22px 40px;margin-top:6px;}""")
sh.rep("""#fmd input[type=text],#fmd input[type=email],#fmd input[type=tel]{
  width:100%;background:none;border:0;border-radius:0;padding:9px 2px;
  font-size:16px;font-family:inherit;color:var(--fg);outline:none;""",
"""#fmd input[type=text],#fmd input[type=email],#fmd input[type=tel]{
  width:100%;background:none;border:0;border-radius:0;padding:11px 2px;min-height:46px;
  font-size:16px;line-height:1.5;font-family:inherit;color:var(--fg);outline:none;""")
sh.rep("""#fmd textarea{width:100%;background:#F7F5F4;border:0;border-radius:2px;
  padding:14px 15px;font-size:15px;font-family:inherit;color:var(--fg);""",
"""#fmd textarea{width:100%;background:#F7F5F4;border:0;border-radius:2px;
  padding:14px 15px;font-size:16px;font-family:inherit;color:var(--fg);""")
sh.rep("""#fmd .tps button{font-family:%%BODYFONT%%;font-size:13px;letter-spacing:0;
  text-transform:none;padding:10px 14px;border:0;border-radius:2px;""",
"""#fmd .tps button{font-family:%%BODYFONT%%;font-size:14px;letter-spacing:0;
  text-transform:none;padding:12px 16px;min-height:44px;border:0;border-radius:2px;""")
sh.rep("""#fmd .drop b{display:inline;font-family:%%BODYFONT%%;font-size:14px;letter-spacing:0;""",
       """#fmd .drop b{display:inline;font-family:%%BODYFONT%%;font-size:15px;letter-spacing:0;""")
sh.rep("""#fmd .drop span{display:block;margin-top:5px;font-size:13px;line-height:1.6;""",
       """#fmd .drop span{display:block;margin-top:5px;font-size:14px;line-height:1.55;""")
sh.rep("""#fmd .att .sz{font-family:%%MONOFONT%%;font-size:12px;color:var(--fg-soft);}
#fmd .att button{width:22px;height:22px;border-radius:2px;background:var(--hair2);
  font-size:14px;line-height:1;}""",
"""#fmd .att .sz{font-family:%%MONOFONT%%;font-size:var(--t-aux);color:var(--fg-soft);}
#fmd .att button{width:44px;height:44px;margin:-9px -10px -9px 0;border-radius:2px;background:transparent;
  font-size:18px;line-height:1;color:var(--fg);transition:background .2s var(--e),color .2s var(--e);}""")
sh.rep("""#fmd .hint{font-size:12px;color:var(--fg-soft);margin:10px 0 var(--s5);}""",
       """#fmd .hint{font-size:14px;color:var(--fg-soft);margin:10px 0 var(--s5);}""")
sh.rep("""#fmd .done p{font-size:14px;line-height:1.7;color:var(--fg-mid);max-width:40ch;margin:0 auto 26px;}""",
       """#fmd .done p{font-size:var(--t-note);line-height:1.6;color:var(--fg-mid);max-width:40ch;margin:0 auto 26px;}""")
sh.rep("""      #fmd .fr{grid-template-columns:1fr;}
}""", """      #fmd .fr{grid-template-columns:1fr;gap:18px;}
      .md .x{top:8px;right:8px;}
}""")
# header button size on ≤960 stays readable
sh.rep("""  .btn{padding:11px 14px;font-size:12px;}""", """  .btn{padding:11px 14px;font-size:13px;}""")

# ---------------------------------------------------------------- Armenian: Mardoto everywhere, less tracking, no forced caps
sh.rep(""":lang(hy) .tag,:lang(hy) .chart .cap,
:lang(hy) .story .lb span,:lang(hy) .eyebrow,
:lang(hy) footer h3,:lang(hy) #imd .lb,:lang(hy) #fmd .ghd{font-weight:600;}
:lang(hy) .tag{letter-spacing:.07em;}
:lang(hy) .eyebrow{letter-spacing:.12em;}""",
"""/* Аудит 2026-09-14: подписи набраны Mardoto 500 (настоящий файл), сплошные прописные и
   широкая разрядка сняты — армянские прописные строятся из одинаковых стоек и в мелком
   кегле с разрядкой читаются частоколом. Длинные слова переносятся по слогам, где
   браузер умеет, и ломаются по буквам только в крайнем случае. */
:lang(hy) .tag,:lang(hy) .eyebrow,:lang(hy) .story .lb span,:lang(hy) footer h3,
:lang(hy) #imd .lb,:lang(hy) #fmd .ghd,:lang(hy) .chart .cap,:lang(hy) .chart .lb,
:lang(hy) footer .fbot,:lang(hy) .alink,:lang(hy) #pmd .pps h4,:lang(hy) #pmd .ppu,
:lang(hy) .ev-tag,:lang(hy) .hmark{text-transform:none;letter-spacing:.02em;font-weight:500;}
:lang(hy) .eyebrow{letter-spacing:.04em;}
:lang(hy) h1,:lang(hy) h2,:lang(hy) h3,:lang(hy) p,:lang(hy) li,:lang(hy) .mlb{overflow-wrap:break-word;}
:lang(hy) p{hyphens:auto;-webkit-hyphens:auto;}""")
sh.rep("""header nav a{font-family:%%NAVFONT%%;""", """header nav a{font-family:%%BODYFONT%%;""")

# ---------------------------------------------------------------- HTML: hero unchanged; industries
sh.rep("""<section class="sec suite" id="applications"><div class="spin"><div class="wrap">
  <div class="rail-head">
    <div><div class="cnt">02</div><h2>%%APP_H2%%</h2></div>
    <div><p class="lede">%%APP_P%%</p>
    </div>
  </div>
</div>
  <div class="railwrap">
    <div class="hrail" id="irail"></div>
  </div>
</div></section>""",
"""<section class="sec suite" id="applications"><div class="wrap">
  <div class="rail-head rv">
    <div><div class="cnt">02</div><h2>%%APP_H2%%</h2></div>
    <div><p class="lede">%%APP_P%%</p></div>
  </div>
  <!-- Аудит 2026-09-14: сетка 3×2 вместо закреплённой ленты. Карточки строит скрипт из
       PT.cards; без скрипта раздел остаётся с заголовком и строкой ниже. -->
  <div class="igrid" id="irail"></div>
  <div class="iother rv">
    <div><h3>%%OTHER_T%%</h3><p>%%OTHER_P%%</p></div>
    <button class="btn" type="button" data-open-form><span>%%CTA%%</span><i>&#8599;</i></button>
  </div>
</div></section>""")

# 03: head in two columns
sh.rep("""<section class="sec plate2" id="services"><div class="wrap">
  <div class="rv"><div class="cnt">03</div>
  <h2 class="h2gap">%%SVC_H2%%</h2>
  <p class="lede">%%SVC_P1%%</p>
  <p class="lede">%%SVC_P2%%</p></div>
  <div class="display rv">%%SVC_DISPLAY%%</div>""",
"""<section class="sec plate2" id="services"><div class="wrap">
  <div class="svc-head">
    <div class="rv"><div class="cnt">03</div>
    <h2 class="h2gap">%%SVC_H2%%</h2>
    <p class="lede">%%SVC_P1%%</p>
    <p class="lede">%%SVC_P2%%</p></div>
    <div class="display rv">%%SVC_DISPLAY%%</div>
  </div>""")

# 08: chart
sh.rep("""  <div class="chart rv"><div class="cap">%%CT_CAP%%</div>
    <svg viewBox="0 0 520 240" fill="none">
      <line x1="0" y1="60" x2="520" y2="60" stroke="rgba(239,237,234,.14)" stroke-dasharray="3 5"/>
      <text x="0" y="50" fill="rgba(239,237,234,.45)" font-size="10" font-family="%%MONOFONT%%" letter-spacing="1.5">%%CT_NOM%%</text>
      <path d="M0,62 L150,60 C168,60 172,64 178,96 C184,130 188,132 196,132 L236,132 C244,132 248,128 254,94 C260,64 264,61 282,61 L520,60" stroke="#C8603D" stroke-width="2" stroke-linecap="round"/>
      <rect x="178" y="150" width="76" height="1" fill="rgba(239,237,234,.3)"/>
      <text x="178" y="172" fill="rgba(239,237,234,.55)" font-size="10" font-family="%%MONOFONT%%" letter-spacing="1.2">%%CT_DIP%%</text>
    </svg>
  </div>""",
"""  <div class="chart rv"><div class="cap">%%CT_CAP%%</div>
    <div class="chart-box">
    <svg viewBox="0 0 520 200" fill="none" aria-hidden="true">
      <line class="nom" x1="0" y1="40" x2="520" y2="40"/>
      <path class="trace" d="M0,42 L150,40 C168,40 172,44 178,76 C184,110 188,112 196,112 L236,112 C244,112 248,108 254,74 C260,44 264,41 282,41 L520,40"/>
      <line class="dipm" x1="178" y1="128" x2="254" y2="128"/>
    </svg>
    <span class="lb lb-nom">%%CT_NOM%%</span>
    <span class="lb lb-dip">%%CT_DIP%%</span>
    </div>
  </div>""")

# form fields: required = name + message + one contact
sh.rep("""    <div class="ghd">%%F_CONTACT%%</div>
    <div class="fr">
      <div><label for="ptfName">%%F_NAME%% <em>*</em></label><input id="ptfName" name="name" type="text" autocomplete="name" placeholder="%%F_NAME_PH%%" required aria-required="true"></div>
      <div><label for="ptfCompany">%%F_COMPANY%% <em>*</em></label><input id="ptfCompany" name="company" type="text" autocomplete="organization" placeholder="%%F_COMPANY_PH%%" required aria-required="true"></div>
      <div><label for="ptfEmail">%%F_EMAIL%% <em>*</em></label><input id="ptfEmail" name="email" type="email" autocomplete="email" placeholder="name@company.com" required aria-required="true"></div>
      <div><label for="ptfPhone">%%F_PHONE%% <em>*</em></label><input id="ptfPhone" name="phone" type="tel" autocomplete="tel" placeholder="+374 ..." required aria-required="true"></div>
    </div>""",
"""    <div class="ghd">%%F_CONTACT%%</div>
    <p class="ghd-note" id="ghdNote">%%F_ONE_CONTACT%%</p>
    <div class="fr">
      <div><label for="ptfName">%%F_NAME%% <em>*</em></label><input id="ptfName" name="name" type="text" autocomplete="name" placeholder="%%F_NAME_PH%%" required aria-required="true" aria-describedby="ptfNameErr"><span class="ferr" id="ptfNameErr" role="alert"></span></div>
      <div><label for="ptfCompany">%%F_COMPANY%% <span class="opt">%%F_ATT_OPT%%</span></label><input id="ptfCompany" name="company" type="text" autocomplete="organization" placeholder="%%F_COMPANY_PH%%"></div>
      <div><label for="ptfEmail">%%F_EMAIL%% <em>*</em></label><input id="ptfEmail" name="email" type="email" autocomplete="email" placeholder="name@company.com" aria-describedby="ghdNote ptfEmailErr"><span class="ferr" id="ptfEmailErr" role="alert"></span></div>
      <div><label for="ptfPhone">%%F_PHONE%% <em>*</em></label><input id="ptfPhone" name="phone" type="tel" autocomplete="tel" placeholder="+374 ..." aria-describedby="ghdNote ptfPhoneErr"><span class="ferr" id="ptfPhoneErr" role="alert"></span></div>
    </div>""")
sh.rep("""    <textarea id="ptfMsg" name="message" placeholder="%%F_MSG_PH%%" required aria-required="true"></textarea>""",
       """    <textarea id="ptfMsg" name="message" placeholder="%%F_MSG_PH%%" required aria-required="true" aria-describedby="ptfMsgErr"></textarea>
    <span class="ferr" id="ptfMsgErr" role="alert"></span>""")

# ---------------------------------------------------------------- JS
# H1 decrypt removed
d0 = sh.s.index("/* ============ DECRYPT H1 — заголовок расшифровывается при загрузке ============ */")
d1 = sh.s.index("/* Грунт шапки и шкала прочтения.")
sh.s = sh.s[:d0] + sh.s[d1:]; sh.n += 1

# accordion: keep the clicked heading where it is
sh.rep("""(function(){
  var list=document.getElementById('qalist');if(!list)return;
  var sec=list.closest('section'),btns=[].slice.call(list.querySelectorAll('.qa-q')),pics=[].slice.call(sec.querySelectorAll('.qa-pic img'));
  function open(i,first){
    btns.forEach(function(b,k){
      var a=document.getElementById(b.getAttribute('aria-controls')),on=k===i;
      b.setAttribute('aria-expanded',on?'true':'false');
      if(on){a.hidden=false;if(first||rm)a.classList.add('open');else requestAnimationFrame(function(){a.classList.add('open');});}
      else{a.classList.remove('open');
        if(first||rm)a.hidden=true;else setTimeout(function(){if(b.getAttribute('aria-expanded')==='false')a.hidden=true;},240);}
    });
    pics.forEach(function(p,k){p.classList.toggle('on',k===i);});
  }
  btns.forEach(function(b,i){b.addEventListener('click',function(){open(i);});});
  open(1,true);
})();""",
"""(function(){
  var list=document.getElementById('qalist');if(!list)return;
  var sec=list.closest('section'),btns=[].slice.call(list.querySelectorAll('.qa-q')),pics=[].slice.call(sec.querySelectorAll('.qa-pic img'));
  var HDR=72;
  /* Аудит 2026-09-14: при переключении вопроса страница прыгала — закрывающийся ответ ВЫШЕ
     нажатого заголовка отдавал высоту, и заголовок уезжал вверх. Теперь нажатый заголовок
     держится на месте: ответ выше закрывается без перехода, а разница высоты компенсируется
     прокруткой в том же кадре (и в нашей плавной прокрутке, если она включена). Единственная
     прокрутка сверх этого — если заголовок ушёл под шапку, его подводят к ней. */
  function scrollByNow(d){
    var h=document.documentElement,prev=h.style.scrollBehavior;h.style.scrollBehavior='auto';
    window.scrollBy(0,d);
    if(typeof PS!=='undefined'){PS.t=PS.c=window.pageYOffset;}
    h.style.scrollBehavior=prev;
  }
  function open(i,first){
    var b0=btns[i],y0=b0.getBoundingClientRect().top;
    var prevOpen=-1;btns.forEach(function(b,k){if(b.getAttribute('aria-expanded')==='true')prevOpen=k;});
    var above=prevOpen>=0&&prevOpen<i;
    btns.forEach(function(b,k){
      var a=document.getElementById(b.getAttribute('aria-controls')),on=k===i;
      b.setAttribute('aria-expanded',on?'true':'false');
      if(on){a.hidden=false;if(first||rm)a.classList.add('open');else requestAnimationFrame(function(){a.classList.add('open');});}
      else{
        var still=(first||rm||above)&&a.classList.contains('open');
        if(still)a.classList.add('still');
        a.classList.remove('open');
        if(first||rm||above){a.hidden=true;requestAnimationFrame(function(){a.classList.remove('still');});}
        else setTimeout(function(){if(b.getAttribute('aria-expanded')==='false')a.hidden=true;},240);}
    });
    pics.forEach(function(p,k){p.classList.toggle('on',k===i);});
    if(first)return;
    var d=b0.getBoundingClientRect().top-y0;
    if(Math.abs(d)>0.5)scrollByNow(d);
    var top=b0.getBoundingClientRect().top;
    if(top<HDR)scrollByNow(top-HDR);
  }
  btns.forEach(function(b,i){
    b.addEventListener('click',function(){open(i);});
    b.addEventListener('keydown',function(e){
      var j=e.key==='ArrowDown'?i+1:e.key==='ArrowUp'?i-1:e.key==='Home'?0:e.key==='End'?btns.length-1:-1;
      if(j<0||j>=btns.length)return;e.preventDefault();btns[j].focus();
    });
  });
  open(1,true);
})();""")

# industries: grid cards instead of the rail
r0 = sh.s.index("/* ============ INDUSTRIES — a stepped rail of card plates ============ */")
r1 = sh.s.index("var navLinks=[].slice.call(document.querySelectorAll('nav a.lk')).map(function(a){")
sh.s = sh.s[:r0] + """/* ============ INDUSTRIES — сетка карточек (аудит 2026-09-14) ============ */
var irail=document.getElementById('irail');
var iovl=document.getElementById('iovl');
function openInd(o,trigger){
  var ph=document.getElementById('im_ph'),img=ph.firstElementChild;
  if(o.img!==undefined&&PT.imgs[o.img]){
    if(!img){img=document.createElement('img');ph.appendChild(img);}
    /* Малый файл уже в кеше карточки — окно открывается с верным снимком сразу; полный
       подменяет его, когда догрузится. Метка want — на случай быстрого перебора карточек. */
    var _full=PT.imgs[o.img],_small=_full.replace(/\\.jpg$/,'-756.jpg');
    img.dataset.want=_full;img.alt=o.title;img.src=_small;
    img.onerror=function(){if(img.dataset.want===_full&&img.src!==_full)img.src=_full;};
    var _up=new Image();
    _up.onload=function(){if(img.dataset.want===_full)img.src=_full;};
    _up.src=_full;
    ph.style.display='';}
  else ph.style.display='none';
  document.getElementById('im_t').textContent=o.title;
  document.getElementById('im_p1').textContent=o.p1;
  var fi=document.getElementById('im_fi');fi.innerHTML='';
  var hasF=o.findings&&o.findings.length;
  document.getElementById('im_lb').style.display=hasF?'':'none';
  if(hasF)o.findings.forEach(function(f){
    var d=document.createElement('li');d.className='fi';
    d.innerHTML='<em></em><span></span>';
    d.querySelector('span').textContent=f;fi.appendChild(d);});
  var st=document.getElementById('im_st');
  var txt=o.note||o.statText||'';
  if(o.stat||txt){
    st.style.display='';
    document.getElementById('im_big').textContent=o.stat||'';
    document.getElementById('im_sx').textContent=txt;
    document.getElementById('im_ss').textContent=o.note?'':(o.statSource||'');
  }else st.style.display='none';
  openDialog(iovl,document.getElementById('imd'),trigger);
}
if(irail)PT.cards.forEach(function(o,i){
  var card=document.createElement('article');card.className='icard rv';card.style.transitionDelay=(i%3)*60+'ms';
  var src=PT.imgs[o.img]||'';
  card.innerHTML='<div class="ic-art"><img alt="" loading="'+(i<3?'eager':'lazy')+'" decoding="async"></div>'+
    '<div class="ic-foot"><h3><button type="button" class="ic-open"></button></h3>'+
    '<span class="ic-go" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3.7 12.3 12.3 3.7"/><path d="M12.3 8.7V3.7H7.3"/></svg></span></div>';
  var img=card.querySelector('img');
  if(src){img.src=src;img.srcset=src.replace(/\\.jpg$/,'-756.jpg')+' 756w, '+src+' 1536w';img.sizes='(max-width:600px) 100vw, (max-width:1024px) 50vw, 400px';}
  var btn=card.querySelector('.ic-open');btn.textContent=o.title;
  btn.addEventListener('click',function(){openInd(o,btn);});
  irail.appendChild(card);
});

""" + sh.s[r1:]; sh.n += 1

# dither: shorter band, no accent flash
sh.rep("""    var cell=Math.max(30,Math.min(46,Math.round(innerWidth/42)));
    var cols=Math.ceil(innerWidth/cell),rows=Math.max(4,Math.round(312/cell));""",
"""    /* Аудит 2026-09-14: полоса ниже (≈180 вместо 312) и без вспышек акцента. */
    var cell=Math.max(30,Math.min(46,Math.round(innerWidth/42)));
    var cols=Math.ceil(innerWidth/cell),rows=Math.max(3,Math.round(180/cell));""")
sh.rep("""      cells.push({el:i,to:bot,acc:(acc&&Math.random()<0.07)?acc:null,now:top});""",
       """      cells.push({el:i,to:bot,acc:null,now:top});""")

# anchors: no pixel wipe for in-page jumps; header offset
a0 = sh.s.index("/* ЯКОРЬ ЧЕРЕЗ ЗАКРЕПЛЁННУЮ ЛЕНТУ.")
a1 = sh.s.index("var brandA=document.querySelector('.brand');")
sh.s = sh.s[:a0] + """/* Аудит 2026-09-14: закреплённой ленты нет — якоря идут обычной (плавной) прокруткой,
   без перекрытия плашками. Смещение под шапку — scroll-margin-top на разделах и HDR_OFF
   в собственной плавной прокрутке ниже. */
var HDR_OFF=72;
""" + sh.s[a1:]; sh.n += 1
sh.rep("""if(brandA)brandA.addEventListener('click',function(e){
  if(e.metaKey||e.ctrlKey||e.shiftKey)return;
  e.preventDefault();
  e.stopPropagation();          /* иначе общий обработчик якорей начнёт прокрутку */
  if(rm||document.visibilityState!=='visible'||window.pageYOffset<4){wipeToTop();return;}
  wipeCoverThen(function(){wipeToTop();wipeReveal();});
},true);                        /* перехват: опережаем делегированный обработчик */""",
"""if(brandA)brandA.addEventListener('click',function(e){
  if(e.metaKey||e.ctrlKey||e.shiftKey)return;
  e.preventDefault();e.stopPropagation();
  if(typeof PS!=='undefined'&&PS.on){psTo(0);}else{window.scrollTo({top:0,behavior:rm?'auto':'smooth'});}
  setUrlHash('top');
},true);""")
sh.rep("""    psTo(el.getBoundingClientRect().top+window.pageYOffset-(id==='top'?0:26));
    setUrlHash(id);""", """    psTo(el.getBoundingClientRect().top+window.pageYOffset-(id==='top'?0:HDR_OFF));
    setUrlHash(id);""")
sh.rep("""var PS={t:0,c:0,raf:0,last:0,self:false,lerp:0.085,mult:0.9,vmax:9,vmin:0.5};""",
       """var PS={t:0,c:0,raf:0,last:0,self:false,lerp:0.085,mult:0.9,vmax:9,vmin:0.5,on:false};""")
sh.rep("""  document.documentElement.style.scrollBehavior='auto';   /* we do the easing now */
  PS.t=PS.c=window.pageYOffset;""", """  document.documentElement.style.scrollBehavior='auto';   /* we do the easing now */
  PS.on=true;PS.t=PS.c=window.pageYOffset;""")

# form validation: name + message + (email or phone); company optional; per-field errors
sh.rep("""  var nm=gv('ptfName').trim(),co=gv('ptfCompany').trim(),em=gv('ptfEmail').trim(),ph=gv('ptfPhone').trim(),ms=gv('ptfMsg').trim();
  var emailOk=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(em);
  var errs={ptfName:!nm,ptfCompany:!co,ptfEmail:!emailOk,ptfPhone:!ph,ptfMsg:!ms};
  var any=false;Object.keys(errs).forEach(function(k){var el=document.getElementById(k);el.classList.toggle('err',errs[k]);
    if(errs[k]){el.setAttribute('aria-invalid','true');any=true;}else{el.removeAttribute('aria-invalid');}});
  document.getElementById('ptfFormErr').style.display=any?'block':'none';
  if(any)return;""",
"""  var nm=gv('ptfName').trim(),co=gv('ptfCompany').trim(),em=gv('ptfEmail').trim(),ph=gv('ptfPhone').trim(),ms=gv('ptfMsg').trim();
  /* Аудит 2026-09-14: обязательны имя, описание и ХОТЯ БЫ ОДИН контакт. Компания и второй
     контакт — по желанию. Ошибка стоит у своего поля; общая строка — только сводка. */
  var emailOk=!em||/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(em);
  var phoneOk=!ph||(ph.replace(/\\D/g,'').length>=6);
  var noContact=!em&&!ph;
  var errs={ptfName:nm?'':PT.errName,ptfMsg:ms?'':PT.errMsg,
            ptfEmail:noContact?PT.errContact:(emailOk?'':PT.errEmail),
            ptfPhone:noContact?PT.errContact:(phoneOk?'':PT.errPhone)};
  var any=false;Object.keys(errs).forEach(function(k){var el=document.getElementById(k),fe=document.getElementById(k+'Err'),bad=!!errs[k];
    el.classList.toggle('err',bad);
    if(fe){fe.textContent=errs[k]||'';fe.classList.toggle('on',bad);}
    if(bad){el.setAttribute('aria-invalid','true');any=true;}else{el.removeAttribute('aria-invalid');}});
  document.getElementById('ptfFormErr').style.display=any?'block':'none';
  if(any){var firstBad=Object.keys(errs).filter(function(k){return errs[k];})[0];
    if(firstBad)document.getElementById(firstBad).focus();return;}""")
sh.rep("""['ptfName','ptfCompany','ptfEmail','ptfPhone','ptfMsg'].forEach(function(id){
  document.getElementById(id).addEventListener('input',function(){this.classList.remove('err');this.removeAttribute('aria-invalid');document.getElementById('ptfFormErr').style.display='none';});
});""",
"""['ptfName','ptfCompany','ptfEmail','ptfPhone','ptfMsg'].forEach(function(id){
  document.getElementById(id).addEventListener('input',function(){this.classList.remove('err');this.removeAttribute('aria-invalid');
    var fe=document.getElementById(id+'Err');if(fe){fe.textContent='';fe.classList.remove('on');}
    /* контакт один на два поля: ввод в одно снимает ошибку и с другого */
    if(id==='ptfEmail'||id==='ptfPhone'){var o=document.getElementById(id==='ptfEmail'?'ptfPhone':'ptfEmail'),oe=document.getElementById(o.id+'Err');
      if(oe&&oe.textContent===PT.errContact){o.classList.remove('err');o.removeAttribute('aria-invalid');oe.textContent='';oe.classList.remove('on');}}
    document.getElementById('ptfFormErr').style.display='none';});
});""")

# modal plumbing: trigger element for focus return
sh.rep("""function openDialog(ovl,dlg){
  lastFocus=document.activeElement;""", """function openDialog(ovl,dlg,trigger){
  lastFocus=trigger||document.activeElement;""")
sh.rep("""function openForm(){
  document.getElementById('f_main').style.display='';document.getElementById('f_done').style.display='none';
  openDialog(fovl,document.getElementById('fmd'));
}
document.querySelectorAll('[data-open-form]').forEach(function(b){b.addEventListener('click',openForm);});""",
"""function openForm(trigger){
  document.getElementById('f_main').style.display='';document.getElementById('f_done').style.display='none';
  openDialog(fovl,document.getElementById('fmd'),trigger&&trigger.nodeType===1?trigger:null);
}
document.querySelectorAll('[data-open-form]').forEach(function(b){b.addEventListener('click',function(){openForm(b);});});""")
sh.rep("""function openPrivacy(){
  ppFocus=document.activeElement;""", """function openPrivacy(trigger){
  ppFocus=trigger||document.activeElement;""")
sh.rep("""document.querySelectorAll('[data-open-privacy]').forEach(function(b){
  b.addEventListener('click',function(e){e.preventDefault();openPrivacy();});});""",
"""document.querySelectorAll('[data-open-privacy]').forEach(function(b){
  b.addEventListener('click',function(e){e.preventDefault();openPrivacy(b);});});""")

# index: plain titles
sh.rep("""  letterize(li.querySelector('.tl'),it.title);
  li.querySelector('a').setAttribute('aria-label',it.no+' '+it.title);""",
       """  li.querySelector('.tl').textContent=it.title;""")
l0 = sh.s.index("/* Название раскладывается на буквы: при наведении каждая уезжает вверх, а")
l1 = sh.s.index("/* which sheet are we on, and what tone is under the bar */")
sh.s = sh.s[:l0] + sh.s[l1:]; sh.n += 1

# scroll pass: suite removed
sh.rep("""  var dO=mObs(),d2=mSuite(),d3=mJoints(),d5=mDither(),
      d6=mNav(),d7=mReveal(),d8=mHeaderTheme(),d9=mTone(),d10=mIx(),d12=mBar();""",
"""  var dO=mObs(),d3=mJoints(),d5=mDither(),
      d6=mNav(),d7=mReveal(),d8=mHeaderTheme(),d9=mTone(),d10=mIx(),d12=mBar();""")
sh.rep("""  aObs(dO);aSuite(d2);aJoints(d3);aDither(d5);""", """  aObs(dO);aJoints(d3);aDither(d5);""")
sh.rep("""layoutSuite&&layoutSuite();
""", "")
sh.rep("""addEventListener('resize',function(){clearTimeout(sizeT);sizeT=setTimeout(function(){buildJoints();buildWipe();buildDither();layoutSuite();},220);});""",
       """addEventListener('resize',function(){clearTimeout(sizeT);sizeT=setTimeout(function(){buildJoints();buildWipe();buildDither();scrollRepaint();},220);});""")
sh.rep("""addEventListener('load',function(){layoutSuite();scrollRepaint();});""", """addEventListener('load',function(){scrollRepaint();});""")
# focus ring rule for old .ic
sh.rep(""".plate2 a:focus-visible,.plate2 button:focus-visible,
.ic:focus-visible{outline-color:#FFFBF9;}""", """.plate2 a:focus-visible,.plate2 button:focus-visible{outline-color:#FFFBF9;}""")
sh.rep(""".plate,.plate2,.other,.chart,.ixp,.navr,.brand{--brand-ink:#D4714E;}""",
       """.plate,.plate2,.icard,.chart,.ixp,.navr,.brand{--brand-ink:#D4714E;}""")

sh.rep('''@media(max-width:419px){ html[data-nav="5"] .ixw{display:none;} }''','''@media(max-width:419px){ html[data-nav="5"] .ixw{display:none;} }
/* Армянское «Բաժիններ» шире: с глобусом и «ENG» группа выходила за край на 430 (замер +9). Слово
   уходит до 479, кнопка указателя остаётся стрелкой с aria-label; зона нажатия — не ниже 40 px. */
@media(max-width:479px){ html[data-nav="5"][lang="hy"] .ixw{display:none;} html[data-nav="5"] .ixb{padding:12px 6px;margin-right:-6px;} }''')
sh.rep('''.mi{position:relative;padding:clamp(20px,2.2vw,30px) clamp(var(--s4),1.8vw,26px);
  display:flex;flex-direction:column;gap:var(--s4);
  border-left:1px solid var(--hair2);}''','''.mi{position:relative;min-width:0;padding:clamp(20px,2.2vw,30px) clamp(var(--s4),1.8vw,26px);
  display:flex;flex-direction:column;gap:var(--s4);
  border-left:1px solid var(--hair2);}''')
sh.rep(''':lang(hy) p{hyphens:auto;-webkit-hyphens:auto;}''',''':lang(hy) p,:lang(hy) .mlb{hyphens:auto;-webkit-hyphens:auto;}
:lang(hy) .mlb{overflow-wrap:anywhere;}''')
sh.rep("  ovl.classList.add('open');document.body.style.overflow='hidden';\n  /* Фокус на саму коробку диалога, а не на первый её элемент: диктор прочтёт\n     заголовок прежде, чем человек окажется в полях. Дальше Tab ведёт внутрь. */\n  dlg.focus();\n}","  ovl.classList.add('open');document.body.style.overflow='hidden';\n  /* Фокус на саму коробку диалога, а не на первый её элемент: диктор прочтёт\n     заголовок прежде, чем человек окажется в полях. Дальше Tab ведёт внутрь.\n     preventScroll: на телефоне окно выше экрана, и фокус прокручивал накладку на 66 px —\n     заголовок открывался срезанным (аудит 2026-09-14). */\n  try{dlg.focus({preventScroll:true});}catch(e){dlg.focus();}\n  ovl.scrollTop=0;\n}")
sh.rep("  povl.classList.add('open');document.body.style.overflow='hidden';\n  document.getElementById('pmd').focus();","  povl.classList.add('open');document.body.style.overflow='hidden';\n  try{document.getElementById('pmd').focus({preventScroll:true});}catch(e){document.getElementById('pmd').focus();}\n  povl.scrollTop=0;")
sh.rep('.qa-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair);}','.qa-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair);\n  /* Положение заголовка при переключении держит скрипт; автопривязка прокрутки браузера\n     (scroll anchoring) здесь выключена, чтобы компенсация не удваивалась. */\n  overflow-anchor:none;}')
sh.rep('    var el=document.activeElement;\n    if(el&&/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName))return;','    var el=document.activeElement;\n    if(el&&/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName))return;\n    /* Пробел и стрелки на кнопке или ссылке — их действие (аудит 2026-09-14: пробел на\n       вопросе раздела 05 листал страницу на экран вместо открытия ответа). */\n    if(el&&/^(BUTTON|A|SUMMARY)$/.test(el.tagName))return;')
sh.rep('    var d=b0.getBoundingClientRect().top-y0;\n    if(Math.abs(d)>0.5)scrollByNow(d);\n    var top=b0.getBoundingClientRect().top;\n    if(top<HDR)scrollByNow(top-HDR);\n  }',"    var d=b0.getBoundingClientRect().top-y0;\n    if(Math.abs(d)>0.5)scrollByNow(d);\n    var r0=b0.getBoundingClientRect();\n    if(r0.top<HDR){scrollByNow(r0.top-HDR);r0=b0.getBoundingClientRect();}\n    /* Минимальная прокрутка ради видимости: если раскрывающийся ответ не помещается под\n       заголовком, страница доезжает ровно настолько, чтобы показать его, но заголовок не\n       уходит под шапку. Без этого при чтении вопросов сверху вниз список уезжал и ответ\n       оказывался за нижней кромкой экрана (владелец, 2026-09-14). */\n    var ab=document.getElementById(b0.getAttribute('aria-controls')),inner=ab&&ab.firstElementChild;\n    if(inner){\n      var need=r0.bottom+inner.scrollHeight+20-innerHeight,room=r0.top-HDR;\n      if(need>0&&room>0){var dy=Math.min(need,room);\n        if(typeof PS!=='undefined'&&PS.on&&typeof psTo==='function')psTo(window.pageYOffset+dy);\n        else window.scrollTo({top:window.pageYOffset+dy,behavior:rm?'auto':'smooth'});}\n    }\n  }")
# 2026-09-14 (2): аккордеон — независимые переключатели, без компенсации прокрутки
a0=sh.s.index("(function(){
  var list=document.getElementById('qalist');if(!list)return;")
e0=sh.s.index("  open(1,true);
})();",a0)+len("  open(1,true);
})();")
sh.s=sh.s[:a0]+"(function(){\n  var list=document.getElementById('qalist');if(!list)return;\n  var sec=list.closest('section'),btns=[].slice.call(list.querySelectorAll('.qa-q')),pics=[].slice.call(sec.querySelectorAll('.qa-pic img'));\n  /* Владелец (2026-09-14): «страница прыгает при раскрытии». Любой аккордеон «открыт один»\n     обязан что-то сдвинуть: либо заголовок уезжает вверх, когда закрывается ответ над ним,\n     либо страницу прокручивают вслед за заголовком — и тогда едет всё остальное. Оба варианта\n     читались скачком. Теперь каждый вопрос открывается и закрывается сам, ничего над нажатым\n     заголовком не меняется, прокрутка не трогается. Иллюстрация слева — последний открытый. */\n  function setOpen(i,on,first){\n    var b=btns[i],a=document.getElementById(b.getAttribute('aria-controls'));\n    b.setAttribute('aria-expanded',on?'true':'false');\n    if(on){a.hidden=false;if(first||rm)a.classList.add('open');else requestAnimationFrame(function(){a.classList.add('open');});\n      pics.forEach(function(p,k){p.classList.toggle('on',k===i);});}\n    else{a.classList.remove('open');\n      if(first||rm)a.hidden=true;else setTimeout(function(){if(b.getAttribute('aria-expanded')==='false')a.hidden=true;},240);}\n  }\n  btns.forEach(function(b,i){\n    b.addEventListener('click',function(){setOpen(i,b.getAttribute('aria-expanded')!=='true');});\n    b.addEventListener('keydown',function(e){\n      var j=e.key==='ArrowDown'?i+1:e.key==='ArrowUp'?i-1:e.key==='Home'?0:e.key==='End'?btns.length-1:-1;\n      if(j<0||j>=btns.length)return;e.preventDefault();btns[j].focus();\n    });\n  });\n  btns.forEach(function(b,i){setOpen(i,i===1,true);});\n})();"+sh.s[e0:];sh.n+=1
sh.rep("  function setOpen(i,on,first){\n    var b=btns[i],a=document.getElementById(b.getAttribute('aria-controls'));\n    b.setAttribute('aria-expanded',on?'true':'false');","  function setOpen(i,on,first){\n    var b=btns[i],a=document.getElementById(b.getAttribute('aria-controls'));\n    /* Владелец (2026-09-14, второе решение): открыт один — новый вопрос закрывает прежний.\n       Закрытие и раскрытие идут одним переходом 220 мс; прокрутку скрипт не трогает. */\n    if(on)btns.forEach(function(o,k){if(k!==i&&o.getAttribute('aria-expanded')==='true')setOpen(k,false,first);});\n    b.setAttribute('aria-expanded',on?'true':'false');")
sh.rep('.rail-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,38%);\n  align-items:start;gap:26px;}\n/* Вводный абзац стоит на строке заголовка, а не над ним: по-армянски он в семь строк, и\n   при выравнивании по низу счётчик 02 уезжал на высоту абзаца. */\n.rail-head .lede{margin-top:0;max-width:none;padding-top:clamp(28px,3.4vw,52px);}','.rail-head{display:block;}\n/* Владелец (2026-09-14): абзац справа от заголовка читался дырой под заголовком. Заголовок и\n   вводный абзац — одной колонкой, абзац до 62ch. */\n.rail-head .lede{margin-top:var(--s5);max-width:62ch;}')
sh.rep('@media (max-width:1024px){.igrid{grid-template-columns:repeat(2,minmax(0,1fr));}}\n@media(max-width:900px){.rail-head{grid-template-columns:1fr;gap:14px;}}','/* Высота кадра от высоты окна: на низком ноутбуке (≈670 px) шесть карточек с пропорцией 4:3\n   не помещались в экран (владелец, 2026-09-14). 25vh: 168 px на 670, 225 на 900, 270 на 1080. */\n@media (min-width:1025px){.ic-art{aspect-ratio:auto;height:clamp(168px,25vh,290px);}}\n@media (max-width:1024px){.igrid{grid-template-columns:repeat(2,minmax(0,1fr));}}')
sh.rep('.rail-head .lede{margin-top:var(--s5);max-width:62ch;}','.rail-head .lede{margin-top:var(--s5);max-width:68ch;}')
sh.rep('@media (min-width:1025px){.ic-art{aspect-ratio:auto;height:clamp(168px,25vh,290px);}}','@media (min-width:1025px){.ic-art{aspect-ratio:auto;height:clamp(150px,26vh,290px);}}')
sh.rep('@media (min-width:1025px){.ic-art{aspect-ratio:auto;height:clamp(150px,26vh,290px);}}','@media (min-width:1025px){.ic-art{aspect-ratio:auto;height:clamp(150px,26vh,290px);}}\n/* Низкое окно ноутбука (до 720 px): кадр ещё ниже и промежутки теснее — заголовок, абзац и все\n   шесть карточек встают в один экран под шапкой (замер 1343×671: 596 px при 599 доступных). */\n@media (min-width:1025px) and (max-height:720px){\n  .ic-art{height:clamp(136px,21vh,290px);}\n  .igrid{gap:14px;margin-top:20px;}\n  .rail-head .lede{margin-top:16px;}\n}')
sh.rep('@media (min-width:1025px){.ic-art{aspect-ratio:auto;height:clamp(150px,26vh,290px);}}','@media (min-width:1025px){.ic-art{aspect-ratio:auto;height:clamp(150px,24vh,290px);}}')
sh.rep('html[data-nav="5"] header{--hc:var(--fg);--hh:rgba(13,14,19,.16);--hw:rgba(239,237,234,.82);\n  isolation:isolate;}\nhtml[data-nav="5"] header[data-tone="ink"]{--hc:#EFEDEA;--hh:rgba(239,237,234,.24);\n  --hw:rgba(13,14,19,.66);}','html[data-nav="5"] header{--hc:var(--fg);--hh:rgba(13,14,19,.16);--hw:rgba(239,237,234,.94);\n  isolation:isolate;}\nhtml[data-nav="5"] header[data-tone="ink"]{--hc:#EFEDEA;--hh:rgba(239,237,234,.24);\n  --hw:rgba(13,14,19,.82);}')
sh.rep('html[data-nav="5"] #hdr::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;\n  background:var(--hh);transform:scaleX(0);transform-origin:left center;\n  transition:transform .62s var(--e);}\nhtml[data-nav="5"].hscr #hdr::after{transform:scaleX(1);}\nhtml[data-nav="5"] #hdr::before{content:"";position:absolute;inset:0;z-index:-1;\n  background:var(--hw);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);\n  transform:scaleX(0);transform-origin:left center;transition:transform .62s var(--e) .06s;}\nhtml[data-nav="5"].hscr #hdr::before{transform:scaleX(1);}','/* Владелец (2026-09-14): «при прокрутке героя на шапке мелькает текст». Лист рисовался слева\n   направо за 0,62 с и начинался после 60 px прокрутки — заголовок героя успевал зайти под шапку\n   раньше листа. Теперь лист проявляется целиком за 0,18 с, а порог — 4 px. */\nhtml[data-nav="5"] #hdr::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;\n  background:var(--hh);opacity:0;transition:opacity .25s var(--e);}\nhtml[data-nav="5"].hscr #hdr::after{opacity:1;}\nhtml[data-nav="5"] #hdr::before{content:"";position:absolute;inset:0;z-index:-1;\n  background:var(--hw);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);\n  opacity:0;transition:opacity .18s var(--e);}\nhtml[data-nav="5"].hscr #hdr::before{opacity:1;}')
sh.rep('html[data-nav="5"]:has(#ixp.on) #hdr::before{background:#0D0E13;\n  -webkit-backdrop-filter:none;backdrop-filter:none;transform:scaleX(1);}','html[data-nav="5"]:has(#ixp.on) #hdr::before{background:#0D0E13;\n  -webkit-backdrop-filter:none;backdrop-filter:none;opacity:1;}')
sh.rep('  return {on:window.pageYOffset>60,p:m>0?Math.min(1,window.pageYOffset/m):0};}','  return {on:window.pageYOffset>4,p:m>0?Math.min(1,window.pageYOffset/m):0};}')
sh.done()

# ============================================================== build.py
b = P('build.py')
# fonts: Mardoto 400/500/700 for the Armenian page; Arian AMU Serif out of the UI
b.rep("""MONO_HY = "'Arian AMU Serif',Georgia,serif\"""", """MONO_HY = "'Mardoto','Arian AMU','Helvetica Neue',sans-serif\"""")
b.rep("""FF_HY = '\\n'.join([
    font_face('Arian AMU', ARIAN_REG, 'arian-amu-400.woff2'),
    font_face('Arian AMU', '600 900', 'arian-amu-700.woff2'),
    font_face('Arian AMU Serif', '400 500', 'arian-amu-serif-400.woff2'),
    font_face('Arian AMU Serif', '600 900', 'arian-amu-serif-700.woff2'),""",
"""# Аудит 2026-09-14: армянская страница целиком на Mardoto — 400 для прозы, 500 для
# заголовков и подписей, 700 для полужирного. Настоящие файлы (подмножества из
# github.com/vahanhovh/mardoto), браузер жир не подделывает. Arian AMU остаётся запасным
# семейством в стеке; Arian AMU Serif из интерфейсных подписей убран.
FF_HY = '\\n'.join([
    font_face('Mardoto', '400', 'mardoto-400.woff2'),
    font_face('Mardoto', '700', 'mardoto-700.woff2'),
    font_face('Arian AMU', ARIAN_REG, 'arian-amu-400.woff2'),
    font_face('Arian AMU', '600 900', 'arian-amu-700.woff2'),""")
b.rep(""" 'BODYFONT': "'Arian AMU','Helvetica Neue',sans-serif",
 'HEADFONT': "'Mardoto','Arian AMU',sans-serif", 'HEADWT': '500',
 'MONOFONT': MONO_HY,
 'NAVFONT': "'Arian AMU Serif',Georgia,serif",""",
""" 'BODYFONT': "'Mardoto','Arian AMU','Helvetica Neue',sans-serif",
 'HEADFONT': "'Mardoto','Arian AMU',sans-serif", 'HEADWT': '500',
 'MONOFONT': MONO_HY,
 'NAVFONT': 'inherit',""")
b.rep("""FF_HY_D = '\\n'.join([
    font_face_url('Arian AMU', ARIAN_REG, 'arian-amu-400.woff2'),
    font_face_url('Arian AMU', '600 900', 'arian-amu-700.woff2'),
    font_face_url('Arian AMU Serif', '400 500', 'arian-amu-serif-400.woff2'),
    font_face_url('Arian AMU Serif', '600 900', 'arian-amu-serif-700.woff2'),""",
"""FF_HY_D = '\\n'.join([
    font_face_url('Mardoto', '400', 'mardoto-400.woff2'),
    font_face_url('Mardoto', '700', 'mardoto-700.woff2'),
    font_face_url('Arian AMU', ARIAN_REG, 'arian-amu-400.woff2'),
    font_face_url('Arian AMU', '600 900', 'arian-amu-700.woff2'),""")
b.rep("""DEPLOY_FONTS = (['overused-grotesk-latin.woff2', 'departure-mono.woff2',
                 'arian-amu-400.woff2', 'arian-amu-700.woff2',
                 'arian-amu-serif-400.woff2', 'arian-amu-serif-700.woff2']
                + ['mardoto-500.woff2'])""",
"""DEPLOY_FONTS = (['overused-grotesk-latin.woff2', 'departure-mono.woff2',
                 'arian-amu-400.woff2', 'arian-amu-700.woff2']
                + ['mardoto-400.woff2', 'mardoto-500.woff2', 'mardoto-700.woff2'])""")
b.rep("""        'hy': ['arian-amu-400.woff2', 'arian-amu-700.woff2', 'arian-amu-serif-400.woff2'],""",
      """        'hy': ['mardoto-400.woff2', 'mardoto-500.woff2'],""")

# palette pass: card class renamed, invitation card gone
b.rep(""".plate,.plate2,.other,.chart,.ic,.rep-head{--brand:%(dark)s;--brand-ink:%(dark)s;--brand-on:%(ink)s;""",
      """.plate,.plate2,.chart,.icard,.rep-head{--brand:%(dark)s;--brand-ink:%(dark)s;--brand-on:%(ink)s;""")
b.rep("""/* Приглашение больше не фирменный блок. Прежде оно заливалось цветом марки
   и получало чернильный текст — в ряду из шести тёмных плит со светлым
   названием седьмая выпадала светлой с тёмным. Теперь она той же семьи,
   а отличается тем, чем и должна: на ней чертёж, а не фотография. */
.ic.is-open-card{color:%(offwhite)s;box-shadow:0 0 0 1px rgba(%(inkrgb)s,.5);}
.ic.is-open-card .ic-art{background:%(ink)s;}
.ic.is-open-card .ic-art svg{color:rgba(%(darkrgb)s,.6);}
/* Сплошные чернила, а не .78: на фирменном фоне карточки .78 давало 4,06:1 в
   синей палитре и 3,54 в тёплой — ниже нормы для 14 пикселей. Приглушать
   абзац теперь приходится кеглем, а не выцветанием: подходящей прозрачности,
   которая проходит норму во всех трёх палитрах, попросту нет. */
.ic.is-open-card .ic-art::after{
  background:linear-gradient(180deg,rgba(%(inkrgb)s,.16) 0%%,rgba(%(inkrgb)s,.04) 46%%,
    rgba(%(inkrgb)s,.9) 86%%,%(ink)s 100%%);}
""", "")

# form texts: one contact, per-field errors (EN + HY)
b.rep(""" 'F_FORM_ERR': 'Please fill in all fields: name, company, a valid email, phone and a short description.',""",
      """ 'F_FORM_ERR': 'Please check the highlighted fields.',
 # Аудит 2026-09-14: обязательны имя, описание и один контакт (почта ИЛИ телефон).
 'F_ONE_CONTACT': 'Email or phone — at least one, so that we can reply.',""")
b.rep(""" 'F_FORM_ERR': 'Լրացրեք բոլոր դաշտերը՝ անուն, ընկերություն, վավեր էլ. փոստ, հեռախոս և կարճ նկարագրություն։',""",
      """ 'F_FORM_ERR': 'Ստուգեք նշված դաշտերը։',
 # ⚠ ЧЕРНОВИК: армянские формулировки ошибок — на проверку владельцу.
 'F_ONE_CONTACT': 'Էլ. փոստ կամ հեռախոս՝ գոնե մեկը, որպեսզի կարողանանք պատասխանել։',""")
b.rep(""" 'viewDetails': 'View details',""", """ 'viewDetails': 'View details',
 'errName': 'Please enter your name.', 'errMsg': 'Please describe what happened.',
 'errEmail': 'Please enter a valid email address.', 'errPhone': 'Please enter a valid phone number.',
 'errContact': 'Enter an email or a phone number.',""")
b.rep(""" 'viewDetails': 'Մանրամասներ',""", """ 'viewDetails': 'Մանրամասներ',
 'errName': 'Նշեք ձեր անունը։', 'errMsg': 'Նկարագրեք՝ ինչ է տեղի ունեցել։',
 'errEmail': 'Նշեք վավեր էլ. փոստի հասցե։', 'errPhone': 'Նշեք վավեր հեռախոսահամար։',
 'errContact': 'Նշեք էլ. փոստ կամ հեռախոսահամար։',""")
# NO_GLUE protects nothing new; F_ONE_CONTACT is prose and may glue.

# Armenian labels: sentence case instead of solid caps (case only, meaning unchanged).
# Matched by line prefix with a regex so the exact capital glyphs need not be retyped.
def rx(pat, new, count=1):
    c = len(re.findall(pat, b.s, flags=re.M))
    if c != count:
        raise SystemExit('build.py: expected %d, found %d for /%s/' % (count, c, pat))
    b.s = re.sub(pat, new, b.s, flags=re.M); b.n += 1
rx(r"^ 'HERO_EYEBROW': 'Է[^']*',", " 'HERO_EYEBROW': 'Էլեկտրաէներգիայի որակի մոնիթորինգ',")
rx(r"^ 'IM_FINDLB': 'Ի[^']*',", " 'IM_FINDLB': 'Ինչ հարցերի կարող է պատասխանել հաշվետվությունը',")
rx(r"^ 'F_CONTACT': 'Կ[^']*',", " 'F_CONTACT': 'Կոնտակտային տվյալներ',")
rx(r"^ 'CT_CAP': 'RMS Լ.*$", " 'CT_CAP': 'RMS լարում · 10-րոպեանոց միտում', 'CT_NOM': 'Անվանական', 'CT_DIP': 'Լարման անկում · 180 մվրկ',")
rx(r"^    \('01 · [^']*',", "    ('Ինչու սկսեցինք',")
rx(r"^    \('02 · [^']*',", "    ('Ինչպես ենք մտածում',")
rx(r"^    \('03 · [^']*',", "    ('Ինչ ենք կառուցում',")
rx(r"^  'statLabel': 'Տ[^']*',", "  'statLabel': 'Տեխնիկական նշում',", count=3)
rx(r"^  'stat': '57%', 'statLabel': 'Վ[^']*',", "  'stat': '57%', 'statLabel': 'Վիճակագրություն',")

b.done()
print('ok')
