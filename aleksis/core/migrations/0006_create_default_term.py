from django.db import migrations, models


def mark_current_term(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    SchoolTerm = apps.get_model('core', 'SchoolTerm')  # noqa

    if not SchoolTerm.objects.filter(current=True).exists():
        SchoolTerm.objects.using(db_alias).latest('date_start').update(current=True)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_verbose_names_meta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='current_term',
        ),
        migrations.AddField(
            model_name='schoolterm',
            name='current',
            field=models.NullBooleanField(default=None, unique=True),
        ),
    ]

