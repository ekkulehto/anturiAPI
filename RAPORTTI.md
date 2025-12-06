# Raportti – AnturiAPI

## 1. Johdanto

Tässä työssä toteutin **AnturiAPI:n**, joka on REST-rajapinta kuvitteellisen tehdashallin lämpötila-anturidatan keräämiseen ja hallintaan. API ei sisällä käyttöliittymää, vaan se on tarkoitettu toimimaan taustapalveluna esimerkiksi web- tai mobiilisovellukselle.

Rajapinnan tavoitteena on:
*   Vastaanottaa mittauksia antureilta.
*   Hallita anturien tilaa ja niiden sijoittelua lohkoihin (segmentteihin).
*   Tarjota riittävän monipuoliset datanäkymät käyttöliittymän tarpeisiin.
*   Olla helposti laajennettavissa tulevaisuudessa (esim. uusia mittaustyyppejä, yksiköitä ja anturitiloja).

---

## 2. Käytetyt resurssit ja tekniset valinnat

### 2.1 Aiempi kokemus ja lähtökohta
Minulla oli tehtävään pieni etulyöntiasema aiemman tekoälyprojektin ansiosta, jossa hyödynsin laajasti Hevy-kuntosalisovelluksen Swagger-dokumentaatiota ja sen API-kutsuja. Tuolloin opin:
*   Miten Swaggerin interaktiivista dokumentaatiota käytetään tehokkaasti.
*   Miten endpoint-kutsujen tekeminen on käytännössä sujuvinta.
*   Kuinka Pydantic-malleja ja API-kutsuja on kätevä yhdistellä.

Tämän ansiosta minulla oli heti alussa selkeä visio rakennettavasta API:sta ja tavoitellusta käyttökokemuksesta Swagger-dokumentaatiossa.

### 2.2 Valitut kirjastot ja perustelut valinnoille
Päädyin käyttämään kurssilla opeteltuja teknologioita, koska ne soveltuvat erinomaisesti juuri tämän tyyppiseen backend-projektiin:

*   **FastAPI**
    *   *Miksi:* Koska projektissa ei ole käyttöliittymää, FastAPIn automaattisesti generoima interaktiivinen dokumentaatio (Swagger UI) on korvaamaton työkalu testauksessa ja kehityksessä. Se myös nopeuttaa kehitystä verrattuna raskaampiin frameworkeihin.
*   **SQLModel (Pydantic + SQLAlchemy)**
    *   *Miksi:* Se mahdollistaa tietokantataulujen ja API-validointimallien määrittelyn samassa luokassa. Tämä vähentää koodin määrää (ei tarvitse ylläpitää erillisiä malleja tietokannalle ja APIlle) ja vähentää virheitä tyypityksessä.
*   **SQLite**
    *   *Miksi:* Tehtävänanto vaati relaatiotietokannan. SQLite on tähän tarkoitukseen paras valinta, koska se ei vaadi erillistä palvelinasennusta, vaan toimii tiedostona. Tämä tekee projektin tarkastamisesta ja siirtämisestä helppoa.

Lisäksi hyödynsin Pythonin standardikirjastoa (mm. `datetime`) sekä FastAPIn työkaluja riippuvuuksien injektointiin (`Depends`) ja virheiden hallintaan (`HTTPException`).

### 2.3 Projektin rakenne
Projektin rakenne on jaettu selkeästi niin, että varsinainen lähdekoodi sijaitsee `src`-kansion alla. Juuressa ovat vain projektin hallintaan liittyvät tiedostot (kuten `requirements.txt`, `README.md` ja tietokanta `sensors.db`).

Koodi on jaoteltu seuraavasti `src`-kansion sisällä:

*   **Ydintiedostot:**
    *   `main.py`: Sovelluksen käynnistys ja reitittimien (routers) yhdistäminen.
    *   `database.py`: Tietokantayhteyden hallinta ja sessioiden luonti.
    *   `models.py`: Kaikki keskeiset tietomallit (`SensorDb`, `SegmentDb`, `MeasurementDb`, enum-tyypit, ulostulomallit) on keskitetty tänne selkeyden vuoksi.

*   **Moduulit (`measurements`, `segments`, `sensors`):**
    Jokainen pääresurssi on omassa kansiossaan, joka sisältää:
    *   `router.py`: Endpointien polut ja HTTP-pyyntöjen käsittely.
    *   `service.py`: Liiketoimintalogiikka ja tietokantaoperaatiot.
    *   `schemas.py`: Moduulikohtaiset apumallit (esim. suodatusluokat).
    *   `docs.py`: Swagger-dokumentaation tekstikuvaukset (`summary`, `description`), jotta ne eivät tuki reititintiedostoa.

Yritin aluksi pilkkoa myös `models.py`-tiedostoa pienempiin osiin, mutta se johti nopeasti hankaliin *circular import* -ongelmiin. Päädyin lopulta pitämään mallit yhdessä tiedostossa, mikä osoittautui selkeimmäksi ratkaisuksi. Muu logiikka on kuitenkin eriytetty omiin moduuleihinsa.

---

## 3. Endpointien polkusuunnittelu

### 3.1 Pääresurssit
Polut rakentuivat kolmen pääresurssin ympärille, mikä palvelee sekä backendin rakennetta että käyttöliittymän logiikkaa:
1.  `/sensors` – Yksittäiset anturit, niiden tila ja historiat.
2.  `/measurements` – Yksittäiset mittaukset.
3.  `/segments` – Lohkot, joihin anturit kuuluvat.

### 3.2 Anturien polut
*   `GET /sensors`: Listaa kaikki anturit (suodatus tilan perusteella).
*   `POST /sensors`: Luo uuden anturin ja liittää sen segmenttiin.
*   `GET /sensors/{sensor_id}`: Palauttaa anturin tiedot ja mittaukset.
*   `PATCH /sensors/{sensor_id}`: Päivittää anturin nimeä ja/tai segmenttiä.
*   `DELETE /sensors/{sensor_id}`: Poistaa anturin ja sen mittaukset.
*   `GET /sensors/{sensor_id}/status_history`: Anturin tilamuutosten historia.
*   `POST /sensors/{sensor_id}/status`: Vaihtaa anturin tilan.

Liitin status-historian ja sen muuttamisen suoraan sensoriin, koska status on loogisesti anturin ominaisuus.

### 3.3 Mittausten polut
*   `GET /measurements`: Listaa mittaukset (suodatus tyypin perusteella).
*   `POST /measurements`: Lisää uuden mittauksen anturille.
*   `GET /measurements/{measurement_id}`: Yksittäisen mittauksen haku.
*   `DELETE /measurements/{measurement_id}`: Yksittäisen mittauksen poisto.

Mittaukset ovat oma resurssinsa, mutta vahvasti kytköksissä anturiin. Luontipyyntö sisältää `sensor_id`:n ja sisäkkäisen `measurement`-objektin (arvo, yksikkö, tyyppi, aikaleima). Tämä rakenne mahdollistaa uusien mittaustyyppien lisäämisen ilman API:n perusrakenteen rikkomista.

### 3.4 Segmenttien polut
*   `GET /segments`: Listaa kaikki segmentit (ml. sensorien lukumäärä).
*   `POST /segments`: Luo uuden segmentin.
*   `GET /segments/{segment_id}`: Palauttaa segmentin, sen sensorit ja näiden mittaukset.
*   `PATCH /segments/{segment_id}`: Päivittää segmentin nimen.
*   `DELETE /segments/{segment_id}`: Poistaa segmentin (vain jos tyhjä).

`GET /segments/{segment_id}` toteutettiin vaatimuksia laajemmin: se mahdollistaa useamman mittauksen hakemisen, määrän rajaamisen sekä suodatuksen mittaustyypin ja aikavälin perusteella.

### 3.5 DELETE- ja virhekäyttäytyminen
REST-käytäntöjen mukaisesti `DELETE`-kutsut palauttavat statuskoodin **204 No Content** ilman bodya.

Logiikkasääntöjä:
*   Anturi virhetilassa (`ERROR`) ei saa lähettää mittauksia (API palauttaa virheen).
*   Segmenttiä ei voi poistaa, jos siinä on sensoreita (API palauttaa 400 Bad Request).

---

## 4. Tietomallit ja laajennettavuus

### 4.1 Perusrakenne
Tietokantamallit (`SQLModel`):
*   `SensorDb`: Yksittäinen anturi.
*   `SegmentDb`: Lohko, johon anturi kuuluu.
*   `MeasurementDb`: Yksittäinen mittaustulos.
*   `SensorStatusDb`: Anturin tilamuutosten historia (aikaleimoineen).

Erillinen `SensorStatusDb` osoittautui parhaaksi tavaksi toteuttaa luotettava status-historia.

### 4.2 Mittausmalli ja Enum-tyypit
Mittaukset on suunniteltu laajennettaviksi.
*   **Tietokanta (`MeasurementDb`):** `sensor_id`, `value`, `unit`, `type`, `timestamp`.
*   **Enumit:** `MeasurementType` (esim. TEMPERATURE) ja `MeasurementUnit` (esim. CELSIUS).
*   **API Payload:** Sisältää arvot, tyypin ja yksikön. Aikaleima on vapaaehtoinen; jos sitä ei anneta, palvelin luo sen.

### 4.3 Suodattimet ja haku
Toteutin erilliset suodatinmallit hauille:
*   **MeasurementFilterForGetSensorById:** Anturin mittausten rajaaminen (`limit`, `since`, `until`).
*   **MeasurementFilterForGetSegmentById:** Segmentin datan rajaaminen (`limit`, `MeasurementType`, `since`, `until`).

Tavoitteena oli, että API toimii ilman parametreja ("näytä kaikki"), mutta tarjoaa tarvittaessa tarkan suodatuksen.

---

## 5. Oppimiskokemukset

### 5.1 Suunnittelu ennen koodausta
Käytin ensimmäisen päivän `models.py`:n suunnitteluun. Tämä auttoi hahmottamaan relaatiot ja datavirrat (input vs. output) ennen koodauksen aloittamista, mikä säästi aikaa myöhemmin.

### 5.2 Relaatiot ja SQLModel
Opin projektin aikana paljon SQLModelin relaatioista:
*   `Relationship`- ja `back_populates`-määrittelyjen käyttö.
*   Ero tietokantamallien ja ulostulomallien välillä.

### 5.3 Sisäkkäiset mallit ja palautusarvot
Suurin haaste liittyi sisäkkäisiin malleihin (esim. lista sensoreita, joilla on sisäkkäisiä mittauksia). Jouduin korjaamaan malleja ja kyselyitä useasti, mutta opin ymmärtämään `model_validate`-kutsujen tarpeen ja manuaalisten vastausmallien rakentamisen logiikan.

### 5.4 Refaktorointi ja "Best Practices"
Projektin loppuvaiheessa refaktoroin koodia *FastAPI Best Practices* -ohjeiden mukaiseksi. Tämä näkyy lopullisessa rakenteessa, jossa routerit, service-kerrokset ja dokumentaatiotiedostot on eriytetty moduuleittain (`src/measurements`, `src/segments` jne.).

### 5.5 Yleinen fiilis
Laajan API:n rakentaminen oli yllättävän suoraviivaista, kun peruspalikat olivat kunnossa. Suurin työmäärä kohdistui suunnitteluun, mallien yhteensovittamiseen ja dokumentaation hiomiseen.

---

## 6. Keinoälyn käyttö työssä

Tässä projektissa käytin keinoälynä **ChatGPT 5.1**:tä. Käyttö oli avustavaa, ei koodin automaattista generointia alusta loppuun.

### 6.1 Missä käytin keinoälyä
*   **Suunnitteluvaihe:** Alkuperäinen visio syntyi ilman tekoälyä, mutta käytin sitä sparrailuapuna relaatiomallien (SensorDb, SegmentDb, jne.) selkeyttämisessä.
*   **Virheenkorjaus:** Pyysin apua syntaksivirheiden ja "circular import" -ongelmien ratkaisemisessa.
*   **Sisäkkäiset mallit:** Hyödynsin tekoälyä tietokantamallien ja API-vastausmallien välisten muunnosten (esim. `MeasurementDb` → `MeasurementOutWithSensor`) rakentamisessa.
*   **Swagger-dokumentaatio:** Annoin tekoälyn muotoilla luonnoksia `summary`- ja `description`-teksteistä, jotka viimeistelin itse vastaamaan tarkasti toteutusta.
*   **Dokumentaation puhtaaksikirjoitus:** Lopuksi käytin tekoälyä kirjoittamaan puhtaaksi `README.md`-tiedoston sekä tämän `RAPORTTI.md`-tiedoston (Gemini 3 Pro Preview).

### 6.2 Miten varmistin, että tulos on oikea
En luottanut vastauksiin sokeasti, vaan:
*   Tarkistin ratkaisut FastAPI:n ja SQLModelin virallisesta dokumentaatiosta.
*   Testasin API:a jatkuvasti paikallisesti ja Swaggerin kautta.
*   Simuloin virhetilanteita (esim. poistoestot ja virheelliset syötteet).

Ratkaisu todettiin valmiiksi vasta, kun koodi, dokumentaatio ja käytännön testit olivat linjassa.

### 6.3 Miksi käytin keinoälyä
Käytin tekoälyä kuten kokeneempaa kollegaa: nopeuttamaan virheiden löytämistä, tarjoamaan vaihtoehtoisia mallinnustapoja ja säästämään aikaa rutiininomaisessa tekstinmuotoilussa. Lopullinen vastuu ratkaisusta ja sen ymmärtämisestä on minulla.