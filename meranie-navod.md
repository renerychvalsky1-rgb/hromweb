# Server-side meranie HROM — čo je hotové a čo treba doplniť

## Čo je nasadené (funguje hneď po nahratí na FTP)

Súbor **`meranie.js`** je pripojený na všetkých 14 verejných stránkach.
Rieši štyri veci, ktoré sú predpokladom akéhokoľvek server-side merania:

| Vec | Prečo je dôležitá |
|---|---|
| **Zachytenie click ID** (`gclid`, `gbraid`, `wbraid`, `fbclid`, `msclkid`, `ttclid`) a UTM parametrov, uložené na **90 dní** | Bez toho sa rezervácia, ktorá príde o 3 dni, nedá priradiť ku kampani. Toto je jadro merania „booking ads". |
| **First-party `client_id`** v cookie na 400 dní | Prežije Safari ITP aj blokovanie 3rd-party cookies. |
| **`event_id` ku každej udalosti** | Deduplikácia medzi prehliadačom a serverom — Meta CAPI aj GA4 Measurement Protocol to vyžadujú, inak sa konverzie počítajú dvakrát. |
| **Odoslanie na server** (`CFG.ENDPOINT`) | Keď doplníš URL server kontajnera, udalosti idú aj mimo prehliadača → nezastaví ich adblock. |

### Merané udalosti

| Udalosť | Kedy sa spustí |
|---|---|
| `page_view_hrom` | zobrazenie stránky |
| `booking_click` | klik na demo/rezerváciu alebo na rezervačný systém (Reservio, Entradio, sterio.sk, mamkrcovezily.sk…) |
| `generate_lead` | odoslanie kontaktného formulára |
| `contact_call` | klik na telefónne číslo |
| `contact_email` | klik na e-mail |
| `select_service` | preklik na produktovú podstránku |
| `scroll_depth` | 25 / 50 / 75 / 90 % stránky |

Každá udalosť nesie so sebou `gclid`, `utm_campaign` a spol. — takže aj lead
odoslaný o týždeň neskôr vie server priradiť ku správnej kampani.

**Overené testom:** príchod z `?gclid=…&utm_campaign=chatboty` → preklik na inú
stránku bez parametrov → udalosť stále nesie `gclid` aj kampaň, `client_id` sa
nemení.

---

## Čo treba doplniť (bez toho beží len klientská vrstva)

### 1. Server-side GTM kontajner
Potrebujem od teba **URL server kontajnera** (napr. `https://sgtm.hrom.marketing`).
Ak ho ešte nemáš, treba ho vytvoriť — GTM → Server container → nasadiť
(Google Cloud Run ~15 €/mes., alebo lacnejšie cez Stape.io).
Potom v `meranie.js` vyplníš:

```js
ENDPOINT: 'https://sgtm.hrom.marketing',
```

### 2. Prístupy pre jednotlivé platformy
| Platforma | Čo potrebujem |
|---|---|
| **Meta (Facebook/Instagram)** | Pixel ID + **Conversions API token** |
| **Google Ads** | Conversion ID + conversion label pre každú akciu (lead, booking) |
| **GA4** | Measurement ID + API secret |

Tie sa vkladajú **do server kontajnera**, nie do webu — preto ich sem nepíš do kódu.

### 3. Súhlas (GDPR)
Web zatiaľ nemá cookie lištu. Server-side meranie sleduje ľudí rovnako ako
klientské — GDPR platí. Odporúčam nasadiť consent banner (napr. Cookiebot,
CookieYes) a v `meranie.js` prepnúť `SEND_USER_DATA` na `true` až po súhlase.
E-mail/telefón sa smie posielať len pre Enhanced Conversions a server ich
**musí zahashovať SHA-256** pred odoslaním do Meta/Google.

---

## ⚠️ Dôležité obmedzenie pri rezerváciách

`booking_click` meria **klik smerom k rezervácii**, nie dokončenú rezerváciu.
Keď sa rezervácia dokončí na **cudzom systéme** (Reservio, Entradio, softvér
ambulancie), prehliadač o tom nemá ako vedieť — tam sa už náš kód nespustí.

Na meranie **dokončených** rezervácií treba jedno z:

1. **Webhook / postback** z rezervačného systému na server kontajner
   (Reservio aj Entradio to vedia — treba si vypýtať prístup).
   Pri rezervácii sa pošle `gclid` + hodnota → server to pošle do Google/Meta
   ako reálnu konverziu s tržbou.
2. **Offline conversion import** — export rezervácií s `gclid` a nahratie
   do Google Ads (aj manuálne, raz týždenne).
3. Ak je rezervačný formulár na vlastnej doméne (Connector), stačí naň pridať
   `meranie.js` a jeden riadok `hromTrack('booking_complete', {value: 120, currency:'EUR'})`.

Bez toho vieš optimalizovať kampane len na klik k rezervácii — čo je lepšie
než nič, ale nie je to skutočná konverzia.

---

## Ručné volanie udalosti

Kdekoľvek v kóde:

```js
hromTrack('booking_complete', { value: 120, currency: 'EUR', service: 'AI chatbot' });
```

## Ladenie

V `meranie.js` prepni `DEBUG: true` a v konzole prehliadača uvidíš každú udalosť
aj s atribúciou.
