from django.db import migrations

from otp_yubikey.models import ValidationService

def create_validation_service(apps, schema_editor):
    ValidationService.objects.create(
        name='default', use_ssl=True
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_school_logo'),
    ]

    operations = [
        migrations.RunPython(create_validation_service),
    ]
