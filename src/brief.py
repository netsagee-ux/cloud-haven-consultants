import json

from common import DIST, PRACTICES, SERVICES, doc, h, icon

ALIASES = {
    'seo-agency-pakistan': 'search engine organic traffic keyword keywords ranking rank google visibility Pakistan strategy',
    'seo-audit-services': 'audit website crawl diagnose traffic drop analyse analysis site health ranking issues',
    'technical-seo-services': 'technical crawl indexing index speed sitemap slow schema robots web vitals',
    'local-seo-services': 'local maps Google business profile GBP nearby local listings Multan map pack directions',
    'content-marketing-services': 'copywriting blog article editorial publishing content writers writing',
    'social-media-marketing-agency-pakistan': 'social media socialmedia engagement Facebook Instagram LinkedIn TikTok posts',
    'digital-marketing-agency-pakistan': 'paid media PPC ads advertising channels conversions campaign digital marketing',
    'medical-billing-services-pakistan': 'medical billing Pakistan billers billing team coding claims posting submit',
    'medical-billing-services-usa': 'US USA United States America American practice medical billing billers Medicare claims posting',
    'revenue-cycle-management-services': 'RCM revenue cycle collections receivables cashflow cash flow payments track metrics',
    'revenue-cycle-management-outsourcing': 'outsource outsourced outsourcing RCM back office external billing workload',
    'denial-management-services': 'denial denied denials claims rejected appeals appeal payer rejection',
    'prior-authorization-services': 'prior authorization authorisation preauthorization approval prior auth payer approvals',
    'provider-credentialing-services': 'provider credentialing credentials credentialed enrolment enrollment renewals payer',
    'business-consultancy-pakistan': 'strategy business priorities growth planning advisory operations business plan Pakistan',
    'startup-consultant-pakistan': 'startup start-up launch founder product idea market validation starting new business',
    'management-consulting-services': 'management responsibilities team accountability leadership reporting roles organisation organization',
    'process-improvement-consulting': 'process improve improvement handoffs slow handovers bottleneck delays rework workflow handover repeated manual work',
}

def write_service_data():
    items = [
        {'id':slug,'title':title,'practice':key,'group':PRACTICES[key]['short'],
         'description':summary,'keywords':ALIASES[slug]}
        for key, services in SERVICES.items() for slug,title,summary in services
    ]
    (DIST/'assets/service-catalogue.json').write_text(json.dumps(items, ensure_ascii=False, separators=(',',':')))

def finder(on_home=False):
    crumb='<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> Project brief</nav>'
    filters = [('all','All'),('digital','Marketing'),('healthcare','Healthcare'),('business','Business')]
    def practice_filter(key, label):
        count = sum(map(len, SERVICES.values())) if key == 'all' else len(SERVICES[key])
        number = '' if on_home else f' <small>{count}</small>'
        return f'<button type="button" data-practice-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}{number}</button>'
    tabs = ''.join(practice_filter(key, label) for key, label in filters)
    examples = ''.join(f'<button type="button" data-example="{h(q)}">{h(q)}</button>' for q in ['Get found on Google Maps','Appeal denied claims','Fix a slow handover'])
    heading = '<h2 class="display">Find your <em>fit.</em></h2>' if on_home else '<h1 class="display">Build your <em>brief.</em></h1><p>Choose services for your consultation.</p>'
    search_examples = '' if on_home else f'<div class="finder-examples"><span>Try</span>{examples}</div>'
    question_examples = '' if on_home else '<div class="finder-examples"><span>Try</span><button type="button" data-question>Is the first call free?</button><button type="button" data-question>What access does an SEO audit need?</button><button type="button" data-question>Who handles US billing?</button></div>'
    return f'''<section id="service-finder" class="finder-area container" aria-label="Service finder and project brief" data-finder="{'compact' if on_home else 'full'}">
    {'' if on_home else crumb}<div class="finder-heading">{heading}</div>
    <div class="finder-grid"><div class="finder-main">
    <div class="finder-modes" hidden><button type="button" data-mode="services" aria-controls="service-search" aria-pressed="true">Find a service</button><button type="button" data-mode="answers" aria-controls="quick-answers" aria-pressed="false">Ask a question</button></div>
    <div id="service-search">
    <form class="finder-search" role="search"><label for="finder-query">What would you like help with?</label><div><input type="search" id="finder-query" maxlength="180" autocomplete="off" placeholder="For example, rejected medical claims"><button class="pill" type="submit">Find services {icon('arr')}</button></div></form>
{search_examples}
    <div class="finder-filters" aria-label="Filter by practice">{tabs}</div>
    <div class="finder-tools"><p class="finder-status" role="status">Explore the service directory below.</p><label>Sort <select aria-label="Sort services"><option value="relevance">Best match</option><option value="az">A–Z</option></select></label></div>
    <ul id="service-matches" class="finder-results"></ul><button class="show-services text-link" aria-controls="service-matches" hidden type="button">Show all results {icon('down')}</button><noscript><a href="/services/">Explore all 18 services</a></noscript></div>
    <section id="quick-answers" class="quick-answers" aria-label="Quick answers" hidden><form class="finder-search" id="questions"><label for="visitor-question">Ask Cloud Haven</label><p>Get an answer from the firm’s published pages.</p><div><input type="search" id="visitor-question" maxlength="220" required placeholder="Is the first consultation free?"><button class="pill" type="submit">Find answer {icon('arr')}</button></div></form>
    {question_examples}<div class="approved-answer" aria-live="polite" hidden></div></section></div>
    <aside class="brief-card" id="chosen-services"><h3>Your project brief<span class="brief-number" data-brief-count>0</span></h3><p class="brief-empty">Select services to discuss on your call.</p><ul class="brief-items"></ul><a class="pill brief-next" href="/contact/">Start an enquiry {icon('ne')}</a></aside></div></section>'''

def brief_page():
    doc('/project-brief/','Service finder & project brief','Match a business need to Cloud Haven services and build a consultation brief.',finder())
