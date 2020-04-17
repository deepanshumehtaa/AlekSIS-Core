# Generated by Django 3.0.5 on 2020-04-17 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_de', models.CharField(db_index=True, max_length=63, verbose_name='Title')),
                ('title_en', models.CharField(blank=True, db_index=True, max_length=63, verbose_name='Title')),
                ('summary_de', models.TextField(verbose_name='Summary')),
                ('summary_en', models.TextField(blank=True, verbose_name='Summary')),
                ('content_de', models.TextField(verbose_name='Terms and Conditions')),
                ('content_en', models.TextField(blank=True, verbose_name='Terms and Conditions')),
                ('date_created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Date and Time of Document Creation')),
                ('group_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='terms', to='auth.Group', verbose_name='Related Group')),
            ],
            options={
                'verbose_name': 'Terms & Conditions',
                'verbose_name_plural': 'Terms & Conditions',
            },
        ),
        migrations.CreateModel(
            name='NotaryPublic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_signed', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Date and Time of User Consent')),
                ('term_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users_agreed', to='letsagree.Term', verbose_name='Terms and Conditions')),
                ('user_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='agreed_terms', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Notary Public',
                'verbose_name_plural': 'Notary Public',
                'unique_together': {('user_key', 'term_key')},
            },
        ),
    ]
