from django.db import models
from django.contrib.auth.models import User

# TODO: Make dynamic
YEARLIST = [(2020, '2020'),
            (2021, '2021'),
            (2022, '2022'),
            (2023, '2023')]


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
    Status(name='bestellt', style_class='darkyellow'),
    Status(name='eingereicht', style_class='blue'),
    Status(name='bezahlt', style_class='green'),
]

status_choices = [(x, val.name) for x, val in enumerate(status_list)]


class Costcenter(models.Model):
    # Kostenstellen z.B. Schulträger-konsumtiv, Schulträger-investiv, Elternverein, ...
    name = models.CharField(max_length=30)
    year = models.IntegerField(default=2019, choices=YEARLIST, verbose_name="Jahr")

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ('manage_costcenter', 'Can manage costcenter'),
        ]


class Account(models.Model):
    # Buchungskonten, z.B. Fachschaften, Sekretariat, Schulleiter, Kopieren, Tafelnutzung
    name = models.CharField(max_length=20, default='')
    costcenter = models.ForeignKey(to=Costcenter, on_delete=models.CASCADE, default='')
    income = models.BooleanField(default=False)  # True, wenn es sich um ein Einnahmekonto handelt
    budget = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rest = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return "{}: {}".format(self.costcenter, self.name)

    class Meta:
        permissions = [
            ('manage_account', 'Can manage account'),
        ]


class Booking(models.Model):
    account = models.ForeignKey(to=Account, on_delete=models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(to=User, related_name='bookings', on_delete=models.SET_NULL
                                , verbose_name="Erstellt von", blank=True, null=True)
    invoice_date = models.DateField(default='2000-12-31')
    invoice_number = models.CharField(max_length=20, default='0')
    firma = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    planned_amount = models.IntegerField()
    submission_date = models.DateField(default='2000-12-31')
    justification = models.CharField(max_length=2000, blank=True, null=True)
    payout_number = models.IntegerField(default=0)
    booking_date = models.DateField(default='2000-12-31')
    maturity = models.DateField(default='2000-12-31')
    upload = models.FileField(upload_to='uploads/fibu/%Y/', default=None, blank=True, null=True)
    status = models.IntegerField(default=0, choices=status_choices, verbose_name="Status")

    def get_status(self):
        return status_list[self.status]

    class Meta:
        permissions = [
            ('manage_booking', 'Can manage bookings'),
            ('request_booking', 'Can request a booking'),
        ]
