# Ajanseurantasovellus
Sovelluksen avulla käyttäjä voi seurata eri aktiviteetteihin käyttämäänsä aikaa.
## Ominaisuudet
Huom: Tällä hetkellä sovellus on suoritettavissa vain paikallisesti Flaskilla.

**Sovellus tarjoaa seuraavat toiminnallisuudet:**
* Etusivulla näkyvät seurattavat aktiviteetit listattuina, ja jokaisen aktiviteetin yhteydessä näkyy siihen käytetty kokonaisaika
* Sovelluksessa voi luoda aktiviteetin klikkaamalla etusivulla 'Lisää aktiviteetti'
  * Aktiviteetille tulee antaa tässä vaiheessa ainoastaan nimi
  * Lisätty aktiviteetti lisätään onnistuneesti tietokantaan
* Aktiviteetille voi lisätä suorituksia (entries) klikkaamalla kyseisen aktiviteetin alta 'Lisää suoritus'
  * Suoritukselle annetaan aloitus- ja päättymisaika
  * Aktiviteetin kokonaisaika päivittyy annettujen aikojen perusteella

**Sovellukseen suunnitellut toiminnallisuudet, jotka vielä puuttuvat:**
* Sovellus on julkaistu ja käytettävissä Herokussa
* Käyttäjä voi luoda oman käyttäjätilin sekä kirjautua sisään ja ulos
* Kirjauduttuaan sisään käyttäjä voi luoda useita seurattavia *kategorioita* (esim. opiskelu, vapaa-aika), mutta tämä ei ole pakollista
  * Jokainen aktiviteetti voi liittyä vain yhteen kategoriaan
* Käyttäjä voi aloittaa ja lopettaa aktiviteetin seurannan
  * Kun käyttäjä lopettaa seurannan, ko. aktiviteetille lisätään *suoritus*, johon tallettuu aloitus- ja lopetusaika
* Käyttäjä voi poistaa ja muokata kategorioita, aktiviteetteja ja niihin liittyviä suorituksia
* Käyttäjä voi tarkastella ajankäytöstään koostettuja yhteenvetoja
* Käyttäjä voi seurata sekä kategoriaan että siihen liittyviin aktiviteetteihin käyttämäänsä aikaa valitsemillaan ajanjaksoilla (päivä, viikko, kuukausi)
  * Käyttäjä voisi esimerkiksi nähdä, kuinka kauan aikaa viime viikolla on mennyt opiskeluun (kategoria) ja kuinka kauan siitä kului tsoha-kurssiin tai matematiikkaan (aktiviteetit)
