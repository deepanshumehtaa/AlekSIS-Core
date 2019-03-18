from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.utils import formats
from datetime import date
from datetime import datetime as dt
from django.core.exceptions import ValidationError

from .apps import AubConfig
from dashboard.models import Activity, register_notification
from .forms import ApplyForAUBForm
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
    aub_user = request.user
    if 'aub-id' in request.POST:
        aub_id = request.POST['aub-id']
        if 'cancel' in request.POST:
            aub = Aub.objects.get(id=aub_id)
            aub.delete()
            a = Activity(user=aub_user, title="Antrag auf Unterrichtsbefreiung gelöscht",
                         description="Sie haben Ihren Antrag auf Unterrichtsbefreiung " +
                                     "für den Zeitraum von {} bis {} gelöscht.".format(
                                         aub.from_date, aub.to_date), app=AubConfig.verbose_name)
            a.save()
            print('Eintrag gelöscht')
    order_crit = '-from_date'
    aubs = Aub.objects.filter(created_by=aub_user).order_by(order_crit)[:100]

    context = {
        'aubs': aubs,
        'user': aub_user,
    }
    return render(request, 'aub/index.html', context)


@login_required
@permission_required('aub.apply_for_aub')
@check_own_aub(login_url='/index.html')
def details(request, id):
    aub = get_object_or_404(Aub, id=id)
    context = {
        'aub': aub
    }
    return render(request, 'aub/details.html', context)


@login_required
@permission_required('aub.apply_for_aub')
def apply_for(request):
    if request.method == 'POST':
        if 'aub-id' in request.POST:
            aub_id = request.POST['aub-id']
            aub = Aub.objects.get(id=aub_id)
            form = ApplyForAUBForm(instance=aub)
            print('Edit-Form erstellt ############# form.is_valid:', form.is_valid())
        else:
            form = ApplyForAUBForm(request.POST or None)
    else:
        form = ApplyForAUBForm()
    if form.is_valid():
        from_date = form.cleaned_data['from_date']
        from_time = form.cleaned_data['from_time']
        to_date = form.cleaned_data['to_date']
        to_time = form.cleaned_data['to_time']
        description = form.cleaned_data['description']

        aub = Aub(from_date=from_date, from_time=from_time, to_date=to_date,
                  to_time=to_time, description=description, created_by=request.user)
        aub.save()

        a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
                     description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
                                 "für den Zeitraum von {} bis {} gestellt.".format(
                                     aub.from_date, aub.to_date), app=AubConfig.verbose_name)
        a.save()
        return redirect('aub_applied_for')
    return render(request, 'aub/apply_for.html', {'form': form})


@login_required
@permission_required('aub.apply_for_aub')
def edit(request, aub_id):
    aub = get_object_or_404(Aub, id=aub_id)
    form = ApplyForAUBForm(instance=aub)
    template = 'aub/edit.html'
    if request.method == 'POST':
        form = ApplyForAUBForm(request.POST, instance=aub)
        if form.is_valid():
            form.save()
            a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung verändert",
                         description="Sie haben Ihren Antrag auf Unterrichtsbefreiung " +
                                     "für den Zeitraum von {} bis {} bearbeitet.".format(
                                         aub.from_date, aub.to_date), app=AubConfig.verbose_name)
            a.save()
            return redirect(reverse('aub_applied_for'))
    context = {
        'form': form
    }
    return render(request, template, context)


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

    aub_list = Aub.objects.filter(status=IN_PROCESSING_STATUS).order_by('created_at')
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
                                      description="Ihr Antrag auf Unterrichtsbefreiung vom {}, {} Uhr bis {}, {} Uhr wurde von der "
                                                  "Schulleitung genehmigt."
                                                  .format(formats.date_format(aub.from_date),
                                                          formats.time_format(aub.from_time),
                                                          formats.date_format(aub.to_date),
                                                          formats.time_format(aub.to_time)),
                                      app=AubConfig.verbose_name, user=aub.created_by,
                                      link=request.build_absolute_uri(reverse('aub_details', args=[aub.id]))
                                      )
            elif 'deny' in request.POST:
                # Update status
                Aub.objects.filter(id=aub_id).update(status=NOT_ALLOWED_STATUS)

                # Notify user
                register_notification(title="Ihr Antrag auf Unterrichtsbefreiung wurde abgelehnt",
                                      description="Ihr Antrag auf Unterrichtsbefreiung vom {}, {} Uhr bis {}, {} Uhr wurde von der "
                                                  "Schulleitung abgelehnt. Für weitere Informationen kontaktieren Sie "
                                                  "bitte die Schulleitung."
                                                  .format(formats.date_format(aub.from_date),
                                                          formats.time_format(aub.from_time),
                                                          formats.date_format(aub.to_date),
                                                          formats.time_format(aub.to_time)),
                                      app=AubConfig.verbose_name, user=aub.created_by,
                                      link=request.build_absolute_uri(reverse('aub_details', args=[aub.id]))
                                      )

    aub_list = Aub.objects.filter(status=SEMI_ALLOWED_STATUS).order_by('created_at')
    aubs = AUBFilter(request.GET, queryset=aub_list)

    return render(request, 'aub/check.html', {'filter': aubs})


@login_required
@permission_required('aub.view_archive')
def archive(request):
    order_crit = '-from_date'
    if 'created_by' in request.GET:
        item = int(request.GET['created_by'])
        aub_list = Aub.objects.filter((Q(status__exact=ALLOWED_STATUS) | Q(status__exact=NOT_ALLOWED_STATUS)) & Q(created_by=item)).order_by(order_crit)
    else:
        aub_list = Aub.objects.filter(Q(status__exact=ALLOWED_STATUS) | Q(status__exact=NOT_ALLOWED_STATUS)).order_by(order_crit)
    aub_filter = AUBFilter(request.GET, queryset=aub_list)
    return render(request, 'aub/archive.html', {'filter': aub_filter})
