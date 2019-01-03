from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import REBUSForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = REBUSForm(request.POST)
        if form.is_valid():
            # process data
            return HttpResponseRedirect('support/rebus_submitted/')
    else:
        form = REBUSForm()

    return render(request, 'support/rebus.html', {'form': form})
