from django.shortcuts import render

from meta import OPEN_SOURCE_COMPONENTS


def about(request):
    return render(request, "common/about.html", context={"components": OPEN_SOURCE_COMPONENTS})
