from django.shortcuts import render

from mailer import send_mail_with_template
from support.models import kanboard_settings
from .forms import REBUSForm
from .forms import FeedbackForm
from kanboard import Kanboard
from dashboard.models import Activity

print("HI")
api_token = kanboard_settings.api_token
p_id_rebus = kanboard_settings.kb_project_id_rebus
p_id_feedback = kanboard_settings.kb_project_id_feedback
kb = Kanboard('https://kanboard.katharineum.de/jsonrpc.php', 'jsonrpc',
              api_token)


# Create your views here.
def rebus(request):
    if request.method == 'POST':
        form = REBUSForm(request.POST)
        if form.is_valid():
            # room = form.cleaned_data['room']
            contraction = request.user.username
            a = form.cleaned_data['a']
            b = form.cleaned_data["b"]
            c = form.cleaned_data["c"]
            short_description = form.cleaned_data['short_description']
            long_description = form.cleaned_data['long_description']
            description = "**Kategorie:** {} > {} > {} \n\n **Übermittelt von:** {} \n\n **Nachricht:** {}".format(a, b,
                                                                                                                   c,
                                                                                                                   contraction,
                                                                                                                   long_description)
            # description = "**Kategorie: **" + a + "\n\n" + "**Raum: **\n\n**Übermittelt von: **" + contraction + "\n\n" + "**Nachricht: **" + long_description + "\n\n"
            # Add kanboard task
            kb.create_task(project_id=p_id_rebus, title=short_description, description=description)

            # Register activity
            desc_act = "{} > {} > {} | {} | {}".format(a, b, c, short_description, long_description)
            act = Activity(title="Du hast uns ein Problem gemeldet.", description=desc_act, app="REBUS",
                           user=request.user)
            act.save()
            context = {
                "a": a,
                "b": b,
                "c": c,
                "short_desc": short_description,
                "long_desc": long_description,
                "user": request.user.username
            }
            send_mail_with_template("Neue REBUS-Meldung", ["support@katharineum.de"], "support/mail/email.txt",
                                    "support/mail/email.html", context)

            return render(request, 'support/rebus_submitted.html')
    else:
        form = REBUSForm()

    return render(request, 'support/rebus.html', {'form': form})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            design_rating = form.cleaned_data['design_rating']
            functions_rating = form.cleaned_data['functions_rating']
            performance_rating = form.cleaned_data['performance_rating']
            compatibility_rating = form.cleaned_data['compatibility_rating']
            usability_rating = form.cleaned_data['usability_rating']
            overall_rating = form.cleaned_data['overall_rating']
            short_description = form.cleaned_data['short_description']
            long_description = form.cleaned_data['long_description']
            ideas = form.cleaned_data['ideas']
            description = "**Bewertung fürs Design: **" + design_rating + "\n\n" + "**Bewertung für die Funktionen: **" + functions_rating + "\n\n" + "**Bewertung für die Performance: **" + performance_rating + "\n\n" + "**Bewertung für die Kompatibilität: **" + compatibility_rating + "\n\n" + "**Bewertung für die Benutzerfreundlichkeit: **" + usability_rating + "\n\n" + "**GESAMTBEWERTUNG: **" + overall_rating + "\n\n" + "**Nachricht: **" + long_description + "\n\n" + "**IDEEN: **" + ideas + "\n\n"

            if int(overall_rating) <= 3:
                kb.create_task(project_id=p_id_feedback, title=short_description, description=description,
                               color_id='red')
            elif 3 < int(overall_rating) <= 7:
                kb.create_task(project_id=p_id_feedback, title=short_description, description=description,
                               color_id='yellow')
            else:
                kb.create_task(project_id=p_id_feedback, title=short_description, description=description,
                               color_id='green')

            return render(request, 'support/feedback_submitted.html')
    else:
        form = FeedbackForm()

    return render(request, 'support/feedback.html', {'form': form})
