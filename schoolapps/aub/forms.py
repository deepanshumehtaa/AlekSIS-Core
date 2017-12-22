from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class ApplyForAUBForm(forms.Form):
    from_dt = forms.DateTimeField(help_text="Bitte geben Sie den Anfangszeitpunkt der gewünschten Befreiung an.")
    to_dt = forms.DateTimeField(help_text="Bitte geben Sie den Endpunkt der gewünschten Befreiung an.")

    description = forms.CharField()

    def clean_from_dt(self):
        data = self.cleaned_data['from_dt']

        if data < timezone.now():
            raise ValidationError("Die Befreiung kann nur zukünftig durchgeführt werden.")

        return data

    def clean_to_dt(self):
        data = self.cleaned_data['to_dt']
        from_dt = self.cleaned_data['from_dt']

        if data < timezone.now():
            raise ValidationError("Die Befreiung kann nur zukünftig durchgeführt werden.")

        if from_dt > data:
            raise ValidationError("Die Befreiung kann nicht an einem Datum enden, " +
                                  "dass zum Beginn der Befreiung schon in der Vergangenheit liegt.")

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if len(data) < 10:
            raise ValidationError("Bitte teilen Sie uns etwas mehr über Ihren Befreiungswunsch mit")

        return data
