from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from dashboard.models import Cache


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
