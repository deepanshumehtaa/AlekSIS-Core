from django import forms
from django.core.validators import FileExtensionValidator
from django.utils import timezone

from mealplan.models import MealPlan

current_year = timezone.datetime.now().year
options_for_year = [(current_year, current_year),
                    (current_year + 1, current_year + 1)]


class MenuUploadForm(forms.ModelForm):
    calendar_week = forms.ChoiceField(label="KW", choices=[(cw, cw) for cw in range(1, 53)])
    year = forms.ChoiceField(label="Jahr", initial=timezone.datetime.now().year,
                             choices=options_for_year)

    pdf = forms.FileField(label="PDF-Datei", validators=[FileExtensionValidator(allowed_extensions=["pdf"])])

    class Meta:
        model = MealPlan
        fields = ("calendar_week", "year", "pdf")
