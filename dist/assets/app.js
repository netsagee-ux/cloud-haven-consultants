'use strict';
const $=(selector, context=document)=>context.querySelector(selector);
const $$=(selector, context=document)=>Array.from(context.querySelectorAll(selector));
const menu=$('#site-menu');
const opener=$('.menu-trigger');
opener.addEventListener('click',()=>{
  menu.showModal();
  $('body').classList.add('menu-lock');
  opener.setAttribute('aria-expanded','true');
  $('.menu-close').focus();
});
function closeNavigation(){
  if(menu.classList.contains('is-closing'))return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){menu.close();return}
  menu.classList.add('is-closing');
  window.setTimeout(()=>{if(menu.open)menu.close()},260);
}
$('.menu-close').addEventListener('click',closeNavigation);
menu.addEventListener('click',event=>{
  const link=event.target.closest('a[href]');
  if(link?.hash && link.origin===location.origin && link.pathname===location.pathname && link.search===location.search){
    menu.close();
  }
});
menu.addEventListener('cancel',event=>{event.preventDefault();closeNavigation()});
menu.addEventListener('close',()=>{
  menu.classList.remove('is-closing');
  $('body').classList.remove('menu-lock');
  opener.setAttribute('aria-expanded','false');
  opener.focus({preventScroll:true});
});
window.addEventListener('pageshow',()=>{if(menu.open)menu.close()});
const filters=$$('[data-filter]');
if(filters.length){
  let chosen='All topics';
  const search=$('#guide-search');
  const list=$$('.guide-row');
  const more=$('.guide-more');
  const batchSize=8;
  let limit=batchSize;
  function update(){
    let count=0;
    const term=search.value.trim().toLocaleLowerCase();
    list.forEach(row=>{
      const matches=(chosen==='All topics'||row.dataset.category===chosen)
        && (row.textContent+' '+row.dataset.summary).toLocaleLowerCase().includes(term);
      row.hidden=!matches||count>=limit;
      if(matches)count++;
    });
    $('.results-count').textContent=count>limit?'Showing '+limit+' of '+count+' guides':count+(count===1?' guide':' guides');
    $('.no-results').hidden=Boolean(count);
    more.hidden=count<=limit;
  }
  function startSearch(){limit=batchSize;update()}
  more.addEventListener('click',()=>{
    const previouslyHidden=new Set(list.filter(row=>row.hidden));
    limit+=batchSize;
    update();
    list.find(row=>previouslyHidden.has(row)&&!row.hidden)?.focus({preventScroll:true});
  });
  filters.forEach(b=>b.addEventListener('click',()=>{
    chosen=b.dataset.filter;
    filters.forEach(f=>f.setAttribute('aria-pressed',String(f===b)));startSearch();
  }));
  search.addEventListener('input',startSearch);
  update();
}
const form=$('#enquiry');
if(form){
  const params=new URLSearchParams(location.hash.startsWith('#brief=')?location.hash.slice(1):location.search);
  const sel=$('#service');
  if(Array.from(sel.options).some(o=>o.value===params.get('service'))) sel.value=params.get('service');
  $('#message').value=(params.get('brief')||'').slice(0,1500);
  form.addEventListener('submit',event=>{
    event.preventDefault();
    const subject='Cloud Haven enquiry — '+sel.value;
    const body=['Name: '+$('#ename').value,'Email: '+$('#em').value,'Company: '+($('#org')?.value||'—'),'Area: '+sel.value,'',$('#message').value].join('\n');
    const url='mailto:info@cloudhavenconsultants.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    const status=$('.form-status');
    status.hidden=false;
    const mail=document.createElement('a');mail.href=url;mail.textContent='Open the email draft again';
    const copy=document.createElement('button');copy.type='button';copy.textContent='Copy enquiry text';
    copy.addEventListener('click',async()=>{
      try{await navigator.clipboard.writeText(body);copy.textContent='Enquiry copied'}catch{
        const field=document.createElement('textarea');field.readOnly=true;field.value=body;field.setAttribute('aria-label','Enquiry text to copy');status.append(field);field.select();
      }
    });
    status.replaceChildren('Review and send your draft in your email app. ',mail,'. ',copy,'.');
    location.href=url;
  });
}
const quoteForm=document.querySelector('#quote form');
if(quoteForm){
  quoteForm.addEventListener('submit',event=>{
    event.preventDefault();
    const data=new URLSearchParams();
    data.set('brief',document.querySelector('#brief').value);
    data.set('service',document.querySelector('#scope').value);
    location.assign('/contact/#'+data.toString());
  });
}

$$('[data-interest]').forEach(button=>{
  button.addEventListener('click',()=>{
    $('#service').value=button.dataset.interest;
    $$('[data-interest]').forEach(other=>other.setAttribute('aria-pressed',String(other===button)));
  });
});

const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
const revealItems=$$('.chapter-photo,.chapter-copy,.practice-intro,.method-grid>div,.journal-row,.sub-photo,.editorial-steps article,.dir-rows a');
if('IntersectionObserver' in window&&!reducedMotion.matches){
  const observer=new IntersectionObserver(entries=>{
    entries.filter(entry=>entry.isIntersecting).forEach(entry=>{
      entry.target.classList.add('in-view');
      observer.unobserve(entry.target);
    });
  },{threshold:.08});
  revealItems.forEach((element,index)=>{
    element.classList.add('reveal');
    element.style.setProperty('--delay',(index%3)*45+'ms');
    observer.observe(element);
  });
}

const steps=$$('[data-step]');
if(steps.length){
  $('.framework-steps').setAttribute('role','tablist');
  function selectStep(index){
    steps.forEach((button,i)=>{
      const panel=document.getElementById(button.getAttribute('aria-controls'));
      button.setAttribute('role','tab');
      button.setAttribute('aria-selected',String(i===index));
      button.tabIndex=i===index?0:-1;
      panel.setAttribute('role','tabpanel');
      panel.tabIndex=0;
      panel.hidden=i!==index;
    });
  }
  steps.forEach((button,i)=>{
    button.addEventListener('click',()=>selectStep(i));
    button.addEventListener('keydown',event=>{
      const keys={ArrowRight:(i+1)%steps.length,ArrowLeft:(i+steps.length-1)%steps.length,Home:0,End:steps.length-1};
      if(!(event.key in keys))return;
      event.preventDefault();selectStep(keys[event.key]);steps[keys[event.key]].focus();
    });
  });
  selectStep(0);
}
