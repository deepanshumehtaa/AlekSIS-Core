from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from material import Layout, Row, Fieldset
from aub.models import Aub


class ApplyForAUBForm(forms.ModelForm):
    lessons = [('', ''), ('8:00', '1.'), ('8:45', '2.'), ('9:45', '3.'), ('10:35', '4.'), ('11:35', '5.'),
               ('12:25', '6.'), ('13:15', '7.'), ('14:05', '8.'), ('14:50', '9.')]
    initial_from_time = '8:00'
    initial_to_time = '15:35'
    from_date = forms.DateField(label='Datum', input_formats=['%d.%m.%Y'])
    from_lesson = forms.ChoiceField(label='Stunde', choices=lessons, required=False, widget=forms.Select(attrs={'onchange': 'setTime(this)'}))
    from_time = forms.TimeField(label='Zeit', input_formats=['%H:%M'], initial=initial_from_time, )
    to_date = forms.DateField(label='Datum', input_formats=['%d.%m.%Y'])
    to_lesson = forms.ChoiceField(label='Stunde', choices=lessons, required=False, widget=forms.Select(attrs={'onchange': 'setTime(this)'}))
    to_time = forms.TimeField(label='Zeit', input_formats=['%H:%M'], initial=initial_to_time)
    description = forms.CharField(label='Bitte begründen Sie Ihren Antrag.')

    layout = Layout(Fieldset('Von',
                             Row('from_date', 'from_lesson', 'from_time'),
                             ),
                    Fieldset('Bis',
                             Row('to_date', 'to_lesson', 'to_time'),
                             ),
                    Fieldset('Grund / Vorhaben',
                             'description'),
                    )

    class Meta:
        model = Aub
        fields = ('id', 'from_date', 'from_time', 'to_date', 'to_time', 'description')

    def clean(self):
        cleaned_data = super().clean()

    def clean_from_to_date(self):
        # not related to a form field, just to clean datetime values
        from_date = self.cleaned_data['from_date']
        # from_lesson = self.cleaned_data['from_lesson']
        from_time = self.cleaned_data['from_time']
        to_date = self.cleaned_data['to_date']
        # to_lesson = self.cleaned_data['to_lesson']
        to_time = self.cleaned_data['to_time']
        from_datetime = timezone.datetime.combine(from_date, from_time)
        print(from_datetime)
        to_datetime = timezone.datetime.combine(to_date, to_time)
        if (from_datetime < datetime.now()) or (to_datetime < datetime.now()):
            raise ValidationError(
                'Die Befreiung kann nicht für bereits vergangene Tage durchgeführt werden (Datumsfehler).')
        elif from_datetime > to_datetime:
            raise ValidationError('Das Von-Datum liegt hinter dem Bis-Datum.')
        return True

    def clean_description(self):
        data = self.cleaned_data['description']
        self.clean_from_to_date()
        if len(data) < 10:
            raise ValidationError('Bitte teilen Sie uns etwas mehr über Ihren Befreiungswunsch mit.')

        return data

 