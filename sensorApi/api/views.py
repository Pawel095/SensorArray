from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LoggedData, RegisteredSensors
from .serializers import (
    RegisteredSensorsSerializer,
    LoggedDataSerializer,
    SingleSensorDataSerialiser,
    AllSensorsDataSerialiser,
)
from .utils.timestampDefaultValues import generate_timestamps

# Create your views here.


class IdentifySelf(APIView):
    def get(self, request):
        return Response("DataCollectorV1", status=status.HTTP_200_OK)


class RegisterSensor(APIView):
    def post(self, request):
        print(request.data)
        ser = RegisteredSensorsSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class DataPerSensor(APIView):
    def post(self, request, sensor_id):
        data = request.data
        try:
            sensor = RegisteredSensors.objects.get(name=sensor_id)
        except RegisteredSensors.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data["sensor"] = sensor.pk
        ser = LoggedDataSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, sensor_id):
        try:
            sensor = RegisteredSensors.objects.get(name=sensor_id)
        except RegisteredSensors.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        startDate, endDate = generate_timestamps(request)

        print(f"start: {startDate}, end: {endDate}")

        data = LoggedData.objects.filter(
            sensor=sensor, timestamp__gte=startDate, timestamp__lte=endDate
        )
        serializer = SingleSensorDataSerialiser(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllData(APIView):
    def get(self, request):

        startDate, endDate = generate_timestamps(request)
        print(f"start: {startDate}, end: {endDate}")

        data = LoggedData.objects.filter(
            timestamp__gte=startDate, timestamp__lte=endDate,
        )
        serializer = AllSensorsDataSerialiser(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
