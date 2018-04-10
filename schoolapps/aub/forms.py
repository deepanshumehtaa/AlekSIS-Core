from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class ApplyForAUBForm(forms.Form):
    from_date = forms.DateField(initial='')
    to_date = forms.DateField(initial='')

    from_time = forms.TimeField(initial='')
    to_time = forms.TimeField(initial='')

    description = forms.CharField(initial='')

    def clean(self):
        cleaned_data = super().clean()

    def clean_from_date(self):
        data = self.cleaned_data['from_date']
        print(data,timezone.datetime.time(timezone.now()) )
        if data < timezone.datetime.date(timezone.now()):
            raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden (Datumsfehler).')

        return data

    def clean_to_date(self):
        data = self.cleaned_data['to_date']

        # if data < timezone.datetime.date(timezone.now()):
        #     raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden.')

        return data

    def clean_from_time(self):
        data = self.cleaned_data['from_time']
       
        if data < timezone.datetime.time(timezone.now()):
            raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden (Zeitfehler).')

        return data

    def clean_to_time(self):
        data = self.cleaned_data['to_time']

        # if data < timezone.datetime.time(timezone.now()):
        #     raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden.')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if len(data) < 10:
            raise ValidationError('Bitte teilen Sie uns etwas mehr über Ihren Befreiungswunsch mit.')

        return data
