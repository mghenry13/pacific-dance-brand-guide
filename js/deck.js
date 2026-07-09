/* WildPath Brand Deck — 16:9 stage scaler + slide navigation */
(function () {
  const deck    = document.getElementById('deck');
  const slides  = Array.from(deck.querySelectorAll('.slide'));
  const curEl   = document.getElementById('cur');
  const totalEl = document.getElementById('total');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  const progEl  = document.getElementById('progress');
  const hint    = document.getElementById('hint');

  const STAGE_W = 1280, STAGE_H = 720;
  let i = slides.findIndex(s => s.classList.contains('is-active'));
  if (i < 0) i = 0;

  totalEl.textContent = String(slides.length).padStart(2, '0');

  /* ---- scale the fixed stage to fit the viewport (with a small margin) ---- */
  function fit() {
    const margin = 0.92;
    const s = Math.min(window.innerWidth / STAGE_W, window.innerHeight / STAGE_H) * margin;
    document.documentElement.style.setProperty('--scale', s.toFixed(4));
  }

  function show(n) {
    n = Math.max(0, Math.min(slides.length - 1, n));
    if (n === i) { return; }
    slides[i].classList.remove('is-active');
    i = n;
    slides[i].classList.add('is-active');
    render();
  }

  function render() {
    curEl.textContent = String(i + 1).padStart(2, '0');
    progEl.style.width = ((i + 1) / slides.length * 100) + '%';
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i === slides.length - 1;
  }

  const next = () => show(i + 1);
  const prev = () => show(i - 1);

  /* ---- input ---- */
  let hinted = false;
  function killHint() { if (!hinted) { hinted = true; hint && hint.classList.add('gone'); } }

  document.addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ': case 'Spacebar':
        e.preventDefault(); next(); killHint(); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp':
        e.preventDefault(); prev(); killHint(); break;
      case 'Home': e.preventDefault(); show(0); killHint(); break;
      case 'End':  e.preventDefault(); show(slides.length - 1); killHint(); break;
      case 'f': case 'F':
        if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
        else document.exitFullscreen?.();
        break;
    }
  });

  nextBtn.addEventListener('click', () => { next(); killHint(); });
  prevBtn.addEventListener('click', () => { prev(); killHint(); });

  /* in-deck jump links: any element with data-goto="<slide id>" */
  document.addEventListener('click', (e) => {
    const g = e.target.closest('[data-goto]');
    if (!g) return;
    e.preventDefault();
    e.stopPropagation();
    const idx = slides.findIndex(s => s.id === g.getAttribute('data-goto'));
    if (idx >= 0) { show(idx); killHint(); }
  }, true);

  /* advance on click in the letterbox area (not on the slide content or links/buttons) */
  document.addEventListener('click', (e) => {
    if (e.target.closest('.slide') || e.target.closest('.chrome') || e.target.closest('a,button')) return;
    next(); killHint();
  });

  window.addEventListener('resize', fit, { passive: true });

  /* deep links: #<slide id> opens that slide (e.g. #q1, #hub) */
  function gotoHash() {
    const id = location.hash.slice(1);
    if (!id) return;
    const idx = slides.findIndex(s => s.id === id);
    if (idx >= 0) { show(idx); killHint(); }
  }
  window.addEventListener('hashchange', gotoHash);

  fit();
  render();
  gotoHash();
})();
