from common import *
from brief import finder
def home_enquiry():
 groups=['Business consultancy','Healthcare revenue','SEO & digital marketing']
 controls=''.join(f'<button type="button" aria-pressed="{str(i==0).lower()}" data-interest="{h(v)}">{label}</button>' for i,(v,label) in enumerate(zip(groups,['Business','Healthcare','Marketing'])))
 return f'''<section class="home-enquiry container" id="consultation"><div>{eyebrow('Get in touch')}<h2 class="display">Start a<br><em>conversation.</em></h2><p>Tell us what you’re working on. We’ll use a free first call to understand the business and agree a next step.</p><a href="mailto:{EMAIL}" class="quiet-email">{EMAIL}</a></div><form id="enquiry" class="enquiry-form" action="mailto:{EMAIL}" method="post" enctype="text/plain"><fieldset class="interest"><legend>What can we help with?</legend><div>{controls}</div></fieldset><select id="service" name="service" aria-label="Selected practice" hidden>{''.join(f'<option>{v}</option>' for v in groups)}</select><div class="field-pair"><div class="field"><label for="ename">Your name</label><input id="ename" name="name" required maxlength="100" autocomplete="name"></div><div class="field"><label for="em">Email address</label><input id="em" name="email" type="email" required maxlength="254" autocomplete="email"></div></div><div class="field"><label for="message">Your message</label><textarea id="message" name="message" rows="4" required maxlength="1800" placeholder="What would you like help with?"></textarea></div><p class="form-hint">Please leave patient details out of your enquiry.</p><button class="pill" type="submit">Prepare email {icon('ne')}</button><p class="form-hint">Review and send the draft in your email app.</p><div class="form-status" role="status" hidden></div></form></section>'''

def homepage():
 opening_script=(ROOT/'src/opening.js').read_text()
 opening=f'''<dialog id="opening" aria-labelledby="opening-name">
 <div class="opening-atlas" aria-hidden="true"></div>
 <div class="opening-head"><span class="opening-monogram" aria-hidden="true">{MARK}</span><button class="skip-opening" type="button">Skip intro {icon('arr')}</button></div>
 <div class="opening-console"><div id="opening-name" class="opening-name"><strong>Cloud Haven</strong><span>Consultants</span></div></div>
 <div class="opening-foot"><button type="button" class="ignition" aria-label="Enter website"><span class="dial-face" aria-hidden="true"><span class="dial-knob"><i></i></span></span><span>Enter website {icon('arr')}</span></button></div>
 <div class="opening-progress" aria-hidden="true"></div></dialog><script>{opening_script}</script>'''
 hero=f'''
 <section class="film-hero" aria-labelledby="intro-title"><div class="film-set" aria-hidden="true"><div class="studio-wall"></div><div class="studio-light"></div><div class="studio-floor"></div></div>
 <div class="film-stage container"><div class="film-copy">{eyebrow('Independent consultancy')}
 <h1 id="intro-title" tabindex="-1"><span><strong>A clearer</strong></span> <span><em>perspective.</em></span></h1>
 <p>Business strategy and digital marketing for teams in Pakistan. Billing and revenue cycle support for medical practices in the United States.</p>
 <div class="intro-actions">{btn('Find your service','#service-finder','pill','arr')}{btn('Book a consultation','#consultation','text-link','ne')}</div></div>
 <div class="instrument" id="instrument" role="group" aria-label="Interactive three-dimensional globe"><div class="model-shadow"></div><img id="globe-poster" src="/assets/meridian-poster.webp" alt="Green and silver atlas globe on a machined metal stand" width="680" height="760" fetchpriority="high"><div id="globe-surface" role="img" aria-label="Globe. Drag horizontally to rotate, or use the rotation buttons."></div></div>
 <div class="film-edge"><a href="#practices" class="film-scroll">{icon('down')} Our practices</a><div class="object-controls" hidden><span class="drag-label">Rotate globe</span><button type="button" data-turn="-1" aria-label="Rotate globe left">{icon('back')}</button><button type="button" data-turn="1" aria-label="Rotate globe right">{icon('arr')}</button><button type="button" class="motion-toggle" aria-label="Pause globe rotation" aria-pressed="false"><svg aria-hidden="true" viewBox="0 0 14 14"><path class="pause-shape" d="M4 2v10M10 2v10"/><path class="play-shape" d="m4 2 7 5-7 5z"/></svg></button></div></div></div></section>'''
 deck_controls=[]
 chapters=[]
 for k,v in PRACTICES.items():
  title={'digital':'Digital marketing','healthcare':'Healthcare revenue','business':'Business consultancy'}[k]
  deck_controls.append(f'<button type="button" data-chapter="{k}" aria-controls="chapter-{k}" aria-pressed="false">{title} {icon("arr")}</button>')
  chapters.append(f'''<article class="practice-entry" id="chapter-{k}" data-practice="{k}"><a class="chapter-photo" href="/services/#{k}" aria-label="View {h(title.lower())} services">{photo_image(k)}</a><div class="chapter-copy">{eyebrow(v['audience'])}<h3><a href="/services/#{k}">{title}</a></h3><p>{h(v['intro'])}</p>{btn('Explore '+str(len(SERVICES[k]))+' services','/services/#'+k,'text-link','arr')}</div></article>''')
 practices=f'''<section class="studio-practices container" id="practices"><div class="practice-intro">{eyebrow('Our practices')}<h2 class="display">Where we <em>help.</em></h2><p>Three specialist practices. One point of contact, from the first conversation to the work itself.</p><div class="practice-picker" aria-label="Select a practice" hidden>{''.join(deck_controls)}</div></div><div class="practice-chapters">{''.join(chapters)}<div class="deck-controls" hidden><span role="status" data-deck-status></span><div><button type="button" data-deck-move="-1" aria-label="Previous practice">{icon('back')}</button><button type="button" data-deck-move="1" aria-label="Next practice">{icon('arr')}</button></div></div></div></section>'''
 phases=[
 ('Discover','Understand the business.','We start with the people doing the work. Together we examine what is happening now, what you want to change and how you will know it is working.'),
 ('Plan','Set the scope.','Your proposal sets out priorities, ownership, timing and price. You can see what the team will deliver before the work begins.'),
 ('Deliver','Review what changes.','Your named contact shares the work completed and the measures agreed at the start. The next review turns those findings into practical decisions.')]
 controls=''.join(f'<button type="button" id="step-{i}" data-step="{i}" aria-controls="method-{i}">{h(label)}</button>' for i,(label,_,_) in enumerate(phases))
 panels=''.join(f'<div id="method-{i}" class="framework-panel" aria-labelledby="step-{i}"><h3>{h(title)}</h3><p>{h(detail)}</p></div>' for i,(_,title,detail) in enumerate(phases))
 firm=f'''<section class="method-panel"><div class="container method-grid"><div>{eyebrow('The firm')}<h2 class="display">A partner in<br><em>the work.</em></h2><p class="method-lead">From Multan to US medical practices, our teams work to a clear scope and an agreed measure of progress.</p>{btn('About Cloud Haven','/about/','text-link')}</div><div class="framework"><div class="framework-steps" aria-label="How we work">{controls}</div>{panels}</div></div></section>'''
 guides=[
 ('Digital marketing','What goes into an SEO quote?','/blog/seo-cost-pakistan/'),
 ('Healthcare revenue','How does medical billing work?','/blog/what-is-medical-billing/'),
 ('Business consultancy','When should you bring in a consultant?','/blog/what-does-a-business-consultant-do/')]
 note_photos=['seo-audit-services','medical-billing-services-pakistan','business-consultancy-pakistan']
 stories=''.join(f'<article class="insight-card"><a href="{url}"><span class="insight-photo">{photo_image(key,sizes="(max-width: 700px) 100vw, 32vw")}</span><span class="art-kicker">{h(practice)}</span><h3>{h(title)}</h3><span class="read-guide">Read guide {icon("ne")}</span></a></article>' for (practice,title,url),key in zip(guides,note_photos))
 notes=f'''<section class="journal container">{eyebrow('Insights')}<div class="section-heading"><h2 class="display">From the <em>journal.</em></h2>{btn('All insights','/blog/','text-link')}</div><div class="insight-grid">{stories}</div></section>'''
 doc('/','Cloud Haven Consultants | Digital Marketing, Healthcare Revenue & Business Strategy','Independent consulting from Multan for businesses in Pakistan and US medical practices. Explore SEO, digital marketing, healthcare revenue and business strategy.',hero+practices+firm+finder()+notes+home_enquiry(),home=True,opening=opening)
