# Собирает страницу просмотра: 11 слайдов + шрифты сайта, всё внутри файла.
import base64, io, os

FONTS = r'D:\Gridec\Site\source\powertech-v2-build\fonts'
HI = 'hi'
OUT = 'view.html'

SLIDES = [
    ('Cover', 'We make power problems visible'),
    ('Who we are', 'The people behind Gridec'),
    ('What we do', 'Measure, understand, act'),
    ('Typical problems', 'Six issues we investigate'),
    ('How we work', 'Five steps, site review to findings'),
    ('Market context', 'What is changing in Armenia'),
    ('Where we start', 'Target segments'),
    ('What we bring', 'Local engineering, reports in three languages'),
    ('Proposed cooperation', 'Four steps'),
    ('Next step', 'Contacts'),
]


def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()


mono = b64(os.path.join(FONTS, 'departure-mono.woff2'))
grot = b64(os.path.join(FONTS, 'overused-grotesk-latin.woff2'))

figs = []
for i, (name, sub) in enumerate(SLIDES, 1):
    img = b64(os.path.join(HI, 'Slide%d.PNG' % i))
    figs.append(
        '<figure class="s" id="s%d">\n'
        '  <figcaption>\n'
        '    <span class="no">%02d</span>\n'
        '    <span class="nm">%s</span>\n'
        '    <span class="sub">%s</span>\n'
        '  </figcaption>\n'
        '  <img src="data:image/png;base64,%s" alt="Slide %d — %s" '
        'width="1920" height="1080" loading="lazy">\n'
        '</figure>' % (i, i, name, sub, img, i, name))

toc = '\n'.join(
    '      <li><a href="#s%d"><span class="no">%02d</span>%s</a></li>'
    % (i, i, n) for i, (n, _) in enumerate(SLIDES, 1))

html = '''<title>Gridec for Janitza</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
@font-face{font-family:'Departure Mono';font-weight:100 900;font-display:swap;
  src:url(data:font/woff2;base64,%s) format('woff2');}
@font-face{font-family:'Overused Grotesk';font-weight:300 900;font-display:swap;
  src:url(data:font/woff2;base64,%s) format('woff2');}

/* Full light palette — the same one used in the deck and on the site. */
:root{
  --paper:#F6F1E9; --raised:#FDFAF4; --ink:#2B2722; --muted:#58534E;
  --hair:#DCD3C4; --acc:#20436E; --shadow:rgba(43,39,34,.13);
  --mono:'Departure Mono',ui-monospace,monospace;
  --body:'Overused Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif;
}
/* Dark theme swaps the token values only, nothing else. */
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#0A1A2E; --raised:#0D2440; --ink:#F6F1E9; --muted:#A9B6C8;
    --hair:#22406C; --acc:#7BA4D0; --shadow:rgba(0,0,0,.45);
  }
}
:root[data-theme="dark"]{
  --paper:#0A1A2E; --raised:#0D2440; --ink:#F6F1E9; --muted:#A9B6C8;
  --hair:#22406C; --acc:#7BA4D0; --shadow:rgba(0,0,0,.45);
}

*{box-sizing:border-box;}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
  -webkit-font-smoothing:antialiased;line-height:1.6;}
.wrap{max-width:1120px;margin:0 auto;padding:clamp(28px,5vw,72px) clamp(18px,4vw,44px) 96px;}

header{display:flex;flex-direction:column;gap:18px;
  padding-bottom:26px;border-bottom:1px solid var(--hair);}
.wm{font-family:var(--mono);font-size:22px;letter-spacing:3px;line-height:1;
  color:var(--ink);}
h1{margin:0;font-size:clamp(21px,2.6vw,28px);font-weight:600;line-height:1.25;
  text-wrap:balance;max-width:24ch;}
.meta{display:flex;flex-wrap:wrap;gap:8px 26px;font-family:var(--mono);
  font-size:11px;letter-spacing:1.6px;text-transform:uppercase;color:var(--muted);}
.meta a{color:var(--acc);text-decoration:none;border-bottom:1px solid var(--hair);}
.meta a:hover{border-bottom-color:var(--acc);}

nav{margin:34px 0 8px;}
nav h2{margin:0 0 14px;font-family:var(--mono);font-size:11px;letter-spacing:1.8px;
  text-transform:uppercase;color:var(--muted);font-weight:400;}
nav ol{list-style:none;margin:0;padding:0;display:grid;gap:0 30px;
  grid-template-columns:repeat(auto-fill,minmax(230px,1fr));}
nav li{border-top:1px solid var(--hair);}
nav a{display:flex;gap:12px;align-items:baseline;padding:9px 0;
  color:var(--ink);text-decoration:none;font-size:14px;}
nav a:hover{color:var(--acc);}
nav .no,figcaption .no{font-family:var(--mono);font-size:11px;letter-spacing:1.2px;
  color:var(--acc);font-variant-numeric:tabular-nums;}

.s{margin:54px 0 0;}
figcaption{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;
  padding-bottom:11px;margin-bottom:14px;border-bottom:1px solid var(--hair);}
figcaption .nm{font-size:15px;font-weight:600;}
figcaption .sub{font-size:13px;color:var(--muted);}
.s img{display:block;width:100%%;height:auto;background:var(--raised);
  box-shadow:0 1px 0 var(--hair),0 18px 34px -28px var(--shadow);}

footer{margin-top:64px;padding-top:22px;border-top:1px solid var(--hair);
  font-size:13px;color:var(--muted);max-width:62ch;}

a:focus-visible,nav a:focus-visible{outline:2px solid var(--acc);outline-offset:3px;}
@media (max-width:600px){.s{margin-top:38px;}}
</style>

<div class="wrap">
  <header>
    <div class="wm">GRIDEC</div>
    <h1>Company presentation for Janitza</h1>
    <div class="meta">
      <span>10 slides</span>
      <span>Gridec LLC</span>
      <span>Yerevan, Armenia</span>
      <a href="https://gridec.am">gridec.am</a>
    </div>
  </header>

  <nav>
    <h2>Slides</h2>
    <ol>
%s
    </ol>
  </nav>

%s

  <footer>
    The deck as it appears in PowerPoint. Slide 02 still carries a placeholder for
    the Director's surname. Nothing in the deck describes an existing partnership
    with Janitza electronics GmbH.
  </footer>
</div>
''' % (mono, grot, toc, '\n\n'.join(figs))

io.open(OUT, 'w', encoding='utf-8').write(html)
print(OUT, round(os.path.getsize(OUT) / 1024 / 1024, 2), 'MB')
