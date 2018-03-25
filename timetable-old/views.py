from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from untisconnect.api import *

try:
    from schoolapps.untisconnect.api import *
except Exception:
    pass


# Create your views here.
@login_required
def admin_all(request):
    teachers = get_all_teachers()
    classes = get_all_classes()
    rooms = get_all_rooms()
    context = {
        'teachers': teachers,
        'classes': classes,
        'rooms': rooms
    }
    return render(request, 'timetable/admin/all.html', context)


@login_required
def plan(request, plan_type, plan_id):
    context = {
        "title": "Stundenplan"
    }

    if plan_type == 'teacher':
        context["title"] = "Lehrkraftstundenplan"
    elif plan_type == 'class':
        pass
    elif plan_type == 'room':
        context["title"] = "Raumplan"
    else:
        raise Http404('Page not found.')

    return render(request, 'timetable/plan.html', context)
