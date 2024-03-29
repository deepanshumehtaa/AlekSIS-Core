# Generated by Django 3.2.4 on 2021-07-24 13:14
import os

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_drop_persons_accounts_perm'),
        ('favicon', '0004_faviconimg_favicon_size_rel_unique'),
    ]

    def _migrate_favicons(apps, schema_editor):
        FaviconImg = apps.get_model('favicon', "FaviconImg")
        for favicon_img in FaviconImg.objects.all():
            old_name = favicon_img.faviconImage.name
            new_name = os.path.join("public", old_name)
            storage = favicon_img.faviconImage.storage
            if storage.exists(old_name):
                storage.save(new_name, favicon_img.faviconImage.file)
                favicon_img.faviconImage.name = new_name
                favicon_img.save()

    operations = [
        migrations.RunPython(_migrate_favicons)
    ]
