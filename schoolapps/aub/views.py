from django.shortcuts import render
from django.http import HttpResponse

from .models import Aub

def index(request):
    aubs = Aub.objects.all()[:10]

    context = {
        'aubs': aubs  
    }
    return render(request, 'index.html', context)

def details(request, todo_id):
    todo = Aub.objects.get(id=todo_id)
    context = {
        'aub': aub
    }
    return render(request, 'details.html', context)