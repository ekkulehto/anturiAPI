# AnturiAPI

AnturiAPI on REST-rajapinta kuvitteellisen tehdashallin lämpötila-anturidatan keräämiseen ja hallintaan.
API on suunniteltu toimimaan taustapalveluna erilliselle web- tai mobiilikäyttöliittymälle.

Nykyisessä versiossa anturit mittaavat vain lämpötilaa, mutta rajapinta on suunniteltu laajennettavaksi myös muille mittaustyypeille. Tiedonsiirrossa käytetään JSON-muotoisia viestejä ja relaatiotietokantana toimii SQLite.

---

## Tekninen toteutus

*   **Kieli:** Python 3.13
*   **Web-kehys:** FastAPI
*   **ORM / mallit:** SQLModel
*   **Tietokanta:** SQLite
*   **Validointi:** Pydantic (v2)
*   **Kehityspalvelin:** fastapi dev

API tarjoaa automaattisesti generoidun interaktiivisen dokumentaation (Swagger UI).

---

## Asennus ja käynnistys

Ohjeet olettavat, että **Python 3.13** on asennettuna ja komennot ajetaan projektin juurikansiossa, jossa `src/`-hakemisto ja `requirements.txt` sijaitsevat.

### 1. Virtuaaliympäristön luonti (suositeltavaa)

On suositeltavaa luoda eristetty ympäristö riippuvuuksille.

**Windows:**
  ```
  python -m venv .venv
  .venv\Scripts\activate
  ```

**Linux / macOS:**
  ```
  python -m venv .venv
  source .venv/bin/activate
  ```

### 2. Riippuvuuksien asennus
  ```
  pip install -r requirements.txt
  ```

### 3. Palvelimen käynnistys

Käynnistä sovellus FastAPIn kehityskomennolla projektin juuresta:
  ```
  fastapi dev .\src\main.py
  ```
*(Huom: Linux/macOS-ympäristössä polku on ./src/main.py)*

### 4. Dokumentaation avaus ja testaus

Kun palvelin on käynnissä, avaa selain ja siirry osoitteeseen:
*   **Swagger UI:** http://127.0.0.1:8000/docs

---

## Pikaopas käyttöön (Esimerkki)

Kun olet avannut Swagger UI:n, voit testata API:n toimintaa seuraavassa järjestyksessä:

1.  **Luo Segmentti:**
    *   Avaa `POST /segments`
    *   Paina "Try it out" ja lähetä JSON: `{ "name": "LOHKO 1" }`
    *   Tämä on välttämätöntä, koska anturi tarvitsee segmentin.

2.  **Luo Anturi:**
    *   Avaa `POST /sensors`
    *   Lähetä JSON: `{ "name": "Lämpö 1", "segment_id": 1 }`

3.  **Lähetä Mittaus:**
    *   Avaa `POST /measurements`
    *   Lähetä JSON:
        ```
        {
          "sensor_id": 1,
          "measurement": {
            "value": 22.5,
            "unit": "CELSIUS",
            "type": "TEMPERATURE"
          }
        }
        ```

4.  **Tarkastele dataa:**
    *   Avaa `GET /sensors/1` nähdäksesi anturin ja sen mittaukset.

---

## Rajapinnan resurssit

API koostuu kolmesta pääresurssista:

### 1. Sensors (Anturit)
Antureiden hallinta, tilatietojen päivitys ja datan haku.

*   `GET /sensors`: Listaa kaikki anturit. Tukee suodatusta tilan mukaan (esim. `?status=ERROR`).
*   `POST /sensors`: Luo uuden anturin ja liittää sen segmenttiin. Anturin poisto poistaa automaattisesti myös sen mittaukset ja tilahistorian (cascade delete).
*   `GET /sensors/{sensor_id}`: Hakee yksittäisen anturin tiedot ja sen mittaushistorian (oletuksena 10 viimeisintä).
*   `PATCH /sensors/{sensor_id}`: Päivittää anturin tietoja (nimi, segmentti).
*   `DELETE /sensors/{sensor_id}`: Poistaa anturin ja kaikki sen mittaukset.
*   `GET /sensors/{sensor_id}/status_history`: Hakee anturin tilamuutoshistorian (`NORMAL` / `ERROR ` aikaleimoineen).
*   `POST /sensors/{sensor_id}/status`: Muuttaa anturin tilaa. Anturi ei voi lähettää mittauksia ERROR-tilassa.

### 2. Measurements (Mittaukset)
Yksittäisten mittaustulosten käsittely. Mittausarvot pyöristetään automaattisesti yhteen desimaaliin tallennuksen yhteydessä.

*   `GET /measurements`: Listaa kaikki järjestelmän mittaukset.
*   `POST /measurements`: Vastaanottaa uuden mittauksen anturilta.
*   `GET /measurements/{measurement_id}`: Hakee yksittäisen mittauksen tiedot ID:n perusteella.
*   `DELETE /measurements/{measurement_id}`: Poistaa yksittäisen mittauksen (esim. virheellisen datan siivous).

### 3. Segments (Lohkot)
Tehdashallin lohkojen hallinta ja niihin kuuluvien antureiden tarkastelu.

*   `GET /segments`: Listaa kaikki segmentit ja niissä olevien antureiden lukumäärän.
*   `POST /segments`: Luo uuden segmentin.
*   `GET /segments/{segment_id}`: Hakee segmentin tiedot sekä listan sen antureista ja näiden viimeisimmistä mittauksista.
*   `PATCH /segments/{segment_id}`: Päivittää segmentin nimen.
*   `DELETE /segments/{segment_id}`: Poistaa segmentin. (Huom: Segmentin tulee olla tyhjä antureista ennen poistoa).

---

## Suodatus ja haut

Datanäkymiä voidaan rajata tarkemmin kyselyparametreilla (Query Parameters):

*   **Anturin haku (`GET /sensors/{id}`):** Keskittyy aikasarjaan.
    *   `limit`: Palautettavien mittausten määrä.
    *   `since` / `until`: Aikavälin rajaus.
*   **Segmentin haku (`GET /segments/{id}`):** Keskittyy tilannekuvaan.
    *   `limit`: Palautettavien mittausten määrä per anturi.
    *   `measurement_type`: Hae vain tietyn tyyppiset mittaukset (oletus: `TEMPERATURE`).
    *   `since` / `until`: Aikavälin rajaus.

---

## Tietomallit ja automatiikka

### Anturi (Sensor)
*   **Tila (status):** `NORMAL` (oletus) tai `ERROR`.
*   **Toiminta:** ERROR-tilassa oleva anturi hylkää uudet mittaukset. Tila on palautettava normaaliksi rajapinnan kautta.
*   **Relaatiot:** Anturin poisto poistaa automaattisesti myös siihen liittyvät mittaukset ja tilahistorian tietokannasta (`cascade: all, delete-orphan`).

### Mittaus (Measurement)
Mittausdata validoidaan automaattisesti ennen tallennusta.
*   **Arvo (value):** Pyöristetään automaattisesti yhteen desimaaliin (esim. 24.567 -> 24.6).
*   **Aikaleima (timestamp):** Tallennetaan UTC-ajassa. Luodaan automaattisesti, jos sitä ei anneta pyynnössä.
*   **Yksikkö (unit) ja tyyppi (type):** Oletusarvoina `CELSIUS` ja `TEMPERATURE`, jos niitä ei määritellä erikseen.

**Uuden mittauksen lähetysrakenne (POST):**

```bash
    {
      "sensor_id": 1,
      "measurement": {
        "value": 24.567,
        "unit": "CELSIUS",
        "type": "TEMPERATURE",
        "timestamp": "2025-12-06T19:57:12.020Z"
      }
    }
```

*Yllä oleva esimerkki tallentuisi arvolla 24.6.*

### Segmentti (Segment)
Sisältää segmentin nimen ja ID:n. Toimii antureiden ryhmittelytasona. Segmenttiä ei voi poistaa, jos siinä on aktiivisia antureita.