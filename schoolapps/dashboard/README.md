# Dashboard 
Das Dashboard dient dazu, den Benutzer zu begrüßen (> Startseite) 
und seine letzten Aktivitäten anzuzeigen.

## Aktivität registrieren
1. Importieren

        from .apps import <Meine App>Config
        from dashboard.models import Activity

2. Registrieren
        
        act = Activity(title="<Titel der Aktion>", description="<Beschreibung der Aktion>", app=<Meine App>Config.verbose_name, user=<Benutzer Objekt>)
        act.save()