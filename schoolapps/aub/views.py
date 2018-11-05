from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils import formats
from datetime import datetime as dt

from .apps import AubConfig
from dashboard.models import Activity, register_notification
from .forms import FilterAUBForm, ApplyForAUBForm
from .models import Aub, Status
from .filters import AUBFilter
from .decorators import check_own_aub

IN_PROCESSING_STATUS = Status.objects.get_or_create(name='In Bearbeitung 1', style_classes='orange')[0]
SEMI_ALLOWED_STATUS = Status.objects.get_or_create(name='In Bearbeitung 2', style_classes='yellow')[0]
ALLOWED_STATUS = Status.objects.get_or_create(name='Genehmigt', style_classes='green')[0]
NOT_ALLOWED_STATUS = Status.objects.get_or_create(name='Abgelehnt', style_classes='red')[0]

@login_required
@permission_required('aub.apply_for_aub')
def index(request):
    if 'aub-id' in request.POST:
        aub_id = request.POST['aub-id']
        # Edit button pressed?
        if 'edit' in request.POST:
            aub = Aub.objects.filter(id=aub_id)
            print('Edit wurde gewählt')
            return render(request, 'aub/update', {'filter': aub})

        # Cancel button pressed?
        elif 'cancel' in request.POST:
            instance = Aub.objects.get(id=aub_id)
            instance.delete()
            print('Eintrag gelöscht')
#    order_crit = '-created_at'
    order_crit = 'from_dt'
    aubs = Aub.objects.filter(created_by=request.user).order_by(order_crit)[:100]

    context = {
        'aubs': aubs
    }
    return render(request, 'aub/index.html', context)

@login_required
@permission_required('aub.apply_for_aub')
@check_own_aub(login_url='/index.html')
def details(request, aub_id):
    aub = get_object_or_404(Aub, id=aub_id)
    context = {
        'aub': aub
    }
    return render(request, 'aub/details.html', context)

@login_required
@permission_required('aub.apply_for_aub')
def apply_for(request):
    if request.method == 'POST':

        form = ApplyForAUBForm(request.POST)

        if form.is_valid():
                from_dt = timezone.datetime.combine(form.cleaned_data['from_date'], form.cleaned_data['from_time'])
                to_dt = timezone.datetime.combine(form.cleaned_data['to_date'], form.cleaned_data['to_time'])
                description = form.cleaned_data['description']

                aub = Aub(from_dt=from_dt, to_dt=to_dt, description=description, created_by=request.user)
                aub.save()

                a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
                             description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
                                         "für den Zeitraum von {} bis {} gestellt.".format(
                                             aub.from_dt, aub.to_dt), app=AubConfig.verbose_name)
                a.save()

                return redirect(reverse('aub_applied_for'))
    else:
        form = ApplyForAUBForm()

    context = {
        'form': form,
    }


    return render(request, 'aub/apply_for.html', context)

@login_required
@permission_required('aub.apply_for_aub')
def apply_for_update(request):
    if request.method == 'POST':
        if 'aub-id' in request.POST:
            aub_id = request.POST['aub-id']
            aub = Aub.objects.get(id=aub_id)
            print(aub)
        form = ApplyForAUBForm(request.POST, initial=[aub.from_dt,aub.to_dt,aub.description])

        if form.is_valid():
                from_dt = timezone.datetime.combine(form.cleaned_data['from_date'], form.cleaned_data['from_time'])
                to_dt = timezone.datetime.combine(form.cleaned_data['to_date'], form.cleaned_data['to_time'])
                description = form.cleaned_data['description']

                aub = Aub(from_dt=from_dt, to_dt=to_dt, description=description, created_by=request.user)
                aub.save()

                a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
                             description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
                                         "für den Zeitraum von {} bis {} gestellt.".format(
                                             aub.from_dt, aub.to_dt), app=AubConfig.verbose_name)
                a.save()
                return redirect(reverse('aub_applied_for'))
    else:
        form = ApplyForAUBForm()
    context = {
        'form': form,
    }
    return render(request, 'aub/apply_for.html', context)



@login_required
@permission_required('aub.apply_for_aub')
def applied_for(request):
    context = {

    }

    return render(request, 'aub/applied_for.html', context)


@login_required
@permission_required('aub.check1_aub')
def check1(request):
    if request.method == 'POST':
        if 'aub-id' in request.POST:
            aub_id = request.POST['aub-id']
            if 'allow' in request.POST:
                Aub.objects.filter(id=aub_id).update(status=SEMI_ALLOWED_STATUS)
            elif 'deny' in request.POST:
                Aub.objects.filter(id=aub_id).update(status=NOT_ALLOWED_STATUS)

    aub_list = Aub.objects.all().order_by('status')
    aubs = AUBFilter(request.GET, queryset=aub_list)
    return render(request, 'aub/check.html', {'filter': aubs})


@login_required
@permission_required('aub.check2_aub')
def check2(request):
    if request.method == 'POST':
        if 'aub-id' in request.POST:
            aub_id = request.POST['aub-id']
            aub = Aub.objects.get(id=aub_id)
            if 'allow' in request.POST:
                # Update status
                Aub.objects.filter(id=aub_id).update(status=ALLOWED_STATUS)

                # Notify user
                register_notification(title="Ihr Antrag auf Unterrichtsbefreiung wurde genehmigt",
                                      description="Ihr Antrag auf Unterrichtsbefreiung vom {} bis {} wurde von der "
                                                  "Schulleitung genehmigt.".format(
                                          formats.date_format(aub.from_dt),
                                          formats.date_format(aub.to_dt)),
                                      app=AubConfig.verbose_name, user=aub.created_by,
                                      link=request.build_absolute_uri(reverse('aub_details', args=[aub.id])))
            elif 'deny' in request.POST:
                # Update status
                Aub.objects.filter(id=aub_id).update(status=NOT_ALLOWED_STATUS)

                # Notify user
                register_notification(title="Ihr Antrag auf Unterrichtsbefreiung wurde abgelehnt",
                                      description="Ihr Antrag auf Unterrichtsbefreiung vom {} bis {} wurde von der "
                                                  "Schulleitung abgelehnt. Für weitere Informationen kontaktieren Sie "
                                                  "bitte die Schulleitung.".format(
                                          formats.date_format(aub.from_dt),
                                          formats.date_format(aub.to_dt)),
                                      app=AubConfig.verbose_name, user=aub.created_by,
                                      link=request.build_absolute_uri(reverse('aub_details', args=[aub.id])))

    aub_list = Aub.objects.all().order_by('status')
    aubs = AUBFilter(request.GET, queryset=aub_list)

    return render(request, 'aub/check.html', {'filter': aubs})
