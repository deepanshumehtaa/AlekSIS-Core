# Generated by Django 2.0 on 2017-12-19 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('teachers', '0002_teacher_shortcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='title',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
