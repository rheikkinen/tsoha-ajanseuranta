# Ajanseurantasovellus
Sovelluksen avulla käyttäjä voi seurata eri aktiviteetteihin käyttämäänsä aikaa.
## Ominaisuudet
Sovellusta voi testata [Herokussa](https://tsoha-ajanseuranta.herokuapp.com/).

### Sovelluksen viimeisin versio tarjoaa seuraavat toiminnallisuudet
* Käyttäjä voi luoda tunnuksen sekä kirjautua sisään ja ulos
* Käyttäjä voi luoda useita kategorioita (categories)
* Käyttäjä voi luoda useita seurattavia aktiviteetteja (activities)
  * Aktiviteetille voi valita kategorian, jos sellainen on luotu
  * Aktiviteetin nimeä ja kategoriaa voi muuttaa myös jälkikäteen  
* Käyttäjä voi lisätä aktiviteetille useita suorituksia (entries)
  * Suoritukselle annetaan aloitus- ja päättymisaika
  * Aktiviteetin kokonaisaika päivittyy lisätyn suorituksen perusteella
* Käyttäjä voi tarkastella, muokata ja poistaa aktiviteetille lisättyjä suorituksia

### Ideoita sovelluksen jatkokehitykseen
Tässä on listattuna joitakin ominaisuuksia ja kehitysideoita, jotka sovellukseen oli suunniteltu mutta jotka jäivät kurssin ajan puitteissa toteuttamatta.
* Käyttäjä voi poistaa kategorioita ja aktiviteetteja
* Käyttäjä voi tarkastella ajankäytöstään koostettuja yhteenvetoja
* Käyttäjä voi seurata sekä kategoriaan että siihen liittyviin aktiviteetteihin käyttämäänsä aikaa valitsemillaan ajanjaksoilla (päivä, viikko, kuukausi)
  * Käyttäjä voisi esimerkiksi nähdä, kuinka kauan aikaa viime viikolla on mennyt opiskeluun (kategoria) ja kuinka kauan siitä kului tsoha-kurssiin tai matematiikkaan (aktiviteetit)
* Käyttäjä voi aloittaa ja lopettaa aktiviteetin reaaliaikaisen seurannan
  * Käyttäjän lopettaessa seurannan, ko. aktiviteetille lisätään suoritus, johon tallettuu aloitus- ja lopetusaika
* Aikojen mielekkäämpi esitystapa (tunteina ja minuutteina esim. 5h 48min) 
* Sovelluksen ulkoasun siistiminen
