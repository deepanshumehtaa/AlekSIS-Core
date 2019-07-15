import os

from local_settings import load_and_check_settings, LocalSetting, SecretSetting

from .util import get_app_packages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SecretSetting()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = LocalSetting(default=False)

ALLOWED_HOSTS = LocalSetting(default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easyaudit',
    'bootstrap4',
    'fa',
    'django_any_js',
    'django_tables2',
    'menu',
    'phonenumber_field',
    'biscuit.core'
]

INSTALLED_APPS += get_app_packages()

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'ENGINE': LocalSetting(default='django.db.backends.sqlite3'),
        'NAME': LocalSetting(default='{{ BASE_DIR }}/db.sqlite3'),
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

LANGUAGE_CODE = LocalSetting(default='de-de')

TIME_ZONE = LocalSetting(default='Europe/Berlin')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'core.Person'

MENU_SELECT_PARENTS = True

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

STATIC_ROOT = LocalSetting()
MEDIA_ROOT = LocalSetting()

FONT_AWESOME = {'url': LocalSetting(
    default="/javascript/font-awesome/css/font-awesome.min.css")}

BOOTSTRAP4 = {
    "css_url": LocalSetting(default="/javascript/bootstrap4/css/bootstrap.min.css"),
    "javascript_url": LocalSetting(default="/javascript/bootstrap4/js/bootstrap.min.js"),
    "jquery_url": LocalSetting(default="/javascript/jquery/jquery.min.js"),
    "popper_url": LocalSetting(default="/javascript/popper.js/popper.min.js"),
    "include_jquery": True
}

ANY_JS = {
    'DataTables': {
        'js_url': LocalSetting(default='/javascript/jquery-datatables/jquery.dataTables.min.js')
    },
    'DataTables-Bootstrap4': {
        'css_url': LocalSetting(default="/javascript/jquery-datatables/css/dataTables.bootstrap4.min.css"),
        'js_url': LocalSetting(default="/javascript/jquery-datatables/dataTables.bootstrap4.min.js")
    }
}


_settings = load_and_check_settings(globals())
globals().update(_settings)
