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

  /* --- Rattrapage des images déjà en erreur ------------------------------ */
  /* L'écouteur principal est en ligne dans le <head>, car ce script est
     différé et arrive après le chargement du hero. Ici on ne fait que
     rattraper celles qui auraient échoué sans déclencher le repli. */
  [].forEach.call(document.images, function (img) {
    if (img.complete && img.naturalWidth === 0 && !img.getAttribute('data-repli')) {
      img.setAttribute('data-repli', '1');
      var pic = img.parentNode;
      if (pic && pic.tagName === 'PICTURE') {
        var sources = pic.querySelectorAll('source');
        for (var i = 0; i < sources.length; i++) sources[i].parentNode.removeChild(sources[i]);
      }
      var jpg = img.getAttribute('src');
      img.removeAttribute('srcset');
      img.removeAttribute('sizes');
      if (jpg) { img.setAttribute('src', jpg + (jpg.indexOf('?') < 0 ? '?r=1' : '&r=1')); }
    }
  });

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

  var note = form.querySelector('[data-formnote]');

  /* --- Anti-robots ------------------------------------------------------ */
  /* L'adresse d'envoi n'est pas dans le HTML : on la reconstitue ici. Un
     robot qui n'exécute pas JavaScript ne trouve donc aucune cible. */
  var armed = false;
  try {
    var ep = form.getAttribute('data-ep');
    if (ep) {
      form.setAttribute('action', atob(ep));
      form.removeAttribute('data-ep');
      /* Le bouton n'est un bouton d'envoi qu'une fois l'adresse en place :
         sans JavaScript, il ne déclenche rien plutôt que d'envoyer le
         formulaire sur une page statique, qui répondrait par une erreur. */
      var btn = form.querySelector('[data-submit]');
      if (btn) { btn.setAttribute('type', 'submit'); }
      armed = true;
    }
  } catch (err) {
    armed = false;
  }

  /* Un humain ne remplit pas six champs en deux secondes. Un robot, si. */
  var openedAt = Date.now();
  var DELAI_MINIMUM = 3000;

  function refuser(message) {
    if (!note) return;
    note.innerHTML = message;
    note.hidden = false;
    note.focus();
  }


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
    /* Une case à cocher porte toujours une valeur : c'est son état coché
       qu'il faut lire, pas son value. Le formulaire étant en novalidate,
       le navigateur ne rattrape pas l'oubli. */
    if (el.type === 'checkbox') {
      if (el.hasAttribute('required') && !el.checked) {
        setError(el, 'Merci de cocher cette case pour que nous puissions vous répondre.');
        return false;
      }
      clearError(el);
      return true;
    }

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
    if (el.type === 'checkbox') {
      el.addEventListener('change', function () { validate(el); });
    }
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

    if (!armed || !form.getAttribute('action')) {
      e.preventDefault();
      refuser('<strong>L\'envoi est indisponible depuis ce navigateur.</strong> ' +
              'Appelez-nous au <a href="tel:+33744817945" style="font-weight:700">07 44 81 79 45</a>.');
      return;
    }

    if (Date.now() - openedAt < DELAI_MINIMUM) {
      e.preventDefault();
      refuser('<strong>Un instant.</strong> Relisez votre demande, puis renvoyez-la — ' +
              'cette courte pause nous protège des envois automatisés.');
      window.setTimeout(function () { if (note) { note.hidden = true; } }, 4000);
      return;
    }

    if (note) { note.hidden = true; }
  });
})();
