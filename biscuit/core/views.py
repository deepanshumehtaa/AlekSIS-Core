from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Person
from .tables import PersonsTable

def index(request):
    context = {}
    return render(request, 'core/index.html', context)

@login_required
def persons(request):
    context = {}

    # Get all upcoming persons
    persons = Person.objects.all()

    # Build table
    persons_table = PersonsTable(persons)
    RequestConfig(request).configure(persons_table)
    context['persons_table'] = persons_table

    return render(request, 'core/persons.html', context)
