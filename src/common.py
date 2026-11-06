from html import escape
from pathlib import Path
import json
import os
from urllib.parse import quote
from catalog import PRACTICES, SERVICES
ROOT=Path(__file__).resolve().parent.parent
DIST=ROOT/'dist'
PHOTOGRAPHY=json.loads((ROOT/'src/photography.json').read_text())
production_domain = os.environ.get('VERCEL_PROJECT_PRODUCTION_URL')
HOST = (os.environ.get('SITE_URL') or
        ('https://' + production_domain if production_domain else
         'https://cloud-haven-consulting-studio.shahzadwebdevelopers.chatgpt.site')).rstrip('/')
EMAIL='info@cloudhavenconsultants.com'
PHONE='+92 342 1958957'
def h(x):return escape(str(x),quote=True)
def icon(name,cls=''):
    paths={
       'ne':'<path d="M5 19 19 5M5 5h14v14"/>',
       'arr':'<path d="M3 12h17m-7-7 7 7-7 7"/>',
       'back':'<path d="M21 12H4m7-7-7 7 7 7"/>',
       'down':'<path d="M12 3v17m-7-7 7 7 7-7"/>',
       'menu':'<path d="M2 8h20M2 15h13"/>',
       'mail':'<rect x="2.5" y="4.5" width="19" height="15" rx="1"/><path d="m3 6 9 7 9-7"/>',
       'close':'<path d="m4 4 16 16M20 4 4 20"/>',
       'plus':'<path d="M5 12h14M12 5v14"/>',
       'search':'<circle cx="10" cy="10" r="6.2"/><path d="m15 15 5 5"/>',
    }
    return f'<svg viewBox="0 0 24 24" class="icon {cls}" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>'
MARK='<span class="mark" aria-hidden="true"></span>' 
def brand():return f'<a class="brand" href="/" aria-label="Cloud Haven Consultants home">{MARK}<span class="brand-words"><b>Cloud Haven</b><small>CONSULTANTS</small></span></a>'
def btn(label,path,kind='pill',ico='ne'):return f'<a class="{h(kind)}" href="{h(path)}">{h(label)} {icon(ico)}</a>'
def eyebrow(label):return f'<div class="eyebrow"><i></i>{h(label)}</div>'
def photo_image(key, *, eager=False, sizes='(max-width: 700px) 100vw, 48vw'):
    item=PHOTOGRAPHY[key]
    full='/assets/'+item['asset']+'.webp?v=editorial-4'
    responsive=''
    if 'small' in item:
        small='/assets/'+item['small']+'.webp?v=editorial-4'
        responsive=f' srcset="{h(small)} 720w, {h(full)} {item["width"]}w" sizes="{h(sizes)}"'
    loading='fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{h(full)}"{responsive} width="{item["width"]}" height="{item["height"]}" alt="{h(item["alt"])}" style="--focus:{h(item["focus"])}" decoding="async" {loading}>'
def header():
 primary=[('Our services','/services/'),('The firm','/about/'),('Contact','/contact/')]
 secondary=[('Insights','/blog/'),('Case studies','/case-studies/'),('Pricing','/pricing/'),('Build a brief','/project-brief/'),('Careers','/careers/')]
 primary_links=''.join(f'<a href="{u}"><span>{t}</span> {icon("ne")}</a>' for t,u in primary)
 secondary_links=''.join(f'<a href="{u}">{t}</a>' for t,u in secondary)
 return f'''<header class="header"><div class="header-inner">{brand()}<nav class="desktop-nav" aria-label="Primary"><a href="/services/">Our services</a><a href="/about/">The firm</a><a href="/blog/">Insights</a><a href="/project-brief/">Your brief <span data-brief-count class="nav-brief">0</span></a></nav><div class="nav-actions"><a aria-label="Contact Cloud Haven" class="nav-talk" href="/contact/"><span>Let’s talk</span> {icon('ne')}{icon('mail','mobile-mail')}</a><button class="menu-trigger" type="button" aria-label="Open menu" aria-controls="site-menu" aria-expanded="false">{icon('menu')}</button></div></div></header>
 <dialog id="site-menu" aria-label="Main navigation"><div class="menu-head">{brand()}<button aria-label="Close menu" class="menu-close">{icon('close')}</button></div><div class="menu-layout"><a class="menu-art menu-portrait" href="/about/#leadership">{photo_image('editorial-menu',sizes='(max-width: 700px) 100vw, 44vw')}<span class="portrait-credit"><span><strong>Umar M.</strong><small>Founder &amp; CEO</small></span><span class="portrait-arrow">{icon('ne')}</span></span></a><div><nav aria-label="Main" class="menu-links">{primary_links}</nav><nav class="menu-secondary" aria-label="More pages">{secondary_links}</nav></div></div><div class="menu-foot"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="/?intro=1">Replay opening</a><a href="/privacy-policy/">Privacy</a></div></dialog>'''
def footer():
 return f'''<footer><div class="footer-top"><div>{brand()}<p>Independent consulting from Multan, Pakistan.</p></div><div class="footer-col"><h2>The firm</h2><a href="/about/">About us</a><a href="/services/">Our services</a><a href="/pricing/">Pricing</a><a href="/project-brief/">Build a project brief</a><a href="/case-studies/">Case studies</a></div><div class="footer-col"><h2>Explore</h2><a href="/blog/">Insights</a><a href="/careers/">Careers</a><a href="/contact/">Contact</a></div><div class="footer-col"><h2>Get in touch</h2><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:+923421958957">{PHONE}</a></div></div><div class="footer-foot"><span>© 2026 Cloud Haven Consultants</span><div><a href="/photography/">Photography</a><a href="/privacy-policy/">Privacy</a><a href="/terms/">Terms</a><a href="#top">Back to top ↑</a></div></div></footer>'''
def end_cta():
 return f'''<section class="closing container"><div><h2 class="display">Let’s talk <em>business.</em></h2>{btn('Book a consultation','/contact/')}</div></section>'''
def doc(path,title,desc,body,home=False,lang='en',canonical=None,noindex=False,opening=''):
 import json
 uri=HOST+(canonical or path)
 meta=f'<meta name="robots" content="noindex,follow">' if noindex else ''
 org={'@context':'https://schema.org','@type':'Organization','name':'Cloud Haven Consultants','url':HOST+'/', 'email':EMAIL,'telephone':'+923421958957'}
 extra=f'<script type="application/ld+json">{json.dumps(org)}</script>' if home else ''
 headtitle=title if home else title+' | Cloud Haven Consultants'
 html=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{h(headtitle)}</title><meta name="description" content="{h(desc)}"><meta name="theme-color" content="{'#101914' if home else '#f6f6ef'}"><link rel="canonical" href="{h(uri)}">{meta}<meta property="og:title" content="{h(headtitle)}"><meta property="og:description" content="{h(desc)}"><meta property="og:image" content="{HOST}/assets/photo/practices/business.webp"><link rel="icon" href="/assets/favicon.png?v=editorial-4" type="image/png"><link rel="preload" href="/assets/montreal-regular.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" as="font" type="font/woff2" href="/assets/syne-bold.woff2" crossorigin><link rel="stylesheet" href="/assets/style.css?v=readable-7"><link rel="stylesheet" href="/assets/studio.css?v=readable-7">{extra}<script src="/assets/app.js?v=readable-7" defer></script><script src="/assets/brief.js?v=editorial-4" defer></script>{'<script type="module" src="/assets/globe.js?v=dial-6"></script><script defer src="/assets/studio.js?v=atlas-5"></script>' if home else ''}</head><body id="top" class="{'studio-home' if home else 'studio-page'}">{opening}<a class="skip" href="#main">Skip to content</a>{header()}<main id="main">{body}</main>{footer()}</body></html>'''
 target=DIST/path.strip('/')/'index.html'
 target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)
def subhero(kicker,title,intro,photo='',links='',parent=None,photo_alt=''):
 crumbs='<a href="/">Home</a> <span>/</span> '+(f'<a href="{h(parent[1])}">{h(parent[0])}</a> <span>/</span> ' if parent else '')+h(kicker)
 if photo in PRACTICES:
  photo_alt=photo_alt or PHOTOGRAPHY[photo]['alt']
  photo=PHOTOGRAPHY[photo]['asset']
 photo_key=next((key for key,item in PHOTOGRAPHY.items() if item['asset']==photo),'')
 photo_markup=f'<div class="sub-photo">{photo_image(photo_key,eager=True)}</div>' if photo_key else ''
 return f'''<section class="subhero container {'with-image' if photo else ''}"><nav class="crumb" aria-label="Breadcrumb">{crumbs}</nav><div class="sub-layout"><div><h1>{h(title)}</h1><p>{h(intro)}</p>{('<div class="sub-actions">'+links+'</div>') if links else ''}</div>{photo_markup}</div></section>'''
def details(items):
 return '<div class="accordions">'+''.join(f'<details><summary>{h(q)}{icon("plus")}</summary><div><p>{h(a)}</p></div></details>' for q,a in items if q and a)+'</div>'
def sect(title,content):
 return f'<section class="content-sec container"><h2 class="sec-heading">{h(title)}</h2><div class="sec-body">{content}</div></section>'
