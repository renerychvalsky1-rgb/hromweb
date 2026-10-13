# SEO a AI vyhľadávače – hajskydvor.sk

Web pôjde ako čisté HTML s fotkami (bez WordPressu). Tieto súbory patria do koreňa domény `https://hajskydvor.sk/` vedľa `index.html`:

| Súbor | Kam | Na čo |
|---|---|---|
| `robots.txt` | `/robots.txt` | povolí Google, Bing aj AI asistentov (ChatGPT, Claude, Perplexity, Gemini…) |
| `sitemap.xml` | `/sitemap.xml` | 6 jazykových verzií s hreflang odkazmi |
| `llms.txt` | `/llms.txt` | stručné fakty o chalupe pre AI asistentov (po anglicky, s miestnymi názvami) |
| `og-image.jpg` | `/og-image.jpg` | obrázok pri zdieľaní na Facebooku, WhatsAppe a pod. (1200 × 630) |

Priamo v stránke sú pripravené:
- štruktúrované dáta JSON-LD: `LodgingBusiness` (adresa, telefón, e-mail, vybavenie, kapacita, jazyky, odkazy na portály), `WebSite`, `FAQPage` z častých otázok,
- hreflang odkazy na jazykové verzie, kanonický odkaz (dopĺňa ho skript podľa jazyka), Open Graph, `geo.region` a `geo.placename`.

Pred spustením:
1. Odstrániť `<meta name="robots" content="noindex, nofollow">` zo stránky.
2. Doplniť presné súradnice (pravý klik na špendlík v Google Mapách): `geo.position`, `ICBM` a `geo` v JSON-LD.
3. Fotky a videá dať ako samostatné súbory (napr. `/img/`, `/video/`) namiesto vložených v HTML – stránka bude rýchlejšia.
4. Odporúčanie pre AI vyhľadávače: jazykové verzie vygenerovať ako samostatné statické stránky (`/hu/`, `/en/`…). AI roboti väčšinou nespúšťajú JavaScript, takže na `?lang=hu` by videli slovenský text. Potom upraviť adresy v `sitemap.xml` a hreflang.
5. Overiť profil Instagramu `@hajsky_dvor` (je aj v JSON-LD a `llms.txt`).
6. Po spustení: Google Search Console a Bing Webmaster Tools – pridať doménu a odoslať sitemapu.
