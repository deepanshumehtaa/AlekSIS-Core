# Generated by Django 3.1.4 on 2021-02-19 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_default_dashboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardwidget',
            name='broken',
            field=models.BooleanField(default=False, verbose_name='Widget is broken'),
        ),
    ]
