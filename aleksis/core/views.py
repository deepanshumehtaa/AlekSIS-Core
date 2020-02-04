from typing import Optional

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _

from django_tables2 import RequestConfig

from .decorators import admin_required, person_required
from .forms import (
    EditGroupForm,
    EditPersonForm,
    EditSchoolForm,
    EditTermForm,
    PersonsAccountsFormSet,
    GroupContactForm,
)
from .models import Activity, Group, Notification, Person, School, DashboardWidget
from .tables import GroupsTable, PersonsTable
from .util import messages


@person_required
def index(request: HttpRequest) -> HttpResponse:
    context = {}

    activities = request.user.person.activities.all()[:5]
    notifications = request.user.person.notifications.all()[:5]
    unread_notifications = request.user.person.notifications.all().filter(read=False)

    context["activities"] = activities
    context["notifications"] = notifications
    context["unread_notifications"] = unread_notifications

    context["widgets"] = DashboardWidget.objects.filter(active=True)

    return render(request, "core/index.html", context)


def offline(request):
    return render(request, "core/offline.html")


@login_required
def persons(request: HttpRequest) -> HttpResponse:
    context = {}

    # Get all persons
    persons = Person.objects.filter(is_active=True)

    # Build table
    persons_table = PersonsTable(persons)
    RequestConfig(request).configure(persons_table)
    context["persons_table"] = persons_table

    return render(request, "core/persons.html", context)


@login_required
def person(request: HttpRequest, id_: int) -> HttpResponse:
    context = {}

    # Get person and check access
    try:
        person = Person.objects.get(pk=id_)
    except Person.DoesNotExist as e:
        # Turn not-found object into a 404 error
        raise Http404 from e

    context["person"] = person

    # Get groups where person is member of
    groups = Group.objects.filter(members=id_)

    # Build table
    groups_table = GroupsTable(groups)
    RequestConfig(request).configure(groups_table)
    context["groups_table"] = groups_table

    return render(request, "core/person_full.html", context)


@login_required
def group(request: HttpRequest, id_: int) -> HttpResponse:
    context = {}

    # Get group and check if it exist
    try:
        group = Group.objects.get(pk=id_)
    except Group.DoesNotExist as e:
        # Turn not-found object into a 404 error
        raise Http404 from e

    context["group"] = group

    # Get group
    group = Group.objects.get(pk=id_)

    # Get members
    members = group.members.filter(is_active=True)

    # Build table
    members_table = PersonsTable(members)
    RequestConfig(request).configure(members_table)
    context["members_table"] = members_table

    # Get owners
    owners = group.owners.filter(is_active=True)

    # Build table
    owners_table = PersonsTable(owners)
    RequestConfig(request).configure(owners_table)
    context["owners_table"] = owners_table

    return render(request, "core/group_full.html", context)


@login_required
def groups(request: HttpRequest) -> HttpResponse:
    context = {}

    # Get all groups
    groups = Group.objects.all()

    # Build table
    groups_table = GroupsTable(groups)
    RequestConfig(request).configure(groups_table)
    context["groups_table"] = groups_table

    return render(request, "core/groups.html", context)


@admin_required
def persons_accounts(request: HttpRequest) -> HttpResponse:
    context = {}

    persons_qs = Person.objects.all()
    persons_accounts_formset = PersonsAccountsFormSet(request.POST or None, queryset=persons_qs)

    if request.method == "POST":
        if persons_accounts_formset.is_valid():
            persons_accounts_formset.save()

    context["persons_accounts_formset"] = persons_accounts_formset

    return render(request, "core/persons_accounts.html", context)


@admin_required
def edit_person(request: HttpRequest, id_: int) -> HttpResponse:
    context = {}

    person = get_object_or_404(Person, id=id_)

    edit_person_form = EditPersonForm(request.POST or None, request.FILES or None, instance=person)

    context["person"] = person

    if request.method == "POST":
        if edit_person_form.is_valid():
            edit_person_form.save(commit=True)

            messages.success(request, _("The person has been saved."))
            return redirect("edit_person_by_id", id_=person.id)

    context["edit_person_form"] = edit_person_form

    return render(request, "core/edit_person.html", context)


@admin_required
def edit_group(request: HttpRequest, id_: Optional[int] = None) -> HttpResponse:
    context = {}

    if id_:
        group = get_object_or_404(Group, id=id_)
        edit_group_form = EditGroupForm(request.POST or None, instance=group)
    else:
        group = None
        edit_group_form = EditGroupForm(request.POST or None)

    if request.method == "POST":
        if edit_group_form.is_valid():
            edit_group_form.save(commit=True)

            messages.success(request, _("The group has been saved."))
            return redirect("groups")

    context["group"] = group
    context["edit_group_form"] = edit_group_form

    return render(request, "core/edit_group.html", context)


@admin_required
def data_management(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "core/data_management.html", context)


@admin_required
def system_status(request: HttpRequest) -> HttpResponse:
    context = {}

    return render(request, "core/system_status.html", context)


@admin_required
def school_management(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "core/school_management.html", context)


@admin_required
def edit_school(request: HttpRequest) -> HttpResponse:
    context = {}

    school = School.objects.first()
    edit_school_form = EditSchoolForm(request.POST or None, request.FILES or None, instance=school)

    context["school"] = school

    if request.method == "POST":
        if edit_school_form.is_valid():
            edit_school_form.save(commit=True)

            messages.success(request, _("The school has been saved."))
            return redirect("index")

    context["edit_school_form"] = edit_school_form

    return render(request, "core/edit_school.html", context)


@admin_required
def edit_schoolterm(request: HttpRequest) -> HttpResponse:
    context = {}

    term = School.objects.first().current_term
    edit_term_form = EditTermForm(request.POST or None, instance=term)

    if request.method == "POST":
        if edit_term_form.is_valid():
            edit_term_form.save(commit=True)

            messages.success(request, _("The term has been saved."))
            return redirect("index")

    context["edit_term_form"] = edit_term_form

    return render(request, "core/edit_schoolterm.html", context)


def notification_mark_read(request: HttpRequest, id_: int) -> HttpResponse:
    context = {}

    notification = get_object_or_404(Notification, pk=id_)

    if notification.recipient.user == request.user:
        notification.read = True
        notification.save()
    else:
        raise PermissionDenied(_("You are not allowed to mark notifications from other users as read!"))

    return redirect("index")

@login_required
def group_contact(request: HttpRequest, id_: int) -> HttpResponse:
    context = {}

    current_person = Person.objects.get(user=request.user)

    group = get_object_or_404(Group, id=id_)
    context['group'] = group

    group_contact_form = GroupContactForm()

    if request.method == 'POST':
        group_contact_form = GroupContactForm(request.POST)
        if group_contact_form.is_valid():
            if group_contact_form.cleaned_data['service'] == 'mail':
                message = EmailMessage()

                if group_contact_form.cleaned_data['sender'] == 'self':
                    message.from_email = '"%s" <%s>' % (
                        current_person.full_name, current_person.email)
                elif group_contact_form.cleaned_data['sender'] == 'self_masq':
                    message.from_email = '"%s" <%s>' % (
                        current_person.first_name, settings.MAIL_OUT)
                elif group_contact_form.cleaned_data['sender'] == 'org':
                    message.from_email = settings.MAIL_OUT

                message.bcc = []
                for person in group.members.all():
                    if 'group' in group_contact_form.cleaned_data['recipients']:
                        message.bcc.append(person.email)
                    if 'guardians' in group_contact_form.cleaned_data['recipients']:
                        for guardian in person.guardians:
                            message.bcc.append(guardian.email)

                if 'owners' in group_contact_form.cleaned_data['recipients']:
                    for owner in group.owners.all():
                        message.bcc.append(owner.email)

                message.subject = group_contact_form.cleaned_data['subject']
                message.body = group_contact_form.cleaned_data['text']

                message.send()
            elif group_contact_form.cleaned_data['service'] == 'sms':
                if group_contact_form.cleaned_data['sender'] == 'self':
                    sender = current_person.mobile
                    if not sender:
                        sender = current_person.first_name[:11]
                elif group_contact_form.cleaned_data['sender'] == 'self_masq':
                    sender = current_person.first_name[:11]
                elif group_contact_form.cleaned_data['sender'] == 'org':
                    sender = settings.SITE_TITLE

                to = []
                for person in group.members.all():
                    if 'group' in group_contact_form.cleaned_data['recipients']:
                        to.append(person.mobile_number)
                    if 'guardians' in group_contact_form.cleaned_data['recipients']:
                        for guardian in person.guardians:
                            to.append(guardian.mobile_number)

                if 'owners' in group_contact_form.cleaned_data['recipients']:
                    for owner in group.owners.all():
                        to.append(owner.mobile_number)

                msg = group_contact_form.cleaned_data['text']

                ret = send_sms(sender, to, msg)
                if ret.status_code != 200:
                    context['error'] = _(
                        'SMS could not be transmitted to provider.')
            return redirect('group_by_id', id_=id_)

    context['group_contact_form'] = group_contact_form

    return render(request, 'core/group_contact.html', context)
