from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
]

# Automatically mount URLs from all installed BiscuIT apps
for app_config in apps.app_configs:
    if not app.startswith('biscuit.apps.'):
        continue

    urlpatterns += path('%s/' % app_config.label, include('%s.urls' % app_config.name))
