# anturiAPI

## Hallinta
- Voi lisätä antureita järjestelmään
- Voi muuttaa anturin tilaa
- Voi muuttaa lohkoa johon anturi kuuluu
- Voi poistaa yksittäisen mittaustuloksen

## Datanäkymät
- Listataan kaikki anturit (näytetään tunniste, lohko ja tila)
- Listataan tietyn lohkon anturit (näytetään tunniste, tila sekä viimeisin mitta-arvo ja sen
aikaleima)
- Näytetään yksittäisen anturin kaikki tiedot (näytetään tunniste, lohko, tila ja mitta-arvot
ajanhetkille)
  - Oletuksena näytetään vain 10 uusinta mittatulosta
  - Näkymässä voidaan valita myös näyttämään mitta-arvo tiettyjen ajankohtien välille
- Näytetään yksittäisen anturin kaikki tilamuutokset ajankohtineen
- Voi hakea anturit niiden nykyisen tilan mukaan (näytetään tunniste, lohko ja tila)
- Näytetään graafi virhetilantenteiden esiintymisajankohdista

## Anturit

- Uniikki tunniste
- Lämpötila-arvo (C) yhden desimaalin tarkkuudella
- Mittauksen aikaleima
- Tila (toimii / yleinen virhe)
- Virhetilanteessa ihmisen pitää manuaalisesti säätää se normaaliin toimintatilaan
- Virhetilanteessa ei lähetä lämpötiladataa
- Ei tiedä mihin lohkoon kuuluu

## Lohkot

- Sisältää vähintään yhden (1) anturin
- Antureilla tunniste, tila sekä viimeisin mitta-arvo ja sen
aikaleima