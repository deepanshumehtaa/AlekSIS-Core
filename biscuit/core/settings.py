from glob import glob
import os
import sys

from django.utils.translation import ugettext_lazy as _

from dynaconf import LazySettings
from easy_thumbnails.conf import Settings as thumbnail_settings

from .util.core_helpers import get_app_packages

ENVVAR_PREFIX_FOR_DYNACONF = 'BISCUIT'
DIRS_FOR_DYNACONF = ['/etc/biscuit']

SETTINGS_FILE_FOR_DYNACONF = []
for directory in DIRS_FOR_DYNACONF:
    SETTINGS_FILE_FOR_DYNACONF += glob(os.path.join(directory, '*.ini'))
    SETTINGS_FILE_FOR_DYNACONF += glob(os.path.join(directory, '*.yaml'))
    SETTINGS_FILE_FOR_DYNACONF += glob(os.path.join(directory, '*.toml'))

_settings = LazySettings(
    ENVVAR_PREFIX_FOR_DYNACONF=ENVVAR_PREFIX_FOR_DYNACONF,
    SETTINGS_FILE_FOR_DYNACONF=SETTINGS_FILE_FOR_DYNACONF
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _settings.get('secret_key', 'DoNotUseInProduction')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _settings.get('debug.enabled', False)
INTERNAL_IPS = _settings.get('debug.internal_ips', [])
DEBUG_TOOLBAR_CONFIG = {
    'RENDER_PANELS': True,
    'SHOW_COLLAPSED': True
}

ALLOWED_HOSTS = _settings.get('http.allowed_hosts', [])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_global_request',
    'settings_context_processor',
    'sass_processor',
    'easyaudit',
    'bootstrap4',
    'fa',
    'django_any_js',
    'django_tables2',
    'easy_thumbnails',
    'image_cropping',
    'maintenance_mode',
    'menu_generator',
    'phonenumber_field',
    'debug_toolbar',
    'biscuit.core'
]

INSTALLED_APPS += get_app_packages()

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder'
]

SASS_PROCESSOR_AUTO_INCLUDE = False
SASS_PROCESSOR_CUSTOM_FUNCTIONS = {
    'get-colour': 'biscuit.core.util.sass_helpers.get_colour',
}
SASS_PROCESSOR_INCLUDE_DIRS = [
    _settings.get('bootstrap.sass_path', '/usr/share/sass/bootstrap')
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_global_request.middleware.GlobalRequestMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'biscuit.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'maintenance_mode.context_processors.maintenance_mode',
                'settings_context_processor.context_processors.settings'
            ],
        },
    },
]

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

# Already included by base template / Bootstrap
IMAGE_CROPPING_JQUERY_URL = None

WSGI_APPLICATION = 'biscuit.core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': _settings.get('database.engine', 'django.db.backends.sqlite3'),
        'NAME': _settings.get('database.name', 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication backends are dynamically populated
AUTHENTICATION_BACKENDS = []

if _settings.get('ldap.uri', None):
    # LDAP dependencies are not necessarily installed, so import them here
    import ldap  # noqa
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType  # noqa

    # Enable Django's integration to LDAP
    AUTHENTICATION_BACKENDS.append('django_auth_ldap.backend.LDAPBackend')

    AUTH_LDAP_SERVER_URI = _settings.get('ldap.uri')

    # Optional: non-anonymous bind
    if _settings.get('ldap.bind.dn', None):
        AUTH_LDAP_BIND_DN = _settings.get('ldap.bind.dn')
        AUTH_LDAP_BIND_PASSWORD = _settings.get('ldap.bind.password')

    # Search attributes to find users by username
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        _settings.get('ldap.users.base'),
        ldap.SCOPE_SUBTREE,
        _settings.get('ldap.users.filter', '(uid=%(user)s)')
    )

    # Mapping of LDAP attributes to Django model fields
    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': _settings.get('ldap.map.first_name', 'givenName'),
        'last_name': _settings.get('ldap.map.first_name', 'sn'),
        'email': _settings.get('ldap.map.email', 'mail'),
    }

# Add ModelBckend last so all other backends get a chance
# to verify passwords first
AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.ModelBackend')

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]
LANGUAGE_CODE = _settings.get('l10n.lang', 'en')
TIME_ZONE = _settings.get('l10n.tz', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = _settings.get('static.url', '/static/')
MEDIA_URL = _settings.get('media.url', '/media/')

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

STATIC_ROOT = _settings.get('static.root', os.path.join(BASE_DIR, 'static'))
MEDIA_ROOT = _settings.get('media.root', os.path.join(BASE_DIR, 'media'))

FONT_AWESOME = {'url': _settings.get(
    'bootstrap.fa_url', '/javascript/font-awesome/css/font-awesome.min.css')}

BOOTSTRAP4 = {
    'css_url': _settings.get('bootstrap.css_url', '/javascript/bootstrap4/css/bootstrap.min.css'),
    'javascript_url': _settings.get('bootstrap.js_url', '/javascript/bootstrap4/js/bootstrap.min.js'),
    'jquery_url': _settings.get('bootstrap.jquery_url', '/javascript/jquery/jquery.min.js'),
    'popper_url': _settings.get('bootstrap.popper_url', '/javascript/popper.js/umd/popper.min.js'),
    'include_jquery': True,
    'include_popper': True,
    'javascript_in_head': True
}

DATATABLES_BASE = _settings.get(
    'bootstrap.datatables_base', '/javascript/jquery-datatables')

ANY_JS = {
    'DataTables': {
        'js_url': DATATABLES_BASE + '/jquery.dataTables.min.js'
    },
    'DataTables-Bootstrap4': {
        'css_url': DATATABLES_BASE + '/css/dataTables.bootstrap4.min.css',
        'js_url': DATATABLES_BASE + '/dataTables.bootstrap4.min.js'
    }
}

COLOUR_PRIMARY = _settings.get('theme.colours.primary', '#007bff')
COLOUR_SECONDARY = _settings.get('theme.colours.secondary', '#6c757d')
COLOUR_SUCCESS = _settings.get('theme.colours.success', '#28a745')
COLOUR_INFO = _settings.get('theme.colours.info', '#17a2b8')
COLOUR_WARNING = _settings.get('theme.colours.warning', '#ffc107')
COLOUR_DANGER = _settings.get('theme.colours.danger', '#dc3545')
COLOUR_LIGHT = _settings.get('theme.colours.light', '#f8f9fa')
COLOUR_DARK = _settings.get('theme.colours.dark', '#343a40')

ADMINS = _settings.get('contact.admins', [])
SERVER_EMAIL = _settings.get('contact.from', 'root@localhost')

TEMPLATE_VISIBLE_SETTINGS = ['ADMINS']

MAINTENANCE_MODE = _settings.get('maintenance.enabled', None)
MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = _settings.get(
    'maintenance.ignore_ips', _settings.get('debug.internal_ips', []))
MAINTENANCE_MODE_GET_CLIENT_IP_ADDRESS = 'ipware.ip.get_ip'
MAINTENANCE_MODE_IGNORE_SUPERUSER = True

_settings.populate_obj(sys.modules[__name__])
