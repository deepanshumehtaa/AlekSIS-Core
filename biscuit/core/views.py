from typing import Callable

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django_tables2 import RequestConfig
from django.utils.translation import ugettext_lazy as _

from .decorators import admin_required
from .forms import PersonsAccountsFormSet, EditPersonForm, EditGroupForm
from .models import Person, Group
from .tables import PersonsTable, GroupsTable
from .util import messages


def index(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'core/index.html', context)


def error_handler(status: int) -> Callable[..., HttpResponse]:
    def real_handler(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {}

        context['status'] = status

        if status == 404:
            context['message'] = _('This page does not exist. If you were redirected by a link on an external page, it is possible that that link was outdated.')
            context['caption'] = _('Page not found')
        elif status == 500:
            context['caption'] = _('Internal server error')
            context['message'] = _('An unexpected error has occurred.')

        return render(request, 'error.html', context, status=status)

    return real_handler


@login_required
def persons(request: HttpRequest) -> HttpResponse:
    context = {}

    # Get all persons
    persons = Person.objects.all()

    # Build table
    persons_table = PersonsTable(persons)
    RequestConfig(request).configure(persons_table)
    context['persons_table'] = persons_table

    return render(request, 'core/persons.html', context)


@login_required
def person(request: HttpRequest, id_: int, template: str) -> HttpResponse:
    context = {}

    # Get person and check access
    try:
        person = Person.objects.get(pk=id_)
    except Person.DoesNotExist as e:
        # Turn not-found object into a 404 error
        raise Http404 from e

    context['person'] = person

    # Get groups where person is member of
    groups = Group.objects.filter(members=id_)

    # Build table
    groups_table = GroupsTable(groups)
    RequestConfig(request).configure(groups_table)
    context['groups_table'] = groups_table

    return render(request, 'core/person_%s.html' % template, context)


@login_required
def group(request: HttpRequest, id_: int, template: str) -> HttpResponse:
    context = {}

    # Get group and check if it exist
    try:
        group = Group.objects.get(pk=id_)
    except Group.DoesNotExist as e:
        # Turn not-found object into a 404 error
        raise Http404 from e

    context['group'] = group

    # Get group
    group = Group.objects.get(pk=id_)

    # Get members
    members = group.members.all()

    # Build table
    members_table = PersonsTable(members)
    RequestConfig(request).configure(members_table)
    context['members_table'] = members_table

    # Get owners
    owners = group.owners.all()

    # Build table
    owners_table = PersonsTable(owners)
    RequestConfig(request).configure(owners_table)
    context['owners_table'] = owners_table

    return render(request, 'core/group_%s.html' % template, context)


@login_required
def groups(request: HttpRequest) -> HttpResponse:
    context = {}

    # Get all groups
    groups = Group.objects.all()

    # Build table
    groups_table = GroupsTable(groups)
    RequestConfig(request).configure(groups_table)
    context['groups_table'] = groups_table

    return render(request, 'core/groups.html', context)


@admin_required
def persons_accounts(request: HttpRequest) -> HttpResponse:
    context = {}

    persons_qs = Person.objects.all()
    persons_accounts_formset = PersonsAccountsFormSet(request.POST or None, queryset=persons_qs)

    if request.method == 'POST':
        if persons_accounts_formset.is_valid():
            persons_accounts_formset.save()

    context['persons_accounts_formset'] = persons_accounts_formset

    return render(request, 'core/persons_accounts.html', context)


@admin_required
def edit_person(request: HttpRequest, id_: int) -> HttpResponse:
    context = {}

    person = get_object_or_404(Person, id=id_)

    edit_person_form = EditPersonForm(request.POST or None, request.FILES or None, instance=person)

    context['person'] = person

    if request.method == 'POST':
        if edit_person_form.is_valid():
            edit_person_form.save(commit=True)

            messages.success(request, _('The person has been saved.'))
            return redirect('edit_person_by_id', id_=person.id)

    context['edit_person_form'] = edit_person_form

    return render(request, 'core/edit_person.html', context)


@admin_required
def edit_group(request: HttpRequest, id_: int) -> HttpResponse:
    context = {}

    group = get_object_or_404(Group, id=id_)

    edit_group_form = EditGroupForm(request.POST or None, instance=group)


    if request.method == 'POST':
        if edit_group_form.is_valid():
            edit_group_form.save(commit=True)

            messages.success(request, _('The group has been saved.'))
            return redirect('groups')

    context['group'] = group
    context['edit_group_form'] = edit_group_form

    return render(request, 'core/edit_group.html', context)


def data_management(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'core/data_management.html', context)
