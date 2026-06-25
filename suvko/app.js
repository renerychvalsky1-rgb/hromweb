/* SUVKO podklad — drobná interaktivita */
(function () {
  // JS je dostupný → povolíme reveal animácie (bez JS ostáva obsah viditeľný)
  document.documentElement.classList.add('js');

  // mobilné menu
  var burger = document.querySelector('.nav-burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      links.classList.toggle('open');
      burger.classList.toggle('x');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { links.classList.remove('open'); });
    });
  }

  // rok v pätičke
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // reveal pri scrollovaní
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
    // failsafe nezávislý od load/fontov: po 1,5 s odkryjeme všetko, čo ešte nie je
    setTimeout(function () {
      reveals.forEach(function (el) { el.classList.add('in'); });
    }, 1500);
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // animácia progress barov (kondícia firmy)
  var bio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.fill').forEach(function (f) {
          f.style.width = (f.getAttribute('data-pct') || 0) + '%';
        });
        bio.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.bars').forEach(function (el) {
    el.querySelectorAll('.fill').forEach(function (f) { f.style.width = '0%'; });
    bio.observe(el);
  });
})();
