from django.db import models

# Create your models here.


class RegisteredSensors(models.Model):
    name = models.TextField(max_length=255, unique=True)
    display_name = models.TextField(max_length=255, default="not_set")
    description = models.TextField(max_length=1000, blank=True)


class LoggedData(models.Model):
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    sensor = models.ForeignKey(RegisteredSensors, on_delete=models.SET_NULL, null=True)
