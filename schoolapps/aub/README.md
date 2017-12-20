# school-apps: AUB (Antrag auf Unterrichtbefreiung)
## Stichworte
### Workflow

1.  Lehrer füllt Formular aus
    - Beginn Datum (DateField)
    - Beginn Stunde oder Uhrzeit (Int 1..9 / Time)
    - Ende Datum (DateField)
    - Ende Stunde oder Uhrzeit (Int 1..9 / Time)
    - Beschreibung (TextField)
    - Antragsteller (Lehrerkürzel) wird automatisch aus angemeldetem Benutzer generiert


2.  Schulleiter erhält Antrag (Link per Mail) und a. bewilligt oder b. lehnt ab

    a. Stellvertreter prüft Antrag und aa. bewilligt oder bb. formuliert Bedenken und lehnt ab

       a. Stellvertreter trägt Absenz in den Vertretungsplan ein. Lehrer erhält positive Rückmeldung.  

       b. Antrag geht an den Schulleiter zurück, der endgültig aa. bewilligt oder b. ablehnt.

    b. Lehrer erhält Ablehnung mit Begründung

