'use strict';
(() => {
  const key = 'cloud-haven-project-brief-v1';
  const finder = document.querySelector('[data-finder]');
  const counters = document.querySelectorAll('[data-brief-count]');
  const saveButtons = document.querySelectorAll('[data-save-service]');
  function readSaved(){
    try {
      const data = JSON.parse(localStorage.getItem(key) || '[]');
      return Array.isArray(data) ? [...new Set(data.filter(id => typeof id === 'string' && /^[a-z0-9-]{1,80}$/.test(id)))].slice(0,18) : [];
    } catch { return []; }
  }
  let saved = readSaved();
  let catalogue = [];
  const make = (tag, className, value) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined) el.textContent = value;
    return el;
  };
  const serviceLink = item => {
    const link = make('a', '', item.title);
    link.href = '/' + item.id + '/';
    return link;
  };
  function toggle(id){
    saved = saved.includes(id) ? saved.filter(item => item !== id) : [...saved,id].slice(0,18);
    try { localStorage.setItem(key, JSON.stringify(saved)); } catch {}
    sync();
  }
  function updateSaveButton(button, id){
    const selected = saved.includes(id);
    button.setAttribute('aria-pressed', String(selected));
    button.textContent = selected ? 'Added to brief ✓' : 'Add to brief +';
  }
  function sync(){
    counters.forEach(el => { el.textContent = String(saved.length); });
    saveButtons.forEach(el => updateSaveButton(el, el.dataset.saveService));
    if (!finder) return;
    finder.querySelectorAll('[data-result-save]').forEach(el => updateSaveButton(el,el.dataset.resultSave));
    const empty = finder.querySelector('.brief-empty');
    const list = finder.querySelector('.brief-items');
    const selected = saved.map(id => catalogue.find(item => item.id === id)).filter(Boolean);
    const next = finder.querySelector('.brief-next');
    empty.hidden = selected.length > 0;
    list.replaceChildren(...selected.map(item => {
      const row = make('li');
      const remove = make('button','remove-choice','×');
      remove.type = 'button';
      remove.setAttribute('aria-label','Remove '+item.title+' from brief');
      remove.addEventListener('click',() => {
        const index = selected.indexOf(item);
        toggle(item.id);
        const controls = list.querySelectorAll('button');
        (controls[Math.min(index, controls.length - 1)] || next).focus({preventScroll:true});
      });
      row.append(serviceLink(item),remove);
      return row;
    }));
    if (selected.length) {
      const prompt = 'I would like to discuss the following services:\n'+selected.map(item => '• '+item.title).join('\n');
      const params = new URLSearchParams({brief:prompt, service:selected.length === 1 ? selected[0].title : 'Not sure yet'});
      next.href = '/contact/#'+params.toString();
    } else { next.href = '/contact/'; }
  }
  saveButtons.forEach(button => button.addEventListener('click',() => toggle(button.dataset.saveService)));
  sync();
  window.addEventListener('pageshow',() => { saved=readSaved(); sync(); });
  window.addEventListener('storage',event => {
    if (event.key === key || event.key === null) { saved=readSaved(); sync(); }
  });
  if (!finder) return;
  const input = finder.querySelector('#finder-query');
  const results = finder.querySelector('.finder-results');
  const status = finder.querySelector('.finder-status');
  const more = finder.querySelector('.show-services');
  const sort = finder.querySelector('select');
  const filters = [...finder.querySelectorAll('[data-practice-filter]')];
  const noText = new Set('a an the my me we our i to of how do does for can us with you is have get what on and want need help let find would like your in are it at'.split(' '));
  const words = value => value.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/).filter(Boolean);
  let group = 'all', expanded = false;
  function score(item, tokens){
    if (!tokens.length) return 1;
    const title = words(item.title), extra = words(item.keywords), summary = words(item.description);
    const matches = tokens.map(token => (title.includes(token)?5:0)+(extra.includes(token)?3:0)+(summary.includes(token)?1:0));
    return matches.some(Boolean) ? matches.reduce((a,b)=>a+b,0) + matches.filter(Boolean).length*3 : 0;
  }
  function render(){
    if(!catalogue.length)return;
    const tokens = [...new Set(words(input.value).filter(w => !noText.has(w) || (w==='us' && /\bUS(?:A)?\b/.test(input.value))))];
    const ranked = catalogue.filter(item => group==='all'||item.practice===group)
      .map(item => ({item,rank:score(item,tokens)})).filter(entry => entry.rank > 0);
    const strongest = Math.max(0,...ranked.map(entry => entry.rank));
    const matches = tokens.length > 1 ? ranked.filter(entry => entry.rank >= strongest * 0.6) : ranked;
    matches.sort((a,b) => sort.value==='az' ? a.item.title.localeCompare(b.item.title) : b.rank-a.rank);
    const count = matches.length;
    const visible = expanded ? matches : matches.slice(0,3);
    status.textContent = count ? (count===1?'1 matching service':count+' matching services') : 'No matching services. Try a different word or choose another practice.';
    results.replaceChildren(...visible.map(({item}) => {
      const row = make('li','match-row'), text = make('div','match-copy');
      const heading = make('h3');
      heading.append(serviceLink(item));
      text.append(make('small','match-group',item.group),heading,make('p','',item.description));
      const button = make('button','match-save');
      button.type = 'button'; button.dataset.resultSave = item.id;
      updateSaveButton(button,item.id);
      button.addEventListener('click',()=>toggle(item.id));
      row.append(text,button);
      return row;
    }));
    if (!count) {
      const link=make('a','text-link','Ask the team about your project ↗');
      link.href='/contact/'; const row=make('li'); row.append(link); results.append(row);
    }
    more.hidden=count<=3;
    more.textContent=expanded?'Show fewer services ↑':'Show all '+count+' services ↓';
    more.setAttribute('aria-expanded',String(expanded));
  }
  function resetResults(){ expanded=false;render(); }
  finder.querySelector('form').addEventListener('submit',event => {event.preventDefault();resetResults();});
  input.addEventListener('input',resetResults);
  sort.addEventListener('change',render);
  function selectGroup(name){
    group=name;
    filters.forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.practiceFilter===group)));
  }
  filters.forEach(button=>button.addEventListener('click',()=>{selectGroup(button.dataset.practiceFilter);resetResults();}));
  finder.querySelectorAll('[data-example]').forEach(button=>button.addEventListener('click',()=>{
    input.value=button.dataset.example;selectGroup('all');resetResults();
  }));
  more.addEventListener('click',()=>{expanded=!expanded;render();});
  fetch('/assets/service-catalogue.json?v=studio-3').then(response=>{
    if(!response.ok)throw Error('Catalogue unavailable');
    return response.json();
  }).then(data=>{
    catalogue=data;
    saved=saved.filter(id=>catalogue.some(item=>item.id===id));
    render();sync();
  }).catch(()=>{
    status.textContent='Open the directory to see all services.';
    const link=make('a','text-link','Open service directory →');
    link.href='/services/';const row=make('li');row.append(link);results.replaceChildren(row);
  });
})();

(() => {
  const box=document.querySelector('[data-finder]');
  if(!box)return;
  const controls=box.querySelector('.finder-modes');
  const servicePane=box.querySelector('#service-search');
  const answerPane=box.querySelector('#quick-answers');
  const question=box.querySelector('#visitor-question');
  const output=box.querySelector('.approved-answer');
  controls.hidden=false;
  controls.querySelectorAll('button').forEach(button=>button.addEventListener('click',()=>{
    const answers=button.dataset.mode==='answers';
    controls.querySelectorAll('button').forEach(el=>el.setAttribute('aria-pressed',String(el===button)));
    servicePane.hidden=answers;answerPane.hidden=!answers;
  }));

  // Each supported question points to the page that supplies the answer.
  const answers=[
    {test:/first (call|consultation)|initial (call|consultation)|introductory (call|consultation)|free.{0,18}(call|consultation)|(call|consultation).{0,18}free/i,title:'Your first consultation',text:'The first consultation is free. Use the 30-minute call to explain your priorities and agree which service fits.',path:'/contact/',source:'Consultation and contact'},
    {test:/pricing|price|quote|how much|fees|cost|charged|charge me/i,title:'How work is priced',text:'The team agrees a written scope before quoting. Marketing can use a monthly retainer, consulting projects have agreed deliverables, and billing may use a per-claim fee or a share of collections.',path:'/pricing/',source:'Scope and pricing'},
    {test:/partner|superbillone|who.*(bill|claims)|who.*us practice/i,title:'US healthcare billing',text:'Cloud Haven coordinates healthcare revenue work with SuperBillOne LLC in Austin, Texas. The introductory call covers the practice workflow, payer mix and responsibilities.',path:'/medical-billing-services-usa/',source:'Billing for US practices'},
    {test:/opening hours|business hours|working hours|when.*open|what time|time zone/i,title:'Office hours',text:'The team is available Monday to Saturday, 9:00 am to 6:00 pm Pakistan time. Include your time zone when requesting a US call.',path:'/contact/',source:'Contact and office hours'},
    {test:/where.*based|where.*located|office address|where.*office/i,title:'Where the firm is based',text:'Cloud Haven is based in Multan, Pakistan, and coordinates healthcare revenue work with its billing partner in the United States.',path:'/about/',source:'About Cloud Haven'},
    {test:/((access|permission|credentials).*(audit|analytics|search console)|(audit|analytics|search console).*(access|permission|credentials))/i,title:'Access for an SEO audit',text:'Read access to Analytics and Search Console usually covers the data review. Hosting credentials are unnecessary for the audit.',path:'/seo-audit-services/',source:'SEO audits'},
    {test:/((long|weeks|time).*(seo audit)|(seo audit).*(long|weeks|take))/i,title:'SEO audit timing',text:'A typical review takes one to two weeks. A larger site may need longer, so timing is confirmed when the scope is agreed.',path:'/seo-audit-services/',source:'SEO audits'},
    {test:/wordpress|shopify|which.*platform|custom sites?/i,title:'Platforms for technical SEO',text:'The technical SEO team works on WordPress, Shopify and custom sites. Checks can cover theme performance, plugins and caching.',path:'/technical-seo-services/',source:'Technical SEO'},
    {test:/languages?|roman urdu/i,title:'Languages for search content',text:'The team looks at how your customers search, then plans English, Urdu or Roman Urdu content to suit those searches.',path:'/seo-agency-pakistan/',source:'SEO strategy in Pakistan'}
  ];
  function answer(){
    const value=question.value.trim();
    if(!value)return;
    const result=answers.find(item=>item.test.test(value));
    const heading=document.createElement('h3');
    const paragraph=document.createElement('p');
    const link=document.createElement('a');
    link.className='text-link';
    if(result){
      heading.textContent=result.title;paragraph.textContent=result.text;
      link.textContent='Source: '+result.source+' ↗';link.href=result.path;
    }else{
      heading.textContent='Ask the consulting team';
      paragraph.textContent='The published answers do not cover this question. You can take it into an enquiry and review the message before sending.';
      link.textContent='Carry this question into an enquiry ↗';
      link.href='/contact/#'+new URLSearchParams({brief:value}).toString();
    }
    output.replaceChildren(heading,paragraph,link);output.hidden=false;
  }
  box.querySelector('#questions').addEventListener('submit',event=>{event.preventDefault();answer()});
  box.querySelectorAll('[data-question]').forEach(button=>button.addEventListener('click',()=>{question.value=button.textContent;answer()}));
})();
