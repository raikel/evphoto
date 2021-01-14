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


class TakePhotoError(Exception):
    pass


def _take_photo():
    try:
        req = requests.get(_IMAGE_URL, timeout=_TIMEOUT)
        with NamedTemporaryFile('wb') as tmp:
            tmp.write(req.content)
            if path.exists(tmp.name) and path.isfile(tmp.name):
                image: np.ndarray = cv.imread(tmp.name)
                if image is not None:
                    if image.ndim == 3:
                        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

                    image_name = f'image_{uuid4()}.jpg'
                    image_path = path.join(settings.MEDIA_ROOT, image_name)
                    cv.imwrite(image_path, image)

                    if path.exists(image_path) and path.isfile(image_path):
                        h, w = image.shape[:2]
                        center_value = image[int(h / 2), int(w / 2)]
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


def take_photo():
    _exc = None
    error = False
    for _ in range(_MAX_RETRIES):
        try:
            return _take_photo() + (error,)
        except TakePhotoError as exc:
            sleep(_ERROR_WAIT)
            error = True
            _exc = exc

    if _exc is not None:
        raise _exc
