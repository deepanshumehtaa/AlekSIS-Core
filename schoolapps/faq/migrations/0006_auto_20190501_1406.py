# Generated by Django 2.2 on 2019-05-01 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0005_auto_20190429_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faqquestion',
            name='answered',
        ),
        migrations.AddField(
            model_name='faqquestion',
            name='show',
            field=models.BooleanField(default=False, verbose_name='Veröffentlicht'),
        ),
    ]
