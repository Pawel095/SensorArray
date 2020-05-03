from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class IdentifySelf(APIView):
    def get(self, request):
        return Response("DataCollectorV1", status=status.HTTP_200_OK)


class LogData(APIView):
    def post(self, request, sensor_id):
        return Response(sensor_id, status=status.HTTP_200_OK)
