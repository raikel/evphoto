import logging
from os import path
from tempfile import NamedTemporaryFile
from time import sleep
from uuid import uuid4

import cv2 as cv
import numpy as np
import requests
from django.conf import settings

_IMAGE_URL = 'https://fake-img-endpoint.vercel.app/api/image'
_TIMEOUT = 22
_MAX_RETRIES = 5
_ERROR_WAIT = 1

_logger = logging.getLogger(__name__)


_COLORMAPS = (
    cv.COLORMAP_HOT,
    cv.COLORMAP_JET,
    cv.COLORMAP_COOL,
    cv.COLORMAP_HSV,
    cv.COLORMAP_SPRING,
    cv.COLORMAP_BONE,
)


class TakePhotoError(Exception):
    pass


def _take_photo(colormap: int = None):
    try:
        req = requests.get(_IMAGE_URL, timeout=_TIMEOUT)
        with NamedTemporaryFile('wb') as tmp:
            tmp.write(req.content)
            if path.exists(tmp.name) and path.isfile(tmp.name):
                img: np.ndarray = cv.imread(tmp.name, cv.IMREAD_GRAYSCALE)
                if img is not None:
                    image_name = f'image_{uuid4()}.jpg'
                    image_path = path.join(settings.MEDIA_ROOT, image_name)

                    if colormap in _COLORMAPS:
                        min_val = img.min()  # noqa
                        max_val = img.max()  # noqa
                        if max_val > min_val:
                            img = np.uint8(
                                255.0 * (img - min_val) / (max_val - min_val)
                            )
                            img = cv.applyColorMap(img, colormap)
                    else:
                        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

                    cv.imwrite(image_path, img)

                    if path.exists(image_path) and path.isfile(image_path):
                        h, w = img.shape[:2]
                        center_value = img[int(h / 2), int(w / 2)][0]
                        temperature = (center_value >> 2) * 0.04 - 273.15
                        return image_name, temperature
                    else:
                        raise TakePhotoError('error writing retrieved image')
                else:
                    raise TakePhotoError('unable to read retrieved image')
            else:
                raise TakePhotoError('error writing retrieved image')
    except Exception as exc:
        raise TakePhotoError('unable to retrieve image: ' + str(exc))


def take_photo(colormap: int = -1):
    _exc = None
    error = False
    for _ in range(_MAX_RETRIES):
        try:
            return _take_photo(colormap) + (error,)
        except TakePhotoError as exc:
            sleep(_ERROR_WAIT)
            error = True
            _exc = exc

    if _exc is not None:
        raise _exc
