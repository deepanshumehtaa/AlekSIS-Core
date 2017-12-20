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

    a. Stellvertreter prüft Antrag und i. bewilligt oder ii. formuliert Bedenken und lehnt ab
    
         i. Stellvertreter trägt Absenz in den Vertretungsplan ein. Lehrer erhält positive Rückmeldung.  
       
         ii. Antrag geht an den Schulleiter zurück, der endgültig aa. bewilligt oder b. ablehnt.

    b. Lehrer erhält Ablehnung mit Begründung

