from datetime import datetime

import pytz
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from tgbot import settings


class Job(models.Model):
    article = models.IntegerField(validators=(MinValueValidator(1),))
    query = models.TextField()
    user_id = models.PositiveIntegerField()
    interval = models.DurationField()
    start_time = models.DateTimeField(default=datetime.now)
    finished = models.BooleanField(default=False)

    @property
    def local_start_time(self):
        start_time = self.start_time.replace(tzinfo=None)
        timezone = pytz.timezone(settings.TIME_ZONE)
        return timezone.localize(start_time)


class Destination(models.Model):
    city = models.CharField(max_length=50)
    index = models.IntegerField()


class ProductPosition(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='productposition'
    )
    datetime = models.DateTimeField(default=datetime.now)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    page = models.IntegerField(validators=(
        MinValueValidator(1),
        MaxValueValidator(60)
    ), null=True)
    position = models.IntegerField(validators=(
        MinValueValidator(1),
        MaxValueValidator(100)
    ), null=True)

    @property
    def total_position(self):
        if self.position is not None and self.page is not None:
            return (self.page - 1) * 100 + self.position
        return None

    @property
    def local_datetime(self):
        local_datetime = self.datetime.replace(tzinfo=None)
        timezone = pytz.timezone(settings.TIME_ZONE)
        return timezone.localize(local_datetime)


class Storehouse(models.Model):
    name = models.CharField(max_length=50)
    index = models.PositiveIntegerField()
