# Generated by Django 2.2.1 on 2019-05-22 13:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('timetable', '0009_hint_classes_formatted'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebugLogGroup',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
