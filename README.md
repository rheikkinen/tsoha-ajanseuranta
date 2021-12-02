# Ajanseurantasovellus
Sovelluksen avulla käyttäjä voi seurata eri aktiviteetteihin käyttämäänsä aikaa.
## Ominaisuudet
Tällä hetkellä sovellus on valitettavasti vielä käyttökelvoton, ja se on suoritettavissa vain paikallisesti Flaskilla. 
Sovelluksessa seuraavat ominaisuudet kuitenkin toimivat:
* Sovellus käynnistyy & selaimessa etusivu tulee näkyviin
  * Etusivulla seurattavat aktiviteetit näkyvät listattuna, ja aktiviteetin yhteydessä näkyy siihen käytetty kokonaisaika
* Sovelluksessa voi luoda aktiviteetin klikkaamalla etusivulla 'Lisää aktiviteetti'
  * Aktiviteetille tulee antaa tässä vaiheessa ainoastaan nimi
  * Lisätty aktiviteetti lisätään onnistuneesti tietokantaan
* Sovelluksessa ei voi vielä lisätä aktiviteetetille suorituksia, ts. aktiviteetin kokonaisaika ei vielä voi lisääntyä

Etusivu:

![tsoha-etusivu](https://user-images.githubusercontent.com/32366546/142779395-737bf6fa-551f-4e4a-8a41-cd03f51a8285.png)

Aktiviteetin lisäys:

![tsoha-uusi-aktiviteetti](https://user-images.githubusercontent.com/32366546/142779516-460608cb-73f3-4b13-80a9-e4b5652a1985.png)

Sovellukseen suunnitellut toiminnallisuudet, jotka vielä puuttuvat:
* Sovellus on julkaistu ja käytettävissä Herokussa
* Käyttäjä voi luoda oman käyttäjätilin sekä kirjautua sisään ja ulos
* Kirjauduttuaan sisään käyttäjä voi luoda useita seurattavia *kategorioita* (esim. opiskelu, vapaa-aika), mutta tämä ei ole pakollista
  * Jokainen aktiviteetti voi liittyä vain yhteen kategoriaan
* Käyttäjä voi aloittaa ja lopettaa aktiviteetin seurannan
  * Kun käyttäjä lopettaa seurannan, ko. aktiviteetille lisätään *suoritus*, johon tallettuu aloitus- ja lopetusaika
  * Yhteen aktiviteettiin voi liittyä useita suorituksia, joista kaikki lisäävät aktiviteettiin käytettyä kokonaisaikaa
  * Suorituksia voi lisätä myös manuaalisesti, ts. ilman reaaliaikaista seurantaa
* Käyttäjä voi poistaa ja muokata kategorioita, aktiviteetteja ja niihin liittyviä suorituksia
* Käyttäjä voi tarkastella ajankäytöstään koostettuja yhteenvetoja
* Käyttäjä voi seurata sekä kategoriaan että siihen liittyviin aktiviteetteihin käyttämäänsä aikaa valitsemillaan ajanjaksoilla (päivä, viikko, kuukausi)
  * Käyttäjä voisi esimerkiksi nähdä, kuinka kauan aikaa viime viikolla on mennyt opiskeluun (kategoria) ja kuinka kauan siitä kului tsoha-kurssiin tai matematiikkaan (aktiviteetit)
