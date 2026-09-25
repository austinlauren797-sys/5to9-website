# -*- coding: utf-8 -*-
"""Static generator for 5to9.me — ME (default) + EN, homepage + 4 landing pages.
Run: python3 build.py  → writes ./out/ (upload its contents to the repo root)."""
import json, os, shutil, html
from urllib.parse import quote
from content_common import *
from content_home import HOME
from content_lp import LP, LP_COMMON
import content_products as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
V = "9"  # cache-busting for css/js

MARK_PATH = open(os.path.join(HERE, "src", "mark_path.txt")).read().strip()
FAVICON = open(os.path.join(HERE, "src", "favicon.txt")).read().strip()

IDS = {  # section anchors per language on landing pages
    "me": {"why": "zasto", "range": "oprema", "who": "za-koga", "process": "proces", "faq": "pitanja", "ask": "upit"},
    "en": {"why": "why", "range": "range", "who": "who", "process": "process", "faq": "faq", "ask": "enquiry"},
}

def esc(s): return html.escape(s, quote=True)
def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", " ", s).replace("&amp;", "&").replace("  ", " ").strip()

def depth_of(path): return path.count("/")
def rel(frm, to):
    """relative link from page path `frm` to page path `to` ('' = root)."""
    r = "../" * depth_of(frm) + to
    return r if r else "./"

# ------------------------------------------------------------------ shared chunks
def head(lang, key, path, title, desc, og_img, jsonld):
    pre = "../" * depth_of(path)
    me, en = PATHS[key]["me"], PATHS[key]["en"]
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}{path}">
<link rel="alternate" hreflang="{HREFLANG['me']}" href="{SITE}{me}">
<link rel="alternate" hreflang="{HREFLANG['en']}" href="{SITE}{en}">
<link rel="alternate" hreflang="x-default" href="{SITE}{me}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="5TO9">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}assets/img/{og_img}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:locale:alternate" content="{OG_LOCALE['en' if lang=='me' else 'me']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A0A0A">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Archivo:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/site.css?v={V}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>"""

def body_open(lp=False):
    return f"""<body{' class="lp"' if lp else ''}>
<script>
(function(){{
  var d=document.documentElement;
  d.className += (window.IntersectionObserver && [].slice.call(document.querySelectorAll('body')).length) ? ' js' : ' no-js';
  /* if the script file never arrives, never leave content hidden */
  setTimeout(function(){{ if(!window.__5to9){{ [].slice.call(document.querySelectorAll('.reveal')).forEach(function(e){{e.classList.add('in');}}); }} }},3500);
}})();
</script>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="mark" viewBox="0 0 499 591">
    <path fill="currentColor" fill-rule="evenodd" d="{MARK_PATH}"/>
  </symbol>
</svg>

<div class="progress" id="progress"></div>
"""

def lang_switch(lang, key, path, cls="lang"):
    out = []
    for L, label in (("me", "ME"), ("en", "EN")):
        href = rel(path, PATHS[key][L])
        cur = ' aria-current="true"' if L == lang else ""
        out.append(f'<a href="{href}" hreflang="{HREFLANG[L]}" lang="{HTML_LANG[L]}"{cur}>{label}</a>')
    sep = "<span>/</span>" if cls == "lang" else ""
    return f'<div class="{cls}" aria-label="{COMMON[lang]["lang_label"]}">' + sep.join(out) + "</div>"

def nav(lang, key, path, links, cta_href, cta_text, lp):
    C = COMMON[lang]
    ACT = ' class="active" aria-current="page"'
    lis = "\n".join(f'    <li><a href="{h}"{ACT if act else ""}>{t}</a></li>' for h, t, act in links)
    return f"""
<nav class="nav{' nav--lp' if lp else ''}" id="nav">
  <a href="{rel(path, PATHS['home'][lang])}" aria-label="{C['home_aria']}"><svg class="mark" viewBox="0 0 499 591"><use href="#mark"/></svg></a>
  <ul class="nav-links">
    <span class="nav-ind" id="nav-ind" aria-hidden="true"></span>
{lis}
  </ul>
  <div class="nav-r">
    {lang_switch(lang, key, path)}
    <a class="cta" href="{cta_href}">{cta_text}</a>
    <button class="burger" id="burger" aria-label="{C['menu_open']}" data-open="{C['menu_open']}" data-close="{C['menu_close']}" aria-expanded="false" aria-controls="mobilemenu"><span></span><span></span></button>
  </div>
</nav>
"""

def mobilemenu(lang, key, path, items):
    C = COMMON[lang]
    a = "\n".join(f'  <a href="{h}"><i>{i+1:02d}</i>{t}</a>' for i, (h, t) in enumerate(items))
    return f"""
<div class="mobilemenu" id="mobilemenu">
{a}
  <div class="mm-foot">
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <span>{C['address']}</span>
  </div>
  {lang_switch(lang, key, path, "mm-lang")}
</div>
"""

def cards(items, lang, pre):
    C = COMMON[lang]
    out = []
    for it in items:
        title = it["title"][lang] if isinstance(it["title"], dict) else it["title"]
        rows = "\n".join(
            f'        <li><b>{s[0] if lang=="me" else s[2]}</b><span>{s[1] if lang=="me" else s[3]}</span></li>' for s in it["specs"])
        out.append(f"""    <div class="model" data-img="{pre}assets/img/{it['img']}" role="button" tabindex="0">
      <h4>{title}</h4><p class="kind">{it['kind'][lang]}</p>
      <ul>
{rows}
      </ul>
      <p class="more">{C['view']}</p>
    </div>""")
    return "\n".join(out)

def strip(items):
    return "".join(f"<span>{s}</span>" for s in items)

def tiles(lang, path, keys, cls="tiles"):
    pre = "../" * depth_of(path)
    C = COMMON[lang]
    out = []
    for k in keys:
        c = CATS[k]; t = c[lang]
        out.append(f"""    <a class="tile" href="{rel(path, PATHS[k][lang])}">
      <div class="ph"><img src="{pre}assets/img/{c['img']}" alt="{esc(t['alt'])}" loading="lazy" width="800" height="560"></div>
      <div class="tx"><h3>{t['title']}</h3><p>{t['text']}</p><span class="go">{C['go']}</span></div>
    </a>""")
    return f'<div class="{cls} reveal">\n' + "\n".join(out) + "\n  </div>"

def contacts(lang):
    C = COMMON[lang]
    return f"""<div class="contacts">
      <div><span>{C['email']}</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div><span>{C['phone']}</span><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
      <div><span>{C['office']}</span><p>{C['address_br']}</p></div>
    </div>"""

def footer(lang, key, path):
    C = COMMON[lang]
    links = "".join(f'<a href="{rel(path, PATHS[k][lang])}">{CATS[k][lang]["nav"]}</a>' for k in CAT_ORDER)
    other = "en" if lang == "me" else "me"
    return f"""
<footer class="band foot">
  <svg class="mark" viewBox="0 0 499 591" aria-hidden="true"><use href="#mark"/></svg>
  <span>{C['foot']}</span>
  <nav class="foot-links">{links}</nav>
  <span><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{rel(path, PATHS[key][other])}" hreflang="{HREFLANG[other]}">{'English' if other=='en' else 'Crnogorski'}</a></span>
</footer>
"""

def sheet(lang, ask_href):
    C = COMMON[lang]
    return f"""
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-title">
  <div class="sheet-inner">
    <button class="sheet-close" id="sheet-close" aria-label="{C['close']}">&times;</button>
    <div class="sheet-img"><img id="sheet-photo" src="data:," alt=""></div>
    <div class="sheet-body">
      <h3 id="sheet-title"></h3>
      <p class="kind" id="sheet-kind"></p>
      <ul id="sheet-specs"></ul>
      <a class="ask" href="{ask_href}" id="sheet-ask">{C['ask']}</a>
    </div>
  </div>
</div>
"""

def end(path):
    pre = "../" * depth_of(path)
    return f'\n<script src="{pre}assets/js/site.js?v={V}"></script>\n</body>\n</html>\n'

def org_ld(lang):
    return {
        "@type": "LocalBusiness", "@id": SITE + "#org", "name": "5TO9", "alternateName": "Five to Nine",
        "url": SITE, "email": EMAIL, "telephone": PHONE, "image": SITE + "assets/img/og-teq.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "Ibrahima Koristovića 11",
                    "addressLocality": "Podgorica", "addressCountry": "ME"},
        "areaServed": "ME",
    }

def ticker(items):
    s = "".join(f"<span>{t}</span>" for t in items)
    return f"""
<div class="band ticker">
  <div class="ticker-track" aria-hidden="true">
    {s}
    {s}
  </div>
</div>
"""

def write(path, content):
    fp = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)

# ------------------------------------------------------------------ HOME
def build_home(lang):
    H = HOME[lang]; C = COMMON[lang]; key = "home"
    path = PATHS[key][lang]; pre = "../" * depth_of(path)
    ld = {"@context": "https://schema.org", "@graph": [org_ld(lang),
          {"@type": "WebSite", "name": "5TO9", "url": SITE, "inLanguage": HREFLANG[lang]}]}
    out = [head(lang, key, path, H["title"], H["desc"], "og-teq.jpg", ld), body_open()]
    out.append(nav(lang, key, path, [(h, t, False) for h, t in H["nav"]], "#contact", C["cta_home"], False))
    mm = list(H["mm"])
    out.append(mobilemenu(lang, key, path, mm))
    out.append('<div class="rail" id="rail">\n' + "\n".join(
        f'  <a href="#{i}" data-t="{i}"><i></i>{t}</a>' for i, t in H["rail"]) + "\n</div>\n")

    def more(group):
        return '<div class="more-row">' + "".join(
            f'<a class="more-link" href="{rel(path, PATHS[k][lang])}">{t}</a>' for k, t in H["more"][group]) + "</div>"

    ps = lambda arr: "\n".join(f"      <p>{p}</p>" for p in arr)
    out.append(f"""
<header class="band dark grain hero" id="top">
  <svg class="hero-mark" viewBox="0 0 499 591" aria-hidden="true"><use href="#mark"/></svg>
  <div class="hero-inner">
    <svg class="logo rise d1" viewBox="0 0 499 591" role="img" aria-label="5TO9"><use href="#mark"/></svg>
    <h1 class="stack rise d2">FIVE<span class="to">TO</span>NINE</h1>
  </div>
  <p class="hero-line rise d3">{H['hero_line']}</p>
  <div class="hero-bottom rise d4">
    <a class="scroll-cue" href="#about" style="text-decoration:none"><b></b> {H['scroll']}</a>
    <span>{H['place']}</span>
  </div>
</header>
{ticker(H['ticker'])}
<section class="band light" id="about">
  <div class="who">
    <div class="reveal">
      <p class="eyebrow">{H['who_eyebrow']}</p>
      <h2 class="h-xl">{H['who_h']}</h2>
    </div>
    <div class="reveal">
      <p class="lede">{H['who_lede']}</p>
      <p class="eyebrow" style="margin-top:36px;margin-bottom:0">{H['pillars_eyebrow']}</p>
      <ul class="pillars">
{"".join(f'        <li><a href="#{a}"><span class="idx">P{i+1}</span>{t}<span class="arrow">→</span></a></li>' + chr(10) for i, (a, t) in enumerate(zip(["sports", "digital", "playgrounds", "fitness"], H['pillars'])))}
      </ul>
    </div>
  </div>
</section>

<section class="band dark grain" id="offer">
  <div class="range-head reveal">
    <div>
      <p class="eyebrow">{H['offer_eyebrow']}</p>
      <h2 class="h-lg">{H['offer_h']}</h2>
    </div>
    <p>{H['offer_p']}</p>
  </div>
  {tiles(lang, path, CAT_ORDER)}
</section>

<section class="band light-2" id="sports">
  <div class="solution">
    <div class="visual-frame reveal">
      <div class="visual"><img src="{pre}assets/img/teq-court.jpg" alt="{esc(H['sports_alt'])}" width="1500" height="1180"></div>
    </div>
    <div class="reveal">
      <span class="tag t-orange">{H['sports_tag']}</span>
      <h3 class="h-md">{H['sports_h']}</h3>
{ps(H['sports_p'])}
      {more('sports')}
    </div>
  </div>
</section>

<section class="band orange grain" id="digital">
  <div class="solution flip">
    <div class="visual-frame reveal" style="--accent:#000">
      <div class="visual"><img src="{pre}assets/img/panel-handover.jpg" alt="{esc(H['digital_alt'])}" loading="lazy" width="1400" height="1100"></div>
    </div>
    <div class="reveal">
      <span class="tag t-black">{H['digital_tag']}</span>
      <h3 class="h-md">{H['digital_h']}</h3>
{ps(H['digital_p'])}
      {more('digital')}
    </div>
  </div>
</section>

<section class="band dark grain" id="playgrounds">
  <div class="solution">
    <div class="visual-frame reveal">
      <div class="visual"><img src="{pre}assets/img/playground.jpg" alt="{esc(H['play_alt'])}" loading="lazy" width="1400" height="1100"></div>
    </div>
    <div class="reveal">
      <span class="tag t-white">{H['play_tag']}</span>
      <h3 class="h-md" style="color:var(--orange)">{H['play_h']}</h3>
{ps(H['play_p'])}
      {more('play')}
    </div>
  </div>
</section>

<section class="band light-2" id="fitness">
  <div class="solution flip">
    <div class="visual-frame reveal">
      <div class="visual"><img src="{pre}assets/img/home-fitness.jpg" alt="{esc(H['fit_alt'])}" loading="lazy" width="1400" height="1100"></div>
    </div>
    <div class="reveal">
      <span class="tag t-orange">{H['fit_tag']}</span>
      <h3 class="h-md">{H['fit_h']}</h3>
{ps(H['fit_p'])}
      {more('fitness')}
    </div>
  </div>
</section>

<section class="band light" id="process">
  <div class="reveal">
    <p class="eyebrow">{H['process_eyebrow']}</p>
    <h2 class="h-lg">{H['process_h']}</h2>
  </div>
  <div class="process">
    <ol class="steps reveal">
{"".join(f'      <li><h4>{h}</h4><p>{p}</p></li>' + chr(10) for h, p in H['steps'])}    </ol>
    <div class="process-note reveal">
      <div class="big">{H['process_big']}</div>
      <p style="margin-top:26px;max-width:34ch;opacity:.75">{H['process_note']}</p>
    </div>
  </div>
</section>

<section class="band dark grain" id="contact">
  <div class="reveal contact">
    <p class="eyebrow">{H['contact_eyebrow']}</p>
    <h2 class="h-lg">{H['contact_h']}</h2>
    {contacts(lang)}
  </div>
</section>
""")
    out.append(footer(lang, key, path))
    out.append(end(path))
    write(path, "".join(out))

# ------------------------------------------------------------------ LANDING
def build_lp(key, lang):
    D = LP[key]; T = D[lang]; C = COMMON[lang]; L = LP_COMMON[lang]; I = IDS[lang]
    path = PATHS[key][lang]; pre = "../" * depth_of(path)
    home = rel(path, PATHS["home"][lang])

    faq = []
    for q, a in T["faq"]:
        if q == "__procurement__": q, a = L["procurement_q"], L["procurement_a"]
        elif q == "__quote__": q = L["quote_q"]
        faq.append((q, a))

    ld = {"@context": "https://schema.org", "@graph": [
        org_ld(lang),
        {"@type": "WebPage", "name": T["title"], "url": SITE + path, "inLanguage": HREFLANG[lang],
         "description": T["desc"], "isPartOf": {"@id": SITE + "#org"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "5TO9", "item": SITE + PATHS["home"][lang]},
            {"@type": "ListItem", "position": 2, "name": CATS[key][lang]["title"], "item": SITE + path}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}

    out = [head(lang, key, path, T["title"], T["desc"], D["og"], ld), body_open(lp=True)]
    links = [(rel(path, PATHS[k][lang]), CATS[k][lang]["nav"], k == key) for k in CAT_ORDER]
    out.append(nav(lang, key, path, links, "#" + I["ask"], C["cta"], True))
    mm = [(rel(path, PATHS[k][lang]), CATS[k][lang]["nav"]) for k in CAT_ORDER]
    mm += [(home, C["home"]), ("#" + I["ask"], C["contact"])]
    out.append(mobilemenu(lang, key, path, mm))

    subject = ("Upit — " if lang == "me" else "Enquiry — ") + T["mail_cat"]
    mailto = f"mailto:{EMAIL}?subject={quote(subject)}&body={quote(L['mail_body'].format(cat=T['mail_cat']))}"
    hero_w = {"teq-court.jpg": (1500, 1180), "panel.webp": (900, 844), "playground.jpg": (1400, 1100),
              "fitness-hero.jpg": (1400, 1120)}[D["hero_img"]]
    facts = "".join(f"<li>{f}</li>" for f in T["facts"])
    bens = "\n".join(f"""    <div class="benefit"><span class="n">{i+1:02d}</span><h3>{h}</h3><p>{p}</p></div>"""
                     for i, (h, p) in enumerate(T["benefits"]))
    aud = "\n".join(f"""      <li><span class="idx">{i+1:02d}</span><h3>{h}</h3><p>{p}</p></li>"""
                    for i, (h, p) in enumerate(T["aud"]))
    steps = "\n".join(f"""    <li><span class="s">{i+1:02d}</span><h3>{h}</h3><p>{p}</p></li>"""
                      for i, (h, p) in enumerate(T["steps"]))
    faqs = "\n".join(f"""      <details><summary>{q}</summary><p>{a}</p></details>""" for q, a in faq)
    others = [k for k in CAT_ORDER if k != key]
    gallery_html = ""
    points_html = ""
    if T.get("gallery_points"):
        points_html = '  <div class="benefits gpoints reveal">\n' + "\n".join(
            f'    <div class="benefit"><span class="n">{i+1:02d}</span><h3>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(T["gallery_points"])) + "\n  </div>"
    if D.get("gallery"):
        def _fig(g):
            name, cls = (g if isinstance(g, tuple) else (g, ""))
            c = f' class="{cls}"' if cls else ""
            return f'''    <figure{c}><img src="{pre}assets/img/{name}" alt="{esc(T['gallery_alt'])}" loading="lazy" width="720" height="540"></figure>'''
        figs = "\n".join(_fig(g) for g in D["gallery"])
        gallery_html = f'''
<section class="band light" id="{D['gallery_id'][lang]}">
  <div class="range-head reveal">
    <div>
      <p class="eyebrow">{T['gallery_eyebrow']}</p>
      <h2 class="h-lg">{T['gallery_h']}</h2>
    </div>
    <p>{T['gallery_p']}</p>
  </div>
{points_html}
  <div class="gallery{' g4' if len(D['gallery'])==4 else ''} reveal">
{figs}
  </div>
</section>
'''
    import re as _re
    longest = max(len(w) for w in _re.sub(r"<[^>]+>", " ", T["h1"]).split())
    fit = round(96 / (longest * 0.66), 2)

    out.append(f"""
<header class="band dark grain" id="top">
  <div class="lp-hero">
    <div>
      <p class="eyebrow rise d1">{T['eyebrow']}</p>
      <h1 class="h-lp rise d2" style="--fit:{fit}">{T['h1']}</h1>
      <p class="lp-lead rise d3">{T['lead']}</p>
      <div class="btns rise d3">
        <a class="btn btn-o" href="#{I['ask']}">{C['cta']}</a>
        <a class="btn btn-g" href="#{I['range']}">{L['see_range']}</a>
      </div>
      <ul class="facts rise d4">{facts}</ul>
    </div>
    <div class="visual-frame rise d2">
      <div class="visual"><img src="{pre}assets/img/{D['hero_img']}" alt="{esc(T['hero_alt'])}" width="{hero_w[0]}" height="{hero_w[1]}" fetchpriority="high"></div>
    </div>
  </div>
</header>
{ticker(T['ticker'])}
<section class="band light" id="{I['why']}">
  <div class="reveal">
    <p class="eyebrow">{L['why_eyebrow']}</p>
    <h2 class="h-lg">{T['why_h']}</h2>
  </div>
  <div class="benefits reveal">
{bens}
  </div>
</section>

<section class="band dark grain" id="{I['range']}">
  <div class="range-head reveal">
    <div>
      <p class="eyebrow">{T['range_eyebrow']}</p>
      <h2 class="h-lg">{T['range_h']}</h2>
    </div>
    <p>{T['range_p']}</p>
  </div>
  <div class="{D['models_cls']} reveal">
{cards(getattr(P, D['products']), lang, pre)}
  </div>
  <p class="swipe-hint">{C['swipe']}</p>
  <div class="specstrip reveal">{strip(getattr(P, D['strip'])[lang])}</div>
</section>

{gallery_html}
<section class="band light-2" id="{I['who']}">
  <div class="aud-wrap">
    <div class="reveal">
      <p class="eyebrow">{L['aud_eyebrow']}</p>
      <h2 class="h-lg">{L['aud_h']}</h2>
    </div>
    <ul class="aud reveal">
{aud}
    </ul>
  </div>
</section>

<section class="band dark grain" id="{I['process']}">
  <div class="reveal">
    <p class="eyebrow">{L['proc_eyebrow']}</p>
    <h2 class="h-lg">{T['proc_h']}</h2>
  </div>
  <ol class="steps-row reveal">
{steps}
  </ol>
</section>

<section class="band light" id="{I['faq']}">
  <div class="faq-wrap">
    <div class="reveal">
      <p class="eyebrow">{L['faq_eyebrow']}</p>
      <h2 class="h-lg">{L['faq_h']}</h2>
    </div>
    <div class="faq reveal">
{faqs}
    </div>
  </div>
</section>

<section class="band orange grain ask-band" id="{I['ask']}">
  <div class="reveal">
    <p class="eyebrow">{L['ask_eyebrow']}</p>
    <div class="ask-grid">
      <h2 class="h-lg">{L['ask_h']}</h2>
      <div>
        <p>{T['ask_p']}</p>
        <div class="btns">
          <a class="btn btn-k" href="{esc(mailto)}">{L['ask_btn']} →</a>
          <a class="btn btn-kl" href="tel:{PHONE_TEL}">{L['call_btn']}</a>
        </div>
      </div>
    </div>
    {contacts(lang)}
  </div>
</section>

<section class="band dark grain">
  <div class="reveal">
    <p class="eyebrow">{L['more_eyebrow']}</p>
    <h2 class="h-lg">{L['more_h']}</h2>
  </div>
  {tiles(lang, path, others, "tiles t3")}
</section>
""")
    out.append(footer(lang, key, path))
    out.append(sheet(lang, "#" + I["ask"]))
    out.append(end(path))
    write(path, "".join(out))

# ------------------------------------------------------------------ 404
def build_404():
    t = """<!DOCTYPE html>
<html lang="sr-Latn-ME"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 — 5TO9</title><meta name="robots" content="noindex"><link rel="icon" href="%s">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&family=Archivo:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v=%s"></head>
<body class="lp"><header class="band dark grain" style="min-height:100svh">
<p class="eyebrow">404</p><h1 class="h-lp">STRANICA<br><em>NE POSTOJI.</em></h1>
<p class="lp-lead">Page not found.</p>
<div class="btns"><a class="btn btn-o" href="/">5TO9 — Početna</a><a class="btn btn-g" href="/en/">English</a></div>
</header></body></html>
""" % (FAVICON, V)
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(t)

def build_sitemap():
    rows = []
    for key in ["home"] + CAT_ORDER:
        for lang in ("me", "en"):
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{HREFLANG[L]}" href="{SITE}{PATHS[key][L]}"/>' for L in ("me", "en"))
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{PATHS[key]["me"]}"/>'
            rows.append(f"  <url>\n    <loc>{SITE}{PATHS[key][lang]}</loc>{alts}\n  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(xml)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets", "css")); os.makedirs(os.path.join(OUT, "assets", "js"))
    img_src = os.path.join(HERE, "src", "img")
    if not os.path.isdir(img_src):  # inside the repo the images live in ../assets/img
        img_src = os.path.join(HERE, "..", "assets", "img")
    shutil.copytree(img_src, os.path.join(OUT, "assets", "img"))
    css = open(os.path.join(HERE, "src", "base.css")).read() + open(os.path.join(HERE, "src", "extra.css")).read()
    open(os.path.join(OUT, "assets", "css", "site.css"), "w").write(css)
    shutil.copy(os.path.join(HERE, "src", "site.js"), os.path.join(OUT, "assets", "js", "site.js"))
    for lang in ("me", "en"):
        build_home(lang)
        for key in CAT_ORDER: build_lp(key, lang)
    build_404(); build_sitemap()
    open(os.path.join(OUT, "CNAME"), "w").write("5to9.me")
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\nSitemap: https://5to9.me/sitemap.xml\n")
    print("built →", OUT)

if __name__ == "__main__":
    main()
