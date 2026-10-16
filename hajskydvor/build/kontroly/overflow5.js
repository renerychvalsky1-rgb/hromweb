const { chromium } = require('playwright');
(async () => {
  const f = 'file://' + process.argv[2];
  const b = await chromium.launch();
  for (const w of [390, 360]) for (const l of ['sk','hu','en','de','pl','uk']) {
    const c = await b.newContext({ viewport: { width: w, height: 800 } }); const p = await c.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='warning') errs.push(m.text()); });
    await p.goto(f + '?lang=' + l); await p.waitForTimeout(150);
    const r = await p.evaluate((w) => {
      const sw = document.documentElement.scrollWidth;
      const bad = [...document.querySelectorAll('body *')].filter(el => { const r = el.getBoundingClientRect(); return r.right > w + 1 && r.width > 0 && getComputedStyle(el).position !== 'fixed' && !el.closest('.sheet,.lang-menu,svg,.marquee'); })
        .map(el => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + ' «' + (el.textContent || '').trim().slice(0, 40) + '» right=' + Math.round(el.getBoundingClientRect().right));
      return { sw, bad: bad.slice(0, 6) };
    }, w);
    console.log(w, l, 'scrollWidth', r.sw, errs.length ? errs : '', r.sw > w ? r.bad : '');
    await c.close();
  }
  await b.close();
})();
