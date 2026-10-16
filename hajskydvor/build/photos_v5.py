"""Verzia 5: reálne fotky (Booking + hostia), galéria s lightboxom, skutočné recenzie.
Spúšťa sa nad v5_src_before_photos.html -> v5_src.html."""
import sys, re
sys.path.insert(0, sys.argv[1] + '/v5')
from photo_list import PHOTOS
S = sys.argv[1]
s = open(S + '/v5_src_before_photos.html').read()
P = {k: (src, cat, alt, pos) for k, src, cat, alt, pos in PHOTOS}

def sub(pat, rep, flags=re.S):
    global s
    s2, n = re.subn(pat, rep, s, count=1, flags=flags)
    assert n == 1, pat[:80]
    s = s2

def ph(key, cls='', tag='div'):
    src, cat, alt, pos = P[key]
    style = '' if pos == '50% 50%' else f' style="object-position:{pos}"'
    inner = f'<img data-photo="{key}" alt="{alt}"{style}>'
    if tag == 'button':
        return f'<button type="button" class="ill photo{cls}" data-open="{key}" aria-label="{alt}">{inner}</button>'
    return f'<div class="ill photo{cls}">{inner}</div>'

# štýly
sub(r'</style>', lambda m: open(S + '/v5/photos.css').read() + open(S + '/v5/flags.css').read() + '</style>')

# kaďa + detský domček s ohniskom (sauna nie je, búdka na fotke je detský domček)
sub(r'<div class="ph dusk"><svg><use href="#i-tub"/></svg><em>foto: kaďa</em></div>\s*<div class="ph wood"><svg><use href="#i-sauna"/></svg><em>foto: sauna</em></div>',
    lambda m: ph('tub_night') + '\n        ' + ph('firepit'))
# záhrada + detský kútik
sub(r'<div class="ph olive"><svg><use href="#i-leaf"/></svg><em>foto: záhrada</em></div>\s*<div class="ill"><img src="data:image/webp;base64,[^"]+" alt=""></div>',
    lambda m: ph('garden') + '\n        ' + ph('kids_corner'))
sub(r'(<span data-i18n="wl.3p">[^<]+</span>) <span class="note-in">\[Doplniť: čo v kútiku je[^<]*</span>',
    lambda m: m.group(1) + ' <span data-i18n="wl.3p2">Vnútri knižky, hračky a indiánsky stan, vonku ihrisko, pieskovisko a hojdacia sieť na terase.</span>')

# izby
for cnt, key, rk in [('1×', 'room_single', 'rm.1t'), ('1×', 'room_double', 'rm.2t'), ('2×', 'attic1', 'rm.3t')]:
    sub(rf'<div class="ill"><span class="room-count">{cnt}</span><img src="data:image/webp;base64,[^"]+" alt=""></div>(<div class="room-body"><h3 data-i18n="{re.escape(rk)}">)',
        lambda m, c=cnt, k=key: ph(k).replace('<img', f'<span class="room-count">{c}</span><img', 1) + m.group(1))
sub(r'<div class="ph water"><span class="room-count">1×</span><svg><use href="#i-water"/></svg><em>foto: kúpeľňa</em></div>',
    lambda m: ph('bath').replace('<img', '<span class="room-count">1×</span><img', 1))
sub(r'(<p class="rooms-note" data-i18n="rm.note">[^<]*</p>)',
    lambda m: m.group(1) + '\n    <p class="note-in" style="text-align:center">[Priradenie fotiek k izbám overiť s Denisou.]</p>')

# galéria
tiles = [('ext_yard', ' tall'), ('living_cozy', ' wide'), ('dining', ''), ('stove', ''), ('terrace_kids', ' wide'),
         ('ext_front', ' wide'), ('teepee', ' tall'), ('kitchen', ''), ('attic2', ''), ('tub_deck', ''), ('yard', '')]
gal = '\n'.join('      ' + ph(k, c, 'button') for k, c in tiles)
sub(r'<div class="gallery">.*?</div>\s*<p class="note-in" style="margin-top:1rem">\[Fotky a videá doplníme[^<]*</p>',
    lambda m: f'''<div class="gallery">
{gal}
    </div>
    <div class="gallery-more"><button type="button" class="btn btn-line" data-open="ext_front"><svg><use href="#i-camera"/></svg><span data-i18n="gl.all">Zobraziť všetky fotky</span> <span class="n">({len(PHOTOS)})</span></button></div>
    <p class="note-in" style="margin-top:1rem;text-align:center">[Fotky sú zatiaľ z Bookingu a od hostí (768–900 px na výšku). Na finálny web pošlite originály v plnom rozlíšení.]</p>''')

# recenzie
sub(r'<p data-i18n="rv.q1">.*?</p>\s*<footer data-i18n="rv.q1f">.*?</footer>',
    lambda m: '<p data-i18n="rv.q1">„Hájsky dvor má dušu. Dom je s veľkým citom zrekonštruovaný a zariadený čisto, útulne a originálne. … Tu sa obyčajné chvíle stávajú neobyčajnými.“</p>\n      <footer data-i18n="rv.q1f">Jitka · rodina · Booking.com</footer>')
Q = [('rv.q2', '„Cítili sme sa ako v rozprávke nielen vďaka čarovnému domu, ale aj dedinke s príjemnými ľuďmi. … Po toľkých zážitkoch sme si oddýchli na terase za domom a okúpali v kadi pod hviezdami.“', 'Diana · rodina · Booking.com'),
     ('rv.q3', '„Toto nie je klasické tuctové ubytovanie… Tento nádherne zrekonštruovaný dom má charakter, všetko je veľmi vkusne zariadené a k dispozícii máte aj celý dvor a záhradu, kde si môžete natrhať zeleninu.“', 'Michal · Booking.com'),
     ('rv.q4', '„Milovali sme každý kútik tohto miesta… Boli sme tu s deťmi a nadchlo ich obrovské množstvo hračiek, aj v záhrade.“', 'Attila · Maďarsko · Booking.com (preklad)')]
quotes = '\n'.join(f'      <blockquote class="quote"><p data-i18n="{k}">{q}</p><footer><b>10</b><span data-i18n="{k}f">{f}</span></footer></blockquote>' for k, q, f in Q)
sub(r'<div class="todo-quotes">.*?</div>\s*</div>\s*</section>',
    lambda m: f'<div class="quotes">\n{quotes}\n    </div>\n  </div>\n</section>')

# mapka: poznámka
sub(r'(<p class="todo-note">Orientačný návrh, rozmiestnenie je zatiaľ vymyslené\.)[^<]*</p>',
    lambda m: m.group(1) + ' Prekreslíme podľa náčrtu od Denisy. Z fotiek dopĺňame: krytá terasa s grilom a hojdacou sieťou, sauna, pieskovisko, ihrisko, ohnisko s kotlíkom a ležadlá.</p>')

# lightbox
sub(r'(<!--SCRIPT-->)',
    lambda m: '''<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Galéria" hidden>
  <figure><img id="lbImg" alt=""><figcaption><span id="lbCap"></span><small id="lbCount"></small></figcaption></figure>
  <button type="button" class="lb-close" id="lbClose" aria-label="Zavrieť">×</button>
  <button type="button" class="lb-prev" id="lbPrev" aria-label="Predchádzajúca fotka">‹</button>
  <button type="button" class="lb-next" id="lbNext" aria-label="Ďalšia fotka">›</button>
</div>

''' + m.group(1))

# Instagram: profil @hajsky_dvor (z videa hostí), kým nemáme odkazy na konkrétne reels
assert s.count('href="https://www.instagram.com/"') == 4
s = s.replace('href="https://www.instagram.com/"', 'href="https://www.instagram.com/hajsky_dvor/"')
sub(r'<p class="note-in">\[Ukážky: 3–5 s slučky bez zvuku[^<]*</p>',
    lambda m: '<p class="note-in">[Ukážky sú z vašich videí. Chýba ukážka k videu „Únik z mesta…“. Odkazy zatiaľ vedú na profil @hajsky_dvor – doplniť odkazy na konkrétne reels.]</p>')

# Google Tag Manager (GTM-57KFFMZ4): GA4 a udalosti sa nastavujú v GTM
sub(r'<!-- Google Analytics 4 — doplniť ID merania.*?-->\n', lambda m: '')
sub(r'(<meta name="viewport" content="width=device-width, initial-scale=1.0">\n)', lambda m: m.group(1) + """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-57KFFMZ4');</script>
<!-- End Google Tag Manager -->
""")
sub(r'(<body data-accent="green">\n)', lambda m: m.group(1) + """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-57KFFMZ4"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
""")

# adresa: presný bod na Google Mapách (odkaz od majiteľky)
MAP = 'https://maps.app.goo.gl/eDrvEYHP3DEzSBfe7'
sub(r'<div><strong>Háj 83, 044 03 Háj</strong>(<small data-i18n="ct.addr">)',
    lambda m: f'<div><a href="{MAP}" target="_blank" rel="noopener">Háj 83, 044 03 Háj</a>' + m.group(1))
sub(r'(<div class="gmap"><iframe [^>]*></iframe></div>)',
    lambda m: m.group(1) + f'\n      <a class="btn btn-line map-btn" href="{MAP}" target="_blank" rel="noopener"><svg><use href="#i-pin"/></svg><span data-i18n="ct.nav">Navigovať v Google Mapách</span></a>')
sub(r'<li>Háj 83, 044 03 Háj</li>', lambda m: f'<li><a href="{MAP}" target="_blank" rel="noopener">Háj 83, 044 03 Háj</a></li>')

# vlajky: tlačidlo jazyka, rozbaľovacie menu, pätička
sub(r'<button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false"><svg><use href="#i-globe"/></svg>',
    lambda m: '<button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false"><i class="flag fl-sk" id="langFlag" aria-hidden="true"></i>')
for code in ['sk', 'hu', 'en', 'de', 'pl', 'uk']:
    sub(rf'(<a href="\?lang={code}" data-lang="{code}">)', lambda m, c=code: m.group(1) + f'<i class="flag fl-{c}" aria-hidden="true"></i>')
LBL = [('sk', 'SK', 'Slovenčina'), ('hu', 'HU', 'Magyar'), ('en', 'EN', 'English'), ('de', 'DE', 'Deutsch'), ('pl', 'PL', 'Polski'), ('uk', 'UA', 'Українська')]
foot = ''.join(f'<a href="?lang={c}" data-lang="{c}" lang="{c}" title="{n}"><i class="flag fl-{c}" aria-hidden="true"></i>{l}</a>' for c, l, n in LBL)
sub(r'<span>SK · HU · EN · DE · PL · UA</span>', lambda m: f'<span class="foot-langs">{foot}</span>')

# Miskolc: vzdialenosť od Reného
sub(r'<div><span>Miskolc \(HU\)</span><b>\[overiť\]</b></div>', lambda m: '<div><span>Miskolc (HU)</span><b>105 km</b></div>')

# ===== Úvodné fotky, Vitajte, časté otázky, telefón, päta, jazyky, SEO =====
import base64, json as _json
def tip_uri(k): return 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/v5/tips/{k}.webp', 'rb').read()).decode()
own_src = re.search(r'<img class="paint own" src="(data:image/webp;base64,[^"]+)" alt="[^"]*">', s).group(1)
# úvod: 3 fotky, ktoré sa pomaly prelínajú (akvarel ide k častým otázkam)
sub(r'<!-- Obrázok od majiteľky[^>]*-->\s*<img class="paint own" src="data:image/webp;base64,[^"]+" alt="[^"]*">',
    lambda m: '<div class="hero-slides">\n        ' + '\n        '.join(ph(k, ' hs' + (' is-on' if i == 0 else '')) for i, k in enumerate(['ext_front', 'ext_street', 'living_cozy'])) + '\n      </div>')
# Vitajte: stará fotka domu
sub(r'(<div class="about-media">\s*)<div class="ill"><img src="data:image/webp;base64,[^"]+" alt=""></div>', lambda m: m.group(1) + ph('old_photo'))
# časté otázky: akvarel od majiteľky pod nadpisom
sub(r'(<h2 data-i18n="faq.h2">[^<]*</h2>\s*<p class="lead" data-i18n="bk.direct">.*?</p>)',
    lambda m: m.group(1) + f'\n      <img class="faq-paint" src="{own_src}" alt="Podkrovie s hojdacím koníkom – akvarel" loading="lazy">')
# cez týždeň: bez zvýhodnenia, fotka vodopádov
sub(r'\s*<li><svg><use href="#i-euro"/></svg>.*?</li>', lambda m: '')
sub(r'<div class="ph water"><svg><use href="#i-water"/></svg><em>foto: Hájske vodopády</em></div>',
    lambda m: f'<div class="ill photo"><img src="{tip_uri("haj")}" alt="Hájske vodopády" loading="lazy"></div>')
sub(r'<span class="note-in">\[Čas jazdy doplníme\.\]</span>',
    lambda m: m.group(0))
# telefón a jazyk v kontakte
sub(r'<a href="tel:\+421900000000">\+421 9XX XXX XXX</a><small>\[[^\]]*\]</small>',
    lambda m: '<a href="tel:+421908864513">+421 908 864 513</a><small data-i18n="ct.prefer">Rezervácie uprednostňujeme cez portály.</small>')
sub(r'<div data-i18n="ct.lang"><strong>Hovoríme po slovensky aj po maďarsky</strong><small>[^<]*</small></div>',
    lambda m: '<div data-i18n="ct.lang"><strong>Hovoríme po slovensky</strong><small>Dohovoríme sa aj anglicky a španielsky.</small></div>')
# päta: popis v bodoch a telefón
FACTS = [('🌿', 'ft.f1', 'Chalupa z roku 1857'), ('🪵', 'ft.f2', 'Hlinené omietky, drevo, kachľová pec, kaďa'),
         ('👨‍👩‍👧‍👦', 'ft.f3', 'Pre rodiny s deťmi'), ('🍎', 'ft.f4', 'Jedlá záhrada'), ('📍', 'ft.f5', 'Košice-okolie')]
sub(r'<p data-i18n="ft\.tag">.*?</p>', lambda m: '<p class="foot-text" data-i18n="ft.text">Chalupa z roku 1857 v Háji, okres Košice-okolie. Hlinené omietky, drevo, kachľová pec a kaďa pod holým nebom. Pre rodiny s deťmi, s jedlou záhradou plnou bylín a ovocia.</p>')
sub(r'(<h4 data-i18n="nav.6">Kontakt</h4>\s*<ul>)',
    lambda m: m.group(1) + '\n          <li><a href="tel:+421908864513">+421 908 864 513</a><small class="foot-note" data-i18n="ct.prefer">Rezervácie uprednostňujeme cez portály.</small></li>')

# SEO: odkazy pre jazyky, Open Graph, poloha, štruktúrované dáta (JSON-LD)
SITE = 'https://hajskydvor.sk/'
LANGS = [('sk', 'sk_SK'), ('hu', 'hu_HU'), ('en', 'en_GB'), ('de', 'de_DE'), ('pl', 'pl_PL'), ('uk', 'uk_UA')]
href = lambda l: SITE if l == 'sk' else f'{SITE}?lang={l}'
sub(r'<meta property="og:image" content="logo.png">', lambda m: '\n'.join([
    f'<meta property="og:image" content="{SITE}og-image.jpg">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
    f'<meta property="og:url" content="{SITE}">', '<meta property="og:site_name" content="Hájsky dvor">', '<meta property="og:locale" content="sk_SK">']
    + [f'<meta property="og:locale:alternate" content="{loc}">' for l, loc in LANGS[1:]]
    + ['<meta name="twitter:card" content="summary_large_image">',
       '<!-- jazykové verzie: kanonický odkaz dopĺňa skript podľa zvoleného jazyka -->']
    + [f'<link rel="alternate" hreflang="{l}" href="{href(l)}">' for l, _ in LANGS]
    + [f'<link rel="alternate" hreflang="x-default" href="{SITE}">',
       '<meta name="geo.region" content="SK-KI">', '<meta name="geo.placename" content="Háj, okres Košice-okolie">',
       '<meta name="geo.position" content="48.6298303;20.8526258">', '<meta name="ICBM" content="48.6298303, 20.8526258">']))
# časté otázky: nová sada zo skutočných údajov o chalupe
sys.path.insert(0, S + '/v5'); from faq_data import FAQ, ROOMS, MORE
faq_html = '\n'.join(f'      <details{" open" if i == 1 else ""}><summary><span data-i18n="faq.q{i}">{q}</span></summary><p data-i18n="faq.a{i}">{a}</p></details>' for i, (q, a) in enumerate(FAQ['sk'], 1))
sub(r'<details open><summary><span data-i18n="faq\.q1">.*?<details><summary><span data-i18n="faq\.q7">.*?</details>', lambda m: faq_html.lstrip())
sub(r'<span data-i18n="rm\.1s">[^<]*</span>', lambda m: f'<span data-i18n="rm.1s">{ROOMS["sk"][0]}</span>')
sub(r'<span data-i18n="rm\.4s">[^<]*</span>', lambda m: f'<span data-i18n="rm.4s">{ROOMS["sk"][1]}</span>')
sub(r'(<span class="chip" data-i18n="more\.5">[^<]*</span>)', lambda m: m.group(1) + ''.join(f'\n      <span class="chip" data-i18n="more.{i}">{t}</span>' for i, t in enumerate(MORE['sk'], 6)))
faq = [(re.sub(r'<[^>]+>', '', q), re.sub(r'<[^>]+>', '', a)) for q, a in re.findall(r'<summary><span data-i18n="faq\.q\d+">(.*?)</span></summary><p data-i18n="faq\.a\d+">(.*?)</p>', s, re.S)]
assert len(faq) == 14, len(faq)
AMEN = ['Vonkajšia kaďa (v cene pobytu)', 'Detský kútik a hračky', 'Detské ihrisko s domčekom, pieskovisko, preliezka a hojdačka',
        'Detský bazén (v lete)', 'Detské postieľky (2) a vysoká stolička', 'Detské postele so zábranou v štýle Montessori (2)', 'Jedlá permakultúrna záhrada', 'Krb a podlahové kúrenie',
        'Zastrešená terasa s grilom', 'Ohnisko s kotlíkom', 'Bedminton', 'Plne vybavená kuchyňa', 'Práčka a sušička',
        'Wi-Fi zdarma', 'Bezplatné parkovisko pri dome', 'Oplotený dvor']
ld = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'LodgingBusiness', '@id': SITE + '#lodging', 'name': 'Hájsky dvor', 'url': SITE,
     'description': 'Chalupa z roku 1857 v obci Háj v Slovenskom krase, celá len pre vás: 10 lôžok, 2 detské postele a 2 detské postieľky v 4 izbách. Kaďa v cene, detský kútik, jedlá záhrada, kachľová pec a terasa s grilom. 0,8 km od Hájskych vodopádov, 3,5 km od Turnianskeho hradu, cca 45 minút od Košíc.',
     'telephone': '+421908864513', 'image': [SITE + 'og-image.jpg'],
     'address': {'@type': 'PostalAddress', 'streetAddress': 'Háj 83', 'postalCode': '044 03', 'addressLocality': 'Háj', 'addressRegion': 'Košický kraj', 'addressCountry': 'SK'},
     'email': 'hajskydvor@gmail.com', 'geo': {'@type': 'GeoCoordinates', 'latitude': 48.6298303, 'longitude': 20.8526258}, 'hasMap': 'https://maps.app.goo.gl/eDrvEYHP3DEzSBfe7', 'numberOfRooms': 4, 'petsAllowed': False, 'smokingAllowed': False, 'checkinTime': '15:00', 'checkoutTime': '10:00', 'availableLanguage': ['sk', 'en', 'es'],
     'amenityFeature': [{'@type': 'LocationFeatureSpecification', 'name': a, 'value': True} for a in AMEN],
     'containsPlace': {'@type': 'House', 'name': 'Hájsky dvor – celá chalupa', 'occupancy': {'@type': 'QuantitativeValue', 'maxValue': 12},
                       'numberOfBedrooms': 4, 'numberOfBathroomsTotal': 1, 'yearBuilt': 1857},
     'sameAs': ['https://www.instagram.com/hajsky_dvor/', 'https://www.facebook.com/profile.php?id=61577241239808', 'https://www.booking.com/hotel/sk/hajsky-dvor.sk.html',
                'https://www.megaubytovanie.sk/hajsky-dvor', 'https://www.airbnb.com/rooms/1272449521521250272']},
    {'@type': 'WebSite', '@id': SITE + '#web', 'url': SITE, 'name': 'Hájsky dvor', 'inLanguage': [l for l, _ in LANGS], 'about': {'@id': SITE + '#lodging'}},
    {'@type': 'FAQPage', '@id': SITE + '#faq', 'inLanguage': 'sk', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}]}
blob = _json.dumps(ld, ensure_ascii=False, indent=1).replace('</', '<\\/')
sub(r'(</head>)', lambda m: '<!-- Štruktúrované dáta pre Google a AI vyhľadávače -->\n<script type="application/ld+json">\n' + blob + '\n</script>\n' + m.group(1))

# e-mail
sub(r'<a href="mailto:info@hajskydvor\.sk">info@hajskydvor\.sk</a><small>\[[^\]]*\]</small>', lambda m: '<a href="mailto:hajskydvor@gmail.com">hajskydvor@gmail.com</a>')
assert s.count('info@hajskydvor.sk') == 2, s.count('info@hajskydvor.sk')
s = s.replace('info@hajskydvor.sk', 'hajskydvor@gmail.com')
# detaily len zelené: prepínač farieb preč
sub(r'\n<div class="draft-bar" title="Len pre návrh">.*?</div>\n', lambda m: '\n')
# H1 na tri riadky
sub(r'<h1 data-i18n="hero.h1">.*?</h1>', lambda m: '<h1 data-i18n="hero.h1"><span class="ln">Celá chalupa</span> <span class="ln">pre vašu rodinu,</span> <em class="ln">kúsok od vodopádov</em></h1>')

# presný pin, PSČ podľa Google Máp, Facebook, videá kompletné
sub(r'src="https://maps\.google\.com/maps\?q=[^"]*"', lambda m: 'src="https://maps.google.com/maps?q=48.6298303,20.8526258&z=15&output=embed"')
assert s.count('044 03') == 3, s.count('044 03')
s = s.replace('044 03', '044 02')
assert s.count('href="https://www.facebook.com/"') == 2
s = s.replace('href="https://www.facebook.com/"', 'href="https://www.facebook.com/profile.php?id=61577241239808"')
sub(r'\s*<p class="note-in">\[Ukážky sú z vašich videí\.[^<]*</p>', lambda m: '')

# interné poznámky v hranatých zátvorkách preč (web je pred spustením)
s, n1 = re.subn(r'\s*<p class="note-in"[^>]*>\[[^\]]*\]</p>', '', s)
s, n2 = re.subn(r'\s*<span class="note-in">\[[^\]]*\]</span>', '', s)
assert n1 + n2 >= 3, (n1, n2)

# svetlý režim je primárny: bez uloženej voľby sa web otvorí svetlý (tmavý len cez prepínač)
old_theme = "(function () { try { var th = localStorage.getItem('hd-theme'); if (th === 'dark' || th === 'light') document.documentElement.dataset.theme = th; } catch (e) {} })();"
assert old_theme in s
s = s.replace(old_theme, "(function () { var th = null; try { th = localStorage.getItem('hd-theme'); } catch (e) {} document.documentElement.dataset.theme = th === 'dark' ? 'dark' : 'light'; })();")

# mapka areálu podľa náčrtu Denisy a jej spresnení (namiesto drevárne dielňa, hosťom neprístupná; sauna a parkovisko v náčrte nie sú)
sub(r'<svg viewBox="0 0 640 440" role="img" aria-label="Hájsky dvor">.*?</svg>', lambda m: open(S + '/v5/areal_map.svg').read().strip())
LEG = [('mp.l1', 'Dom so 4 spálňami, kuchyňou a krbom'), ('mpn.2', 'Altánok so stolom pre 10, grilom, závesným kreslom a detskou hojdačkou'), ('mpn.3', 'Detský domček'),
       ('mpn.4', 'Kaďa so svetielkami'), ('mpn.5', 'Šmykľavka'), ('mpn.6', 'Ohnisko na rovinke nad svahom'),
       ('mpn.7', 'Rovná tráva na hry a bedminton'), ('mpn.8', 'Svah so stromami'),
       ('mpn.9', 'Dielňa (pre hostí neprístupná)'), ('mpn.10', 'Pieskovisko'),
       ('mpn.11', 'Tehlový chodník pri dome s drevenou lavičkou'), ('mpn.12', 'Kvety pri susedovom plote'),
       ('mpn.13', 'Lavička pod dielňou'), ('mpn.14', 'Ohnisko s kotlíkom pri domčeku'),
       ('mpn.15', 'Kamenný múrik pod kaďou')]
sub(r'<ol class="legend">.*?</ol>', lambda m: '<ol class="legend">\n' + '\n'.join(f'        <li><b>{i}</b> <span data-i18n="{k}">{t}</span></li>' for i, (k, t) in enumerate(LEG, 1)) + '\n      </ol>')
sub(r'\s*<p class="todo-note">Orientačný návrh.*?</p>', lambda m: '')
# mapka je na výšku (pohľad zhora ako na náčrte Denisy), na širokej obrazovke ju zúžime
sub(r'<div class="areal-map">', lambda m: '<div class="areal-map areal-tall">')
# výlety rovno z domu bez auta (pešo a na bicykli), zvýraznené na začiatku sekcie Okolie
sub(r'\n    <div class="season-tabs" role="tablist">', lambda m: '\n' + open(S + '/v5/walk_block.html').read().rstrip('\n') + m.group(0))
# ďalšie tipy: nové od Denisy (rybníky, husitský kostolík) dopredu, k rastlinnému kostolu
m = re.search(r'(<strong data-i18n="ok\.more">[^<]*</strong>)(.*?)(\n    </div>)', s, re.S)
chips = dict(re.findall(r'<span class="chip" data-i18n="(more\.\d+)">([^<]*)</span>', m.group(2)))
assert sorted(chips) == sorted(f'more.{i}' for i in range(1, 11)), sorted(chips)
s = s[:m.start(2)] + ''.join(f'\n      <span class="chip" data-i18n="more.{i}">{chips[f"more.{i}"]}</span>' for i in [6, 7, 8, 1, 2, 3, 4, 5, 9, 10]) + s[m.end(2):]
# saunu nemajú (Denisa 14. 10.): texty, menu, výbava
for _a, _b in [('Kaďa a sauna v cene, detský kútik, jedlá záhrada a krb.', 'Kaďa v cene, detský kútik, jedlá záhrada a krb.'), ('content="Kaďa a sauna v cene, detský kútik a jedlá záhrada.', 'content="Kaďa v cene, detský kútik a jedlá záhrada.'), ('<strong>Kaďa aj sauna sú v cene pobytu.</strong>', '<strong>Kaďa je v cene pobytu.</strong>'), ('<strong data-i18n="bs.wt">Kaďa a sauna</strong>', '<strong data-i18n="bs.wt">Vonkajšia kaďa</strong>'), ('<div class="amen-item"><svg><use href="#i-sauna"/></svg><h3 data-i18n="f4t">Sauna</h3><span data-i18n="f4s">v cene pobytu</span></div>', '<div class="amen-item"><svg><use href="#i-tree"/></svg><h3 data-i18n="am.play.t">Ihrisko a pieskovisko</h3><span data-i18n="am.play.s">šmykľavka, hojdačky, domček</span></div>'), ('<h2 data-i18n="wl.h2">Kaďa, sauna a záhrada, ktorú môžete ochutnať</h2>', '<h2 data-i18n="wl.h2">Kaďa a záhrada, ktorú môžete ochutnať</h2>'), ('Kaďa aj sauna sú v cene pobytu. Večer potom všetci spolu pri krbe.', 'Kaďa je v cene pobytu. Večer potom všetci spolu pri krbe.'), ('<div class="sub"><h4 data-i18n="f4t">Sauna</h4><p data-i18n="wl.2p">Na prehriatie po túre k vodopádom alebo na Turniansky hrad. <strong>V cene pobytu.</strong></p></div>', '<div class="sub"><h4 data-i18n="wl.fire.h">Ohnisko s kotlíkom</h4><p data-i18n="wl.fire.p">Večer guláš z kotlíka alebo opekačka pri ohni. Drevo máte pripravené.</p></div>'), ('<strong data-i18n="wk.3t">Kaďa a sauna každý večer, v cene</strong>', '<strong data-i18n="wk.3t">Kaďa každý večer, v cene</strong>'), ('<!-- ============ KAĎA, SAUNA, ZÁHRADA ============ -->', '<!-- ============ KAĎA A ZÁHRADA ============ -->')]:
    assert s.count(_a) == 1, _a; s = s.replace(_a, _b)
s = s.replace('data-i18n="nav.2">Kaďa a sauna</a>', 'data-i18n="nav.2">Kaďa a záhrada</a>')
s = s.replace('/* ---------- Kaďa, sauna, záhrada ---------- */', '/* ---------- Kaďa a záhrada ---------- */')
# zdieľanie odkazu (WhatsApp, Facebook…): fotka z úvodu a text z päty
_ft = _json.load(open(S + '/i18n/v5_sk.json'))['ft.text']
sub(r'<meta property="og:description" content="[^"]*">', lambda m: f'<meta property="og:description" content="{_ft}">')
sub(r'<meta property="og:image" content="[^"]*">', lambda m: f'<meta property="og:image" content="{SITE}og-image.jpg?v=2">')
sub(r'(<meta property="og:image:height" content="630">)', lambda m: m.group(1) + '\n<meta property="og:image:alt" content="Hájsky dvor – chalupa z roku 1857 v Háji">')
# lôžka a izby podľa Denisy (15. 10.)
_rooms = re.search(r'<div class="rooms">\n(.*?)\n    </div>', s, re.S)
_arts = _rooms.group(1).split('\n')
assert len(_arts) == 4, len(_arts)
_new = [
 '      <article class="room"><div class="ill photo"><span class="room-count">1×</span><img data-photo="room_double2" alt="Spálňa na prízemí s dverami do detskej izby"></div><div class="room-body"><h3 data-i18n="rm.1t">Spálňa na prízemí</h3><span data-i18n="rm.1s">manželská posteľ + detská postieľka</span></div></article>',
 '      <article class="room"><div class="ill photo"><span class="room-count">1×</span><img data-photo="kids_room" alt="Detská izba s posteľami Montessori"></div><div class="room-body"><h3 data-i18n="rm.2t">Detská izba</h3><span data-i18n="rm.2s">2 detské postele so zábranou v štýle Montessori, 200 × 90 a 140 × 70</span></div></article>',
 '      <article class="room"><div class="ill photo"><span class="room-count">2×</span><img data-photo="attic1" alt="Spálňa v podkroví"></div><div class="room-body"><h3 data-i18n="rm.3t">Spálňa v podkroví</h3><span data-i18n="rm.3s">manželská posteľ + 2 jednolôžka</span></div></article>',
 _arts[3]]
s = s[:_rooms.start(1)] + '\n'.join(_new) + s[_rooms.end(1):]
sub(r'(\n    <p class="rooms-note")', lambda m: '\n    <p class="rooms-layout" data-i18n="rm.layout">Spálňa a detská izba na prízemí sú vedľa seba a sú prechodné, obe spálne v podkroví sú samostatné. Spolu 10 lôžok, 2 detské postele a 2 detské postieľky.</p>' + m.group(1))
for _a, _b in [('Celý pre 11 hostí,', 'Celý pre 10 hostí a vaše deti,'), ('celý pre 11 hostí.', 'celý pre 10 hostí a deti.'),
               ('<strong data-i18n="f1t">11 lôžok</strong><span data-i18n="f1s">celá chalupa len pre vás</span>', '<strong data-i18n="f1t">10 lôžok</strong><span data-i18n="f1s">+ 2 detské postele a 2 postieľky</span>')]:
    assert s.count(_a) == 1, _a; s = s.replace(_a, _b)
# spustenie (15. 10.): web sa môže indexovať, vlastná cookie lišta (Google Consent Mode v2), prevádzkovateľ v päte
sub(r'<meta name="robots" content="noindex, nofollow">\n?', lambda m: '')
s = s.replace('<!-- NÁVRH 5: pred spustením na hajskydvor.sk odstrániť noindex -->\n', '')
CONSENT_HEAD = open(S + '/v5/consent_head.html').read()
sub(r'(<!-- Google Tag Manager -->)', lambda m: CONSENT_HEAD + m.group(1))
sub(r'<span>© 2026 Hájsky dvor</span>', lambda m: '<span class="foot-legal">© 2026 Hájsky dvor · <span data-i18n="ft.operator">Prevádzkovateľ</span>: VOLTOM s.r.o., Čižatice 78, 044 47 Čižatice, IČO 50580426 · <a href="ochrana-osobnych-udajov.html" data-i18n="ft.privacy">Ochrana osobných údajov</a> · <a href="#cookies" data-ck-open data-i18n="ft.cookies">Nastavenia cookies</a></span>')
sub(r'(<!--SCRIPT-->)', lambda m: open(S + '/v5/cookie_bar.html').read() + m.group(1))
open(S + '/v5_src.html', 'w').write(s)
print('ok', len(s) // 1024, 'KB')
