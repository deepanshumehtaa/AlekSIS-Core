# Generated by Django 2.0.3 on 2018-04-14 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0004_notification_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
