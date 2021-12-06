# Generated by Django 3.2.9 on 2021-12-05 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_person_place_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthapplication',
            name='allowed_groups',
            field=models.ManyToManyField(blank=True, related_name='oauth_apps', to='core.Group', verbose_name='Allowed groups'),
        ),
    ]
