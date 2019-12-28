from django import forms
from django.contrib.auth.models import User
from material import Layout, Row, Fieldset

from .models import YEARS, Booking, Costcenter, Account, status_choices


class BookingForm(forms.ModelForm):
    description = forms.CharField(label='Beschreibung – Was soll angeschafft werden?')
    planned_amount = forms.IntegerField(
        label='Erwarteter Betrag – Welcher Betrag ist erforderlich?', help_text="in Euro, ohne Komma")
    justification = forms.CharField(label='Begründung – Begründe ggf. deinen Antrag.', required=False)

    layout = Layout(Row('description', 'planned_amount'), Row('justification'))

    class Meta:
        model = Booking
        fields = ['id', 'description', 'planned_amount', 'justification']


class CheckBookingForm(forms.ModelForm):
    account = forms.ModelChoiceField(Account.objects.filter().order_by('costcenter','name'))
    class Meta:
        model = Booking
        fields = ['account',]


class BookBookingForm(forms.ModelForm):
    accounts = Account.objects.filter().order_by('costcenter', 'name')
    user = User.objects.filter()
    description = forms.CharField(label='Beschreibung')
    planned_amount = forms.IntegerField(label='Erwarteter Betrag (ganze Euro)')
    justification = forms.CharField(label='Begründung', required=False)
    account = forms.ModelChoiceField(queryset=accounts, label='Buchungskonto')
    contact = forms.ModelChoiceField(queryset=user, label='Kontakt')
    invoice_date = forms.DateField(label='Rechnungsdatum')
    invoice_number = forms.CharField(label='Rechnungsnummer')
    firma = forms.CharField(label='Firma')
    amount = forms.DecimalField(max_digits=9, decimal_places=2, label='Betrag')
    submission_date = forms.DateField(label='Bearbeitungsdatum')
    payout_number = forms.IntegerField(label='Auszahlungsnummer')
    booking_date = forms.DateField(label='Buchungsdatum')
    maturity = forms.DateField(label='Fälligkeit')
    upload = forms.FileField(label='Scan der Rechnung', required=False)
    status = forms.ChoiceField(choices=status_choices, label='Status')

    layout = Layout(Fieldset("Allgemeines",
                             Row('description', 'justification', 'contact'),
                             Row('account', 'status', 'planned_amount')
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
    name = forms.CharField(max_length=30, label='Kostenstelle')
    year = forms.ChoiceField(choices=YEARS, label='Jahr')

    layout = Layout(Row('name', 'year'))

    class Meta:
        model = Costcenter
        fields = ['id', 'name', 'year']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['id', 'name', 'costcenter', 'income', 'budget']

