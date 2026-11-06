from common import *
from brief import finder

def home_enquiry():
 groups=['Business consultancy','Healthcare revenue','SEO & digital marketing']
 controls=''.join(f'<button type="button" aria-pressed="{str(i==0).lower()}" data-interest="{h(v)}">{label}</button>' for i,(v,label) in enumerate(zip(groups,['Business','Healthcare','Marketing'])))
 return f'''<section class="home-enquiry container" id="consultation"><div><h2 class="display">Start a<br><em>conversation.</em></h2><p>Tell us what you’d like to discuss on a free first call.</p><a href="mailto:{EMAIL}" class="quiet-email">{EMAIL}</a></div><form id="enquiry" class="enquiry-form" action="mailto:{EMAIL}" method="post" enctype="text/plain"><fieldset class="interest"><legend>What can we help with?</legend><div>{controls}</div></fieldset><select id="service" name="service" aria-label="Selected practice" hidden>{''.join(f'<option>{v}</option>' for v in groups)}</select><div class="field-pair"><div class="field"><label for="ename">Your name</label><input id="ename" name="name" required maxlength="100" autocomplete="name"></div><div class="field"><label for="em">Email address</label><input id="em" name="email" type="email" required maxlength="254" autocomplete="email"></div></div><div class="field"><label for="message">Your message</label><textarea id="message" name="message" rows="4" required maxlength="1800" placeholder="What would you like help with?"></textarea></div><p class="form-hint">Omit patient information.</p><button class="pill" type="submit">Prepare email {icon('ne')}</button><p class="form-hint">Opens your email app.</p><div class="form-status" role="status" hidden></div></form></section>'''

def homepage():
 opening_script=(ROOT/'src/opening.js').read_text()
 opening=f'''<dialog id="opening" aria-label="Cloud Haven opening animation"><div class="opening-head">{brand()}<button type="button" class="skip-opening">Skip intro {icon('arr')}</button></div><div class="opening-console"><div class="opening-label">Independent consultancy</div><div class="nameplate" aria-label="Cloud Haven"><span aria-hidden="true">CLOUD HAVEN</span></div><button class="ignition" type="button" aria-label="Turn the dial to enter"><span class="dial-states" aria-hidden="true"><i>Off</i><i>On</i></span><span class="dial-face" aria-hidden="true"><span class="dial-knob"><i></i></span></span><span class="dial-caption">Turn to enter</span></button></div></dialog><script>{opening_script}</script>'''
 hero=f'''
 <section class="film-hero" aria-labelledby="intro-title"><div class="film-set" aria-hidden="true"><div class="studio-wall"></div><div class="studio-light"></div><div class="studio-floor"></div></div>
 <div class="film-stage container"><div class="film-copy">
 <h1 id="intro-title" tabindex="-1"><span><strong>A clearer</strong></span> <span><em>perspective.</em></span></h1>
 <p>Strategy and marketing for Pakistani businesses. Medical billing for US practices.</p>
 <div class="intro-actions">{btn('Find a service','#service-finder','pill','arr')}{btn('Book a consultation','#consultation','text-link','ne')}</div></div>
 <div class="instrument" id="instrument" role="group" aria-label="Interactive three-dimensional globe"><div class="model-shadow"></div><img id="globe-poster" src="/assets/meridian-poster.webp" alt="Green and silver atlas globe on a machined metal stand" width="680" height="760" fetchpriority="high"><div id="globe-surface" role="img" aria-label="Green and silver globe."></div></div>
 <div class="film-edge"><a href="#practices" class="film-scroll">{icon('down')} Our practices</a></div></div></section>'''
 deck_controls=[]
 chapters=[]
 for k,v in PRACTICES.items():
  title={'digital':'Digital marketing','healthcare':'Healthcare revenue','business':'Business consultancy'}[k]
  deck_controls.append(f'<button type="button" data-chapter="{k}" aria-controls="chapter-{k}" aria-pressed="false">{title} {icon("arr")}</button>')
  chapters.append(f'''<article class="practice-entry" id="chapter-{k}" data-practice="{k}"><a class="chapter-photo" href="/services/#{k}" aria-label="View {h(title.lower())} services">{photo_image(k)}</a><div class="chapter-copy"><h3><a href="/services/#{k}">{title}</a></h3><p>{h(v['intro'])}</p>{btn('View services','/services/#'+k,'text-link','arr')}</div></article>''')
 practices=f'''<section class="studio-practices container" id="practices"><div class="practice-intro"><h2 class="display">Where we <em>help.</em></h2><div class="practice-picker" aria-label="Select a practice" hidden>{''.join(deck_controls)}</div></div><div class="practice-chapters">{''.join(chapters)}<div class="deck-controls" hidden><span role="status" data-deck-status></span><div><button type="button" data-deck-move="-1" aria-label="Previous practice">{icon('back')}</button><button type="button" data-deck-move="1" aria-label="Next practice">{icon('arr')}</button></div></div></div></section>'''
 firm=f'''<section class="method-panel" aria-labelledby="firm-title"><div class="container method-grid"><div><h2 class="display" id="firm-title">A partner in<br><em>the work.</em></h2>{btn('About Cloud Haven','/about/','text-link')}</div>{method_tabs()}</div></section>'''
 guides=[
 ('Digital marketing','What goes into an SEO quote?','/blog/seo-cost-pakistan/'),
 ('Healthcare revenue','How does medical billing work?','/blog/what-is-medical-billing/'),
 ('Business consultancy','When should you bring in a consultant?','/blog/what-does-a-business-consultant-do/')]
 note_photos=['seo-audit-services','medical-billing-services-pakistan','business-consultancy-pakistan']
 stories=''.join(f'<article class="insight-card"><a href="{url}"><span class="insight-photo">{photo_image(key,sizes="(max-width: 700px) 100vw, 32vw")}</span><span class="art-kicker">{h(practice)}</span><h3>{h(title)}</h3></a></article>' for (practice,title,url),key in zip(guides,note_photos))
 notes=f'''<section class="journal container"><div class="section-heading"><h2 class="display">From the <em>journal.</em></h2>{btn('All insights','/blog/','text-link')}</div><div class="insight-grid">{stories}</div></section>'''
 doc('/','Cloud Haven Consultants | Digital Marketing, Healthcare Revenue & Business Strategy','Independent consulting from Multan for businesses in Pakistan and US medical practices. Explore SEO, digital marketing, healthcare revenue and business strategy.',hero+practices+firm+finder(on_home=True)+notes+home_enquiry(),home=True,opening=opening)
