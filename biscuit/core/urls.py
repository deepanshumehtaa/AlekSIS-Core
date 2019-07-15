from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('persons', views.persons, name='persons'),
    path('', views.index, name='index'),
]

# Serve javascript-common if in development
if settings.DEBUG:
    urlpatterns += static('/javascript/',
                          document_root='/usr/share/javascript/')

# Automatically mount URLs from all installed BiscuIT apps
for app_config in apps.app_configs.values():
    if not app_config.name.startswith('biscuit.apps.'):
        continue

    urlpatterns.append(path('app/%s/' % app_config.label,
                            include('%s.urls' % app_config.name)))
