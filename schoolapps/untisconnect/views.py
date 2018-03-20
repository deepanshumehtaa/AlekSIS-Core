from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from .api import get_all_teachers


@login_required
def test(request):
    teachers = get_all_teachers()
    context = {
        'teachers': teachers
    }
    return render(request, "untisconnect/test.html", context=context)
