from django import forms
from django.core.exceptions import ValidationError
#from django.utils import timezone
from datetime import datetime


class ApplyForAUBForm(forms.Form):
    from_date = forms.DateField(initial='')
    to_date = forms.DateField(initial='')

    from_time = forms.TimeField(initial='')
    to_time = forms.TimeField(initial='')

    description = forms.CharField(initial='')

    def clean(self):
        cleaned_data = super().clean()

    def clean_from_to_date(self):
        # not related to a form field, just to clean datetime values
        from_date = self.cleaned_data['from_date']
        from_time = self.cleaned_data['from_time']
        to_date = self.cleaned_data['to_date']
        to_time = self.cleaned_data['to_time']
        from_datetime = datetime.combine(from_date,from_time)
        print(from_datetime)
        to_datetime = datetime.combine(to_date, to_time)
        if (from_datetime < datetime.now()) or (to_datetime < datetime.now()):
            raise ValidationError('Die Befreiung kann nicht für vergangenen Unterricht durchgeführt werden (Datumsfehler).')
        elif from_datetime > to_datetime:
            raise ValidationError('Das erste Datum liegt später als das zweiten Datum.')
        return True

    def clean_from_date(self):
        data = self.cleaned_data['from_date']
        # if data < timezone.datetime.date(timezone.now()):
        #     raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden (Datumsfehler).')
        return data

    def clean_to_date(self):
        data = self.cleaned_data['to_date']
        # if data < timezone.datetime.date(timezone.now()):
        #     raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden.')
        return data

    def clean_from_time(self):
        data = self.cleaned_data['from_time']
        #print('Data:', type(data), 'Now:', type(timezone.datetime.time(timezone.now())))
        
        # if data < timezone.datetime.time(timezone.now()):
        #     raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden (Zeitfehler).')

        return data

    def clean_to_time(self):
        data = self.cleaned_data['to_time']

        # if data < timezone.datetime.time(timezone.now()):
        #     raise ValidationError('Die Befreiung kann nur zukünftig durchgeführt werden.')
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        self.clean_from_to_date()
        if len(data) < 10:
            raise ValidationError('Bitte teilen Sie uns etwas mehr über Ihren Befreiungswunsch mit.')

        return data
