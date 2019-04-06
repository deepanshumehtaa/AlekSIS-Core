from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from material import Layout, Row, Fieldset
from .models import Booking, CostCenter

class AddCostCenterForm(forms.ModelForm):
    cost_center = forms.CharField(max_length=30, label='Kostenstelle')

class AcquisitionForm(forms.ModelForm):
    # Cost_center choices
    def getCostCenter():
        ''' Find all cost center'''
        cost_center = CostCenter.objects.values_list('name')
        return cost_center
    cost_center     = forms.ModelChoiceField(getCostCenter())
    #invoice_date    = models.DateField()
    #invoice_number  = models.CharField(max_length=20)
    #firma           = models.CharField(max_length=30)
    description     = models.CharField(max_length=50)
    #amount          = models.DecimalField(max_digits=10, decimal_places=2)
    planned_amount  = models.IntegerField()
    #submission_date = models.DateField()
    #payout_number   = models.IntegerField()
    #booking_date    = models.DateField()
    #maturity        = models.DateField()
    #account         = models.ForeignKey(to=Account.number, on_delete=models.CASCADE)
    #budget          = models.ForeignKey(to=Budget.name, on_delete=models.CASCADE)
    #upload          = models.FileField(upload_to='uploads/fibu/%Y/')


    # layout = Layout(Fieldset('Von',
    #                          Row('from_date', 'from_lesson', 'from_time'),
    #                          ),
    #                 Fieldset('Bis',
    #                          Row('to_date', 'to_lesson', 'to_time'),
    #                          ),
    #                 Fieldset('Grund / Vorhaben',
    #                          'description'),
    #                 )

    class Meta:
        model = Booking
        fields = ('cost_center', 'description', 'planned_amount')