from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Costcenter
from .filters import BookingFilter
from .forms import EditBookingForm, EditCostcenterForm


@login_required
#@permission_required('fibu.view_booking')
def index(request):
    if request.method == 'POST':
        if 'booking-id' in request.POST:
            booking_id = request.POST['booking-id']
            booking = Booking.objects.get(id=booking_id)
            if 'cancel' in request.POST:
                booking.delete()
#                a = Activity(user=aub_user, title="Antrag auf Unterrichtsbefreiung gelöscht",
#                             description="Sie haben Ihren Antrag auf Unterrichtsbefreiung " +
#                                         "für den Zeitraum von {} bis {} gelöscht.".format(
#                                             aub.from_date, aub.to_date), app=AubConfig.verbose_name)
#                a.save()
                print('Eintrag gelöscht')
                return redirect('fibu_index')
            elif 'ordered' in request.POST:
                Booking.objects.filter(id=booking_id).update(status=3)
                return redirect('fibu_index')
            elif 'submit-invoice' in request.POST:
                Booking.objects.filter(id=booking_id).update(status=4)
                return redirect('fibu_index')
            print('Edit-Form erstellt ############# form.is_valid:', form.is_valid())
            form = EditBookingForm(instance=booking)
        else:
            form = EditBookingForm(request.POST or None)
    else:
        form = EditBookingForm()
    if form.is_valid():
        account = ''
        description = form.cleaned_data['description']
        planned_amount = form.cleaned_data['planned_amount']
        justification = form.cleaned_data['justification']
        booking = Booking(account=account, description=description, planned_amount=planned_amount, contact=request.user, justification=justification)
        booking.save()

        # a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
        #              description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
        #                          "für den Zeitraum von {} bis {} gestellt.".format(
        #                              aub.from_date, aub.to_date), app=AubConfig.verbose_name)
        # a.save()
        # return redirect('fibu_make_booking')
        return redirect('fibu_index')
    bookings = Booking.objects.filter()
    context = {'bookings': bookings, 'form': form}
    return render(request, 'fibu/index.html', context)


@login_required
# @permission_required('aub.apply_for_aub')
def edit(request, id):
    booking = get_object_or_404(Booking, id=id)
    form = EditBookingForm(instance=booking)
    template = 'fibu/edit.html'
    if request.method == 'POST':
        form = EditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            # a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung verändert",
            #              description="Sie haben Ihren Antrag auf Unterrichtsbefreiung " +
            #                          "für den Zeitraum von {} bis {} bearbeitet.".format(
            #                              aub.from_date, aub.to_date), app=AubConfig.verbose_name)
            # a.save()
            return redirect(reverse('fibu_index'))
    context = {'form': form}
    return render(request, template, context)




@login_required
# @permission_required('fibu.check_booking')
def check(request):
    if request.method == 'POST':
        if 'booking-id' in request.POST:
            booking_id = request.POST['booking-id']
            booking = Booking.objects.get(id=booking_id)
            if 'allow' in request.POST:
                Booking.objects.filter(id=booking_id).update(status=1)
            elif 'deny' in request.POST:
                Booking.objects.filter(id=booking_id).update(status=2)
                # Notify user
                # register_notification(title="Ihr Antrag auf Unterrichtsbefreiung wurde abgelehnt",
                #                       description="Ihr Antrag auf Unterrichtsbefreiung vom {}, {} Uhr bis {}, {} Uhr wurde von der "
                #                                   "Schulleitung abgelehnt. Für weitere Informationen kontaktieren Sie "
                #                                   "bitte die Schulleitung."
                #                       .format(formats.date_format(aub.from_date),
                #                               formats.time_format(aub.from_time),
                #                               formats.date_format(aub.to_date),
                #                               formats.time_format(aub.to_time)),
                #                       app=AubConfig.verbose_name, user=aub.created_by,
                #                       link=request.build_absolute_uri(reverse('aub_details', args=[aub.id]))
                #                       )

    booking_list = Booking.objects.filter(status=0).order_by('submission_date')
    bookings = BookingFilter(request.GET, queryset=booking_list)
    return render(request, 'fibu/check.html', {'filter': bookings})


@login_required
#@permission_required('fibu.view_booking')
def costcenter(request):
    if request.method == 'POST':
        if 'costcenter-id' in request.POST:
            costcenter_id = request.POST['costcenter-id']
            costcenter = Costcenter.objects.get(id=costcenter_id)
            if 'cancel' in request.POST:
                costcenter.delete()
#                a = Activity(user=aub_user, title="Antrag auf Unterrichtsbefreiung gelöscht",
#                             description="Sie haben Ihren Antrag auf Unterrichtsbefreiung " +
#                                         "für den Zeitraum von {} bis {} gelöscht.".format(
#                                             aub.from_date, aub.to_date), app=AubConfig.verbose_name)
#                a.save()
                print('Eintrag gelöscht')
                return redirect('costcenter')
            print('Edit-Form erstellt ############# form.is_valid:', form.is_valid())
            form = EditCostcenterForm(instance=costcenter)
        else:
            form = EditCostcenterForm(request.POST or None)
    else:
        form = EditCostcenterForm()
    if form.is_valid():
        name = form.cleaned_data['name']
        schoolyear = form.cleaned_data['schoolyear']
        costcenter = Costcenter(name=name, schoolyear=schoolyear)
        costcenter.save()

        # a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
        #              description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
        #                          "für den Zeitraum von {} bis {} gestellt.".format(
        #                              aub.from_date, aub.to_date), app=AubConfig.verbose_name)
        # a.save()
        # return redirect('fibu_make_booking')
        return redirect('costcenter')
    costcenter = Costcenter.objects.filter()
    context = {'costcenter': costcenter, 'form': form}
    return render(request, 'fibu/costcenter.html', context)
