## Miksi päädyin käyttämääni resursseihin

Lähdin liikkeelle aika selkeällä fiiliksellä siitä, mitä haluan rakentaa. Olin ennen tätä kurssia tehnyt tekoälyprojektin, jossa purin Hevy-kuntosalisovelluksen Swagger-dokumentaatiota ja kokeilin sen rajapintoja käsin. Siitä jäi tosi konkreettinen tuntuma siihen, miltä “mukava” API tuntuu – tai ainakin pitäisi tuntua – käyttäjän näkökulmasta: miten endpointit ketjuuntuvat, mitä tietoa on kätevä palauttaa ja miten Pydantic-tyyliset mallit istuvat siihen väliin.

Samaan aikaan tein IIoT-kurssin lopputyötä, jossa pyörittelin huomattavasti isompaa teollista kokonaisuutta ja sensorimaailmaa. Se oli tavallaan hyödyllistä taustaa, mutta ehkä enemmän haitaksi kuin hyödyksi tässä työssä, koska aloin alkuun suunnitella AnturiAPI:a aivan liian raskaana järjestelmänä. Jouduin monta kertaa muistuttamaan itseäni siitä, että nyt tehdään kurssityötä, ei kokonaista tehdasoperaatiojärjestelmää.

Teknologioiden osalta päätin pysyä täysin siinä työkalupakissa, jonka kurssilla olimme jo ottaneet käyttöön: FastAPI, SQLModel ja SQLite. Ne riittivät kaikkeen mitä tehtävä vaati, enkä nähnyt mitään tarvetta ottaa mitään ylimääräistä mukaan. FastAPI antoi minulle automaattisesti hyvän Swagger-dokumentaation, SQLModel yhdisti järkevästi tietokantamallit ja skeemat, ja SQLite on helppo jakaa mukana ilman erillistä asennusta. Käytännössä näin pystyin keskittymään ihan rauhassa rakenteeseen ja logiikkaan, en ympäristöongelmiin.

Koko projektin ajan minulla oli mielessä, että ratkaisua pitäisi olla mahdollista laajentaa tulevaisuudessa. Tästä syystä rakensin mittausmallin alusta asti siten, että käytössä on enum-tyypit mittaustyypille ja yksikölle (esimerkiksi `MeasurementType` ja `MeasurementUnit`) sekä erilliset kentät tyypille ja yksikölle. Nykyisessä versiossa mitataan vain lämpötilaa Celsius-asteina, mutta rakenne tukee sitä, että myöhemmin voidaan lisätä muitakin mittaustyyppejä ilman, että koko APIa tarvitsee repiä auki.

Projektin alussa käytin kokonaisen päivän pelkästään `models.py`-tiedoston hiomiseen. Halusin ymmärtää kunnolla, miten sensorit, segmentit, mittaukset ja status-historia liittyvät toisiinsa, ennen kuin kirjoitan ensimmäistäkään oikeaa endpointia. Vasta kun mallit olivat mielestäni alustavasti järkevässä kunnossa, aloin rakentaa lopullista API:a niiden ympärille.

---

## Mikä ohjasi endpointien polkusuunnittelua

Alkuperäinen suunnitelma oli jakaa kaikki kolmeen koriin: `/segments`, `/sensors` ja `/measurements`. Tämä näytti paperilla siistiltä, mutta käytännössä alkoi tuntua sekavalta, kun yritin katsoa kokonaisuutta Swaggerin näkökulmasta. Aivan loppumetreillä päädyin siihen, että haluan korostaa sitä, että mittaukset ja tilat ovat anturin “alaresursseja”, mikä aiheutti vähän aikataulupaineita.

Siksi muutin kokonaisuuden lopussa muotoon:

- Segments  
- Sensors  
- Sensor Status  
- Sensor Measurements  

Segmentit ovat ylempi taso, sensorit elävät siellä sisällä, ja sekä tilat että mittaukset ovat selkeästi yksittäisen sensorin alla. Tämä tuntui paljon luonnollisemmalta sekä dokumentaation että käyttöliittymän kannalta.

Tein myös tietoisesti ratkaisun, että sensorin perustiedot ja sensorin mittaushistoria eivät tule samasta endpointista. `GET /sensors/{sensor_id}` palauttaa vain perustiedot (id, nimi, segmentti, tila), ja varsinainen mittausdata (sekä sensorin perustiedot) haetaan erikseen `GET /sensors/{sensor_id}/measurements` -polulta, jossa sitä voi rajata limitillä ja aikavälillä. Tämä on pieni poikkeama tehtävänannosta, mutta tuntui oikeammalta mallilta, jos ajattelen käyttöliittymän tai muiden järjestelmien kannalta laajempaa tuotantokäyttöä.

Segmenttinäkymä on tietoisesti hiukan rikkaampi. Siellä on tehtävänannon mukaisesti mukana myös sensoreiden viimeisin mittaus, jotta yhdellä haulla saa “tilannekuvan” lohkosta. Siihen lisäsin myös mahdollisuuden suodattaa segmentin anturit niiden `sensor_status`-arvon mukaan, jotta esimerkiksi segmentin virhetilassa olevat sensorit löytyvät helposti.

Mittauspuolella tein ehkä kiistanalaisimman ratkaisun: yksittäisen mittauksen haku ja poisto tehdään polulla `/sensors/{sensor_id}/measurements/{measurement_id}`. Puhdas tietokanta ei tietenkään tarvitsisi sensorin id:tä, koska mittauksen id on jo yksilöllinen. Halusin kuitenkin polun, joka kertoo suoraan, minkä sensorin mittauksesta puhutaan, ja varmistaa samalla, ettei kukaan vahingossa poista tai käsittele “väärään sensoriin” kuuluvaa mittausta, jos järjestelmä tulevaisuudessa laajenisi. Tästä en ole vieläkään varma, onko se paras mahdollinen kompromissi, mutta se palveli tavoitettani korostaa mittausten kuulumista selkeästi tietylle sensorille. Mittauspuolelta löytyy myös lisäominaisuutena mahdollisuus suodattaa mittauksia niiden tyypin mukaan.

Kaiken taustalla oli ajatus siitä, että Swaggerin näkymä olisi ihmiselle luettava ja selkeä: ensin lohkot, sitten sensorit, ja niiden alla tila ja mittaukset. Halusin, että polut tukevat ja korostavat tätä hierarkiaa.

---

## Mitä opin työtä tehdessä

Isoin oppi oli ehkä se, kuinka paljon suunnittelu etukäteen helpottaa kaikkea muuta. Kun käytin ensimmäisen päivän pelkästään mallien miettimiseen, se maksoi itsensä takaisin myöhemmin, vaikka jouduinkin refaktoroimaan rakennetta vielä ihan loppumetreilläkin.

Toinen iso oppi liittyi siihen, miten helposti “ylisuunnittelu” vie mukanaan. Koska olin samaan aikaan miettimässä IIoT-järjestelmää, mieli karkasi koko ajan kohti valtavia tulevaisuuden laajennuksia. Huomasin, että lisäsin liikaa erilaisia paluu- ja näkymämalleja, suodattimia ja pieniä lisäominaisuuksia. Lopussa tämä kostautui: aikataulu alkoi painaa päälle ja jouduin palaamaan perusasioihin ja karsimaan turhaa monimutkaisuutta. Se oli hyvä muistutus siitä, että kaikkea mahdollista ei tarvitse tehdä yhdellä kertaa.

Opin myös käytännössä paljon SQLModelin ja relaatioiden käytöstä. Esimerkiksi kaskadipoistot, status-historian erottaminen omaksi taulukokseen ja se, miten eri ulostulomalleja kannattaa rakentaa samoista tietokantariveistä, tulivat tutuksi pikkuhiljaa – välillä virheiden ja debuggerin kautta. Eri ulostulomalleja tässä työssä riittää, koska minulla oli selkeä visio siitä, minkälaista dataa haluan ottaa sisään ja minkälaista dataa haluan antaa ulos. Päätöksiäni ohjasi monesti aikaisempi kuntosalisovelluksen kehitys, jossa hain yhdestä endpointista tietoa ja siinä olevia kenttiä käytin suoraan toiseen endpointtiin. Moni asia, jonka olin aiemmin nähnyt Hevyn APIsta generoidusta SDK:sta, muuttui tässä työssä “lihaksi luiden päälle”.

Yllättävän iso osa oppimista liittyi myös siihen, miten dokumentaatio ja API kulkevat käsi kädessä. Kun työstin Swagger-dokumentaatiota, huomasin helposti, mitkä ratkaisut olivat intuitiivisia ja mitkä selitystä vaativia. Jos jonkin endpointin joutui selittämään useiden vaiheiden kautta, se oli usein merkki siitä, että polkua tai rakennetta kannatti vielä hienosäätää.

Jossakin vaiheessa projektia halusin myös refaktoroida sitä näiden oppien mukaisesti [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) -ohjeiden suuntaan ja paloittelin projektin mielestäni melko modulaarisesti. Yritin myös pilkkoa `models.py`-tiedostoa useampaan pienempään osaan, mutta tämä aiheutti `circular import` -helvetin, joten päädyin käyttämään vain yhtä globaalia `models.py`-tiedostoa.

---

## Keinoälyn käyttö

Tekoäly oli mukana käytännössä koko projektin ajan, mutta ei niin, että olisin “tilannut valmiin ratkaisun”, vaan enemmänkin niin kuin olisi ollut kokenut kollega vieressä.

Suunnitteluvaiheen tein pitkälti itse: suunnittelin mallit, hahmottelin relaatiot ja rakensin ensimmäisen version `models.py`-tiedostosta ilman tekoälyä. Sen jälkeen aloin käyttää ChatGPT:tä lähinnä peilinä: kysyin, onko jokin rakenne järkevä, onko jokin suhde turhan monimutkainen tai olisiko jokin malli syytä pilkkoa toisin. Monesti en ottanut ehdotuksia sellaisenaan, mutta keskustelut auttoivat kirkastamaan omaa näkemystäni.

Käytin tekoälyä myös konkreettisena “bugiapuna”: kun vastaan tuli outo virheilmoitus, typerä syntaksivirhe tai koodini ei vain yksinkertaisesti toiminut, oli nopeaa liittää pätkä terminaalista tai koodista keskusteluun ja pyytää, että “mikä tässä ei täsmää suhteessa siihen, mitä yritän tehdä”. Sama koski muutamia relaatiomallinnuksen ja varsinkin sisäkkäisten mallien yksityiskohtia, jotka eivät meinanneet jäädä päähän pelkän dokumentaation perusteella.

Halusin myös, että APIni Swagger-dokumentaatio on hyvin kirjoitettu, joten käytin tekoälyä generoimaan itselleni `summary`- ja `description`-tekstit, joita kylläkin itse sitten lopuksi muokkasin lopulliseen versioon. Nämä säilöin jokaisen osion omaan `docs`-tiedostoon, jotta itse koodipuoli ei menisi niin älyttömän tukkoon kattavasta dokumentaatiosta huolimatta.

Dokumentaation puolella tekoäly auttoi erityisesti README- ja raporttitekstien jäsentelyssä. README-tiedostoon käytin enemmän hyväksi tekstin generointia koodikantani ja ohjeideni mukaisesti. Raportista generoin ensin “teknisen version” käyttäen tekoälyä ja omia kertomuksiani, josta sitten kirjoitin itse oman kömpelön versioni. Lopuksi annoin tekoälylle tämän raakatekstini, jonka jälkeen pyysin apua sen tiivistämiseen ja selkeyttämiseen. En kuitenkaan kopioinut mitään sokkona, vaan kävin kaikki tekstit läpi ja muokkasin niitä, jotta ne vastasivat varmasti omaa toteutustani ja ajatuksiani.

Luottamus tekoälyn tuottamaan sisältöön syntyi kolmella tavalla: ensin tarkistin koodiin liittyvät ehdotukset ajamalla sovellusta ja testaamalla endpointteja Swaggerissa, toiseksi vertasin ratkaisuja FastAPIn ja SQLModelin dokumentaatioon, ja kolmanneksi arvioin, tuntuiko ehdotettu ratkaisu järkevältä tässä projektissa. Vasta kun nämä kolme kohtasivat, hyväksyin muutoksen osaksi lopullista versiota.

Lopputuloksena voin aika hyvällä omallatunnolla sanoa, että AnturiAPI on minun tekemäni ja ymmärrän sen jokaisen koodirivin toiminnon – tekoäly auttoi, kyseenalaisti ja nopeutti, mutta ei päättänyt puolestani. Myös pari sataa committia GitHubissa kertoo, että projektiin käytettiin aikaa ja vaivaa.
