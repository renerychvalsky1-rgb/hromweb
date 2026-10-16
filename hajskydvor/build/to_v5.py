import sys, re, base64
S = sys.argv[1]; V = S + '/v4'; V5 = S + '/v5'
s = open(S + '/v3_src.html').read()

def sub(pat, rep, count=1, flags=re.S):
    global s
    s2, n = re.subn(pat, rep, s, count=count, flags=flags)
    assert n == (count or n) and n > 0, (n, pat[:70])
    s = s2
def img(name): return 'data:image/webp;base64,' + base64.b64encode(open(f'{V}/img/{name}.webp', 'rb').read()).decode()

sub(r'family=Caveat:[^"]+&display=swap', 'family=Bitter:ital,wght@0,500;0,600;0,700;1,500&family=Nunito:wght@400;600;700;800;900&display=swap')
sub(r'<style>.*?</style>', lambda m: open(V5 + '/v5.css').read())
s = s.replace('<!-- NÁVRH 3:', '<!-- NÁVRH 5:')
# kreslené čmáranice preč
s, n = re.subn(r'\n\s*<svg class="doodle[^"]*"[^>]*><use href="#d-[a-z]+"/></svg>', '', s); print('doodles removed', n)
# úvod: akvarel domu z návrhu majiteľky
sub(r'<!-- Návrh: akvarelová ilustrácia domu[^>]*-->\s*<svg class="paint".*?</svg>',
    lambda m: '<!-- Obrázok od majiteľky – ukážka štýlu, ďalšie dodá sama -->\n      <img class="paint own" src="data:image/webp;base64,' + base64.b64encode(open(V5 + '/img/own_hero.webp', 'rb').read()).decode() + '" alt="Hájsky dvor – podkrovie s hojdacím koníkom">')
# o nás: dom zvonku
sub(r'<div class="ph wood"><svg><use href="#i-camera"/></svg><em>foto: dom zvonku</em></div>', lambda m: f'<div class="ill"><img src="{img("house6")}" alt=""></div>')
# pre deti: ilustrácie
for k, name in [('k-toys', 'ico_toys'), ('k-garden', 'sprig_berry'), ('k-yard', 'yard7')]:
    sub(rf'<div class="pic"><svg><use href="#{k}"/></svg></div>', lambda m, n=name: f'<div class="pic"><img src="{img(n)}" alt=""></div>')
sub(r'<div class="pic"><svg><use href="#k-falls"/></svg></div>', lambda m: '<div class="pic">' + open(V + '/falls.svg').read() + '</div>')
# kútik v sekcii záhrada
sub(r'<div class="ph stone"><svg><use href="#i-kids"/></svg><em>foto: detský kútik</em></div>', lambda m: f'<div class="ill"><img src="{img("kidsroom7")}" alt=""></div>')
# izby
for cnt, name in [('1×', 'kidsroom6'), ('1×', 'bedroom6'), ('2×', 'bedroom7')]:
    sub(rf'<div class="ph [a-z]+"><span class="room-count">{cnt}</span><svg><use href="#i-bed"/></svg><em>foto: izba</em></div>',
        lambda m, n=name, c=cnt: f'<div class="ill"><span class="room-count">{c}</span><img src="{img(n)}" alt=""></div>')
# galéria
sub(r'<div class="ph olive tall"><svg><use href="#i-camera"/></svg><em>dvor a záhrada</em></div>', lambda m: f'<div class="ill tall"><img src="{img("yard6")}" alt=""></div>')
sub(r'<div class="ph wood wide"><svg><use href="#i-camera"/></svg><em>obývačka s krbom</em></div>', lambda m: f'<div class="ill wide"><img src="{img("shelf7")}" alt=""></div>')
# akvarelové škvrny po okrajoch sekcií (namiesto vetvičiek)
def blot(style): return f'\n  <span class="blot" aria-hidden="true" style="{style}"></span>'
sub(r'(<section id="deti" class="wash wash-sun">)', lambda m: m.group(1) + blot('left:-1%;top:-1rem;width:300px;height:250px') + blot('right:0;bottom:0;width:240px;height:200px;transform:scaleX(-1)'))
sub(r'(<section class="reviews">)', lambda m: m.group(1) + blot('right:1%;top:1rem;width:270px;height:220px'))
sub(r'(<section id="rezervacia" class="book wash wash-peach">)', lambda m: m.group(1) + blot('left:1%;top:1rem;width:260px;height:210px;transform:scaleX(-1)'))
# videá z Instagramu: len ukážky, celé video na Instagrame
s = s.replace('<em>video z IG (reels)</em>', '<em>záhrada</em>')
sub(r'(?=<!-- ============ AREÁL ============ -->)', lambda m: '''<!-- ============ VIDEÁ Z INSTAGRAMU ============ -->
<section id="videa" class="wash wash-sky">
  <div class="wrap">
    <div class="split-head">
      <div>
        <span class="eyebrow"><span data-i18n="vid.eyebrow">Videá z Instagramu</span></span>
        <h2 data-i18n="vid.h2">Pozrite sa, ako to u nás žije</h2>
        <p class="lead" data-i18n="vid.lead">Krátke ukážky z nášho Instagramu. Po kliknutí si pozriete celé video.</p>
      </div>
      <a href="https://www.instagram.com/" class="btn btn-line" target="_blank" rel="noopener"><svg><use href="#i-ig"/></svg><span data-i18n="gl.ig">Viac na Instagrame</span></a>
    </div>
    <div class="reels" id="reels"><!-- generuje JS zo zoznamu REELS --></div>
    <p class="note-in">[Ukážky: 3–5 s slučky bez zvuku (MP4/WebM, do ~500 kB), vystrihnuté z vašich reels. Celé videá ostávajú na Instagrame.]</p>
  </div>
</section>

''')
# detailová farba: zelená podľa návrhu, alternatíva okrová
sub(r'<body data-accent="yellow">', '<body data-accent="green">')
sub(r'<button class="on" data-accent="yellow" style="background:#F0B640" aria-label="Žltá"></button>\s*<button data-accent="green" style="background:#8DB45A" aria-label="Zelená"></button>',
    '<button class="on" data-accent="green" style="background:#6A7A50" aria-label="Šalviová"></button>\n  <button data-accent="yellow" style="background:#A8733C" aria-label="Medová"></button>')
s = s.replace('Návrh 3 · detail:', 'Návrh 5 · detail:')
# mapka: písmo

open(S + '/v5_src.html', 'w').write(s)
print('ok', len(s) // 1024, 'KB')
