import json
import os
from uuid import uuid4

import cv2 as cv
from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory

from ..models import Photo
from ..serializers import PhotoSerializer
from ..views import PhotoView

# initialize the APIClient app
client = Client()
factory = APIRequestFactory()


_CURR_DIR = os.path.abspath(os.path.dirname(__file__))
_IMAGE_PATH = os.path.join(_CURR_DIR, 'data/image.jpg')


def _create_image_file():
    image_name = f'image_{uuid4()}.jpg'
    dst_path = os.path.join(settings.MEDIA_ROOT, image_name)
    image = cv.imread(_IMAGE_PATH)
    cv.imwrite(dst_path, image)
    return image_name


class GetAllPhotosTest(TestCase):
    """ Test module for GET all photos API """

    def setUp(self):
        Photo.objects.create(
            session='123456',
            side=Photo.SIDE_LEFT,
            temperature=295.3,
            error=False,
            image=_create_image_file(),
            colormap=Photo.COLORMAP_NONE
        )

    def test_list_photos(self):
        request = factory.get('/api/photos')
        response = PhotoView.as_view({'get': 'list'})(request)  # noqa

        photos = Photo.objects.all()
        serializer = PhotoSerializer(
            photos,
            many=True,
            context={'request': request}
        )

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePhotoTest(TestCase):
    """ Test module for GET single photo API """

    def setUp(self):
        self.photo = Photo.objects.create(
            session='123456',
            side=Photo.SIDE_LEFT,
            temperature=295.3,
            error=False,
            image=_create_image_file(),
            colormap=Photo.COLORMAP_NONE
        )

    def test_get_valid_single_photo(self):
        request = factory.get(f'/api/photos/')
        response = PhotoView.as_view({'get': 'retrieve'})(  # noqa
            request, self.photo.pk
        )

        photo = Photo.objects.get(pk=self.photo.pk)
        serializer = PhotoSerializer(photo, context={'request': request})

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_photo(self):
        request = factory.get(f'/api/photos/')
        response = PhotoView.as_view({'get': 'retrieve'})(request, 1001)  # noqa

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPhotoTest(TestCase):
    """ Test module for inserting a new photo """

    def setUp(self):
        self.valid_payload = {
            'session': '123456',
            'side': 'center',
            'colormap': 1,
        }
        self.invalid_payload = {
            'side': 'center',
            'colormap': 1,
        }

    def test_create_valid_photo(self):
        request = factory.post(
            f'/api/photos/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response = PhotoView.as_view({'post': 'create'})(request)  # noqa

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_photo(self):
        request = factory.post(
            f'/api/photos/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        response = PhotoView.as_view({'post': 'create'})(request)  # noqa

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePhotoTest(TestCase):
    """ Test module for deleting an existing photo record """

    def setUp(self):
        self.photo = Photo.objects.create(
            session='123456',
            side=Photo.SIDE_CENTER,
            temperature=285.3,
            error=False,
            image=_create_image_file(),
            colormap=Photo.COLORMAP_JET
        )

    def test_valid_delete_photo(self):
        request = factory.delete(f'/api/photos/')
        response = PhotoView.as_view({'delete': 'destroy'})(  # noqa
            request, self.photo.pk
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        request = factory.delete(f'/api/photos/')
        response = PhotoView.as_view({'delete': 'destroy'})(  # noqa
            request, 199
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
