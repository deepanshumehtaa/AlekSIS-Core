# Generated by Django 2.0 on 2017-12-20 19:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('todos', '0015_auto_20171220_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 20, 19, 42, 9, 373482, tzinfo=utc)),
        ),
    ]
