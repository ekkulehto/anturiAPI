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

API tarjoaa automaattisesti generoidun interaktiivisen dokumentaation (Swagger UI), jossa kaikki endpointit ovat kokeiltavissa suoraan selaimesta.

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
   * Paina **Try it out** ja lähetä JSON:

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

   * Avaa `POST /sensors/{sensor_id}/measurements` (esim. `sensor_id = 1`)  
   * Lähetä JSON:

         {
           "value": 22.5,
           "unit": "CELSIUS",
           "type": "TEMPERATURE",
           "timestamp": "2025-12-08T10:00:00Z"
         }

   * `timestamp`-kentän voi jättää myös pois, jolloin palvelin luo sen automaattisesti.

4. **Tarkastele Dataa**

   * `GET /sensors/1` – anturin perustiedot (nimi, lohko, tila).  
   * `GET /sensors/1/measurements` – anturin uusimmat mittaukset.  
   * `GET /sensors/1/status/history` – anturin tilamuutokset ajassa.  
   * `GET /segments/1` – segmentin sensoreiden tilannekuva (tila + viimeisin mittaus per anturi).  

---

## Rajapinnan resurssit lyhyesti

Swagger-dokumentaatiossa endpointit on ryhmitelty loogisiksi kokonaisuuksiksi:

* **Segments** – tehdashallin lohkot, joihin anturit liitetään  
* **Sensors** – anturien luonti, muokkaus, poisto ja perustietojen haku  
* **Sensor Status** – anturin tilan (`NORMAL` / `ERROR`) päivitys ja tilahistoria  
* **Sensor Measurements** – mittausten lisääminen ja hakeminen anturikohtaisesti  
* **Measurements** – yksittäisten mittausten käsittely globaalin `measurement_id`-arvon perusteella  

---

## Tietomallit lyhyesti

Rajapinnan sisäinen malli rakentuu muutaman selkeän kokonaisuuden ympärille:

* **Segmentit**  
  * Ryhmittelevät sensoreita (esim. tehdashallin lohkot).  
  * Yhdellä segmentillä voi olla monta sensoria.  

* **Sensorit**  
  * Kuuluvat aina johonkin segmenttiin.  
  * Sensoreilla on nykyinen tila ja ne tuottavat mittauksia.  
  * Ei voi lähettää mittauksia `ERROR`-tilassa.
  * Jos sensori poistetaan, siihen liittyvät mittaukset ja tilahistoria poistuvat automaattisesti.

* **Tilahistoria**  
  * Jokainen tilan vaihto (esim. `NORMAL` → `ERROR`) tallentuu omana rivinään tilahistoriaan.  
  * Tilahistorian rivit kytkeytyvät aina yhteen sensoriin, samalla tavalla kuin mittaukset.  
  * Jos sensori poistetaan, myös sen koko tilahistoria poistuu automaattisesti.  
  * Tätä dataa voidaan käyttää esim. graafeihin ja raportointiin siitä, milloin antureissa on esiintynyt virhetiloja.

* **Mittaukset**  
  * Tallentuvat erilliseen mittaustauluun ja kytkeytyvät aina yhteen sensoriin.  
  * Mittausarvo (`value`) pyöristetään automaattisesti yhteen desimaaliin.  
  * Mittauksella on yksikkö (`CELSIUS`), tyyppi (`TEMPERATURE`) ja aikaleima (UTC).  
  * Mittaus ei voi olla olemassa ilman siihen liittyvää sensoria – sensorin poistuessa myös sen mittaukset poistetaan.

Yhdessä nämä muodostavat kokonaisuuden, jossa:

* Segmentit ryhmittelevät anturit  
* Sensorit kuuluvat segmentteihin ja lähettävät mittauksia  
* Mittaukset ja tilamuutokset tallentuvat historiaan analyysiä ja seurantaa varten  
* Sensorin poistaminen siivoaa automaattisesti siihen liittyvän mittaus- ja tilahistoriadatan  
