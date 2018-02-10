from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Activity
from .apps import DashboardConfig
from mailer import send_mail_with_template


# Create your views here.

@login_required
def index(request):
    """ Index page: Lists activities und notifications """
    # Register visit
    act = Activity(title="Dashboard aufgerufen", description="Sie haben das Dashboard aufgerufen.",
                   app=DashboardConfig.verbose_name, user=request.user)
    act.save()

    # Load activities
    activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:5]
    notifications = request.user.notifications.all()[:5]

    context = {
        'activities': activities,
        'notifications': notifications,
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def test_mail(request):
    """ Sends a test mail """
    send_mail_with_template("Test", [request.user.email], 'mail/email.txt', 'mail/email.html', {'user': request.user})
    return redirect(reverse('dashboard'))
