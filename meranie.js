/* ============================================================
   HROM — server-side ready meranie
   ------------------------------------------------------------
   Čo to robí:
   1. Zachytí a ULOŽÍ reklamné click ID (gclid, fbclid, msclkid…)
      → bez toho sa rezervácia, ktorá príde o 3 dni, nedá priradiť
        ku kampani.
   2. Vytvorí a udrží first-party ID návštevníka (cookie, 1st party).
   3. Ku každej udalosti dá event_id → deduplikácia medzi
      prehliadačom a serverom (Meta CAPI / GA4 MP to vyžadujú).
   4. Pushne čisté udalosti do dataLayer (zoberie ich tvoj GTM).
   5. Ak vyplníš ENDPOINT nižšie, pošle udalosť aj priamo na server
      (server-side GTM) — čiže meranie nezávislé od adblockov a ITP.

   NASADENIE: na každú stránku pred </body> pridaj:
      <script src="meranie.js" defer></script>
   ============================================================ */
(function () {
  'use strict';

  /* ---------- KONFIGURÁCIA (vyplň) ---------------------------- */
  var CFG = {
    // URL tvojho server-side GTM kontajnera, napr. 'https://sgtm.hrom.marketing'
    // Nechaj prázdne = posiela sa len do dataLayer (bezpečné, nič sa nerozbije).
    ENDPOINT: '',
    // Cesta na server kontajneri, kam sa posielajú udalosti
    PATH: '/mp/collect',
    // Doména pre first-party cookie (necháva sa prázdne = aktuálna doména)
    COOKIE_DOMAIN: '',
    // Posielať e-mail z formulára na server (pre Enhanced Conversions / CAPI)?
    // Server ho MUSÍ zahashovať (SHA-256). Zapni len ak máš na to súhlas.
    SEND_USER_DATA: false,
    DEBUG: false
  };
  /* ------------------------------------------------------------ */

  var DAY = 864e5;
  window.dataLayer = window.dataLayer || [];

  /* ---------- pomocné ---------- */
  function log() { if (CFG.DEBUG && window.console) console.log.apply(console, ['[HROM meranie]'].concat([].slice.call(arguments))); }

  function setCookie(name, value, days) {
    var d = new Date(Date.now() + days * DAY);
    var dom = CFG.COOKIE_DOMAIN ? '; domain=' + CFG.COOKIE_DOMAIN : '';
    document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + d.toUTCString() +
                      '; path=/' + dom + '; SameSite=Lax' + (location.protocol === 'https:' ? '; Secure' : '');
  }
  function getCookie(name) {
    var m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : '';
  }
  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
  function param(n) { return new URLSearchParams(location.search).get(n) || ''; }

  /* ---------- 1) identita návštevníka (first-party) ---------- */
  var clientId = getCookie('hrom_cid');
  if (!clientId) { clientId = uuid(); }
  setCookie('hrom_cid', clientId, 400);           // obnovuje sa pri každej návšteve

  var sessionId = sessionStorage.getItem('hrom_sid');
  if (!sessionId) { sessionId = uuid(); try { sessionStorage.setItem('hrom_sid', sessionId); } catch (e) {} }

  /* ---------- 2) reklamné click ID + zdroj návštevy ----------
     Kľúčové pre "booking ads": rezervácia často príde neskôr a inde,
     preto si click ID držíme 90 dní a posielame ho s konverziou.    */
  var CLICK_IDS = ['gclid', 'gbraid', 'wbraid', 'fbclid', 'msclkid', 'ttclid', 'li_fat_id'];
  CLICK_IDS.forEach(function (k) {
    var v = param(k);
    if (v) setCookie('hrom_' + k, v, 90);
  });
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
    var v = param(k);
    if (v) setCookie('hrom_' + k, v, 90);
  });

  function attribution() {
    var a = { client_id: clientId, session_id: sessionId, page_location: location.href, page_title: document.title };
    CLICK_IDS.concat(['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']).forEach(function (k) {
      var v = getCookie('hrom_' + k); if (v) a[k] = v;
    });
    if (document.referrer && document.referrer.indexOf(location.hostname) === -1) a.page_referrer = document.referrer;
    return a;
  }

  /* ---------- 3) odoslanie udalosti ---------- */
  function track(name, params) {
    var payload = Object.assign({ event: name, event_id: uuid(), event_time: Math.floor(Date.now() / 1000) },
                                attribution(), params || {});
    dataLayer.push(payload);                       // → klientský GTM
    log(name, payload);

    if (CFG.ENDPOINT) {                            // → server-side kontajner
      try {
        var body = JSON.stringify(payload);
        var url = CFG.ENDPOINT.replace(/\/$/, '') + CFG.PATH;
        if (navigator.sendBeacon) navigator.sendBeacon(url, new Blob([body], { type: 'application/json' }));
        else fetch(url, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'application/json' }, mode: 'no-cors' });
      } catch (e) { log('chyba odoslania', e); }
    }
    return payload.event_id;
  }
  window.hromTrack = track;                        // dá sa volať aj ručne

  /* ---------- 4) automatické udalosti ---------- */

  // 4a) REZERVÁCIE / DEMO — jadro merania "booking ads"
  var BOOKING_HOSTS = /(reservio\.com|entradio\.sk|sterio\.sk|mamkrcovezily\.sk|ultrazvukove\w*\.sk|agnesoptik\.sk|optikavokel\.sk)/i;
  var BOOKING_PATHS = /(chatbot-demo|online-objednavka|rezervac|objednav|booking)/i;

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a || !a.getAttribute('href')) return;
    var href = a.getAttribute('href');
    var text = (a.textContent || '').trim().slice(0, 80);

    if (href.indexOf('tel:') === 0) {
      track('contact_call', { method: 'phone', link_url: href, link_text: text });

    } else if (href.indexOf('mailto:') === 0) {
      track('contact_email', { method: 'email', link_url: href, link_text: text });

    } else if (BOOKING_HOSTS.test(href) || BOOKING_PATHS.test(href)) {
      // klik smerujúci k rezervácii/demu = mikro-konverzia pre kampane
      track('booking_click', {
        link_url: a.href, link_text: text,
        destination: (function () { try { return new URL(a.href, location.href).hostname; } catch (e) { return ''; } })(),
        outbound: a.hostname !== location.hostname
      });

    } else if (a.hostname === location.hostname && /\.html$/.test(href) && href !== 'index.html') {
      track('select_service', { service_page: href.replace('.html', ''), link_text: text });
    }
  }, true);

  // 4b) ODOSLANIE FORMULÁRA = lead
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM') return;
    var d = {};
    try {
      var fd = new FormData(f);
      d.form_id = f.id || f.className || 'form';
      if (CFG.SEND_USER_DATA) {
        // server MUSÍ tieto údaje zahashovať (SHA-256) pred odoslaním do Meta/Google
        var em = fd.get('email'), tel = fd.get('telefon');
        if (em) d.user_data_email = String(em).trim().toLowerCase();
        if (tel) d.user_data_phone = String(tel).replace(/[^\d+]/g, '');
      }
    } catch (err) {}
    track('generate_lead', d);
  }, true);

  // 4c) HĹBKA SCROLLU (kvalita návštevy pre optimalizáciu kampaní)
  var hit = {};
  window.addEventListener('scroll', function () {
    var h = document.documentElement;
    var pct = Math.round((h.scrollTop + innerHeight) / h.scrollHeight * 100);
    [25, 50, 75, 90].forEach(function (p) {
      if (pct >= p && !hit[p]) { hit[p] = 1; track('scroll_depth', { percent: p }); }
    });
  }, { passive: true });

  // 4d) ZOBRAZENIE STRÁNKY
  track('page_view_hrom', {});
})();
