from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import REBUSForm
from .forms import FeedbackForm


# Create your views here.
def rebus(request):
    if request.method == 'POST':
        form = REBUSForm(request.POST)
        if form.is_valid():
            # process data
            return HttpResponseRedirect('/rebus_submitted/')
    else:
        form = REBUSForm()

    return render(request, 'support/rebus.html', {'form': form})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # process data
            return HttpResponseRedirect('/feedback_submitted/')
    else:
        form = FeedbackForm()

    return render(request, 'support/feedback.html', {'form': form})
