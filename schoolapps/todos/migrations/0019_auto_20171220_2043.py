# Generated by Django 2.0 on 2017-12-20 19:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('todos', '0018_auto_20171220_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
