from django.db import models


class Callback(models.Model):
    query = models.TextField(blank=False, null=False)
    article = models.IntegerField(null=False)
    interval = models.DurationField(null=True)
    start_time = models.DateTimeField(null=True)
