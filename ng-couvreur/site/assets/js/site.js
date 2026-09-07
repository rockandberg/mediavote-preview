/* NG Couvreur — interactions. Discrètes, sans dépendance. */
(function () {
  'use strict';
  document.documentElement.classList.remove('no-js');
  document.documentElement.classList.add('js');

  /* --- Menu mobile ------------------------------------------------------ */
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('menu-mobile');

  function closeDrawer() {
    if (!burger || !drawer) return;
    burger.setAttribute('aria-expanded', 'false');
    drawer.setAttribute('data-open', 'false');
    document.body.style.overflow = '';
  }

  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      drawer.setAttribute('data-open', String(!open));
      document.body.style.overflow = open ? '' : 'hidden';
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeDrawer();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeDrawer();
    });
    // Repasser en desktop referme et rend le scroll
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1024) closeDrawer();
    });
  }

  /* --- Apparition au scroll --------------------------------------------- */
  var targets = document.querySelectorAll('.reveal');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!targets.length) {
    /* rien à faire */
  } else if (reduced || !('IntersectionObserver' in window)) {
    for (var i = 0; i < targets.length; i++) targets[i].classList.add('is-in');
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  }

  /* --- Formulaire de devis ---------------------------------------------- */
  var form = document.querySelector('form[data-devis]');
  if (!form) return;

  var notice = form.querySelector('[data-notice]');

  function fieldWrap(el) { return el.closest('.field'); }

  function setError(el, message) {
    var wrap = fieldWrap(el);
    if (!wrap) return;
    wrap.classList.add('field--err');
    var slot = wrap.querySelector('.err');
    if (slot) { slot.textContent = message; }
    el.setAttribute('aria-invalid', 'true');
  }

  function clearError(el) {
    var wrap = fieldWrap(el);
    if (!wrap) return;
    wrap.classList.remove('field--err');
    var slot = wrap.querySelector('.err');
    if (slot) { slot.textContent = ''; }
    el.removeAttribute('aria-invalid');
  }

  function validate(el) {
    var v = (el.value || '').trim();
    if (el.hasAttribute('required') && !v) {
      setError(el, 'Ce champ est nécessaire pour vous répondre.');
      return false;
    }
    if (el.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
      setError(el, 'Vérifiez votre adresse e-mail.');
      return false;
    }
    if (el.type === 'tel' && v && v.replace(/[^0-9]/g, '').length < 9) {
      setError(el, 'Vérifiez votre numéro de téléphone.');
      return false;
    }
    clearError(el);
    return true;
  }

  var controls = form.querySelectorAll('input, select, textarea');
  controls.forEach(function (el) {
    el.addEventListener('blur', function () { validate(el); });
    el.addEventListener('input', function () {
      if (fieldWrap(el) && fieldWrap(el).classList.contains('field--err')) validate(el);
    });
  });

  form.addEventListener('submit', function (e) {
    var ok = true;
    var first = null;
    controls.forEach(function (el) {
      if (!validate(el) && ok) { ok = false; first = el; }
      else if (!validate(el)) { /* déjà signalé */ }
    });

    if (!ok) {
      e.preventDefault();
      if (first) { first.focus(); }
      return;
    }

    /* Tant que l'endpoint n'est pas configuré, on ne simule pas un envoi :
       on le dit et on renvoie vers le téléphone. */
    var action = form.getAttribute('action') || '';
    if (action.indexOf('REMPLACER') !== -1 || action === '') {
      e.preventDefault();
      if (notice) {
        notice.hidden = false;
        notice.focus();
        notice.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
      }
    }
  });
})();
