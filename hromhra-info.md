# HROM HRA — ako je to zapojené

Stránka `hromhra.html` je pripojená na **Supabase projekt HROM**
(`hsdjsgpwxgkkwpijeufv`, eu-west-1). Nič nemusíte nastavovať — stačí nahrať
`hromhra.html` a `logo.png` na FTP a hra aj rebríček fungujú.

## Čo je v databáze

**Tabuľka `hra_hraci`**

| stĺpec | čo je v ňom |
|---|---|
| `meno` | meno, ktoré hráč zadal (zobrazuje sa v rebríčku) |
| `email` | e-mail hráča, unikátny — jeden hráč = jeden riadok |
| `skore` | koľko faktov vytočil (0–100) |
| `vytvorene` | kedy sa prihlásil prvýkrát |
| `naposledy` | kedy naposledy hral |

**Dve funkcie, cez ktoré ide všetko**

- `hra_zapis(meno, email, skore)` — založí hráča alebo **zvýši** jeho skóre.
  Nižšie skóre nikdy neprepíše vyššie, takže hráč si výsledok nepokazí.
- `hra_rebricek(email, limit)` — vráti TOP hráčov. **Vracia iba meno a skóre.**
  E-maily z tejto funkcie nikdy neodchádzajú, aj keby ju niekto volal priamo.

## Prečo je to bezpečné

Kľúč v HTML (`sb_publishable_…`) je **verejný a je určený do prehliadača** — to nie je
únik. Podstatné je, čo sa s ním dá:

- na tabuľku `hra_hraci` sa cez neho **priamo dostať nedá** (RLS je zapnuté a tabuľka
  nemá žiadnu policy, takže priame čítanie aj zápis sú zamietnuté),
- funkčné je len tých dvoch funkcií vyššie,
- e-maily hráčov teda z webu nikto nevytiahne.

Bezpečnostný linter Supabase kvôli tomu hlási dve upozornenia
(*„RLS enabled no policy"* a *„Public can execute SECURITY DEFINER function"*).
**Pri tomto riešení sú očakávané — presne takto to má byť nastavené.** Sú to
upozornenia typu „skontroluj, či si to chcel", nie chyby.

## Ako sa dostanete k e-mailom

V Supabase → **Table Editor → `hra_hraci`**. Alebo v SQL editore:

```sql
select meno, email, skore, vytvorene
from hra_hraci
order by skore desc;
```

Export do CSV je v Table Editore vpravo hore (**Export**).

## Užitočné príkazy

Vynulovať rebríček pred novou kampaňou:

```sql
truncate table hra_hraci;
```

Vymazať jedného hráča (napr. na jeho žiadosť podľa GDPR):

```sql
delete from hra_hraci where email = 'niekto@firma.sk';
```

Zmeniť, koľko hráčov sa zobrazuje v rebríčku: v `hromhra.html` hodnota `TOP: 10`.

## Koľko volaní to spotrebuje

Hra nevolá databázu po každom točení. Zapisuje pri prihlásení, potom
**každých 5 faktov**, pri 100. fakte a keď hráč odchádza zo stránky. Jeden hráč,
ktorý vytočí všetkých 100 faktov, urobí asi 22 zápisov a 22 čítaní. Free tier
Supabase to znesie aj pri tisícoch hráčov.

## Ochrana údajov

Zbierate meno a e-mail, takže ide o osobné údaje. Pri kampani myslite na to, aby:

- pri QR kóde alebo na plagáte bolo jasné, kto údaje zbiera a prečo,
- ste mali kam odkázať na zásady spracovania osobných údajov,
- ste vedeli hráča na požiadanie vymazať (príkaz vyššie).
