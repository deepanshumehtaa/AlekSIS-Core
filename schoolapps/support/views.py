from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import REBUSForm
from .forms import FeedbackForm
from kanboard import Kanboard


# Create your views here.
def rebus(request):
    if request.method == 'POST':
        form = REBUSForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            contraction = request.user.username
            category = form.cleaned_data['category']
            short_description = form.cleaned_data['short_description']
            long_description = form.cleaned_data['long_description']
            description = "**Kategorie: **" + category + "\n\n" + "**Raum: **" + room + "\n\n" + "**Übermittelt von: **" + contraction + "\n\n" + "**Nachricht: **" + long_description + "\n\n"

            kb = Kanboard('https://kanboard.katharineum.de/jsonrpc.php', 'jsonrpc', 'f984754c9e87ab43e98ed2f94d2080b6f8e5c499aca95e1fb98c4fc3c7ea')
            kb.create_task(project_id=4, title=short_description, description=description)

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

            kb = Kanboard('https://kanboard.katharineum.de/jsonrpc.php', 'jsonrpc', 'f984754c9e87ab43e98ed2f94d2080b6f8e5c499aca95e1fb98c4fc3c7ea')
            if int(overall_rating) <= 3:
                kb.create_task(project_id=18, title=short_description, description=description, color_id='red')
            elif 3 < int(overall_rating) <= 7:
                kb.create_task(project_id=18, title=short_description, description=description, color_id='yellow')
            else:
                kb.create_task(project_id=18, title=short_description, description=description, color_id='green')

            return render(request, 'support/feedback_submitted.html')
    else:
        form = FeedbackForm()

    return render(request, 'support/feedback.html', {'form': form})

