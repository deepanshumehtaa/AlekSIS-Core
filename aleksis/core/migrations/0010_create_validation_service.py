from django.db import migrations


def create_validation_service(apps, schema_editor):
    apps.get_model('otp_yubikey', 'ValidationService').objects.update_or_create(
        name='default', defaults={'use_ssl': True, 'param_sl': '', 'param_timeout': ''}
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_dashboard_widget'),
        ('otp_yubikey', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_validation_service)
    ]

