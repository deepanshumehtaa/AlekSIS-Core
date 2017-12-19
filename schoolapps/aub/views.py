from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Aub


@login_required
def index(request):
    aubs = Aub.objects.all()[:10]

    context = {
        'aubs': aubs
    }
    return render(request, 'index.html', context)


@login_required
def details(request, todo_id):
    todo = Aub.objects.get(id=todo_id)
    context = {
        'aub': aub
    }
    return render(request, 'details.html', context)
