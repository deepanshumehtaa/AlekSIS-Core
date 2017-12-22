from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Activity
from .apps import DashboardConfig


# Create your views here.

@login_required
def index(request):
    # Register visit
    act = Activity(title="Dashboard aufgerufen", description="Sie haben das Dashboard aufgerufen.",
                   app=DashboardConfig.verbose_name, user=request.user)
    act.save()

    # Load activities
    activities = Activity.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'activities': activities
    }

    return render(request, 'index.html', context)
