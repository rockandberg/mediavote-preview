/* ==========================================================================
   MEDIA VOTE — Interactions
   Défilement natif, ressorts pour le mouvement,
   navigation / FAQ / formulaires pour l'usage.
   Tout le contenu reste accessible et lisible sans JavaScript.
   ========================================================================== */
/* Lenis a été retiré : son défilement piloté en JavaScript rendait la
   navigation lente et parfois bloquée. Le défilement natif du navigateur
   est instantané, fiable, et fonctionne avec toutes les technologies
   d'assistance. */

document.documentElement.classList.add('js');

const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const canHover = () => innerWidth > 768;

/* ==========================================================================
   Grille rem adaptative — mise à l'échelle au-delà de 1920px
   ========================================================================== */
const FONT_BASE = 16, BASE_W = 1920, COEF = 0.6666;
function setRootSize() {
  const reduction = ((BASE_W - innerWidth) / BASE_W) * 100 * COEF;
  const size = FONT_BASE - (FONT_BASE * reduction) / 100;
  if (size > FONT_BASE) document.documentElement.style.fontSize = size + 'px';
  else document.documentElement.style.removeProperty('font-size');
}
setRootSize();
addEventListener('resize', setRootSize);

/* ==========================================================================
   Ressorts et interpolations, intégrés dans une seule boucle rAF
   ========================================================================== */
const springs = new Set();
function spring(from, cfg, apply) {
  const s = { x: from, v: 0, target: from, t: cfg.tension, f: cfg.friction, apply };
  s.to = (v) => { s.target = v; };
  springs.add(s); apply(from); return s;
}

const easeOutExpo    = t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
const easeOutQuart   = t => 1 - Math.pow(1 - t, 4);
const easeInOutCubic = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

const tweens = new Set();
function tween({ from = 0, to = 1, duration = 800, delay = 0, easing = easeOutExpo, apply, done }) {
  const tw = { from, to, duration: REDUCED ? 1 : duration, delay: REDUCED ? 0 : delay, easing, apply, done, elapsed: 0 };
  apply(from); tweens.add(tw); return tw;
}

/* ==========================================================================
   Défilement
   ========================================================================== */
/* Verrouillage du défilement : on fige la position sans faire sauter la page. */
let lockCount = 0, savedScroll = 0;
function lockScroll() {
  if (lockCount++ === 0) {
    savedScroll = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${savedScroll}px`;
    document.body.style.width = '100%';
  }
}
function unlockScroll() {
  lockCount = Math.max(0, lockCount - 1);
  if (lockCount === 0) {
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    window.scrollTo(0, savedScroll);
  }
}

let last = performance.now();
function raf(time) {
  const ms = Math.min(64, time - last); last = time;

  for (const tw of [...tweens]) {
    tw.elapsed += ms;
    const t = tw.elapsed - tw.delay;
    if (t < 0) continue;
    const p = Math.min(1, t / tw.duration);
    tw.apply(tw.from + (tw.to - tw.from) * tw.easing(p));
    if (p === 1) { tweens.delete(tw); tw.done && tw.done(); }
  }

  const dt = ms / 1000;
  for (const s of springs) {
    if (REDUCED) { if (s.x !== s.target) { s.x = s.target; s.v = 0; s.apply(s.x); } continue; }
    const a = -s.t * (s.x - s.target) - s.f * s.v;
    s.v += a * dt; s.x += s.v * dt;
    if (Math.abs(s.x - s.target) < 0.0004 && Math.abs(s.v) < 0.0004) { s.x = s.target; s.v = 0; }
    s.apply(s.x);
  }

  parallaxFrame();
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);
scrollTo(0, 0);

/* ==========================================================================
   Primitives de révélation
   ========================================================================== */
function splitWords(el, text) {
  el.textContent = '';
  const words = text.split(' ');
  return words.map((w, i) => {
    const clip = document.createElement('span'); clip.className = 'clip';
    const inner = document.createElement('span'); inner.textContent = w;
    clip.appendChild(inner); el.appendChild(clip);
    if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    return inner;
  });
}
function buildLines(el, spec) {
  el.textContent = '';
  return spec.split('|').map(line => {
    const clip = document.createElement('span'); clip.className = 'clip clip--line';
    const inner = document.createElement('span'); inner.textContent = line;
    clip.appendChild(inner); el.appendChild(clip);
    return inner;
  });
}
function revealSpans(spans, { stagger = 55, duration = 520, delay = 0, easing = easeOutExpo } = {}) {
  spans.forEach((s, i) => tween({
    duration, delay: delay + i * stagger, easing,
    apply: v => { s.style.transform = `translateY(${(1 - v) * 115}%)`; s.style.opacity = v; }
  }));
}
function observeOnce(el, fn) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { fn(); io.disconnect(); } });
  }, { threshold: .12, rootMargin: '0px 0px -5% 0px' });
  io.observe(el);
}

/* Titres à lignes empilées */
document.querySelectorAll('[data-lines]').forEach(el => {
  const spans = buildLines(el, el.dataset.lines);
  if (el.hasAttribute('data-gated')) { el._spans = spans; return; }
  observeOnce(el, () => revealSpans(spans, { stagger: 55, duration: 520 }));
});

/* Corps de texte révélé mot à mot */
document.querySelectorAll('[data-words]').forEach(el => {
  const text = el.textContent.trim();
  el.textContent = '';
  const spans = text.split(' ').map((w, i, arr) => {
    const s = document.createElement('span'); s.className = 'wordfade'; s.textContent = w;
    el.appendChild(s); if (i < arr.length - 1) el.appendChild(document.createTextNode(' '));
    return s;
  });
  observeOnce(el, () => spans.forEach((s, i) => tween({
    duration: 380, delay: 100 + i * 12, easing: easeOutQuart,
    apply: v => { s.style.transform = `translateY(${(1 - v) * 18}px)`; s.style.opacity = v; }
  })));
});

/* Révélation générique à l'entrée dans le viewport */
/* Tensions relevees et amplitudes reduites : les valeurs du template
   d'origine mettaient pres d'une seconde a se stabiliser. */
const FROM = {
  rise:       { y: 26, scale: 1,   cfg: { tension: 420, friction: 30 } },
  'rise-sm':  { y: 18, scale: 1,   cfg: { tension: 440, friction: 30 } },
  'rise-lg':  { y: 32, scale: .96, cfg: { tension: 400, friction: 30 } },
  scale:      { y: 0,  scale: .94, cfg: { tension: 460, friction: 28 } },
  'scale-sm': { y: 0,  scale: .92, cfg: { tension: 480, friction: 28 } },
  def:        { y: 20, scale: 1,   cfg: { tension: 440, friction: 30 } }
};
document.querySelectorAll('.inview').forEach(el => {
  const f = FROM[el.dataset.from] || FROM.def;
  const delay = +(el.dataset.delay || 0);
  el.style.opacity = 0;
  el.style.transform = `translateY(${f.y}px) scale(${f.scale})`;
  const play = () => setTimeout(() => {
    spring(0, f.cfg, v => {
      el.style.opacity = v;
      el.style.transform = `translateY(${(1 - v) * f.y}px) scale(${f.scale + (1 - f.scale) * v})`;
    }).to(1);
  }, REDUCED ? 0 : delay);
  if (el.hasAttribute('data-gated')) el._play = play;
  else observeOnce(el, play);
});

/* ==========================================================================
   Parallaxe liée au défilement
   ========================================================================== */
const parallaxItems = [];
function addParallax(el, from, to, axis = 'y') {
  const host = el.closest('section, header, .hero') || el;
  parallaxItems.push({ el, from, to, axis, host });
}
function parallaxFrame() {
  if (REDUCED) return;
  for (const p of parallaxItems) {
    const r = p.host.getBoundingClientRect();
    if (r.bottom < -200 || r.top > innerHeight + 200) continue;
    const t = Math.min(1, Math.max(0, (innerHeight - r.top) / (innerHeight + r.height)));
    const v = p.from + (p.to - p.from) * t;
    p.el.style.transform = p.axis === 'y' ? `translateY(${v}%)` : `translateX(${v}%)`;
  }
}
const heroPlate = document.querySelector('.hero__plate-inner');
if (heroPlate) addParallax(heroPlate, 0, 12, 'y');

const ghostWords = [...document.querySelectorAll('.ghost-w')];
/* Amplitudes réduites par rapport au template : en français les mots sont
   plus longs et sortaient du conteneur, qui est en overflow-x: clip. */
[[-1.5, 1.5], [1.5, -1.5], [-1, 2], [2, -1.5]].forEach((pair, i) => {
  if (ghostWords[i]) addParallax(ghostWords[i], pair[0], pair[1], 'x');
});

/* Mots surdimensionnés — révélation au scroll */
const ghostHost = document.querySelector('.ghost-h');
if (ghostHost) {
  const spans = ghostWords.map(w => {
    const t = w.textContent.trim();
    return splitWords(w, t);
  }).flat();
  observeOnce(ghostHost, () => revealSpans(spans, { stagger: 60, duration: 700 }));
}

/* ==========================================================================
   Ajustement du titre géant à la largeur réelle du conteneur
   Une valeur vw fixe déborde dès que la langue allonge les mots.
   ========================================================================== */
function fitDisplay() {
  document.querySelectorAll('.hero__display').forEach(el => {
    const host = el.parentElement;
    const cs = getComputedStyle(host);
    const avail = host.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 2;
    let vw = 11, guard = 0;
    el.style.fontSize = vw + 'vw';
    /* offsetWidth et non scrollWidth : l'élément est inline-block,
       sa largeur suit donc réellement celle du texte. */
    while (el.offsetWidth > avail && vw > 3 && guard++ < 120) {
      vw -= 0.1;
      el.style.fontSize = vw + 'vw';
    }
  });
}
fitDisplay();
addEventListener('resize', fitDisplay);

/* ==========================================================================
   Micro-interactions au survol — désactivées ≤768px
   ========================================================================== */
function hoverSpring(el, cfg, apply, trigger) {
  const s = spring(0, cfg, apply);
  const host = trigger || el;
  host.addEventListener('pointerenter', () => canHover() && s.to(1));
  host.addEventListener('pointerleave', () => s.to(0));
  host.addEventListener('focusin', () => s.to(1));
  host.addEventListener('focusout', () => s.to(0));
  return s;
}

document.querySelectorAll('.numlist a').forEach(row => {
  const arrow = row.querySelector('.numlist__arrow');
  if (!arrow) return;
  hoverSpring(arrow, { tension: 520, friction: 24 }, v => {
    arrow.style.transform = `translateX(${8 * v}px)`;
    arrow.style.opacity = .55 + .45 * v;
  }, row);
});

document.querySelectorAll('.card').forEach(card => {
  hoverSpring(card, { tension: 520, friction: 26 }, v => { card.style.translate = `0 ${-6 * v}px`; });
});

document.querySelectorAll('.tile').forEach(tile => {
  const media = tile.querySelector('.tile__media');
  if (!media) return;
  const s = spring(1, { tension: 520, friction: 26 }, v => { media.style.transform = `scale(${v})`; });
  tile.addEventListener('pointerenter', () => canHover() && s.to(1.03));
  tile.addEventListener('pointerleave', () => s.to(1));
});

document.querySelectorAll('.btn svg, .arrowbtn svg').forEach(svg => {
  const btn = svg.closest('.btn, .arrowbtn');
  const isArrow = btn.classList.contains('arrowbtn');
  const flip = btn.classList.contains('arrowbtn--prev') ? -1 : 1;
  hoverSpring(svg, { tension: 560, friction: isArrow ? 22 : 24 }, v => {
    svg.style.transform = isArrow ? `scaleX(${flip}) scale(${1 + .15 * v})` : `translateX(${5 * v}px)`;
  }, btn);
});

document.querySelectorAll('.iconbtn svg').forEach(svg => {
  hoverSpring(svg, { tension: 520, friction: 22 }, v => { svg.style.transform = `rotate(${90 * v}deg)`; }, svg.closest('.iconbtn'));
});

/* ==========================================================================
   Défilement doux vers les ancres
   ========================================================================== */
document.addEventListener('click', e => {
  const a = e.target.closest('a[href^="#"]');
  if (!a) return;
  const id = a.getAttribute('href');
  if (!id || id === '#') return;
  const target = document.querySelector(id);
  if (!target) return;
  e.preventDefault();
  target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  target.setAttribute('tabindex', '-1');
  target.focus({ preventScroll: true });
});

/* ==========================================================================
   Header — se masque en descendant, réapparaît en remontant
   ========================================================================== */
let menuOpen = false, menuReturn = null;
const siteHeader = document.querySelector('.site-header');
if (siteHeader) {
  let lastY = window.scrollY, ticking = false;
  const HIDE_AFTER = 160;   /* on ne masque pas dans le haut de page */

  const update = () => {
    const y = window.scrollY;
    const goingDown = y > lastY;

    /* Fond opaque dès qu'on quitte le haut : le header était illisible
       par-dessus les sections claires. */
    siteHeader.classList.toggle('is-solid', y > 24);

    if (menuOpen) { siteHeader.classList.remove('is-hidden'); }
    else if (goingDown && y > HIDE_AFTER) siteHeader.classList.add('is-hidden');
    else siteHeader.classList.remove('is-hidden');

    lastY = y; ticking = false;
  };

  addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });

  /* Le header doit réapparaître dès qu'un élément y prend le focus au clavier */
  siteHeader.addEventListener('focusin', () => siteHeader.classList.remove('is-hidden'));
  update();
}

/* ==========================================================================
   Sous-menus de navigation
   ========================================================================== */
const navToggles = document.querySelectorAll('.nav__toggle');
function closeAllSubmenus(except) {
  navToggles.forEach(btn => {
    if (btn === except) return;
    btn.setAttribute('aria-expanded', 'false');
    const panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (panel) panel.hidden = true;
  });
}
navToggles.forEach(btn => {
  const panel = document.getElementById(btn.getAttribute('aria-controls'));
  if (!panel) return;
  panel.hidden = true;

  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    closeAllSubmenus(btn);
    btn.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
  });

  const item = btn.closest('.nav__item');
  let timer;
  if (item && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    item.addEventListener('mouseenter', () => {
      clearTimeout(timer); closeAllSubmenus(btn);
      btn.setAttribute('aria-expanded', 'true'); panel.hidden = false;
    });
    item.addEventListener('mouseleave', () => {
      timer = setTimeout(() => { btn.setAttribute('aria-expanded', 'false'); panel.hidden = true; }, 200);
    });
  }
});
document.addEventListener('click', e => { if (!e.target.closest('.nav__item')) closeAllSubmenus(null); });

/* ==========================================================================
   Menu plein écran
   ========================================================================== */
const mobileNav = document.getElementById('mobile-nav');
const openBtn = document.querySelector('.nav-toggle');
const mobileLinks = mobileNav ? [...mobileNav.querySelectorAll('.mobile-nav__link, .mobile-nav__toggle')] : [];
menuOpen = false; menuReturn = null;

let menuBdSpring, menuPanelSpring;
if (mobileNav) {
  const bd = mobileNav.querySelector('.mobile-nav__bd');
  const panel = mobileNav.querySelector('.mobile-nav__panel');
  menuBdSpring = spring(0, { tension: 520, friction: 34 }, v => { bd.style.opacity = v; });
  menuPanelSpring = spring(0, { tension: 460, friction: 32 }, v => {
    panel.style.opacity = v; panel.style.transform = `translateY(${(1 - v) * -24}px)`;
  });
}

function openMenu() {
  if (!mobileNav || menuOpen) return;
  menuOpen = true; menuReturn = document.activeElement;
  mobileNav.hidden = false; mobileNav.classList.add('is-open');
  openBtn.setAttribute('aria-expanded', 'true');
  lockScroll();
  menuBdSpring.to(1); menuPanelSpring.to(1);
  mobileLinks.forEach((l, i) => {
    l.style.opacity = 0; l.style.transform = 'translateY(28px)';
    const s = spring(0, { tension: 460, friction: 30 }, v => {
      l.style.opacity = v; l.style.transform = `translateY(${(1 - v) * 20}px)`;
    });
    setTimeout(() => s.to(1), REDUCED ? 0 : 50 + i * 28);
  });
  setTimeout(() => { const c = mobileNav.querySelector('button.mobile-nav__close'); c && c.focus(); }, 60);
}
function closeMenu() {
  if (!mobileNav || !menuOpen) return;
  menuOpen = false;
  openBtn.setAttribute('aria-expanded', 'false');
  menuBdSpring.to(0); menuPanelSpring.to(0);
  mobileNav.classList.remove('is-open');
  setTimeout(() => { mobileNav.hidden = true; }, REDUCED ? 0 : 200);
  unlockScroll();
  menuReturn && menuReturn.focus();
}
if (openBtn) openBtn.addEventListener('click', openMenu);
document.querySelectorAll('.mobile-nav__close').forEach(b => b.addEventListener('click', closeMenu));
document.querySelectorAll('.mobile-nav__link, .mobile-nav__sub a').forEach(l =>
  l.addEventListener('click', () => setTimeout(closeMenu, 10)));

document.querySelectorAll('.mobile-nav__toggle').forEach(btn => {
  const panel = document.getElementById(btn.getAttribute('aria-controls'));
  if (!panel) return;
  panel.hidden = true;
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
  });
});

/* Échap + piège de focus */
addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (menuOpen) { closeMenu(); return; }
    const openSub = document.querySelector('.nav__toggle[aria-expanded="true"]');
    if (openSub) { closeAllSubmenus(null); openSub.focus(); }
    return;
  }
  if (e.key !== 'Tab' || !menuOpen) return;
  const host = mobileNav.querySelector('.mobile-nav__panel');
  const f = [...host.querySelectorAll('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])')]
    .filter(el => el.offsetParent !== null);
  if (!f.length) return;
  const first = f[0], lastEl = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); lastEl.focus(); }
  else if (!e.shiftKey && document.activeElement === lastEl) { e.preventDefault(); first.focus(); }
});

/* ==========================================================================
   FAQ — ouverture indépendante
   ========================================================================== */
document.querySelectorAll('.faq__button').forEach(btn => {
  const panel = document.getElementById(btn.getAttribute('aria-controls'));
  if (!panel) return;
  panel.hidden = btn.getAttribute('aria-expanded') !== 'true';
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
  });
});

/* ==========================================================================
   Carrousel du hero
   ========================================================================== */
const sliderRoot = document.getElementById('hero-slider');
let restartAutoplay = () => {};
if (sliderRoot) {
  const SLIDES = JSON.parse(sliderRoot.dataset.slides);
  const card = sliderRoot.querySelector('.slider__card');
  const thumb = sliderRoot.querySelector('.slider__thumb');
  const brand = sliderRoot.querySelector('.slider__brand');
  const title = sliderRoot.querySelector('.slider__title');
  const cta = sliderRoot.querySelector('.slider__cta');
  const dots = sliderRoot.querySelector('.dots');
  let idx = 0, timer = null;

  const paint = i => {
    const s = SLIDES[i];
    brand.textContent = s.brand;
    title.textContent = s.title;
    cta.textContent = s.cta + ' →';
    cta.setAttribute('href', s.url);
    thumb.innerHTML = s.icon;
    [...dots.children].forEach((b, k) => b.setAttribute('aria-current', String(k === i)));
  };
  const render = (i, animate = true) => {
    if (!animate) { paint(i); return; }
    const s = spring(1, { tension: 480, friction: 30 }, v => {
      card.style.opacity = v;
      card.style.transform = `translateY(${(1 - v) * 16}px) scale(${.96 + .04 * v})`;
    });
    s.to(0);
    setTimeout(() => { paint(i); s.to(1); }, REDUCED ? 0 : 110);
  };
  SLIDES.forEach((_, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.setAttribute('role', 'tab');
    b.setAttribute('aria-label', `Solution ${i + 1} sur ${SLIDES.length}`);
    b.innerHTML = '<i></i>';
    b.addEventListener('click', () => { idx = i; render(i); restartAutoplay(); });
    dots.appendChild(b);
  });
  paint(0);
  restartAutoplay = () => {
    clearInterval(timer);
    timer = setInterval(() => { idx = (idx + 1) % SLIDES.length; render(idx); }, 3800);
  };
}

/* ==========================================================================
   Formulaires — validation à la soumission, aucun envoi simulé
   ========================================================================== */
const MESSAGES = {
  required: name => 'Merci de renseigner ' + name + '.',
  email: 'Cette adresse e-mail ne semble pas valide. Vérifiez qu’elle contient un @ et un nom de domaine.',
  tel: 'Ce numéro ne semble pas valide. Format attendu : 01 23 45 67 89.',
  select: name => 'Merci de sélectionner ' + name + '.',
  consent: 'Merci de confirmer votre accord pour être recontacté.'
};
/* Le libellé d'erreur vient de data-error-name, pas du <label> : un libellé
   comme « Votre organisation » produirait « renseigner votre votre organisation ». */
function fieldName(field) {
  const explicit = field.getAttribute('data-error-name');
  if (explicit) return explicit;
  const lbl = document.querySelector(`label[for="${field.id}"]`);
  return lbl ? 'le champ « ' + lbl.textContent.replace('*', '').trim() + ' »' : 'ce champ';
}
function setError(field, message) {
  const box = document.getElementById(field.id + '-error');
  if (!box) return;
  box.textContent = message || '';
  field.setAttribute('aria-invalid', message ? 'true' : 'false');
}
function validateField(field) {
  const value = (field.value || '').trim();
  const name = fieldName(field);
  if (field.type === 'checkbox') {
    if (field.required && !field.checked) { setError(field, MESSAGES.consent); return false; }
    setError(field, ''); return true;
  }
  if (field.required && !value) {
    setError(field, field.tagName === 'SELECT' ? MESSAGES.select(name) : MESSAGES.required(name));
    return false;
  }
  if (field.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) { setError(field, MESSAGES.email); return false; }
  if (field.type === 'tel' && value && !/^[+0-9\s().-]{9,20}$/.test(value)) { setError(field, MESSAGES.tel); return false; }
  setError(field, ''); return true;
}

document.querySelectorAll('form[data-validate]').forEach(form => {
  const fields = form.querySelectorAll('.form__control, .form__consent input');
  fields.forEach(field => field.addEventListener('blur', () => {
    if (field.getAttribute('aria-invalid') === 'true' || (field.value || '').trim()) validateField(field);
  }));

  form.addEventListener('submit', e => {
    e.preventDefault();
    let valid = true, firstInvalid = null;
    fields.forEach(field => {
      if (!validateField(field)) { valid = false; if (!firstInvalid) firstInvalid = field; }
    });
    const status = form.querySelector('[data-form-status]');
    if (!valid) {
      if (status) status.textContent = 'Le formulaire comporte des erreurs. Vérifiez les champs signalés.';
      if (firstInvalid) firstInvalid.focus();
      return;
    }
    /* Aucun endpoint validé (Q-B8) : la soumission n'est pas simulée. */
    if (status) {
      status.textContent =
        'Le formulaire est complet et valide. L’envoi n’est pas encore raccordé : ' +
        'la destination technique est en attente de validation. ' +
        'En attendant, écrivez-nous à contact@media-vote.com ou appelez le 01 47 08 55 13.';
    }
  });
});

/* ==========================================================================
   Rideau de chargement
   ========================================================================== */
const MIN_VISIBLE_MS = REDUCED ? 150 : 620;
const MAX_VISIBLE_MS = 1500;
const EXIT_MS = REDUCED ? 1 : 420;
const loader = document.querySelector('.mv-loader');

if (loader) {
  lockScroll();
  const mark = loader.querySelector('.mv-loader__mark');
  const fill = loader.querySelector('.mv-loader__fill');
  mark.style.opacity = 0;
  spring(0, { tension: 480, friction: 28 }, v => {
    mark.style.opacity = v; mark.style.transform = `translateY(${(1 - v) * 12}px)`;
  }).to(1);
  tween({ duration: Math.max(1, MIN_VISIBLE_MS - 60), delay: 60, easing: easeInOutCubic,
    apply: v => { fill.style.transform = `scaleX(${v})`; } });

  let started = false;
  const finish = () => {
    if (started) return; started = true;

    /* ready = true : les éléments gated s'animent */
    document.querySelectorAll('[data-gated]').forEach(el => {
      if (el._play) { el._play(); return; }
      if (el.classList.contains('hero__display')) {
        const spans = splitWords(el, el.textContent.trim());
        fitDisplay();
        revealSpans(spans, { stagger: 70, duration: 620 });
        return;
      }
      if (el._spans) revealSpans(el._spans, { stagger: 55, duration: 520, delay: 140 });
    });

    restartAutoplay();
    unlockScroll();
    tween({ duration: EXIT_MS, easing: easeInOutCubic,
      apply: v => { loader.style.transform = `translateY(${-105 * v}%)`; },
      done: () => loader.remove() });
  };
  const arm = () => setTimeout(finish, MIN_VISIBLE_MS);
  if (document.readyState === 'complete') arm(); else addEventListener('load', arm);
  setTimeout(finish, MAX_VISIBLE_MS);
} else {
  /* Pages sans rideau : on joue immédiatement les éléments gated */
  document.querySelectorAll('[data-gated]').forEach(el => {
    if (el._play) el._play();
    else if (el._spans) revealSpans(el._spans, { stagger: 55, duration: 520 });
  });
}
