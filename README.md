# Ajanseurantasovellus
Sovelluksen avulla käyttäjä voi seurata eri aktiviteetteihin käyttämäänsä aikaa.
## Ominaisuudet
Sovelluksen perusversioon on odotettavissa seuraavat toiminnallisuudet:
* Käyttäjä voi luoda oman käyttäjätilin sekä kirjautua sisään ja ulos
* Kirjauduttuaan sisään käyttäjä voi luoda useita seurattavia *kategorioita/luokkia* (esim. opiskelu, vapaa-aika), mutta tämä ei ole pakollista
* Käyttäjä voi luoda useita *aktiviteetteja* (esim. tsoha-kurssi), joihin käytettyä aikaa haluaa seurata
  * Jokainen aktiviteetti voi liittyä vain yhteen kategoriaan
* Käyttäjä voi aloittaa ja lopettaa aktiviteetin seurannan
  * Kun käyttäjä lopettaa seurannan, ko. aktiviteetille lisätään *suoritus*, johon tallettuu aloitus- ja lopetusaika
  * Yhteen aktiviteettiin voi liittyä useita suorituksia, joista kaikki lisäävät aktiviteettiin käytettyä kokonaisaikaa
  * Suorituksia voi lisätä myös manuaalisesti, ts. ilman reaaliaikaista seurantaa
* Käyttäjä voi poistaa ja muokata kategorioita, aktiviteetteja ja niihin liittyviä suorituksia
* Käyttäjä voi tarkastella ajankäytöstään koostettuja yhteenvetoja
* Käyttäjä voi seurata sekä kategoriaan että siihen liittyviin aktiviteetteihin käyttämäänsä aikaa valitsemillaan ajanjaksoilla (päivä, viikko, kuukausi)
  * Käyttäjä voisi esimerkiksi nähdä, kuinka kauan aikaa viime viikolla on mennyt opiskeluun (kategoria) ja kuinka kauan siitä kului tsoha-kurssiin tai matematiikkaan (aktiviteetit)
