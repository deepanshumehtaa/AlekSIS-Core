from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import debug_toolbar

from . import views

urlpatterns = [
    path('data_management/', views.data_management, name='data_management'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('persons', views.persons, name='persons'),
    path('persons/accounts', views.persons_accounts, name='persons_accounts'),
    path('person', views.person, name='person'),
    path('person/<int:id_>', views.person,
         {'template': 'full'}, name='person_by_id'),
    path('person/<int:id_>/card', views.person,
         {'template': 'card'}, name='person_by_id_card'),
    path('person/<int:id_>/edit', views.edit_person, name='edit_person_by_id'),
    path('groups', views.groups, name='groups'),
    path('group/<int:id_>', views.group,
         {'template': 'full'}, name='group_by_id'),
    path('group/<int:id_>/edit', views.edit_group, name='edit_group_by_id'),
    path('', views.index, name='index'),
    path('maintenance-mode/', include('maintenance_mode.urls')),
    path('contact/', include('contact_form.urls')),
    path('impersonate/', include('impersonate.urls')),
    path('__i18n__/', include('django.conf.urls.i18n'))
]

# Custom error pages
handler404 = views.error_handler(404)
handler500 = views.error_handler(500)

# Serve javascript-common if in development
if settings.DEBUG:
    urlpatterns += static('/javascript/',
                          document_root='/usr/share/javascript/')
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

# Automatically mount URLs from all installed BiscuIT apps
for app_config in apps.app_configs.values():
    if not app_config.name.startswith('biscuit.apps.'):
        continue

    urlpatterns.append(path('app/%s/' % app_config.label,
                            include('%s.urls' % app_config.name)))
