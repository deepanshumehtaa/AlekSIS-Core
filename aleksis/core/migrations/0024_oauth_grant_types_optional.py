# Generated by Django 3.2.8 on 2021-11-04 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_oauth_application_model'),
        ('oauth2_provider', '0004_auto_20200902_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthapplication',
            name='authorization_grant_type',
            field=models.CharField(blank=True, choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials'), ('openid-hybrid', 'OpenID connect hybrid')], max_length=32, null=True),
        ),
    ]