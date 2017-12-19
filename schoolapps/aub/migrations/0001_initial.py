# Generated by Django 2.0 on 2017-12-19 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('teacher_id', models.IntegerField(
                    choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11),
                             (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
                             (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29),
                             (30, 30), (31, 31)])),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2017, 12, 19, 19, 22, 15, 235748))),
            ],
        ),
    ]
