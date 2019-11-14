from email.utils import formatdate

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone, formats
from martor.templatetags.martortags import safe_markdown

from dashboard.settings import latest_article_settings, current_events_settings
from helper import get_current_events, get_newest_article_from_news, get_current_events_with_cal
from untisconnect.datetimeutils import get_name_for_next_week_day_from_today, calendar_week, weekday
from timetable.hints import get_all_hints_by_class_and_time_period, get_all_hints_for_teachers_by_time_period
from timetable.views import get_next_weekday_with_time, get_calendar_week
from untisconnect.api import TYPE_TEACHER, TYPE_CLASS
from untisconnect.plan import get_plan
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponseNotFound

from untisconnect.utils import get_type_and_object_of_user, get_plan_for_day
from .models import Activity, register_notification
from .models import Activity, register_notification, Cache
# from .apps import DashboardConfig
from mailer import send_mail_with_template
from userinformation import UserInformation
from .models import Activity, Notification


@login_required
def index(request):
    """ Dashboard: Show daily relevant information """

    return render(request, 'dashboard/index.html')


@login_required
def api_information(request):
    """ API request: Give information for dashboard in JSON """
    # Load activities
    activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Load notifications
    notifications = request.user.notifications.all().filter(user=request.user).order_by('-created_at')[:5]
    unread_notifications = request.user.notifications.all().filter(user=request.user, read=False).order_by(
        '-created_at')

    # Get latest article from homepage
    if latest_article_settings.latest_article_is_activated:
        newest_article = get_newest_article_from_news(domain=latest_article_settings.wp_domain)
    else:
        newest_article = None

    # Get date information
    date_formatted = get_name_for_next_week_day_from_today()
    next_weekday = get_next_weekday_with_time(timezone.now(), timezone.now().time())

    # Get user type (student, teacher, etc.)
    _type, el = get_type_and_object_of_user(request.user)

    # Get hints
    if _type == TYPE_TEACHER:
        # Get hints for teachers
        hints = list(get_all_hints_for_teachers_by_time_period(next_weekday, next_weekday))
    elif _type == TYPE_CLASS:
        # Get hints for students
        hints = list(get_all_hints_by_class_and_time_period(el, next_weekday, next_weekday))
    else:
        hints = []

    # Serialize hints
    ser = []
    for hint in hints:
        serialized = {
            "from_date": formatdate(float(hint.from_date.strftime('%s'))),
            "to_date": formatdate(float(hint.to_date.strftime('%s'))),
            "html": safe_markdown(hint.text)
        }
        ser.append(serialized)
    hints = ser

    context = {
        'activities': list(activities.values()),
        'notifications': list(notifications.values()),
        "unread_notifications": list(unread_notifications.values()),
        # 'user_type': UserInformation.user_type(request.user),
        # 'user_type_formatted': UserInformation.user_type_formatted(request.user),
        # 'classes': UserInformation.user_classes(request.user),
        # 'courses': UserInformation.user_courses(request.user),
        # 'subjects': UserInformation.user_subjects(request.user),
        # 'has_wifi': UserInformation.user_has_wifi(request.user),
        "newest_article": newest_article,
        "current_events": get_current_events_with_cal() if current_events_settings.current_events_is_activated else None,
        "date_formatted": date_formatted,
        "user": {
            "username": request.user.username,
            "full_name": request.user.first_name
        }
    }

    # If plan is available for user give extra information
    if _type is not None and request.user.has_perm("timetable.show_plan"):
        context["plan"] = {
            "type": _type,
            "name": el.shortcode if _type == TYPE_TEACHER else el.name,
            "hints": hints
        }
        context["has_plan"] = True
    else:
        context["has_plan"] = False

    return JsonResponse(context)


@login_required
def api_read_notification(request, id):
    """ API request: Mark notification as read """

    notification = get_object_or_404(Notification, id=id, user=request.user)
    notification.read = True
    notification.save()

    return JsonResponse({"success": True})


@login_required
def api_my_plan_html(request):
    """ API request: Get rendered lessons with substitutions for dashboard """

    # Get user type (student, teacher, etc.)
    _type, el = get_type_and_object_of_user(request.user)

    # Plan is only for teachers and students available
    if (_type != TYPE_TEACHER and _type != TYPE_CLASS) or not request.user.has_perm("timetable.show_plan"):
        return JsonResponse({"success": False})

    # Get calendar week and monday of week
    next_weekday = get_next_weekday_with_time()

    # Get plan
    plan, holiday = get_plan_for_day(_type, el.id, next_weekday)

    # Serialize plan
    lessons = []
    for lesson_container, time in plan:
        html = render_to_string("timetable/lesson.html", {"col": lesson_container, "type": _type}, request=request)
        lessons.append({"time": time, "html": html})

    # Return JSON
    return JsonResponse(
        {"success": True, "lessons": lessons, "holiday": holiday[0].__dict__ if len(holiday) > 0 else None})


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
    """ 404 page """
    return render(request, 'common/404.html')
