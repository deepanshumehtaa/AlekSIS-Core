from glob import glob
import os
import sys

from django.utils.translation import ugettext_lazy as _

from dynaconf import LazySettings

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
DEBUG = _settings.get('debug', False)

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
    'sass_processor',
    'easyaudit',
    'bootstrap4',
    'fa',
    'django_any_js',
    'django_tables2',
    'menu_generator',
    'phonenumber_field',
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
            ],
        },
    },
]

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
    'include_popper': True
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

ADMINS = _settings.get('admins', [])

_settings.populate_obj(sys.modules[__name__])
