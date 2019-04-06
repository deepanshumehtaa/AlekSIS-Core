from django.db import models

class CostCenter(models.Model):
    name = models.CharField(max_length=20, primary_key=True, unique=True)
    class Meta:
        permissions = (
            ('edit_costcenter', 'Can edit cost center'),
        )

class Account(models.Model):
    number = models.IntegerField(primary_key=True, unique=True)
    class Meta:
        permissions = (
            ('edit_account', 'Can edit account'),
        )

class Budget(models.Model):
    name = models.CharField(max_length=30, primary_key=True, unique=True)
    class Meta:
        permissions = (
            ('edit_budget', 'Can edit budget'),
        )

class Booking(models.Model):
    cost_center     = models.ForeignKey(to=CostCenter.name, on_delete=models.CASCADE)
    invoice_date    = models.DateField()
    invoice_number  = models.CharField(max_length=20)
    firma           = models.CharField(max_length=30)
    description     = models.CharField(max_length=50)
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    planned_amount  = models.IntegerField()
    submission_date = models.DateField()
    payout_number   = models.IntegerField()
    booking_date    = models.DateField()
    maturity        = models.DateField()
    account         = models.ForeignKey(to=Account.number, on_delete=models.CASCADE)
    budget          = models.ForeignKey(to=Budget.name, on_delete=models.CASCADE)
    upload          = models.FileField(upload_to='uploads/fibu/%Y/')

    class Meta:
        permissions = (
            ('view_booking', 'Can view a list of bookings'),
            ('edit_booking', 'Can edit bookings'),
            ('apply_acquisition', 'Can apply an acquisition'),
        )