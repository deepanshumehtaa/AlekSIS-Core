from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import date

current_year = timezone.now().year
YEARS = [(x, str(x)) for x in range(current_year, current_year + 4)]


class Status:
    def __init__(self, name, style_class):
        self.name = name
        self.style_class = style_class

    def __str__(self):
        return self.name


status_list = [
    Status(name='beantragt', style_class='red'),
    Status(name='abgelehnt', style_class='black'),
    Status(name='bewilligt', style_class='orange'),
    Status(name='bestellt', style_class='yellow darken-1'),
    Status(name='eingereicht', style_class='blue'),
    Status(name='bezahlt', style_class='green'),
]

status_choices = [(x, val.name) for x, val in enumerate(status_list)]


class Costcenter(models.Model):
    # Kostenstellen z.B. Schulträger-konsumtiv, Schulträger-investiv, Elternverein, ...
    name = models.CharField(max_length=30, blank=False, verbose_name="Kostenstelle")
    year = models.IntegerField(default=timezone.now().year, choices=YEARS, blank=False, verbose_name="Jahr")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kostenstelle"
        verbose_name_plural = "Kostenstellen"
        permissions = [
            ('manage_costcenter', 'Can manage costcenter'),
        ]


class Account(models.Model):
    # Buchungskonten, z.B. Fachschaften, Sekretariat, Schulleiter, Kopieren, Tafelnutzung
    name = models.CharField(max_length=20, blank=False, verbose_name="Buchungskonto")
    costcenter = models.ForeignKey(to=Costcenter, on_delete=models.CASCADE, blank=False, verbose_name="Kostenstelle")
    income = models.BooleanField(default=False,
                                 verbose_name="Einnahmekonto")  # True, wenn es sich um ein Einnahmekonto handelt
    budget = models.IntegerField(default=0, verbose_name="Budget")
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rest = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return "{}: {}".format(self.costcenter, self.name)

    class Meta:
        verbose_name = "Buchungskonto"
        verbose_name_plural = "Buchungskonten"
        permissions = [
            ('manage_account', 'Can manage account'),
        ]


class Booking(models.Model):
    account = models.ForeignKey(to=Account, on_delete=models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(to=User, related_name='bookings', on_delete=models.SET_NULL
                                , verbose_name="Erstellt von", blank=True, null=True)
    invoice_date = models.DateField(default=date.today)
    invoice_number = models.CharField(max_length=20, default='0')
    firma = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    planned_amount = models.IntegerField()
    submission_date = models.DateField(default=date.today)
    justification = models.CharField(max_length=2000, blank=True, null=True)
    payout_number = models.IntegerField(default=0)
    booking_date = models.DateField(default=date.today)
    maturity = models.DateField(default=date.today)
    upload = models.FileField(upload_to='uploads/fibu/%Y/', default=None, blank=True, null=True)
    status = models.IntegerField(default=0, choices=status_choices, verbose_name="Status")

    def get_status(self):
        return status_list[self.status]

    def __str__(self):
        return "{} ({})".format(self.description, self.account)

    class Meta:
        verbose_name = "Buchung"
        verbose_name_plural = "Buchungen"
        permissions = [
            ('manage_booking', 'Can manage bookings'),
            ('request_booking', 'Can request a booking'),
            ('check_booking', 'Can check bookings'),
        ]
