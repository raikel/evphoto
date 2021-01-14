import tempfile

from .development import *

MEDIA_ROOT = os.path.realpath(tempfile.gettempdir())