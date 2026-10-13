# SEO a AI vyhľadávače – hajskydvor.sk

Súbory pripravené na koreň domény `https://hajskydvor.sk/`:

| Súbor | Kam | Na čo |
|---|---|---|
| `robots.txt` | `/robots.txt` | povolí Google, Bing aj AI asistentov (ChatGPT, Claude, Perplexity, Gemini…), zakáže len `/wp-admin/` |
| `sitemap.xml` | `/sitemap.xml` | 6 jazykových verzií s hreflang odkazmi |
| `llms.txt` | `/llms.txt` | stručné fakty o chalupe pre AI asistentov (po anglicky, s miestnymi názvami) |
| `og-image.jpg` | `/og-image.jpg` | obrázok pri zdieľaní na Facebooku, WhatsAppe a pod. (1200 × 630) |

Priamo v stránke (`v5.html`) sú pripravené:
- štruktúrované dáta JSON-LD: `LodgingBusiness` (adresa, telefón, vybavenie, kapacita, odkazy na portály), `WebSite`, `FAQPage` z častých otázok,
- hreflang odkazy na jazykové verzie, kanonický odkaz (dopĺňa ho skript podľa jazyka), Open Graph, `geo.region` a `geo.placename`.

Pred spustením:
1. Odstrániť `<meta name="robots" content="noindex, nofollow">` zo stránky.
2. Doplniť presné súradnice (pravý klik na špendlík v Google Mapách): `geo.position`, `ICBM` a `geo` v JSON-LD.
3. Ak bude web na WordPresse s jazykmi na adresách `/hu/`, `/en/`… (Polylang/WPML), upraviť adresy v `sitemap.xml` a hreflang, prípadne nechať sitemapu generovať Yoast/Rank Math a v `robots.txt` zmeniť riadok `Sitemap:`.
4. Overiť profil Instagramu `@hajsky_dvor` (je aj v JSON-LD a `llms.txt`).
5. Po spustení: Google Search Console a Bing Webmaster Tools – pridať doménu a odoslať sitemapu.
