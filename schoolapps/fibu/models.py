from django.db import models
from django.contrib.auth.models import User

SCHOOLYEARLIST = ['2019/2020','2020/2021','2021/2022','2022/2023','2023/2024']

class Status:
    def __init__(self, name, style_class):
        self.name = name
        self.style_class = style_class

    def __str__(self):
        return self.name


status_list = [
    Status(name='beantragt', style_class='red'),
    Status(name='bewilligt', style_class='orange'),
    Status(name='abgelehnt', style_class='black'),
    Status(name='bestellt', style_class='yellow'),
    Status(name='bezahlt', style_class='green'),
]

status_choices = [(x, val.name) for x, val in enumerate(status_list)]



class Costcenter(models.Model):
    # Kostenstellen z.B. Schoolträger-konsumtiv, Schulträger-investiv, Elternberein, ...
    name = models.CharField(max_length=20)
    schoolyear = models.CharField(max_length=20)
    class Meta:
        permissions = (
            ('edit_costcenter', 'Can edit cost center'),
        )

class Account(models.Model):
    # Buchungskonten, z.B. Fachschaften, Sekretariat, Schulleiter, Kopieren, Tafelnutzung
    name = models.CharField(max_length=20)
    costcenter = models.ForeignKey(to=Costcenter, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    class Meta:
        permissions = (
            ('edit_account', 'Can edit account'),
        )

class Booking(models.Model):
    account         = models.ForeignKey(to=Account, on_delete=models.SET_NULL, blank=True, null=True)
    contact         = models.ForeignKey(to=User, related_name='bookings', on_delete=models.SET_NULL
                                   , verbose_name="Erstellt von", blank=True, null=True)
#    invoice_date    = models.DateField()
#    invoice_number  = models.CharField(max_length=20)
#    firma           = models.CharField(max_length=30)
    description     = models.CharField(max_length=50)
#    amount          = models.DecimalField(max_digits=9, decimal_places=2)
    planned_amount  = models.IntegerField()
    submission_date = models.DateField(default='2019-01-01')
    justification   = models.CharField(max_length=2000, blank=True, null=True)
#    payout_number   = models.IntegerField()
#    booking_date    = models.DateField()
#    maturity        = models.DateField()
#    upload          = models.FileField(upload_to='uploads/fibu/%Y/')
    status          = models.IntegerField(default=0, choices=status_choices, verbose_name="Status")


    def getStatus(self):
        return status_list[self.status]


    class Meta:
        permissions = (
            ('edit_booking', 'Can edit bookings'),
            ('apply_acquisition', 'Can apply an acquisition'),
        )