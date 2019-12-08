# Generated by Django 2.2.5 on 2019-09-14 12:55

import biscuit.core.util.core_helpers
from django.db import migrations, models
import django.db.models.deletion
from django.utils.translation import ugettext_lazy as _


def create_default_terms(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    School = apps.get_model('core', 'School')  # noqa
    SchoolTerm = apps.get_model('core', 'SchoolTerm')  # noqa

    for school in School.objects.using(db_alias).all():
        term = SchoolTerm.objects.using(db_alias).create(school=school, caption=_('Default term'))
        school.current_term = term
        school.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=30, verbose_name='Visible caption of the term')),
                ('date_start', models.DateField(null=True, verbose_name='Effective start date of term')),
                ('date_end', models.DateField(null=True, verbose_name='Effective end date of term')),
                ('school', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.School')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='school',
            name='current_term',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.SchoolTerm', null=True),
            preserve_default=False,
        ),
        migrations.RunPython(create_default_terms),
        migrations.AlterField(
            model_name='school',
            name='current_term',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.SchoolTerm'),
            preserve_default=False,
        ),
    ]
