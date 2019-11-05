from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import MakeBookingForm


@login_required
#@permission_required('fibu.view_booking')
def index(request):
    items = Booking.objects.filter()
    print(items)

# @login_required
# @permission_required('fibu.make_booking')
# def make_booking(request):
    if request.method == 'POST':
        if 'booking-id' in request.POST:
            booking_id = request.POST['booking-id']
            booking = Booking.objects.get(id=booking_id)
            form = MakeBookingForm(instance=booking)
            print('Edit-Form erstellt ############# form.is_valid:', form.is_valid())
        else:
            form = MakeBookingForm(request.POST or None)
    else:
        form = MakeBookingForm()
    if form.is_valid():
        description = form.cleaned_data['description']
        planned_amount = form.cleaned_data['planned_amount']
        booking = Booking(description=description, planned_amount=planned_amount, contact=request.user)
        booking.save()

        # a = Activity(user=request.user, title="Antrag auf Unterrichtsbefreiung gestellt",
        #              description="Sie haben einen Antrag auf Unterrichtsbefreiung " +
        #                          "für den Zeitraum von {} bis {} gestellt.".format(
        #                              aub.from_date, aub.to_date), app=AubConfig.verbose_name)
        # a.save()
        # return redirect('fibu_make_booking')
        return redirect('fibu_index')
    context = {'bookings': items, 'form': form}
    return render(request, 'fibu/index.html', context)
