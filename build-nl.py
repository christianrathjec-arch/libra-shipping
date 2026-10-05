import re
PAGES=['index','chartering','agency','contact','conditions','disclaimer','privacy']
def rep(s, pairs, name):
    for a,b in pairs:
        if s.count(a)==0: raise SystemExit(f'MISSING in {name}: {a[:70]}')
        s=s.replace(a,b)
    return s
COMMON=[
 ('<html lang="en">','<html lang="nl">'),
 ('aria-label="Libra Shipping B.V. — home"','aria-label="Libra Shipping B.V. — startpagina"'),
 ('<nav class="nav" aria-label="Main">','<nav class="nav" aria-label="Hoofdmenu">'),
 ('<p>Specialist in coastal shipping. Since 1976.</p>','<p>Specialist in kustvaart. Sinds 1976.</p>'),
 ('<span class="certsub">certified &middot;','<span class="certsub">gecertificeerd &middot;'),
 ('<p>Waalhaven Oostzijde 85<br><span class="num">3087 BM</span> Rotterdam<br>The Netherlands</p>','<p>Waalhaven Oostzijde 85<br><span class="num">3087 BM</span> Rotterdam<br>Nederland</p>'),
 ('<div class="ft">Antwerp</div>\n        <p>Cadixstraat 23<br><span class="num">2000</span> Antwerp<br>Belgium</p>','<div class="ft">Antwerpen</div>\n        <p>Cadixstraat 23<br><span class="num">2000</span> Antwerpen<br>België</p>'),
 ('LinkedIn &rarr; [page URL]','LinkedIn &rarr; [pagina-URL]'),
 ('Libra Shipping B.V. &mdash; Rotterdam &middot; Antwerp</span>','Libra Shipping B.V. &mdash; Rotterdam &middot; Antwerpen</span>'),
 ('>Terms &amp; Conditions</a>','>Algemene voorwaarden</a>'),
 ('>Privacy statement</a>','>Privacyverklaring</a>'),
 ('KvK 24126021 &middot; VAT NL003589390B01','KvK 24126021 &middot; btw NL003589390B01'),
]
PANEL=[
 ('<a class="btn" href="contact.html">Contact us</a>','<a class="btn" href="contact.html">Neem contact op</a>'),
 ('<div class="lab">Telephone</div>','<div class="lab">Telefoon</div>'),
 ('<div class="lab">Email</div>','<div class="lab">E-mail</div>'),
 ('<h2>Our team.</h2>','<h2>Ons team.</h2>'),
]
GMP=[('<strong>GMP+ certified.</strong> Feed cargoes are handled under the Feed Safety Assurance scheme, audited by an independent body.',
      '<strong>GMP+ gecertificeerd.</strong> Diervoederladingen worden afgehandeld volgens het Feed Safety Assurance-schema, gecontroleerd door een onafhankelijke instantie.')]
T={}
T['index']=[
 ('<title>Libra Shipping B.V. — Ship brokers and agents, Rotterdam</title>','<title>Libra Shipping B.V. — Scheepsmakelaars en scheepsagenten, Rotterdam</title>'),
 ('Ship brokers and agents &middot; Rotterdam &middot; Antwerp &middot; since 1976','Scheepsmakelaars en scheepsagenten &middot; Rotterdam &middot; Antwerpen &middot; sinds 1976'),
 ('<h1>Maritime solutions for logistics challenges</h1>','<h1>Maritieme oplossingen voor logistieke uitdagingen</h1>'),
 ('<p>Established in 1976, Libra Shipping is the maritime and logistics service provider offering world-wide sea transport solutions and ship agencies in the Netherlands and Belgium.</p>',
  '<p>Libra Shipping, opgericht in 1976, is de maritieme en logistieke dienstverlener die wereldwijde zeetransportoplossingen en scheepsagentuur biedt in Nederland en België.</p>'),
 ('<p>No matter what size, cargo type or trade, our skilled and experienced team will be able to find the vessel that suits your needs at the right time and right price.</p>',
  '<p>Ongeacht omvang, ladingsoort of vaargebied: ons deskundige en ervaren team vindt het schip dat bij uw behoefte past, op het juiste moment en tegen de juiste prijs.</p>'),
 ('<span class="kvhead">Excellent services</span><span class="kvcap">with competitive rates and high-quality subcontractors</span>','<span class="kvhead">Uitstekende dienstverlening</span><span class="kvcap">tegen concurrerende tarieven en met hoogwaardige onderaannemers</span>'),
 ('<span class="num">24/7</span> manned office</span><span class="kvcap">by experienced operators</span>','<span class="num">24/7</span> bemand kantoor</span><span class="kvcap">door ervaren operators</span>'),
 ('<span class="kvhead">Tailor-made solutions</span><span class="kvcap">for an efficient port turnaround</span>','<span class="kvhead">Oplossingen op maat</span><span class="kvcap">voor een efficiënte afhandeling in de haven</span>'),
 ('<h2>One desk for the vessel and the cargo. Since 1976.</h2>','<h2>Eén loket voor schip en lading. Sinds 1976.</h2>'),
 ('<p>Libra Shipping has been a ship broker and ship agent in Rotterdam since 1976: a chartering desk in the Waalhaven that fixes dry cargo on sea-going vessels worldwide, and its own agencies in the Netherlands and Belgium, covering every port in the ARA range.</p>',
  '<p>Libra Shipping is sinds 1976 scheepsmakelaar en scheepsagent in Rotterdam: een bevrachtingsafdeling in de Waalhaven die wereldwijd droge lading op zeeschepen bevracht, en eigen agenturen in Nederland en België voor alle havens in de ARA-range.</p>'),
 ('<p>One call is enough. Whoever picks up knows both the vessel and the cargo, because each of our operators is dedicated to a vessel type and a cargo. The office is manned around the clock by experienced people. Safety comes first, always. Everything else is built around a fast, cost-efficient port turnaround.</p>',
  '<p>Eén telefoontje is genoeg. Wie opneemt, kent zowel het schip als de lading, omdat elk van onze operators gespecialiseerd is in een scheepstype en een ladingsoort. Het kantoor is dag en nacht bemand door ervaren mensen. Veiligheid staat altijd voorop. Al het overige is gericht op een snelle, kostenefficiënte afhandeling in de haven.</p>'),
 ('<h3>Chartering</h3>\n          <p>We find the vessel that fits your cargo best and coordinate loading and discharging to enable a smooth turnaround.</p>',
  '<h3>Bevrachting</h3>\n          <p>Wij vinden het schip dat het best bij uw lading past en coördineren het laden en lossen voor een vlotte afhandeling.</p>'),
 ('<h3>Agency</h3>\n          <p>Ship&rsquo;s agents in Rotterdam and Antwerp, available 24/7, focused on a safe, smooth and efficient port turnaround.</p>',
  '<h3>Agentuur</h3>\n          <p>Scheepsagenten in Rotterdam en Antwerpen, 24/7 bereikbaar, gericht op een veilige, vlotte en efficiënte afhandeling in de haven.</p>'),
 ('Read more &rarr;','Lees meer &rarr;'),
 ('<h2>One partner for all types of cargo.</h2>','<h2>Eén partner voor alle soorten lading.</h2>'),
 ('<span class="tag">Agricultural products</span><span class="tag">Minerals</span><span class="tag">Fertilisers</span><span class="tag">Salt</span>','<span class="tag">Agrarische producten</span><span class="tag">Mineralen</span><span class="tag">Meststoffen</span><span class="tag">Zout</span>'),
 ('<span class="tag">Steel products</span><span class="tag">Project cargoes</span><span class="tag">Ferro alloys</span>','<span class="tag">Staalproducten</span><span class="tag">Projectlading</span><span class="tag">Ferrolegeringen</span>'),
 ('<h2>Tell us the cargo and route. We tell you the logistics cost.</h2>','<h2>Geef ons de lading en de route. Wij geven u de logistieke kosten.</h2>'),
 ('alt="Loaded bulk carrier under way on a grey sea"','alt="Beladen bulkcarrier varend op een grijze zee"'),
 ('alt="Bulk terminal with a vessel loading"','alt="Bulkterminal met een schip onder belading"'),
]+PANEL
T['chartering']=[
 ('<title>Chartering — Libra Shipping B.V.</title>','<title>Bevrachting — Libra Shipping B.V.</title>'),
 ('Chartering &middot; freight calculation &middot; forwarding','Bevrachting &middot; vrachtcalculatie &middot; expeditie'),
 ('<h1>Your maritime specialist</h1>','<h1>Uw maritieme specialist</h1>'),
 ('Voyage or time charter, bulk, break-bulk or project cargo: one desk that finds the right ship for your parcel, anywhere in the world.','Reis- of tijdbevrachting, bulk, stukgoed of projectlading: één loket dat wereldwijd het juiste schip vindt voor uw partij.'),
 ('<h2>What chartering means for you.</h2>','<h2>Wat bevrachting voor u betekent.</h2>'),
 ('<p>You have cargo to move. We find the vessel that fits best and coordinate loading and discharging to enable a smooth turnaround.</p>','<p>U heeft lading te vervoeren. Wij vinden het schip dat het best past en coördineren het laden en lossen voor een vlotte afhandeling.</p>'),
 ('<p>One point of contact will ensure a reliable and carefree maritime solution.</p>','<p>Eén aanspreekpunt zorgt voor een betrouwbare en zorgeloze maritieme oplossing.</p>'),
 ('<p>We have in-house expertise in the short sea shipping markets covering, amongst others, the North Sea, the Atlantic, the Mediterranean and the Baltic. Additionally we are well positioned to cover your sea transport requirements worldwide.</p>',
  '<p>Wij hebben eigen expertise in de shortsea-markten, waaronder de Noordzee, de Atlantische Oceaan, de Middellandse Zee en de Oostzee. Daarnaast zijn wij goed gepositioneerd om wereldwijd in uw zeetransportbehoefte te voorzien.</p>'),
 ('<p>Besides sea transportation, we are able to arrange cargo handling, warehousing and on-carriage by barges, train and trucks as well as relevant customs formalities if required.</p>',
  '<p>Naast het zeetransport kunnen wij ook de ladingbehandeling, opslag en het natransport per binnenvaart, spoor en vrachtwagen verzorgen, evenals de benodigde douaneformaliteiten.</p>'),
 ('<p class="figunit">metric tonnes</p>','<p class="figunit">ton</p>'),
 ('<p class="figcap">Whatever the parcel size, there is a ship for it.</p>','<p class="figcap">Voor elke partijgrootte is er een schip.</p>'),
 ('<h2>What we fix.</h2>','<h2>Wat wij voor u afsluiten.</h2>'),
 ('<h3>Voyage charter</h3>\n          <p>One cargo, one voyage: we fix the vessel for a single shipment, load port to discharge port.</p>','<h3>Reisbevrachting</h3>\n          <p>Eén lading, één reis: wij bevrachten het schip voor een enkele zending, van laadhaven tot loshaven.</p>'),
 ('<h3>Time charter</h3>\n          <p>A vessel at your disposal for a period, with the crew and the day-to-day operation taken care of.</p>','<h3>Tijdbevrachting</h3>\n          <p>Een schip voor een bepaalde periode tot uw beschikking, met bemanning en dagelijkse operatie geregeld.</p>'),
 ('<h3>Freight calculation</h3>\n          <p>We calculate ocean freight costs to assist our customers in buying and selling goods.</p>','<h3>Vrachtcalculatie</h3>\n          <p>Wij berekenen de zeevrachtkosten om onze klanten te ondersteunen bij de in- en verkoop van goederen.</p>'),
 ('<span class="fwd-eyebrow">Beyond the ship</span>\n          <h3>Forwarding</h3>','<span class="fwd-eyebrow">Voorbij het schip</span>\n          <h3>Expeditie</h3>'),
 ('<p>Where others stop at the fixture, we can also arrange everything around it: the legs before and after the sea voyage, the paperwork, the storage. One partner for the full shipment.</p>',
  '<p>Waar anderen stoppen bij de bevrachting, kunnen wij ook alles eromheen regelen: het voor- en natransport, de documenten, de opslag. Eén partner voor de hele zending.</p>'),
 ('Explained below &darr;','Hieronder uitgelegd &darr;'),
 ('<h3 class="fwd-h">The ship is our trade. The cargo does not stop at the port.</h3>','<h3 class="fwd-h">Het schip is ons vak. De lading stopt niet in de haven.</h3>'),
 ('<p>Chartering is everything about finding and fixing the ship. Forwarding is everything about moving the cargo through the chain, from the factory gate to the receiver&rsquo;s yard. The two overlap on the sea leg, and that is exactly where Libra sits. Once we have fixed the vessel, we can take care of the rest of your supply chain.</p>',
  '<p>Bevrachting draait om het vinden en vastleggen van het schip. Expeditie draait om het vervoer van de lading door de hele keten, van de fabriekspoort tot het terrein van de ontvanger. De twee overlappen op het zeetraject, en precies daar zit Libra. Zodra wij het schip hebben bevracht, kunnen wij ook de rest van uw logistieke keten verzorgen.</p>'),
 ('<li>Pre- and on-carriage by barge, rail or road</li>','<li>Voor- en natransport per binnenvaart, spoor of weg</li>'),
 ('<li>Transhipment and storage</li>','<li>Overslag en opslag</li>'),
 ('<li>Shipping documents, bills of lading</li>','<li>Scheepsdocumenten, cognossementen</li>'),
 ('<li>Customs and export or import formalities</li>','<li>Douane- en in- of uitvoerformaliteiten</li>'),
 ('<li>Cargo handling, loading and discharge</li>','<li>Ladingbehandeling, laden en lossen</li>'),
 ('<li>Cargo insurance where needed</li>','<li>Transportverzekering waar nodig</li>'),
 ('<span class="cl">Source</span>','<span class="cl">Herkomst</span>'),('<span class="cl">Pre-carriage</span>','<span class="cl">Voortransport</span>'),
 ('<span class="cl">Load port</span>','<span class="cl">Laadhaven</span>'),('<span class="cl">Sea transport</span>','<span class="cl">Zeetransport</span>'),
 ('<span class="cl">Discharge port</span>','<span class="cl">Loshaven</span>'),('<span class="cl">On-carriage</span>','<span class="cl">Natransport</span>'),
 ('<span class="cl">Final destination</span>','<span class="cl">Eindbestemming</span>'),
 ('<a class="btn light" href="contact.html">Contact us</a>','<a class="btn light" href="contact.html">Neem contact op</a>'),
 ('<h2>Chartering and agency, one team.</h2>','<h2>Bevrachting en agentuur, één team.</h2>'),
 ('Once we have fixed the vessel, the same desk can handle her port call. No handover between broker and agent, nothing lost in between, one contact for both.','Zodra wij het schip hebben bevracht, kan hetzelfde team de havenaanloop verzorgen. Geen overdracht tussen makelaar en agent, niets gaat verloren, één contactpersoon voor beide.'),
 ('See what the agency does &rarr;','Bekijk wat de agentuur doet &rarr;'),
 ('<h2>Where we trade.</h2>','<h2>Waar wij actief zijn.</h2>'),
 ('aria-label="Map of the trading areas: North Sea, Baltic, Atlantic, Mediterranean, Black Sea and West Africa, with Rotterdam and Antwerp marked."','aria-label="Kaart van de vaargebieden: Noordzee, Oostzee, Atlantische Oceaan, Middellandse Zee, Zwarte Zee en West-Afrika, met Rotterdam en Antwerpen gemarkeerd."'),
 ('>North Sea</text>','>Noordzee</text>'),('>Baltic</text>','>Oostzee</text>'),('>Atlantic</text>','>Atlantische Oceaan</text>'),
 ('>Mediterranean</text>','>Middellandse Zee</text>'),('>Black Sea</text>','>Zwarte Zee</text>'),('>West Africa</text>','>West-Afrika</text>'),
 ('>Rotterdam &middot; Antwerp</text>','>Rotterdam &middot; Antwerpen</text>'),
 ('Every trade is different. <a href="contact.html">Tell us what you need to move &rarr;</a>','Elk vaargebied is anders. <a href="contact.html">Vertel ons wat u wilt vervoeren &rarr;</a>'),
 ('<h2>Interested in our services?</h2>','<h2>Interesse in onze diensten?</h2>'),
 ('alt="Bulk carrier seen from above"','alt="Bulkcarrier van bovenaf gezien"'),
]+PANEL+GMP
T['agency']=[
 ('<title>Agency — Libra Shipping B.V.</title>','<title>Agentuur — Libra Shipping B.V.</title>'),
 ('Ship&rsquo;s agency &middot; the Netherlands and Belgium','Scheepsagentuur &middot; Nederland en België'),
 ('<h1>We think in solutions</h1>','<h1>Wij denken in oplossingen</h1>'),
 ('Libra Shipping offers ship agency services in the Netherlands and Belgium.','Libra Shipping biedt scheepsagentuurdiensten in Nederland en België.'),
 ('<h2>Available 24/7 at our offices in Rotterdam and Antwerp.</h2>','<h2>24/7 bereikbaar op onze kantoren in Rotterdam en Antwerpen.</h2>'),
 ('<p>We focus on a safe, smooth and efficient port turnaround. Our employees have specialised knowledge of all types of vessels and cargoes, with a long track record.</p>',
  '<p>Wij richten ons op een veilige, vlotte en efficiënte afhandeling in de haven. Onze medewerkers hebben specialistische kennis van alle scheepstypen en ladingsoorten, met een lange staat van dienst.</p>'),
 ('<p>At Libra Shipping we believe in a pro-active approach by dedicated staff, which results in the optimisation of port rotations and a reduction in the overall time spent in port. All of this is always aligned with the customer&rsquo;s requirements, without compromising on safety requirements or local regulations.</p>',
  '<p>Bij Libra Shipping geloven wij in een proactieve aanpak door toegewijde medewerkers, wat leidt tot een optimale havenrotatie en een kortere totale verblijftijd in de haven. Dit alles altijd afgestemd op de wensen van de klant, zonder concessies aan veiligheidseisen of lokale regelgeving.</p>'),
 ('<h2>Amongst other things, our agency department can offer:</h2>','<h2>Onze agentuurafdeling biedt onder meer:</h2>'),
 ('<h3>Husbandry agency</h3>','<h3>Husbandry-agentuur</h3>'),('<h3>Bunkering services</h3>','<h3>Bunkerdiensten</h3>'),('<h3>Crewing services</h3>','<h3>Bemanningsdiensten</h3>'),
 ('<h3>Lay-by services</h3>','<h3>Lay-by-diensten</h3>'),('<h3>Repair services</h3>','<h3>Reparatiediensten</h3>'),('<h3>Cargo handling</h3>','<h3>Ladingbehandeling</h3>'),
 ('<h2>Where we work.</h2>','<h2>Waar wij werken.</h2>'),
 ('Agency covering all ports in the ARA range, with offices in Rotterdam and Antwerp.','Agentuur voor alle havens in de ARA-range, met kantoren in Rotterdam en Antwerpen.'),
 ('aria-label="Map of the ARA range: ports served from the Rotterdam office (Rotterdam, Amsterdam, Moerdijk, Terneuzen, Flushing) and from the Antwerp office (Antwerp, Ghent, Zeebrugge, Hemiksem and the upper Scheldt)."',
  'aria-label="Kaart van de ARA-range: havens bediend vanuit het kantoor Rotterdam (Rotterdam, Amsterdam, Moerdijk, Terneuzen, Vlissingen) en vanuit het kantoor Antwerpen (Antwerpen, Gent, Zeebrugge, Hemiksem en de Boven-Schelde)."'),
 ('>North Sea</text>','>Noordzee</text>'),('>Flushing</text>','>Vlissingen</text>'),('>Ghent</text>','>Gent</text>'),('>Antwerp</text>','>Antwerpen</text>'),
 ('>Hemiksem &amp; upper Scheldt</text>','>Hemiksem &amp; Boven-Schelde</text>'),('>Agency, all ARA ports</text>','>Agentuur, alle ARA-havens</text>'),
 ('>Rotterdam office &middot; NL</text>','>Kantoor Rotterdam &middot; NL</text>'),('>Antwerp office &middot; BE</text>','>Kantoor Antwerpen &middot; BE</text>'),
 ('<span class="on">Rotterdam</span><span class="oc">The Netherlands</span>','<span class="on">Rotterdam</span><span class="oc">Nederland</span>'),
 ('<li>Terneuzen</li><li>Flushing</li>','<li>Terneuzen</li><li>Vlissingen</li>'),
 ('<address>Waalhaven Oostzijde 85<br><span class="num">3087 BM</span> Rotterdam<br>The Netherlands</address>','<address>Waalhaven Oostzijde 85<br><span class="num">3087 BM</span> Rotterdam<br>Nederland</address>'),
 ('<span class="on">Antwerp</span><span class="oc">Belgium</span>','<span class="on">Antwerpen</span><span class="oc">België</span>'),
 ('<li>Antwerp</li><li>Ghent</li><li>Zeebrugge</li><li>Hemiksem and upper Scheldt</li>','<li>Antwerpen</li><li>Gent</li><li>Zeebrugge</li><li>Hemiksem en Boven-Schelde</li>'),
 ('<address>Cadixstraat 23<br><span class="num">2000</span> Antwerp<br>Belgium</address>','<address>Cadixstraat 23<br><span class="num">2000</span> Antwerpen<br>België</address>'),
 ('Calling elsewhere? <a href="contact.html">Ask us about our network &rarr;</a>','Aanloop elders? <a href="contact.html">Vraag naar ons netwerk &rarr;</a>'),
 ('<h2>Our agency workflow.</h2>','<h2>Onze agentuurprocedure.</h2>'),
 ('<span class="st">Appointment</span><span class="sd">We confirm your nomination the same day.</span>','<span class="st">Aanstelling</span><span class="sd">Wij bevestigen uw nominatie dezelfde dag.</span>'),
 ('<span class="sd">A disbursement estimate before the port call, so there are no surprises.</span>','<span class="sd">Een kostenraming vóór de havenaanloop, zodat er geen verrassingen zijn.</span>'),
 ('<span class="st">Pre-arrival</span><span class="sd">Berth, notices, terminal and services lined up prior to the vessel arriving.</span>','<span class="st">Vóór aankomst</span><span class="sd">Ligplaats, meldingen, terminal en diensten geregeld vóór aankomst van het schip.</span>'),
 ('<span class="st">Vessel in port</span><span class="sd">A dedicated operator monitoring from arrival until departure.</span>','<span class="st">Schip in de haven</span><span class="sd">Een vaste operator die toezicht houdt van aankomst tot vertrek.</span>'),
 ('<span class="st">Departure</span><span class="sd">Clearance and sailing without delay.</span>','<span class="st">Vertrek</span><span class="sd">Uitklaring en vertrek zonder vertraging.</span>'),
 ('<span class="st">Final DA &amp; documents</span><span class="sd">The account settled, the related documents distributed and the final DA issued.</span>','<span class="st">Eind-DA &amp; documenten</span><span class="sd">De afrekening afgehandeld, de bijbehorende documenten verzonden en de eind-DA uitgegeven.</span>'),
 ('<h2>Chartering and agency, one team.</h2>','<h2>Bevrachting en agentuur, één team.</h2>'),
 ('When Libra fixes the vessel, the same desk handles the port call. No handover, nothing lost between broker and agent, one contact for both.','Wanneer Libra het schip bevracht, verzorgt hetzelfde team de havenaanloop. Geen overdracht, niets gaat verloren tussen makelaar en agent, één contactpersoon voor beide.'),
 ('See what we fix &rarr;','Bekijk wat wij afsluiten &rarr;'),
 ('<h2>Nominate a vessel, or if interested, ask what a port call will cost.</h2>','<h2>Nomineer een schip, of vraag vrijblijvend wat een havenaanloop kost.</h2>'),
 ('alt="Bulk carrier alongside the quay with grab cranes working"','alt="Bulkcarrier aan de kade met werkende grijperkranen"'),
]+PANEL+GMP
T['contact']=[
 ('<h1>Let&rsquo;s talk shipping.</h1>','<h1>Laten we het over scheepvaart hebben.</h1>'),
 ('For a quick response, just give us a ring.','Voor een snel antwoord belt u ons gewoon even.'),
 ('<h2>Choose your desk.</h2>','<h2>Kies uw afdeling.</h2>'),
 ('<span class="dk">Chartering</span>\n            <p>Cargo to move, a freight indication, or a vessel open for employment.</p>','<span class="dk">Bevrachting</span>\n            <p>Lading te vervoeren, een vrachtindicatie of een schip beschikbaar voor bevrachting.</p>'),
 ('<span class="dk">Agency services in Netherlands and Belgium</span>\n            <p>Port calls, proforma disbursement accounts, crew changes and husbandry.</p>','<span class="dk">Agentuurdiensten in Nederland en België</span>\n            <p>Havenaanlopen, proforma disbursement accounts, bemanningswissels en husbandry.</p>'),
 ('<span class="ooh-lab">24/7 phone number</span>','<span class="ooh-lab">24/7 telefoonnummer</span>'),
 ('<span class="on">Head office Rotterdam</span><span class="oc">The Netherlands</span>','<span class="on">Hoofdkantoor Rotterdam</span><span class="oc">Nederland</span>'),
 ('<h2>Give us the voyage. We will come back with a number.</h2>','<h2>Geef ons de reis. Wij komen terug met een prijs.</h2>'),
 ('Name, email and a few words about your cargo or vessel are all we need. Voyage details help us answer faster, but they can wait for the phone call.','Naam, e-mail en een paar woorden over uw lading of schip zijn genoeg. Reisgegevens helpen ons sneller te antwoorden, maar die kunnen ook wachten tot het telefoongesprek.'),
 ('<label for="name">Your name</label>','<label for="name">Uw naam</label>'),('<label for="company">Company</label>','<label for="company">Bedrijf</label>'),
 ('<label for="email">Email</label>','<label for="email">E-mail</label>'),('<label for="phone">Telephone</label>','<label for="phone">Telefoon</label>'),
 ('<label for="message">Tell us about your cargo or vessel</label>','<label for="message">Vertel ons over uw lading of schip</label>'),
 ('placeholder="What needs to move, roughly how much, and when &mdash; or the vessel you have open."','placeholder="Wat moet er vervoerd worden, ongeveer hoeveel en wanneer &mdash; of het schip dat u beschikbaar heeft."'),
 ('<summary>Add voyage details <span class="muted">(optional)</span></summary>','<summary>Reisgegevens toevoegen <span class="muted">(optioneel)</span></summary>'),
 ('<label for="cargo">Cargo</label><input id="cargo" name="cargo" type="text" placeholder="Wheat, urea, steel coils&hellip;">','<label for="cargo">Lading</label><input id="cargo" name="cargo" type="text" placeholder="Tarwe, ureum, staalrollen&hellip;">'),
 ('<label for="quantity">Quantity</label><input id="quantity" name="quantity" type="text" placeholder="3,000 mt 10% moloo (500&ndash;50.000)">','<label for="quantity">Hoeveelheid</label><input id="quantity" name="quantity" type="text" placeholder="3.000 mt 10% moloo (500&ndash;50.000)">'),
 ('<label for="loadport">Load port</label>','<label for="loadport">Laadhaven</label>'),('<label for="dischport">Discharge port</label>','<label for="dischport">Loshaven</label>'),
 ('placeholder="12&ndash;18 October"','placeholder="12&ndash;18 oktober"'),
 ('<label for="terms">Load / discharge terms</label>','<label for="terms">Laad-/loscondities</label>'),
 ('<summary>Add port call details <span class="muted">(optional)</span></summary>','<summary>Gegevens havenaanloop toevoegen <span class="muted">(optioneel)</span></summary>'),
 ('<label for="vessel">Vessel name</label>','<label for="vessel">Scheepsnaam</label>'),
 ('placeholder="14 October, am"','placeholder="14 oktober, ochtend"'),
 ('<label for="port">Port</label><input id="port" name="port" type="text" placeholder="Rotterdam, Antwerp, Ghent&hellip;">','<label for="port">Haven</label><input id="port" name="port" type="text" placeholder="Rotterdam, Antwerpen, Gent&hellip;">'),
 ('<label for="agentneeds">What is needed</label><input id="agentneeds" name="agentneeds" type="text" placeholder="Full agency, husbandry only, crew change&hellip;">','<label for="agentneeds">Wat is er nodig</label><input id="agentneeds" name="agentneeds" type="text" placeholder="Volledige agentuur, alleen husbandry, bemanningswissel&hellip;">'),
 ('> Please send a proforma disbursement account</label>','> Stuur mij een proforma disbursement account</label>'),
 ('> I agree that Libra Shipping stores this enquiry and contacts me about it. <a href="privacy.html">Privacyverklaring</a></label>','> Ik ga ermee akkoord dat Libra Shipping deze aanvraag bewaart en mij hierover benadert. <a href="privacy.html">Privacyverklaring</a></label>'),
 ('> I have read the <a href="conditions.html">General Terms &amp; Conditions</a>.</label>','> Ik heb de <a href="conditions.html">Algemene voorwaarden</a> gelezen.</label>'),
 ('<button class="btn" type="submit">Send enquiry</button>','<button class="btn" type="submit">Aanvraag versturen</button>'),
 ('[Response time, if Libra will promise one: &ldquo;We answer within the working day.&rdquo;]','[Reactietijd, als Libra die wil toezeggen: &ldquo;Wij antwoorden binnen één werkdag.&rdquo;]'),
 ('alt="Harbour under an overcast sky"','alt="Haven onder een bewolkte lucht"'),
 ('<h2>Our team.</h2>','<h2>Ons team.</h2>'),
]
T['conditions']=[
 ('<title>Terms &amp; Conditions — Libra Shipping B.V.</title>','<title>Algemene voorwaarden — Libra Shipping B.V.</title>'),
 ('<p class="eyebrow">Legal</p>','<p class="eyebrow">Juridisch</p>'),
 ('<h1>Terms &amp; Conditions.</h1>','<h1>Algemene voorwaarden.</h1>'),
 ('<p class="lead">The conditions under which Libra Shipping B.V. works.</p>','<p class="lead">De voorwaarden waaronder Libra Shipping B.V. werkt.</p>'),
 ('<p>All our operations, activities, services rendered, and contracts concluded are governed by the latest versions of &lsquo;the Dutch forwarding conditions&rsquo; in the context of organising contracts for carriage of goods, and &lsquo;the General conditions or rules for Dutch shipbrokers and agents&rsquo; in case of shipagency activities, both filed with the Registry of the Court of Rotterdam.</p>',
  '<p>Op al onze werkzaamheden, activiteiten, verleende diensten en gesloten overeenkomsten zijn de meest recente versies van toepassing van de &lsquo;Nederlandse Expeditievoorwaarden&rsquo;, voor zover het gaat om het organiseren van overeenkomsten tot vervoer van goederen, en van de &lsquo;Algemene Nederlandse Cargadoorsvoorwaarden&rsquo;, voor zover het gaat om scheepsagentuurwerkzaamheden, beide gedeponeerd ter griffie van de Rechtbank Rotterdam.</p>'),
 ('<p>In the event of doubt or dispute, Libra Shipping B.V. shall exclusively determine which of the two sets of conditions applies. All our offers are without engagement unless expressly stated otherwise.</p>',
  '<p>Bij twijfel of geschil bepaalt uitsluitend Libra Shipping B.V. welke van de twee sets voorwaarden van toepassing is. Al onze aanbiedingen zijn vrijblijvend, tenzij uitdrukkelijk anders vermeld.</p>'),
 ('<h3>Dutch Forwarding Conditions</h3>\n            <p>Apply to organising contracts for the carriage of goods. Issued by FENEX.</p>','<h3>Nederlandse Expeditievoorwaarden</h3>\n            <p>Van toepassing op het organiseren van overeenkomsten tot vervoer van goederen. Uitgegeven door FENEX.</p>'),
 ('<h3>General Conditions and Rules for Dutch Shipbrokers and Agents</h3>\n            <p>Apply to ship agency activities. Issued by the United Dutch Shipbrokers and Agents.</p>','<h3>Algemene Nederlandse Cargadoorsvoorwaarden</h3>\n            <p>Van toepassing op scheepsagentuurwerkzaamheden. Uitgegeven door de Verenigde Nederlandse Cargadoors.</p>'),
 ('href="assets/legal/general-conditions-dutch-shipbrokers-and-agents.pdf"','href="assets/legal/algemene-nederlandse-cargadoorsvoorwaarden.pdf"'),
 ('href="assets/legal/dutch-forwarding-conditions.pdf"','href="assets/legal/nederlandse-expeditievoorwaarden.pdf"'),
 ('Read the conditions (PDF)','Lees de voorwaarden (PDF)'),
 ('<p class="docsrc">Latest version at','<p class="docsrc">Meest recente versie op'),
]
T['disclaimer']=[
 ('<p class="eyebrow">Legal</p>','<p class="eyebrow">Juridisch</p>'),
 ('<p class="lead">What applies to the use of this website.</p>','<p class="lead">Wat geldt voor het gebruik van deze website.</p>'),
 ('<h2>This website.</h2>','<h2>Deze website.</h2>'),
 ('<p>The content of this website has been put together with care. Still, Libra Shipping B.V. accepts no liability for information that is incomplete, out of date or incorrect, nor for any consequence of using it. No rights can be derived from the information on this website.</p>',
  '<p>De inhoud van deze website is met zorg samengesteld. Toch aanvaardt Libra Shipping B.V. geen aansprakelijkheid voor informatie die onvolledig, verouderd of onjuist is, noch voor enig gevolg van het gebruik ervan. Aan de informatie op deze website kunnen geen rechten worden ontleend.</p>'),
 ('<p>Links to other websites are provided for convenience. Libra Shipping B.V. has no control over their content and is not responsible for it.</p>','<p>Links naar andere websites zijn opgenomen voor uw gemak. Libra Shipping B.V. heeft geen invloed op de inhoud daarvan en is daarvoor niet verantwoordelijk.</p>'),
 ('<p>All text, images and the Libra Shipping logo on this website are the property of Libra Shipping B.V. and may not be reproduced without written permission.</p>','<p>Alle teksten, afbeeldingen en het logo van Libra Shipping op deze website zijn eigendom van Libra Shipping B.V. en mogen niet zonder schriftelijke toestemming worden overgenomen.</p>'),
 ('<p>Questions about this disclaimer: ','<p>Vragen over deze disclaimer: '),
]
T['privacy']=[]
LANG_EN_OLD='<span class="lang" aria-label="Language"><a href="#" aria-current="true">EN</a><a href="#" title="Dutch version — to build">NL</a></span>'
def lang_en(p): return f'<span class="lang" aria-label="Language"><a href="{p}.html" aria-current="true" hreflang="en">EN</a><a href="{p}-nl.html" hreflang="nl">NL</a></span>'
def lang_nl(p): return f'<span class="lang" aria-label="Taal"><a href="{p}.html" hreflang="en">EN</a><a href="{p}-nl.html" aria-current="true" hreflang="nl">NL</a></span>'
def nl_links(s):
    for p in PAGES:
        s=re.sub(r'href="%s\.html(#[^"]*)?"(?! hreflang)'%p, lambda m: f'href="{p}-nl.html{m.group(1) or ""}"', s)
    return s
def nav_nl(s):
    s=re.sub(r'(<a href="chartering\.html"[^>]*>)Chartering</a>', r'\1Bevrachting</a>', s)
    s=re.sub(r'(<a href="agency\.html"[^>]*>)Agency</a>', r'\1Agentuur</a>', s)
    return s
for p in PAGES:
    src = 'privacy-nl.html' if p=='privacy' else p+'.html'
    s=open(src).read()
    if p!='privacy':
        en=s
        if LANG_EN_OLD in en:
            en=en.replace(LANG_EN_OLD, lang_en(p))
            en=en.replace('</title>', f'</title>\n<link rel="alternate" hreflang="nl" href="{p}-nl.html">',1)
            open(p+'.html','w').write(en)
        s=rep(s, COMMON, p); s=nav_nl(s); s=rep(s, T[p], p)
        s=s.replace(LANG_EN_OLD,'@@LANG@@')
        if '@@LANG@@' not in s:
            s=re.sub(r'<span class="lang" aria-label="Language">.*?</span>','@@LANG@@',s,count=1,flags=re.S)
        s=re.sub(r'<link rel="alternate" hreflang="nl" href="%s-nl.html">\n'%p,'',s)
    else:
        if '<html lang="en">' not in s: s=s.replace('<html lang="nl">','<html lang="en">',1)  # normalise for COMMON
        s=rep(s, COMMON, p); s=nav_nl(s)
        s=re.sub(r'<span class="lang" aria-label="Taal">.*?</span>','@@LANG@@',s,count=1,flags=re.S)
        s=re.sub(r'<link rel="alternate" hreflang="en" href="privacy.html">\n','',s)
    s=nl_links(s)
    s=s.replace('@@LANG@@', lang_nl(p))
    s=s.replace('</title>', f'</title>\n<link rel="alternate" hreflang="en" href="{p}.html">',1)
    open(p+'-nl.html','w').write(s)
    print('ok', p+'-nl.html')
