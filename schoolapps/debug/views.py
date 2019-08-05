from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from debug.models import DebugLogGroup


@login_required
# @permission_required("timetable.")
def debugging_tool(request):
    groups = DebugLogGroup.objects.all()
    return render(request, "debug/debug.html", {"groups": groups})
