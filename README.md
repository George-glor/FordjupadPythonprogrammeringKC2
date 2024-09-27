
# Weather Data Automation Project

## Projektbeskrivning
Detta projekt syftar till att automatisera insamling, bearbetning och lagring av väderdata från Open-Meteo API till en SQL-databas. Projektet består av tre huvudsakliga delar:

1. **`Weather.py`:** Huvudskriptet för att hämta väderdata från API:et, bearbeta datan och infoga den i en SQL-databas.
2. **`WeatherViewerApp.py`:** Ett grafiskt användargränssnitt (GUI) för att visa, filtrera och exportera data från databasen.
3. **`test_weather.py`:** Ett testskript för att verifiera huvudskriptets funktionalitet och säkerställa att allt fungerar som förväntat.

Alla dessa komponenter kan schemaläggas och köras automatiskt med hjälp av Windows Task Scheduler.

## Funktioner
- **Automatiserad datainsamling:** Hämta historiska väderdata för en specifik plats och tidsperiod.
- **Databearbetning:** Bearbetning och formatering av data, inklusive hantering av saknade värden och omvandling av temperaturer.
- **Databaslagring:** Infogning av bearbetad data i en SQL-databas.
- **Grafiskt användargränssnitt (GUI):** Visa, filtrera och exportera data med en användarvänlig GUI-applikation.
- **Automatiska tester:** Verifiering av skriptets funktionalitet med enhetstester.

## Krav
- Python 3.7 eller senare
- Installerade Python-paket:
  - `requests`
  - `pandas`
  - `sqlalchemy`
  - `pyodbc`
  - `tkinter`
  - `unittest`

## Installation
1. **Klona projektet från GitHub:**
   ```bash
   git clone <URL-till-ditt-repo>
   cd <project-directory>
   ```

2. **Skapa en virtuell miljö och installera beroenden:**
   ```bash
   python -m venv myenv
   myenv\Scripts\activate  # För Windows
   source myenv/bin/activate  # För macOS/Linux
   pip install -r requirements.txt
   ```

3. **Ställ in SQL-databasen:**
   - Se till att du har en SQL-databas konfigurerad enligt anslutningssträngen i `Weather.py`.
   - Skapa tabellen `weather_forecast` med rätt kolumner om den inte redan finns.

## Användning

### 1. Kör huvudskriptet
Hämta, bearbeta och infoga väderdata i databasen:
```bash
python Weather.py
```

### 2. Starta GUI-applikationen
Använd GUI:t för att visa, filtrera och exportera data:
```bash
python WeatherViewerApp.py
```

### 3. Kör automatiska tester
Verifiera att huvudskriptet fungerar som förväntat:
```bash
python test_weather.py
```

## Schemaläggning av Skriptet
För att köra skriptet automatiskt vid en specifik tidpunkt, använd Windows Task Scheduler:
1. Öppna Task Scheduler och skapa en ny grundläggande uppgift.
2. Välj när du vill att skriptet ska köras.
3. Välj "Starta ett program" och ange sökvägen till Python-exekverbara filen och skriptet `Weather.py`.
4. Spara och aktivera uppgiften.

## Filstruktur
- `Weather.py`: Huvudskriptet för att hämta och infoga väderdata i SQL-databasen.
- `WeatherViewerApp.py`: GUI-applikationen för att visa och interagera med väderdata.
- `test_weather.py`: Testskriptet som verifierar huvudskriptets funktionalitet.
- `README.md`: Dokumentation och instruktioner för projektet.
- `requirements.txt`: Lista över beroenden för att köra projektet.

## Självutvärdering
### Utmaningar
- Hantering av API-fel och anslutningsproblem.
- Databearbetning och validering för att säkerställa korrekt infogning i databasen.
- Implementering av ett användarvänligt GUI.

### Betygsbedömning
Jag anser att projektet uppfyller kraven för betyget **Väl Godkänd** eftersom jag har implementerat automatisering, felhantering, testning och ett grafiskt användargränssnitt med tillhörande dokumentation.

## Kontakt
För frågor eller feedback, vänligen kontakta:
- **Namn:** George Glor
- **E-post:** georgeglor40@hotmail.com
- **GitHub:** [George-glor](https://github.com/George-glor)


