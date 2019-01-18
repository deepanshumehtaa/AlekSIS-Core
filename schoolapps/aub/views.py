from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils import formats
from datetime import date
from datetime import datetime as dt
from django.core.exceptions import ValidationError

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
        id = request.POST['aub-id']
        # Edit button pressed?
        if 'edit' in request.POST:
            instance = Aub.objects.filter(id=id)
            print('...Edit wurde gewählt')
            # return render(request, 'aub/apply_for.html', {'filter': instance})
            apply_for(request, id=id)

        # Cancel button pressed?
        elif 'cancel' in request.POST:
            instance = Aub.objects.get(id=id)
            instance.delete()
            print('Eintrag gelöscht')
    #    order_crit = '-created_at'
    order_crit = 'from_date'
    aubs = Aub.objects.filter(created_by=request.user).order_by(order_crit)[:100]

    context = {
        'aubs': aubs
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
        print('Fall 1 - ')
        if 'aub-id' in request.POST:
            id = request.POST['aub-id']
            instance = Aub.objects.get(id=id)
            form = ApplyForAUBForm(instance=instance)
            print('Fall 2 - ', 'form.is_valid:', form.is_valid(), 'form.errors:', form.errors)
        else:
            form = ApplyForAUBForm(request.POST or None)
            print('Fall 3 - ', 'request.POST:', request.POST, 'form.is_valid:', form.is_valid(), 'form.errors:',
                  form.errors)
    else:
        form = ApplyForAUBForm()
        print('Fall 4 - ', 'form.is_valid:', form.is_valid(), 'form.errors:', form.errors)
    print('Fall 5 - ', 'form.is_valid:', form.is_valid(), 'form.errors:', form.errors)
    if form.is_valid():
        print('form:', form)
        # form.save()
        from_date = form.cleaned_data['from_date']
        from_time = form.cleaned_data['from_time']
        to_date = form.cleaned_data['to_date']
        to_time = form.cleaned_data['to_time']
        description = form.cleaned_data['description']

        aub = Aub(from_date=from_date, from_time=from_time, to_date=to_date, to_time=to_time, description=description,
                  created_by=request.user)
        aub.save()

        a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
                     description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
                                 "für den Zeitraum von {} bis {} gestellt.".format(
                                     aub.from_date, aub.to_date), app=AubConfig.verbose_name)
        a.save()
        return redirect('aub_applied_for')
    return render(request, 'aub/apply_for.html', {'form': form})


#     # Form is filled
#     if request.method == 'POST':
#         # get form via edit-button
#         if 'aub-id' in request.POST:
#             id = request.POST['aub-id']
# #            instance = get_object_or_404(Aub, id=id)
#             instance = Aub.objects.get(id=id)
#             print('AUB:', id, '|', instance.from_date, '|', instance.to_date, '|', instance.description)
#             #instance.description = 'Mal was ganz anderes'
#             form = ApplyForAUBForm(request.POST, instance=instance)
#             #print('Form ist valid? IF:', instance.created_by, instance.to_date, instance.id)
#             return render(request, 'aub/apply_for.html', {'form': form})
#         # get a new item
#         else:
#             form = ApplyForAUBForm(request.POST or None)
#             print('Form ist valid? ELSE:', form.errors)
#             if form.is_valid():
#                 print('Form ist valid!', form.errors)
#                 aub = form.save()
#                 print('aub-id:', aub.id)
#                 aub.created_by = request.user
#                 aub.save()
#                 return redirect('aub_applied_for')
#     form = ApplyForAUBForm()
# #    return render(request, 'aub/apply_for.html', {'form': form, 'from_dt': instance.from_dt})
#     return render(request, 'aub/apply_for.html', {'form': form})

# if request.method == 'POST':
#
#     if 'aub-id' in request.POST:
#         aub_id = request.POST['aub-id']
#         aub = Aub.objects.get(id=aub_id)
#         print('AUB:', aub_id, '|', aub.from_dt, '|', aub.to_dt, '|', aub.description)
#         form = ApplyForAUBForm(request.POST, instance=aub)
#     else:
#         form = ApplyForAUBForm(request.POST)
#     # form = ApplyForAUBForm(request.POST, initial=[aub.from_dt, aub.to_dt, aub.description])
#     if form.is_valid():
#             from_dt = timezone.datetime.combine(form.cleaned_data['from_date'], form.cleaned_data['from_time'])
#             to_dt = timezone.datetime.combine(form.cleaned_data['to_date'], form.cleaned_data['to_time'])
#             description = form.cleaned_data['description']
#
#             aub = Aub(from_dt=from_dt, to_dt=to_dt, description=description, created_by=request.user)
#             aub.save()
#
#             a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
#                          description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
#                                      "für den Zeitraum von {} bis {} gestellt.".format(
#                                          aub.from_dt, aub.to_dt), app=AubConfig.verbose_name)
#             a.save()
#
#             return redirect(reverse('aub_applied_for'))
#
# else:
#     form = ApplyForAUBForm()
#
# context = {
#     'Aub': aub,
#     'form': form,
# }
# return render(request, 'aub/apply_for.html', context)


# @login_required
# @permission_required('aub.apply_for_aub')
# def apply_for(request):
#     if request.method == 'POST':
#
#         if 'aub-id' in request.POST:
#             aub_id = request.POST['aub-id']
#             aub = Aub.objects.get(id=aub_id)
#             print('AUB:', aub_id, '|', aub.from_dt, '|', aub.to_dt, '|', aub.description)
#             form = ApplyForAUBForm(request.POST, instance=aub)
#         else:
#             form = ApplyForAUBForm(request.POST)
#         # form = ApplyForAUBForm(request.POST, initial=[aub.from_dt, aub.to_dt, aub.description])
#         if form.is_valid():
#                 from_dt = timezone.datetime.combine(form.cleaned_data['from_date'], form.cleaned_data['from_time'])
#                 to_dt = timezone.datetime.combine(form.cleaned_data['to_date'], form.cleaned_data['to_time'])
#                 description = form.cleaned_data['description']
#
#                 aub = Aub(from_dt=from_dt, to_dt=to_dt, description=description, created_by=request.user)
#                 aub.save()
#
#                 a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
#                              description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
#                                          "für den Zeitraum von {} bis {} gestellt.".format(
#                                              aub.from_dt, aub.to_dt), app=AubConfig.verbose_name)
#                 a.save()
#
#                 return redirect(reverse('aub_applied_for'))
#
#     else:
#         form = ApplyForAUBForm()
#
#     context = {
#         'Aub': aub,
#         'form': form,
#     }
#     return render(request, 'aub/apply_for.html', context)

@login_required
@permission_required('aub.apply_for_aub')
def edit(request, id):
    aub = get_object_or_404(Aub, id=id)
    form = ApplyForAUBForm(instance=aub)
    template = 'aub/edit.html'
    if request.method == 'POST':
        form = ApplyForAUBForm(request.POST, instance=aub)
        if form.is_valid():
            form.save()
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
            id = request.POST['aub-id']
            if 'allow' in request.POST:
                Aub.objects.filter(id=id).update(status=SEMI_ALLOWED_STATUS)
            elif 'deny' in request.POST:
                Aub.objects.filter(id=id).update(status=NOT_ALLOWED_STATUS)

    aub_list = Aub.objects.all().order_by('status')
    aubs = AUBFilter(request.GET, queryset=aub_list)
    return render(request, 'aub/check.html', {'filter': aubs})


@login_required
@permission_required('aub.check2_aub')
def check2(request):
    if request.method == 'POST':
        if 'aub-id' in request.POST:
            id = request.POST['aub-id']
            aub = Aub.objects.get(id=id)
            if 'allow' in request.POST:
                # Update status
                Aub.objects.filter(id=id).update(status=ALLOWED_STATUS)

                # Notify user
                register_notification(title="Ihr Antrag auf Unterrichtsbefreiung wurde genehmigt",
                                      description="Ihr Antrag auf Unterrichtsbefreiung vom {} bis {} wurde von der "
                                                  "Schulleitung genehmigt.".format(
                                          #                                            formats.date_format(aub.from_dt),
                                          #                                            formats.date_format(aub.to_dt)),
                                          formats.date_format(aub.from_date),
                                          formats.date_format(aub.to_date)),
                                      app=AubConfig.verbose_name, user=aub.created_by,
                                      link=request.build_absolute_uri(reverse('aub_details', args=[aub.id])))
            elif 'deny' in request.POST:
                # Update status
                Aub.objects.filter(id=id).update(status=NOT_ALLOWED_STATUS)

                # Notify user
                register_notification(title="Ihr Antrag auf Unterrichtsbefreiung wurde abgelehnt",
                                      description="Ihr Antrag auf Unterrichtsbefreiung vom {} bis {} wurde von der "
                                                  "Schulleitung abgelehnt. Für weitere Informationen kontaktieren Sie "
                                                  "bitte die Schulleitung.".format(
                                          #                                          formats.date_format(aub.from_dt),
                                          #                                          formats.date_format(aub.to_dt)),
                                          formats.date_format(aub.from_date),
                                          formats.date_format(aub.to_date)),
                                      app=AubConfig.verbose_name, user=aub.created_by,
                                      link=request.build_absolute_uri(reverse('aub_details', args=[aub.id])))

    aub_list = Aub.objects.all().order_by('status')
    aubs = AUBFilter(request.GET, queryset=aub_list)

    return render(request, 'aub/check.html', {'filter': aubs})
