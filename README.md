# AnturiAPI

AnturiAPI on REST-rajapinta kuvitteellisen tehdashallin lämpötila-anturidatan keräämiseen ja hallintaan. API on suunniteltu toimimaan taustapalveluna erilliselle web- tai mobiilikäyttöliittymälle.

Nykyisessä versiossa anturit mittaavat vain lämpötilaa, mutta rajapinta on suunniteltavissa laajennettavaksi myös muille mittaustyypeille. Tiedonsiirrossa käytetään JSON-muotoisia viestejä ja relaatiotietokantana toimii SQLite.

---

## Tekninen toteutus

* **Kieli:** Python 3.13  
* **Web-kehys:** FastAPI  
* **ORM / mallit:** SQLModel  
* **Tietokanta:** SQLite  
* **Validointi:** Pydantic (v2)  
* **Kehityspalvelin:** fastapi dev  

API tarjoaa automaattisesti generoidun interaktiivisen dokumentaation (Swagger UI).

---

## Asennus ja käynnistys

Ohjeet olettavat, että **Python 3.13** on asennettuna ja komennot ajetaan projektin juurikansiossa, jossa `src/`-hakemisto ja `requirements.txt` sijaitsevat.

### 1. Virtuaaliympäristön luonti (suositeltavaa)

On suositeltavaa luoda eristetty ympäristö riippuvuuksille.

**Windows:**

    python -m venv .venv
    .venv\Scripts\activate

**Linux / macOS:**

    python -m venv .venv
    source .venv/bin/activate

### 2. Riippuvuuksien asennus

    pip install -r requirements.txt

### 3. Palvelimen käynnistys

Käynnistä sovellus FastAPIn kehityskomennolla projektin juuresta:

    fastapi dev .\src\main.py

*(Huom: Linux/macOS-ympäristössä polku on `./src/main.py`.)*

### 4. Dokumentaation avaus ja testaus

Kun palvelin on käynnissä, avaa selain ja siirry osoitteeseen:

* **Swagger UI:** http://127.0.0.1:8000/docs

---

## Pikaopas käyttöön

Kun olet avannut Swagger UI:n, voit testata API:n toimintaa esimerkiksi seuraavassa järjestyksessä:

1. **Luo Segmentti**

   * Avaa `POST /segments`  
   * Paina "Try it out" ja lähetä JSON:

         {
           "name": "LOHKO_1"
         }

   * Segmentti on välttämätön, koska anturi liitetään aina johonkin lohkoon.

2. **Luo Anturi**

   * Avaa `POST /sensors`  
   * Lähetä JSON (olettaen, että segmentin id on 1):

         {
           "name": "ANTURI_1",
           "segment_id": 1
         }

3. **Lähetä Mittaus Anturilta**

   * Avaa `POST /sensors/{sensor_id}/measurements` (esim. sensor_id = 1)  
   * Lähetä JSON:

         {
           "value": 22.5,
           "unit": "CELSIUS",
           "type": "TEMPERATURE",
           "timestamp": "2025-12-08T10:00:00Z"
         }

   * `timestamp`-kentän voi jättää myös pois, jolloin palvelin luo sen automaattisesti.

4. **Tarkastele Dataa**

   * Avaa `GET /sensors/1` nähdäksesi anturin perustiedot (nimi, lohko, tila).  
   * Avaa `GET /sensors/1/measurements` nähdäksesi anturin uusimmat mittaukset.  
   * Avaa `GET /segments/1` nähdäksesi segmentin sensoreiden tilannekuvan (tila + viimeisin mittaus per anturi).

---

## Rajapinnan resurssit

Swagger-dokumentaatiossa resurssit näkyvät seuraavassa järjestyksessä:

1. **Segments**  
2. **Sensors**  
3. **Sensor Status**  
4. **Sensor Measurements**  
5. **Measurements**

### 1. Segments (Lohkot)

Tehdashallin lohkojen hallinta ja niihin kuuluvien antureiden tarkastelu.

* `GET /segments`  
  Listaa kaikki segmentit.  
  Vastauksessa näkyy segmenttien perustiedot (id, name).

* `POST /segments`  
  Luo uuden segmentin.

      {
        "name": "LOHKO_1"
      }

* `GET /segments/{segment_id}`  
  Hakee segmentin tiedot sekä listan sen antureista.  
  Jokaiselle sensorille palautetaan:

  * tunniste (`id`, `name`)  
  * nykyinen tila (`status`)  
  * viimeisin mittaus (`last_measurement`), tai `null` jos sensori ei ole vielä lähettänyt mittauksia  

  Lisäksi endpoint tukee sensoreiden suodatusta nykyisen tilan perusteella:

  * query-parametri `sensor_status` (esim. `NORMAL`, `ERROR`)  

  Esimerkki: `GET /segments/1?sensor_status=ERROR` palauttaa vain virhetilassa olevat anturit ja niiden viimeisimmät mittaukset.

* `PATCH /segments/{segment_id}`  
  Päivittää segmentin nimen.  
  Jos uusi nimi on sama kuin vanha tai nimeä ei anneta, segmenttiä ei kirjoiteta turhaan uudelleen tietokantaan.

* `DELETE /segments/{segment_id}`  
  Poistaa segmentin **vain jos segmentissä ei ole yhtään anturia**.  
  Jos segmenttiin on liitetty sensoreita, rajapinta palauttaa virheen ja poisto estetään.

---

### 2. Sensors (Anturit)

Antureiden hallinta, tilatietojen päivitys ja hakeminen.

* `GET /sensors`  
  Listaa kaikki anturit.  
  Tukee suodatusta tilan mukaan query-parametrilla `sensor_status` (esim. `?sensor_status=ERROR`).  
  Vastauksessa näkyy ainakin anturin tunniste, nimi, segmentti ja nykyinen tila.

* `POST /sensors`  
  Luo uuden anturin ja liittää sen segmenttiin.

      {
        "name": "ANTURI_1",
        "segment_id": 1
      }

  Uudelle sensorille asetetaan automaattisesti tila `NORMAL`, ja tilahistoriaan luodaan ensimmäinen rivi (`NORMAL` + timestamp).

* `GET /sensors/{sensor_id}`  
  Hakee yksittäisen anturin perustiedot:  
  tunniste, nimi, segmentti, nykyinen tila (`status`).  
  Mittaushistoria haetaan erillisellä Sensor Measurements -endpointilla.

* `PATCH /sensors/{sensor_id}`  
  Päivittää anturin tietoja (esimerkiksi nimen tai lohkon vaihtaminen).  
  Jos päivitettävät arvot ovat samat kuin nykyiset, anturia ei kirjoiteta turhaan uudelleen tietokantaan.

* `DELETE /sensors/{sensor_id}`  
  Poistaa anturin ja kaikki siihen liittyvät mittaukset sekä tilahistorian tietokannasta  
  (toteutettu kaskadipoistona / delete-orphan -tyyppisesti).

---

### 3. Sensor Status (Anturin tila ja tilahistoria)

Anturin tilamuutokset (`NORMAL`, `ERROR`) mallinnetaan erillisenä resurssina.

* `GET /sensors/{sensor_id}/status/history`  
  Hakee anturin tilamuutoshistorian uusimmasta vanhimpaan.  
  Jokaisella rivillä on tila (`status`) ja aikaleima (`timestamp`).  
  Tätä dataa voidaan käyttää esimerkiksi graafin piirtämiseen virhetilanteiden esiintymisajankohdista.

* `POST /sensors/{sensor_id}/status`  
  Muuttaa anturin nykyistä tilaa ja tallentaa muutoksen tilahistoriaan.

      {
        "status": "ERROR"
      }

  Anturin ajatellaan lopettavan mittausten lähettämisen ollessaan `ERROR`-tilassa, ja tila palautetaan normaaliksi vain tämän endpointin kautta.  
  Jos uusi tila on sama kuin nykyinen tila, status-historiaan ei lisätä uutta riviä eikä anturin statusta päivitetä turhaan uudelleen.

---

### 4. Sensor Measurements (Mittaukset anturikohtaisesti)

Mittaukset käsitellään anturin aliresurssina silloin, kun halutaan tarkastella tai lisätä mittauksia nimenomaan tietylle sensorille. Mittausarvot pyöristetään automaattisesti yhteen desimaaliin tallennuksen yhteydessä.

* `GET /sensors/{sensor_id}/measurements`  
  Listaa anturin mittaukset.  
  Oletuksena palautetaan 10 uusinta mittausta.  
  Tukee seuraavia kyselyparametreja:

  * `measurement_type` – mittaustyyppi, jos käytössä on useampia kuin yksi tyyppi  
  * `limit` – palautettavien mittausten määrä (1–100, oletus 10)  
  * `since` – aikavälin alku (ISO 8601 -aikaleima)  
  * `until` – aikavälin loppu (ISO 8601 -aikaleima)  

* `POST /sensors/{sensor_id}/measurements`  
  Vastaanottaa uuden mittauksen anturilta.

      {
        "value": 24.567,
        "unit": "CELSIUS",
        "type": "TEMPERATURE",
        "timestamp": "2025-12-06T19:57:12.020Z"
      }

  Tallennusvaiheessa `value` pyöristyy automaattisesti yhteen desimaaliin (esimerkissä 24.6).  
  `timestamp` voidaan jättää pois, jolloin palvelin käyttää nykyhetkeä (UTC).  

  Lisäksi liiketoimintasääntö:  
  * Jos sensori on tilassa `ERROR`, mittaus hylätään ja palvelin palauttaa virheen.  
    Toisin sanoen virhetilassa oleva sensori **ei voi** lähettää mittauksia, ja tämä on estetty myös palvelinpäässä.

---

### 5. Measurements (Yksittäiset mittaukset)

Measurements-resurssi tarjoaa tavan käsitellä yksittäisiä mittauksia niiden globaalin tunnisteen (`measurement_id`) perusteella riippumatta siitä, miltä sensorilta mittaus on tullut.

* `GET /measurements/{measurement_id}`  
  Hakee yksittäisen mittauksen tiedot `measurement_id`-arvon perusteella.  
  Palauttaa mittauksen peruskentät (`MeasurementOut`), kuten arvon, tyypin, yksikön ja aikaleiman.

* `DELETE /measurements/{measurement_id}`  
  Poistaa yksittäisen mittauksen (esimerkiksi virheellisen datan siivoaminen).  
  Jos mittausta ei löydy, palautetaan virhe (404).

---

## Suodatus ja haut

Datanäkymiä voidaan rajata tarkemmin kyselyparametreilla (Query Parameters).

* **Anturien listaus (`GET /sensors`)** – keskittyy anturien tilaan ja perusinfoon.
  * `sensor_status`: suodattaa anturit nykyisen tilan mukaan (esim. `NORMAL`, `ERROR`).

* **Segmentin haku (`GET /segments/{segment_id}`)** – keskittyy tilannekuvaan lohkotasolla.
  * `sensor_status`: suodattaa segmentin anturit nykyisen tilan mukaan.  
    Palauttaa segmentin sensoreista listan, jossa kullekin anturille on tila ja viimeisin mittaus.

* **Anturin mittaushistoria (`GET /sensors/{sensor_id}/measurements`)** – keskittyy aikasarjaan.
  * `measurement_type`: mittaustyyppi, jos käytössä on useampia tyyppejä.  
  * `limit`: palautettavien mittausten määrä (oletus 10).  
  * `since` / `until`: aikavälin rajaus.  

---

## Tietomallit ja automatiikka

Tässä kaikki projektissa käytetyt tietomallit:

1. Enumerables  
2. Segments  
3. Sensors  
4. Sensor Statuses  
5. Measurements  

### 1. Enumerables

* **SensorStatus**  
  * `NORMAL` – normaali toimintatila  
  * `ERROR` – virhetilanne, jossa anturi ei saa lähettää mittauksia

* **MeasurementType**  
  * `TEMPERATURE` – lämpötilamittaus (nykyisessä versiossa ainoa käytössä oleva tyyppi)

* **MeasurementUnit**  
  * `CELSIUS` – lämpötilan yksikkö (°C)

Näitä enum-tyyppejä käytetään sekä tietokantamalleissa että rajapinnan vastauksissa, jotta arvojen vaihteluväli pysyy hallittuna ja selkeänä.

---

### 2. Segments (Segmenttimallit)

* **SegmentBase / SegmentIn**  
  * Yksinkertainen malli, jossa on vain `name`.  
  * Käytetään uuden segmentin luonnissa (`POST /segments`).

* **SegmentOut**  
  * Palautusmalli, jossa on `id` ja `name`.

* **SegmentOutWithNumberOfSensors**  
  * Palautusmalli, jossa näkyy segmentin id, nimi ja segmenttiin liitettyjen sensoreiden lukumäärä.  
  * Soveltuu esimerkiksi yleisiin listausnäkymiin.

* **SegmentOutWithSensors**  
  * Palauttaa segmentin id:n, nimen ja listan sen sensoreista (`SensorOutInSegmentWithLastMeasurement`).  
  * Käytössä `GET /segments/{segment_id}` -endpointissa.

* **SegmentDb**  
  * Tietokantamalli (taulu), jossa:  
    * `id` – pääavain  
    * `name` – segmentin nimi  
    * `sensors` – suhde sensoreihin (yksi segmentti, monta sensoria)

---

### 3. Sensors (Anturimallit)

* **SensorBase / SensorIn**  
  * Kentät:  
    * `name` – anturin nimi  
    * `segment_id` – viittaus lohkoon, johon anturi kuuluu  
  * `SensorIn`-mallia käytetään anturin luonnissa (`POST /sensors`).

* **SensorOut**  
  * Palauttaa anturin perustiedot:  
    * `id`, `name`, `status` (`SensorStatus`)  
    * `segment` (`SegmentOut`)

* **SensorOutWithMeasurements**  
  * Sisältää anturin perustiedot sekä listan mittauksista (`measurements: list[MeasurementOut]`).  
  * Soveltuu, kun halutaan palauttaa anturin metatiedot ja mittaussarja samassa vastauksessa.

* **SensorOutInSegmentWithLastMeasurement**  
  * Käytetään segmenttinäkymässä.  
  * Kentät: `id`, `name`, `status` sekä `last_measurement: MeasurementOut | null`.  
  * Jos anturi ei ole vielä lähettänyt yhtään mittausta, `last_measurement` on `null`.

* **SensorOutWithStatusHistory**  
  * Sisältää anturin tunnisteen, nimen, segmentin ja tilahistorian (`status_history: list[SensorStatusOut]`).  
  * Käytössä tilahistoria-endpointissa.

* **SensorDb**  
  * Tietokantamalli (taulu), jossa:  
    * `id` – pääavain  
    * `name` – anturin nimi  
    * `segment_id` – viittaus `SegmentDb`-tauluun  
    * `status` – nykyinen tila (`SensorStatus`, oletus `NORMAL`)  
    * `segment` – suhde segmenttiin  
    * `measurements` – suhde mittauksiin (`MeasurementDb`), kaskadipoisto käytössä (`cascade: all, delete-orphan`)  
    * `status_history` – suhde tilahistoriaan (`SensorStatusDb`), myös kaskadipoistolla

---

### 4. Sensor Statuses (Tilamallit)

* **SensorStatusBase / SensorStatusIn**  
  * Kentät:  
    * `status: SensorStatus`  
    * `timestamp: datetime` (oletuksena nykyhetki UTC-ajassa)  
  * `SensorStatusIn` sisältää lisäksi `sensor_id`-kentän, jota käytetään, kun tallennetaan uusi tilarivi tietokantaan.

* **SensorStatusOut**  
  * Palauttaa tilahistoriaan liittyvät tiedot:  
    * `id`, `status`, `timestamp`

* **SensorStatusDb**  
  * Tietokantamalli tilahistorian riveille:  
    * `id` – pääavain  
    * `sensor_id` – viittaus `SensorDb`-tauluun  
    * `status` – tilakoodi (`SensorStatus`)  
    * `timestamp` – tilamuutoksen aikaleima  
    * `sensor` – suhde takaisin sensoriin (`SensorDb.status_history`)

---

### 5. Measurements (Mittausmallit)

* **MeasurementBase**  
  * Sisältää `sensor_id`-kentän (mihin sensoriin mittaus liittyy).  
  * Perusluokka, jota muut mallit laajentavat.

* **MeasurementIn**  
  * Käytetään, kun anturi lähettää uuden mittauksen (`POST /sensors/{sensor_id}/measurements`).  
  * Kentät:  
    * `value: float` – mitattu arvo  
    * `unit: MeasurementUnit` – oletus `CELSIUS`  
    * `type: MeasurementType` – oletus `TEMPERATURE`  
    * `timestamp: datetime` – oletuksena nykyhetki UTC-ajassa  
  * `value` pyöristetään automaattisesti yhteen desimaaliin `field_validator`-funktion avulla.

* **MeasurementOut**  
  * Palautusmalli yksittäiselle mittaukselle:  
    * `id`, `value`, `unit`, `type`, `timestamp`

* **MeasurementOutWithSensor**  
  * Käytetään, kun halutaan palauttaa sekä mittaus että sen anturi.  
  * Kentät:  
    * `sensor_id` (peritty `MeasurementBase`-luokasta)  
    * `measurement: MeasurementOut`

* **MeasurementDb**  
  * Tietokantamalli mittauksille:  
    * `id` – pääavain  
    * `sensor_id` – viittaus `SensorDb`-tauluun  
    * `sensor` – suhde takaisin sensoriin (`SensorDb.measurements`)  
    * `value: float` – pyöristetty mittausarvo  
    * `unit: MeasurementUnit` – esim. `CELSIUS`  
    * `type: MeasurementType` – esim. `TEMPERATURE`  
    * `timestamp: datetime` – mittauksen aikaleima (UTC)

Yhdessä nämä mallit muodostavat johdonmukaisen kokonaisuuden, jossa:

* Segmentit ryhmittelevät sensoreita  
* Sensorit kuuluvat segmentteihin ja tuottavat mittauksia  
* Sensorien tilat ja tilahistoria tallentuvat erilliseen tauluun  
* Mittaukset ja tilahistoria ovat aina sidottuja tiettyyn sensoriin