import os

_prod = os.environ.get('EVPHOTO_PROD', False)

if _prod:
    from .production import *
else:
    from .development import *
