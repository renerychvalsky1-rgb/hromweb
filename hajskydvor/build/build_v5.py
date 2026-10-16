import sys, re, json, base64, os
S = sys.argv[1]
v1 = open('hajskydvor/v1.html').read()
s = open(S + '/v5_src.html').read()
# icons from v1
defs = re.search(r'<defs>\n(.*?)\n  </defs>', v1, re.S).group(1)
s = s.replace('<!--ICONS-->', defs)
# logo (cropped) + host photo
logo = re.search(r'<img src="(data:image/png;base64,[^"]+)" alt="Hájsky dvor">', v1).group(1)
host = 'data:image/jpeg;base64,' + base64.b64encode(open('hajskydvor/hostitelia.jpg', 'rb').read()).decode()
s = s.replace('__LOGO__', logo).replace('__HOST__', host)
# trips: v1 markup -> v2 cards with picture placeholder
tips_v1 = re.search(r'    <div class="tips">\n(.*?)\n    </div>\n    <div class="more-tips">', v1, re.S).group(1)
arts = re.findall(r'<article class="tip" data-seasons="([^"]+)">\n(.*?)\n      </article>', tips_v1, re.S)
VAR = ['water', 'stone', 'olive', 'water', 'dusk', 'water', 'wood', 'olive', 'stone', 'wood', 'dusk', 'wood']
ICO = ['i-water', 'i-pin', 'i-tree', 'i-water', 'i-pin', 'i-water', 'i-pin', 'i-tree', 'i-tree', 'i-camera', 'i-pin', 'i-fire']
# vlastné fotky pri tipoch (kľúč zo zoznamu PHOTOS)
OWN = {11: ('yard2', 'Ležadlá na dvore')}
# fotky výletov (od Reného, z internetu – overiť práva)
TIPIMG = ['haj', 'turna', 'zadiel', 'hrhov', 'jasov', 'domica', 'krasna', 'betliar', 'silica', 'granarium', 'kosice']
# tipy, kam sa dá ísť pešo priamo z domu (vodopády, Turniansky hrad, Zádiel)
WALK = {0, 1, 2}
out = []
for i, (seasons, body) in enumerate(arts):
    km = re.search(r'\s*(<span class="km"[^>]*>.*?</span>)\n', body).group(1)
    rest = body.replace(re.search(r'\s*<span class="km"[^>]*>.*?</span>\n', body).group(0), '\n', 1).strip('\n')
    rest = re.sub(r'\s*\[[^\]]*\]', '', rest)  # interné poznámky [..] na webe nechceme
    if i in WALK: km += '<span class="walk-badge" data-i18n="walk.badge">🥾 pešo z domu</span>'
    media = (f'<div class="ill photo">{km}<img data-photo="{OWN[i][0]}" alt="{OWN[i][1]}"></div>' if i in OWN
             else f'<div class="ill photo">{km}<img src="data:image/webp;base64,' + base64.b64encode(open(f'{S}/v5/tips/{TIPIMG[i]}.webp', 'rb').read()).decode() + f'" alt="{re.search(r"<h3[^>]*>(.*?)</h3>", body).group(1)}" loading="lazy"></div>' if i < len(TIPIMG)
             else f'<div class="ph {VAR[i]}">{km}<svg><use href="#{ICO[i]}"/></svg></div>')
    out.append(f'''      <article class="tip reveal" data-seasons="{seasons}">
        {media}
        <div class="tip-body">
{rest}
        </div>
      </article>''')
assert len(out) == 12, len(out)
s = s.replace('<!--TIPS-->', '\n'.join(out))
# Granárium samostatne (bez viaduktu)
for old, new in [('<h3 data-i18n="tip.10h">Granárium a Jablonovský viadukt</h3>', '<h3 data-i18n="tip.10h">Granárium</h3>'),
                 ('alt="Granárium a Jablonovský viadukt"', 'alt="Granárium"'),
                 ('Esterházyho sýpka Granárium a kamenný viadukt pri Jablonove nad Turňou. Krátke zastávky, ktoré sa dajú spojiť s výletom na hrad.',
                  'Esterházyho sýpka Granárium. Krátka zastávka, ktorá sa dá spojiť s výletom na hrad.'),
                 ('Záhrada, hry s deťmi, sauna a večer kaďa, v chladné dni aj krb.', 'Záhrada, hry s deťmi, večer kaďa a v chladné dni krb.')]:
    assert old in s, old; s = s.replace(old, new)
s = s.replace('<!--SCRIPT-->', open(S + '/v5/v5_script.html').read())
# fotky do zoznamu PHOTOS (raz, galéria aj sekcie sa na ne odkazujú)
sys.path.insert(0, S + '/v5'); from photo_list import PHOTOS
plist = [{'k': k, 'cat': cat, 'alt': alt, 'src': 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/v5/photos/{k}.webp', 'rb').read()).decode()} for k, src, cat, alt, pos in PHOTOS]
s = s.replace('/*__PHOTOS__*/[]/*__END_PHOTOS__*/', json.dumps(plist, ensure_ascii=False))
for name in ['raj', 'materska', 'unik', 'zima']:
    s = s.replace(f'__REEL_{name}__', 'data:video/mp4;base64,' + base64.b64encode(open(f'{S}/v5/reels/{name}.mp4', 'rb').read()).decode())
    s = s.replace(f'__REELPOSTER_{name}__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/v5/reels/{name}_poster.webp', 'rb').read()).decode())
# translations: v1 + v2 keys, only those used on this page
used = set(re.findall(r'data-i18n="([^"]+)"', s))
JS = {'js.check', 'js.note.booking', 'js.note.mega', 'js.note.airbnb', 'ui.theme', 'ui.portal', 'meta.title', 'meta.desc', 'vid.cta', 'vid.1', 'vid.2', 'vid.3', 'vid.4', 'gl.eyebrow', 'lb.close', 'lb.prev', 'lb.next'} | {f'gc.{c}' for c in ['house', 'living', 'kitchen', 'rooms', 'attic', 'bath', 'kids', 'terrace', 'garden', 'tub', 'history']}
EXTRA = {'hu': {'tip.unesco': 'UNESCO', 'tip.gemer': 'Gömör'}, 'en': {'tip.unesco': 'UNESCO', 'tip.gemer': 'Gemer'},
         'de': {'tip.unesco': 'UNESCO', 'tip.gemer': 'Gemer'}, 'pl': {'tip.unesco': 'UNESCO', 'tip.gemer': 'Gemer'},
         'uk': {'tip.unesco': 'ЮНЕСКО', 'tip.gemer': 'Гемер'}}
sk = json.load(open(f'{S}/i18n/sk.json')); sk.update(json.load(open(f'{S}/i18n/v2_sk.json'))); sk.update(json.load(open(f'{S}/i18n/v3_sk.json'))); sk.update(json.load(open(f'{S}/i18n/v5_sk.json')))
d_all = {}
for l in ['hu', 'en', 'de', 'pl', 'uk']:
    d = json.load(open(f'{S}/i18n/{l}.json')); d.update(EXTRA[l])
    f2 = f'{S}/i18n/v2_{l}.json'
    if os.path.exists(f2): d.update(json.load(open(f2)))
    d.update(json.load(open(f'{S}/i18n/v3_{l}.json'))); d.update(json.load(open(f'{S}/i18n/v5_{l}.json')))
    need = (used | JS) - {'tip.unesco', 'tip.gemer'}
    missing = sorted(k for k in need if k not in d)
    if missing: print(l, 'MISSING', missing)
    d_all[l] = {k: v for k, v in d.items() if k in used | JS}
# SK in HTML must equal sk.json for reused keys
html_sk = {}
for k, v in re.findall(r'data-i18n="([^"]+)"[^>]*>(.*?)</(?:span|strong|h[1-4]|p|a|small|em|summary|text|button|div)>', s, re.S):
    html_sk.setdefault(k, v.strip())
for k, v in html_sk.items():
    if k in sk and re.sub(r'\s+', ' ', v) != sk[k] and '<' not in v:
        print('SK MISMATCH', k, '|', v, '|', sk[k])
blob = '{\n' + ',\n'.join(f'    {l}: ' + json.dumps(d, ensure_ascii=False, indent=6)[:-1] + '    }' for l, d in d_all.items()) + '\n  }'
assert '</script' not in blob
s = re.sub(r'/\*__I18N__\*/.*?/\*__END__\*/', lambda m: '/*__I18N__*/' + blob + '/*__END__*/', s, flags=re.S)
open('hajskydvor/v5.html', 'w').write(s)
print('built v5.html', len(s), 'bytes; used keys', len(used))
