# Generated by Django 3.2.8 on 2021-11-02 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_public_favicon'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Place of birth'),
        ),
    ]
