## Miksi päädyin käyttämääni resursseihin

### Lähtötilanne ja aiempi kokemus

Lähdin liikkeelle aika selkeällä fiiliksellä siitä, mitä haluan rakentaa. Olin ennen tätä kurssia tehnyt tekoälyprojektin, jossa purin Hevy-kuntosalisovelluksen Swagger-dokumentaatiota ja kokeilin sen rajapintoja käsin. Siitä jäi tosi konkreettinen tuntuma siihen, miltä “mukava” API tuntuu (tai ainakin pitäisi tuntua) käyttäjän näkökulmasta: miten endpointit ketjuuntuvat, mitä tietoa on kätevä palauttaa ja miten Pydantic-tyyliset mallit istuvat siihen väliin.

### IIoT-opintojen vaikutus ajatteluun

Samaan aikaan tein IIoT-kurssin lopputyötä, jossa pyörittelin mielessäni huomattavasti isompaa teollista kokonaisuutta ja sensorimaailmaa. Se oli tavallaan hyödyllistä taustaa, mutta ehkä enemmän haitaksi kuin hyödyksi tässä työssä, koska aloin alkuun suunnitella AnturiAPI:a aivan liian raskaana järjestelmänä. Jouduin monta kertaa muistuttamaan itseäni siitä, että nyt tehdään kurssityötä, ei kokonaista tehdasoperaatiojärjestelmää.

### Teknologiavalinnat

Teknologioiden osalta päätin pysyä täysin siinä työkalupakissa, jonka kurssilla olimme jo ottaneet käyttöön: FastAPI, SQLModel ja SQLite. Ne riittivät kaikkeen mitä tehtävä vaati, enkä nähnyt mitään tarvetta ottaa mitään ylimääräistä mukaan. FastAPI antoi minulle automaattisesti hyvän Swagger-dokumentaation, SQLModel yhdisti järkevästi tietokantamallit ja skeemat, ja SQLite on helppo jakaa mukana ilman erillistä asennusta. Käytännössä näin pystyin keskittymään ihan rauhassa rakenteeseen ja logiikkaan, en ympäristöongelmiin.

### Laajennettavuuden huomioiminen

Koko projektin ajan minulla oli mielessä, että ratkaisua pitäisi olla mahdollista laajentaa tulevaisuudessa. Tästä syystä rakensin mittausmallin (melkein) alusta asti siten, että käytössä on enum-tyypit mittaustyypille ja yksikölle (esimerkiksi `MeasurementType` ja `MeasurementUnit`) sekä erilliset kentät tyypille ja yksikölle. Nykyisessä versiossa mitataan vain lämpötilaa Celsius-asteina, mutta rakenne tukee sitä, että myöhemmin voidaan lisätä muitakin mittaustyyppejä ilman, että koko APIa tarvitsee repiä auki.

### Mallien suunnittelu ennen endpointteja

Projektin alussa käytin kokonaisen päivän pelkästään `models.py`-tiedoston hiomiseen. Halusin ymmärtää kunnolla, miten sensorit, segmentit, mittaukset ja status-historia liittyvät toisiinsa, ennen kuin kirjoitan ensimmäistäkään oikeaa endpointia. Vasta kun mallit olivat mielestäni alustavasti järkevässä kunnossa, aloin rakentaa lopullista API:a niiden ympärille.

---

## Mikä ohjasi endpointien polkusuunnittelua

### Alkuperäinen ajatus

Alkuperäinen suunnitelma oli jakaa kaikki kolmeen koriin: `/segments`, `/sensors` ja `/measurements`. Tämä näytti paperilla siistiltä, mutta käytännössä alkoi tuntua sekavalta, kun yritin katsoa kokonaisuutta Swaggerin näkökulmasta. Aivan loppumetreillä päädyin siihen, että haluan korostaa sitä, että mittaukset ja tilat ovat sensorin “alaresursseja”. Tämä päätös aiheuttikin pientä aikataulupainetta.

### Lopullinen jaottelu Swaggerissa

Siksi muutin kokonaisuuden lopussa muotoon:

- Segments  
- Sensors  
- Sensor Status  
- Sensor Measurements  
- Measurements  

Segmentit ovat ylempi taso ja sensorit elävät siellä sisällä.

### Segments-osion rooli

`Segments`-osio vastaa lohkojen hallinnasta ja segmenttinäkymä on tietoisesti hiukan rikkaampi: siellä voi suodattaa segmentin sensorit niiden tilan mukaan (esimerkiksi löytääkseen nopeasti virhetilassa olevat). Mukaan on otettu myös ohjeiden mukaisesti kunkin sensorin viimeisin mittaus, jotta yhdellä haulla saa “tilannekuvan” lohkosta.

### Sensorin ympärille rakennetut kolme osa-aluetta

Sensorin ympärille jaoin asiat periaatteessa kolmeen osaan. `Sensors`-osio keskittyy sensorin perustietoihin – luomiseen, hakemiseen, päivittämiseen ja poistamiseen. `Sensor Status` -osio kuvaa sensorin tilaa ja tilahistoriaa: siellä näkyy aikajana tilamuutoksista ja on oma rajapintansa tilan vaihtamiseen niin, että jokainen muutos tallentuu myös historiaan. `Sensor Measurements` -osio käsittelee sensorikohtaista mittaushistoriaa, jossa mittauksia voidaan hakea rajattuna esimerkiksi aikavälin tai maksimimäärän perusteella, ja uudet mittaukset luodaan aina nimenomaan jonkin tietyn sensorin alle.

### Mittausrajapinnan kaksitasoinen malli

Mittauspuolella refaktoroin ratkaisun lopulta kahteen tasoon. Sensorikohtainen rajapinta kuuluu `Sensor Measurements` -osioon, kun taas `Measurements`-osio on erillinen globaali resurssi yksittäisen mittauksen käsittelyyn mittauksen tunnisteen perusteella (hakeminen ja poistaminen). Tietokanta ei tarvitse sensorin id:tä, koska mittauksen id on jo yksilöllinen, ja tämä malli noudattaa paremmin REST-tyylistä ajattelua. Halusin silti korostaa mittauksen kuulumista tietylle sensorille, joten mittaus luodaan aina sensorin kautta. Sensorin mittauspuolelta löytyy lisäksi mahdollisuus suodattaa mittauksia niiden tyypin mukaan.

### Swaggerin luettavuus

Kaiken taustalla oli ajatus siitä, että Swaggerin näkymä olisi ihmiselle luettava ja selkeä: ensin lohkot (`Segments`), sitten sensorit ja niiden ympärille jaetut kolme osa-aluetta (`Sensors`, `Sensor Status`, `Sensor Measurements`) sekä lopuksi yksittäinen mittaus omana resurssinaan (`Measurements`). Halusin, että polut tukevat ja korostavat tätä hierarkiaa.

---

## Mitä opin työtä tehdessä

### Suunnittelun merkitys

Isoin oppi oli ehkä se, kuinka paljon suunnittelu etukäteen helpottaa kaikkea muuta. Kun käytin ensimmäisen päivän pelkästään mallien miettimiseen, se maksoi itsensä takaisin myöhemmin, vaikka jouduinkin refaktoroimaan rakennetta vielä ihan loppumetreilläkin.

### Ylisuunnittelu

Toinen iso oppi liittyi siihen, miten helposti “ylisuunnittelu” vie mukanaan. Koska olin samaan aikaan miettimässä IIoT-järjestelmää, mieli karkasi koko ajan kohti valtavia tulevaisuuden laajennuksia. Huomasin, että lisäsin liikaa erilaisia paluu- ja näkymämalleja, suodattimia ja pieniä lisäominaisuuksia. Lopussa tämä kostautui: aikataulu alkoi painaa päälle ja jouduin palaamaan perusasioihin ja karsimaan turhaa monimutkaisuutta. Se oli hyvä muistutus siitä, että kaikkea mahdollista ei tarvitse tehdä yhdellä kertaa.

### Relaatiot ja SQLModel

Opin myös käytännössä paljon SQLModelin ja relaatioiden käytöstä. Esimerkiksi kaskadipoistot, status-historian erottaminen omaksi taulukokseen ja se, miten eri ulostulomalleja kannattaa rakentaa samoista tietokantariveistä, tulivat tutuksi pikkuhiljaa – välillä virheiden ja debuggerin kautta. Eri ulostulomalleja tässä työssä riittää, koska minulla oli selkeä visio siitä, minkälaista dataa haluan ottaa sisään ja minkälaista dataa haluan antaa ulos. Päätöksiäni ohjasi monesti aikaisempi tekoälyprojektin kehitys, jossa hain yhdestä endpointista tietoa ja siinä olevia kenttiä käytin suoraan toiseen endpointtiin. Moni asia, jonka olin aiemmin nähnyt Hevyn APIsta generoidusta SDK:sta, muuttui tässä työssä “lihaksi luiden päälle”.

### API-rakenne ja dokumentaatio

Yllättävän iso osa oppimista liittyi myös siihen, miten dokumentaatio ja API kulkevat käsi kädessä. Kun työstin Swagger-dokumentaatiota, huomasin helposti, mitkä ratkaisut olivat intuitiivisia ja mitkä selitystä vaativia. Jos jonkin endpointin joutui selittämään useiden vaiheiden kautta, se oli usein merkki siitä, että polkua tai rakennetta kannatti vielä hienosäätää.

### Projektin modulaarisuus

Jossakin vaiheessa projektia halusin myös refaktoroida sitä [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) oppien mukaisesti ja paloittelin projektin mielestäni melko modulaarisesti. Yritin myös pilkkoa `models.py`-tiedostoa useampaan pienempään osaan, mutta tämä aiheutti `circular import` -helvetin, joten päädyin käyttämään vain yhtä globaalia models.py-tiedostoa.

---

## Mitä olisi voinut tehdä toisin

### Rakenteen lukitseminen

Vaikka käytin projektin alussa kokonaisen päivän mallien suunnitteluun, jälkikäteen ajateltuna olisin käyttänyt vieläkin enemmän aikaa nimenomaan rakenteen lukitsemiseen ennen kuin aloin rakentaa suodattimia, lisänäkymiä ja kaikkea “kivaa extraa”. Olisi ollut järkevää varmistaa, että perusrunko – segmentit, sensorit, mittaukset ja status-historia sekä niiden väliset relaatiot – on 100 % varma, ja vasta sitten panostaa monipuolisiin suodatusvaihtoehtoihin ja erilaisiin ulostulomalleihin.

### Toteutusjärjestys

Käytännössä tein asioita välillä väärässä järjestyksessä: rakensin esimerkiksi aika paljon lisämalleja ja suodattimia jo siinä vaiheessa, kun kokonaisuus ei ollut vielä täysin lukossa. Tämä johti siihen, että jouduin refaktoroimaan samoja kohtia useaan kertaan, kun hierarkiaa ja endpointtien polkuja tarkennettiin loppua kohti. Se toimi oppimiskokemuksena, mutta söi turhaan aikaa.

### Modulaarisuus

Toinen asia, jonka tekisin toisin, olisi projektin modulaarisuuden suunnittelu aikaisemmassa vaiheessa. Yritin pilkkoa `models.py`-tiedoston useampaan pienempään tiedostoon vasta melko myöhään, jolloin tuloksena oli `circular import` -ongelmia. Jos lähtisin nyt alusta, miettisin modulaarisuuden ja jaottelun rauhassa jo ennen ensimmäistä isoa commitia: miten sensorit, segmentit, mittaukset, status-historia ja dokumentaatio kannattaa jakaa kansioihin ja moduuleihin, jotta laajennettavuus olisi helpompaa.

### Minimiominaisuudet ensin, laajennukset myöhemmin

Olisin voinut myös tietoisemmin rajata ensimmäisen version “minimiominaisuuksiin”: perus-CRUD segmentille ja sensorille, yksinkertainen mittausmalli ja sensorikohtaiset mittaukset ilman laajaa filtteriarsenaalia. Kun tämä ydin olisi ollut täysin valmis ja testattu, suodattimia ja lisämalleja olisi ollut turvallisempaa kasvattaa kerros kerrokselta. Nyt osa lisäominaisuuksista syntyi vähän liian aikaisin ja teki refaktoroinnista raskaampaa.

---

## Keinoälyn käyttö

### Suunnitteluvaihe

Tekoäly oli mukana käytännössä koko projektin ajan, mutta ei niin, että olisin “tilannut valmiin ratkaisun”, vaan enemmänkin niin kuin olisi ollut kokenut kollega vieressä.

Suunnitteluvaiheen tein pitkälti itse: suunnittelin mallit, hahmottelin relaatiot ja rakensin ensimmäisen version `models.py`-tiedostosta ilman tekoälyä. Sen jälkeen aloin käyttää ChatGPT:tä lähinnä peilinä: kysyin, onko jokin rakenne järkevä, onko jokin suhde turhan monimutkainen tai olisiko jokin malli syytä pilkkoa toisin. Monesti en ottanut ehdotuksia sellaisenaan, mutta keskustelut auttoivat kirkastamaan omaa näkemystäni.

### Tekoäly bugien ja virheiden ratkaisussa

Käytin tekoälyä myös konkreettisena “bugiapuna”: kun vastaan tuli outo virheilmoitus, typerä syntaksivirhe tai koodini ei vain yksinkertaisesti toiminut, oli nopeaa liittää pätkä terminaalista tai koodista keskusteluun ja pyytää, että “mikä tässä ei täsmää suhteessa siihen, mitä yritän tehdä”. Sama koski muutamia relaatiomallinnuksen ja varsinkin sisäkkäisten mallien yksityiskohtia, jotka eivät meinanneet jäädä päähän pelkän dokumentaation perusteella.

### Dokumentaation kirjoittaminen

Halusin myös, että APIn Swagger-dokumentaatio on hyvin kirjoitettu, joten käytin tekoälyä generoimaan itselleni `summary`- ja `description`-tekstit, joita kylläkin itse sitten lopuksi muokkasin lopulliseen versioon. Nämä säilöin jokaisen osion omaan `docs`-tiedostoon, jotta itse koodipuoli ei menisi niin älyttömän tukkoon kattavasta dokumentaatiosta huolimatta.

Dokumentaation puolella tekoäly auttoi erityisesti README- ja raporttitekstien jäsentelyssä. README-tiedostoon käytin enemmän hyväksi tekstin generointia koodikantani ja ohjeideni mukaisesti. Raportista generoin ensin “teknisen version” käyttäen tekoälyä, josta sitten kirjoitin itse oman kömpelön versioni. Lopuksi annoin tekoälylle raakatekstini, jonka jälkeen pyysin apua sen tiivistämiseen ja selkeyttämiseen. Raporttia myös muokattiin jälkikäteen useita kertoja tekoälyä hyväksi käyttäen. En kuitenkaan kopioinut mitään sokkona, vaan kävin kaikki tekstit läpi ja muokkasin niitä, jotta ne vastasivat varmasti omaa toteutustani ja ajatuksiani. 

### Luottamus tekoälyn ehdotuksiin

Luottamus tekoälyn tuottamaan sisältöön syntyi kolmella tavalla: ensin tarkistin koodiin liittyvät ehdotukset ajamalla sovellusta ja testaamalla endpointteja Swaggerissa, toiseksi vertasin ratkaisuja FastAPIn ja SQLModelin dokumentaatioon (ja joissakin tapauksissa google-hakuihin), ja kolmanneksi arvioin, tuntuiko ehdotettu ratkaisu järkevältä tässä projektissa. Vasta kun nämä kolme kohtasivat, hyväksyin muutoksen osaksi lopullista versiota.

### Oma työ vs. tekoälyn apu

Lopputuloksena voin aika hyvällä omallatunnolla sanoa, että AnturiAPI on minun tekemäni ja ymmärrän sen jokaisen koodirivin toiminnon – tekoäly auttoi, kyseenalaisti ja nopeutti, mutta ei päättänyt puolestani. Myös pari sataa committia GitHubissa kertoo, että projektiin käytettiin aikaa ja vaivaa.
