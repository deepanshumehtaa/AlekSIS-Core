from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from material import Layout, Row, Fieldset
from .models import YEARLIST, Booking, Costcenter, Account


class EditBookingForm(forms.ModelForm):
    description = forms.CharField(label='Beschreibung - Was soll gekauft werden?')
    planned_amount = forms.IntegerField(label='Erwarteter Betrag - Welcher Betrag ist erforderlich (in Euro ohne Komma)?')
    justification = forms.CharField(label='Begründung - Begründe ggf. deinen Antrag.', required=False)

    layout = Layout(Row('description', 'planned_amount'), Row('justification'))

    class Meta:
        model = Booking
        fields = ('id', 'description', 'planned_amount', 'justification')


class CheckBookingForm(forms.ModelForm):
    costcenterlist = Costcenter.objects.filter()
    costcenter = forms.ModelChoiceField(queryset=costcenterlist, label='Kostenstelle')

    class Meta:
        model = Costcenter
        fields = ('id', 'name')


class EditCostcenterForm(forms.ModelForm):
     name = forms.CharField(max_length=30, label='Kostenstelle')
     year = forms.ChoiceField(choices=YEARLIST, label='Jahr')

     layout = Layout(Row('name','year'))

     class Meta:
         model = Costcenter
         fields = ('id', 'name', 'year')


class EditAccountForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='Buchungskonto')
    costcenterlist = Costcenter.objects.filter()
    costcenter = forms.ModelChoiceField(queryset=costcenterlist, label='Kostenstelle')
    budget = forms.IntegerField(label='Budget')

    layout = Layout(Row('name', 'costcenter', 'budget'))

    class Meta:
        model = Account
        fields = ('id', 'name', 'costcenter', 'budget')


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


