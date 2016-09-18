from django.db import models
from django.contrib.postgres.fields import JSONField


class Data(models.Model):
    name = models.CharField(max_length=129)
    data = JSONField()
    result = JSONField(default={}, null=True)


class ErrorLog(models.Model):
    ts = models.DateTimeField()
    msg = models.TextField()
    data = models.ForeignKey(Data)


class Calculate(models.Model):
    ts = models.DateTimeField()
    error = models.ForeignKey(ErrorLog, null=True, blank=True,
                              default=None)
    started = models.BooleanField(default=False)
