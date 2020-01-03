# Dashboard
Das Dashboard dient dazu, den Benutzer zu begrüßen (> Startseite)
und seine letzten Aktivitäten anzuzeigen.

Edit: Außerdem zeigt das Dashboard aktuelle Nachrichten für den Benutzer an.

## Aktivitäten
Als Aktivität gilt alles, was der Nutzer selbst macht, d.h., bewusst.

### Eine Aktivität registrieren
1. Importieren

        from .apps import <Meine App>Config
        from dashboard.models import Activity

2. Registrieren

        act = Activity(title="<Titel der Aktion>", description="<Beschreibung der Aktion>", app=<Meine App>Config.verbose_name, user=<Benutzer Objekt>)
        act.save()

## Benachrichtigungen
Als Benachrichtigung gilt eine Aktion, die den Nutzer betrifft.

### Eine Benachrichtigung verschicken
1. Importieren

        from .apps import <Meine App>Config
        from dashboard.models import Notification

2. Verschicken

          register_notification(title="<Titel der Nachricht>",
                                      description="<Weitere Informationen>",
                                      app=<Meine App>Config.verbose_name, user=<Benutzer Objekt>,
                                      link=request.build_absolute_uri(<Link für weitere Informationen>))

    **Hinweis:** Der angegebene Link muss eine absolute URL sein.
    Dies wird durch übergabe eines dynamischen Linkes (z. B. /aub/1) an die Methode `request.build_absolute_uri()` erreicht.

    Um einen dynamischen Link durch den Namen einer Django-URL zu "errechnen", dient die Methode `reverse()`.

    Literatur:
    - [1] https://docs.djangoproject.com/en/2.1/ref/request-response/#django.http.HttpRequest.build_absolute_uri
    - [2] https://docs.djangoproject.com/en/2.1/ref/urlresolvers/#reverse

## Caches
### Sitecache
Ein Seitencache basiert auf dem Django-Decorator `@cache_page`  und cacht die HTML-Ausgabe des entsprechenden Views.

### Variablencache
Ein Variablencache nutzt die Low-Level-Cache-API von Django und speichert den Inhalt einer Variable.

### Verwaltung
Jedes gecachte Objekt (ob Sitecache oder Variablencache) benötigt ein Cache-Objekt in der DB. Bei Cacheinhalten für die nur eine Variable gespeichert werden muss oder ein View, wird die Datei `caches.py` verwendet, wo der Cache als Konstante gespeichert ist:
```
<EXAMPLE_CACHE>, _ = Cache.objects.get_or_create(id="<example_cache>",
                                                 defaults={
                                                     "site_cache": <True/False>,
                                                     "name": "<Readable name>",
                                                     "expiration_time": <10>}) # in seconds

```
#### Variablencache
Für Variablencaches kann mit der Funktion `get()` eines Cache-Objektes der aktuelle Inhalt des Caches abgefragt werden.
Bei abgelaufenen Caches wird `False` zurückgeben, dann ist der Wert neu zu berechnen und mit `update(<new_value>)` zu aktualisieren, wobei die Aktualisierungszeit automatisch zurückgesetzt wird.

#### Sitecache
Für einen Sitecache kann folgender Decorator zum entsprechenden View hinzugefügt werden:
```
@cache_page(<EXAMPLE_CACHE>.expiration_time)
```

### Literatur
- https://docs.djangoproject.com/en/2.2/topics/cache/
