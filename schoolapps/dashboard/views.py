from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Activity, register_notification
# from .apps import DashboardConfig
from mailer import send_mail_with_template


# Create your views here.

@login_required
def index(request):
    """ Index page: Lists activities und notifications """
    # Register visit
    # act = Activity(title="Dashboard aufgerufen", description="Sie haben das Dashboard aufgerufen.",
    #                app=DashboardConfig.verbose_name, user=request.user)
    # act.save()

    # Load activities
    activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Load notifications
    notifications = request.user.notifications.all().filter(user=request.user).order_by('-created_at')

    context = {
        'activities': activities,
        'notifications': notifications,
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def test_notification(request):
    """ Sends a test mail """
    # send_mail_with_template("Test", [request.user.email], 'mail/email.txt', 'mail/email.html', {'user': request.user})
    register_notification(user=request.user, title="Ihr Antrag wurde genehmigt",
                          description="Ihr Antrag XY wurde von der Schulleitung genehmigt.", app="AUB",
                          link=reverse("aub_details", args=[1]))
    print(reverse("aub_details", args=[1]))
    return redirect(reverse('dashboard'))


def impress(request):
    return render(request, 'common/impress.html')


def error_404(request, exception):
    return render(request, 'common/404.html')
