from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from debug.models import DebugLogGroup


@login_required
@permission_required("debug.can_view_debug_log")
def debugging_tool(request):
    groups = DebugLogGroup.objects.all()
    return render(request, "debug/debug.html", {"groups": groups})
