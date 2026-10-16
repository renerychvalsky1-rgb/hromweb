import sys, os
D = sys.argv[1]
brush = open(os.path.join(D, 'brush.txt')).read()
TOTAL = 4
def foot(n): return f'<div class="foot"><span>Hájsky dvor · odovzdanie webu</span><span>{n} / {TOTAL}</span></div>'
def table(head, rows, cls=''):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

sections = table(['Časť', 'Čo v nej hostia nájdu'], [
    ['Úvod', '3 striedajúce sa fotky domu, „Celá chalupa pre vašu rodinu, kúsok od vodopádov“, tlačidlá na rezerváciu'],
    ['Izby', 'spálňa na prízemí, vedľa nej detská izba (prechodné), 2 samostatné spálne v podkroví, kúpeľňa; spolu 10 lôžok, 2 detské postele Montessori a 2 postieľky'],
    ['Kaďa a záhrada', 'vonkajšia kaďa v cene, ohnisko s kotlíkom, jedlá záhrada'],
    ['Pre deti', 'detský kútik, ihrisko, pieskovisko, hračky'],
    ['Galéria', '35 fotiek, otvárajú sa na celú obrazovku'],
    ['Videá', '4 ukážky z Instagramu s odkazmi na celé videá'],
    ['Mapka areálu', 'nakreslená podľa vášho náčrtu, 15 očíslovaných miest'],
    ['Okolie', 'výlety rovno z domu bez auta a 12 tipov podľa ročných období'],
    ['Hodnotenia', 'Booking.com 9,7 (22 hodnotení), Megaubytovanie 9,9 (5 hodnotení), 4 citáty hostí'],
    ['Časté otázky', '14 otázok: príchod, kaďa, lôžka, čo si priniesť, pravidlá'],
    ['Rezervácia a kontakt', 'odkazy na portály, telefón, e-mail, adresa Háj 83, mapa, Instagram, Facebook'],
], 'two')
tasks = [
    'Prejdite si web na mobile aj na počítači a pošlite Renému pripomienky.',
    'Prečítajte si stránku <b>Ochrana osobných údajov</b> (hajskydvor.sk/ochrana-osobnych-udajov.html). Je to právny text firmy VOLTOM s.r.o. s kontaktom na poverenca info@voltom.sk.',
    'Plaťte včas faktúry z WebSupportu za doménu a hosting. Pri nezaplatenej faktúre web prestane fungovať.',
    'Pridajte odkaz <b>https://hajskydvor.sk</b> do profilu na Instagrame a na Facebooku.',
    'Ak ešte nemáte Firemný profil Google, založte si ho s adresou Háj 83 a odkazom na web. Hostia vás tak nájdu v Mapách Google.',
    'Prihláste sa do Google Analytics (analytics.google.com) účtom <b>hajskydvor@gmail.com</b>. Uvidíte tam, koľko ľudí na web chodí.',
]
task_html = '<ul class="tasks">' + ''.join(f'<li><i></i><span>{t}</span></li>' for t in tasks) + '</ul>'
changes = table(['Čo sa zmenilo', 'Čo poslať Renému'], [
    ['Vybavenie, lôžka, izby', 'čo pribudlo alebo ubudlo'],
    ['Príchod, odchod, poplatky', 'nové časy a sumy (teraz príchod 15:00 – 23:59, odchod 7:00 – 10:00, skorší príchod alebo neskorší odchod 60 €)'],
    ['Nové fotky alebo videá', 'fotky v plnej kvalite cez Google Drive, pri videu odkaz na Instagram'],
    ['Hodnotenia na portáloch', 'nové skóre a počet hodnotení, na webe sú zadané ručne'],
    ['Recenzia, ktorú chcete ukázať', 'text recenzie, meno hosťa a portál'],
    ['Telefón, e-mail, sociálne siete', 'nový kontakt alebo odkaz'],
    ['Tipy na výlety', 'názov miesta, a či sa tam dá ísť pešo z domu'],
], 'two')
tech = table(['Čo', 'Kde', 'Poznámka'], [
    ['Doména a hosting', 'WebSupport, váš účet voltomhajskydvor', 'súbory webu a fotky sú na FTP'],
    ['Zabezpečenie (HTTPS)', 'WebSupport, certifikát Let\'s Encrypt', 'obnovuje sa sám, teraz platí do 12. 1. 2027'],
    ['Meranie návštevnosti', 'Google Tag Manager (GTM-57KFFMZ4) a Google Analytics 4 (G-GZV49VR3M4)', 'meria aj kliknutia na rezerváciu, telefón, e-mail, videá, galériu a mapu; prístup má hajskydvor@gmail.com'],
    ['Vyhľadávanie Google', 'Google Search Console', 'mapa stránok: hajskydvor.sk/sitemap.xml'],
    ['AI vyhľadávače', 'súbor llms.txt na webe', 'fakty o chalupe pre ChatGPT, Claude, Perplexity a pod.'],
], 'three')

html = f'''<!DOCTYPE html>
<html lang="sk"><head><meta charset="utf-8"><title>Hájsky dvor – odovzdanie webu</title>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@500;600;700&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Nunito', sans-serif; color: #4A3B2D; font-size: 10pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .page {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; background: #F7EFE1; page-break-after: always; padding: 16mm 17mm 0; }}
  .page:last-child {{ page-break-after: auto; }}
  .page::before {{ content: ''; position: absolute; right: -30mm; top: -26mm; width: 110mm; height: 80mm; border-radius: 50%; background: radial-gradient(closest-side, rgba(211,168,119,.22), rgba(211,168,119,0)); }}
  .page::after {{ content: ''; position: absolute; left: -36mm; bottom: -20mm; width: 120mm; height: 80mm; border-radius: 50%; background: radial-gradient(closest-side, rgba(147,161,94,.18), rgba(147,161,94,0)); }}
  .page > * {{ position: relative; z-index: 1; }}
  h1, h2, h3 {{ font-family: 'Bitter', serif; font-weight: 600; line-height: 1.15; color: #3F2F22; }}
  h2 {{ font-size: 19pt; margin-bottom: 1mm; }}
  h2::after {{ content: ''; display: block; width: 38mm; height: 4mm; margin-top: 1.6mm; background: {brush} left center / 100% 100% no-repeat; }}
  .eyebrow {{ display: block; font-size: 8.5pt; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: #A06E3A; }}
  p {{ margin-top: 2.5mm; color: #594836; }}
  .lead {{ font-size: 10.5pt; }}
  section + section {{ margin-top: 9mm; }}
  b {{ color: #3F2F22; }}
  .foot {{ position: absolute; left: 0; right: 0; bottom: 0; height: 12mm; display: flex; justify-content: space-between; align-items: center; padding: 0 17mm; font-size: 8.5pt; color: #8C7A66; border-top: .3mm solid rgba(58,46,34,.12); z-index: 2; }}

  /* titulka */
  .cover .top {{ display: flex; align-items: center; gap: 5mm; }}
  .cover .logo {{ width: 22mm; height: 22mm; border-radius: 4mm; }}
  .cover h1 {{ font-size: 30pt; margin: 6mm 0 1.5mm; }}
  .cover h1 em {{ font-style: normal; color: #6A7A50; }}
  .cover .url {{ font-size: 13pt; color: #6A7A50; font-weight: 800; }}
  .browser {{ margin-top: 7mm; border-radius: 4mm; overflow: hidden; box-shadow: 0 3mm 9mm rgba(58,46,34,.18); border: .3mm solid rgba(58,46,34,.15); background: #fff; }}
  .browser .bar {{ height: 7mm; background: #EEE4D2; display: flex; align-items: center; gap: 1.6mm; padding: 0 4mm; }}
  .browser .bar i {{ width: 2.6mm; height: 2.6mm; border-radius: 50%; background: #C9B89A; display: block; }}
  .browser .bar span {{ margin-left: 4mm; font-size: 8pt; color: #6A7A50; background: #F7F1E6; border-radius: 2mm; padding: .6mm 4mm; font-weight: 700; }}
  .browser img {{ width: 100%; display: block; }}
  .features {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2.2mm 8mm; margin-top: 7mm; list-style: none; font-size: 10pt; }}
  .features li {{ display: flex; gap: 2.5mm; }}
  .features li::before {{ content: ''; flex: 0 0 2.4mm; height: 2.4mm; margin-top: 1.5mm; border-radius: 50%; background: #93A15E; }}
  .note {{ margin-top: 6mm; font-size: 10pt; color: #4A3B2D; background: #EEE4D2; border-left: 1.2mm solid #6A7A50; padding: 3.5mm 4.5mm; border-radius: 0 2.5mm 2.5mm 0; }}
  .made {{ position: absolute; left: 17mm; right: 17mm; bottom: 17mm; display: flex; justify-content: space-between; font-size: 9pt; color: #85725A; }}

  /* tabuľky */
  table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 4mm; background: #FCF7EC; border: .3mm solid rgba(74,59,45,.14); border-radius: 3mm; overflow: hidden; font-size: 9.4pt; line-height: 1.42; }}
  th {{ text-align: left; background: #EEE4D2; color: #3F2F22; font-weight: 800; font-size: 8.6pt; letter-spacing: .03em; padding: 2.4mm 3.5mm; }}
  td {{ padding: 2.3mm 3.5mm; border-top: .3mm solid rgba(74,59,45,.10); vertical-align: top; color: #4A3B2D; }}
  td:first-child {{ font-weight: 700; color: #3F2F22; }}
  table.two td:first-child {{ width: 40mm; }}
  table.three td:first-child {{ width: 36mm; }}
  table.three td:nth-child(2) {{ width: 58mm; }}

  /* úlohy */
  .tasks {{ list-style: none; margin-top: 4mm; display: grid; gap: 2.6mm; }}
  .tasks li {{ display: flex; gap: 3.2mm; background: #FCF7EC; border: .3mm solid rgba(74,59,45,.14); border-radius: 2.5mm; padding: 2.6mm 3.5mm; font-size: 9.6pt; line-height: 1.45; }}
  .tasks i {{ flex: 0 0 4.4mm; height: 4.4mm; margin-top: .3mm; border: .5mm solid #6A7A50; border-radius: 1.1mm; background: #fff; }}

  .closing {{ display: grid; grid-template-columns: 1fr 52mm; gap: 9mm; align-items: start; }}
  .phone {{ width: 52mm; border: 2.2mm solid #2E2418; border-radius: 8mm; overflow: hidden; background: #2E2418; box-shadow: 0 2mm 6mm rgba(58,46,34,.18); }}
  .phone img {{ width: 100%; display: block; }}
  figcaption {{ text-align: center; font-size: 8.5pt; color: #85725A; margin-top: 2mm; }}
  .contact {{ margin-top: 7mm; background: #FCF7EC; border: .3mm solid rgba(74,59,45,.14); border-radius: 3mm; padding: 4mm 5mm; }}
  .contact h3 {{ font-size: 12pt; margin-bottom: 1mm; }}
</style></head><body>

<section class="page cover">
  <div class="top"><img class="logo" src="logo.png" alt=""><span class="eyebrow">Odovzdanie webu · október 2026</span></div>
  <h1>Web Hájsky dvor<br><em>je spustený</em></h1>
  <div class="url">https://hajskydvor.sk</div>
  <p class="lead">Web beží na WebSupporte so zabezpečeným pripojením, v 6 jazykoch, s cookie lištou a meraním návštevnosti. V tomto dokumente je, čo na ňom je, čo urobiť vy a čo poslať, keď sa niečo zmení.</p>
  <div class="browser"><div class="bar"><i></i><i></i><i></i><span>🔒 hajskydvor.sk</span></div><img src="hero.jpg" alt=""></div>
  <ul class="features">
    <li>6 jazykov: SK, HU, EN, DE, PL, UA</li>
    <li>Prispôsobený mobilu, svetlý aj tmavý režim</li>
    <li>Zabezpečené pripojenie (HTTPS)</li>
    <li>Vlastná cookie lišta podľa GDPR</li>
    <li>Meranie návštevnosti v Google Analytics</li>
    <li>Pripravený pre Google aj AI vyhľadávače</li>
  </ul>
  <div class="note">Doména aj hosting sú kúpené na vašom účte vo WebSupporte, takže sa k webu dostanete kedykoľvek. Heslá v tomto dokumente nie sú.</div>
  <div class="made"><span>Pripravil: René Rychvalský, HROM Marketing</span><span>Pre: Denisa a Tomáš Kapasní</span></div>
  {foot(1)}
</section>

<section class="page">
  <section>
    <span class="eyebrow">Prehľad</span>
    <h2>Čo je na webe</h2>
    <p>Web je jedna stránka v 6 jazykoch, so svetlým aj tmavým režimom a prispôsobená mobilu. V päte je prevádzkovateľ VOLTOM s.r.o. s IČO, odkaz na Ochranu osobných údajov a Nastavenia cookies.</p>
    {sections}
  </section>
  <section>
    <span class="eyebrow">Rezervácie</span>
    <h2>Rezervácie a kontakt</h2>
    <p>Web sám rezervácie neprijíma a neukazuje ceny. Tlačidlá „Rezervovať“ a „Overiť voľný termín“ vedú na Booking.com, Megaubytovanie.sk a Airbnb, kde sú aktuálne ceny a voľné termíny. <b>Ceny a dostupnosť teda meníte len na portáloch, na webe netreba nič.</b></p>
    <p>Na webe je telefón +421 908 864 513 s poznámkou, že rezervácie uprednostňujete cez portály, a e-mail hajskydvor@gmail.com. Pri zdieľaní odkazu na WhatsApp alebo Facebook sa ukáže fotka domu a krátky popis chalupy.</p>
  </section>
  {foot(2)}
</section>

<section class="page">
  <section>
    <span class="eyebrow">Teraz po spustení</span>
    <h2>Úlohy pre vás</h2>
    <p>Web nemá administráciu, texty a fotky v ňom mení René. Od vás treba len tieto kroky:</p>
    {task_html}
  </section>
  <section>
    <span class="eyebrow">Zmeny</span>
    <h2>Keď sa niečo zmení</h2>
    <p>Pošlite Renému podklady a on web upraví vo všetkých 6 jazykoch.</p>
    {changes}
  </section>
  {foot(3)}
</section>

<section class="page">
  <section>
    <span class="eyebrow">Technika</span>
    <h2>Kde web beží</h2>
    <p>Doména aj hosting sú kúpené na vašom účte vo WebSupporte, takže sa k webu dostanete kedykoľvek.</p>
    {tech}
  </section>
  <section class="closing">
    <div>
      <span class="eyebrow">GDPR</span>
      <h2>Cookies a ochrana osobných údajov</h2>
      <p>Web má vlastnú cookie lištu v 6 jazykoch s tlačidlami Prijať všetky, Odmietnuť a Nastavenia. Google Analytics ukladá cookies až po súhlase návštevníka a voľba sa pamätá 12 mesiacov. Návštevník ju zmení cez „Nastavenia cookies“ v päte.</p>
      <p>V štatistikách preto uvidíte len návštevníkov, ktorí súhlasili. Stránka Ochrana osobných údajov uvádza prevádzkovateľa VOLTOM s.r.o., poverenca Ing. Tomáša Kapasného a aké údaje web spracúva.</p>
      <div class="contact"><h3>S čímkoľvek sa ozvite</h3>René Rychvalský, HROM Marketing. Pošlite fotky, zmeny alebo otázky a web upravím.</div>
    </div>
    <figure><div class="phone"><img src="m_hero.jpg" alt=""></div><figcaption>Web na mobile</figcaption></figure>
  </section>
  {foot(4)}
</section>
</body></html>'''
open(os.path.join(D, 'odovzdanie.html'), 'w').write(html)
print('ok')
