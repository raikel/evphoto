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

    session = models.CharField(max_length=255)

    side = models.CharField(choices=SIDE_CHOICES, max_length=16)

    temperature = models.FloatField()

    error = models.BooleanField(default=False)

    image = models.ImageField()

    def __str__(self):
        return self.session
