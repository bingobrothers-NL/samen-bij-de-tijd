# Samen Bij de Tijd — ochtend- en avondeditie

## Wat werkt nu
- `index.html` is geschikt voor mobiele Safari en twee iPhones.
- Ochtend-/avondknoppen, artikelen met bronlinks, uitleg, gespreksvraag, quiz en voorlezen via de stemmen op het apparaat.
- `ochtend.json` bevat een **handmatig samengestelde editie van 13 november 2026**. Dit is geen live doorlopende nieuwsdienst.
- `update_news.py` leest recente openbare NOS-RSS-feeds en maakt een ochtend- of avondeditie. Deze automatische editie bevat RSS-beschrijvingen, **geen AI-geverifieerde analyse**. Quiz gaat voorlopig over rubrieken.
- Als de RSS-feeds niet bereikbaar zijn, faalt de update zonder de vorige editie te overschrijven.

## Publiceren en automatische updates activeren
1. Maak een GitHub-repository en upload alle bestanden, inclusief `.github/workflows/update.yml`.
2. Ga naar Settings > Pages > Build and deployment > Deploy from a branch > `main` / root > Save.
3. Ga naar Actions en activeer workflows wanneer GitHub daarom vraagt. Start `Nieuws vernieuwen om 08:00 en 18:00 (Nederland)` één keer handmatig via Run workflow.
4. Controleer of `ochtend.json` of `avond.json` is aangemaakt en of de website de editie toont.
5. Deel de GitHub Pages-URL met beide iPhones. Safari > Deel > Zet op beginscherm.

De GitHub Actions-cron draait op UTC en controleert de Nederlandse tijd, ook bij zomer-/wintertijd. GitHub Actions is niet gegarandeerd exact om 08:00 of 18:00; drukte kan vertraging veroorzaken. Zonder repository/hosting/ingeschakelde workflow **wordt morgen niets automatisch vernieuwd**.

## Bronnen en beperkingen
NOS openbare RSS-feeds: `feeds.nos.nl`. De nieuwsselectie kiest per categorie recente berichten en vult aan tot maximaal zeven, maar is nog geen redactionele ranking op impact. Browser-voorlezen is afhankelijk van beschikbare Nederlandse stemmen en garandeert geen mannenstem. Een aparte TTS-dienst is nodig om die te garanderen. Voor inhoudelijke nieuwsquiz en diepgaande gecontroleerde uitleg is extra serverlogica nodig.


## Nieuw design en actualiteit
De nieuwsfeed wordt met de workflow elk uur gecontroleerd. De app toont de laatste gepubliceerde editie en laadt deze opnieuw via de knop Vernieuw. GitHub Actions moet geactiveerd zijn en kan vertraging hebben. Het is geen live streaming nieuwsfeed. Video's linken naar NOS; automatisch ingesloten video's en AI-samenvattingen zijn niet geimplementeerd.


## Vernieuwd ontwerp
- Logo in `logo.svg` en cartoonpresentator in `nieuwslezer.png`.
- Nieuwskaarten met categorieafbeelding of RSS-afbeelding wanneer beschikbaar. Illustraties zijn geen journalistieke bronfoto's.
- Meer ruimte voor samenvatting en toelichting. De bron-RSS biedt soms slechts korte tekst: voor langere geverifieerde details moet de gebruiker het bronartikel openen.
- Let op: demo-artikelen zijn geen gegarandeerd actueel nieuws.

## Laatste ontwerp (13 november 2026)
- Geen foto of cartoonpersoon in de app; nieuw visueel hoofdscherm met een gestileerde wereldbol.
- Donkerblauwe achtergrond, oranje knoppen, compacte nieuwsafbeeldingen, uitgebreidere artikelen waar de RSS dat toelaat.
- Knop Vernieuw nieuws toont `daily.json`, de meest recent gepubliceerde editie.
- De app is NIET online en nieuws wordt NIET automatisch vernieuwd totdat GitHub Pages en GitHub Actions zijn geactiveerd.
- Nieuwsafbeeldingen kunnen bronafbeeldingen zijn indien de RSS die levert; anders illustraties.


## Verdieping in de app
Open een nieuwskaart met **Lees het verhaal**. De voorbeeldeditie bevat een uitgebreidere toelichting en context binnen de app. Voor nieuwe automatisch opgehaalde berichten is de beschikbare RSS-tekst beperkt: de app toont uitsluitend feitelijk beschikbare informatie en verzint geen artikelinhoud. Een uitgebreid automatisch journalistiek samenvattingssysteem vereist een aanvullende betrouwbare content-/samenvattingspipeline.


## Nieuwe sportpagina en langere verdieping
- Open `sport.html` of gebruik **Sport** in de onderste navigatie.
- De sportpagina heeft filters voor voetbal, Formule 1, wielrennen, tennis en overig.
- Offline toont sport.html duidelijk gemarkeerde algemene sportuitleg, **geen verzonnen actuele uitslagen**. Na publicatie maakt de workflow `sport.json` op basis van de NOS-sportfeed, wanneer deze bereikbaar is.
- De bestaande vijf handmatig samengestelde nieuwsvoorbeelden hebben langere achtergrondteksten. Automatische RSS-berichten blijven beperkt tot de beschikbare feedinformatie; er is nog geen AI-onderzoek of volledige artikelverdieping.

## Nieuwsafbeeldingen (nieuwe versie)
- Nieuwskaarten tonen waar beschikbaar de **originele foto uit de RSS-feed van de nieuwsbron**. Dit is niet automatisch bij elk bericht beschikbaar.
- Voor Microsoft-nieuws zonder bronfoto gebruikt de app `microsoft-logo.svg`, lokaal meegeleverd.
- Voor andere berichten zonder bronfoto blijft een neutrale categorieillustratie staan. We verzinnen geen nieuwsbeelden en kopiëren geen afbeeldingen van NOS of NU.nl buiten de beschikbare feed om.
- De automatische workflow blijft elk uur lopen en schrijft nieuwe `image`-velden in `daily.json` en `sport.json`.
- Upload de volledige inhoud van deze map naar de hoofdmap van je GitHub-repository. **Vervang bestaande bestanden** en voeg `microsoft-logo.svg` toe. De verborgen map `.github/workflows/update.yml` moet ook aanwezig blijven.
