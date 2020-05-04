from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LoggedData, RegisteredSensors
from .serializers import RegisteredSensorsSerializer, LoggedDataSerializer

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


class LogData(APIView):
    def post(self, request, sensor_id):
        data = request.data
        try:
            sensor = RegisteredSensors.objects.get()
        except RegisteredSensors.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data["sensor"] = sensor.pk
        ser = LoggedDataSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
