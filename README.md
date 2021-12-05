# Ajanseurantasovellus
Sovelluksen avulla käyttäjä voi seurata eri aktiviteetteihin käyttämäänsä aikaa.
## Ominaisuudet
Sovellusta voi testata [Herokussa](https://tsoha-ajanseuranta.herokuapp.com/).

**Sovellus tarjoaa seuraavat toiminnallisuudet:**
* Käyttäjä voi luoda tunnuksen sekä kirjautua sisään ja ulos
* Käyttäjä voi luoda useita seurattavia aktiviteetteja (activities)
  * Aktiviteetille tulee antaa tässä vaiheessa ainoastaan nimi
* Käyttäjä voi lisätä valitsemalleen aktiviteetille useita suorituksia (entries)
  * Suoritukselle annetaan aloitus- ja päättymisaika
  * Aktiviteetin kokonaisaika päivittyy lisätyn suorituksen perusteella
* Käyttäjä voi tarkastella aktiviteetille lisättyjä suorituksia
* Käyttäjä voi poistaa lisäämiään suorituksia

**Sovellukseen suunniteltuja toiminnallisuuksia:**
* Käyttäjä voi luoda useita seurattavia kategorioita (categories)
  * Jokainen aktiviteetti voi liittyä vain yhteen kategoriaan
* Käyttäjä voi poistaa ja muokata kategorioita ja aktiviteetteja
* Käyttäjä voi muokata suorituksia
* Käyttäjä voi tarkastella ajankäytöstään koostettuja yhteenvetoja
* Käyttäjä voi seurata sekä kategoriaan että siihen liittyviin aktiviteetteihin käyttämäänsä aikaa valitsemillaan ajanjaksoilla (päivä, viikko, kuukausi)
  * Käyttäjä voisi esimerkiksi nähdä, kuinka kauan aikaa viime viikolla on mennyt opiskeluun (kategoria) ja kuinka kauan siitä kului tsoha-kurssiin tai matematiikkaan (aktiviteetit)
* Käyttäjä voi aloittaa ja lopettaa aktiviteetin reaaliaikaisen seurannan
  * Kun käyttäjä lopettaa seurannan, ko. aktiviteetille lisätään suoritus, johon tallettuu aloitus- ja lopetusaika
