from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path

import debug_toolbar
from two_factor.urls import urlpatterns as tf_urls

from . import views

urlpatterns = [
    path('data_management/', views.data_management, name='data_management'),
    path('status/', views.system_status, name='system_status'),
    path('school_management', views.school_management, name='school_management'),
    path('school/information/edit', views.edit_school, name='edit_school_information'),
    path('school/term/edit', views.edit_schoolterm, name='edit_school_term'),
    path('', include(tf_urls)),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('persons', views.persons, name='persons'),
    path('persons/accounts', views.persons_accounts, name='persons_accounts'),
    path('person', views.person, name='person'),
    path('person/<int:id_>', views.person,
         {'template': 'full'}, name='person_by_id'),
    path('person/<int:id_>/card', views.person,
         {'template': 'card'}, name='person_by_id_card'),
    path('person/<int:id_>/edit', views.edit_person, name='edit_person_by_id'),
    path('groups', views.groups, name='groups'),
    path('group/create', views.edit_group, name='create_group'),
    path('group/<int:id_>', views.group,
         {'template': 'full'}, name='group_by_id'),
    path('group/<int:id_>/edit', views.edit_group, name='edit_group_by_id'),
    path('', views.index, name='index'),
    path('maintenance-mode/', include('maintenance_mode.urls')),
    path('contact/', include('contact_form.urls')),
    path('impersonate/', include('impersonate.urls')),
    path('__i18n__/', include('django.conf.urls.i18n')),
    path('select2/', include('django_select2.urls'))
]

# Add URLs for optional features
if hasattr(settings, 'TWILIO_ACCOUNT_SID'):
    from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls  # noqa
    urlpatterns += [path('', include(tf_twilio_urls))]

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
