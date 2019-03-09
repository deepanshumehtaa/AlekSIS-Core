from django.shortcuts import render

from mailer import send_mail_with_template
from support.models import kanboard_settings
from untisconnect.api import get_all_rooms
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
            # Read out form data
            contraction = request.user.username
            a = form.cleaned_data['a']
            b = form.cleaned_data["b"]
            c = form.cleaned_data["c"]
            short_description = form.cleaned_data['short_description']
            long_description = form.cleaned_data['long_description']

            # Build description for kanboard
            description = "**Kategorie:** {} → {} → {} \n\n **Übermittelt von:** {} \n\n **Nachricht:** {}".format(a, b,
                                                                                                                   c,
                                                                                                                   contraction,
                                                                                                                   long_description)
            # Add kanboard task
            kb.create_task(project_id=p_id_rebus, title=short_description, description=description)

            # Register activity
            desc_act = "{} → {} → {} | {}".format(a, b, c, short_description)
            act = Activity(title="Du hast uns ein Problem gemeldet.", description=desc_act, app="REBUS",
                           user=request.user)
            act.save()

            # Send mail
            context = {
                "a": a,
                "b": b,
                "c": c,
                "short_desc": short_description,
                "long_desc": long_description,
                "user": request.user.username
            }
            send_mail_with_template("Neue REBUS-Meldung", ["support@katharineum.de"], "support/mail/rebus.txt",
                                    "support/mail/rebus.html", context)

            return render(request, 'support/rebus_submitted.html')
    else:
        form = REBUSForm()

    rooms = [room.name for room in get_all_rooms()]

    return render(request, 'support/rebus.html', {'form': form, "props": {"rooms": rooms}})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Read out form data
            design_rating = form.cleaned_data['design_rating']
            performance_rating = form.cleaned_data['performance_rating']
            usability_rating = form.cleaned_data['usability_rating']
            overall_rating = form.cleaned_data['overall_rating']
            more = form.cleaned_data['more']
            ideas = form.cleaned_data['ideas']
            apps = form.cleaned_data["apps"]

            # Build description for kanboard
            description = """
             **Bewertungen:** {}/5 (Design), {}/5 (Geschwindigkeit), {}/5 (Benutzerfreundlichkeit)
    
             **Bewertung (insgesamt):** {}/5
    
             **Pro/Contra:** {}
    
             **Ideen/Wünsche:** {}
    
             **Sonstiges:** {}
             """.format(design_rating, performance_rating, usability_rating, overall_rating, apps, ideas, more)

            # Get color for kanboard by rating
            if int(overall_rating) < 2:
                color = "red"
            elif 2 < int(overall_rating) <= 3:
                color = "yellow"
            else:
                color = "green"

            # Add kanboard task
            kb.create_task(project_id=p_id_feedback,
                           title="Feedback von {}".format(request.user.username),
                           description=description,
                           color_id=color)

            # Register activity
            act = Activity(title="Du hast uns Feedback gegeben.",
                           description="Du hast SchoolApps mit {} von 5 Sternen bewertet.".format(
                               overall_rating), app="Feedback",
                           user=request.user)
            act.save()

            # Send mail
            context = {
                "design": design_rating,
                "performance": performance_rating,
                "usability": usability_rating,
                "overall": overall_rating,
                "more": more,
                "apps": apps,
                "ideas": ideas,
                "user": request.user.username
            }
            send_mail_with_template("Neues Feedback von {}".format(request.user.username), ["support@katharineum.de"],
                                    "support/mail/feedback.txt",
                                    "support/mail/feedback.html", context)
            print(context)

            return render(request, 'support/feedback_submitted.html')
    else:
        form = FeedbackForm()

    return render(request, 'support/feedback.html', {'form': form})
