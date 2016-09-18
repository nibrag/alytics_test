from django.db import models
from django.contrib.postgres.fields import JSONField


class Data(models.CharField):
    name = models.CharField(max_length=129)
    data = JSONField()


class ErrorLog(models.CharField):
    ts = models.DateTimeField()
    error = models.TextField()
