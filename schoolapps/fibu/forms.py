from django import forms
from django.contrib.auth.models import User
from material import Layout, Row, Fieldset

from .models import YEARLIST, Booking, Costcenter, Account, status_choices


class BookingForm(forms.ModelForm):
    description = forms.CharField(label='Beschreibung – Was soll angeschafft werden?')
    planned_amount = forms.IntegerField(
        label='Erwarteter Betrag – Welcher Betrag ist erforderlich?', help_text="in Euro, ohne Komma")
    justification = forms.CharField(label='Begründung – Begründe ggf. deinen Antrag.', required=False)

    layout = Layout(Row('description', 'planned_amount'), Row('justification'))

    class Meta:
        model = Booking
        fields = ('id', 'description', 'planned_amount', 'justification')


class CheckBookingForm(forms.ModelForm):
    accounts = Account.objects.filter().order_by('costcenter', 'name')
    account = forms.ModelChoiceField(queryset=accounts, label='Buchungskonto')

    class Meta:
        model = Account
        fields = ('account',)


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
        fields = ('id', 'description', 'planned_amount', 'justification', 'account', 'contact', 'invoice_date',
                  'invoice_number', 'firma', 'amount', 'submission_date', 'payout_number', 'booking_date',
                  'maturity', 'upload', 'status')


class EditCostcenterForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='Kostenstelle')
    year = forms.ChoiceField(choices=YEARLIST, label='Jahr')

    layout = Layout(Row('name', 'year'))

    class Meta:
        model = Costcenter
        fields = ('id', 'name', 'year')


class EditAccountForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='Buchungskonto')
    costcenterlist = Costcenter.objects.filter()
    costcenter = forms.ModelChoiceField(queryset=costcenterlist, label='Kostenstelle')
    income = forms.BooleanField(label='Budget-/Einnanhmekonto', required=False)
    budget = forms.IntegerField(label='Budget')

    layout = Layout(Row('name', 'costcenter', 'income', 'budget'))

    class Meta:
        model = Account
        fields = ('id', 'name', 'costcenter', 'income', 'budget')

#
# class AcquisitionForm(forms.ModelForm):
#     # Cost_center choices
#     def getCostCenter():
#         ''' Find all cost center'''
#         cost_center = CostCenter.objects.values_list('name')
#         return cost_center
#     cost_center     = forms.ModelChoiceField(getCostCenter())
#     #invoice_date    = models.DateField()
#     #invoice_number  = models.CharField(max_length=20)
#     #firma           = models.CharField(max_length=30)
#     description     = models.CharField(max_length=50)
#     #amount          = models.DecimalField(max_digits=10, decimal_places=2)
#     planned_amount  = models.IntegerField()
#     #submission_date = models.DateField()
#     #payout_number   = models.IntegerField()
#     #booking_date    = models.DateField()
#     #maturity        = models.DateField()
#     #account         = models.ForeignKey(to=Account.number, on_delete=models.CASCADE)
#     #budget          = models.ForeignKey(to=Budget.name, on_delete=models.CASCADE)
#     #upload          = models.FileField(upload_to='uploads/fibu/%Y/')
#
#
#     # layout = Layout(Fieldset('Von',
#     #                          Row('from_date', 'from_lesson', 'from_time'),
#     #                          ),
#     #                 Fieldset('Bis',
#     #                          Row('to_date', 'to_lesson', 'to_time'),
#     #                          ),
#     #                 Fieldset('Grund / Vorhaben',
#     #                          'description'),
#     #                 )
#
#     class Meta:
#         model = Booking
#         fields = ('cost_center', 'description', 'planned_amount')
