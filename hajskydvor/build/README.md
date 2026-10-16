# Hájsky dvor – ako vznikol web (skripty)

Skripty, ktorými sa ručne staval hajskydvor.sk (verzia 5, akvarelový štýl).
Sú tu ako referencia pre projekt LamaPage. Samostatne sa nespustia:
chýbajú medzivýsledky starších verzií a fotky (sú na hostingu v priečinkoch
`galeria/`, `vylety/`, `videa/`, `ostatne/`).

Hlavné poučenie: web vznikal ako reťaz úprav HTML pomocou regulárnych výrazov
(v1 → v2 → … → v5). Každá zmena faktu (sauna, počet lôžok) sa preto musela
robiť na viacerých miestach. LamaPage to má robiť opačne: dáta projektu
a šablóna, z ktorých sa web zostaví celý znova.

## Poradie krokov

1. `to_v5.py` – z návrhu 3 a 4 urobí kostru verzie 5 (akvarelový štýl, písma, CSS).
2. `photos_v5.py` – doplní fotky, izby, recenzie, FAQ, mapku areálu, výlety,
   cookie lištu a pätičku s prevádzkovateľom. Na konci sú úpravy podľa
   pripomienok klientky (bez sauny, lôžka, mapka zhora, výlety pešo z domu).
3. `build_v5.py` – vloží ikony, logo, fotky a videá ako base64, spojí preklady
   a skontroluje, že slovenský text v HTML sedí so slovníkom.
   Výstup: `../v5.html` (náhľad, všetko v jednom súbore, asi 5,5 MB).
4. `externalize.py` – z náhľadu urobí produkčný `../web/index.html`:
   obrázky a videá nahradí odkazmi na súbory (zhoda podľa md5). HTML má asi 556 KB.

## Súbory

| Súbor | Čo obsahuje |
|---|---|
| `photo_list.py` | zoznam fotiek: kľúč, kategória, popis, orez |
| `faq_data.py` | otázky a odpovede FAQ, popisy izieb, ďalšie tipy, v 6 jazykoch |
| `gen_areal_portrait.py` | kreslí mapku areálu pohľadom zhora → `casti/areal_map.svg` |
| `casti/consent_head.html` | Consent Mode v2: default denied a uložený súhlas, pred GTM |
| `casti/cookie_bar.html` | HTML cookie lišty |
| `casti/v5_script.html` | JavaScript stránky: preklady, galéria, reels, meranie (dataLayer), cookie lišta, tmavý režim |
| `casti/walk_block.html` | mapka výletov „z domu bez auta“ |
| `i18n/` | preklady kľúč → text; `v5_*` prepisuje staršie `v3_*`, `v2_*` a základné súbory |
| `kontroly/overflow5.js` | Playwright: 360 a 390 px × 6 jazykov, nič nepreteká do strany |
| `kontroly/check_ftp.js` | Playwright: produkčná verzia načíta všetky obrázky a videá zo súborov |
| `odovzdanie/build.py` | HTML pre odovzdávacie PDF (`../Hajsky-dvor-odovzdanie-webu.pdf`) |

Test merania a cookie lišty je v `../tests/datalayer.test.js`.
