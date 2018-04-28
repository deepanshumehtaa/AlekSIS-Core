# EMAIL
EMAIL_HOST = 'postoffice.katharineum.de'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'infoplan@katharineum.de'
EMAIL_HOST_PASSWORD = 'grummelPASS1531'

# SECRET KEY
SECRET_KEY = '_89lg!56$d^sf$22cz1ja_f)x9z(nc*y-x*@j4!!vzmlgi*53u'

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schoolapps',
        'USER': 'www-data',
        'PASSWORD': 'grummelPASS1531',
        'HOST': '',
        'PORT': ''
    },
    'untis': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'untiskath',
        'USER': 'www-data',
        'PASSWORD': 'grummelPASS1531',
        'HOST': '',
        'PORT': ''
    }
}
