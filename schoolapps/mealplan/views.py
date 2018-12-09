import datetime
import os

from django.http import FileResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from mealplan.models import MealPlan
from .forms import MenuUploadForm


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


def delete(request, id):
    print(id)
    MealPlan.objects.get(id=id).delete()

    return redirect("menu_index_msg", msg="delete_success")


def index(request, msg=None):
    menus = MealPlan.objects.all().order_by("calendar_week", "year")
    return render(request, 'menu/index.html', {"msg": msg, "menus": menus})


def return_pdf(filename):
    """Read and response a PDF file"""

    file = open(filename, "rb")
    return FileResponse(file, content_type="application/pdf")


def return_default_pdf():
    """Response the default PDF"""

    return return_pdf(os.path.join("mealplan", "default.pdf"))


def show_current(request):
    # Get current date with year and calendar week
    current_date = timezone.datetime.now()
    year, calendar_week = current_date.isocalendar()[:2]

    # Calculate the number of days to next friday
    days_to_add = 5 - current_date.isoweekday()
    if days_to_add < 0:
        days_to_add = days_to_add + 7

    # Create datetime with next friday and time 14:10
    friday = current_date + datetime.timedelta(days=days_to_add)
    friday_14_10 = timezone.datetime(friday.year, friday.month, friday.day, 14, 10)

    # Check whether to show the plan of the next week or the current week
    if current_date > friday_14_10:
        calendar_week += 1

    # Look for matching PDF in DB
    try:
        obj = MealPlan.objects.get(year=year, calendar_week=calendar_week)
        return return_pdf(os.path.join("media", str(obj.pdf)))

    # Or show the default PDF
    except MealPlan.DoesNotExist:
        return return_default_pdf()
