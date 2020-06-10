# Generated by Django 3.0.7 on 2020-06-10 19:54

import aleksis.core.mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuth2Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Name of token')),
                ('token_type', models.CharField(max_length=40, verbose_name='Type of token')),
                ('access_token', models.CharField(max_length=200, verbose_name='Access token')),
                ('refresh_token', models.CharField(max_length=200, verbose_name='Refresh token')),
                ('expires_at', models.PositiveIntegerField(verbose_name='Expires at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            bases=(models.Model, aleksis.core.mixins.PureDjangoModel),
        ),
    ]
