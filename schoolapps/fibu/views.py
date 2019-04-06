from django.shortcuts import render

from .models import Booking

# Create your views here.

@login_required
@permission_required('fibu.view_booking')
def index(request):
    items = Booking.objects.filter()

    context = {
        'bookings': items,
    }
    return render(request, 'fibu/index.html', context)
