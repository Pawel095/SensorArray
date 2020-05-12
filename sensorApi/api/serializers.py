from rest_framework import serializers
from .models import LoggedData, RegisteredSensors


class LoggedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoggedData
        fields = ["temperature", "humidity", "sensor"]


class RegisteredSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredSensors
        fields = "__all__"


class SingleSensorDataSerialiser(serializers.ModelSerializer):
    class Meta:
        model = LoggedData
        fields = ["temperature", "humidity", "timestamp"]


class AllSensorsDataSerialiser(serializers.ModelSerializer):
    class Meta:
        model = LoggedData
        fields = ["temperature", "humidity", "timestamp", "sensor_id_string"]
