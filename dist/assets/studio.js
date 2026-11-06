'use strict';

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
