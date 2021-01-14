# Create your models here.
from django.db import models


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

    def __str__(self):
        return self.session
