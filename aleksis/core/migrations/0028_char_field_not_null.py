# Generated by Django 3.2.10 on 2021-12-15 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_person_place_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthapplication',
            name='authorization_grant_type',
            field=models.CharField(blank=True, choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials'), ('openid-hybrid', 'OpenID connect hybrid')], default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='place_of_birth',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Place of birth'),
            preserve_default=False,
        ),
    ]
