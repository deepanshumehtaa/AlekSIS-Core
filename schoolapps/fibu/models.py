from django.db import models

class CostCenter(models.Model):
    name = models.CharField(max_length=20, primary_key=True, unique=True)

class Account(models.Model):
    number = models.IntegerField(primary_key=True, unique=True)

class Budget(models.Model):
    name = models.CharField(max_length=30, primary_key=True, unique=True)

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
