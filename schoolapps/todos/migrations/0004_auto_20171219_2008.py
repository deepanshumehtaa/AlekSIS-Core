# Generated by Django 2.0 on 2017-12-19 19:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('todos', '0003_auto_20171219_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 19, 20, 8, 50, 896590)),
        ),
    ]
