# HROM HRY — ako sú zapojené

Obe hry sú pripojené na **Supabase projekt HROM** (`hsdjsgpwxgkkwpijeufv`, eu-west-1).
Nič nemusíte nastavovať — stačí nahrať súbory na FTP a hry aj rebríčky fungujú.

| Hra | Súbor | Tabuľka | QR kód |
|---|---|---|---|
| 100 faktov o reklame | `hromhra.html` | `hra_hraci` | `hromhra-qr.svg` |
| HROM SKOK (skákajúci blesk) | `hromskok.html` | `hra_skok` | `hromskok-qr.svg` |

Obe hry zdieľajú prihlásenie — kto sa prihlásil v jednej, v druhej už meno a e-mail
zadávať nemusí. Z každej hry vedie odkaz na tú druhú.

**Na FTP patria:** `hromhra.html`, `hromskok.html`, `logo.png`.
QR súbory sú pre tlačiara, tento návod je len pre vás.

## Čo je v databáze

### Hra o faktoch — tabuľka `hra_hraci`

| stĺpec | čo je v ňom |
|---|---|
| `meno` | meno, ktoré hráč zadal (zobrazuje sa v rebríčku) |
| `email` | e-mail hráča, unikátny — jeden hráč = jeden riadok |
| `skore` | koľko faktov vytočil (0–100) |
| `vytvorene` | kedy sa prihlásil prvýkrát |
| `naposledy` | kedy naposledy hral |

Funkcie: `hra_zapis(meno, email, skore)` a `hra_rebricek(email, limit)`.

### HROM SKOK — tabuľka `hra_skok`

Rovnaké stĺpce plus `pokusy` (koľkokrát hráč hral). Skóre je vzdialenosť v metroch.

Funkcie: `skok_zapis(meno, email, skore)` a `skok_rebricek(email, limit)`.

### Ako funkcie fungujú

- `*_zapis` založí hráča alebo **zvýši** jeho skóre. Nižšie skóre nikdy neprepíše
  vyššie, takže si hráč výsledok nepokazí ďalším horším pokusom.
- `*_rebricek` vráti TOP hráčov a **vracia iba meno a skóre**. E-maily z nej nikdy
  neodchádzajú, aj keby ju niekto volal priamo.

## Prečo je to bezpečné

Kľúč v HTML (`sb_publishable_…`) je **verejný a je určený do prehliadača** — to nie je
únik. Podstatné je, čo sa s ním dá:

- na tabuľky `hra_hraci` a `hra_skok` sa cez neho **priamo dostať nedá** (RLS je
  zapnuté a tabuľky nemajú žiadnu policy, takže priame čítanie aj zápis sú zamietnuté),
- funkčné sú len tie štyri funkcie vyššie,
- e-maily hráčov teda z webu nikto nevytiahne.

Bezpečnostný linter Supabase kvôli tomu hlási dve upozornenia
(*„RLS enabled no policy"* a *„Public can execute SECURITY DEFINER function"*).
**Pri tomto riešení sú očakávané — presne takto to má byť nastavené.** Sú to
upozornenia typu „skontroluj, či si to chcel", nie chyby.

## Ako sa dostanete k e-mailom

V Supabase → **Table Editor → `hra_hraci`**. Alebo v SQL editore:

```sql
-- hráči z hry o faktoch
select meno, email, skore, vytvorene from hra_hraci order by skore desc;

-- hráči z HROM SKOK
select meno, email, skore, pokusy from hra_skok order by skore desc;

-- všetky e-maily z oboch hier naraz, bez duplicít
select distinct email, max(meno) as meno from (
  select email, meno from hra_hraci
  union all
  select email, meno from hra_skok
) x group by email;
```

Export do CSV je v Table Editore vpravo hore (**Export**).

## Užitočné príkazy

Vynulovať rebríček pred novou kampaňou:

```sql
truncate table hra_hraci;   -- hra o faktoch
truncate table hra_skok;    -- HROM SKOK
```

Vymazať jedného hráča (napr. na jeho žiadosť podľa GDPR):

```sql
delete from hra_hraci where email = 'niekto@firma.sk';
delete from hra_skok  where email = 'niekto@firma.sk';
```

Zmeniť, koľko hráčov sa zobrazuje v rebríčku: hodnota `TOP: 10` v HTML danej hry.

## Koľko volaní to spotrebuje

Hra o faktoch nevolá databázu po každom točení — zapisuje pri prihlásení, potom
každých 5 faktov, pri 100. fakte a keď hráč odchádza zo stránky. HROM SKOK zapisuje
raz na konci každého pokusu. Pri oboch hrách ide o jednotky až desiatky volaní na
hráča, čo free tier Supabase znesie aj pri tisícoch ľudí.

## Ochrana údajov

Zbierate meno a e-mail, takže ide o osobné údaje. Pri kampani myslite na to, aby:

- pri QR kóde alebo na plagáte bolo jasné, kto údaje zbiera a prečo,
- ste mali kam odkázať na zásady spracovania osobných údajov,
- ste vedeli hráča na požiadanie vymazať (príkaz vyššie).
