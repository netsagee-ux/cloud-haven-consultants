import json
from shutil import copyfile
from common import *
from home import homepage
from brief import brief_page, write_service_data

PAGES={v['path']:v for v in json.loads((ROOT/'src/pages.json').read_text())}
GUIDES=json.loads((ROOT/'src/guides.json').read_text())
if (ROOT/'src/extra-guides.json').is_file():
    GUIDES+=json.loads((ROOT/'src/extra-guides.json').read_text())
EXTRAS=json.loads((ROOT/'src/service-extras.json').read_text())
ARCHIVES=json.loads((ROOT/'src/archives.json').read_text())
GIMAGE={'Digital marketing':'digital','Healthcare revenue':'healthcare','Business consultancy':'business','Roman Urdu':'digital'}
GUIDEHOME={'digital':'/blog/what-is-an-seo-audit/','healthcare':'/blog/what-is-medical-billing/','business':'/blog/what-does-a-business-consultant-do/'}
def cards(items):
 return '<div class="editorial-steps">'+''.join(f'<article><h3>{h(q)}</h3><p>{h(a)}</p></article>' for q,a in items)+'</div>'
def sections(rec):return [(s['heading'],s['text']) for s in rec['sections']]
def rows(items):
 return '<div class="dir-rows">'+''.join(f'<a href="{h(link)}"><div><h3>{h(title)}</h3><p>{h(desc)}</p></div>{icon("ne")}</a>' for title,link,desc in items)+'</div>'
def service_hub():
 body=subhero('Services','Our services.','Explore three connected practices. Choose the help you need now, from a focused audit to ongoing support.')
 tiles=''.join(f'<a class="service-tile" href="#{key}">{photo_image(key,sizes="(max-width: 700px) 100vw, 32vw")}<span><small>{len(SERVICES[key])} services</small><strong>{h(item["short"])}</strong></span>{icon("down")}</a>' for key,item in PRACTICES.items())
 body+=f'<nav class="practice-shelf container" aria-label="Practice directory">{tiles}</nav>'
 for k,v in PRACTICES.items():
  body+=f'<section id="{k}" class="directory container"><div class="dir-head">{eyebrow(v["audience"])}<h2>{h(v["name"])}</h2><p>{h(v["intro"])}</p></div>'+rows([(title,'/'+slug+'/',desc) for slug,title,desc in SERVICES[k]])+'</section>'
 doc('/services/','Services',PAGES['/services/']['summary'],body+end_cta())
def service_pages():
 for k,group in SERVICES.items():
  v=PRACTICES[k]
  for j,(slug,title,desc) in enumerate(group):
   path='/'+slug+'/'; rec=PAGES[path]
   action=btn('Discuss this service','/contact/?service='+quote(title))+f'<button class="text-link" type="button" data-save-service="{slug}" aria-pressed="false">Add to brief +</button>'+btn('View brief','/project-brief/#chosen-services','text-link','arr')
   photo=PHOTOGRAPHY[slug]['asset']
   description=PHOTOGRAPHY[slug]['alt']
   body=subhero(v['short'],title+'.',rec['summary'],photo,action,('Services','/services/'),photo_alt=description)
   body+=sect('Scope of work','What we work on.',cards(sections(rec)))
   extra=EXTRAS[path]
   body+=sect('Deliverables','What you receive.','<ul class="deliverables">'+''.join(f'<li>{h(d)}</li>' for d in extra['deliverables'])+'</ul>')
   if k=='healthcare':
    body+=sect('Delivery partner','US healthcare operations.', '<p>Cloud Haven coordinates billing work with SuperBillOne LLC, a US-registered medical billing company in Austin, Texas. Your introductory call covers the practice workflow, payer mix and the responsibilities on each side.</p>'+btn('Meet the billing partner','https://superbillone.com/','text-link'))
   body+=sect('Questions','Before you start.',details([(qa['q'],qa['a']) for qa in extra['faq']]))
   related=[group[(j+a)%len(group)] for a in (1,2)]
   body+=sect('Next steps','Related services.',rows([(t,'/'+s+'/',d) for s,t,d in related])+btn('All '+v['short']+' services','/services/#'+k,'text-link'))
   related_guides={
    'seo-agency-pakistan':['seo-cost-pakistan','how-to-choose-an-seo-agency'],
    'seo-audit-services':['what-is-an-seo-audit','keyword-research-for-beginners'],
    'technical-seo-services':['what-is-technical-seo','speed-up-wordpress-site'],
    'local-seo-services':['what-is-local-seo','google-business-profile-setup'],
    'content-marketing-services':['content-marketing-strategy','how-to-brief-a-content-writer'],
    'social-media-marketing-agency-pakistan':['social-media-marketing-for-small-business','facebook-ads-for-beginners'],
    'digital-marketing-agency-pakistan':['digital-marketing-kya-hai','seo-vs-sem'],
    'medical-billing-services-pakistan':['what-is-medical-billing','how-to-choose-a-medical-billing-company'],
    'medical-billing-services-usa':['medical-billing-contract-checklist','medical-billing-cost'],
    'revenue-cycle-management-services':['what-is-revenue-cycle-management','rcm-metrics-to-track'],
    'revenue-cycle-management-outsourcing':['should-you-outsource-medical-billing','medical-billing-contract-checklist'],
    'denial-management-services':['top-claim-denial-reasons','how-to-write-a-claim-appeal-letter'],
    'prior-authorization-services':['what-is-prior-authorization','prior-authorization-checklist'],
    'provider-credentialing-services':['what-is-provider-credentialing','new-practice-credentialing-checklist'],
    'business-consultancy-pakistan':['what-does-a-business-consultant-do','business-consultant-fees'],
    'startup-consultant-pakistan':['how-to-start-a-business-in-pakistan','what-does-a-business-consultant-do'],
    'management-consulting-services':['business-consultant-vs-business-analyst','what-is-process-improvement'],
    'process-improvement-consulting':['what-is-process-improvement','what-does-a-business-consultant-do']}
   reading={f'/blog/{r}/' for r in related_guides[slug]}
   body+=sect('Field notes','Further reading.',rows([(g['title'],g['path'],g['summary']) for g in GUIDES if g['path'] in reading]))
   doc(path,title,rec['summary'],body+end_cta())
def contact():
 body=subhero('Contact','Let’s talk.','Tell us a little about your business and what you’d like to change. The first consultation is free.')
 opts=['Not sure yet',*[v['name'] for v in PRACTICES.values()],*[t for g in SERVICES.values() for _,t,_ in g],'Careers','Reference or sample report']
 body+=f'''<section class="contact-layout container"><div><div class="contact-info">{eyebrow('Contact the team')}<h2>Multan, Pakistan.</h2><p>Monday–Saturday<br>9:00 am–6:00 pm PKT</p><p>For a US call, include your time zone so we can arrange a suitable time.</p><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:+923421958957">{PHONE}</a></div></div>
 <form id="enquiry" class="enquiry-form" action="mailto:{EMAIL}" method="post" enctype="text/plain"><h2>Project enquiry.</h2><div class="field-pair"><div class="field"><label for="ename">Your name</label><input id="ename" name="name" required maxlength="100" autocomplete="name"></div><div class="field"><label for="em">Email address</label><input id="em" name="email" type="email" required maxlength="254" autocomplete="email"></div></div><div class="field"><label for="org">Company (optional)</label><input id="org" name="company" maxlength="150" autocomplete="organization"></div><div class="field"><label for="service">What can we help with?</label><select id="service" name="service">{''.join(f'<option>{h(o)}</option>' for o in opts)}</select></div><div class="field"><label for="message">Your message</label><textarea id="message" name="message" rows="5" required maxlength="1800" placeholder="A little about your project, priorities and timeline"></textarea></div><p class="form-hint">Please leave patient details out of your enquiry.</p><button class="pill" type="submit">Prepare email {icon('ne')}</button><p class="form-hint">Opens a draft in your email app for you to review and send.</p><div class="form-status" role="status" hidden></div></form></section>'''
 body+=sect('After your enquiry','What happens next.',cards([('An initial conversation','Use a free 30-minute call to explain your priorities and decide which service fits.'),('A written scope','Review the proposed work, timescale and price before deciding whether to proceed.')]))
 doc('/contact/','Contact',PAGES['/contact/']['summary'],body)
def company():
 rec=PAGES['/about/']
 body=subhero('The firm','Independent advice. Shared direction.',rec['summary'],'editorial/firm',btn('Work with us','/contact/'),photo_alt='Colleagues reviewing work together around a table')
 body+=f'''<section class="leadership container" id="leadership"><figure class="founder-photo">{photo_image('editorial-menu')}</figure><div>{eyebrow('Leadership')}<h2 class="display">Umar M.</h2><p class="founder-role">Founder &amp; CEO</p><p>Umar leads Cloud Haven from Multan, Pakistan. The firm brings digital marketing, business consulting and healthcare revenue support together through one point of contact.</p>{btn('Explore the services','/services/','text-link','arr')}</div></section>'''
 body+=sect('About Cloud Haven','A team built around your business.',cards([('One person to call','You have one contact for your account. When an issue crosses from marketing into operations, the two teams can work from the same brief.'),('A written plan','We agree what the work covers, who is responsible and how to measure progress. Reviews cover what changed and what to do next.'),('A US billing partner','SuperBillOne LLC, based in Austin, Texas, delivers healthcare revenue work with Cloud Haven. We coordinate with US medical practices during their working hours.')]))
 body+=sect('Explore the firm','Working with us.',rows([('Careers','/careers/','Explore the disciplines we recruit for and introduce yourself.'),('Case studies','/case-studies/','See how client evidence is measured and shared.'),('Pricing','/pricing/','Learn how we scope work and prepare a quote.')]))
 doc('/about/','About Cloud Haven',rec['summary'],body+end_cta())
 rec=PAGES['/careers/']
 body=subhero('Careers','Work with Cloud Haven.',rec['summary'],'editorial/careers',btn('Introduce yourself','mailto:'+EMAIL+'?subject=Career%20enquiry'),photo_alt='A group gathered around a laptop at work')
 body+=sect('Opportunities','Where you can contribute.',cards([('Healthcare operations','Claims submission, accounts receivable, denial follow-up and provider credentialing for US medical practices.'),('Search and content','Technical SEO, content planning, campaign delivery and reporting for local and national businesses.'),('Business consulting','Process mapping, analysis and practical planning for founders and management teams.')]))
 body+=sect('Applications','Send a short introduction.',f'<p>Tell us the role you’re interested in, where you’re based and one relevant example of your work. Attach your CV to your email. The team accepts introductions even between hiring rounds.</p>{btn("Email your CV","mailto:"+EMAIL+"?subject=Career%20enquiry","text-link")}')
 doc('/careers/','Careers',rec['summary'],body)
 rec=PAGES['/case-studies/']
 body=subhero('Case studies','Evidence behind the work.',rec['summary'],'editorial/case-review',btn('Request a reference','/contact/?service=Reference%20or%20sample%20report'),photo_alt='Colleagues looking over printed charts at a meeting')
 body+=sect('Our approach','How a case is documented.',cards([('Agree the baseline','Choose the question, the measure and a time period before work starts. For billing, the team can review aggregate claims, denials and payment data.'),('Record the changes','Document the work, compare the same measure over a comparable period and explain other factors that affect the result.'),('Get client approval','The client reviews the wording and the figures before publication. Healthcare examples exclude identifiable patient information.')]))
 body+=sect('Available by request','References and sample reports.','<p>The firm is preparing its approved case studies. In the meantime, you can ask for a sample report using illustrative data, or a reference call subject to the client’s agreement.</p>'+btn('Request a sample','/contact/?service=Reference%20or%20sample%20report','text-link'))
 doc('/case-studies/','Case studies',rec['summary'],body)
 rec=PAGES['/pricing/']
 body=subhero('Pricing','Scope first. Then a quote.',rec['summary'],links=btn('Build your brief','#quote','pill','down'))
 body+=sect('Pricing models','How engagements are priced.',cards([('Monthly marketing','An agreed monthly scope covers search, content or social campaigns. Marketing retainers typically begin with a three-month term. Advertising spend is budgeted separately.'),('Projects and advice','An audit or a defined consulting project has a written scope, milestones and deliverables. Site size, complexity, available data and team capacity affect the quote.'),('Healthcare revenue','The billing proposal may use a per-claim fee or a share of collections. Claim volume, payer mix and the work retained by your practice affect the model.')]))
 body+=f'''<section class="contact-layout container" id="quote"><div>{eyebrow('Request a quote')}<h2 class="standalone">Build your brief.</h2><p class="large-muted">Share a starting point for the conversation. We’ll carry your answers into the enquiry form.</p></div><form class="enquiry-form" action="/contact/"><div class="field"><label for="scope">Practice</label><select id="scope" name="service">{''.join(f'<option>{h(v["name"])}</option>' for v in PRACTICES.values())}</select></div><div class="field"><label for="brief">What should the work cover?</label><textarea required id="brief" name="brief" rows="3" maxlength="1500" placeholder="Current situation, goals and timing"></textarea></div><button class="pill">Continue to enquiry {icon("arr")}</button></form></section>'''
 doc('/pricing/','Pricing',rec['summary'],body)
def guide_list(path,title,intro,items,archive=False,roman=False):
 body=subhero('Insights' if not roman else 'Roman Urdu',title,intro,'editorial/research' if path=='/blog/' else '',photo_alt='Three people comparing information on their phones')
 cats=list(GIMAGE)
 if not archive:
  body+='<div class="filter-bar container"><div class="chips filter-chips" aria-label="Filter guides by practice">'+''.join(f'<button type="button" data-filter="{h(c)}" aria-pressed="{str(i==0).lower()}">{h(c)}</button>' for i,c in enumerate(['All topics',*cats]))+'</div><label class="guide-search">'+icon('search')+'<span class="sr-only">Search guides</span><input type="search" id="guide-search" placeholder="Search guides"></label></div>'
 body+='<section class="guide-list container" aria-label="Guides"><p class="results-count micro" aria-live="polite">'+str(len(items))+' guides</p>'
 body+=''.join(f'<a class="guide-row" data-category="{h(v["category"])}" href="{h(v["path"])}"><span class="entry-category">{h(v["category"])}</span><div><h2>{h(v["title"])}</h2><p>{h(v["summary"])}</p></div>{icon("ne")}</a>' for v in items)
 body+='<p class="no-results" hidden>No guides match your search. Try another term or choose All topics.</p></section>'
 if path=='/blog/':
  categories=[p for p in ARCHIVES['archives'] if p.startswith('/category/')]
  body+='<div class="archive-nav container">'+eyebrow('Article archive')+'<div>'+''.join(f'<a href="{h(p)}">{h(p.split("/")[2].capitalize())}</a>' for p in categories)+'<a href="/author/hostsuperbillonegmail-com/">Editorial archive</a></div></div>'
 if path.startswith('/author/'):
  other=next((p for p in ARCHIVES['archives'] if p.startswith('/author/') and p!=path),'')
  if other:body+='<div class="container">'+btn('Previous entries' if '/page/2/' in path else 'Older entries',other,'text-link')+'</div>'
 if archive:body+='<div class="container archive-out">'+btn('All insights','/blog/','text-link')+'</div>'
 doc(path,title.rstrip('.'),intro,body+end_cta())
def write_guides():
 guide_list('/blog/','Field notes.','Practical reading on search, healthcare revenue and running a business. Browse guides in English and Roman Urdu.',GUIDES)
 guide_list('/blog/category/roman-urdu/','Roman Urdu guides.','Search aur digital marketing ko seedhi Roman Urdu mein samjhein.',[v for v in GUIDES if v['category']=='Roman Urdu'],True,True)
 hello={'path':'/hello-world/','category':'Business consultancy','lang':'en','title':'Welcome to Cloud Haven','summary':'Find the practice and reading material that fit your business.','sections':[{'heading':'Explore the firm','text':'Our team works across search, healthcare revenue and business consulting. Start with our service directory to see which practice fits your priorities.'}]}
 store={r['path']:r for r in [*GUIDES,hello]}
 for v in store.values():
  k=GIMAGE[v['category']]
  body=subhero(v['category'],v['title'],v['summary'],parent=('Insights','/blog/'))
  body+='<section class="reader container"><nav aria-label="In this guide">'+eyebrow('In this guide')+''.join(f'<a href="#section-{i}">{h(s["heading"])}</a>' for i,s in enumerate(v['sections']))+'</nav><div>'+''.join(f'<article id="section-{i}"><h2>{h(s["heading"])}</h2><p>{h(s["text"])}</p></article>' for i,s in enumerate(v['sections']))+btn('Explore related services','/services/#'+k,'text-link')+'</div></section>'
  doc(v['path'],v['title'],v['summary'],body+end_cta(),lang=v['lang'])
 for path,v in ARCHIVES['archives'].items():
  tag=path.split('/')[2]
  title=(('SaaS' if tag=='saas' else tag.capitalize())+' articles.') if path.startswith('/category/') else 'Editorial archive.'
  items=[store[p] for p in v['posts'] if p in store]
  guide_list(path,title,'Explore articles from the Cloud Haven archive.',items,True)
def photography():
 body=subhero('Photography','Photography credits.','Explore the original photographers and sources for the editorial images shown across this website.')
 for heading,entries in [('Service photography',[v for v in PHOTOGRAPHY.values() if v['asset'].startswith('photo/services/')]),('Practices and editorial',[v for v in PHOTOGRAPHY.values() if not v['asset'].startswith('photo/services/')])]:
  credit_rows=[]
  for item in entries:
   original=item['original']
   ref=item.get('reference','')
   source_name=next((label for pattern,label in [('cloudhavenconsultants.com','Cloud Haven'),('dribbble.com','Dribbble'),('pexels.com','Pexels'),('unsplash.com','Unsplash'),('shopify.com','Burst'),('picjumbo.com','Picjumbo')] if pattern in original),'Photographer')
   links=f'<a href="{h(original)}">{source_name} original ↗</a>'
   if ref and ref!=original:
    label='Pinterest' if 'pinterest.' in ref else ('Dribbble' if 'dribbble.com' in ref else 'Company website')
    links+=f' <a href="{h(ref)}">{label} ↗</a>'
   credit_rows.append(f'<li><strong>{h(item["title"])}</strong><span>{h(item["photographer"])}</span><div>{links}</div></li>')
  body+=sect('Credits',heading,'<ul class="credits-list">'+''.join(credit_rows)+'</ul>')
 doc('/photography/','Photography credits','Original photographers and editorial image sources.',body)
def policies():
 for path, title, intro, items in [
  ('/privacy-policy/','Privacy.','How this site handles an enquiry.',[('Contact details','The enquiry form uses the information you enter to prepare an email draft on your device. You choose whether to send it. Your email provider then handles delivery.'),('Browsing','This website does not set advertising cookies. It may use session storage in your browser to remember whether you have seen the opening animation. If you add services to your brief, the site stores their names on this device so they are here when you return. You can remove each selection in Your brief. The hosting service may process ordinary connection and access information.'),('Healthcare enquiries','Keep messages at the business level. Please send only the details needed to arrange a conversation, and leave out patient records and medical identifiers.'),('Privacy questions','For enquiries about an email you sent to the firm, contact '+EMAIL+'.')]),
  ('/terms/','Website terms.','Using the information and enquiry tools on this website.',[('Service information','The directory describes areas of work available for discussion. Project scope, fees, delivery dates and responsibilities are agreed in a separate written proposal.'),('Editorial guides','The guides are general information for business teams. A practice or business should review the specific requirements that apply to its own work.'),('Enquiries','Opening an email draft does not submit a booking or start a paid engagement. Review and send the draft to contact the firm.')])]:
  doc(path,title.rstrip('.'),intro,subhero('Website information',title,intro)+sect('Information',title,cards(items)))
def alias(path,target):
 file=DIST/path.strip('/')/'index.html';file.parent.mkdir(parents=True,exist_ok=True)
 file.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cloud Haven Consultants</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{h(HOST+target)}"><meta http-equiv="refresh" content="0; url={h(target)}"></head><body style="background:#f6f6ef;color:#183b32;font:20px system-ui"><a style="color:inherit" href="{h(target)}">Continue to Cloud Haven Consultants</a></body></html>')
def build():
 write_service_data();homepage();service_hub();service_pages();brief_page();contact();company();write_guides();policies();photography()
 for path,target in {'/blog/how-to-choose-seo-agency/':'/blog/how-to-choose-an-seo-agency/','/services-2/':'/services/','/2240-2/':'/management-consulting-services/','/business-consultancy-services-in-pakistan/':'/business-consultancy-pakistan/','/seo-agency-in-pakistan-cloud-haven-consultants/':'/seo-agency-pakistan/','/startup-consultant-in-pakistan-cloud-haven-consultants/':'/startup-consultant-pakistan/','/local-seo-multan/':'/local-seo-services/','/seo-agency-multan/':'/seo-agency-pakistan/','/business-consultancy-multan/':'/business-consultancy-pakistan/'}.items():alias(path,target)
 doc('/not-found/','Page not found','Find your way back to Cloud Haven.',subhero('404','Page not found.','Try the service directory or return to the homepage.',links=btn('Home','/')+btn('All services','/services/','text-link')),noindex=True);copyfile(DIST/'not-found/index.html',DIST/'404.html')
 sitemap=[HOST+'/'+p.parent.relative_to(DIST).as_posix().strip('./')+('/' if p.parent!=DIST else '') for p in sorted(DIST.rglob('index.html')) if 'noindex,follow' not in p.read_text()]
 (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+h(x)+'</loc></url>' for x in sitemap)+'</urlset>')
 (DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+HOST+'/sitemap.xml\n')
if __name__=='__main__':build()
