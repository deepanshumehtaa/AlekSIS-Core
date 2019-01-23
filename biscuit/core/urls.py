from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]

# Automatically mount URLs from all installed BiscuIT apps
for app_config in apps.app_configs.values():
    if not app_config.name.startswith('biscuit.apps.'):
        continue

    urlpatterns.append(path('%s/' % app_config.label, include('%s.urls' % app_config.name)))
