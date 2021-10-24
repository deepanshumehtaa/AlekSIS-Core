# Generated by Django 3.2.8 on 2021-10-24 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_pdf_file_person_optional'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='globalpermissions',
            options={'default_permissions': (), 'managed': False, 'permissions': (('view_system_status', 'Can view system status'), ('manage_data', 'Can manage data'), ('impersonate', 'Can impersonate'), ('search', 'Can use search'), ('change_site_preferences', 'Can change site preferences'), ('change_person_preferences', 'Can change person preferences'), ('change_group_preferences', 'Can change group preferences'), ('add_oauth_applications', 'Can add oauth applications'), ('list_oauth_applications', 'Can list oauth applications'), ('view_oauth_applications', 'Can view oauth applications'), ('update_oauth_applications', 'Can update oauth applications'), ('delete_oauth_applications', 'Can delete oauth applications'), ('test_pdf', 'Can test PDF generation'))},
        ),
    ]
