from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# Enable CORS for all domains
CORS_ORIGIN_ALLOW_ALL = True

