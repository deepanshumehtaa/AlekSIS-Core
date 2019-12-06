# Releases/Änderungen
## 1.0-beta "Aebli"
_Veröffentlicht_

## 1.0 "Aebli"
Veröffentlicht unter [v1.0](https://github.com/Katharineum/school-apps/releases/tag/v1.0)

### Funktionen
- AUB (Antrag auf Unterrichtsbefreiung)
  - Antragstellung mit anschließender Bearbeitungs- und Löschfunktion
  - Genehmigen bzw. Ablehnen von Anträgen in zwei Runden
  - Archivfunktion für alte Anträge
  - Automatische Benachrichtigung bei Genehmigung bzw. Ablehnung per E-Mail an den Antragssteller
- Timetable (Stundenplan, basierend auf UNTIS 2020)
  - Anzeige aller Studenpläne (Schüler, Lehrer, Räume) inkl. Mobilversion
  - Anzeige des Vertretungsplans über Tabelle (Webapp) oder PDF
  - Direkte Einbindung von Vertretungen in die Regelpläne ("SMART PLAN")
  - Bereitstellung eines Tagesplanes für jeden Nutzer ("Mein Plan", SMART PLAN für einen Wochentag)
- Speisepläne
  - Hochladen von Speiseplänen im PDF-Format für jeweils eine Kalenderwoche
  - Bereitstellung einer PDF-URL, welche dynamisch den aktuellen Plan anzeigt
- Support
  - REBUS: Fehlermeldeportal mit dreistufiger Kategoriesierungsmöglichkeit
  - Feedback: Feedbackformular mit Sternewertung
  - FAQ: Datenbankgestütztet FAQ-Anzeige inkl. Fragemöglichkeit
  - Benachrichtigungen für REBUS, Feedback und FAQ via E-Mail

## 1.0.1 "Aebli"
Veröffentlicht unter [v1.0](https://github.com/Katharineum/school-apps/releases/tag/v1.0.1)

### Änderungen
Diverse Nachbesserungen des Releases 1.0 "Aebli"
* Umgestaltung des Menüs
* Umgestaltung des Footers
* Nächsten Tag im Vertretungsplan und Mein Plan bereits ab 15:35 Uhr des Vortages anzeigen
* Verbesserungen bei REBUS
* Anpassung für OTRS
* Kleine Designänderungen (Timetable, AUB, FAQ)
* Beheben von kleinen Bugs (Timetable, Speiseplan)

## 1.0.2 "Aebli"
### Änderungen
Weitere Nachbesserungen der Releases 1.0 sowie 1.0.1 "Aebli"
* Ferien/Feiertage werden nun angezeigt
* Icon für Nimbus im Footer hinzugefügt
* Vertretungsplantabelle mobil optimiert
* Sortierung der AUBs geändert
* Darstellung der REBUS-E-Mails verbessert
* Weitere Kategorien für "Fehler melden" hinzugefügt (Drucker, etc.)
* Designanpassungen im Vertretungsplan-PDF (u. a. Minimierung des Platzbedarfes)
* Entfernung des Hinweises "erste Version"
* SMART PLAN wird ab Freitag, 15:35 Uhr bereits für die nächste Woche angezeigt
* Umbenennung von class.pdf in aktuell.pdf
* Interne Optimierungen und Verbesserungen sowie Fehlerbehebungen

## 1.1 "Aebli"
### Änderungen
Weitere Verbesserungen der vorangegeangen Versionen dieses Releases.
* Einführung eines neuen Dashboards auf JS-Basis
  + dynamische Aktualisierung
  + SMART PLAN
  + Aktuelle Termine
  + Aktueller Artikel von der Homepage
  + Benachrichtigungen/Hinweise
* Verbesserung der PWA
* Verbesserung der Geschwindigkeit
* Überarbeitung des PDF-Vertretungsplans
  + Ausblenden der Stunden, die durch Veranstaltungen entfallen
  + Ausblenden der Änderungen an Verfügungsstunden
  + Ausblenden von nicht betroffenen Parallelkursen bei Vertretungen
  + Zusammenfassen von Stundenblöcken (statt zwei Einzelstunden wird eine Doppelstunde angezeigt)
  + Zusammenfassen der Seiten für mehrere Tage, sodass der zweite Tag bereits auf der Seite anfängt, auf der der erste Tag endet
* Behebung kleinerer Fehler
  + Support-Seiten waren auch ohne Anmeldung nutzbar
  + Pläne sind auf der Übersichtsseite sortiert
