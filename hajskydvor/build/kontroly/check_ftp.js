const { chromium } = require('playwright');
(async () => {
  const [dir, out] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const [w, h] of [[1366, 900], [390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    const failed = [];
    p.on('requestfailed', r => { if (r.url().startsWith('file:')) failed.push(r.url()); });
    await p.route(/secureprivacy|googletagmanager/, r => r.abort());
    await p.goto('file://' + dir + '/index.html');
    const res = await p.evaluate(async () => {
      document.querySelectorAll('img').forEach(i => i.loading = 'eager');
      await Promise.all([...document.querySelectorAll('img')].map(i => i.decode().catch(() => {})));
      const imgs = [...document.querySelectorAll('img')].filter(i => i.getAttribute('src'));
      const broken = imgs.filter(i => !i.naturalWidth).map(i => i.getAttribute('src').slice(0, 60));
      const vids = [...document.querySelectorAll('video')].map(v => (v.getAttribute('poster') || '') + ' ' + (v.querySelector('source')?.getAttribute('src') || v.getAttribute('src') || ''));
      return { n: imgs.length, broken, vids, kb: document.documentElement.outerHTML.length >> 10 };
    });
    // otvor galériu (lightbox) – fotka sa musí načítať
    await p.click('#galeria [data-open="kitchen"]'); await p.waitForTimeout(400);
    const lb = await p.evaluate(() => { const i = document.querySelector('.lb img'); return i && i.naturalWidth; });
    await p.keyboard.press('Escape');
    console.log(w, 'imgs', res.n, 'broken', res.broken, 'lightbox', lb, 'failed', failed.slice(0, 5), 'videos', res.vids.length);
    if (w === 1366) { await p.screenshot({ path: out + '/ftp_top.png' }); }
    await p.close();
  }
  const p = await b.newPage({ viewport: { width: 390, height: 844 } });
  await p.route(/secureprivacy|googletagmanager|fonts/, r => r.abort());
  await p.goto('file://' + dir + '/ochrana-osobnych-udajov.html');
  await p.screenshot({ path: out + '/privacy_m.png', fullPage: false });
  console.log('privacy overflow', await p.evaluate(() => document.documentElement.scrollWidth - innerWidth));
  await b.close();
})();
