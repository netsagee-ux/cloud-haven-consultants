'use strict';
const opening=document.getElementById('opening');
const film=document.querySelector('.film-hero');
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
const address=new URL(location.href);
const replay=address.searchParams.get('intro')==='1';
let seen=false;
try{seen=sessionStorage.getItem('cloud-haven-studio-opening')==='seen'}catch{}
if(replay){
  address.searchParams.delete('intro');
  history.replaceState(null,'',address.pathname+address.search+address.hash);
}
if((replay||!seen)&&!location.hash&&!reduced.matches&&typeof opening.showModal==='function'){
  const dial=opening.querySelector('.ignition');
  const skip=opening.querySelector('.skip-opening');
  let autoTurn=0,finishTimer=0,touchOrigin=null;
  function finish(animate){
    if(!opening.open)return;
    clearTimeout(autoTurn);
    clearTimeout(finishTimer);
    if(animate&&!reduced.matches)film.classList.add('is-revealing');
    opening.close();
    document.body.classList.remove('opening-lock');
    try{sessionStorage.setItem('cloud-haven-studio-opening','seen')}catch{}
    document.getElementById('intro-title').focus({preventScroll:true});
  }
  function turn(){
    if(opening.classList.contains('is-turning')||!opening.open)return;
    clearTimeout(autoTurn);
    opening.classList.add('is-turning');
    finishTimer=window.setTimeout(()=>finish(true),950);
  }
  opening.showModal();
  document.body.classList.add('opening-lock');
  dial.focus({preventScroll:true});
  dial.addEventListener('click',turn);
  dial.addEventListener('pointerdown',event=>{
    touchOrigin={x:event.clientX,y:event.clientY};
    dial.setPointerCapture(event.pointerId);
  });
  dial.addEventListener('pointermove',event=>{
    if(touchOrigin&&Math.hypot(event.clientX-touchOrigin.x,event.clientY-touchOrigin.y)>10)turn();
  });
  dial.addEventListener('lostpointercapture',()=>{touchOrigin=null});
  skip.addEventListener('click',()=>finish(false));
  opening.addEventListener('cancel',event=>{event.preventDefault();finish(false)});
  reduced.addEventListener('change',()=>{if(reduced.matches)finish(false)});
  window.addEventListener('pagehide',()=>finish(false),{once:true});
  if(!replay)autoTurn=window.setTimeout(turn,2300);
}

const picker=document.querySelector('.practice-picker');
if(picker){
  const select=[...picker.querySelectorAll('[data-chapter]')];
  const chapters=[...document.querySelectorAll('.practice-entry')];
  const pager=document.querySelector('.deck-controls');
  const count=pager.querySelector('[data-deck-status]');
  let current=0;
  function showChapter(index){
    current=(index+chapters.length)%chapters.length;
    chapters.forEach((chapter,i)=>{chapter.hidden=i!==current});
    select.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===current)));
    count.textContent='Practice '+(current+1)+' of '+chapters.length;
  }
  select.forEach((button,i)=>{
    button.addEventListener('click',()=>showChapter(i));
    button.addEventListener('keydown',event=>{
      const step={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[event.key];
      if(!step)return;
      event.preventDefault();showChapter(i+step);select[current].focus();
    });
  });
  pager.querySelectorAll('[data-deck-move]').forEach(button=>button.addEventListener('click',()=>showChapter(current+Number(button.dataset.deckMove))));
  picker.hidden=false;pager.hidden=false;
  document.querySelector('.practice-chapters').classList.add('interactive');
  showChapter(0);
}
