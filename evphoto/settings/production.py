from .base import *

# Note that when debug is turned off in production, Django will not handle
# static files
DEBUG = False

_hosts = os.environ.get('EVPHOTO_ALLOWED_HOSTS')

ALLOWED_HOSTS.extend(_hosts.split(','))

SECRET_KEY = os.environ['EVPHOTO_SECRET_KEY']

MIDDLEWARE.remove('corsheaders.middleware.CorsMiddleware')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['EVPHOTO_DB_NAME'],
        'USER': os.environ['EVPHOTO_DB_USER'],
        'PASSWORD': os.environ['EVPHOTO_DB_PASSWORD'],
        'HOST': os.environ['EVPHOTO_DB_HOST'],
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa
    },
]

# Django rest framework
# REST_FRAMEWORK.update({
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'users.backends.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ]
# })



