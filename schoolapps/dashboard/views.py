from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone, formats

from helper import get_newest_articles, get_current_events, get_newest_article_from_news
from schoolapps.settings import LONG_WEEK_DAYS
from timetable.helper import get_name_for_next_week_day_from_today, get_type_and_object_of_user
from timetable.views import get_next_weekday_with_time, get_calendar_week
from untisconnect.api import TYPE_TEACHER, TYPE_CLASS
from untisconnect.plan import get_plan
from .models import Activity, Notification
from userinformation import UserInformation


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
    newest_article = get_newest_article_from_news()

    date_formatted = get_name_for_next_week_day_from_today()

    # Get user type (student, teacher, etc.)
    _type, el = get_type_and_object_of_user(request.user)
    hints = None
    if _type == TYPE_TEACHER:
        # Teacher
        plan_id = el.id
        raw_type = "teacher"

        # Get hints
        # hints = list(get_all_hints_for_teachers_by_time_period(next_weekday, next_weekday))

    elif _type == TYPE_CLASS:
        # Student

        plan_id = el.id
        raw_type = "class"

        # Get hints
        # hints = list(get_all_hints_by_class_and_time_period(el, next_weekday, next_weekday))

    context = {
        'activities': list(activities.values()),
        'notifications': list(notifications.values()),
        "unread_notifications": list(unread_notifications.values()),
        'user_type': UserInformation.user_type(request.user),
        'user_type_formatted': UserInformation.user_type_formatted(request.user),
        'classes': UserInformation.user_classes(request.user),
        'courses': UserInformation.user_courses(request.user),
        'subjects': UserInformation.user_subjects(request.user),
        'has_wifi': UserInformation.user_has_wifi(request.user),
        "newest_article": newest_article,
        "current_events": get_current_events()[:3],
        "date_formatted": date_formatted,
        "user": {
            "username": request.user.username,
            "full_name": request.user.first_name
        }
    }

    if _type is not None:
        context["plan"] = {
            "type": _type,
            "name": el.shortcode if _type == TYPE_TEACHER else el.name,
            "hints": hints
        }
        context["has_plan"] = True
    else:
        context["has_plan"] = False

    print(context)
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
    hints = None
    if _type == TYPE_TEACHER:
        # Teacher
        plan_id = el.id
        raw_type = "teacher"

        # Get hints
        # hints = list(get_all_hints_for_teachers_by_time_period(next_weekday, next_weekday))

    elif _type == TYPE_CLASS:
        # Student

        plan_id = el.id
        raw_type = "class"

        # Get hints
        # hints = list(get_all_hints_by_class_and_time_period(el, next_weekday, next_weekday))
    else:
        return JsonResponse({"success": False})

    # Get calendar week and monday of week
    next_weekday = get_next_weekday_with_time(timezone.now(), timezone.now().time())
    calendar_week = next_weekday.isocalendar()[1]
    monday_of_week = get_calendar_week(calendar_week, next_weekday.year)["first_day"]
    week_day = next_weekday.isoweekday() - 1
    print(raw_type, plan_id, next_weekday, calendar_week, monday_of_week)

    # Get plan
    plan = get_plan(_type, plan_id, smart=True, monday_of_week=monday_of_week)
    lessons = []
    for row, time in plan:
        lesson_container = row[week_day]
        for element in lesson_container.elements:
            if element.substitution is not None:
                print(time)
                html = render_to_string("timetable/lesson.html", {"col": lesson_container}, request=request)
                time["start"] = formats.date_format(time["start"], "H:i")
                time["end"] = formats.date_format(time["end"], "H:i")

                lessons.append({"time": time, "html": html})
                break
    print(lessons)

    return JsonResponse({"success": True, "lessons": lessons})


def error_404(request, exception):
    return render(request, 'common/404.html')
