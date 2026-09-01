# lamaon.com — marketingový web

**Verzia 1.0 · Návrh štruktúry, copy a dizajnového smeru**
Postavené na Brand booku V1.0 (august 2026). Predávame platformu lamaon.com — nikdy jednotlivé produkty.

> **Poznámka k rodine produktov:** Brief spomínal staršie pracovné mená (lamaboost, lamasure, LamaCinema). Brand book V1.0 ich nepozná a definuje rodinu: lamapage, lamatrack, lamazap, lamatax, lamacare, lamadesk, lamascope, lamademo. Tento dokument sa drží brand booku. Vlajkový účtovný asistent (60 €/rok pre platiteľa DPH) = **lamatax**.

---

## 0. Globálny dizajnový systém (platí pre celý web)

### Farby
- **Hero a master momenty:** výhradne master gradient `#ED1E24 → #F7911E`, 90°. Tam, kde gradient technicky nejde (favicon, jednofarebné plochy), plná `#ED3706`.
- **Produktové farby** sa objavujú **iba vnútri produktových kariet** — nikde inde na stránke. Žiadna dúha.
- **Žiadne sivé.** Paleta je čierna `#000000` a biela `#FFFFFF`. Jemnejšie tóny = čierna so zníženým krytím (napr. text 60 %, vypnuté stavy 15–20 %), nikdy nová farba. Toto je zároveň mechanika stavu OFF: „vypnuté" veci sú čierna s nízkym krytím, „zapnuté" veci majú farbu.

### Typografia
- Jedno písmo: **Poppins**. Bold 700 (slovo „lama", zvýraznenia), SemiBold 600 (nadpisy, prestrk −0,025 em), Regular 400 (text, riadkovanie 1,6), Light 300 (suffixy, úvodné vety, veľké citáty).
- Malé popisky (labely sekcií, badge) verzálkami s prestrkom +0,12 em.
- Logika „lama bold + suffix light" sa prepisuje do nadpisov: kľúčové slovo bold, zvyšok light. Príklad: „**Zapni** si lamu."

### Ústredná metafora: vypínač
- **Primárne CTA** je fyzicky tvarované ako toggle: pilulka s kruhovým paličkovým prvkom vľavo; na hover sa palička presunie doprava a pozadie prejde z čiernej 15 % do gradientu. Klik = zapnutie.
- **Sekcie sa „zapínajú"** pri scrolle: obsah vstupuje v čiernej so zníženým krytím a pri dosiahnutí viewportu „cvakne" do plnej farby/krytia (150–200 ms, ease-out, jemný posun 8 px hore). Žiadne dlhé fade-iny — cvaknutie, nie rozplývanie.
- **Preloader:** bežiaca lama v slučke (sivá silueta = čierna 20 %), po načítaní doskočí do stredu, prepne prepínač v tele a gradient sa zaleje. Trvanie max 1,2 s, potom sa už nikdy nezobrazuje (session cookie).
- `prefers-reduced-motion`: všetky animácie sa nahradia okamžitým prepnutím stavu bez pohybu.

### Hlavička
Horizontálny lockup vľavo, výška znaku 32 px, dodržaná ochranná zóna. Navigácia: Ako to funguje · Produkty · Príbeh · Cenník. Vpravo jediné CTA-toggle „Zapnúť". Hlavička biela, pri scrolle jemný blur, žiadny tieň s farbou.

### Jazyk
Claim vždy a všade po slovensky: **„Zapni si lamu."** Nikdy sa neprekladá. Telo webu: [SITE LANGUAGE — Slovak / English]; nižšie je copy v slovenčine (primárny trh) + anglická verzia každého bloku pre EÚ mutáciu.

### Hlas
Krátke vety. Slovesá. Žiadne superlatívy, žiadne „revolučné". Číslo alebo ticho. Nikdy sa neospravedlňujeme za AI. Nesľubujeme, že pomáha — nahrádza.

---

## 1. Hero

**Layout:** Celá obrazovka, gradientová plocha `#ED1E24 → #F7911E`. Vertikálny lockup (znak nad logotypom) v strede hore, claim pod ním, jedna podporná veta, jedno CTA. Nič iné — žiadne screenshoty, žiadne floating karty.

**Copy (SK):**
- Headline: **Zapni si lamu.**
- Subhead: Jedna platforma, ktorá robí prácu namiesto teba. Účtovníctvo, web, automatizácie — zapneš a beží.
- CTA: **Zapnúť** *(toggle button, biely na gradiente)*
- Mikrotext pod CTA: Jeden účet. Jedna peňaženka. Kredity míňaš len na to, čo je zapnuté.

**Copy (EN):**
- Headline: **Zapni si lamu.** *(never translated; small caption on EN mutation: "Turn on your llama.")*
- Subhead: One platform that does the work instead of you. Accounting, web, automations — switch it on and it runs.
- CTA: **Switch on**
- Microcopy: One account. One wallet. Credits are spent only on what's switched on.

**Dizajn/motion:** Toto je moment podpisovej animácie. Pri načítaní stojí logo sivé (biela 30 % na gradiente… presnejšie: znak v bielej so zníženým krytím), prepínač v polohe OFF. Lama „pribehne" zľava (2D silueta, 6–8 frameov), skočí do znaku, prepínač cvakne do ON a znak sa zaleje plnou bielou; súčasne sa doostrí claim. Celé do 1,5 s. Headline: „Zapni" Bold 700, „si lamu." Light 300 — presná logika logotypu. Scroll cue: malý prepínač, ktorý sa sám prepne a odscrolluje stránku.

---

## 2. Ako to funguje

**Layout:** Biela sekcia, tri kroky vedľa seba (mobil: pod sebou). Každý krok je karta s veľkou číslicou a jedným piktogramom v štýle znaku. Label sekcie verzálkami: `AKO TO FUNGUJE`.

**Copy (SK):**
- Headline: Jeden účet. Všetky lamy.
- Subhead: lamaon nie je balík nástrojov. Je to vypínač — každý produkt je ďalšia lama, ktorú zapneš.

- **01 — Zapni si účet.** Jedna adresa, jedno prihlásenie: lamaon.com. Žiadne ďalšie heslá, žiadne ďalšie faktúry.
- **02 — Nabi peňaženku.** Jedna peňaženka, kredity. Míňajú sa len vtedy, keď lama pracuje. Vidíš každý pohyb.
- **03 — Prepínaj lamy.** Účtovníctvo, web, automatizácie. Zapneš, čo potrebuješ. Vypneš, čo nepotrebuješ. Bez viazanosti.

- CTA: **Zapnúť účet**

**Copy (EN):**
- Headline: One account. All the llamas.
- Subhead: lamaon isn't a bundle of tools. It's a switch — every product is another llama you turn on.
- 01 — Switch on your account. One address, one login: lamaon.com. No extra passwords, no extra invoices.
- 02 — Top up the wallet. One wallet, credits. Spent only while a llama is working. You see every move.
- 03 — Flip the llamas. Accounting, web, automations. Turn on what you need. Turn off what you don't. No lock-in.
- CTA: **Switch on your account**

**Dizajn/motion:** Každá karta má v rohu malý toggle; pri vstupe do viewportu sa postupne (stagger 120 ms) prepnú do ON a číslica prejde z čiernej 20 % do čiernej 100 %. Piktogramy čierne, žiadna farba — farby patria produktom.

---

## 3. Produktová mriežka

**Layout:** Biela sekcia, mriežka 4×2 (tablet 2×4, mobil 1 stĺpec). Každá karta = jedna lama: silueta znaku so symbolom produktu, meno („lama" bold + suffix light), jedna veta, toggle v pravom hornom rohu. **Východiskový stav OFF: celá karta čierna v 15–20 % krytí.** Hover/tap: toggle cvakne, silueta aj akcenty sa zalejú farbou produktu, veta stmavne na 100 %. lamatax je zapnutá už pri načítaní — vlajková loď svieti ako jediná.

**Copy (SK):**
- Label: `RODINA LÁM`
- Headline: Každá lama vie jednu vec. Poriadne.
- Subhead: Všetky žijú na jednej adrese a na jednej peňaženke. Kupuješ platformu, nie nástroje.

| Lama | Farba | Symbol | Veta na karte (SK) | Veta na karte (EN) |
|---|---|---|---|---|
| **lama**tax | `#1B3B6F` | percento | Pošli doklady. Podané. | Send the documents. Filed. |
| **lama**page | `#48A0FF` | bublina | Povedz, čo predávaš. Stránka stojí. | Say what you sell. The page is up. |
| **lama**track | `#4D309C` | graf | Vidíš, čo funguje. Bez tabuliek. | See what works. No spreadsheets. |
| **lama**zap | `#23B35B` | blesk | Čo robíš dvakrát, už nerobíš. | Whatever you do twice, you stop doing. |
| **lama**care | `#009B72` | kríž | Ambulancia, ktorá dvíha, aj keď nikto nedvíha. | The clinic that picks up when nobody picks up. |
| **lama**desk | `#E5007D` | headset | Asistentka, ktorá nespí. | The assistant that doesn't sleep. |
| **lama**scope | `#8E1F3E` | lupa | Zadanie prečíta skôr, než ho draho pochopíš. | Reads the brief before you pay to understand it. |
| **lama**demo | `#00B4D8` | play | Vyskúšaj si zákazku nanečisto. | Test-run the job before it's real. |

- Poznámka pod mriežkou: Nové lamy pribúdajú. Subdoména sa zapína až s produktom.
- CTA: žiadne samostatné CTA na kartách — klik na zapnutú kartu vedie na subdoménu (tax.lamaon.com…), karta v stave OFF vedie na kotvu cenníka. Produkty sa tu nepredávajú ani necenia.

**Copy (EN):** Label `THE LLAMA FAMILY` · Headline: Every llama does one thing. Properly. · Subhead: They all live at one address, on one wallet. You buy the platform, not the tools. · Footnote: New llamas keep coming. A subdomain switches on only with its product.

**Dizajn/motion:** Jediné miesto na webe, kde sa objavujú produktové farby — a vždy len vnútri karty. Toggle cvaknutie: 150 ms, prepínač sa presunie, farba sa zaleje radiálne od prepínača (od tela lamy von). Zvuk žiadny. Na mobile stav ON spúšťa tap, druhý tap otvára subdoménu.

---

## 4. Príbeh slova „lama"

**Layout:** Úzka textová sekcia na čiernom podklade, biely text, veľký citát v Light 300. Krátka — max 5 viet. Znak lamy jednofarebne biely s vyrezaným prepínačom, malý, v rohu.

**Copy (SK):**
- Label: `PREČO LAMA`
- Veľký citát (Light 300): „Lama" sa kedysi hovorilo tomu, kto hru nevedel hrať.
- Body: My to slovo otáčame. V účtovníctve si lama? Presne preto ho nemáš robiť ty. Zapneš lamu, ktorá to hrá za teba — a hrá to dobre. Byť v niečom lama prestalo byť problém. Stalo sa to dôvodom.
- Bodka na záver (Bold 700): Prácu spraví ona.

**Copy (EN):**
- Label: `WHY A LLAMA`
- Quote: "Lama" is what gamers used to call the player who couldn't play.
- Body: We flip the word. Clueless about accounting? That's exactly why you shouldn't be doing it. You switch on a llama that plays it for you — and plays it well. Being a "lama" at something stopped being a problem. It became the reason.
- Closer: The llama does the work.

**Dizajn/motion:** Sebavedomý, žartovný tón — nikdy výsmech používateľa; terčom vtipu je značka a slovo, nie človek. Sekcia sa „zapne" inverzne: čierny podklad nabehne cvaknutím, text vstúpi z bielej 20 % do bielej 100 %. Žiadny gradient, žiadna produktová farba — čisto čiernobiely moment.

---

## 5. Dôvera a princípy

**Layout:** Biela sekcia, tri stĺpce s krátkym titulkom a dvomi vetami. Bez ikoniek zo stockových sád — len typografia a tenké linky. Label: `AKO PRACUJEME`.

**Copy (SK):**
- Headline: Nemáme AI vo firme. Naša firma je AI.

- **AI Only, nie AI First.** lamaon od prvého dňa stavajú a prevádzkujú AI agenti. Nie je to vrstva na starej firme — je to celá firma. Používame AI a netajíme to.
- **Zákon 7 dní.** Každý nový produkt má funkčné MVP do siedmich dní. Buď to beží, alebo to nerobíme. Problém je pomalosť, nie chyba — chybu priznáme vetou a vyriešime ďalšou.
- **Staviame pre EÚ.** Európske firmy, európske pravidlá, európske termíny. Faktúry, podania a dáta tak, ako ich vyžaduje tvoj štát, nie Silicon Valley.

- Riadok pod stĺpcami (verzálky, +0,12 em): NESĽUBUJEME, ŽE POMÁHA. NAHRÁDZA.

**Copy (EN):**
- Headline: We don't have AI in the company. The company is AI.
- **AI Only, not AI First.** lamaon has been built and run by AI agents since day one. Not a layer on an old firm — the whole firm. We use AI and we don't hide it.
- **The 7-day law.** Every new product ships a working MVP within seven days. Either it runs, or we don't do it. Slowness is the problem, not mistakes — a mistake gets admitted in one sentence and fixed in the next.
- **Built for the EU.** European businesses, European rules, European deadlines. Invoices, filings and data the way your country requires — not Silicon Valley.
- Strapline: WE DON'T PROMISE IT HELPS. IT REPLACES.

**Dizajn/motion:** Žiadne vymyslené logá klientov, žiadne čísla, ktoré nemáme. Keď budú reálne referencie a metriky, pribudne tenký pás: „[CLIENT] · [METRIC]" — dovtedy sekcia stojí na princípoch, nie na dôkazoch, a je to priznané dizajnom: čisté, strohé, bez ozdôb.

---

## 6. Cenník — teaser

**Layout:** Sekcia na gradientovej ploche (druhý a posledný výskyt gradientu na stránke — rám hero ↔ cenník). Biely text. Jedna cenová kotva, vysvetlenie kreditov, jedno CTA. Žiadna cenová tabuľka produktov.

**Copy (SK):**
- Headline: Účtovník za 60 € na rok.
- Subhead: Toľko stojí lamatax pre platiteľa DPH. Zvyšok platformy funguje na kreditoch — jedna peňaženka, míňaš len to, čo je zapnuté.
- Tri riadky (odrážky s malým prepínačom namiesto guľky):
  - Účet aj peňaženka zadarmo. Platíš, až keď lama pracuje.
  - Kredity platia naprieč všetkými lamami. Žiadne balíčky pre každý nástroj zvlášť.
  - Vypneš kedykoľvek. Kredity nezhoria, viazanosť neexistuje.
- CTA: **Zapnúť lamu**
- Mikrotext: Ceny s DPH. Podrobný cenník nájdeš po prihlásení v peňaženke.

**Copy (EN):**
- Headline: An accountant for €60 a year.
- Subhead: That's lamatax for a VAT payer. The rest of the platform runs on credits — one wallet, you spend only on what's switched on.
- Bullets: Account and wallet are free — you pay only when a llama works. · Credits work across every llama — no per-tool bundles. · Switch off anytime. Credits don't expire, there's no lock-in.
- CTA: **Switch on your llama**
- Microcopy: Prices include VAT. The full price list lives in your wallet after login.

**Dizajn/motion:** Číslo „60 €" je najväčší typografický prvok sekcie (Poppins SemiBold, mierne zväčšený prestrk pre čísla podľa brand booku). Pozor na tón: peňaženka a kredity sú úžitkové slová — nikdy „investícia", „zhodnotenie", „zarábaj". Nič, čo by pripomínalo krypto alebo finančné poradenstvo. Slovo „tokeny" sa na webe nesmie objaviť ani raz — vždy „kredity".

---

## 7. Pätička

**Layout:** Čierny podklad, biely horizontálny lockup (plná biela s vyrezaným prepínačom), tri úzke stĺpce + spodný právny riadok.

**Copy (SK):**
- Stĺpec 1 — Platforma: Ako to funguje · Rodina lám · Cenník · Prihlásenie
- Stĺpec 2 — Firma: Príbeh · Kontakt: office@lamaon.com
- Stĺpec 3 — Právne: Obchodné podmienky · Ochrana osobných údajov · Cookies
- Spodný riadok: © [YEAR] LAMAON.COM s.r.o. · lamaon.com je jediná adresa, ktorú si musíš pamätať.

**Copy (EN):**
- Platform: How it works · The llama family · Pricing · Log in
- Company: Story · Contact: office@lamaon.com
- Legal: Terms · Privacy · Cookies
- Bottom line: © [YEAR] LAMAON.COM s.r.o. · lamaon.com is the only address you need to remember.

**Dizajn/motion:** Bez gradientu (tmavý podklad = plná biela verzia loga podľa brand booku). Jediný easter egg webu: malý prepínač úplne dole; kliknutie prepne stránku do „OFF" — celý web na sekundu zosivie (čierna 15 %) a cvakne späť. Raz za reláciu.

---

## Poznámky k realizácii

1. **Poradie sekcií na stránke:** Hero → Ako to funguje → Produktová mriežka → Príbeh „lama" → Princípy → Cenník teaser → Pätička. Gradient sa vyskytuje presne dvakrát (hero, cenník) — stránka tak začína aj vrcholí značkou.
2. **Konverzná logika:** jeden cieľ celej stránky = registrácia účtu („Zapnúť"). Všetky CTA vedú na ten istý signup; produktové karty vedú na subdomény len v stave ON. Nikde sa nepredáva jednotlivý produkt, jediná cena na stránke je kotva 60 €/rok.
3. **Interná definícia** „AI, ktoré uľahčuje život" sa v žiadnom viditeľnom texte nepoužíva.
4. **SEO/meta:** title „lamaon — Zapni si lamu." · description (SK): „Jedna platforma, ktorá robí prácu namiesto teba. Jeden účet, jedna peňaženka, kredity. Zapni si lamu na lamaon.com." OG obrázok: znak v gradiente na bielej.
5. **Favicon:** plná `#ED3706`, znak bez prepínača (podľa brand booku — odznak sa v 16 px zlieva).
6. **Referencie a čísla:** do webu sa nedopĺňajú, kým nie sú reálne. Vyhradené placeholdery: [CLIENT], [METRIC].
