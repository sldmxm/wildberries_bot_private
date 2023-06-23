from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Job(models.Model):
    article = models.IntegerField(validators=(MinValueValidator(1),))
    query = models.TextField()
    user_id = models.PositiveIntegerField()
    interval = models.DurationField()
    start_time = models.DateTimeField(default=datetime.now)
    finished = models.BooleanField(default=False)


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


class Storehouse(models.Model):
    name = models.CharField(max_length=50)
    index = models.PositiveIntegerField()
    