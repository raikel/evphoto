# Create your models here.
from django.db import models
import cv2 as cv


class TimeTrack(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Photo(TimeTrack):

    SIDE_LEFT = 'left'
    SIDE_RIGHT = 'right'
    SIDE_CENTER = 'center'

    SIDE_CHOICES = [
        (SIDE_LEFT, 'Left'),
        (SIDE_RIGHT, 'Right'),
        (SIDE_CENTER, 'Center'),
    ]

    COLORMAP_NONE = -1
    COLORMAP_HOT = cv.COLORMAP_HOT
    COLORMAP_JET = cv.COLORMAP_JET
    COLORMAP_COOL = cv.COLORMAP_COOL
    COLORMAP_HSV = cv.COLORMAP_HSV
    COLORMAP_SPRING = cv.COLORMAP_SPRING
    COLORMAP_BONE = cv.COLORMAP_BONE

    COLORMAP_CHOICES = [
        (COLORMAP_NONE, 'None'),
        (COLORMAP_HOT, 'Hot'),
        (COLORMAP_JET, 'Jet'),
        (COLORMAP_COOL, 'Cool'),
        (COLORMAP_HSV, 'HSV'),
        (COLORMAP_SPRING, 'Spring'),
        (COLORMAP_BONE, 'Bone'),
    ]

    session = models.CharField(
        max_length=255,
        help_text='The user session ID'
    )

    side = models.CharField(
        choices=SIDE_CHOICES,
        max_length=16,
        help_text='The side the photo was taken'
    )

    temperature = models.FloatField(
        help_text='The estimated center temperature'
    )

    error = models.BooleanField(
        default=False,
        help_text='Whether an error occurred or not during photo acquisition'
    )

    image = models.ImageField(
        help_text='The acquired image'
    )

    colormap = models.SmallIntegerField(
        default=COLORMAP_NONE,
        choices=COLORMAP_CHOICES,
        blank=True,
        help_text='Colormap name used when saving the image'
    )

    def __str__(self):
        return self.session
