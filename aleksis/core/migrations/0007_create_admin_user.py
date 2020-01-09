from django.contrib.auth import get_user_model
from django.db import migrations


def create_superuser(apps, schema_editor):
    User = get_user_model()

    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='root@example.com',
            password='admin'
        ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_create_default_term'),
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]

