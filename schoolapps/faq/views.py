from django.shortcuts import render

# Create your views here.

def create_info(text):
    return '<div class="alert success"> <p> <i class="material-icons left">info</i>' + text + '</p> </div>'


def faq(request):
    """ Shows the FAQ site, also if not logged in"""
    context = {
        'questions':
            [
                {'question': "Was ist Schoolapps?", 'answer': "Schoolapps sind eine Reihe von selbst entwickelten Anwendungen, die den Alltag von Schülern erleichtern sollen. <br />"+
                                                             "Hier könnt ihr euren Stundenplan angucken, welcher sich auch dynamisch ändert. Zudem lädt die Vorwerker Diakonie hier ihren wöchentlichen Speiseplan hoch. "+
                                                             "Schoolapps wird von der <a href='https://katharineum-zu-luebeck.de/aktivitaeten/arbeitsgemeinschaften/computer-ag/'>Computer-AG</a> entwickelt.", 'icon':"widgets"},

                {'question': "Ab wann kann ich Schoolapps nutzen?", 'answer': "Zurzeit läuft Schoolapps im Beta-Betrieb. Das heißt, nur einige Peronen -verschiedene Schüller*innen und Lehrer*innen- " +
                                                                               "testen es zurzeit. Diese Probephase endet spätestens am Ende des Schuljahres 18/19.", 'icon': "access_time"},

                {'question': "Ich kann mich nicht anmelden?", 'answer': create_info("Dieser Abschnitt ist zurzeit nur für Testnutzer relevant") + "<ol>"
                                                                        "   <li>Stelle sicher, dass du deinen Benutzernamen und dein Passwort richtig eingegeben hast.</li>"
                                                                        "   <li>Überprüfe, ob du dich auf dem Forum, und bei Gosa anmelden kannst. Wenn nicht, wende dich an deinen Medienscout.</li>"
                                                                        "   <li>Beachte, dass du mit dem Internet verbunden sein musst, und keine gecashte Version der Seite nutzen kannst.</li>"
                                                                        "   <li>Kontaktiere den Support über <a href='mailto:support@katharineum.de'>support@katharineum.de</a>"
                                                                        "</ol>",'icon': "screen_lock_portrait"},

                {'question': "Gibt es eine Smartphone-APP für SchoolApps?", 'answer': 'Ein Smartphone-APP haben wir zwar nicht, jedoch etwas einliches, eine sogenannte <abbr title="Progressive'
                                                                                      ' Web App">PWA</abbr>. <br />Um diese auf deinem Smartphone zu aktivieren, musst du SchoolApps lediglich in'
                                                                                      'einem Webbrowser öffnen, dort dann oben rechts auf das Kontextmenü (die drei Punkte) gehen, und auf '
                                                                                      '<q>Zu Startbildschirm hinzufügen</q> drücken. Solltest du Hilfe benötigen, folgen hier die Anleitungen'
                                                                                      'für die drei verbreitetesten Browser.'
                                                                                      '<div class="row">'
                                                                                      '<a class="btn-large col s4 orange">Firefox</a>'
                                                                                      '<a class="btn-large col s4 red">Chrome</a>'
                                                                                      '<a class="btn-large col s4 blue">Safari</a>'
                                                                                      '</div>',
                                                                            'icon': "phonelink"},
            ]
    }
    return render(request, 'faq/faq.html', context)