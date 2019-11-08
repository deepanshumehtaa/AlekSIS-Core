from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponseNotFound
from .models import Activity, register_notification, Cache
# from .apps import DashboardConfig
from mailer import send_mail_with_template
from userinformation import UserInformation


# Create your views here.

@login_required
def index(request):
    """ Index page: Lists activities und notifications """
    # Register visit
    # act = Activity(title="Dashboard aufgerufen", description="Sie haben das Dashboard aufgerufen.",
    #                app=DashboardConfig.verbose_name, user=request.user)
    # act.save()
    print(request.user)
    # UserInformation.user_classes(request.user)
    print(UserInformation.user_courses(request.user))

    # Load activities
    activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Load notifications
    notifications = request.user.notifications.all().filter(user=request.user).order_by('-created_at')[:5]

    # user_type = UserInformation.user_type(request.user)
    context = {
        'activities': activities,
        'notifications': notifications,
        'user_type': UserInformation.user_type(request.user),
        'user_type_formatted': UserInformation.user_type_formatted(request.user),
        'classes': UserInformation.user_classes(request.user),
        'courses': UserInformation.user_courses(request.user),
        'subjects': UserInformation.user_subjects(request.user),
        'has_wifi': UserInformation.user_has_wifi(request.user)
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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tools(request):
    msg = None
    if request.session.get("msg", False):
        msg = request.session["msg"]
        request.session["msg"] = None

    caches = Cache.objects.all()
    context = {
        "msg": msg,
        "caches": caches
    }
    return render(request, "dashboard/tools.html", context)


@login_required
def tools_clear_cache(request, id=None):
    if id is not None:
        cache.delete(id)
        request.session["msg"] = "success_cleared_single_cache"
        print("[IMPORTANT] Single cache cleared!")
    else:
        cache.clear()
        request.session["msg"] = "success_cleared_whole_cache"
        print("[IMPORTANT] Whole cache cleared!")

    return redirect(reverse("tools"))


def error_404(request, exception):
    return render(request, 'common/404.html')