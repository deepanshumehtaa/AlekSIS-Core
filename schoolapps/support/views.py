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
            contraction = form.cleaned_data['contraction']
            category = form.cleaned_data['category']
            short_description = form.cleaned_data['short_description']
            ld = form.cleaned_data['long_description']
            long_description = "Kategorie: " + category + "\nRaum: " + room + "\nÜbermittelt von: " + contraction + "\nLange Beschreibung: " + ld

            #kb = Kanboard('https://kanboard.katharineum.de/jsonrpc.php', 'yuha', 'token')
            #kb.create_task(project_id=4, title=short_description, description=long_description)

            # process data
            return render(request, 'support/rebus_submitted.html')
    else:
        form = REBUSForm()

    return render(request, 'support/rebus.html', {'form': form})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # process data
            return render(request, 'support/feedback_submitted.html')
    else:
        form = FeedbackForm()

    return render(request, 'support/feedback.html', {'form': form})

