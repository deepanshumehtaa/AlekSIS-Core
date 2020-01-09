from django.db import migrations, models

from datetime import date

def create_or_mark_current_term(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    SchoolTerm = apps.get_model('core', 'SchoolTerm')  # noqa

    if not SchoolTerm.objects.filter(current=True).exists():
        if SchoolTerm.objects.using(db_alias).latest():
            SchoolTerm.objects.using(db_alias).latest('date_start').update(current=True)
        else:
            SchoolTerm.objects.using(db_alias).create(date_start=date.today(), current=True)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_verbose_names_meta'),
    ]

    operations = [
        migrations.RunPython(create_or_mark_current_term)
    ]
