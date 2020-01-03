from django import forms
from django.utils import timezone
from material import Layout, Row, Fieldset

from .models import Booking, CostCenter, Account


class SimpleBookingForm(forms.ModelForm):
    description = forms.CharField(label='Beschreibung – Was soll angeschafft werden?')
    planned_amount = forms.IntegerField(
        label='Erwarteter Betrag – Welcher Betrag ist erforderlich?', help_text="in Euro, ohne Komma")
    justification = forms.CharField(label='Begründung – Begründe ggf. deinen Antrag.', required=False)

    layout = Layout(Row('description', 'planned_amount'), Row('justification'))

    class Meta:
        model = Booking
        fields = ['id', 'description', 'planned_amount', 'justification']


class CheckBookingForm(forms.ModelForm):
    account = forms.ModelChoiceField(Account.objects.filter().order_by('cost_center', 'name'))

    class Meta:
        model = Booking
        fields = ['account', ]


class CompleteBookingForm(forms.ModelForm):
    accounts = Account.objects.filter().order_by('cost_center', 'name')
    account = forms.ModelChoiceField(queryset=accounts)
    submission_date = forms.DateField(label='Bearbeitungsdatum', initial=timezone.now())

    layout = Layout(Fieldset("Allgemeines",
                             Row('description', 'justification'),
                             Row("contact", "planned_amount"),
                             Row('account', 'status')
                             ),
                    Fieldset('Details',
                             Row('firma', 'invoice_number', 'amount'),
                             Row('invoice_date', 'maturity', 'submission_date', 'booking_date'),
                             Row('payout_number', 'upload')
                             )
                    )

    class Meta:
        model = Booking
        fields = ['id', 'description', 'planned_amount', 'justification', 'account', 'contact', 'invoice_date',
                  'invoice_number', 'firma', 'amount', 'submission_date', 'payout_number', 'booking_date',
                  'maturity', 'upload', 'status']


class CostCenterForm(forms.ModelForm):
    class Meta:
        model = CostCenter
        fields = ['id', 'name', 'year']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['id', 'name', 'cost_center', 'income', 'budget']
