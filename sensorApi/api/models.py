from django.db import models

# Create your models here.


class RegisteredSensors(models.Model):
    name = models.TextField(max_length=255, unique=True)
    display_name = models.TextField(max_length=255, default="not_set")
    description = models.TextField(max_length=1000, blank=True)


class LoggedData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    sensor = models.ForeignKey(RegisteredSensors, on_delete=models.SET_NULL, null=True)

    @property
    def sensor_id_string(self):
        return self.sensor.name
