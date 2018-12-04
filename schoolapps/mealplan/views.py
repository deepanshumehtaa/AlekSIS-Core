import datetime
import os

from django.http import FileResponse
from django.shortcuts import render, redirect
from django.utils import timezone

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


def return_pdf(filename):
    print(filename)
    # Read and response PDF
    file = open(filename, "rb")
    return FileResponse(file, content_type="application/pdf")


def return_default_pdf():
    return return_pdf(os.path.join("mealplan", "default.pdf"))


def show_current(request):
    current_date = timezone.datetime.now()
    year, calendar_week = current_date.isocalendar()[:2]
    # print(calendar_week)
    # current_date += datetime.timedelta(days=4)
    days_to_add = 5 - current_date.isoweekday()
    # print(days_to_add)
    if days_to_add < 0:
        days_to_add = days_to_add + 7
    # print(days_to_add)
    friday = current_date + datetime.timedelta(days=days_to_add)
    # print(friday)
    friday_14_10 = timezone.datetime(friday.year, friday.month, friday.day, 14, 10)
    # print(friday_14_10)
    if current_date > friday_14_10:
        calendar_week += 1
    print(calendar_week)
    try:
        obj = MealPlan.objects.get(year=year, calendar_week=calendar_week)
        print(os.path.join("media", str(obj.pdf)))
        return return_pdf(os.path.join("media", str(obj.pdf)))
    except MealPlan.DoesNotExist:
        return return_default_pdf()
