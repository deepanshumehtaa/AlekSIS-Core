from .models import Booking
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
#@permission_required('fibu.view_booking')
def index(request):
    #items = Booking.objects.filter()
    items = [1,2]
    print(items)

    context = {
        'bookings': items,
    }
    return render(request, 'fibu/index.html', context)
