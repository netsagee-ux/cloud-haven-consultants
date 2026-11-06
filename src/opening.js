(() => {
  const opening = document.getElementById('opening');
  const url = new URL(location.href);
  const replay = url.searchParams.get('intro') === '1';
  const navigation = performance.getEntriesByType('navigation')[0];
  if (!replay && (url.hash || navigation?.type === 'back_forward')) return;
  if (typeof opening.showModal !== 'function') return;
  if (replay) {
    url.searchParams.delete('intro');
    history.replaceState(history.state, '', url.pathname + url.search + url.hash);
  }

  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const enter = opening.querySelector('.ignition');
  let advanceTimer;
  let exitTimer;
  function finish(reveal = true) {
    clearTimeout(advanceTimer);
    clearTimeout(exitTimer);
    if (!opening.open) return;
    if (reveal && !motion.matches) document.querySelector('.film-hero')?.classList.add('is-revealing');
    opening.close();
    document.documentElement.classList.remove('opening-active');
    if (reveal && !url.hash) document.getElementById('intro-title')?.focus({preventScroll: true});
  }
  function enterSite() {
    if (!opening.open || opening.classList.contains('is-turning')) return;
    clearTimeout(advanceTimer);
    opening.classList.add('is-turning');
    if (motion.matches) finish();
    else exitTimer = setTimeout(finish, 950);
  }

  opening.showModal();
  document.documentElement.classList.add('opening-active');
  advanceTimer = setTimeout(enterSite, motion.matches ? 850 : 2300);
  enter.addEventListener('click', enterSite);
  let start = null;
  enter.addEventListener('pointerdown', event => {
    start = {x: event.clientX, y: event.clientY};
    enter.setPointerCapture(event.pointerId);
  });
  enter.addEventListener('pointermove', event => {
    if (start && Math.hypot(event.clientX - start.x, event.clientY - start.y) > 12) enterSite();
  });
  enter.addEventListener('lostpointercapture', () => { start = null; });
  opening.querySelector('.skip-opening').addEventListener('click', () => finish());
  opening.addEventListener('cancel', event => { event.preventDefault(); finish(); });
  motion.addEventListener('change', () => { if (motion.matches) finish(); });
  window.addEventListener('pagehide', () => finish(false), {once: true});
})();
