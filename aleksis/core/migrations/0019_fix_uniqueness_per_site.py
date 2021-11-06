# Generated by Django 3.2.3 on 2021-05-21 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_pdffile_html_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custommenu',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Menu ID'),
        ),
        migrations.AlterField(
            model_name='person',
            name='short_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Short name'),
        ),
        migrations.AlterField(
            model_name='schoolterm',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AddConstraint(
            model_name='additionalfield',
            constraint=models.UniqueConstraint(fields=('site_id', 'title'), name='unique_title_per_site'),
        ),
        migrations.AddConstraint(
            model_name='custommenu',
            constraint=models.UniqueConstraint(fields=('site_id', 'name'), name='unique_menu_name_per_site'),
        ),
        migrations.AddConstraint(
            model_name='custommenuitem',
            constraint=models.UniqueConstraint(fields=('menu', 'name'), name='unique_name_per_menu'),
        ),
        migrations.AddConstraint(
            model_name='grouptype',
            constraint=models.UniqueConstraint(fields=('site_id', 'name'), name='unique_group_type_name_per_site'),
        ),
        migrations.AddConstraint(
            model_name='person',
            constraint=models.UniqueConstraint(fields=('site_id', 'short_name'), name='unique_short_name_per_site'),
        ),
        migrations.AddConstraint(
            model_name='schoolterm',
            constraint=models.UniqueConstraint(fields=('site_id', 'name'), name='unique_school_term_name_per_site'),
        ),
        migrations.AddConstraint(
            model_name='schoolterm',
            constraint=models.UniqueConstraint(fields=('site_id', 'date_start', 'date_end'), name='unique_school_term_dates_per_site'),
        ),
    ]
