from rest_framework import serializers
from .models import LoggedData, RegisteredSensors


class LoggedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoggedData
        fields = "__all__"


class RegisteredSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredSensors
        fields = "__all__"
