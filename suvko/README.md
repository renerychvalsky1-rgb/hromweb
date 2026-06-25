# SUVKO — podklad nového webu (dizajn manuál 2026)

Statický **podklad / náhľad pre klienta**. Tri podstránky zjednotené do nového
dizajn manuálu SUVKO 2026. Nie je to finálna produkčná verzia — slúži ako základ
na schválenie smeru a ďalšiu prácu.

## Podstránky
| Súbor | Stránka |
|---|---|
| `index.html` | **Domov** — hero, oblasti partnerstva, avokádo koncept (Poznanie / Zručnosť / Skúsenosť), prehľad služieb, tím, kontakt |
| `sluzby.html` | **Služby** — vlajkový program *Zrelá firma* + **7 avokádových rozvojových ciest** (s obsahom a rozbaľovacím HPLJ), meranie potenciálu, rozvíjanie kultúry, metóda HPLJ |
| `test-zrelej-firmy.html` | **Test zrelej firmy** — landing s diagnostikou 7 oblastí a ukážkou výsledku |

Zdieľané: `styl.css` (dizajn systém), `app.js` (mobilné menu, reveal, animácia barov).

## Dizajn tokeny (z manuálu)
| Token | HEX | Použitie |
|---|---|---|
| Žltá | `#FFCF06` | akcenty, CTA, slovná značka |
| Tmavomodrá | `#052452` | plochy, gradient |
| Navy | `#0D1833` | tmavé pozadia, text na svetlom |
| Tyrkysová | `#21AAB4` | nadpisové akcenty, ikony |
| Zelená | `#7AD093` | doplnok symbolu |
| Krémová | `#F5F1E8` | svetlé sekcie |

## Typografia — POZOR (substitúcia)
Manuál predpisuje **Forma DJR Micro** (text) a **Grover Heavy** (logo/display).
Sú to **komerčné fonty** — v tomto podklade sú dočasne nahradené najbližšími
bezplatnými z Google Fonts:

- Forma DJR Micro → **Hanken Grotesk**
- Grover Heavy → **Fredoka** (slovná značka SUVKO)

Pre finálny web treba doplniť **licencované woff2** súbory a prepísať
`--font` / `--display` v `styl.css`.

## Logo
Symbol avokáda je v podklade **dočasná SVG rekonštrukcia** (tyrkysovo-zelené
oblúky + žltá kvapka) podľa manuálu. Vo finále nahradiť **oficiálnym logo assetom**
(manuál: logo sa nesmie prekresľovať).

## Spustenie
Statické HTML — stačí otvoriť `index.html` v prehliadači. Bez buildu, bez závislostí.

> Formuláre sú zatiaľ nefunkčné (`onsubmit` blokovaný) — pred nasadením napojiť na
> reálny endpoint / e-mail službu.
