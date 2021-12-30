# Generated by Django 3.2.10 on 2021-12-30 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_user_attributes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='globalpermissions',
            options={'default_permissions': (), 'managed': False, 'permissions': (('view_system_status', 'Can view system status'), ('manage_data', 'Can manage data'), ('impersonate', 'Can impersonate'), ('search', 'Can use search'), ('change_site_preferences', 'Can change site preferences'), ('change_person_preferences', 'Can change person preferences'), ('change_group_preferences', 'Can change group preferences'), ('test_pdf', 'Can test PDF generation'))},
        ),
        migrations.AddField(
            model_name='externallinkwidget',
            name='use_ogp',
            field=models.BooleanField(default=False, verbose_name='Use OpenGraph'),
        ),
        migrations.AlterField(
            model_name='dashboardwidget',
            name='title',
            field=models.CharField(blank=True, max_length=150, verbose_name='Widget Title'),
        ),
        migrations.AlterField(
            model_name='externallinkwidget',
            name='icon_url',
            field=models.URLField(blank=True, verbose_name='Icon URL'),
        ),
        migrations.AlterField(
            model_name='personinvitation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
