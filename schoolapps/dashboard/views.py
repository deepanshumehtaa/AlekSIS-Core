from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Activity, register_notification
# from .apps import DashboardConfig
from mailer import send_mail_with_template
from userinformation import UserInformation

def create_info(text):
    return '<div class="alert success"> <p> <i class="material-icons left">info</i>' + text + '</p> </div>'

# Create your views here.

@login_required
def index(request):
    """ Index page: Lists activities und notifications """
    # Register visit
    # act = Activity(title="Dashboard aufgerufen", description="Sie haben das Dashboard aufgerufen.",
    #                app=DashboardConfig.verbose_name, user=request.user)
    # act.save()
    print(request.user)
    # UserInformation.user_classes(request.user)
    print(UserInformation.user_courses(request.user))

    # Load activities
    activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Load notifications
    notifications = request.user.notifications.all().filter(user=request.user).order_by('-created_at')

    # user_type = UserInformation.user_type(request.user)
    context = {
        'activities': activities,
        'notifications': notifications,
        'user_type': UserInformation.user_type(request.user),
        'user_type_formatted': UserInformation.user_type_formatted(request.user),
        'classes': UserInformation.user_classes(request.user),
        'courses': UserInformation.user_courses(request.user),
        'subjects': UserInformation.user_subjects(request.user),
        'has_wifi': UserInformation.user_has_wifi(request.user)
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def test_notification(request):
    """ Sends a test mail """
    # send_mail_with_template("Test", [request.user.email], 'mail/email.txt', 'mail/email.html', {'user': request.user})
    register_notification(user=request.user, title="Ihr Antrag wurde genehmigt",
                          description="Ihr Antrag XY wurde von der Schulleitung genehmigt.", app="AUB",
                          link=reverse("aub_details", args=[1]))
    print(reverse("aub_details", args=[1]))
    return redirect(reverse('dashboard'))


def error_404(request, exception):
    return render(request, 'common/404.html')

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

                {'question': "Test-Frage?", 'answer': '<span class="red-text">Gut!</span>'},
            ]
    }
    return render(request, 'dashboard/faq.html', context)