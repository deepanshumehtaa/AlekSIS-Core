from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.http import Http404
from django.shortcuts import redirect, render
from django_tables2 import RequestConfig
from django.urls import reverse
from .models import Person
from .tables import PersonsTable

def index(request):
    context = {}
    return render(request, 'core/index.html', context)

@login_required
def persons(request):
    context = {}

    # Get all persons
    persons = Person.objects.all()

    # Build table
    persons_table = PersonsTable(persons)
    RequestConfig(request).configure(persons_table)
    context['persons_table'] = persons_table

    return render(request, 'core/persons.html', context)

@login_required
def person(request, id_):
    context = {}

    # Get person and check access
    try:
        person = Person.objects.get(pk=id_)
    except Person.DoesNotExist as e:
        # Turn not-found object into a 404 error
        raise Http404 from e

    context['person'] = person

    return render(request, 'core/person.html', context)
