from django import forms
from django.utils import timezone

from mealplan.models import MealPlan


class MenuUploadForm(forms.ModelForm):
    calendar_week = forms.ChoiceField(label="KW", choices=[(cw, cw) for cw in range(1, 53)])
    year = forms.ChoiceField(label="Jahr", initial=timezone.datetime.now().year,
                             choices=[(timezone.datetime.now().year, timezone.datetime.now().year),
                                      (timezone.datetime.now().year + 1, timezone.datetime.now().year + 1)])

    # pdf = forms.FileField(label="PDF-Datei")

    class Meta:
        model = MealPlan
        fields = ("calendar_week", "year", "pdf")
