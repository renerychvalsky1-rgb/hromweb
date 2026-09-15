# HROM HRA — zapnutie rebríčka a zberu e-mailov

Stránka `hromhra.html` funguje aj bez tohto nastavenia — hra sa hrá, e-maily chodia cez
web3forms do schránky. **Rebríček sa však zobrazí až vtedy, keď stránku pripojíte na
Google tabuľku.** Nastavenie zaberie asi 5 minút a je zadarmo.

Zároveň tým vyriešite zber e-mailov: namiesto jedného e-mailu za každého hráča vám
mená, adresy a skóre padajú rovno do tabuľky.

---

## 1. Vytvorte tabuľku

1. Choďte na [sheets.new](https://sheets.new) a vytvorte novú tabuľku.
2. Pomenujte ju napríklad **HROM HRA — hráči**.

## 2. Vložte skript

1. V tabuľke choďte na **Rozšírenia → Apps Script**.
2. Zmažte, čo je v editore, a vložte celý obsah súboru **`hromhra-leaderboard.gs`**.
3. Kliknite na ikonu diskety (Uložiť projekt).

## 3. Nasaďte ako webovú aplikáciu

1. Vpravo hore **Nasadiť → Nové nasadenie**.
2. Pri „Vyberte typ" kliknite na ozubené koliesko a zvoľte **Webová aplikácia**.
3. Nastavte:
   - **Spustiť ako:** Ja (váš účet)
   - **Kto má prístup:** **Ktokoľvek** ← toto je dôležité, inak hra k tabuľke nedočiahne
4. **Nasadiť** → Google si vypýta povolenie → **Povoliť**.
5. Skopírujte **URL webovej aplikácie**. Vyzerá takto:
   `https://script.google.com/macros/s/AKfycb.../exec`

## 4. Vložte adresu do stránky

V súbore `hromhra.html` nájdite (je hneď na začiatku skriptu dole):

```js
var CFG = {
  API: '',
```

a vložte skopírovanú adresu:

```js
var CFG = {
  API: 'https://script.google.com/macros/s/AKfycb.../exec',
```

Uložte a nahrajte `hromhra.html` na FTP. Hotovo.

---

## Čo sa deje potom

- Po prihlásení a po každom točení sa do tabuľky zapíše **meno, e-mail a skóre**.
- Jeden e-mail = jeden riadok. Skóre sa iba zvyšuje, nikdy neprepíše vyšší výsledok nižším.
- Pod hrou sa zobrazí **rebríček TOP 10** — kto vytočil najviac faktov.
- Hráč vidí v rebríčku **len mená**, nie e-maily. E-maily zostávajú v tabuľke.
- Vlastný riadok hráča je v rebríčku zvýraznený a označený „— vy".

## Keď skript neskôr upravíte

Po každej zmene v Apps Scripte musíte urobiť **Nasadiť → Spravovať nasadenia → ceruzka →
Verzia: Nová verzia → Nasadiť.** Bez toho beží stále stará verzia.

## Koľko hráčov to znesie

Apps Script má denný limit, ktorý pri bežnej plagátovej kampani nedosiahnete
(rádovo tisíce volaní denne). Stránka volá server pri prihlásení a potom najviac raz
za sekundu pri točení — pri stovkách hráčov je to bez problémov.

## Ochrana údajov

Zbierate meno a e-mail, takže ide o osobné údaje. Pri kampani myslite na to, aby:
- pri QR kóde alebo na plagáte bolo jasné, kto údaje zbiera a prečo,
- ste mali kam odkázať na zásady spracovania osobných údajov,
- ste vedeli hráča na požiadanie z tabuľky vymazať.
