from django.db import models

# Create your models here.


class RegisteredSensors(models.Model):
    name = models.TextField(max_length=255)
    description = models.TextField(max_length=1000)


class LoggedData(models.Model):
    temperature = models.FloatField
    humidity = models.FloatField
    sensor = models.ForeignKey(RegisteredSensors, on_delete=models.SET_NULL)
