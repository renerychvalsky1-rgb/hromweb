# Mapka areálu na výšku, ako na náčrtoch Denisy (dom dole vľavo, altánok zarovno nad domom, chodník vedľa domu)
import sys
S = sys.argv[1]
bricks = ''.join(f'M140 {y} H159 ' if (y // 14) % 2 == 0 else f'M159 {y} H178 ' for y in range(486, 636, 14))
hach = ' '.join(f'M{x} {y} L{x + 4} {y + 16}' for y, xs in [(108, range(40, 220, 40)), (138, range(60, 220, 40))] for x in xs)
leaves = ''.join(f'<circle cx="430" cy="{y}" r="7"/>' for y in range(482, 612, 22))
blossoms = ''.join(f'<circle cx="{422 if i % 2 else 432}" cy="{476 + i * 20}" r="5.5" fill="{c}"/>' for i, c in enumerate(['#D98BA0', '#E8C774', '#B79BD3', '#D98BA0', '#E8C774', '#B79BD3', '#D98BA0']))
bulbs = ''.join(f'<circle cx="{x}" cy="196" r="3.4"/>' for x in range(60, 205, 24))
chairs = ''.join(f'<circle cx="{x}" cy="{y}" r="3.4"/>' for y in (428, 456) for x in range(45, 110, 14))
marks = [(1, 80, 592), (2, 202, 441), (3, 49, 388), (4, 192, 280), (5, 237, 252), (6, 162, 60), (7, 372, 362), (8, 196, 150),
         (9, 418, 62), (10, 163, 386), (11, 159, 612), (12, 400, 540), (13, 322, 142), (14, 106, 388), (15, 262, 306)]
wall = ''.join(f'<rect x="{x}" y="300" width="{min(17, 438 - x)}" height="12" rx="3" fill="{"#D6C4A0" if i % 2 else "#C8B48E"}"/>' for i, x in enumerate(range(22, 438, 18)))
mk = '\n'.join(f'          <g><circle cx="{x}" cy="{y}" r="14" fill="var(--accent)"/><text x="{x}" y="{y + 5}" fill="var(--accent-ink)">{n}</text></g>' for n, x, y in marks)
svg = f'''<svg viewBox="0 0 460 660" role="img" aria-label="Mapka areálu Hájsky dvor">
        <!-- Pohľad zhora podľa náčrtov Denisy: dole dom s chodníkom a altánkom, nad nimi domček, ohnisko, pieskovisko a kaďa, hore svah, rovinka s ohniskom a dielňa -->
        <rect width="460" height="660" rx="16" fill="#F4EAD3"/>
        <rect x="20" y="20" width="420" height="620" rx="18" fill="#DDE0B6"/>
        <!-- rovinka s ohniskom -->
        <path d="M20 38 Q20 20 38 20 H262 V92 C200 98 120 92 20 100Z" fill="#E4E6C2"/>
        <!-- svah klesá smerom k domu -->
        <path d="M20 100 C120 92 200 98 262 92 V150 C250 166 228 180 214 186 C160 192 80 182 20 190Z" fill="#C9D29A"/>
        <path d="{hach}" fill="none" stroke="#9DAA6B" stroke-width="2" stroke-linecap="round" opacity=".85"/>
        <text x="120" y="178" text-anchor="middle" font-family="Nunito" font-size="13" font-weight="700" fill="#5E6B34" data-i18n="mpn.slope">Svah</text>
        <!-- rovná tráva -->
        <path d="M440 226 C380 222 300 236 268 270 C246 296 300 330 318 372 C334 420 280 466 240 512 C210 548 214 590 262 598 V640 H422 Q440 640 440 622Z" fill="#E9ECC9"/>
        <text x="372" y="334" text-anchor="middle" font-family="Nunito" font-size="14" font-weight="700" fill="#7D8B4A" data-i18n="mpn.lawn">Rovná tráva</text>
        <!-- ohnisko na rovinke, kríky -->
        <g fill="#93A15E"><circle cx="46" cy="40" r="9"/><circle cx="58" cy="74" r="8"/><circle cx="176" cy="34" r="7"/><circle cx="44" cy="124" r="8"/></g>
        <g fill="#7D8B4A"><circle cx="34" cy="152" r="12"/><circle cx="62" cy="176" r="10"/></g>
        <circle cx="110" cy="56" r="18" fill="#B9A57F" stroke="#6B5338" stroke-width="2"/>
        <circle cx="110" cy="56" r="9" fill="#E8A33A"/>
        <g fill="#A89A80"><circle cx="88" cy="36" r="3.5"/><circle cx="132" cy="36" r="3.5"/><circle cx="88" cy="76" r="3.5"/><circle cx="132" cy="76" r="3.5"/></g>
        <!-- dielňa (pre hostí neprístupná) -->
        <path d="M263 21 H422 Q439 21 439 38 V103 H263Z" fill="#E2DACB"/>
        <path d="M262 20 V104 H440" fill="none" stroke="#8C6A43" stroke-width="3" stroke-linecap="round"/>
        <rect x="290" y="34" width="100" height="56" rx="4" fill="#CDBFA6" stroke="#6B5338" stroke-width="2"/>
        <path d="M286 36 H394" stroke="#8C7A62" stroke-width="5" stroke-linecap="round"/>
        <rect x="302" y="48" width="14" height="12" rx="1.5" fill="#EFE8DA" stroke="#6B5338" stroke-width="1.2"/>
        <rect x="364" y="48" width="14" height="12" rx="1.5" fill="#EFE8DA" stroke="#6B5338" stroke-width="1.2"/>
        <rect x="330" y="62" width="20" height="28" rx="1.5" fill="#8C6A43" stroke="#6B5338" stroke-width="1.2"/>
        <circle cx="340" cy="52" r="6" fill="#C0533A"/>
        <path d="M336.5 52 H343.5" stroke="#FFFCF6" stroke-width="2" stroke-linecap="round"/>
        <!-- lavička pod dielňou a strom -->
        <rect x="300" y="112" width="42" height="9" rx="2" fill="#A07A4E" stroke="#6B5338" stroke-width="1.5"/>
        <path d="M304 121 V126 M338 121 V126" stroke="#6B5338" stroke-width="2" stroke-linecap="round"/>
        <circle cx="394" cy="152" r="26" fill="#7D8B4A"/><circle cx="372" cy="138" r="13" fill="#93A15E"/>
        <!-- šmykľavka -->
        <rect x="226" y="118" width="22" height="110" rx="10" fill="#D98B5F" stroke="#9E5A37" stroke-width="2"/>
        <rect x="262" y="110" width="30" height="32" rx="3" fill="#E6D5B5" stroke="#8C6A43" stroke-width="2"/>
        <path d="M248 126 H262" stroke="#8C6A43" stroke-width="2"/>
        <!-- kaďa so svetielkami -->
        <rect x="48" y="202" width="160" height="94" rx="8" fill="#E3C9A0" stroke="#8C6A43" stroke-width="2"/>
        <circle cx="128" cy="249" r="40" fill="#C9A86E" stroke="#6B5338" stroke-width="3"/>
        <circle cx="128" cy="249" r="29" fill="#9CC3C9"/>
        <path d="M52 196 C90 192 160 200 204 196" fill="none" stroke="#8C7A62" stroke-width="1.2"/>
        <g fill="#E8C774">{bulbs}</g>
        <!-- kamenný múrik pod kaďou cez celú úroveň -->
        <g stroke="#8C7A62" stroke-width="1">{wall}</g>
        <!-- detský domček, malé ohnisko s kotlíkom, strom -->
        <path d="M28 340 L49 318 L70 340 V364 H28Z" fill="#F1E4CB" stroke="#8C6A43" stroke-width="2" stroke-linejoin="round"/>
        <circle cx="106" cy="344" r="13" fill="#B9A57F" stroke="#6B5338" stroke-width="2"/>
        <circle cx="106" cy="344" r="7" fill="#3E3730"/>
        <path d="M106 344 L93 330 M106 344 L119 330 M106 344 V360" stroke="#5E4A33" stroke-width="1.5" stroke-linecap="round"/>
        <circle cx="170" cy="334" r="20" fill="#7D8B4A"/><circle cx="158" cy="322" r="10" fill="#93A15E"/>
        <!-- pieskovisko napravo nad altánkom -->
        <rect x="130" y="364" width="66" height="44" rx="6" fill="#EBD9A8" stroke="#A07A4E" stroke-width="4"/>
        <!-- altánok zarovno s domom: stôl s 10 stoličkami, gril, závesné kreslo, detská hojdačka -->
        <rect x="24" y="414" width="154" height="54" rx="6" fill="#E3C9A0" stroke="#8C6A43" stroke-width="2"/>
        <path d="M24 418 H178" stroke="#B5643A" stroke-width="5" stroke-linecap="round"/>
        <rect x="38" y="434" width="72" height="16" rx="3" fill="#C9A06A" stroke="#8C6A43" stroke-width="1.5"/>
        <g fill="#B07A43">{chairs}</g>
        <rect x="118" y="426" width="18" height="12" rx="2" fill="#4A4038" stroke="#2E2822" stroke-width="1.5"/>
        <circle cx="127" cy="454" r="6" fill="#F4EDE0" stroke="#8C7A62" stroke-width="1.5"/>
        <path d="M146 428 H172" stroke="#6B5338" stroke-width="3" stroke-linecap="round"/>
        <path d="M150 428 V442 M168 428 V442" stroke="#8C7A62" stroke-width="1.5"/>
        <rect x="146" y="441" width="26" height="6" rx="2" fill="#D98B5F" stroke="#9E5A37" stroke-width="1.2"/>
        <!-- dom -->
        <rect x="24" y="472" width="112" height="164" rx="8" fill="#FFFCF6" stroke="#6B5338" stroke-width="3"/>
        <path d="M30 478 H130" stroke="#B5643A" stroke-width="5" stroke-linecap="round"/>
        <text x="80" y="548" text-anchor="middle" font-family="Bitter" font-size="20" font-weight="600" fill="#3B301E" data-i18n="mp.house">Dom</text>
        <!-- tehlový chodník vedľa domu s drevenou lavičkou -->
        <rect x="140" y="472" width="38" height="164" rx="3" fill="#D29C7C" stroke="#A9694B" stroke-width="1.5"/>
        <path d="M159 472 V636 {bricks}" fill="none" stroke="#A9694B" stroke-width="1"/>
        <rect x="148" y="526" width="14" height="50" rx="2" fill="#A07A4E" stroke="#6B5338" stroke-width="1.5"/>
        <!-- kvety pri susedovom plote -->
        <g fill="#93A15E">{leaves}</g>
        <g>{blossoms}</g>
        <!-- plot -->
        <rect x="20" y="20" width="420" height="620" rx="18" fill="none" stroke="#B08A5A" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round"/>
        <!-- čísla podľa legendy -->
        <g font-family="Nunito" font-size="14" font-weight="600" text-anchor="middle">
{mk}
        </g>
      </svg>
'''
open(S + '/v5/areal_map.svg', 'w').write(svg)
