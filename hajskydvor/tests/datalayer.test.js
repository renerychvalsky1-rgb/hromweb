// Test meracích udalostí pre GTM (GTM-57KFFMZ4).
// Každý push pre booking_click, contact_click, reel_click a gallery_open musí obsahovať všetkých 5 kľúčov
// (portal, method, reel, photo, lang); nepoužité sú undefined, aby GTM neprenášal hodnoty z predchádzajúcej udalosti.
// Spustenie: NODE_PATH=$(npm root -g) node hajskydvor/tests/datalayer.test.js hajskydvor/v5.html
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const KEYS = ['portal', 'method', 'reel', 'photo', 'lang'];
const EXPECT = { booking_click: 'portal', contact_click: 'method', reel_click: 'reel', gallery_open: 'photo' };
const file = path.resolve(process.argv[2] || path.join(__dirname, '..', 'v5.html'));

(async () => {
  const html = fs.readFileSync(file, 'utf8');
  const fail = [];
  if (!html.includes("'GTM-57KFFMZ4'")) fail.push('chýba kontajner GTM-57KFFMZ4');
  if (/googletagmanager\.com\/gtag\/js/.test(html)) fail.push('web obsahuje gtag.js – GA4 má bežať len cez GTM');

  const b = await chromium.launch();
  const p = await b.newPage({ locale: 'sk-SK' });
  await p.route('**/*googletagmanager.com/**', r => r.abort());   // nič sa neodošle do Google
  await p.goto('file://' + file);
  await p.evaluate(() => document.querySelectorAll('a[target=_blank], a[href^="tel:"], a[href^="mailto:"]').forEach(a => a.addEventListener('click', e => e.preventDefault())));

  // cookie lišta: pred súhlasom je analytics_storage zamietnuté, po „Prijať všetky“ príde update granted
  const consentLog = () => p.evaluate(() => window.dataLayer.filter(e => e && e[0] === 'consent').map(e => e[1] + ':' + e[2].analytics_storage));
  const c0 = await consentLog();
  if (c0[0] !== 'default:denied' || c0.length !== 1) fail.push(`pred súhlasom má byť len default:denied, je ${c0.join(', ')}`);
  if (!(await p.isVisible('#ckBar'))) fail.push('cookie lišta sa pri prvej návšteve neukázala');
  await p.click('#ckBar [data-ck="accept"]');
  const c1 = await consentLog();
  if (c1[c1.length - 1] !== 'update:granted') fail.push('po „Prijať všetky“ chýba update:granted');
  if (await p.isVisible('#ckBar')) fail.push('lišta po súhlase nezmizla');
  console.log('cookies: pred súhlasom', c0.join(', '), '→ po súhlase', c1[c1.length - 1]);

  // poradie schválne strieda udalosti, aby sa ukázal prípadný prenos hodnôt
  await p.click('#galeria [data-open="kitchen"]'); await p.keyboard.press('Escape');
  await p.click('#bookCards [data-portal="booking"]');
  await p.click('#kontakt a[href^="tel:"]');
  await p.click('#reels .reel');
  await p.click('#kontakt a[href^="mailto:"]');
  await p.click('#galeria [data-open="dining"]'); await p.keyboard.press('Escape');
  await p.click('#bookCards [data-portal="mega"]');

  const pushes = await p.evaluate(() => window.dataLayer.filter(e => e && typeof e.event === 'string' && !e.event.startsWith('gtm'))
    .map(e => ({ event: e.event, own: Object.keys(e), vals: Object.fromEntries(Object.keys(e).map(k => [k, e[k] === undefined ? '__undef__' : e[k]])) })));

  // odmietnutie: lišta zmizne, voľba sa zapamätá a po obnovení sa GA4 nepovolí; v päte sa dá voľba zmeniť
  const r = await b.newPage({ locale: 'sk-SK' });
  await r.route('**/*googletagmanager.com/**', x => x.abort());
  await r.goto('file://' + file);
  await r.click('#ckBar [data-ck="reject"]');
  await r.reload();
  const afterReload = await r.evaluate(() => ({ bar: !document.getElementById('ckBar').hidden, log: window.dataLayer.filter(e => e && e[0] === 'consent').map(e => e[1] + ':' + e[2].analytics_storage) }));
  if (afterReload.bar) fail.push('po odmietnutí a obnovení sa lišta zobrazila znova');
  if (afterReload.log.join() !== 'default:denied') fail.push(`po odmietnutí má zostať len default:denied, je ${afterReload.log.join(', ')}`);
  await r.click('footer [data-ck-open]');
  if (!(await r.isVisible('#ckPanel'))) fail.push('odkaz „Nastavenia cookies“ v päte neotvoril nastavenia');
  console.log('cookies: odmietnutie zapamätané, po obnovení', afterReload.log.join(', '), '· nastavenia z päty OK');

  await b.close();

  const tracked = pushes.filter(x => EXPECT[x.event]);
  if (tracked.length !== 7) fail.push(`čakal som 7 udalostí, prišlo ${tracked.length}`);
  // ako dátový model GTM: každý push sa zlúči do predchádzajúceho stavu, chýbajúci kľúč si GTM pamätá z minula
  const model = Object.fromEntries(KEYS.map(k => [k, '__undef__']));
  for (const x of tracked) {
    for (const k of KEYS) {
      if (!x.own.includes(k)) { fail.push(`${x.event}: chýba kľúč ${k}`); continue; }
      const v = x.vals[k];
      if (k === 'lang' || k === EXPECT[x.event]) { if (v === '__undef__' || v === '' || v == null) fail.push(`${x.event}: ${k} nemá hodnotu`); }
      else if (v !== '__undef__') fail.push(`${x.event}: ${k} má byť undefined, je „${v}“`);
      model[k] = v;
    }
    const leaked = KEYS.filter(k => k !== 'lang' && k !== EXPECT[x.event] && model[k] !== '__undef__');
    if (leaked.length) fail.push(`${x.event}: v GTM by zostali staré hodnoty ${leaked.join(', ')}`);
    console.log('OK?', x.event.padEnd(14), KEYS.map(k => `${k}=${x.vals[k] === '__undef__' ? 'undefined' : x.vals[k]}`).join('  '));
  }
  if (fail.length) { console.error('\nCHYBY:\n- ' + fail.join('\n- ')); process.exit(1); }
  console.log(`\nVšetkých ${tracked.length} pushov má 5 kľúčov, nepoužité sú undefined, nič sa neprenáša. gtag.js na webe nie je. Cookie lišta funguje.`);
})();
