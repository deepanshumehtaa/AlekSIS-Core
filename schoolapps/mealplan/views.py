from django.shortcuts import render, redirect

from mealplan.models import MealPlan
from .forms import MenuUploadForm


# Create your views here.
def upload(request):
    if request.method == 'POST':
        form = MenuUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('menu_index_msg', msg="success")
    else:
        form = MenuUploadForm()
    return render(request, 'menu/upload.html', {
        'form': form
    })


def index(request, msg=None):
    menus = MealPlan.objects.all().order_by("calendar_week", "year")
    return render(request, 'menu/index.html', {"msg": msg, "menus": menus})
